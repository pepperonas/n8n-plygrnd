# Setup-Anleitung: Neukölln Lead Generation Workflow

## 🚀 Schnellstart

### 1. Voraussetzungen
- n8n läuft auf deinem Server
- PostgreSQL Datenbank
- Google Maps API Key
- OpenAI API Key  
- SMTP-Server (z.B. Gmail, Mailgun, oder eigener Server)

### 2. Datenbank Setup

```bash
# Verbinde dich mit deiner PostgreSQL-Datenbank
psql -U dein_user -d deine_datenbank

# Führe das Schema aus
\i database_schema.sql
```

### 3. API-Keys einrichten

#### Google Maps API
1. Gehe zu: https://console.cloud.google.com/
2. Aktiviere "Places API" und "Maps JavaScript API"
3. Erstelle API-Key
4. Beschränke den Key auf deine Server-IP

**In n8n:**
- Gehe zu: Settings → Credentials
- Füge "Header Auth" hinzu
- Name: "Google Maps API"
- Header Name: `key`
- Value: `DEIN_API_KEY`

#### OpenAI API
1. Gehe zu: https://platform.openai.com/api-keys
2. Erstelle neuen API-Key
3. In n8n: Settings → Credentials → "OpenAI"
4. API Key eingeben

#### SMTP / Email
**Option A: Gmail (einfach für Tests)**
- App-Passwort erstellen: https://myaccount.google.com/apppasswords
- In n8n: SMTP Credentials
  - Host: smtp.gmail.com
  - Port: 587
  - User: deine-email@gmail.com
  - Password: App-Passwort

**Option B: Eigener SMTP-Server (professioneller)**
- Host: mail.celox.io
- Port: 587
- TLS aktivieren
- Authentifizierung: deine Credentials

### 4. Workflow importieren

```bash
# In n8n Web-Interface:
1. Klicke auf "+" (Neuer Workflow)
2. Klicke auf "..." → "Import from File"
3. Wähle: neukoelln_lead_workflow.json
4. Workflow wird importiert
```

### 5. Credentials zuweisen

Gehe durch jeden Node und weise die entsprechenden Credentials zu:
- **Google Places Search**: Google Maps API Credentials
- **Generate Personalized Email**: OpenAI Credentials
- **Generate Follow-up**: OpenAI Credentials
- **Save to Database**: PostgreSQL Credentials
- **Send Email**: SMTP Credentials
- **Get Follow-up Leads**: PostgreSQL Credentials

### 6. Anpassungen vornehmen

#### Wichtige Variablen zum Anpassen:

**Im "Google Places Search" Node:**
- `location`: Koordinaten von Neukölln (aktuell: 52.4797,13.4363)
- `radius`: Suchradius in Metern (aktuell: 5000m = 5km)

**Im "Lead Scoring" Node:**
- `highPotentialKeywords`: Füge weitere Branchen hinzu
- `score >= 30`: Ändere Mindest-Score

**Im "Generate Personalized Email" Node:**
- Ersetze "Martin" und "celox.io" mit deinen Daten
- Passe den System-Prompt an deine Tonalität an

**Im "Send Email" Node:**
- `fromEmail`: martin@celox.io → deine E-Mail
- Signatur anpassen

### 7. E-Mail-Extraktion verbessern

Der Workflow nutzt eine Fallback-Lösung für E-Mails:
```
info@[website-domain]
```

**Bessere Optionen:**
1. **Hunter.io API** integrieren (Email-Finder)
2. **LinkedIn Sales Navigator** (manuell)
3. **Snov.io API** für B2B-E-Mails
4. Manuelles Anrufen (höchste Erfolgsrate!)

### 8. Workflow testen

```bash
# Manueller Test-Durchlauf:
1. Öffne den Workflow
2. Klicke auf "Execute Workflow"
3. Überprüfe jeden Node-Output
4. Prüfe die Datenbank: SELECT * FROM leads_email_campaign;
```

**Wichtig für Tests:**
- Verwende erstmal eine kleine Suche (radius: 1000)
- Setze den Score-Filter hoch (>60)
- Teste mit deiner eigenen E-Mail als Empfänger

### 9. Produktiv-Modus aktivieren

```bash
# Empfohlene Settings für Live-Betrieb:
```

**Rate Limiting:**
- Max. 20 E-Mails pro Tag
- Pause zwischen E-Mails: 2-5 Minuten
- Vermeide Wochenenden

**Optimale Versandzeiten:**
- Dienstag - Donnerstag
- 9:00 - 11:00 Uhr oder 14:00 - 16:00 Uhr

