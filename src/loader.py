from pathlib import Path
import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet"}


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load CSV, Excel, JSON, or Parquet files into a DataFrame."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)
    suffix = source.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(source)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(source)
    if suffix == ".json":
        return pd.read_json(source)
    if suffix == ".parquet":
        return pd.read_parquet(source)
    raise ValueError(f"Unsupported input format: {suffix}. Use {sorted(SUPPORTED_EXTENSIONS)}")


def save_dataset(frame: pd.DataFrame, path: str | Path) -> Path:
    """Persist a frame according to output suffix."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix == ".parquet":
        frame.to_parquet(target, index=False)
    elif target.suffix == ".xlsx":
        frame.to_excel(target, index=False)
    else:
        frame.to_csv(target, index=False)
    return target
