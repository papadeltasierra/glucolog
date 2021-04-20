"""Create an SQLite3 database to us whilst testing the Glucolog application."""
import os
import sqlite3
from typing import Dict, List, Any

# Database definition keys.
TABLES = "tables"
NAME = "name"
EN_NAME = "en_name"
COLUMNS = "columns"
DATA = "data"

# Database definition.
DATABASE: Dict[str, List[Dict[str, Any]]] = {
    TABLES: [
        # This tables is an internal SQLite3 table and we should not create it
        #  ourselves.
        # {
        #     NAME: "sqlite_sequence",
        #     COLUMNS: [
        #         "name",
        #         "seq"
        #     ]
        # },
        {
            NAME: "android_metadata",
            EN_NAME: "android_metadata",
            COLUMNS: ["sconosciuta", "locale"],
            DATA: [("", "en_GB")],
        },
        {
            NAME: "t_parametri",
            EN_NAME: "t_parameters",
            COLUMNS: [
                "_id",
                "cognome",
                "nome",
                "data_nascita",
                "sesso",
                "mail_medico",
                "um_glicemia",
                "um_carboidrati",
                "livello_basso",
                "livello_alto",
                "digiuno",
                "mattino",
                "primo_pomeriggio",
                "tardo_pomeriggio",
                "sera",
                "notte",
                "sconosciuta",
                "chetoni",
                "insulina",
                "meter",
                "web_server",
                "PID",
                "barcode_areo",
                "areo_nfc_bt",
                "noareo_bt_btle",
                "periodocustoms1",
                "periodocustoms2",
                "periodocustoms3",
                "periodocustoms4",
                "shealth",
                "web_server_auto",
                "show_delete",
            ],
            DATA: [
                (
                    1,
                    "Garibaldi",
                    "Giuseppe",
                    "04-07-2007",
                    "M",
                    "giuseppe@garibaldi.nowhere",
                    2,
                    1,
                    "",
                    "",
                    "24:00",
                    "06:00",
                    "12:00",
                    "16:00",
                    "19:00",
                    "21:00",
                    "",
                    "S",
                    "S",
                    11,
                    "",
                    "",
                    "null@XX123456",
                    0,
                    0,
                    "01:00",
                    "01:00",
                    "01:00",
                    "01:00",
                    "",
                    "",
                    "",
                )
            ],
        },
        {
            NAME: "t_risultati",
            EN_NAME: "t_results",
            COLUMNS: [
                "_id",
                "data",
                "ora",
                "periodo",
                "attivita",
                "aeroC",
                "aeroF",
                "aeroFB",
                "aeroEX",
                "evento",
                "commento",
                "risultato",
                "carboidrati",
                "insulina",
                "dose",
                "origine",
                "analisi",
                "dt_cancel",
                "dt_invio",
                "fl_invio",
            ],
            DATA: [
                # Dates and times are in milliseconds relative to 1-Jan-1970 and
                # 00:00.
                (
                    17,
                    1619611200000,
                    21900000,
                    "mattino",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    8.5,
                    "",
                    "",
                    "",
                    "S",
                    "Glu",
                    "",
                    0,
                    "W",
                ),
                (
                    18,
                    1619697600000,
                    43620000,
                    "primo_pomeriggio",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    9.1,
                    "",
                    "",
                    "",
                    "S",
                    "Glu",
                    "",
                    0,
                    "W",
                ),
                (
                    19,
                    1619784000000,
                    58080000,
                    "tardo_pomeriggio",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    7.3,
                    "",
                    "",
                    "",
                    "S",
                    "Glu",
                    "",
                    0,
                    "W",
                ),
                (
                    22,
                    1619870400000,
                    69060000,
                    "sera",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    10.1,
                    "",
                    "",
                    "",
                    "S",
                    "Glu",
                    "",
                    0,
                    "W",
                ),
                (
                    20,
                    1619956800000,
                    76500000,
                    "notte",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    8.7,
                    "",
                    "",
                    "",
                    "S",
                    "Glu",
                    "",
                    0,
                    "W",
                ),
                (
                    20,
                    1620043200000,
                    76500000,
                    "mezzanotte",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    8.6,
                    "",
                    "",
                    "",
                    "S",
                    "Glu",
                    "",
                    0,
                    "W",
                ),
            ],
        },
        {
            NAME: "t_insulina",
            EN_NAME: "t_insulin",
            COLUMNS: [
                "_id",
                "sconosciuta",
                "desc_insulina",
            ],
        },
        {
            NAME: "t_glucometri",
            EN_NAME: "t_glucometers",
            COLUMNS: [
                "_id",
                "serial",
                "data",
                "ora",
                "sconosciuta",
                "risultato",
                "last_dw_index",
                "last_dw_index_ket",
            ],
            DATA: [(1, "XX123456", "", "", "", "", 79, 3)],
        },
        # This is a fake table created to test table name translation.
        {NAME: "t_nascosto", EN_NAME: "t_nascosto", COLUMNS: ["idiota"]},
    ]
}

# Create a list of tables
DB_TABLES = [x[NAME] for x in DATABASE[TABLES]]
DB_EN_TABLES = [x[EN_NAME] for x in DATABASE[TABLES]]


def mock_database(filename):
    """Create a mock database."""
    # Always start from a fresh database so delete any old copies.
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    # Create a new database.
    con = sqlite3.connect(filename)
    cur = con.cursor()

    # Create table
    for table in DATABASE[TABLES]:
        columns = table[COLUMNS]
        cur.execute(
            "CREATE TABLE {table} ({columns})".format(
                table=table[NAME], columns=",".join(columns)
            )
        )  # nosec
        if DATA in table:
            for data in table[DATA]:
                cur.execute(  # nosec
                    "INSERT INTO {table} VALUES {values}".format(
                        table=table[NAME], values=data
                    )
                )

    # Save (commit) the changes
    con.commit()

    # Close the connection (database file).
    con.close()
