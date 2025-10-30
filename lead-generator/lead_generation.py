#!/usr/bin/env python3
"""
Lead Generation & Email Campaign Script
Alternative zu n8n - kann standalone verwendet werden
"""

import os
import time
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Konfiguration
CONFIG = {
    'google_api_key': os.getenv('GOOGLE_MAPS_API_KEY', ''),
    'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
    'smtp_host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'smtp_user': os.getenv('SMTP_USER', 'martin@celox.io'),
    'smtp_password': os.getenv('SMTP_PASSWORD', ''),
    'db_host': os.getenv('DB_HOST', 'localhost'),
    'db_name': os.getenv('DB_NAME', 'n8n'),
    'db_user': os.getenv('DB_USER', 'postgres'),
    'db_password': os.getenv('DB_PASSWORD', ''),
    'search_location': '52.4797,13.4363',  # Neukölln
    'search_radius': 5000,
    'max_emails_per_day': 20,
    'delay_between_emails': 120,  # Sekunden
}

# High-Potential Keywords für Branchen
HIGH_POTENTIAL_KEYWORDS = [
    'steuerberater', 'buchhaltung', 'accounting', 'tax',
    'immobilien', 'hausverwaltung', 'property',
    'personaldienstleister', 'recruiting', 'hr',
    'versicherung', 'insurance',
    'rechtsanwalt', 'law', 'kanzlei',
    'marketing', 'werbeagentur', 'agency',
    'logistik', 'spedition', 'transport'
]


