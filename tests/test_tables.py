"""Test the 'tables' command."""
import os
import logging
import pytest
from mock_database import DB_TABLES, DB_EN_TABLES
from src.glucolog.glucolog import PROC_NAME, main

log = logging.getLogger()


@pytest.fixture
def logfile(tmp_path, request):
    log_filename = os.path.join(tmp_path, "%s.log" % request.function.__name__)
    yield log_filename
    os.remove(log_filename)


def test_tables_minimal(logfile, db, capsys):
    """Perform a minimal tables listing."""
    # Note that running with maximal logging exposed a bug so leave here to
    # trap any recurrence of the issue.
    argv = [
        PROC_NAME,
        "--debug",
        "--debug",
        "--verbose",
        "--verbose",
        "--logfile",
        logfile,
        db,
        "list-tables",
    ]
    main(argv)

    # stderr output contains the debug level logging enabled by requesting
    # verbose twice.
    captured = capsys.readouterr()
    assert "Exit: } main" in captured.err

    # We will want to discard the logging file at the end of the test so
    # shutdown logging.
    logging.shutdown()

    tables_found = captured.out.split()
    for table in DB_TABLES:
        assert table in tables_found


def test_tables_translated(db, capsys, caplog):
    """Perform a minimal tables listing."""
    # Note that one of the table names if faked and is not one that can be
    # translated.  This will test the "no matching table" translation code.
    argv = [PROC_NAME, "--xlat", "en", db, "list-tables"]
    main(argv)

    captured = capsys.readouterr()
    # stderr test is below.
    tables_found = captured.out.split()
    for table in DB_EN_TABLES:
        assert table in tables_found

    # This tests that a table name for which there is no translation is rendered
    # in the original italian.
    assert "t_nascosto" in tables_found

    # This tests that an ERROR log is created indicating that there is no
    # translation for this 'sconosciuta'.
    assert "Missing 'en' translation for table 't_nascosto'" in captured.err
    assert "Missing 'en' translation for table 't_nascosto'" in caplog.text
