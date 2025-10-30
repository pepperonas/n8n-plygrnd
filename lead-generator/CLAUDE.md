# CLAUDE.md - Lead Generator

Diese Datei bietet Anleitung für Claude Code (claude.ai/code) bei der Arbeit mit dem Lead-Generierungs-Workflow in diesem Verzeichnis.

## Projektkontext

Dies ist ein automatisiertes Lead-Generierungs- und E-Mail-Kampagnensystem zur Identifizierung mittelständischer Unternehmen in Berlin-Neukölln mit hohem KI-Automatisierungspotenzial. Das Projekt bietet mehrere Implementierungsansätze:

1. **n8n Workflow** - Visueller Automatisierungs-Workflow (`neukoelln_lead_workflow.json`)
2. **Python Alternative** - Standalone CLI-Skript (`lead_generation.py`)
3. **REST API + Dashboard** - Flask API mit HTML-Monitoring-Interface

## Architektur-Übersicht

### Datenfluss
```
Google Places API → Lead-Scoring → Website-Analyse →
GPT-4 E-Mail-Generierung → PostgreSQL Speicherung → SMTP Versand →
Follow-up System
```

### Lead-Scoring-Algorithmus
- Basis-Scoring: 0-100 Punkte
- High-Potential Branchen: +30 Punkte (Steuerberater, Immobilien, Recruiting, Versicherung, Kanzleien)
- Gutes Rating (>4.0): +10 Punkte
- Etabliertes Unternehmen (>20 Bewertungen): +10 Punkte
- Manuelle Prozess-Indikatoren: +5 Punkte je Indikator
- Moderne Website erkannt: -10 Punkte
- Minimum-Schwellenwert für Ansprache: 40 Punkte

### Datenbankschema
- Haupt-Tabelle: `leads_email_campaign` (PostgreSQL)
- Tracking: Firmeninfo, Scores, E-Mail-Inhalte, Status, Follow-ups, Antworten
- View: `campaign_stats` für aggregierte Metriken
- Indizes auf: status, sent_at, followup_count

## Wesentliche Befehle

### Python-Skript-Operationen
```bash
# Zum Projektverzeichnis navigieren
cd lead-generator/

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate  # Auf macOS/Linux
# venv\Scripts\activate   # Auf Windows

# Dependencies installieren
pip install -r requirements.txt

# Environment-Variablen einrichten
cp .env.example .env
# .env mit deinen API-Keys bearbeiten

# Neue Kampagne starten
python lead_generation.py --campaign

# Follow-ups senden
python lead_generation.py --followup

# Statistiken anzeigen
python lead_generation.py --stats
```

### Datenbank-Setup
```bash
# Datenbank und Schema erstellen
psql -U postgres -d n8n < database_schema.sql

# Leads anzeigen
psql -U postgres -d n8n -c "SELECT * FROM leads_email_campaign ORDER BY score DESC LIMIT 10;"

# Kampagnen-Statistiken anzeigen
psql -U postgres -d n8n -c "SELECT * FROM campaign_stats;"

# Leads als CSV exportieren
psql -U postgres -d n8n -c "\COPY (SELECT * FROM leads_email_campaign) TO '/tmp/leads.csv' CSV HEADER;"
```

### API & Dashboard
```bash
# Flask API starten
cd lead-generator/
python api.py

# API läuft auf http://localhost:5000
# Endpoints: /api/stats, /api/leads, /api/leads/<id>

# dashboard.html im Browser öffnen für Monitoring
```

### Automatisiertes Setup
```bash
cd lead-generator/
chmod +x install.sh
./install.sh

# Cronjobs einrichten
chmod +x setup_cronjobs.sh
./setup_cronjobs.sh
# Zeitplan: Mo-Fr 9 Uhr (Kampagnen), Täglich 14 Uhr (Follow-ups), Fr 18 Uhr (Reports)
```

## n8n Workflow-Konfiguration

### Workflow importieren
1. n8n Web-Interface öffnen
2. Auf "+" klicken (Neuer Workflow)
3. Auf "..." → "Import from File" klicken
4. `neukoelln_lead_workflow.json` auswählen

### Erforderliche Credentials
- **Google Maps API**: Places API + Maps JavaScript API aktiviert
- **OpenAI API**: GPT-4o-mini Modellzugriff
- **PostgreSQL**: Datenbankverbindung
- **SMTP**: E-Mail-Versand (Gmail mit App-Passwort oder Mailgun)