**In n8n:** Füge einen "Split In Batches" Node hinzu:
- Batch Size: 20
- Zwischen Batches: 24 Stunden warten

### 10. Monitoring & Tracking

#### Dashboard-Abfragen (PostgreSQL):

```sql
-- Kampagnen-Übersicht
SELECT * FROM campaign_stats;

-- Beste Leads (noch nicht kontaktiert)
SELECT company_name, score, website 
FROM leads_email_campaign 
WHERE status = 'pending' 
ORDER BY score DESC 
LIMIT 10;

-- Response-Rate nach Branche
SELECT 
    SUBSTRING(address FROM 'Neukölln') as area,
    COUNT(*) as total,
    COUNT(CASE WHEN response_received THEN 1 END) as responses
FROM leads_email_campaign
WHERE status = 'sent'
GROUP BY area;
```

### 11. Rechtliche Absicherung

⚠️ **WICHTIG - Rechtliche Hinweise:**

**DSGVO-Compliance:**
- E-Mail-Adressen sind personenbezogene Daten
- Berechtigtes Interesse nach Art. 6 Abs. 1 lit. f DSGVO möglich
- Dokumentiere deine Interessensabwägung
- Biete einfachen Opt-Out an (in jeder E-Mail)

**UWG (Gesetz gegen unlauteren Wettbewerb):**
- § 7 UWG regelt unzumutbare Belästigung
- B2B Cold E-Mails sind rechtlich *möglich*, aber grenzwertig
- Telefon-Cold-Calls sind verboten (ohne Einwilligung)

**Empfehlungen:**
1. **Opt-Out in jeder E-Mail:**
   ```
   Falls Sie keine weiteren Informationen wünschen, 
   antworten Sie einfach mit "Abmelden".
   ```

2. **Impressum in jeder E-Mail** (Pflicht!)

3. **Dokumentation:** 
   - Speichere, wo du die Kontaktdaten gefunden hast
   - Dokumentiere dein berechtigtes Interesse

4. **Sichere Alternative:** 
   - LinkedIn InMail (mit Premium)
   - Kontakt über Website-Formular
   - Telefonische Kaltakquise nur mit Einwilligung

### 12. Optimierungen für bessere Ergebnisse

**A/B Testing:**
- Teste verschiedene Betreffzeilen
- Teste verschiedene Call-to-Actions
- Teste verschiedene Versandzeiten

**Personalisierung verbessern:**
- LinkedIn-Profil des Entscheiders recherchieren
- Aktuelle News über das Unternehmen erwähnen
- Spezifische Pain Points der Branche adressieren

**Nachfassen:**
- Follow-up nach 3 Tagen
- Follow-up nach 7 Tagen
- Maximal 2 Follow-ups (sonst Spam)

### 13. Fehlerbehebung

**Google Places API gibt keine Ergebnisse:**
- Prüfe API-Key und Quota
- Teste mit breiterer Suche
- Prüfe ob API aktiviert ist

**E-Mails kommen nicht an:**
- Prüfe Spam-Ordner
- Verwende SPF/DKIM/DMARC Records
- Starte mit kleiner Menge (5-10/Tag)
- Wärme deine E-Mail-Domain "auf"

**OpenAI API Fehler:**
- Prüfe Credits/Guthaben
- Prüfe Rate Limits
- Fallback auf günstigeres Modell (gpt-4o-mini)

**Workflow läuft nicht:**
- Prüfe Error-Log in n8n
- Aktiviere Debug-Modus
- Teste jeden Node einzeln

## 📊 Erwartete Ergebnisse

**Realistische Zahlen:**
- 100 recherchierte Unternehmen
- 40-60 Unternehmen mit Website
- 20-30 qualifizierte Leads (Score > 40)
- 15-25 versendete E-Mails
- 1-3 Antworten (5-10% Response-Rate)
- 0-1 Kunde (Conversion-Rate ~5%)

**Verbesserungen:**
- Mit LinkedIn-Recherche: ~15-20% Response
- Mit Telefon-Follow-up: ~30% Response
- Mit persönlicher Ansprache: ~40% Response

## 🎯 Nächste Schritte

1. ✅ Workflow importieren
2. ✅ Credentials einrichten
3. ✅ Datenbank erstellen
4. ⚠️ Mit Test-E-Mail testen
5. 🚀 Klein starten (5-10 Leads)
6. 📈 Optimieren basierend auf Daten
7. 💰 Skalieren

Viel Erfolg mit deiner Lead-Generation!

---

Bei Fragen oder Problemen:
- n8n Community Forum: https://community.n8n.io/
- n8n Dokumentation: https://docs.n8n.io/
