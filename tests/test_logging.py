import logging
from src.glucolog.glucolog import PROC_NAME, parse_args, setup_logging

log = logging.getLogger()

# Default arguments just to ensure that we get through parse_args.
FMT_ARGUMENTS = "{proc} {debug} {verbose} --logfile {logfile} database.dat list-tables"


def test_logging_defaults(logfile, capsys):
    """Basic test of setup logging."""
    args = parse_args(
        FMT_ARGUMENTS.format(
            proc=PROC_NAME, debug="", verbose="", logfile=logfile
        ).split()
    )
    print(args)
    setup_logging(args)

    # We now expect both on-screen and logging file error levels to be set to
    # warning.
    log.info("Info: should not be seen")
    log.warning("Warning: should be seen")

    captured = capsys.readouterr()
    assert "Info:" not in captured.out
    assert "Warning:" in captured.err

    # To test the logging output we need to first close the logging file.
    logging.shutdown()

    # Read the logging file and see if we wrote it
    with open(logfile, "r") as source:
        logdata = source.read()
        assert "Info:" not in logdata
        assert "Warning:" in logdata


def test_logging_v_dd(logfile, capsys):
    """Test increasing logging levels #1."""
    args = parse_args(
        FMT_ARGUMENTS.format(
            proc=PROC_NAME,
            debug="--debug --debug",
            verbose="--verbose",
            logfile=logfile,
        ).split()
    )
    setup_logging(args)

    # We now expect both on-screen and logging file error levels to be set to
    # warning.
    log.debug("Debug: should be in logfile only")
    log.info("Info: should be in both")

    captured = capsys.readouterr()
    assert "Debug:" not in captured.err
    assert "Info:" in captured.err

    # To test the logging output we need to first close the logging file.
    logging.shutdown()

    # Read the logging file and see if we can see
    with open(logfile, "r") as source:
        logdata = source.read()
        assert "Debug:" in logdata
        assert "Info:" in logdata


def test_logging_vv_d(logfile, capsys):
    """Test increasing logging levels #2."""
    args = parse_args(
        FMT_ARGUMENTS.format(
            proc=PROC_NAME, debug="--debug", verbose="--verbose", logfile=logfile
        ).split()
    )

    setup_logging(args)

    # We now expect both on-screen and logging file error levels to be set to
    # warning.
    log.debug("Debug: should be in stdout only")
    log.info("Info: should be in both")

    captured = capsys.readouterr()
    # assert "Debug:" in captured.err
    assert "Info:" in captured.err

    # To test the logging output we need to first close the logging file.
    logging.shutdown()

    # Read the logging file and see if we can see
    with open(logfile, "r") as source:
        logdata = source.read()
        # assert "Debug:" not in logdata
        assert "Info:" in logdata
