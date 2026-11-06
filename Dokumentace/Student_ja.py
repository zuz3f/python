import sqlite3
import sys
from contextlib import closing
from pathlib import Path

DB = Path(__file__).parent / "skola.db"

SCHEMA = """
DROP TABLE IF EXISTS jmeno;
DROP TABLE IF EXISTS predmet;
DROP TABLE IF EXISTS znamky;

CREATE TABLE jmeno (
id     INTEGER PRIMERY KEY,
jmeno   TEXT NOT NULL UNIQUE,
prijmeni    TEXT NOT NULL UNIQUE

);

CREATE TABLE predmet (
id      INTEGER PRIMARY KEY,
nazev   TEXT NOT NULL UNIQUE
);

CREATE TABLE znamky (
id      INTEGER PRIMARY KEY,

);
"""
JMENO = [
    ("Jana", "Nováková"),
]
