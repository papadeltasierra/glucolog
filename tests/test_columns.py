"""Test the 'columns' command."""
from mock_database import (
    DATABASE,
    TABLES,
    NAME,
    COLUMNS,
    DB_TABLES,
)
from src.glucolog.glucolog import (
    PROC_NAME,
    main,
)

DATABASE_FILENAME = "{function}.sql3"


def test_columns_minimal(db, capsys):
    """Perform a minimal columns listing."""
    argv = [PROC_NAME, db, "list-columns", "--table", DB_TABLES[1]]
    main(argv)

    columns = DATABASE[TABLES][1][COLUMNS]
    captured = capsys.readouterr()
    assert captured.err == ""
    columns_found = captured.out.split("\n")
    # +3 for table name, separator, trailing LF
    assert len(columns_found) == (len(columns) + 3)
    assert ("'%s'" % DB_TABLES[1]) in columns_found[0]
    for column in columns:
        assert column in columns_found


def test_columns_bad_table_name(db, capsys, caplog):
    """Request the columns for a table that does not exit."""
    # Remember that because we are translating, we need to provide the table
    # name in English!
    argv = [PROC_NAME, db, "list-columns", "--table", "t_mancante"]
    rc = main(argv)
    assert rc == 2
    captured = capsys.readouterr()
    assert "Table 't_mancante' is not recognised." in captured.err


def test_columns_bad_translated_table_name(db, capsys, caplog):
    """Request the columns for a table that does not exit."""
    # Remember that because we are translating, we need to provide the table
    # name in English!
    argv = [PROC_NAME, "--xlat", "en", db, "list-columns", "--table", "t_missing"]
    rc = main(argv)
    assert rc == 2
    captured = capsys.readouterr()
    assert "Table 't_missing' is not recognised." in captured.err


def test_columns_translated(db, capsys, caplog):
    """Perform a minimal translated columns listing."""
    # Remember that because we are translating, we need to provide the table
    # name in English!
    assert DB_TABLES[1] == "t_parametri"
    assert DATABASE[TABLES][1][NAME] == "t_parametri"
    argv = [PROC_NAME, "--xlat", "en", db, "list-columns", "--table", "t_parameters"]
    main(argv)

    columns = DATABASE[TABLES][1][COLUMNS]
    captured = capsys.readouterr()
    # See test below of stderr.
    columns_found = captured.out.split("\n")
    # +3 for table name, separator, trailing LF
    assert len(columns_found) == (len(columns) + 3)

    # This tests that the table name is in the first line.
    print(columns_found[0])
    assert "'t_parameters'" in columns_found[0]

    # This tests that a column name for which there is no translation is rendered
    # in the original italian but a column that we know does have a translation
    # is also present.
    assert "sconosciuta" in columns_found
    assert "custom1_period" in columns_found

    # This tests that an ERROR log is created indicating that there is no
    # translation for this 'sconosciuta'.
    assert "Missing 'en' translation for column 'sconosciuta'" in captured.err
    assert "Missing 'en' translation for column 'sconosciuta'" in caplog.text
