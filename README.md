# GlucoLog - GlucoLog Back-up Database Explorer
![Build Status](https://github.com/papadeltasierra/singles/actions/workflows/workflow.yml/badge.svg)
# Disclaimer
Disclaimer: [Paul D.Smith][pds] has not connection to [Menarini Diagnostics UK][Menarini Diagnostics UK] and they are not responsible for this application in any way.
## Installation and Usage
Install this tool using [Python][python] [pip][pip]:
```
$ pip install glucolog
```
The command line options for the tool are:
```
$ glucolog --help
usage: glucolog [-h] [-v] [-d] [-l LOGFILE] [-x {en,it}] database {list-tables,list-columns,export-table,dump-db} ...

Tool to extract information from a GlucoLog back-up database

positional arguments:
  database              name of the GlucoLog backup database
  {list-tables,list-columns,export-table,dump-db}

optional arguments:
  -h, --help            show this help message and exit

Common options:
  Options which apply to all commands

  -v, --verbose         make the program more verbose
  -d, --debug           add debugging information to the log file
  -l LOGFILE, --logfile LOGFILE
                        specify log file name
  -x {en,it}, --xlat {en,it}
                        language to translate to
```
Each command has additional options e.g.
```
$ glucolog database_backup.dbglu list-columns --help
usage: glucolog database list-columns [-h] -t TABLE

optional arguments:
  -h, --help            show this help message and exit
  -t TABLE, --table TABLE
                        name of a specific table in the database
```
## Language Translations
The database is written in Italian but the ability to translate the table and column names is provided.  Language files are provided in a simple [YAML][yaml] format and users are encouraged to contribute additional language files to the project.

## Under The Hood
1. The GlucoLog database file is a simple [SQLite3][sqlite3] database and us read using [Python][python]'s native [SQLite3 package][py-SQLite3].
2. The data is written to a CSV, comma-seperated-values, file using [Python][python]'s native [csv package][py-csv] package.
3. The data is written to a [Microsoft Excel][microsoft] spreadsheet using the [Python][python] [openpyxl package][openpyxl].
4. All times are represented as UTC (GMT) times and dates are formated using the [ISO 8601][iso8601] format of *YYYY-MM-DD* which avoids confusion between English and American date representations (e.g. *03-04-2021* the 3rd April or the 4th of March?).

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Menarini Diagnostics UK]: <https://www.menarinidiag.co.uk>
   [pds]: <mailto:paul@pauldsmith.org.uk>
   [python]: <https://python.org>
   [pip]: <https://pypi.org/project/pip/>
   [openpyxl]: <https://openpyxl.readthedocs.io/en/stable/>
   [py-csv]: <https://docs.python.org/3/library/csv.html>
   [py-sqlite3]: <https://docs.python.org/3/library/sqlite3.html>
   [sqlite3]: <https://www.sqlite.org>
   [yaml]: <https://yaml.org/>
   [microsoft]: <https://microsoft.com>
   [iso8601]: <https://en.wikipedia.org/wiki/ISO_8601>
   [contributing]: <https://github.com/papadeltasierra/glucolog/CONTRIBUTING.md>



