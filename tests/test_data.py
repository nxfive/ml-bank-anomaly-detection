import os
import tempfile

import pandas as pd
from src.data import data
from src.data.data import data_transform


def test_read_data_mock(monkeypatch):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp_file.write(b"col1,col2\n1,2\n3,4\n")
    tmp_file.close()

    monkeypatch.setattr(data, "read_data", lambda: pd.read_csv(tmp_file.name))

    df = data.read_data()
    assert not df.empty
    assert "col1" in df.columns

    os.remove(tmp_file.name)


def test_data_transform_sets_datetime_index(sample_df):
    df = data_transform(sample_df)
    assert df.index.dtype == "datetime64[ns]"
    assert df.index.is_monotonic_increasing