### Wichtige Konfigurationspunkte
- **Suchparameter**: Location (52.4797,13.4363), Radius (5000m)
- **Lead-Scoring**: `HIGH_POTENTIAL_KEYWORDS` und Minimum-Score-Schwellenwert anpassen
- **Rate-Limiting**: Max 20 E-Mails/Tag, 2-5 Minuten Verzögerung zwischen Sendungen
- **Personalisierung**: Absendername/-E-Mail im "Generate Personalized Email" Node aktualisieren

## API-Keys & Externe Services

### Google Maps API (Places API)
- Console: https://console.cloud.google.com/
- Aktivieren: Places API, Maps JavaScript API
- **Kostenstruktur (Stand März 2025)**:
  - **Free Tier**: 10.000 Anfragen/Monat für "Essentials" SKUs (beinhaltet Places API)
  - **Bezahlt**: $17 pro 1.000 Basic Place Details Anfragen
  - **Echte Kosten Beispiel**: Du kannst 10.000 Unternehmen pro Monat komplett kostenlos finden!

### OpenAI API
- Dashboard: https://platform.openai.com/
- Modell: gpt-4o-mini (empfohlen für Kosteneffizienz)
- **Kostenstruktur**:
  - Input: $0.15 pro 1M Tokens
  - Output: $0.60 pro 1M Tokens
  - **Echte Kosten Beispiel**:
    - 100 E-Mails (~50k Input + 30k Output Tokens) = $0.026 (NICHT $0.50!)
    - 1.000 E-Mails = ~$0.26
  - Viel günstiger als anfangs geschätzt!

### Zusammenfassung: 10.000 Unternehmen/Monat
- **Google API**: KOSTENLOS (innerhalb Free Tier)
- **E-Mail-Generierung (10.000 E-Mails)**: ~$2.60
- **Gesamt**: ~$2.60/Monat für 10.000 Leads! 🎉

### Rate-Limiting
- **Places API**: Mehrere hundert Anfragen pro Minute (prüfe dein spezifisches Projekt-Quota)
- **GPT-4o-mini**: Tausende Anfragen pro Minute (Tier 1)
- Deine Limits in den jeweiligen Dashboards einsehen

### SMTP-Optionen
**Gmail (Testing)**:
- Host: smtp.gmail.com, Port: 587
- Benötigt App-Passwort von https://myaccount.google.com/apppasswords

**Produktions-Services**:
- Mailgun: 5000 E-Mails/Monat kostenlos
- SendGrid: 100 E-Mails/Tag kostenlos
- Amazon SES: Sehr niedrige Kosten

## Kritische Konfiguration

### Environment-Variablen (.env)
```
GOOGLE_MAPS_API_KEY=dein_key
OPENAI_API_KEY=dein_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=deine-email@domain.com
SMTP_PASSWORD=dein_app_passwort
DB_HOST=localhost
DB_NAME=n8n
DB_USER=postgres
DB_PASSWORD=dein_db_passwort
```

### Python-Skript-Konfiguration
In `lead_generation.py` Zeilen 21-36:
- `search_location`: GPS-Koordinaten für Suchzentrum
- `search_radius`: Suchradius in Metern
- `max_emails_per_day`: Tägliches E-Mail-Limit (Standard: 20)
- `delay_between_emails`: Pause zwischen Sendungen in Sekunden

### E-Mail Best Practices
- Versand Dienstag-Donnerstag, 9-11 Uhr oder 14-16 Uhr (beste Öffnungsraten)
- Wochenenden und Montagmorgen vermeiden
- Opt-out Option in jeder E-Mail einbinden
- Vollständiges Impressum (DSGVO/UWG-Konformität)
- Max 2 Follow-ups pro Lead
- Personalisierung basierend auf Branche, Standort, spezifischen Schmerzpunkten

## Entwicklungs-Workflow

### Testing
1. Mit kleinem Suchradius (1000m) und hohem Score-Schwellenwert (>60) starten
2. Mit eigener E-Mail als Empfänger testen
3. Datenbankeinträge verifizieren: `SELECT * FROM leads_email_campaign WHERE created_at > NOW() - INTERVAL '1 hour';`
4. n8n Node-Outputs im Execution-Log prüfen
5. SMTP-Zustellbarkeit mit Tools wie mail-tester.com überwachen

