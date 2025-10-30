# 🎯 Neukölln Lead Generation & Email Campaign

Automatisierter Workflow zur Identifizierung von Mittelständlern in Neukölln mit hohem KI-Automatisierungspotenzial und personalisierten E-Mail-Kampagnen.

## 📦 Was ist enthalten?

### 1. n8n Workflow (neukoelln_lead_workflow.json)
Vollständiger visueller Workflow für n8n mit:
- Google Places API Integration
- Lead-Scoring-Algorithmus
- Website-Analyse
- GPT-4 E-Mail-Generierung
- Automatischer Follow-up System
- PostgreSQL-Tracking

### 2. Python Alternative (lead_generation.py)
Standalone Python-Skript mit identischer Funktionalität:
- Unabhängig von n8n lauffähig
- Command-line Interface
- Cronjob-fähig
- Voll konfigurierbar

### 3. API & Dashboard
- Flask REST API (api.py)
- HTML Dashboard (dashboard.html)
- Echtzeit-Statistiken
- Lead-Management

### 4. Datenbank
- PostgreSQL Schema (database_schema.sql)
- Optimierte Indizes
- Reporting Views

## 🚀 Quick Start

### Option A: n8n Workflow (Empfohlen)

```bash
# 1. Datenbank einrichten
psql -U postgres -d n8n < database_schema.sql

# 2. n8n öffnen und Workflow importieren
# Dashboard → Import from File → neukoelln_lead_workflow.json

# 3. Credentials konfigurieren
# - Google Maps API
# - OpenAI API
# - PostgreSQL
# - SMTP

# 4. Workflow aktivieren und testen
```

### Option B: Python Skript

```bash
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. Environment Variables setzen
cp .env.example .env
# Fülle .env mit deinen API-Keys

# 3. Datenbank einrichten
psql -U postgres -d n8n < database_schema.sql

# 4. Kampagne starten
python lead_generation.py --campaign

# 5. Follow-ups senden
python lead_generation.py --followup

# 6. Statistiken anzeigen
python lead_generation.py --stats
```

### Option C: Dashboard Setup

```bash
# 1. API starten
python api.py

# 2. Dashboard öffnen
# Öffne dashboard.html in Browser
# oder hoste mit nginx/Apache

# 3. Zugriff
# http://localhost:5000 - API
# http://localhost:8080 - Dashboard
```

## 🔑 API-Keys beschaffen

### Google Maps API
1. Gehe zu: https://console.cloud.google.com/
2. Erstelle neues Projekt
3. Aktiviere APIs:
   - Places API
   - Maps JavaScript API
4. Erstelle API-Key
5. Beschränke auf deine IP

**Kosten:** ~$17 pro 1000 Anfragen (erste $200/Monat gratis)

### OpenAI API
1. Gehe zu: https://platform.openai.com/
2. Erstelle Account
3. API-Key generieren
4. Guthaben aufladen

**Kosten:** ~$0.50 pro 100 E-Mails (GPT-4o-mini)

### SMTP
**Option 1: Gmail (Testing)**
```
Host: smtp.gmail.com
Port: 587
User: deine-email@gmail.com
Pass: App-Passwort (nicht dein normales Passwort!)
```

App-Passwort erstellen: https://myaccount.google.com/apppasswords

**Option 2: Eigener SMTP (Production)**
- Mailgun: https://www.mailgun.com/ (5000 E-Mails/Monat gratis)
- SendGrid: https://sendgrid.com/ (100 E-Mails/Tag gratis)
- Amazon SES: https://aws.amazon.com/ses/ (Sehr günstig)

## 📊 Workflow-Ablauf

```
1. OSINT Recherche
   ↓
2. Lead-Scoring (0-100 Punkte)
   ↓
3. Website-Analyse
   ↓
4. High-Potential Filter (>40 Punkte)
   ↓
5. Entscheider recherchieren
   ↓
6. Personalisierte E-Mail generieren (GPT-4)
   ↓
7. In Datenbank speichern
   ↓
8. E-Mail versenden (Rate-Limited)
   ↓
9. Status tracken
   ↓
10. Follow-up nach 3 Tagen
```

## 🎯 Lead-Scoring-Kriterien

| Kriterium | Punkte |
|-----------|--------|
| High-Potential Branche | +30 |
| Gutes Rating (>4.0) | +10 |
| Etabliert (>20 Reviews) | +10 |
| Manuelle Prozesse erkennbar | +5 pro Indikator |
| Moderne Website | -10 |

**Branchen mit hohem Potenzial:**
- Steuerberater / Buchhaltung
- Immobilienverwaltung
- Personaldienstleister / Recruiting
- Versicherungsmakler
- Rechtsanwälte / Kanzleien
- Marketing-Agenturen
- Logistik / Spedition

## 📧 E-Mail Best Practices

### ✅ DO's
- Personalisierung auf Branche & Unternehmen
- Konkrete Use-Cases nennen
- Klare Zeitersparnis quantifizieren
- Einfache Call-to-Action
- Impressum & Opt-Out anbieten
- Professioneller Ton auf Augenhöhe

### ❌ DON'Ts
- Keine generischen Templates
- Keine übertriebenen Versprechen
- Nicht zu viele E-Mails (Max 20/Tag)
- Keine Follow-ups nach 2 Versuchen
- Kein Spam-Verhalten

## ⚖️ Rechtliche Hinweise

