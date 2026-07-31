from difflib import SequenceMatcher
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest
from .models import CleaningOptions


def infer_types(frame: pd.DataFrame) -> dict[str, str]:
    """Infer useful business types without mutating the input."""
    inferred = {}
    for name, series in frame.items():
        text = str(name).lower()
        if pd.api.types.is_bool_dtype(series): inferred[str(name)] = "boolean"
        elif pd.api.types.is_numeric_dtype(series): inferred[str(name)] = "currency" if any(x in text for x in ["price", "cost", "revenue", "amount"]) else "numeric"
        elif pd.api.types.is_datetime64_any_dtype(series): inferred[str(name)] = "date"
        elif series.nunique(dropna=True) <= max(20, len(series) * .05): inferred[str(name)] = "category"
        else: inferred[str(name)] = "text"
    return inferred


def _fuzzy_deduplicate(frame: pd.DataFrame, threshold: float) -> pd.DataFrame:
    text_columns = frame.select_dtypes(include="object").columns.tolist()
    if not text_columns or len(frame) > 5000:
        return frame.drop_duplicates()
    keep, seen = [], []
    for idx, row in frame.iterrows():
        signature = " | ".join(str(row[col]).strip().lower() for col in text_columns)
        if not any(SequenceMatcher(None, signature, prior).ratio() >= threshold for prior in seen):
            keep.append(idx); seen.append(signature)
    return frame.loc[keep].copy()


def clean(frame: pd.DataFrame, options: CleaningOptions) -> tuple[pd.DataFrame, dict]:
    """Clean data and return a transparent change log."""
    result = frame.copy(); changes: dict[str, object] = {"initial_rows": len(frame)}
    result.columns = [str(c).strip().replace(" ", "_").lower() for c in result.columns]
    for column in result.select_dtypes(include="object"):
        result[column] = result[column].astype("string").str.strip().replace({"": pd.NA, "null": pd.NA, "None": pd.NA})
    before = len(result)
    if options.duplicate_mode == "exact": result = result.drop_duplicates()
    elif options.duplicate_mode == "fuzzy": result = _fuzzy_deduplicate(result, options.fuzzy_threshold)
    changes["duplicates_removed"] = before - len(result)
    numeric = result.select_dtypes(include=np.number).columns.tolist()
    strategy = options.missing_strategy
    if strategy == "knn" and numeric:
        result[numeric] = KNNImputer().fit_transform(result[numeric])
    else:
        for col in result.columns:
            if not result[col].isna().any(): continue
            if strategy == "drop": result = result.dropna(subset=[col]); continue
            value = (result[col].median() if strategy in {"median", "auto"} and col in numeric else result[col].mean() if strategy == "mean" and col in numeric else result[col].mode(dropna=True).iloc[0] if not result[col].mode(dropna=True).empty else "Unknown")
            result[col] = result[col].fillna(value)
    changes["missing_after"] = int(result.isna().sum().sum())
    if options.remove_outliers and numeric and options.outlier_method != "none":
        if options.outlier_method == "isolation_forest":
            mask = IsolationForest(contamination="auto", random_state=42).fit_predict(result[numeric].fillna(0)) == 1
        else:
            values = result[numeric]; mask = pd.Series(True, index=result.index)
            for col in numeric:
                if options.outlier_method == "zscore":
                    std = values[col].std(); mask &= True if not std else ((values[col]-values[col].mean()).abs()/std < 3)
                else:
                    q1,q3=values[col].quantile([.25,.75]); iqr=q3-q1; mask &= values[col].between(q1-1.5*iqr,q3+1.5*iqr)
        changes["outliers_removed"] = int((~mask).sum()); result = result.loc[mask].copy()
    changes["final_rows"] = len(result); changes["types"] = infer_types(result)
    return result, changes
