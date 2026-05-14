import pytest
from src.api_client import get_daily_tip

def test_api_connection():
    tip = get_daily_tip()
    assert isinstance(tip, str)
    assert len(tip) > 0