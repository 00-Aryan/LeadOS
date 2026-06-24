"""Schemas for dashboard-ready BI export datasets."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

BIExportCellValue = str | int | float | bool | None
BIExportColumnType = Literal["string", "integer", "number", "boolean", "datetime"]
BIExportFormat = Literal["csv"]


class BIExportColumn(BaseModel):
    """One flat BI export table column."""

    name: str
    data_type: BIExportColumnType = "string"


class BIExportTable(BaseModel):
    """One dashboard-ready BI export table."""

    name: str
    source_report: str
    columns: list[BIExportColumn] = Field(default_factory=list)
    rows: list[dict[str, BIExportCellValue]] = Field(default_factory=list)
    row_count: int = Field(ge=0)
    generated_at: datetime


class BIExportDataset(BaseModel):
    """Collection of BI export tables built from SQL-backed reports."""

    name: str
    tables: list[BIExportTable] = Field(default_factory=list)
    table_count: int = Field(ge=0)
    generated_at: datetime
