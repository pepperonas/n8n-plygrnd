# 🚀 Quick Reference - Lead Generation Workflow

## ⚡ Schnellstart-Befehle

### Python Skript
```bash
# Neue Kampagne starten
python lead_generation.py --campaign

# Follow-ups senden
python lead_generation.py --followup

# Statistiken anzeigen
python lead_generation.py --stats
```

### API & Dashboard
```bash
# API starten
python api.py

# Im Browser öffnen
# Dashboard: file:///pfad/zu/dashboard.html
# API: http://localhost:5000/api/stats
```

### Datenbank
```bash
# Leads anzeigen
psql -U postgres -d n8n -c "SELECT * FROM leads_email_campaign ORDER BY score DESC LIMIT 10;"

# Statistiken
psql -U postgres -d n8n -c "SELECT * FROM campaign_stats;"

# Export als CSV
psql -U postgres -d n8n -c "\COPY (SELECT * FROM leads_email_campaign) TO '/tmp/leads.csv' CSV HEADER;"
```

## 🔑 Wichtige API-Keys

### Google Maps API
- Console: https://console.cloud.google.com/
- APIs aktivieren: Places API, Maps JavaScript API
- Kosten: ~$17/1000 Anfragen (erste $200/Monat gratis)

### OpenAI API
- Dashboard: https://platform.openai.com/
- Model: gpt-4o-mini (günstig & effizient)
- Kosten: ~$0.50/100 E-Mails

### SMTP
```bash
# Gmail (Testing)
Host: smtp.gmail.com
Port: 587
User: deine-email@gmail.com
Pass: App-Passwort

# Mailgun (Production)
Host: smtp.mailgun.org
Port: 587
User: postmaster@deine-domain.de
```

## 📊 SQL Abfragen für Monitoring

```sql
-- Top 10 Leads
SELECT company_name, score, status, website 
FROM leads_email_campaign 
ORDER BY score DESC 
LIMIT 10;

-- Heute versendete E-Mails
SELECT COUNT(*) 
FROM leads_email_campaign 
WHERE DATE(sent_at) = CURRENT_DATE;

-- Response-Rate
SELECT 
    COUNT(*) as total,
    COUNT(CASE WHEN response_received THEN 1 END) as responses,
    ROUND(100.0 * COUNT(CASE WHEN response_received THEN 1 END) / COUNT(*), 2) as rate
FROM leads_email_campaign 
WHERE status = 'sent';

-- Noch nicht kontaktierte High-Potential Leads
SELECT company_name, score, website 
FROM leads_email_campaign 
WHERE status = 'pending' 
AND score > 50 
ORDER BY score DESC;

-- Follow-ups fällig
SELECT company_name, sent_at, followup_count 
FROM leads_email_campaign 
WHERE status = 'sent' 
AND sent_at < NOW() - INTERVAL '3 days'
AND followup_count < 2
AND response_received = FALSE;
```

## 🎯 Workflow-Konfiguration

### n8n Workflow
```javascript
// Lead-Scoring anpassen (in "Lead Scoring" Node)
const highPotentialKeywords = [
  'steuerberater',
  'immobilien',
  'personaldienstleister',
  // Füge weitere hinzu...
];

// Mindest-Score ändern
if (score >= 30) { // Erhöhe auf 40 oder 50 für höhere Qualität
  results.push(lead);
}
```

### Python Skript
```python
# In lead_generation.py, Zeile ~12-19
CONFIG = {
    'search_radius': 5000,  # Radius in Metern
    'max_emails_per_day': 20,  # Tages-Limit
    'delay_between_emails': 120,  # Pause in Sekunden
}
```

## 📧 E-Mail-Templates anpassen

### OpenAI Prompt (in GPT Node)
```
Erstelle eine E-Mail mit:
- Tonalität: [formal/locker/auf Augenhöhe]
- Länge: [kurz <100 Wörter / mittel 100-150 / lang >150]
- Call-to-Action: [Telefonat/Meeting/Demo/...]
- USP: [Was ist dein Alleinstellungsmerkmal?]
```

## 🔧 Troubleshooting

### Google API Fehler
```bash
# Test API-Key
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Restaurant&location=52.4797,13.4363&radius=1000&key=DEIN_KEY"

# Erwartete Antwort: {"results": [...], "status": "OK"}
```