class LeadGenerator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=CONFIG['openai_api_key'])
        self.db_conn = None
        self.connect_db()

    def connect_db(self):
        """Verbindung zur PostgreSQL-Datenbank"""
        try:
            self.db_conn = psycopg2.connect(
                host=CONFIG['db_host'],
                database=CONFIG['db_name'],
                user=CONFIG['db_user'],
                password=CONFIG['db_password']
            )
            print("✓ Datenbankverbindung hergestellt")
        except Exception as e:
            print(f"✗ Datenbankfehler: {e}")
            raise

    def search_places(self) -> List[Dict]:
        """Sucht Unternehmen via Google Places API"""
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        params = {
            'query': 'Unternehmen Neukölln Berlin',
            'location': CONFIG['search_location'],
            'radius': CONFIG['search_radius'],
            'type': 'establishment',
            'key': CONFIG['google_api_key']
        }
        
        print(f"🔍 Suche Unternehmen in Neukölln...")
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"✗ Google API Fehler: {response.status_code}")
            return []
        
        data = response.json()
        results = data.get('results', [])
        print(f"✓ {len(results)} Unternehmen gefunden")
        
        return results

    def score_lead(self, place: Dict) -> int:
        """Bewertet Lead nach Automatisierungspotenzial"""
        score = 0
        name = place.get('name', '').lower()
        
        # Branchen-Check
        for keyword in HIGH_POTENTIAL_KEYWORDS:
            if keyword in name:
                score += 30
                break
        
        # Rating-Bonus
        rating = place.get('rating', 0)
        if rating >= 4.0:
            score += 10
        
        # Etabliertes Unternehmen
        if place.get('user_ratings_total', 0) > 20:
            score += 10
        
        return score

    def get_place_details(self, place_id: str) -> Dict:
        """Holt detaillierte Informationen zu einem Place"""
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_phone_number,website,business_status',
            'key': CONFIG['google_api_key']
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('result', {})
        return {}

    def analyze_website(self, url: str) -> Dict:
        """Analysiert Website auf Automatisierungspotenzial"""
        try:
            response = requests.get(url, timeout=10)
            html = response.text.lower()
            
            manual_indicators = [
                'anfrage', 'kontaktformular', 'telefonisch',
                'manuell', 'persönlich', 'verwaltung'
            ]
            
            automation_potential = sum(5 for indicator in manual_indicators if indicator in html)
            
            # Moderne Tech-Check
            modern_tech = ['react', 'vue', 'angular', 'next.js']
            is_modern = any(tech in html for tech in modern_tech)
            
            return {
                'automation_potential': automation_potential,
                'is_modern': is_modern,
                'length': len(html)
            }
        except:
            return {'automation_potential': 0, 'is_modern': False, 'length': 0}

    def generate_email(self, lead: Dict) -> Dict:
        """Generiert personalisierte E-Mail mit GPT-4"""
        prompt = f"""Erstelle eine personalisierte B2B-E-Mail für folgendes Unternehmen:

Firmenname: {lead['name']}
Branche: {lead.get('types', 'Unbekannt')}
Standort: {lead.get('address', 'Neukölln, Berlin')}

Die E-Mail soll:
1. Professionell und auf Augenhöhe sein
2. Konkrete Automatisierungspotenziale nennen (Rechnungsverarbeitung, Kundenkommunikation)
3. Zeitersparnis und Kostenreduktion betonen
4. Klare Call-to-Action: kostenloses 30-Min-Erstgespräch
5. Maximal 150 Wörter
6. Format: BETREFF: ... | BODY: ...

Absender: Martin von celox.io, IT-Dienstleister für KI-Automatisierung"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Du bist ein B2B-Sales-Experte für KI-Automatisierung."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            # Parse Betreff und Body
            parts = content.split('|')
            subject = parts[0].replace('BETREFF:', '').strip()
            body = parts[1].replace('BODY:', '').strip() if len(parts) > 1 else content
            
            return {'subject': subject, 'body': body}
        except Exception as e:
            print(f"✗ OpenAI Fehler: {e}")
            return None

    def save_lead(self, lead: Dict):
        """Speichert Lead in Datenbank"""
        cursor = self.db_conn.cursor()
        
        query = """
        INSERT INTO leads_email_campaign 
        (company_name, address, phone, website, score, email_subject, email_body, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (company_name, address) DO NOTHING
        """
        
        values = (
            lead['name'],
            lead.get('address'),
            lead.get('phone'),
            lead.get('website'),
            lead.get('score'),
            lead.get('email_subject'),
            lead.get('email_body'),
            'pending',
            datetime.now()
        )
        
        cursor.execute(query, values)
        self.db_conn.commit()
        cursor.close()

    def send_email(self, to_email: str, subject: str, body: str):
        """Versendet E-Mail via SMTP"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = CONFIG['smtp_user']
        msg['To'] = to_email
        
        # E-Mail-Body mit Signatur
        full_body = f"""{body}

---
Mit freundlichen Grüßen,

Martin
celox.io - IT-Dienstleistungen
Berlin

Web: https://celox.io
Telefon: [Ihre Telefonnummer]

Falls Sie keine weiteren Informationen wünschen, 
antworten Sie einfach mit "Abmelden".
"""
        
        msg.attach(MIMEText(full_body, 'plain'))
        
        try:
            server = smtplib.SMTP(CONFIG['smtp_host'], CONFIG['smtp_port'])
            server.starttls()
            server.login(CONFIG['smtp_user'], CONFIG['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✓ E-Mail gesendet an: {to_email}")
            return True
        except Exception as e:
            print(f"✗ E-Mail-Fehler: {e}")
            return False

    def update_email_status(self, company_name: str, status: str):
        """Aktualisiert E-Mail-Status in Datenbank"""
        cursor = self.db_conn.cursor()
        query = """
        UPDATE leads_email_campaign 
        SET status = %s, sent_at = %s 
        WHERE company_name = %s
        """
        cursor.execute(query, (status, datetime.now(), company_name))
        self.db_conn.commit()
        cursor.close()

    def run_campaign(self):
        """Führt komplette Kampagne aus"""
        print("\n🚀 Lead Generation Campaign gestartet\n")
        
        # 1. Suche Unternehmen
        places = self.search_places()
        
        # 2. Score & Filter
        qualified_leads = []
        for place in places:
            score = self.score_lead(place)
            if score >= 30:
                place['score'] = score
                qualified_leads.append(place)
        
        qualified_leads.sort(key=lambda x: x['score'], reverse=True)
        print(f"✓ {len(qualified_leads)} qualifizierte Leads gefunden\n")
        
        # 3. Detailinfos & E-Mail-Generierung
        emails_sent = 0
        max_emails = CONFIG['max_emails_per_day']
        
        for lead in qualified_leads[:50]:  # Top 50
            if emails_sent >= max_emails:
                print(f"\n⚠️ Tages-Limit erreicht ({max_emails} E-Mails)")
                break
            
            print(f"\n📧 Verarbeite: {lead['name']}")
            
            # Hole Details
            details = self.get_place_details(lead['place_id'])
            lead.update(details)
            
            # Prüfe ob Website vorhanden
            if not lead.get('website'):
                print("  ⊘ Keine Website - überspringe")
                continue
            
            # Analysiere Website
            website_analysis = self.analyze_website(lead['website'])
            lead['final_score'] = lead['score'] + website_analysis['automation_potential']
            
            # Nur Leads mit hohem Potenzial
            if lead['final_score'] < 40:
                print(f"  ⊘ Score zu niedrig ({lead['final_score']}) - überspringe")
                continue
            
            # Generiere E-Mail
            email_content = self.generate_email(lead)
            if not email_content:
                continue
            
            lead['email_subject'] = email_content['subject']
            lead['email_body'] = email_content['body']
            
            # Speichere in DB
            self.save_lead(lead)
            
            # Erstelle E-Mail-Adresse (Fallback)
            email = f"info@{lead['website'].replace('https://', '').replace('http://', '').split('/')[0]}"
            
            # Versende E-Mail
            if self.send_email(email, email_content['subject'], email_content['body']):
                self.update_email_status(lead['name'], 'sent')
                emails_sent += 1
                
                # Rate Limiting
                if emails_sent < max_emails:
                    print(f"  ⏳ Warte {CONFIG['delay_between_emails']}s...")
                    time.sleep(CONFIG['delay_between_emails'])
            
        print(f"\n✅ Kampagne abgeschlossen: {emails_sent} E-Mails versendet")

    def send_followups(self):
        """Sendet Follow-up E-Mails"""
        print("\n📬 Prüfe Follow-ups...\n")
        
        cursor = self.db_conn.cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT * FROM leads_email_campaign 
        WHERE status = 'sent' 
        AND sent_at < NOW() - INTERVAL '3 days'
        AND followup_count < 2
        AND response_received = FALSE
        LIMIT 10
        """
        
        cursor.execute(query)
        leads = cursor.fetchall()
        
        print(f"✓ {len(leads)} Follow-ups zu versenden\n")
        
        for lead in leads:
            # Generiere Follow-up
            prompt = f"""Erstelle eine kurze Follow-up E-Mail für {lead['company_name']}.
Erste E-Mail hatte Betreff: {lead['email_subject']}

Follow-up soll:
- Kurz sein (max 80 Wörter)
- Konkreten Mehrwert bieten (z.B. kostenloser KI-Potenzial-Check)
- Nicht aufdringlich wirken
Format: BETREFF: ... | BODY: ..."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            parts = content.split('|')
            subject = parts[0].replace('BETREFF:', '').strip()
            body = parts[1].replace('BODY:', '').strip() if len(parts) > 1 else content
            
            # Versende Follow-up
            email = f"info@{lead['website'].replace('https://', '').replace('http://', '').split('/')[0]}"
            
            if self.send_email(email, subject, body):
                # Update Datenbank
                cursor = self.db_conn.cursor()
                query = """
                UPDATE leads_email_campaign 
                SET followup_count = followup_count + 1, last_followup = %s 
                WHERE company_name = %s
                """
                cursor.execute(query, (datetime.now(), lead['company_name']))
                self.db_conn.commit()
                cursor.close()
                
                time.sleep(CONFIG['delay_between_emails'])

    def show_stats(self):
        """Zeigt Kampagnen-Statistiken"""
        cursor = self.db_conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM campaign_stats")
        stats = cursor.fetchone()
        
        print("\n📊 Kampagnen-Statistiken:")
        print(f"   Gesamt Leads: {stats['total_leads']}")
        print(f"   E-Mails versendet: {stats['emails_sent']}")
        print(f"   Antworten: {stats['responses']}")
        print(f"   Response-Rate: {stats['response_rate']}%")
        print(f"   Durchschnitt Score: {stats['avg_score']:.1f}")
        print(f"   Letzte E-Mail: {stats['last_email_sent']}\n")
        
        cursor.close()


def main():
    """Hauptfunktion"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lead Generation & Email Campaign')
    parser.add_argument('--campaign', action='store_true', help='Start neue Kampagne')
    parser.add_argument('--followup', action='store_true', help='Sende Follow-ups')
    parser.add_argument('--stats', action='store_true', help='Zeige Statistiken')
    
    args = parser.parse_args()
    
    generator = LeadGenerator()
    
    if args.campaign:
        generator.run_campaign()
    elif args.followup:
        generator.send_followups()
    elif args.stats:
        generator.show_stats()
    else:
        print("Verwendung:")
        print("  python lead_generation.py --campaign   # Neue Kampagne")
        print("  python lead_generation.py --followup   # Follow-ups")
        print("  python lead_generation.py --stats      # Statistiken")


if __name__ == '__main__':
    main()
