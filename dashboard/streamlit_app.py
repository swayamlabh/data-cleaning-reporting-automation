import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
import streamlit as st
from src.automation import run_pipeline
from src.models import CleaningOptions

st.set_page_config(page_title="Data Automation", page_icon="ð", layout="wide")
st.title("ð AI Data Cleaning & Reporting")
st.caption("Upload a dataset to clean it, explore KPIs, and download executive-ready outputs.")
file = st.file_uploader("Dataset", type=["csv", "xlsx", "xls", "json", "parquet"])
with st.sidebar:
    strategy=st.selectbox("Missing values", ["auto","mean","median","mode","knn","drop"])
    remove=st.toggle("Remove outliers")
if file and st.button("Run automation", type="primary"):
    raw=Path("data/raw"); raw.mkdir(parents=True,exist_ok=True); path=raw/file.name; path.write_bytes(file.getbuffer())
    with st.spinner("Profiling, cleaning, analyzing, and writing reports..."):
        result=run_pipeline(path, CleaningOptions(missing_strategy=strategy, remove_outliers=remove))
    a,b=st.columns(2); a.metric("Data quality", f"{result.quality_score}/100"); b.metric("Rows", result.profile["shape"]["rows"])
    st.subheader("AI executive summary"); st.write(result.insights)
    st.subheader("Downloads")
    for label,path in result.report_paths.items():
        if Path(path).is_file(): st.download_button(label, Path(path).read_bytes(), file_name=Path(path).name)
