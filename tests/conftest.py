"""Fixtures to create, and discard, files for testing."""
import os
import pytest
from mock_database import mock_database


@pytest.fixture
def db(tmp_path, request):
    """Create an input SQLite3 DB filename for the specific test."""
    db_filename = os.path.join(tmp_path, "%s.sql3" % request.function.__name__)
    mock_database(db_filename)
    yield db_filename
    os.remove(db_filename)


@pytest.fixture
def csv(tmp_path, request):
    """Create an output CSV filename for the specific test."""
    csv_filename = os.path.join(tmp_path, "%s.csv" % request.function.__name__)
    yield csv_filename
    os.remove(csv_filename)


@pytest.fixture
def excel(tmp_path, request):
    """Create an output Excel filename for the specific test."""
    excel_filename = os.path.join(tmp_path, "%s.xlsx" % request.function.__name__)
    yield excel_filename
    os.remove(excel_filename)


@pytest.fixture
def logfile(tmp_path, request):
    """Create a logfile for the specific test."""
    log_filename = os.path.join(tmp_path, "%s.log" % request.function.__name__)
    yield log_filename
    os.remove(log_filename)


def data_translation_validation(output):
    """Confirm translation took place."""
    # Assert translation word has been replaced.
    assert "primo_pomeriggio" not in output
    assert "early_afternoon" in output

    # "mezzanotte" is not a word in the translation table.
    assert "mezzanotte" in output
