#!/usr/bin/env python3
"""
Flask REST API für Lead Generation Dashboard
Stellt Daten für das HTML-Dashboard bereit
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Erlaube Cross-Origin Requests

# Datenbank-Konfiguration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'n8n'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}


def get_db_connection():
    """Erstellt Datenbankverbindung"""
    return psycopg2.connect(**DB_CONFIG)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Liefert Kampagnen-Statistiken"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM campaign_stats")
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify(dict(stats) if stats else {})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Liefert alle Leads (mit optionalem Filter)"""
    try:
        # Query-Parameter
        status = request.args.get('status')
        limit = request.args.get('limit', 50)
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
        SELECT 
            id,
            company_name,
            address,
            phone,
            website,
            score,
            status,
            sent_at,
            followup_count,
            response_received,
            created_at
        FROM leads_email_campaign
        """
        
        # Filter nach Status
        if status:
            query += f" WHERE status = %s"
            cursor.execute(query + " ORDER BY score DESC, created_at DESC LIMIT %s", (status, limit))
        else:
            cursor.execute(query + " ORDER BY score DESC, created_at DESC LIMIT %s", (limit,))
        
        leads = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Konvertiere datetime zu ISO-Format
        result = []
        for lead in leads:
            lead_dict = dict(lead)
            for key in ['sent_at', 'created_at']:
                if lead_dict.get(key):
                    lead_dict[key] = lead_dict[key].isoformat()
            result.append(lead_dict)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Liefert Details zu einem spezifischen Lead"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT * FROM leads_email_campaign WHERE id = %s
        """, (lead_id,))
        
        lead = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        lead_dict = dict(lead)
        for key in ['sent_at', 'created_at', 'response_date', 'last_followup']:
            if lead_dict.get(key):
                lead_dict[key] = lead_dict[key].isoformat()
        
        return jsonify(lead_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/leads/<int:lead_id>/response', methods=['POST'])
def mark_response(lead_id):
    """Markiert Lead als 'Antwort erhalten'"""
    try:
        data = request.get_json()
        notes = data.get('notes', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE leads_email_campaign 
            SET response_received = TRUE, 
                response_date = %s,
                notes = %s
            WHERE id = %s
        """, (datetime.now(), notes, lead_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Lead als beantwortet markiert'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/leads/<int:lead_id>/notes', methods=['PUT'])
def update_notes(lead_id):
    """Aktualisiert Notizen zu einem Lead"""
    try:
        data = request.get_json()
        notes = data.get('notes', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE leads_email_campaign 
            SET notes = %s
            WHERE id = %s
        """, (notes, lead_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Notizen aktualisiert'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/timeline', methods=['GET'])
def get_timeline():
    """Liefert Timeline der gesendeten E-Mails (letzte 30 Tage)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                DATE(sent_at) as date,
                COUNT(*) as emails_sent,
                COUNT(CASE WHEN response_received THEN 1 END) as responses
            FROM leads_email_campaign
            WHERE sent_at > NOW() - INTERVAL '30 days'
            GROUP BY DATE(sent_at)
            ORDER BY date DESC
        """)
        
        timeline = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        result = []
        for entry in timeline:
            entry_dict = dict(entry)
            if entry_dict.get('date'):
                entry_dict['date'] = entry_dict['date'].isoformat()
            result.append(entry_dict)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/top-performers', methods=['GET'])
def get_top_performers():
    """Liefert die besten Leads (höchster Score)"""
    try:
        limit = request.args.get('limit', 10)
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                company_name,
                score,
                status,
                response_received,
                website
            FROM leads_email_campaign
            ORDER BY score DESC
            LIMIT %s
        """, (limit,))
        
        top_leads = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify([dict(lead) for lead in top_leads])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search_leads():
    """Sucht Leads nach Firmenname"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify([])
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                id,
                company_name,
                address,
                score,
                status,
                website
            FROM leads_email_campaign
            WHERE company_name ILIKE %s
            ORDER BY score DESC
            LIMIT 20
        """, (f'%{query}%',))
        
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify([dict(lead) for lead in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['GET'])
def export_leads():
    """Exportiert Leads als CSV"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                company_name,
                address,
                phone,
                website,
                score,
                status,
                sent_at,
                response_received
            FROM leads_email_campaign
            ORDER BY score DESC
        """)
        
        leads = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # CSV-Header
        csv_data = "Firma,Adresse,Telefon,Website,Score,Status,Gesendet,Antwort\n"
        
        # CSV-Zeilen
        for lead in leads:
            csv_data += f"{lead['company_name']},"
            csv_data += f"{lead['address'] or ''},"
            csv_data += f"{lead['phone'] or ''},"
            csv_data += f"{lead['website'] or ''},"
            csv_data += f"{lead['score']},"
            csv_data += f"{lead['status']},"
            csv_data += f"{lead['sent_at'] or ''},"
            csv_data += f"{'Ja' if lead['response_received'] else 'Nein'}\n"
        
        from flask import Response
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=leads_export.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health-Check Endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


if __name__ == '__main__':
    # Development Server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
    
    # Production: Verwende Gunicorn
    # gunicorn -w 4 -b 0.0.0.0:5000 api:app
