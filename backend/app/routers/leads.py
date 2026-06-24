"""Lead import and listing API routes."""

import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.repositories import LeadRepository
from app.schemas.lead import LeadImportResult, LeadOutput
from app.services.lead_import_service import LeadImportService

router = APIRouter(prefix="/leads", tags=["leads"])
CSV_CONTENT_TYPES = {"text/csv", "application/csv", "application/vnd.ms-excel"}


class LeadImportRequest(BaseModel):
    """Request body for importing CSV lead data."""

    csv_content: str = Field(min_length=1)
    source_name: str | None = None


@router.post("/import", response_model=LeadImportResult)
async def import_leads(
    request: Request,
    db: Annotated[Session, Depends(get_db_session)],
) -> LeadImportResult:
    """Validate, transform and persist leads from uploaded CSV content."""
    csv_content, source_name = await _read_import_request(request)
    service = LeadImportService()
    return service.import_csv_content(
        db,
        csv_content,
        source_name=source_name,
    )


@router.get("", response_model=list[LeadOutput])
def list_leads(
    db: Annotated[Session, Depends(get_db_session)],
    limit: int = 100,
    offset: int = 0,
) -> list[LeadOutput]:
    """Return persisted leads."""
    repository = LeadRepository()
    return list(repository.list_leads(db, limit=limit, offset=offset))


async def _read_import_request(request: Request) -> tuple[bytes | str, str | None]:
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("multipart/form-data"):
        return _extract_multipart_csv(await request.body(), content_type)
    if content_type.startswith("application/json"):
        try:
            payload = LeadImportRequest.model_validate(await request.json())
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exc.errors(),
            ) from exc
        return payload.csv_content, payload.source_name
    if content_type.startswith("text/csv") or content_type.startswith("application/csv"):
        return await request.body(), None
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="Upload a CSV file as multipart/form-data or send text/csv content.",
    )


def _extract_multipart_csv(body: bytes, content_type: str) -> tuple[bytes, str | None]:
    boundary = _extract_boundary(content_type)
    if boundary is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multipart request is missing a boundary.",
        )

    file_content: bytes | None = None
    filename: str | None = None
    form_source_name: str | None = None

    for part in _iter_multipart_parts(body, boundary):
        headers, content = _split_part_headers(part)
        disposition = headers.get("content-disposition", "")
        field_name = _extract_disposition_value(disposition, "name")
        if field_name == "source_name":
            form_source_name = content.decode("utf-8").strip() or None
            continue
        if field_name != "file":
            continue

        filename = _extract_disposition_value(disposition, "filename")
        part_content_type = headers.get("content-type")
        _validate_uploaded_csv(filename, part_content_type)
        file_content = content

    if file_content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multipart request must include a CSV file field named 'file'.",
        )
    return file_content, form_source_name or filename


def _extract_boundary(content_type: str) -> str | None:
    for part in content_type.split(";"):
        item = part.strip()
        if item.startswith("boundary="):
            return item.removeprefix("boundary=").strip('"')
    return None


def _iter_multipart_parts(body: bytes, boundary: str) -> list[bytes]:
    marker = f"--{boundary}".encode()
    parts = []
    for part in body.split(marker):
        stripped = part.strip(b"\r\n")
        if not stripped or stripped == b"--":
            continue
        if stripped.endswith(b"--"):
            stripped = stripped[:-2].rstrip(b"\r\n")
        parts.append(stripped)
    return parts


def _split_part_headers(part: bytes) -> tuple[dict[str, str], bytes]:
    header_blob, separator, content = part.partition(b"\r\n\r\n")
    if not separator:
        return {}, b""
    headers: dict[str, str] = {}
    for raw_header in header_blob.decode("latin-1").split("\r\n"):
        name, _, value = raw_header.partition(":")
        if name:
            headers[name.strip().lower()] = value.strip()
    if content.endswith(b"\r\n"):
        content = content[:-2]
    return headers, content


def _extract_disposition_value(disposition: str, key: str) -> str | None:
    match = re.search(rf'{key}="([^"]*)"', disposition)
    if match:
        return match.group(1)
    return None


def _validate_uploaded_csv(filename: str | None, content_type: str | None) -> None:
    if filename and not filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded lead import file must use a .csv filename.",
        )
    normalized_content_type = content_type.split(";", maxsplit=1)[0].strip().lower()
    if normalized_content_type and normalized_content_type not in CSV_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded lead import file must be CSV content.",
        )
