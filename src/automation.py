from pathlib import Path
from loguru import logger
from .loader import load_dataset, save_dataset
from .models import CleaningOptions, PipelineResult
from .validator import validate
from .cleaner import clean
from .transformer import engineer_features
from .analyzer import profile
from .ai_summary import generate_insights
from .visualization import build_charts
from .report_generator import generate_reports
from .powerbi import export_star_schema


def run_pipeline(input_path: str | Path, options: CleaningOptions | None = None, output_dir: str | Path = "reports") -> PipelineResult:
    """Execute the end-to-end data cleaning and reporting workflow."""
    options = options or CleaningOptions(); logger.info("Loading dataset: {}", input_path)
    raw=load_dataset(input_path); validation=validate(raw); cleaned, changes=clean(raw, options); enriched=engineer_features(cleaned)
    data_path=save_dataset(enriched, Path("data/cleaned") / f"{Path(input_path).stem}_cleaned.csv")
    analysis=profile(enriched); analysis["validation"]=validation; analysis["changes"]=changes
    charts=build_charts(enriched, Path(output_dir)/"html"/"charts"); insights=generate_insights(analysis, changes)
    reports=generate_reports(enriched, analysis, insights, output_dir); reports["power_bi"] = str(Path(output_dir)/"power_bi")
    export_star_schema(enriched, reports["power_bi"]); reports.update({f"chart_{key}": value for key,value in charts.items()})
    return PipelineResult(cleaned_path=str(data_path),report_paths=reports,quality_score=analysis["quality_score"],insights=insights,profile=analysis)
