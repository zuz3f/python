"""
3) UKOLY pro studenty - dopis SQL mezi trojite uvozovky.
Spust:  python 03_ukoly.py        -> vsechny ukoly
        python 03_ukoly.py 7      -> jen ukol 7
"""
import sqlite3
import sys

DB = "skola.db"

UKOLY = [
    # ---------- ZAKLADNI SELECT ----------
    ("1. Vypis vsechny sloupce a radky z tabulky studenti.",
     """ 
     SELECT * FROM studenti;
     """),

    ("2. Vypis jen jmeno a prijmeni vsech ucitelu.",
     """
     SELECT jmeno,prijmeni FROM ucitele;
     """),

    # ---------- WHERE ----------
    ("3. Vypis studenty, kteri bydli v Praze.",
     """
     SELECT * FROM studenti
     WHERE mesto = 'Praha';
     """),

    ("4. Vypis ucitele s platem vetsim nez 40 000.",
     """
     SELECT * FROM ucitele
     WHERE plat >= 40000;
     """),

    ("5. Vypis studenty narozene v roce 2008 (pouzij BETWEEN).",
     """
     SELECT * FROM studenti
     WHERE datum_narozeni BETWEEN '2008-01-01' AND '2008-12-31';
     """),

    ("6. Vypis studenty z Brna nebo z Kladna (pouzij IN).",
     """
     SELECT * FROM studenti
     WHERE mesto IN ('Brno','Kladno');
     """),

    ("7. Vypis studenty, jejichz prijmeni konci na 'ova' (pouzij LIKE).",
     """
     SELECT * FROM studenti
     WHERE prijmeni LIKE '%ova';
     """),

    ("8. Vypis studenty, u kterych nezname mesto (IS NULL).",
     """
      SELECT * FROM studenti
      WHERE mesto IS NULL;
     """),

    # ---------- ORDER BY, LIMIT, DISTINCT ----------
    ("9. Vypis studenty serazene podle prijmeni abecedne.",
     """
     SELECT * FROM studenti
     ORDER BY prijmeni;
     """),

    ("10. Vypis 3 nejlepe placene ucitele.",
     """
     SELECT * FROM ucitele
     ORDER BY plat DESC
     LIMIT 3;
     """),

    ("11. Vypis seznam mest, odkud studenti jsou (kazde mesto jen jednou).",
     """
    SELECT DISTINCT mesto FROM studenti;
     """),

    # ---------- AGREGACE ----------
    ("12. Kolik je celkem studentu?",
     """
     SELECT COUNT(*)
     FROM studenti;
     """),

    ("13. Jaky je nejnizsi, nejvyssi a prumerny plat ucitelu?",
     """
     SELECT MIN(plat), MAX(plat), AVG(plat)
     FROM ucitele;
     """),

    # ---------- GROUP BY, HAVING ----------
    ("14. Kolik studentu bydli v jednotlivych mestech? (seradit od nejvic)",
     """
     SELECT mesto, COUNT(mesto) AS [pocet lidi z mesta]
     FROM studenti
     GROUP BY mesto
     ORDER BY COUNT(mesto) DESC;
     """),

    ("15. Kolik bylo udeleno jednotlivych znamek (1, 2, 3, 4, 5)?",
     """
     SELECT znamka, COUNT(znamka) AS [pocet znamky]
     FROM znamky
     GROUP BY znamka;
     """),

    ("16. Vypis id studentu, kteri maji prumer znamek horsi nez 2.5 (HAVING).",
     """
     -- sem napis svuj SQL
     """),

    # ---------- JOIN ----------
    ("17. Vypis jmeno, prijmeni studenta a nazev jeho tridy.",
     """
     -- sem napis svuj SQL
     """),

    ("18. Vypis predmety a cele jmeno ucitele, ktery je uci.",
     """
     -- sem napis svuj SQL
     """),

    ("19. Vypis vsechny petky (znamka 5): jmeno studenta, predmet, datum.",
     """
     -- sem napis svuj SQL
     """),

    ("20. Vypis VSECHNY studenty a jejich tridu - i ty, co tridu nemaji (LEFT JOIN).",
     """
     -- sem napis svuj SQL
     """),

    ("21. Vypis predmety, ze kterych nebyla udelena zadna znamka.",
     """
     -- sem napis svuj SQL
     """),

    # ---------- JOIN + GROUP BY ----------
    ("22. Prumerna znamka v kazdem predmetu (nazev predmetu, prumer), od nejlepsiho.",
     """
     -- sem napis svuj SQL
     """),

    ("23. Pocet studentu v kazde tride + jmeno tridniho ucitele.",
     """
     -- sem napis svuj SQL
     """),

    ("24. Top 5 studentu s nejlepsim prumerem (jmeno, prijmeni, prumer).",
     """
     -- sem napis svuj SQL
     """),

    # ---------- PODDOTAZY (bonus) ----------
    ("25. BONUS: Vypis ucitele, kteri maji vyssi plat nez je prumer (poddotaz).",
     """
     -- sem napis svuj SQL
     """),

    ("26. BONUS: Vypis studenty, kteri nemaji zadnou znamku (NOT IN / NOT EXISTS).",
     """
     -- sem napis svuj SQL
     """),

    ("27. BONUS: Vazeny prumer kazdeho studenta z Databazovych systemu (DBS).",
     """
     -- sem napis svuj SQL
     """),
]


def spust(cislo, zadani, sql):
    print("=" * 70)
    print(zadani)
    print("-" * 70)
    bez_komentaru = "\n".join(r for r in sql.splitlines() if not r.strip().startswith("--"))
    if not bez_komentaru.strip():
        print("  (TODO - zatim nevyreseno)")
        return
    try:
        cur = conn.execute(sql)
    except sqlite3.Error as e:
        print(f"  CHYBA v SQL: {e}")
        return
    hlavicka = [d[0] for d in cur.description]
    radky = cur.fetchall()
    print(" | ".join(hlavicka))
    for r in radky:
        print(" | ".join("NULL" if v is None else str(v) for v in r))
    print(f"({len(radky)} radku)")


if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    if len(sys.argv) > 1:
        i = int(sys.argv[1])
        spust(i, *UKOLY[i - 1])
    else:
        for i, (zadani, sql) in enumerate(UKOLY, start=1):
            spust(i, zadani, sql)
    conn.close()
