import pandas as pd
from sklearn.preprocessing import StandardScaler


def engineer_features(frame: pd.DataFrame, scale_numeric: bool = False) -> pd.DataFrame:
    """Add calendar features and optional normalized numeric values."""
    result = frame.copy()
    for column in result.columns:
        if pd.api.types.is_datetime64_any_dtype(result[column]):
            result[f"{column}_year"] = result[column].dt.year
            result[f"{column}_month"] = result[column].dt.month
            result[f"{column}_weekday"] = result[column].dt.dayofweek
    if scale_numeric:
        cols = result.select_dtypes(include="number").columns
        if len(cols): result[cols] = StandardScaler().fit_transform(result[cols])
    return result
