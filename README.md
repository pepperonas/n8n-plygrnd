# n8n Playground - Lead Generation System

Automated lead generation and email campaign system for identifying mid-sized businesses with high AI automation potential.

## 🎯 Overview

This repository contains a complete B2B lead generation workflow that:
- Searches for businesses using Google Places API
- Scores leads based on automation potential (0-100 points)
- Analyzes company websites for manual processes
- Generates personalized outreach emails with GPT-4
- Tracks campaigns and responses in PostgreSQL
- Automates follow-up sequences

## 📦 What's Included

### Implementation Options

1. **n8n Visual Workflow** - Drag-and-drop automation (recommended for non-developers)
2. **Python Standalone Script** - CLI tool that can run independently
3. **REST API + Dashboard** - Flask API with real-time monitoring interface

### Key Features

- **Intelligent Lead Scoring**: Prioritizes high-value prospects based on industry, ratings, and online presence
- **AI-Powered Personalization**: GPT-4 generates custom emails for each prospect
- **Automated Follow-ups**: Sends up to 2 follow-up emails after 3 and 7 days
- **Rate Limiting**: Respects best practices (max 20 emails/day with delays)
- **Response Tracking**: Monitors open rates, responses, and conversions
- **DSGVO Compliant**: Built-in opt-out and legal compliance features

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- n8n instance (for workflow option)
- API keys: Google Maps, OpenAI, SMTP credentials

### Installation

```bash
# Clone repository
git clone https://github.com/pepperonas/n8n-plygrnd.git
cd n8n-plygrnd

# Navigate to lead generation project
cd lead-generator

# Run automated setup (Linux/macOS)
chmod +x install.sh
./install.sh

# Or manual setup:
pip install -r requirements.txt
psql -U postgres -d n8n < database_schema.sql
cp .env.example .env  # Configure your API keys
```

### Usage

```bash
# Python Script
python lead_generation.py --campaign    # Start new campaign
python lead_generation.py --followup    # Send follow-ups
python lead_generation.py --stats       # View statistics

# API + Dashboard
python api.py                           # Start REST API on :5000
# Open dashboard.html in browser

# n8n Workflow
# Import neukoelln_lead_workflow.json in n8n interface
# Configure credentials and activate workflow
```

## 📊 Architecture

```
Google Places API
       ↓
Lead Scoring Algorithm (0-100 points)
       ↓
Website Analysis
       ↓
High-Potential Filter (>40 points)
       ↓
GPT-4 Email Generation
       ↓
PostgreSQL Storage
       ↓
SMTP Delivery (rate-limited)
       ↓
Follow-up System
```

### Lead Scoring Criteria

| Criterion | Points |
|-----------|--------|
| High-potential industry (tax, real estate, recruiting, insurance, law) | +30 |
| Good rating (>4.0 stars) | +10 |
| Established business (>20 reviews) | +10 |
| Manual process indicators detected | +5 each |
| Modern website with automation | -10 |

**Threshold**: Only leads with score >40 receive outreach emails

## 📈 Expected Results

Based on B2B benchmarks for 100 researched companies:

| Metric | Average | With Optimization |
|--------|---------|-------------------|
| Qualified Leads | 30-40 | 40-50 |
| Emails Sent | 20-25 | 25-30 |
| Open Rate | 30-40% | 40-50% |
| Response Rate | 5-10% | 10-20% |
| Meetings Booked | 1-2 | 2-4 |
| Conversion Rate | ~5% | ~10% |

**Optimization Factors**:
- LinkedIn research before email: +50% response rate
- Phone follow-up: +100% response rate
- Hyper-personalization: +75% response rate
- Optimal send time (Tue-Thu, 9-11am): +20% open rate

## 🔑 Required API Keys

### Google Maps API
- **Console**: https://console.cloud.google.com/
- **APIs to enable**: Places API, Maps JavaScript API
- **Cost**: ~$17 per 1000 requests (first $200/month free)

### OpenAI API
- **Dashboard**: https://platform.openai.com/
- **Model**: gpt-4o-mini (cost-effective)
- **Cost**: ~$0.50 per 100 emails

### SMTP
- **Gmail** (testing): smtp.gmail.com:587 with app password
- **Mailgun** (production): 5000 emails/month free
- **SendGrid** (production): 100 emails/day free
- **Amazon SES** (production): Very low cost

## 📁 Project Structure

