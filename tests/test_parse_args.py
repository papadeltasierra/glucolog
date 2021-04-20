import logging
import pytest
from src.glucolog.glucolog import parse_args, PROC_NAME

log = logging.getLogger()


def test_pa_no_args(capsys):
    """Test no arguments."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME])
    assert ee.type == SystemExit
    assert ee.value.code == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: database" in captured.err


def test_pa_help(capsys):
    """Test printing help."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "-h"])

    assert ee.type == SystemExit
    assert ee.value.code == 0

    captured = capsys.readouterr()
    # !!PDS: Why not captured?
    # A peak picking and fitting program for EI TOFMS data
    assert "usage:" in captured.out
    assert captured.err == ""


def test_pa_no_database(capsys):
    """Test missing database."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "-vv", "-d", "-l", "logfile.dat"])
    assert ee.type == SystemExit
    assert ee.value.code == 2

    captured = capsys.readouterr()
    # !!PDS: Why not captured?
    # A peak picking and fitting program for EI TOFMS data
    assert captured.out == ""
    assert "required: database" in captured.err


def test_pa_no_command(capsys):
    """Test missing command."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "-vv", "-d", "-l", "logfile.dat", "database.dat"])
    assert ee.type == SystemExit
    assert ee.value.code == 2

    # Note when we flag an error, it appears in stderr but Argparse flags
    # "usage" errors in stdout!
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "No database command" in captured.err


def test_pa_tables_minimal(capsys):
    """Test minimal short options."""
    args = parse_args([PROC_NAME, "input.dat", "list-tables"])

    assert args.verbose == 0
    assert args.debug == 0
    assert args.database == "input.dat"
    assert args.logfile == "glucolog.log"
    assert args.cmd == "list-tables"
    assert "format" not in args
    assert args.xlat is None
    assert args.xlat_to == {}
    assert args.xlat_from == {}


def test_pa_tables_short(capsys):
    """Test maximal short options."""
    args = parse_args(
        [PROC_NAME, "-vv", "-d", "-x", "it", "-l", "logfile.dat", "input.dat", "list-tables"]
    )

    assert args.verbose == 2
    assert args.debug == 1
    assert args.database == "input.dat"
    assert args.logfile == "logfile.dat"
    assert args.cmd == "list-tables"
    assert "format" not in args
    assert args.xlat == "it"
    assert "columns" in args.xlat_to
    assert "data" in args.xlat_from


def test_pa_tables_long(capsys):
    """Test maximal long options."""
    args = parse_args(
        [
            PROC_NAME,
            "--verbose",
            "--debug",
            "--debug",
            "--logfile",
            "logfile.dat",
            "--xlat",
            "en",
            "database.dat",
            "list-tables",
        ]
    )

    assert args.verbose == 1
    assert args.debug == 2
    assert args.logfile == "logfile.dat"
    assert args.database == "database.dat"
    assert args.cmd == "list-tables"
    assert "format" not in args
    assert args.xlat == "en"
    assert "tables" in args.xlat_to
    assert "columns" in args.xlat_from


def test_pa_columns_missing_table(capsys):
    """Test minimal short options."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "database.dat", "list-columns"])
    assert ee.type == SystemExit
    assert ee.value.code == 2

    # Note when we flag an error, it appears in stderr but Argparse flags
    # "usage" errors in stdout!
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: -t/--table" in captured.err


def test_pa_columns_minimal(capsys):
    """Test minimal short options."""
    args = parse_args([PROC_NAME, "database.dat", "list-columns", "-t", "t_something"])

    assert args.verbose == 0
    assert args.debug == 0
    assert args.database == "database.dat"
    assert args.logfile == "glucolog.log"
    assert args.cmd == "list-columns"
    assert args.table == "t_something"
    assert "format" not in args
    assert args.xlat is None
    assert args.xlat_to == {}
    assert args.xlat_from == {}


def test_pa_columns_short(capsys):
    """Test maximal short options."""
    args = parse_args(
        [
            PROC_NAME,
            "-vv",
            "-d",
            "-l",
            "logfile.log",
            "-x",
            "en",
            "database.dat",
            "list-columns",
            "-t",
            "t_something",
        ]
    )

    assert args.verbose == 2
    assert args.debug == 1
    assert args.database == "database.dat"
    assert args.logfile == "logfile.log"
    assert args.cmd == "list-columns"
    assert args.table == "t_something"
    assert "format" not in args
    assert args.xlat == "en"
    assert "tables" in args.xlat_to
    assert "columns" in args.xlat_from


def test_pa_columns_long(capsys):
    """Test maximal long options."""
    args = parse_args(
        [
            PROC_NAME,
            "--verbose",
            "--debug",
            "--debug",
            "--xlat",
            "it",
            "--logfile",
            "logfile.dat",
            "database.dat",
            "list-columns",
            "--table",
            "t_something",
        ]
    )

    assert args.verbose == 1
    assert args.debug == 2
    assert args.logfile == "logfile.dat"
    assert args.database == "database.dat"
    assert args.cmd == "list-columns"
    assert args.table == "t_something"
    assert "format" not in args
    assert args.xlat == "it"
    assert "data" in args.xlat_to
    assert "columns" in args.xlat_from


def test_pa_export_missing_table(capsys):
    """Test export with missing output file."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "database.dat", "export-table", "-f", "excel", "output.dat"])
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: -t/--table" in captured.err


def test_pa_export_missing_output(capsys):
    """Test export with missing output file."""
    with pytest.raises(SystemExit) as ee:
        parse_args(
            [PROC_NAME, "database.dat", "export-table", "-t", "t_something", "-f", "csv"]
        )
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: output" in captured.err


