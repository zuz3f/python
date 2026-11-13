"""
2) Naplneni databaze mock daty.
Spust az po 01_create.py:  python 02_data.py
"""
import random
import sqlite3
from datetime import date, timedelta

DB = "skola.db"
random.seed(42)  # aby meli vsichni stejna data

conn = sqlite3.connect(DB)
cur = conn.cursor()

# --- ucitele -----------------------------------------------------------
ucitele = [
    ("Jan",     "Novak",     "novak@skola.cz",     42000),
    ("Petra",   "Svobodova", "svobodova@skola.cz", 39000),
    ("Karel",   "Dvorak",    "dvorak@skola.cz",    45000),
    ("Lucie",   "Cerna",     "cerna@skola.cz",     37000),
    ("Tomas",   "Prochazka", "prochazka@skola.cz", 48000),
    ("Eva",     "Kucerova",  None,                 35000),  # nema email, neuci predmet
]
cur.executemany(
    "INSERT INTO ucitele (jmeno, prijmeni, email, plat) VALUES (?, ?, ?, ?)",
    ucitele,
)

# --- tridy -------------------------------------------------------------
tridy = [
    ("I1A", 1, 1),
    ("I2A", 2, 2),
    ("I3B", 3, 3),
    ("I4A", 4, 5),
]
cur.executemany(
    "INSERT INTO tridy (nazev, rocnik, tridni_ucitel_id) VALUES (?, ?, ?)",
    tridy,
)

# --- studenti ----------------------------------------------------------
studenti = [
    ("Adam",     "Kral",      "2009-03-14", "Praha",   1),
    ("Barbora",  "Mala",      "2009-07-02", "Brno",    1),
    ("Cyril",    "Horak",     "2008-11-23", "Praha",   1),
    ("Dana",     "Vesela",    "2009-01-30", "Kladno",  1),
    ("Emil",     "Pokorny",   "2008-05-12", "Praha",   2),
    ("Filip",    "Marek",     "2008-09-09", "Beroun",  2),
    ("Gabriela", "Pospisilova","2008-02-17","Praha",   2),
    ("Hugo",     "Hajek",     "2007-12-01", "Kladno",  2),
    ("Ivana",    "Jelinkova", "2007-06-25", "Praha",   3),
    ("Jakub",    "Ruzicka",   "2007-04-04", "Brno",    3),
    ("Klara",    "Benesova",  "2007-08-19", "Praha",   3),
    ("Lukas",    "Fiala",     "2006-10-10", "Beroun",  3),
    ("Martin",   "Sedlacek",  "2006-03-03", "Praha",   4),
    ("Nikola",   "Dolezalova","2006-01-15", "Kladno",  4),
    ("Ondrej",   "Zeman",     "2005-12-24", "Praha",   4),
    ("Pavla",    "Kolarova",  "2006-07-07", None,      4),     # nezname mesto
    ("Radek",    "Navratil",  "2008-04-18", "Praha",   None),  # nema tridu
]
cur.executemany(
    "INSERT INTO studenti (jmeno, prijmeni, datum_narozeni, mesto, trida_id) "
    "VALUES (?, ?, ?, ?, ?)",
    studenti,
)

# --- predmety ----------------------------------------------------------
predmety = [
    ("Matematika",           "MAT", 1),
    ("Cesky jazyk",          "CJL", 2),
    ("Anglicky jazyk",       "ANJ", 4),
    ("Programovani",         "PRG", 3),
    ("Databazove systemy",   "DBS", 3),
    ("Telesna vychova",      "TEV", 5),
    ("Robotika",             "ROB", None),  # zatim bez ucitele i bez znamek
]
cur.executemany(
    "INSERT INTO predmety (nazev, zkratka, ucitel_id) VALUES (?, ?, ?)",
    predmety,
)

# --- znamky (nahodne, ale diky seedu porad stejne) ----------------------
zacatek = date(2026, 9, 1)
znamky = []
for student_id in range(1, 17):          # Radek (17) nema zadne znamky
    for predmet_id in range(1, 7):       # Robotika (7) nema znamky
        for _ in range(random.randint(2, 4)):
            znamka = random.choices([1, 2, 3, 4, 5], weights=[30, 30, 20, 13, 7])[0]
            vaha = random.choice([1, 1, 1, 2, 3])
            datum = zacatek + timedelta(days=random.randint(0, 70))
            znamky.append((student_id, predmet_id, znamka, vaha, datum.isoformat()))

cur.executemany(
    "INSERT INTO znamky (student_id, predmet_id, znamka, vaha, datum) "
    "VALUES (?, ?, ?, ?, ?)",
    znamky,
)

conn.commit()
conn.close()
print(f"Vlozeno: {len(ucitele)} ucitelu, {len(tridy)} trid, {len(studenti)} studentu, "
      f"{len(predmety)} predmetu, {len(znamky)} znamek.")