**DSGVO-Compliance:**
- Personenbezogene Daten (E-Mail) werden verarbeitet
- Rechtsgrundlage: Berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO)
- Dokumentiere Interessensabwägung
- Biete einfachen Opt-Out an

**UWG-Konformität:**
- B2B Cold E-Mails sind möglich, aber grenzwertig
- Telefonische Kaltakquise verboten ohne Einwilligung
- Transparente Absenderangabe
- Impressumspflicht in jeder E-Mail

**Empfehlungen:**
1. ✅ Opt-Out in Signatur: "Bei Abmeldewunsch einfach antworten"
2. ✅ Vollständiges Impressum in E-Mail
3. ✅ Dokumentation der Datenquelle
4. ⚠️ Alternative: LinkedIn InMail (rechtlich sicherer)

## 📈 Erwartbare Ergebnisse

**Realistische Zahlen (basierend auf B2B-Benchmarks):**

| Metrik | Durchschnitt | Mit Optimierung |
|--------|--------------|-----------------|
| Recherchierte Unternehmen | 100 | 100 |
| Qualifizierte Leads | 30-40 | 40-50 |
| Versendete E-Mails | 20-25 | 25-30 |
| Öffnungsrate | 30-40% | 40-50% |
| Response-Rate | 5-10% | 10-20% |
| Meetings gebucht | 1-2 | 2-4 |
| Conversion zu Kunden | ~5% | ~10% |

**Optimierungsfaktoren:**
- ✨ LinkedIn-Recherche vor E-Mail: +50% Response
- 📞 Telefon-Follow-up: +100% Response
- 🎯 Hyper-Personalisierung: +75% Response
- ⏰ Optimale Versandzeit (Di-Do, 9-11 Uhr): +20% Öffnung

## 🛠️ Cronjob Setup

```bash
# Installation
chmod +x setup_cronjobs.sh
./setup_cronjobs.sh

# Cronjobs:
# - Montag-Freitag 9:00 Uhr: Neue Kampagne
# - Täglich 14:00 Uhr: Follow-ups
# - Freitag 18:00 Uhr: Wochenreport
```

## 🔧 Troubleshooting

### Problem: Google API gibt keine Ergebnisse
```bash
# Prüfe API-Key
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Restaurant&key=DEIN_KEY"

# Prüfe Quota
# Google Cloud Console → APIs → Places API → Quotas
```

### Problem: E-Mails kommen nicht an
```bash
# Prüfe SMTP-Verbindung
python -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); print('OK')"

# Tipps:
# - SPF/DKIM/DMARC konfigurieren
# - Domain "aufwärmen" (langsam starten)
# - Spam-Score testen: mail-tester.com
```

### Problem: OpenAI API Fehler
```bash
# Prüfe Guthaben
# https://platform.openai.com/account/usage

# Prüfe Rate Limits
# Tier 1: 500 requests/Minute
# Lösung: Pausen zwischen Requests
```

## 📁 Dateistruktur

```
lead-generation/
├── neukoelln_lead_workflow.json  # n8n Workflow
├── lead_generation.py            # Python Alternative
├── api.py                        # REST API
├── dashboard.html                # Monitoring Dashboard
├── database_schema.sql           # DB Schema
├── requirements.txt              # Python Deps
├── .env.example                  # Config Template
├── setup_cronjobs.sh            # Automatisierung
├── SETUP_ANLEITUNG.md           # Detaillierte Anleitung
└── README.md                     # Diese Datei
```

## 🔄 Workflow erweitern

### Hunter.io Integration (E-Mail-Finder)
```python
import pyhunter

hunter = pyhunter.PyHunter('YOUR_API_KEY')
email = hunter.email_finder('celox.io')
```

### LinkedIn Scraping
```python
# Mit linkedin-api Package
from linkedin_api import Linkedin

api = Linkedin('user@email.com', 'password')
profile = api.get_profile('company-name')
```

### Webhook für Antworten
```python
# In n8n: Webhook Node hinzufügen
# URL: https://dein-server.de/webhook/email-response
# Bei Antwort: Lead in DB als "responded" markieren
```

## 💡 Optimierungsideen

1. **Multi-Channel Approach**
   - E-Mail + LinkedIn Message
   - E-Mail + Telefon-Follow-up
   - Content Marketing + Retargeting

2. **A/B Testing**
   - Verschiedene Betreffzeilen
   - Verschiedene CTAs
   - Verschiedene Versandzeiten

3. **Lead-Enrichment**
   - LinkedIn Company Data
   - Crunchbase Funding Info
   - Technographie (welche Tools nutzen sie?)

4. **Automatisierte Qualification**
   - Chatbot auf Website
   - Terminbuchungs-Link in E-Mail
   - Qualification-Fragebogen

## 🎓 Weiterführende Ressourcen

- n8n Dokumentation: https://docs.n8n.io/
- Google Places API: https://developers.google.com/maps/documentation/places/web-service
- OpenAI API: https://platform.openai.com/docs/
- DSGVO B2B: https://www.datenschutz.org/b2b-marketing/
- Cold Email Best Practices: https://www.saleshandy.com/blog/cold-email-best-practices/

## 📞 Support

Bei Fragen oder Problemen:
- n8n Community: https://community.n8n.io/
- GitHub Issues: [Dein Repo]
- E-Mail: martin@celox.io

## 📄 Lizenz

MIT License - Frei verwendbar für kommerzielle Projekte.

---

**Viel Erfolg mit deiner Lead-Generation! 🚀**

Made with ❤️ in Berlin-Neukölln
