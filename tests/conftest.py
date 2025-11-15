"""
Test configuration and fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_data():
    """Fixture for sample election data."""
    from src.data.make_dataset import generate_synthetic_election_data
    return generate_synthetic_election_data(n_samples=100, random_state=42)


@pytest.fixture
def temp_model_path(tmp_path):
    """Fixture for temporary model path."""
    return tmp_path / "test_model.pkl"


@pytest.fixture
def config():
    """Fixture for configuration."""
    from src.utils.config import Config
    return Config
