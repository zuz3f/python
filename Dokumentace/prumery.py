import sqlite3
import sys
from contextlib import closing
from pathlib import Path

DB = Path(__file__).parent / "skola.db"

DOTAZ_PRUMERY = """
    SELECT p.nazev                 AS predmet,
           COUNT(*)                AS pocet,
           ROUND(AVG(z.znamka), 2) AS prumer
    FROM znamky AS z
    JOIN studenti AS s ON s.id = z.student_id
    JOIN predmety AS p ON p.id = z.predmet_id
    WHERE s.jmeno = ?
    GROUP BY p.id
    ORDER BY p.nazev
"""


def pripoj():
    conn = sqlite3.connect(f"{DB.as_uri()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def prumery_studenta(conn, jmeno):
    return conn.execute(DOTAZ_PRUMERY, (jmeno,)).fetchall()


def seznam_studentu(conn):
    return [r["jmeno"] for r in conn.execute("SELECT jmeno FROM studenti ORDER BY jmeno")]


def main():
    if not DB.exists():
        print("Databáze neexistuje – nejdřív spusť vytvor_db.py")
        return 1

    jmeno = sys.argv[1] if len(sys.argv) > 1 else input("Jméno studenta: ").strip()

    try:
        with closing(pripoj()) as conn:
            radky = prumery_studenta(conn, jmeno)
            if not radky:
                print(f"Student „{jmeno}“ nebyl nalezen. Na výběr jsou:")
                for s in seznam_studentu(conn):
                    print("  -", s)
                return 1
    except sqlite3.Error as e:
        print("Chyba databáze:", e)
        return 1

    print(f"Průměry studenta: {jmeno}\n")
    print(f"{'Předmět':<15} {'Známek':>6} {'Průměr':>7}")
    print("-" * 30)
    for r in radky:
        print(f"{r['predmet']:<15} {r['pocet']:>6} {r['prumer']:>7.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
