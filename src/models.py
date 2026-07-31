from typing import Any, Literal
from pydantic import BaseModel, Field


class CleaningOptions(BaseModel):
    missing_strategy: Literal["mean", "median", "mode", "knn", "drop", "auto"] = "auto"
    duplicate_mode: Literal["exact", "fuzzy", "none"] = "exact"
    outlier_method: Literal["iqr", "zscore", "isolation_forest", "none"] = "iqr"
    remove_outliers: bool = False
    fuzzy_threshold: float = Field(default=0.93, ge=0.5, le=1.0)


class PipelineResult(BaseModel):
    cleaned_path: str
    report_paths: dict[str, str]
    quality_score: float
    insights: str
    profile: dict[str, Any]
