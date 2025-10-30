# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is an automated lead generation and email campaign system for identifying mid-sized businesses in Berlin-Neukölln with high AI automation potential. The project offers multiple implementation approaches:

1. **n8n Workflow** - Visual automation workflow (`lead-generator/neukoelln_lead_workflow.json`)
2. **Python Alternative** - Standalone CLI script (`lead-generator/lead_generation.py`)
3. **REST API + Dashboard** - Flask API with HTML monitoring interface

## Architecture Overview

### Data Flow
```
Google Places API → Lead Scoring → Website Analysis →
GPT-4 Email Generation → PostgreSQL Storage → SMTP Delivery →
Follow-up System
```

### Lead Scoring Algorithm
- Base scoring: 0-100 points
- High-potential industries: +30 points (tax consultants, real estate, recruiting, insurance, law firms)
- Good rating (>4.0): +10 points
- Established business (>20 reviews): +10 points
- Manual process indicators: +5 points each
- Modern website detected: -10 points
- Minimum threshold for outreach: 40 points

### Database Schema
- Main table: `leads_email_campaign` (PostgreSQL)
- Tracks: company info, scores, email content, status, follow-ups, responses
- View: `campaign_stats` for aggregated metrics
- Indexes on: status, sent_at, followup_count

## Essential Commands

### Python Script Operations
```bash
# Navigate to project directory
cd lead-generator/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Run new campaign
python lead_generation.py --campaign

# Send follow-ups
python lead_generation.py --followup

# View statistics
python lead_generation.py --stats
```

### Database Setup
```bash
# Create database and schema
psql -U postgres -d n8n < lead-generator/database_schema.sql

# View leads
psql -U postgres -d n8n -c "SELECT * FROM leads_email_campaign ORDER BY score DESC LIMIT 10;"

# View campaign statistics
psql -U postgres -d n8n -c "SELECT * FROM campaign_stats;"

# Export leads to CSV
psql -U postgres -d n8n -c "\COPY (SELECT * FROM leads_email_campaign) TO '/tmp/leads.csv' CSV HEADER;"
```

### API & Dashboard
```bash
# Start Flask API
cd lead-generator/
python api.py

# API runs on http://localhost:5000
# Endpoints: /api/stats, /api/leads, /api/leads/<id>

# Open dashboard.html in browser for monitoring
```

### Automated Setup
```bash
cd lead-generator/
chmod +x install.sh
./install.sh

# Setup cronjobs
chmod +x setup_cronjobs.sh
./setup_cronjobs.sh
# Schedules: Mon-Fri 9am (campaigns), Daily 2pm (follow-ups), Fri 6pm (reports)
```

## n8n Workflow Configuration

### Importing Workflow
1. Open n8n web interface
2. Click "+" (New Workflow)
3. Click "..." → "Import from File"
4. Select `lead-generator/neukoelln_lead_workflow.json`

### Required Credentials
- **Google Maps API**: Places API + Maps JavaScript API enabled
- **OpenAI API**: GPT-4o-mini model access
- **PostgreSQL**: Database connection
- **SMTP**: Email sending (Gmail with app password or Mailgun)

### Key Configuration Points
- **Search Parameters**: Location (52.4797,13.4363), radius (5000m)
- **Lead Scoring**: Adjust `HIGH_POTENTIAL_KEYWORDS` and minimum score threshold
- **Rate Limiting**: Max 20 emails/day, 2-5 minute delays between sends
- **Personalization**: Update sender name/email in "Generate Personalized Email" node

## API Keys & External Services

### Google Maps API
- Console: https://console.cloud.google.com/
- Enable: Places API, Maps JavaScript API
- Cost: ~$17 per 1000 requests (first $200/month free)

### OpenAI API
- Dashboard: https://platform.openai.com/
- Model: gpt-4o-mini (recommended for cost efficiency)
- Cost: ~$0.50 per 100 emails

### SMTP Options
**Gmail (Testing)**:
- Host: smtp.gmail.com, Port: 587
- Requires app password from https://myaccount.google.com/apppasswords

**Production Services**:
- Mailgun: 5000 emails/month free
- SendGrid: 100 emails/day free
- Amazon SES: Very low cost

## Critical Configuration

### Environment Variables (.env)
```
GOOGLE_MAPS_API_KEY=your_key
OPENAI_API_KEY=your_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@domain.com
SMTP_PASSWORD=your_app_password
DB_HOST=localhost
DB_NAME=n8n
DB_USER=postgres
DB_PASSWORD=your_db_password
```

