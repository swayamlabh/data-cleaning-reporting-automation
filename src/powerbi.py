from pathlib import Path
import pandas as pd


def export_star_schema(frame: pd.DataFrame, output_dir: str | Path) -> dict[str, str]:
    """Export a simple fact and dimension layout consumable by Power BI."""
    root=Path(output_dir); root.mkdir(parents=True, exist_ok=True)
    categorical=frame.select_dtypes(exclude="number").columns.tolist(); outputs={}
    fact=frame.copy()
    for col in categorical:
        dim=frame[[col]].drop_duplicates().reset_index(drop=True); dim[f"{col}_key"]=dim.index+1
        path=root/f"dim_{col}.csv"; dim.to_csv(path,index=False); outputs[f"dim_{col}"]=str(path)
        fact=fact.merge(dim,on=col,how="left").drop(columns=[col])
    path=root/"fact_data.csv"; fact.to_csv(path,index=False); outputs["fact"]=str(path)
    return outputs
