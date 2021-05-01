"""Test the 'export' command."""
import re
from typing import Dict
from mock_database import (
    DATABASE,
    TABLES,
    COLUMNS,
    DATA,
    DB_TABLES,
    DB_EN_TABLES,
)
from src.glucolog.glucolog import (
    PROC_NAME,
    main,
    CSV_SEPARATOR,
)
from conftest import data_translation_validation


def export_basic_validation(output: str, table: Dict, name: str) -> None:
    """Basic export table validation."""
    lines = output.count("\n")
    # Expect table name and then columns + data
    assert lines == (2 + len(table[DATA]))

    assert re.search(r"^" + name + r"$", output, re.MULTILINE)

    # check all separators are present.
    separators = re.findall(r"^" + ",".join(CSV_SEPARATOR) + r"$", output, re.MULTILINE)
    assert len(separators) == 0


def test_export_minimal(db, csv, capsys):
    """Perform a minimal export."""
    args = [
        PROC_NAME,
        db,
        "export-table",
        "--table",
        DB_TABLES[1],
        "--format",
        "csv",
        csv,
    ]
    main(args)

    # We now need to perform some checking of the output file.
    with open(csv, "r") as source:
        output = source.read()

    export_basic_validation(output, DATABASE[TABLES][1], DB_TABLES[1])


def test_export_excel(db, excel, capsys):
    """Perform a minimal export to Excel listing."""
    args = [
        PROC_NAME,
        db,
        "export-table",
        "--table",
        DB_TABLES[1],
        "--format",
        "excel",
        excel,
    ]
    main(args)

    # We do not bother checking the output as we would have to use openpyxl to
    # do that and then we're using the same interface to write as to test.
    pass


def test_export_bad_column_name(db, csv, capsys):
    """Request data for a table with a column do not exist."""
    assert DB_TABLES[2] == "t_risultati"
    columns = DATABASE[TABLES][2][COLUMNS][5:9]
    columns.append("t_perduta")
    columns_str = ",".join(columns)
    argv = [
        PROC_NAME,
        db,
        "export-table",
        "--columns",
        columns_str,
        "--table",
        "t_risultati",
        "--format",
        "csv",
        csv,
    ]
    rc = main(argv)
    assert rc == 2
    captured = capsys.readouterr()
    print(captured.err)
    assert "columns are not recognised." in captured.err


def test_export_bad_translated_column_name(db, csv, capsys):
    """Request data for a table with a column that does not exit."""
    # Remember that because we are translating, we need to provide the table
    # name in English!
    assert DB_TABLES[2] == "t_risultati"
    columns = DATABASE[TABLES][2][COLUMNS][5:9]
    columns.append("t_lost")
    columns_str = ",".join(columns)
    argv = [
        PROC_NAME,
        "--xlat",
        "en",
        db,
        "export-table",
        "--columns",
        columns_str,
        "--table",
        "t_results",
        "--format",
        "csv",
        csv,
    ]
    rc = main(argv)
    assert rc == 2
    captured = capsys.readouterr()
    assert "Column 't_lost' is not recognised." in captured.err


def test_export_specific_columns(db, csv, capsys):
    """Perform a minimal export with specific columns."""
    # Remember that because we are translating, we need to provide the table
    # name in English!
    assert DB_TABLES[2] == "t_risultati"
    assert len(DATABASE[TABLES][2][COLUMNS]) > 10
    columns = ",".join(DATABASE[TABLES][2][COLUMNS][5:9])
    args = [
        PROC_NAME,
        "--xlat",
        "en",
        db,
        "export-table",
        "--table",
        "t_results",
        "--columns",
        columns,
        "--format",
        "csv",
        csv,
    ]
    main(args)

    # We now need to perform some checking of the output file.
    with open(csv, "r") as source:
        output = source.read()

    export_basic_validation(output, DATABASE[TABLES][2], DB_EN_TABLES[2])


def test_export_translated(db, csv, capsys):
    """Perform an export with translated columns and data."""
    # Remember that because we are translating, we need to provide the table
    # name in English!
    assert DB_TABLES[2] == "t_risultati"
    args = [
        PROC_NAME,
        "--xlat",
        "en",
        db,
        "export-table",
        "--table",
        DB_EN_TABLES[2],
        "--format",
        "csv",
        csv,
    ]
    main(args)

    # We now need to perform some checking of the output file.
    with open(csv, "r") as source:
        output = source.read()

    export_basic_validation(output, DATABASE[TABLES][2], DB_EN_TABLES[2])
    data_translation_validation(output)
