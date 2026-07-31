import pandas as pd


def validate(frame: pd.DataFrame) -> dict:
    """Run deterministic checks and a lightweight Pandera contract when installed."""
    issues: list[dict] = []
    if frame.empty:
        issues.append({"severity": "error", "message": "Dataset contains no rows."})
    duplicate_count = int(frame.duplicated().sum())
    if duplicate_count:
        issues.append({"severity": "warning", "message": f"{duplicate_count} exact duplicate rows."})
    for column in frame.columns:
        if not str(column).strip():
            issues.append({"severity": "error", "message": "A column has an empty name."})
        nulls = int(frame[column].isna().sum())
        if nulls:
            issues.append({"severity": "warning", "column": str(column), "message": f"{nulls} missing values."})
    pandera_valid = True
    try:
        import pandera.pandas as pa
        schema = pa.DataFrameSchema({str(column): pa.Column(dtype, nullable=True) for column, dtype in frame.dtypes.items()}, strict=True)
        schema.validate(frame, lazy=True)
    except ImportError:
        pass
    except Exception as exc:
        pandera_valid = False
        issues.append({"severity": "error", "message": f"Pandera schema validation failed: {exc}"})
    valid = not any(item["severity"] == "error" for item in issues)
    return {"valid": valid, "pandera_valid": pandera_valid, "issues": issues, "rows": len(frame), "columns": len(frame.columns)}
