"""Read a GlucoLog backup database."""
import os
import sys
import argparse
from logging import getLogger, StreamHandler, DEBUG, INFO, WARNING
from logging.handlers import RotatingFileHandler
import sqlite3

EXCEL_EPOCH = 25569
DAY_IN_SECS = 24 * 60 * 60

log = getLogger()


def print_row(row, target):
    datestamp = int(row[1] / 1000)
    date_value = int(datestamp / DAY_IN_SECS)

    timestamp = int(row[2]/1000)
    time_value = int(timestamp % DAY_IN_SECS)
    hour_value = time_value / (60 * 60)
    min_value = (time_value % (60 * 60)) / 60
    sec_value = time_value % 60

    excel_date = date_value + EXCEL_EPOCH

    glu = "" if row[16] == "Ket" else row[11]
    ket = "" if row[16] == "Glu" else row[11]



    target.write("%d,%2.2d:%2.2d:%2.2d,%s,%s\n" % (excel_date, hour_value, min_value, sec_value, glu, ket))
    # print(row)





def list_tables(args, cur):
    """List the tables available in the database."""
    rows = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = [row[0] for row in rows]
    return rows


def do_list_tables(args, cur):
    """List the tables available in the database."""

    print("Tables found")
    print("============")
    rows = list_tables(args, cur)
    for row in rows:
        print(row)


def list_columns(args, cur, table):
    """List the columns available from the indicated table."""
    rows = cur.execute("SELECT * FROM %s" % table)
    names = [description[0] for description in rows.description]

    return names


def do_list_columns(args, cur):
    """List the columns available from the indicated table."""
    assert getattr(args, "table"), "Table name should have been supplied"

    print("Columns Found")
    print("=============")
    names = list_columns(args, cur, args.table)
    for name in names:
        print(name)


def export_data(args, cur, table, columns):
    """Write a CSV file that contains the columns from a specific table."""

    # Each row is returned as a tuple...
    rows = cur.execute("SELECT %s FROM %s" % (",".join(columns), table))
    # ...which convert to a list
    rows = [list(row) for row in rows]
    #...and then convert each field to a string.
    rows2 = []
    for row in rows:
        row = [str(field) for field in row]
        rows2.append(row)
    return rows2


def do_export_data(args, cur):
    """Write a CSV file that contains the columns from a specific table."""
    assert getattr(args, "table", None), "Table should have been defined"
    assert getattr(args, "columns", None), "Columns should have been defined"

    print(",".join(args.columns))

    rows = export_data(args, cur, args.table, args.columns)
    for row in rows:
        # May want to strip whitespace from fields.
        print(",".join(row))


def do_dump_db(args, cur):
    """Write a CSV file that contains the columns from a specific table."""

    # First get the tables...
    tables = list_tables(args, cur)

    for table in tables:
        print(table)
        columns = list_columns(args, cur, table)
        print(",".join(columns))
        rows = export_data(args, cur, table, columns)
        for row in rows:
            print(",".join(row))


def setup_logging(args):
    """Set up logging."""
    # Default logging level has to be DEBUG as the filtering is done at Handler level
    # and then global level.
    log.setLevel(DEBUG)

    stream_handler = StreamHandler()
    if args.verbose >= 2:
        stream_handler.setLevel(DEBUG)
    elif args.verbose >= 1:
        stream_handler.setLevel(INFO)
    else:
        stream_handler.setLevel(WARNING)

    file_handler = RotatingFileHandler(
        args.logfile, mode="a", maxBytes=0, backupCount=4
    )
    if args.debug >= 2:
        file_handler.setLevel(DEBUG)
    elif args.debug >= 1:
        file_handler.setLevel(INFO)
    else:
        file_handler.setLevel(WARNING)

    log.addHandler(stream_handler)
    log.addHandler(file_handler)



def parse_args(argv):
    """Parse command line arguments."""
    default_logfile = os.path.splitext(os.path.basename(argv[0]))[0] + ".log"

    parser = argparse.ArgumentParser(description="Tool to extract information from a GlucoLog back-up database")
    parser.add_argument("-v", "--verbose", action="count", help="make the program more verbose", default=0)
    parser.add_argument("-d", "--debug", action="count", help="add debugging information to the log file", default=0)
    parser.add_argument("-l", "--logfile", help="specify log file name", default=default_logfile)


    subparsers = parser.add_subparsers()
    table_parser = subparsers.add_parser("tables")
    table_parser.set_defaults(func=do_list_tables)

    columns_parser = subparsers.add_parser("columns")
    columns_parser.add_argument("-t", "--table", required=True, help="name of a specific table in the database")
    columns_parser.set_defaults(func=do_list_columns)

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("-t", "--table", required=True, help="name of a specific table in the database")
    export_parser.add_argument("-c", "--columns", required=True, help="name of a specific table in the database")
    export_parser.set_defaults(func=do_export_data)

    export_parser = subparsers.add_parser("dump")
    export_parser.set_defaults(func=do_dump_db)

    parser.add_argument("database", type=str, action="store", help="name of the GlucoLog backup database")

    args = parser.parse_args(argv[1:])

    columns = getattr(args, "columns", None)
    if columns:
        setattr(args, "columns", columns.split(","))

    # print(args)
    return args

def main(argv):
    """Mainline routine."""
    args = parse_args(argv)
    setup_logging(args)

    with sqlite3.connect(args.database) as con:
        cur = con.cursor()
        args.func(args, cur)


if __name__ == "__main__":
    main(sys.argv)
