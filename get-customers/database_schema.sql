-- PostgreSQL Datenbank-Schema für Lead-Tracking
-- Erstelle diese Tabelle in deiner n8n-Datenbank

CREATE TABLE IF NOT EXISTS leads_email_campaign (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(50),
    website VARCHAR(500),
    score INTEGER,
    email VARCHAR(255),
    email_subject TEXT,
    email_body TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    followup_count INTEGER DEFAULT 0,
    last_followup TIMESTAMP,
    response_received BOOLEAN DEFAULT FALSE,
    response_date TIMESTAMP,
    notes TEXT,
    UNIQUE(company_name, address)
);

-- Index für Performance
CREATE INDEX idx_status ON leads_email_campaign(status);
CREATE INDEX idx_sent_at ON leads_email_campaign(sent_at);
CREATE INDEX idx_followup ON leads_email_campaign(followup_count, sent_at);

-- View für Reporting
CREATE OR REPLACE VIEW campaign_stats AS
SELECT 
    COUNT(*) as total_leads,
    COUNT(CASE WHEN status = 'sent' THEN 1 END) as emails_sent,
    COUNT(CASE WHEN response_received THEN 1 END) as responses,
    ROUND(COUNT(CASE WHEN response_received THEN 1 END)::NUMERIC / 
          NULLIF(COUNT(CASE WHEN status = 'sent' THEN 1 END), 0) * 100, 2) as response_rate,
    AVG(score) as avg_score,
    MAX(sent_at) as last_email_sent
FROM leads_email_campaign;

-- Beispiel-Abfragen für dein Dashboard:

-- Alle gesendeten E-Mails der letzten 7 Tage
-- SELECT * FROM leads_email_campaign 
-- WHERE sent_at > NOW() - INTERVAL '7 days' 
-- ORDER BY score DESC;

-- Top-Leads die noch keine Antwort gegeben haben
-- SELECT company_name, email, score, sent_at 
-- FROM leads_email_campaign 
-- WHERE status = 'sent' 
-- AND response_received = FALSE 
-- ORDER BY score DESC 
-- LIMIT 20;