```
n8n-plygrnd/
├── README.md                          # This file
├── CLAUDE.md                          # Instructions for Claude Code
├── lead-generator/                    # Main lead generation project
│   ├── neukoelln_lead_workflow.json  # n8n visual workflow
│   ├── lead_generation.py            # Python standalone script
│   ├── api.py                        # Flask REST API
│   ├── dashboard.html                # Monitoring dashboard
│   ├── database_schema.sql           # PostgreSQL schema
│   ├── requirements.txt              # Python dependencies
│   ├── install.sh                    # Automated setup
│   ├── setup_cronjobs.sh            # Cronjob automation
│   ├── README.md                     # Detailed documentation
│   ├── SETUP_ANLEITUNG.md           # Setup guide (German)
│   └── QUICK_REFERENCE.md           # Command reference
├── package.json
└── index.js
```

## 📖 Documentation

- **[Detailed README](lead-generator/README.md)** - Complete feature overview and examples
- **[Setup Guide](lead-generator/SETUP_ANLEITUNG.md)** - Step-by-step installation (German)
- **[Quick Reference](lead-generator/QUICK_REFERENCE.md)** - Command cheat sheet
- **[CLAUDE.md](CLAUDE.md)** - Developer guide for Claude Code

## ⚖️ Legal Compliance

### DSGVO (GDPR)
- Personal data (emails) is processed under legitimate interest (Art. 6 para. 1 lit. f DSGVO)
- Opt-out option provided in every email
- Data source documentation included
- Easy deletion upon request

### UWG (German Unfair Competition Law)
- B2B cold emails are legally possible but borderline
- Phone cold calling requires explicit consent
- Full legal imprint required in every email
- Maximum 2 follow-ups to avoid spam classification

**Safer Alternatives**: LinkedIn InMail, website contact forms, or phone calls with prior consent

## 🔧 Common Commands

```bash
# Database queries
psql -U postgres -d n8n -c "SELECT * FROM leads_email_campaign ORDER BY score DESC LIMIT 10;"
psql -U postgres -d n8n -c "SELECT * FROM campaign_stats;"

# Test Google API
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Restaurant&location=52.4797,13.4363&radius=1000&key=YOUR_KEY"

# Test SMTP connection
python3 -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); print('OK')"

# Setup cronjobs (automated campaigns)
cd lead-generator && chmod +x setup_cronjobs.sh && ./setup_cronjobs.sh
```

## 🛠️ Troubleshooting

### Google API returns no results
- Check API key and quota in Google Cloud Console
- Verify Places API is enabled
- Test with broader search parameters

### Emails not being delivered
- Verify SMTP credentials
- Configure SPF/DKIM/DMARC records
- Start with low volume (5-10/day) to "warm up" domain
- Test spam score at mail-tester.com

### OpenAI API errors
- Check account balance at https://platform.openai.com/account/usage
- Verify rate limits (Tier 1: 500 requests/minute)
- Add delays between requests if hitting limits

## 🎓 Best Practices

### Email Campaign Tips
- Send Tuesday-Thursday between 9-11am for best open rates
- Personalize based on industry-specific pain points
- Keep emails under 150 words with clear call-to-action
- Include full legal imprint and opt-out instructions
- Limit to 20 emails per day maximum
- Wait 3 days between follow-ups, max 2 follow-ups total

### Lead Quality
- Focus on high-scoring leads (>50 points) first
- Research decision-makers on LinkedIn before sending
- Reference specific company details in emails
- Mention current industry trends or challenges

## 💡 Extension Ideas

- **Hunter.io Integration**: Automatic email address discovery
- **LinkedIn Scraping**: Enrich leads with company and decision-maker data
- **Webhook System**: Track email opens and clicks in real-time
- **A/B Testing**: Test different subject lines and CTAs
- **Multi-channel**: Combine email with LinkedIn messages and phone calls

## 📞 Support

- **Issues**: https://github.com/pepperonas/n8n-plygrnd/issues
- **n8n Community**: https://community.n8n.io/
- **Email**: martin.pfeffer@celox.io

## 👨‍💻 Developer

**Martin Pfeffer**
[celox.io](https://celox.io) | martin.pfeffer@celox.io
© 2025

## 📄 License

MIT License - Free to use for commercial projects

---

**Made with ❤️ in Berlin-Neukölln**

🚀 Happy lead generating!