def test_pa_export_missing_format(capsys):
    """Test minimal short options."""
    with pytest.raises(SystemExit) as ee:
        parse_args(
            [PROC_NAME, "database.dat", "export-table", "-t", "t_something", "output.dat"]
        )
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: -f/--format" in captured.err


def test_pa_export_filename_not_csv(capsys):
    """Test minimal short options."""
    with pytest.raises(SystemExit) as ee:
        parse_args(
            [
                PROC_NAME,
                "database.dat",
                "export-table",
                "-t",
                "t_something",
                "-f",
                "csv",
                "output.dat",
            ]
        )
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "does not end in '.csv'" in captured.err


def test_pa_export_filename_not_excel(capsys):
    """Test minimal short options."""
    with pytest.raises(SystemExit) as ee:
        parse_args(
            [
                PROC_NAME,
                "database.dat",
                "export-table",
                "-t",
                "t_something",
                "-f",
                "excel",
                "output.dat",
            ]
        )
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "does not end in '.xlsx'" in captured.err


def test_pa_export_minimal(capsys):
    """Test minimal."""
    args = parse_args(
        [
            PROC_NAME,
            "database.dat",
            "export-table",
            "-t",
            "t_something",
            "-f",
            "excel",
            "output.xlsx",
        ]
    )

    assert args.verbose == 0
    assert args.debug == 0
    assert args.database == "database.dat"
    assert args.logfile == "glucolog.log"
    assert args.cmd == "export-table"
    assert args.table == "t_something"
    assert args.columns is None
    assert args.format == "excel"
    assert args.xlat is None
    assert args.output == "output.xlsx"


def test_pa_export_short(capsys):
    """Test maximal short options."""
    args = parse_args(
        [
            PROC_NAME,
            "-vv",
            "-d",
            "-l",
            "logfile.log",
            "-x",
            "en",
            "database.dat",
            "export-table",
            "-t",
            "t_something",
            "-c",
            "c_firstName",
            "-f",
            "excel",
            "output.xlsx",
        ]
    )

    assert args.verbose == 2
    assert args.debug == 1
    assert args.database == "database.dat"
    assert args.logfile == "logfile.log"
    assert args.cmd == "export-table"
    assert args.table == "t_something"
    assert args.columns == ["c_firstName"]
    assert args.format == "excel"
    assert args.xlat == "en"
    assert "tables" in args.xlat_to
    assert "columns" in args.xlat_from
    assert args.output == "output.xlsx"


def test_pa_export_long(capsys):
    """Test maximal long options."""
    args = parse_args(
        [
            PROC_NAME,
            "--verbose",
            "--debug",
            "--debug",
            "--xlat",
            "it",
            "--logfile",
            "logfile.dat",
            "database.dat",
            "export-table",
            "--table",
            "t_something",
            "--columns",
            "c_firstName,c_middleName,c_lastName",
            "--format",
            "csv",
            "output.csv",
        ]
    )

    assert args.verbose == 1
    assert args.debug == 2
    assert args.logfile == "logfile.dat"
    assert args.database == "database.dat"
    assert args.cmd == "export-table"
    assert args.table == "t_something"
    assert args.columns == ["c_firstName", "c_middleName", "c_lastName"]
    assert args.format == "csv"
    assert args.xlat == "it"
    assert "data" in args.xlat_to
    assert "columns" in args.xlat_from
    assert args.output == "output.csv"


def test_pa_dump_missing_output(capsys):
    """Test export with missing output file."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "database.dat", "dump-db", "-f", "csv"])
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: output" in captured.err


def test_pa_dump_missing_format(capsys):
    """Test dump with missing output file format."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "database.dat", "dump-db", "output.dat"])
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "required: -f/--format" in captured.err


def test_pa_dump_filename_not_csv(capsys):
    """Test minimal short options."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "database.dat", "dump-db", "-f", "csv", "output.dat"])
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "does not end in '.csv'" in captured.err


def test_pa_dump_filename_not_excel(capsys):
    """Test minimal short options."""
    with pytest.raises(SystemExit) as ee:
        parse_args([PROC_NAME, "database.dat", "dump-db", "-f", "excel", "output.dat"])
    assert ee.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "does not end in '.xlsx'" in captured.err


def test_pa_dump_short(capsys):
    """Test maximal short options."""
    args = parse_args(
        [
            PROC_NAME,
            "-vv",
            "-d",
            "-l",
            "logfile.log",
            "-x",
            "en",
            "database.dat",
            "dump-db",
            "-f",
            "excel",
            "output.xlsx",
        ]
    )

    assert args.verbose == 2
    assert args.debug == 1
    assert args.database == "database.dat"
    assert args.logfile == "logfile.log"
    assert args.cmd == "dump-db"
    assert args.format == "excel"
    assert args.xlat == "en"
    assert "tables" in args.xlat_to
    assert "columns" in args.xlat_from
    assert args.output == "output.xlsx"


def test_pa_dump_long(capsys):
    """Test maximal long options."""
    args = parse_args(
        [
            PROC_NAME,
            "--verbose",
            "--debug",
            "--debug",
            "--xlat",
            "it",
            "--logfile",
            "logfile.dat",
            "database.dat",
            "dump-db",
            "--format",
            "csv",
            "output.csv",
        ]
    )

    assert args.verbose == 1
    assert args.debug == 2
    assert args.logfile == "logfile.dat"
    assert args.database == "database.dat"
    assert args.cmd == "dump-db"
    assert args.format == "csv"
    assert args.xlat == "it"
    assert "data" in args.xlat_to
    assert "columns" in args.xlat_from
    assert args.output == "output.csv"
