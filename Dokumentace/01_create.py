"""
1) Vytvoreni databaze skola.db a tabulek.
Spust: python 01_create.py
"""
import sqlite3

DB = "skola.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS znamky;
DROP TABLE IF EXISTS predmety;
DROP TABLE IF EXISTS studenti;
DROP TABLE IF EXISTS tridy;
DROP TABLE IF EXISTS ucitele;

CREATE TABLE ucitele (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno     TEXT NOT NULL,
    prijmeni  TEXT NOT NULL,
    email     TEXT UNIQUE,
    plat      INTEGER
);

CREATE TABLE tridy (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev             TEXT NOT NULL UNIQUE,     -- napr. 'I1A'
    rocnik            INTEGER NOT NULL,         -- 1 - 4
    tridni_ucitel_id  INTEGER REFERENCES ucitele(id)
);

CREATE TABLE studenti (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno           TEXT NOT NULL,
    prijmeni        TEXT NOT NULL,
    datum_narozeni  TEXT,                       -- format 'YYYY-MM-DD'
    mesto           TEXT,
    trida_id        INTEGER REFERENCES tridy(id) -- muze byt NULL
);

CREATE TABLE predmety (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev      TEXT NOT NULL,
    zkratka    TEXT NOT NULL UNIQUE,
    ucitel_id  INTEGER REFERENCES ucitele(id)
);

CREATE TABLE znamky (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL REFERENCES studenti(id),
    predmet_id  INTEGER NOT NULL REFERENCES predmety(id),
    znamka      INTEGER NOT NULL CHECK (znamka BETWEEN 1 AND 5),
    vaha        INTEGER NOT NULL DEFAULT 1,
    datum       TEXT NOT NULL               -- format 'YYYY-MM-DD'
);
""")

conn.commit()
conn.close()
print(f"Databaze {DB} vytvorena.")
