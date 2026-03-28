-- =====================================================
--  Healthcare Sterilization Analytics SQL Queries
-- =====================================================
-- Dieses SQL-Skript analysiert die Daten aus der AEMP,
-- berechnet operative KPIs und verbindet Instrumentendaten.
-- Jede Zeile beginnt mit einem Kommentar (# ersetzt durch -- in SQL)
-- =====================================================

-- 1️.Instrumententabelle erstellen (nur einmal ausführen)
-- Falls die Tabelle schon existiert, kann dieser Block auskommentiert werden
DROP TABLE IF EXISTS instrument_info;

CREATE TABLE instrument_info (
    instrument_name TEXT PRIMARY KEY,   -- Name des Instruments
    instrument_type TEXT,               -- Typ des Instruments (Sieb, Pinzette, etc.)
    set_name TEXT                       -- Zugehöriges Set
);

-- 2️.Instrumentendaten einfügen
-- Jeder Eintrag beschreibt ein Instrument + Set + Typ
INSERT INTO instrument_info (instrument_name, instrument_type, set_name) VALUES
('Sieb A', 'Sieb', 'Set 1'),
('Pinzette', 'Pinzette', 'Set 1'),
('Schere', 'Schere', 'Set 1'),
('Sieb B', 'Sieb', 'Set 2'),
('Klemme', 'Klemme', 'Set 2'),
('Sieb C', 'Sieb', 'Set 3'),
('Skalpell', 'Skalpell', 'Set 3'),
('Sieb D', 'Sieb', 'Set 4'),
('Nadelhalter', 'Nadelhalter', 'Set 4');

-- =====================================================
-- 3️.Erfolgreiche Sterilisationszyklen
-- Zeigt nur die Zyklen, die erfolgreich abgeschlossen wurden
-- =====================================================
SELECT *
FROM sterilization_cycles
WHERE status = 'success';

-- =====================================================
-- 4.Durchsatz pro Maschine
-- COUNT(*) = Anzahl Dokumentierte Instrumente
-- SUM(total_cycle_min)/60.0 = Gesamtstunden pro Maschine
-- =====================================================
SELECT machine_id,
       COUNT(*) AS instrument_count,
       SUM(total_cycle_min)/60.0 AS hours_used
FROM sterilization_cycles
GROUP BY machine_id;

-- =====================================================
-- 5.Left Join mit Instrumententabelle
-- Verbindet jeden Zyklus mit Typ und Set des Instruments
-- Left Join = alle Sterilisationszyklen erscheinen, auch wenn Instrument info fehlt
-- =====================================================
SELECT sc.cycle_id,
       sc.machine_id,
       sc.status,
       sc.instruments,
       ii.instrument_type,
       ii.set_name
FROM sterilization_cycles AS sc
LEFT JOIN instrument_info AS ii
ON sc.instruments = ii.instrument_name;