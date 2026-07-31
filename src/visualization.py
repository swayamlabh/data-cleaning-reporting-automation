from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


def build_charts(frame: pd.DataFrame, output_dir: str | Path) -> dict[str, str]:
    """Create portable Plotly HTML assets for the report/dashboard."""
    target = Path(output_dir); target.mkdir(parents=True, exist_ok=True); charts = {}
    missing = frame.isna().sum().reset_index(name="missing").rename(columns={"index": "column"})
    path = target / "missing_values.html"; px.bar(missing, x="column", y="missing", title="Missing Values").write_html(path); charts["missing"] = str(path)
    numeric = frame.select_dtypes(include="number")
    if not numeric.empty:
        path = target / "correlation.html"; fig = ff.create_annotated_heatmap(z=numeric.corr().fillna(0).round(2).values, x=numeric.columns.tolist(), y=numeric.columns.tolist(), colorscale="Viridis"); fig.update_layout(title="Correlation Matrix"); fig.write_html(path); charts["correlation"] = str(path)
        for column in numeric.columns[:3]:
            path = target / f"distribution_{column}.html"; px.histogram(frame, x=column, title=f"Distribution: {column}").write_html(path); charts[f"distribution_{column}"] = str(path)
    return charts
