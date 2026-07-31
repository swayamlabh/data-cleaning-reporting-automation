from pathlib import Path
import typer
from rich import print
from src.automation import run_pipeline
from src.models import CleaningOptions

app=typer.Typer(help="AI-powered data cleaning and reporting automation.")

@app.command()
def clean(input_file: Path, strategy: str = "auto"):
    result=run_pipeline(input_file, CleaningOptions(missing_strategy=strategy)); print(f"[green]Cleaned:[/] {result.cleaned_path}")

@app.command()
def analyze(input_file: Path):
    result=run_pipeline(input_file); print(result.profile)

@app.command()
def report(input_file: Path):
    result=run_pipeline(input_file); print(result.report_paths)

@app.command()
def dashboard():
    import subprocess; subprocess.run(["streamlit","run","dashboard/streamlit_app.py"], check=True)

if __name__ == "__main__": app()
