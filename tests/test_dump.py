"""Test the 'dump' command."""
import re
from mock_database import (
    DATABASE,
    TABLES,
    NAME,
    DATA,
    EN_NAME,
)
from src.glucolog.glucolog import (
    PROC_NAME,
    main,
    CSV_SEPARATOR,
)
from conftest import data_translation_validation

DATABASE_FILENAME = "{function}.sql3"


def dump_basic_validation(output: str, name: str) -> None:
    """Basic validation of the rows present."""
    num_tables = len(DATABASE[TABLES])

    data_lines = 0
    for table in DATABASE[TABLES]:
        if DATA in table:
            data_lines = data_lines + len(table[DATA])

    lines = output.count("\n")
    # Each table consists of separator, name, columns except for first table
    # which does not start with a separator.
    assert lines == (num_tables * 3) - 1 + data_lines

    # Check all tables are present.
    for table in DATABASE[TABLES]:
        assert re.search(r"^" + table[name] + r"$", output, re.MULTILINE)

    # check all separators are present.
    separators = re.findall(r"^" + ",".join(CSV_SEPARATOR) + r"$", output, re.MULTILINE)
    assert len(separators) == (len(DATABASE[TABLES]) - 1)


def test_dump_minimal(db, csv, capsys):
    """Perform a minimal dump."""
    args = [PROC_NAME, db, "dump-db", "--format", "csv", csv]
    main(args)

    # We now need to perform some checking of the output file.
    with open(csv, "r") as source:
        output = source.read()

    dump_basic_validation(output, NAME)


def test_dump_excel(db, excel, capsys):
    """Perform a minimal dump to Excel."""
    args = [PROC_NAME, db, "dump-db", "--format", "excel", excel]
    main(args)


def test_dump_translated(db, csv, capsys):
    """Perform an dump with translated tables, columns and data."""
    args = [PROC_NAME, "--xlat", "en", db, "dump-db", "--format", "csv", csv]
    main(args)

    # We now need to perform some checking of the output file.
    with open(csv, "r") as source:
        output = source.read()

    dump_basic_validation(output, EN_NAME)
    data_translation_validation(output)
    assert "primo_pomeriggio" not in output
    assert "mezzanotte" in output