### SMTP Fehler
```python
# Test SMTP-Verbindung
python3 << EOF
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('deine-email@gmail.com', 'app-passwort')
    print("✓ SMTP OK")
    server.quit()
except Exception as e:
    print(f"✗ Fehler: {e}")
EOF
```

### Datenbank-Verbindung testen
```bash
psql -U postgres -d n8n -c "SELECT version();"
```

## 📈 Optimale Versandzeiten

| Tag | Beste Zeit | Öffnungsrate |
|-----|-----------|--------------|
| Montag | 10:00-11:00 | Mittel |
| Dienstag | 9:00-11:00 | Hoch ⭐ |
| Mittwoch | 9:00-11:00 | Hoch ⭐ |
| Donnerstag | 9:00-11:00 | Hoch ⭐ |
| Freitag | 9:00-10:00 | Mittel |
| Wochenende | ❌ Vermeiden | Niedrig |

**Nachmittags-Slot:** 14:00-16:00 (Zweitbeste Zeit)

## 🎨 E-Mail-Personalisierung

### High-Impact Variablen
```
{{ company_name }}
{{ industry }}
{{ decision_maker }}
{{ location }}
{{ specific_pain_point }}
{{ custom_use_case }}
```

### Beispiel
```
Betreff: {{ company_name }} - KI-Automatisierung für {{ industry }}

Guten Tag {{ decision_maker }},

ich habe gesehen, dass {{ company_name }} in {{ location }} 
{{ specific_pain_point }} betreibt. 

Viele Unternehmen in Ihrer Branche sparen durch 
{{ custom_use_case }} bis zu 15 Stunden/Woche.

Interesse an einem 15-Min-Gespräch?

Beste Grüße,
Martin
```

## 🔐 Sicherheit & DSGVO

### Checklist
- [ ] Impressum in jeder E-Mail
- [ ] Opt-Out-Möglichkeit anbieten
- [ ] Datenquelle dokumentiert
- [ ] Interessensabwägung durchgeführt
- [ ] SSL/TLS für Datenbank-Verbindung
- [ ] API-Keys in .env (nicht in Git!)
- [ ] Regelmäßige Backups

### Opt-Out Template
```
---
Falls Sie keine weiteren Informationen wünschen, 
antworten Sie einfach mit "ABMELDEN".

Ihre Daten werden umgehend aus unserem System gelöscht.
```

## 📊 KPIs tracken

### Wichtigste Metriken
```
1. Lead-Qualität: Durchschnitts-Score > 50
2. E-Mail-Deliverability: > 95%
3. Öffnungsrate: > 30%
4. Response-Rate: > 5%
5. Meetings gebucht: > 2%
6. Conversion-Rate: > 0.5%
```

### Monitoring-Abfrage
```sql
SELECT 
    DATE(created_at) as date,
    AVG(score) as avg_score,
    COUNT(*) as total_leads,
    COUNT(CASE WHEN status='sent' THEN 1 END) as sent,
    COUNT(CASE WHEN response_received THEN 1 END) as responses
FROM leads_email_campaign
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

## 🚀 Skalierung

### Phase 1: Manuelle Qualität (Woche 1-2)
- 10-20 E-Mails/Tag
- Manuelle Review jeder E-Mail
- Feedback sammeln

### Phase 2: Semi-Automatisch (Woche 3-4)
- 30-50 E-Mails/Tag
- Stichproben-Kontrolle
- A/B-Testing

### Phase 3: Voll-Automatisch (Monat 2+)
- 50-100 E-Mails/Tag
- Monitoring via Dashboard
- Kontinuierliche Optimierung

## 🎓 Ressourcen

- n8n Community: https://community.n8n.io/
- Cold Email Guide: https://www.saleshandy.com/blog/cold-email-guide/
- DSGVO B2B: https://www.datenschutz.org/b2b-marketing/
- E-Mail Deliverability: https://www.mail-tester.com/

## ⚡ Hotkeys & Shortcuts

### n8n
- `Ctrl + S` - Workflow speichern
- `Ctrl + Enter` - Workflow ausführen
- `Ctrl + /` - Node-Suche

### psql
- `\dt` - Tabellen anzeigen
- `\d tablename` - Tabellenstruktur
- `\q` - Beenden

---

**Bei Fragen:** martin@celox.io | https://celox.io
