import pytest
from fastapi.testclient import TestClient
import pandas as pd
import numpy as np
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'numeric': [1, 2, 3, 4, 5],
        'categorical': ['A', 'B', 'A', 'B', 'C'],
        'missing': [1, np.nan, 3, np.nan, 5],
        'target': [0, 1, 0, 1, 0]
    })
