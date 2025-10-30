# n8n Workflows Playground

Eine Sammlung von n8n-Automatisierungs-Workflows für verschiedene Business-Automatisierungsaufgaben. Jeder Workflow ist eigenständig und produktionsbereit.

## 🎯 Überblick

Dieses Repository dient als Playground für die Entwicklung und das Testen mehrerer n8n-Automatisierungs-Workflows. Jedes Workflow-Verzeichnis enthält alles, was zum Deployment und zur Ausführung dieser spezifischen Automatisierung benötigt wird.

## 📦 Verfügbare Workflows

### 1. Lead Generator (`lead-generator/`)

Automatisiertes B2B-Lead-Generierungs- und E-Mail-Kampagnensystem zur Identifizierung von Unternehmen mit hohem KI-Automatisierungspotenzial.

**Features**:
- Google Places API Integration zur Unternehmensrecherche
- Intelligentes Lead-Scoring (0-100 Punkte)
- KI-gestützte E-Mail-Personalisierung mit GPT-4
- Automatische Follow-up-Sequenzen
- PostgreSQL Tracking und Analytics
- DSGVO/UWG-konform

**Implementierungsoptionen**:
- n8n visueller Workflow
- Python Standalone-Skript
- REST API + Dashboard

**Dokumentation**: Siehe [lead-generator/README.md](lead-generator/README.md) für vollständige Setup-Anleitung

**Quick Start**:
```bash
cd lead-generator
./install.sh  # Automatisches Setup
python lead_generation.py --campaign
```

---

### 2. [Zukünftiger Workflow]

Demnächst verfügbar...

---

### 3. [Zukünftiger Workflow]

Demnächst verfügbar...

## 🏗️ Projektstruktur

```
n8n-plygrnd/
├── README.md                    # Diese Datei - Projektübersicht
├── CLAUDE.md                    # Claude Code Entwicklungsanleitung
├── package.json                 # Node.js Konfiguration
├── index.js                     # Entry Point
│
├── lead-generator/              # Lead-Generierungs-Workflow
│   ├── README.md               # Detaillierte Dokumentation
│   ├── CLAUDE.md               # Workflow-spezifische Entwickleranleitung
│   ├── neukoelln_lead_workflow.json
│   ├── lead_generation.py
│   ├── api.py
│   ├── dashboard.html
│   ├── database_schema.sql
│   ├── requirements.txt
│   ├── install.sh
│   └── ...
│
├── [workflow-2]/                # Zukünftiger Workflow
│   ├── README.md
│   ├── CLAUDE.md
│   └── ...
│
└── [workflow-3]/                # Zukünftiger Workflow
    ├── README.md
    ├── CLAUDE.md
    └── ...
```

## 🚀 Erste Schritte

### Voraussetzungen

- **n8n**: Laufende Instanz (self-hosted oder cloud)
- **Python 3.8+**: Für Standalone-Skripte
- **PostgreSQL**: Datenbank für Datenpersistenz
- **API Keys**: Variiert je Workflow (Google Maps, OpenAI, etc.)

### Installation

```bash
# Repository klonen
git clone https://github.com/pepperonas/n8n-plygrnd.git
cd n8n-plygrnd

# Zum spezifischen Workflow navigieren
cd lead-generator

# Workflow-spezifische README.md befolgen
```

## 📖 Dokumentationsstruktur

Jedes Workflow-Verzeichnis enthält:

- **README.md** - Benutzerdokumentation mit Setup-Anweisungen
- **CLAUDE.md** - Entwickleranleitung für Claude Code mit technischen Details
- **Workflow-Dateien** - n8n JSON-Exports und/oder Python-Skripte
- **Datenbankschemas** - SQL-Setup-Skripte falls benötigt
- **Konfigurationsvorlagen** - `.env.example` Dateien

## 🛠️ Entwicklungs-Workflow

### Neuen Workflow hinzufügen

1. Neues Verzeichnis erstellen: `mkdir workflow-name/`
2. Workflow-Dateien und Dokumentation hinzufügen:
   - `README.md` - Benutzerdokumentation
   - `CLAUDE.md` - Entwickleranleitung
   - Workflow-Implementierungsdateien
   - Datenbankschemas falls benötigt
   - Konfigurationsvorlagen
3. Root README mit Workflow-Zusammenfassung aktualisieren
4. Root CLAUDE.md bei Bedarf aktualisieren

### Arbeiten mit Claude Code

Jeder Workflow hat seine eigene `CLAUDE.md` Datei mit:
- Technischen Architekturdetails
- Wesentlichen Befehlen und Operationen
- Konfigurationsspezifika
- Troubleshooting-Anleitungen
- Entwicklungs-Workflows

Siehe individuelle Workflow-Verzeichnisse für Details.

## 🔧 Allgemeine Operationen

### n8n Workflow Import

```bash
# 1. n8n Interface öffnen
# 2. Auf "+" klicken (Neuer Workflow)
# 3. Auf "..." → "Import from File" klicken
# 4. Workflow-JSON-Datei auswählen
# 5. Credentials konfigurieren
# 6. Workflow aktivieren
```

### Datenbank-Operationen

```bash
# Schema importieren
psql -U postgres -d n8n < workflow-name/database_schema.sql

# Daten sichern
pg_dump -U postgres -d n8n -t table_name > backup.sql

# Als CSV exportieren
psql -U postgres -d n8n -c "\COPY table_name TO 'export.csv' CSV HEADER;"
```

### Python-Skript-Operationen

```bash
# Virtuelle Umgebung einrichten
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Dependencies installieren
pip install -r requirements.txt

# Skript ausführen
python script_name.py --options
```

## 📊 Workflow-Vergleich

| Workflow | Typ | Komplexität | Voraussetzungen | Anwendungsfall |
|----------|------|------------|----------------|----------------|
| Lead Generator | B2B Automation | Mittel | Google API, OpenAI, SMTP | Automatisierte Kundenakquise |
| [Workflow 2] | TBD | TBD | TBD | TBD |
| [Workflow 3] | TBD | TBD | TBD | TBD |

## 🎓 Best Practices

### Workflow-Design
- Workflows modular und eigenständig halten
- Umfassendes Error-Handling einbauen
- Logging für Debugging hinzufügen
- Environment-Variablen für Konfiguration verwenden
- Rate-Limiting für externe APIs implementieren

### Dokumentation
- Immer sowohl README.md als auch CLAUDE.md bereitstellen
- Alle benötigten API-Keys und Credentials dokumentieren
- Funktionierende Beispiele und Test-Befehle bereitstellen
- Troubleshooting-Sektion einbeziehen

### Versionskontrolle
- Workflow-JSON-Exports regelmäßig committen
- Semantic Versioning für Releases verwenden
- Stabile Versionen taggen
- Breaking Changes dokumentieren

## 💡 Mitwirken

Um einen neuen Workflow hinzuzufügen:

1. Workflow-Verzeichnis erstellen
2. Funktionalität implementieren
3. Umfassende Dokumentation hinzufügen
4. Gründlich testen
5. Pull Request einreichen

## 📞 Support

- **Issues**: https://github.com/pepperonas/n8n-plygrnd/issues
- **n8n Community**: https://community.n8n.io/
- **Email**: martin.pfeffer@celox.io

## 👨‍💻 Entwickler

**Martin Pfeffer**
[celox.io](https://celox.io) | martin.pfeffer@celox.io
© 2025

## 📄 Lizenz

MIT License - Frei verwendbar für kommerzielle Projekte

---

**Made with ❤️ in Berlin**

🚀 Viel Erfolg beim Automatisieren!