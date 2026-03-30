# ============================================================
# Healthcare Portfolio – Sterilization Traceability Pipeline
# ============================================================
#
# Dieses Skript simuliert einen realistischen Sterilisationsprozess
# aus der AEMP (Aufbereitungseinheit für Medizinprodukte).
#
# Ziel dieses Projekts:
# ------------------------------------------------------------
# 1) Simulation validierter Autoklav-Zyklen (ca. 60 Minuten)
# 2) Dokumentation der Plateauzeit (5 Minuten = 3 + 2 Sicherheitszuschlag)
# 3) Lückenlose Traceability auf Instrumentenebene
# 4) Export der Daten als CSV (für Power BI)
# 5) Speicherung in einer SQLite-Datenbank (für SQL-Analysen)
#
# Warum das wichtig ist:
# ------------------------------------------------------------
# In der Realität dürfen Medizinprodukte NUR freigegeben werden,
# wenn:
# - der Sterilisationszyklus erfolgreich war
# - alle Instrumente korrekt dokumentiert wurden
# - 
#
# Dieses Skript bildet genau diese Logik datengetrieben ab.
# ============================================================


# =========================
# Benötigte Bibliotheken
# =========================
# pandas  → Verarbeitung tabellarischer Daten
# sqlite3 → Erstellung einer SQL-Datenbank ohne Installation
# os      → Sichere Pfad- und Ordnerverwaltung

import pandas as pd
import sqlite3
import os


# ============================================================
# 1) Sicherstellen, dass der Ordner /data existiert
# ============================================================
# Egal von wo das Skript gestartet wird (VS Code, PowerShell,
# Git Bash), der Pfad wird immer korrekt relativ zur Datei gebaut.

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)


# ============================================================
# 2) Simulation realer Autoklav-Zyklen
# ============================================================
# Jede Zeile entspricht einem Sterilisationszyklus.
# Instrumente werden zunächst als Liste erfasst.

data = [
    {
        "cycle_id": 1,
        "machine_id": "M1",
        "status": "success",
        "instruments": ["Sieb A", "Pinzette", "Schere"],
    },
    {
        "cycle_id": 2,
        "machine_id": "M1",
        "status": "success",
        "instruments": ["Sieb B", "Klemme"],
    },
    {
        "cycle_id": 3,
        "machine_id": "M2",
        "status": "fail",
        "instruments": ["Sieb C", "Skalpell"],
    },
    {
        "cycle_id": 4,
        "machine_id": "M2",
        "status": "success",
        "instruments": ["Sieb D", "Nadelhalter"],
    },
]

# Umwandlung in eine Tabelle (DataFrame)
df = pd.DataFrame(data)


# ============================================================
# 3) Prozesslogik – Zykluszeit berechnen
# ============================================================
#
# Fachliche Realität:
# - Autoklav läuft validiert ca. 60 Minuten
# - Plateauzeit = 5 Minuten (3 Min Haltezeit + 2 Min Sicherheitszuschlag)
# - Bei Fehler muss der komplette Zyklus erneut durchgeführt werden und die Instrumente neu verpackt werden

base_cycle_min = 60
plateau_min = 5

df["total_cycle_min"] = df["status"].apply(
    lambda x: base_cycle_min + plateau_min
    if x == "success"
    else (base_cycle_min + plateau_min) * 2
)


# ============================================================
# 4) Traceability auf Instrumentenebene
# ============================================================
#
# explode() zerlegt die Instrumentenlisten in einzelne Zeilen.
#
# Warum entscheidend?
# → Jedes einzelne Instrument muss dokumentiert sein.
# → Was nicht dokumentiert ist, darf NICHT freigegeben werden.

df = df.explode("instruments")


# ============================================================
# 5) Freigabelogik
# ============================================================
#
# Ein Instrument darf nur freigegeben werden, wenn
# der Zyklus erfolgreich war.

df["released"] = df["status"] == "success"


# ============================================================
# 6) CSV-Datei erzeugen (für Power BI)
# ============================================================

csv_path = os.path.join(data_dir, "healthcare.csv")
df.to_csv(csv_path, index=False, encoding="utf-8")

print("CSV gespeichert unter:", csv_path)


# ============================================================
# 7) SQLite-Datenbank erzeugen (für SQL-Analysen)
# ============================================================

db_path = os.path.join(data_dir, "healthcare.db")
conn = sqlite3.connect(db_path)

df.to_sql("sterilization_cycles", conn, if_exists="replace", index=False)
conn.close()

print("SQLite DB erstellt unter:", db_path)