### Python Script Configuration
In `lead_generation.py` lines 21-36:
- `search_location`: GPS coordinates for search center
- `search_radius`: Search radius in meters
- `max_emails_per_day`: Daily email limit (default: 20)
- `delay_between_emails`: Pause between sends in seconds

### Email Best Practices
- Send Tuesday-Thursday, 9-11am or 2-4pm (best open rates)
- Avoid weekends and Monday mornings
- Include opt-out option in every email
- Include full legal imprint (DSGVO/UWG compliance)
- Max 2 follow-ups per lead
- Personalize based on industry, location, specific pain points

## Development Workflow

### Testing
1. Start with small search radius (1000m) and high score threshold (>60)
2. Test with your own email as recipient
3. Verify database entries: `SELECT * FROM leads_email_campaign WHERE created_at > NOW() - INTERVAL '1 hour';`
4. Check n8n node outputs in execution log
5. Monitor SMTP deliverability with tools like mail-tester.com

### Common SQL Queries
```sql
-- Leads ready for follow-up
SELECT company_name, sent_at, followup_count
FROM leads_email_campaign
WHERE status = 'sent'
AND sent_at < NOW() - INTERVAL '3 days'
AND followup_count < 2
AND response_received = FALSE;

-- Response rate analysis
SELECT
    COUNT(*) as total,
    COUNT(CASE WHEN response_received THEN 1 END) as responses,
    ROUND(100.0 * COUNT(CASE WHEN response_received THEN 1 END) / COUNT(*), 2) as rate
FROM leads_email_campaign
WHERE status = 'sent';

-- Today's email count
SELECT COUNT(*)
FROM leads_email_campaign
WHERE DATE(sent_at) = CURRENT_DATE;
```

## Troubleshooting

### Google API Returns No Results
```bash
# Test API key
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Restaurant&location=52.4797,13.4363&radius=1000&key=YOUR_KEY"

# Check quota in Google Cloud Console → APIs → Places API → Quotas
```

### Emails Not Sending
```bash
# Test SMTP connection
python3 -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); print('OK')"

# Verify SPF/DKIM/DMARC records
# Test spam score at mail-tester.com
# "Warm up" domain by starting with low volume
```

### OpenAI API Errors
- Check balance at https://platform.openai.com/account/usage
- Tier 1 rate limit: 500 requests/minute
- Add delays between requests if hitting limits

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U postgres -d n8n -c "SELECT version();"

# Check if table exists
psql -U postgres -d n8n -c "\dt leads_email_campaign"
```

## Legal Compliance (DSGVO/UWG)

### Required Elements
- Opt-out option in every email footer
- Full legal imprint in email signature
- Document data sources and legitimate interest assessment
- B2B cold emails are legally possible but borderline under German law
- Phone cold calling requires explicit consent

### Opt-Out Template
```
Falls Sie keine weiteren Informationen wünschen,
antworten Sie einfach mit "ABMELDEN".
Ihre Daten werden umgehend aus unserem System gelöscht.
```

## Project Structure

```
n8n-plygrnd/
├── lead-generator/
│   ├── neukoelln_lead_workflow.json  # n8n visual workflow
│   ├── lead_generation.py            # Python standalone script
│   ├── api.py                        # Flask REST API
│   ├── dashboard.html                # HTML monitoring dashboard
│   ├── database_schema.sql           # PostgreSQL schema
│   ├── requirements.txt              # Python dependencies
│   ├── install.sh                    # Automated setup script
│   ├── setup_cronjobs.sh            # Cronjob automation
│   ├── README.md                     # Main documentation
│   ├── SETUP_ANLEITUNG.md           # Detailed setup guide
│   └── QUICK_REFERENCE.md           # Command reference
├── package.json                      # Node.js config (minimal)
└── index.js                          # Placeholder
```

## Expected Results & KPIs

**Realistic Benchmarks** (per 100 researched companies):
- Qualified leads (score >40): 30-40
- Emails sent: 20-25
- Open rate: 30-40%
- Response rate: 5-10%
- Meetings booked: 1-2
- Conversion to customers: ~5%

**Optimization Factors**:
- LinkedIn research before email: +50% response
- Phone follow-up: +100% response
- Hyper-personalization: +75% response
- Optimal send time (Tue-Thu, 9-11am): +20% opens

## Extension Ideas

### Hunter.io Integration (Email Finder)
```python
import pyhunter
hunter = pyhunter.PyHunter('YOUR_API_KEY')
email = hunter.email_finder('company-domain.com')
```

### LinkedIn Integration
```python
from linkedin_api import Linkedin
api = Linkedin('user@email.com', 'password')
profile = api.get_profile('company-name')
```

### Webhook for Email Responses
Add webhook node in n8n to automatically mark leads as "responded" when emails are received.