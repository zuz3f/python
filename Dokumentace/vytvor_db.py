import random
import sqlite3
from contextlib import closing
from pathlib import Path

DB = Path(__file__).parent / "skola.db"

SCHEMA = """
DROP TABLE IF EXISTS znamky;
DROP TABLE IF EXISTS studenti;
DROP TABLE IF EXISTS predmety;

CREATE TABLE studenti (
    id     INTEGER PRIMARY KEY,
    jmeno  TEXT NOT NULL UNIQUE,
    trida  TEXT NOT NULL
);

CREATE TABLE predmety (
    id     INTEGER PRIMARY KEY,
    nazev  TEXT NOT NULL UNIQUE
);

CREATE TABLE znamky (
    id          INTEGER PRIMARY KEY,
    student_id  INTEGER NOT NULL REFERENCES studenti(id),
    predmet_id  INTEGER NOT NULL REFERENCES predmety(id),
    znamka      INTEGER NOT NULL CHECK (znamka BETWEEN 1 AND 5)
);
"""

STUDENTI = [
    ("Jana Nováková", "3.A"),
    ("Petr Svoboda", "3.A"),
    ("Eva Dvořáková", "3.B"),
    ("Tomáš Černý", "3.B"),
]

PREDMETY = ["Matematika", "Český jazyk", "Angličtina", "Programování"]


def pripoj():
    """Otevře spojení se stejným nastavením pro celý program."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def vytvor_tabulky(conn):
    conn.executescript(SCHEMA)


def vloz_data(conn):
    conn.executemany(
        "INSERT INTO studenti (jmeno, trida) VALUES (?, ?)", STUDENTI
    )
    conn.executemany(
        "INSERT INTO predmety (nazev) VALUES (?)",
        [(nazev,) for nazev in PREDMETY],
    )

    student_ids = [r["id"] for r in conn.execute("SELECT id FROM studenti")]
    predmet_ids = [r["id"] for r in conn.execute("SELECT id FROM predmety")]

    random.seed(42)
    znamky = []
    for student_id in student_ids:
        for predmet_id in predmet_ids:
            for _ in range(random.randint(4, 7)):
                znamka = random.choices([1, 2, 3, 4, 5], weights=[30, 30, 20, 12, 8])[0]
                znamky.append((student_id, predmet_id, znamka))

    conn.executemany(
        "INSERT INTO znamky (student_id, predmet_id, znamka) VALUES (?, ?, ?)",
        znamky,
    )
    return len(znamky)


def main():
    try:
        with closing(pripoj()) as conn:
            vytvor_tabulky(conn)
            with conn:  # transakce: vše se uloží, nebo nic
                pocet = vloz_data(conn)
    except sqlite3.Error as e:
        print("Chyba databáze:", e)
        return 1

    print(f"Databáze vytvořena: {DB}")
    print(f"Vloženo {len(STUDENTI)} studentů, {len(PREDMETY)} předmětů a {pocet} známek.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
