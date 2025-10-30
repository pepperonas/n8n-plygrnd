# CLAUDE.md

Diese Datei bietet Anleitung für Claude Code (claude.ai/code) bei der Arbeit mit Code in diesem Repository.

## Projektkontext

Dies ist ein **n8n Workflows Playground** - eine Sammlung mehrerer n8n-Automatisierungs-Workflows für verschiedene Business-Automatisierungsaufgaben. Jeder Workflow ist eigenständig und produktionsbereit, mit eigenem Verzeichnis, Dokumentation und Implementierung.

### Aktuelle Workflows

1. **lead-generator/** - Automatisiertes B2B-Lead-Generierungs- und E-Mail-Kampagnensystem
   - Siehe `lead-generator/CLAUDE.md` für workflow-spezifische Anleitung
   - Beinhaltet n8n-Workflow, Python-Skripte, REST API und Dashboard

2. **[Zukünftige Workflows]** - Werden hinzugefügt, während das Projekt wächst

## Wichtig: Multi-Workflow Repository-Struktur

**Bei der Arbeit an spezifischen Workflows, immer auf die CLAUDE.md-Datei dieses Workflows verweisen** für detaillierte technische Anleitung. Diese Root-CLAUDE.md bietet nur allgemeine Repository-weite Anleitung.

## Repository-Struktur

```
n8n-plygrnd/
├── README.md                    # Projektübersicht (Multi-Workflow)
├── CLAUDE.md                    # Diese Datei - Allgemeine Anleitung
├── package.json                 # Node.js Konfiguration
├── index.js                     # Entry Point
│
├── lead-generator/              # Erster Workflow
│   ├── CLAUDE.md               # Workflow-spezifische Anleitung
│   ├── README.md               # Benutzerdokumentation
│   └── [Implementierungsdateien]
│
├── [workflow-2]/                # Zukünftige Workflows
│   ├── CLAUDE.md
│   ├── README.md
│   └── [Implementierungsdateien]
│
└── [workflow-3]/
    └── ...
```

## Allgemeine Entwicklungsrichtlinien

### Dateiorganisation
- Jeder Workflow lebt in seinem eigenen Verzeichnis
- Jeder Workflow hat seine eigene CLAUDE.md und README.md
- Root-Verzeichnis enthält nur allgemeine Projektdateien
- Kein workflow-spezifischer Code im Root-Verzeichnis

### Dokumentationsstandards
- **README.md**: Benutzerseitige Dokumentation
  - Installationsanweisungen
  - Verwendungsbeispiele
  - Konfigurationsanleitung
  - Troubleshooting
- **CLAUDE.md**: Entwickleranleitung für Claude Code
  - Technische Architektur
  - Wesentliche Befehle
  - Entwicklungs-Workflow
  - Interne Implementierungsdetails

## Allgemeine Operationen für alle Workflows

### Allgemeiner Git-Workflow
```bash
# Status prüfen
git status

# Feature-Branch für neuen Workflow erstellen
git checkout -b workflow-name

# Änderungen committen
git add .
git commit -m "Add workflow-name implementation"

# Änderungen pushen
git push origin workflow-name
```

### n8n Workflow-Management
```bash
# Workflow in n8n importieren:
# 1. n8n Interface öffnen
# 2. Auf "+" klicken (Neuer Workflow)
# 3. Auf "..." → "Import from File" klicken
# 4. Workflow-JSON-Datei auswählen
# 5. Credentials konfigurieren
# 6. Workflow aktivieren

# Workflow aus n8n exportieren:
# 1. Workflow in n8n öffnen
# 2. Auf "..." → "Download" klicken
# 3. In entsprechendes Workflow-Verzeichnis speichern
```

### Datenbank-Operationen (PostgreSQL)
```bash
# Schema importieren
psql -U postgres -d n8n < workflow-name/database_schema.sql

# Datenbank sichern
pg_dump -U postgres -d n8n > backup.sql

# Tabelle als CSV exportieren
psql -U postgres -d n8n -c "\COPY table_name TO 'export.csv' CSV HEADER;"

# Tabellenstruktur anzeigen
psql -U postgres -d n8n -c "\d table_name"
```

### Python-Skript-Operationen (Allgemeines Muster)
```bash
# Zum Workflow-Verzeichnis navigieren
cd workflow-name/

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Dependencies installieren
pip install -r requirements.txt

# Environment einrichten
cp .env.example .env
# .env mit deiner Konfiguration bearbeiten

# Skript ausführen (variiert je Workflow)
python script_name.py --options
```

## Neuen Workflow hinzufügen

### Schritt-für-Schritt-Prozess

1. **Verzeichnisstruktur erstellen**
```bash
mkdir workflow-name
cd workflow-name
```

2. **Erforderliche Dateien erstellen**
```bash
touch README.md           # Benutzerdokumentation
touch CLAUDE.md           # Entwickleranleitung
touch .env.example        # Konfigurationsvorlage
touch requirements.txt    # Python Dependencies (falls benötigt)
```

3. **Workflow implementieren**
- n8n Workflow JSON-Export erstellen
- Oder Python/Node.js Skripte erstellen
- Datenbankschemas falls benötigt hinzufügen
- Setup-Skripte hinzufügen

4. **Dokumentation schreiben**
- **README.md**: Benutzerseitige Dokumentation
  - Was der Workflow macht
  - Voraussetzungen und Setup
  - Verwendungsanweisungen
  - Konfigurationsoptionen
  - Troubleshooting
- **CLAUDE.md**: Entwickleranleitung
  - Technische Architektur
  - Wesentliche Befehle
  - Entwicklungs-Workflow
  - Interne Details

5. **Root-Dateien aktualisieren**
- Workflow zur Root README.md hinzufügen
- Workflow-Referenz zur Root CLAUDE.md hinzufügen
- Projektstruktur-Diagramme aktualisieren

6. **Gründlich testen**
- Alle Skripte und Befehle testen
- Dokumentationsgenauigkeit überprüfen
- Auf sauberer Umgebung testen

## Workflow-spezifische Anleitung

### Für lead-generator Workflow
Siehe `lead-generator/CLAUDE.md` für:
- Lead-Scoring-Algorithmus Details
- Datenbankschema und Queries
- API-Integrationen (Google Maps, OpenAI, SMTP)
- E-Mail-Kampagnen-Management
- Kostenberechnungen und Optimierung

### Für zukünftige Workflows
Jeder Workflow wird seine eigene CLAUDE.md mit spezifischer Anleitung haben.

## Entwicklungs-Best-Practices

### Code-Qualität
- Konsistente Namenskonventionen verwenden
- Error-Handling hinzufügen
- Logging für Debugging einbauen
- Klare Kommentare schreiben
- Python PEP 8 oder JavaScript Standards befolgen

### Konfigurations-Management
- Niemals API-Keys oder Credentials committen
- `.env`-Dateien für sensible Daten verwenden
- `.env.example`-Vorlagen bereitstellen
- Alle erforderlichen Environment-Variablen dokumentieren

### Testing
- Zuerst mit kleinen Datensätzen testen
- API-Verbindungen vor vollständigen Läufen verifizieren
- Datenbank-Operationen überprüfen
- Error-Szenarien testen
- Rate-Limiting validieren

### Versionskontrolle
- Häufig committen mit klaren Nachrichten
- Workflow-JSON-Exports aktuell halten
- Stabile Releases taggen
- Breaking Changes dokumentieren
- Feature-Branches verwenden

## Troubleshooting (Allgemein)

### n8n Probleme
```bash
# n8n Logs prüfen
docker logs n8n  # wenn in Docker läuft

# n8n neustarten
docker restart n8n  # wenn in Docker läuft

# n8n Cache leeren
# n8n Interface → Settings → Clear cache
```

### Datenbank-Probleme
```bash
# PostgreSQL Status prüfen
sudo systemctl status postgresql

# PostgreSQL neustarten
sudo systemctl restart postgresql

# Verbindungen prüfen
psql -U postgres -d n8n -c "SELECT * FROM pg_stat_activity;"
```

### Python-Probleme
```bash
# Python-Version überprüfen
python3 --version

# Installierte Pakete prüfen
pip list

# Dependencies neu installieren
pip install -r requirements.txt --force-reinstall

# Virtuelle Umgebung prüfen
which python  # Sollte auf venv zeigen
```

## Projekt-Wartung

### Regelmäßige Aufgaben
- Dependencies monatlich aktualisieren
- Dokumentation überprüfen und aktualisieren
- Neueste n8n-Workflows exportieren
- Datenbanken sichern
- API-Nutzung und -Kosten überwachen
- Logs auf Fehler überprüfen

### Bevor neuer Workflow hinzugefügt wird
- Sicherstellen, dass Workflow-1 stabil ist
- Gesamte Dokumentation vervollständigen
- Aktuelle Version taggen
- Root README.md aktualisieren

## Nützliche Ressourcen

- **n8n Dokumentation**: https://docs.n8n.io/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Python Best Practices**: https://peps.python.org/pep-0008/
- **Git Guide**: https://git-scm.com/doc

## Kontakt & Support

Für workflow-spezifische Fragen siehe die individuelle CLAUDE.md-Datei des Workflows.

Für allgemeine Repository-Fragen:
- Email: martin.pfeffer@celox.io
- GitHub Issues: https://github.com/pepperonas/n8n-plygrnd/issues
