import pandas as pd
from src.cleaner import clean, infer_types
from src.models import CleaningOptions
from src.validator import validate


def test_clean_removes_duplicates_and_fills_missing():
    source=pd.DataFrame({"Revenue":[10,None,10],"Name":[" A ","B"," A "]})
    output, changes=clean(source, CleaningOptions())
    assert len(output)==2
    assert output.isna().sum().sum()==0
    assert changes["duplicates_removed"]==1


def test_validation_reports_empty_dataset():
    result=validate(pd.DataFrame())
    assert not result["valid"]


def test_type_inference_detects_currency():
    assert infer_types(pd.DataFrame({"Revenue":[1,2]}))["Revenue"] == "currency"