### Häufige SQL-Queries
```sql
-- Leads bereit für Follow-up
SELECT company_name, sent_at, followup_count
FROM leads_email_campaign
WHERE status = 'sent'
AND sent_at < NOW() - INTERVAL '3 days'
AND followup_count < 2
AND response_received = FALSE;

-- Response-Rate Analyse
SELECT
    COUNT(*) as total,
    COUNT(CASE WHEN response_received THEN 1 END) as responses,
    ROUND(100.0 * COUNT(CASE WHEN response_received THEN 1 END) / COUNT(*), 2) as rate
FROM leads_email_campaign
WHERE status = 'sent';

-- Heutige E-Mail-Anzahl
SELECT COUNT(*)
FROM leads_email_campaign
WHERE DATE(sent_at) = CURRENT_DATE;
```

## Troubleshooting

### Google API gibt keine Ergebnisse zurück
```bash
# API-Key testen
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Restaurant&location=52.4797,13.4363&radius=1000&key=DEIN_KEY"

# Quota in Google Cloud Console prüfen → APIs → Places API → Quotas
```

### E-Mails werden nicht versendet
```bash
# SMTP-Verbindung testen
python3 -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); print('OK')"

# SPF/DKIM/DMARC Records verifizieren
# Spam-Score testen bei mail-tester.com
# Domain "aufwärmen" durch niedrige Anfangsvolumina
```

### OpenAI API Fehler
- Guthaben prüfen bei https://platform.openai.com/account/usage
- Tier 1 Rate-Limit: 500 Anfragen/Minute
- Verzögerungen zwischen Anfragen hinzufügen falls Limits erreicht werden

### Datenbankverbindungs-Probleme
```bash
# PostgreSQL-Verbindung testen
psql -U postgres -d n8n -c "SELECT version();"

# Prüfen ob Tabelle existiert
psql -U postgres -d n8n -c "\dt leads_email_campaign"
```

## Rechtliche Compliance (DSGVO/UWG)

### Erforderliche Elemente
- Opt-out Option in jedem E-Mail-Footer
- Vollständiges Impressum in E-Mail-Signatur
- Datenquellen und Interessenabwägung dokumentieren
- B2B Cold-E-Mails sind rechtlich möglich aber grenzwertig unter deutschem Recht
- Telefonische Kaltakquise benötigt explizite Einwilligung

### Opt-Out Template
```
Falls Sie keine weiteren Informationen wünschen,
antworten Sie einfach mit "ABMELDEN".
Ihre Daten werden umgehend aus unserem System gelöscht.
```

## Projektstruktur

```
lead-generator/
├── neukoelln_lead_workflow.json  # n8n visueller Workflow
├── lead_generation.py            # Python Standalone-Skript
├── api.py                        # Flask REST API
├── dashboard.html                # HTML Monitoring-Dashboard
├── database_schema.sql           # PostgreSQL Schema
├── requirements.txt              # Python Dependencies
├── install.sh                    # Automatisiertes Setup-Skript
├── setup_cronjobs.sh            # Cronjob-Automatisierung
├── README.md                     # Haupt-Dokumentation
├── SETUP_ANLEITUNG.md           # Detaillierte Setup-Anleitung (Deutsch)
├── QUICK_REFERENCE.md           # Befehls-Referenz
└── CLAUDE.md                    # Diese Datei
```

## Erwartete Ergebnisse & KPIs

**Realistische Benchmarks** (pro 100 recherchierte Unternehmen):
- Qualifizierte Leads (Score >40): 30-40
- Versendete E-Mails: 20-25
- Öffnungsrate: 30-40%
- Response-Rate: 5-10%
- Gebuchte Meetings: 1-2
- Conversion zu Kunden: ~5%

**Optimierungsfaktoren**:
- LinkedIn-Recherche vor E-Mail: +50% Response
- Telefon-Follow-up: +100% Response
- Hyper-Personalisierung: +75% Response
- Optimale Versandzeit (Di-Do, 9-11 Uhr): +20% Öffnungen

## Erweiterungs-Ideen

### Hunter.io Integration (E-Mail-Finder)
```python
import pyhunter
hunter = pyhunter.PyHunter('DEIN_API_KEY')
email = hunter.email_finder('firma-domain.com')
```

### LinkedIn Integration
```python
from linkedin_api import Linkedin
api = Linkedin('user@email.com', 'passwort')
profile = api.get_profile('firmen-name')
```

### Webhook für E-Mail-Antworten
Webhook-Node in n8n hinzufügen, um automatisch Leads als "responded" zu markieren, wenn E-Mails empfangen werden.
