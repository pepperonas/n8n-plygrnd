#!/bin/bash
# Cronjob Setup für Lead Generation Campaign
# 
# Installation:
# chmod +x setup_cronjobs.sh
# ./setup_cronjobs.sh

echo "🔧 Setting up cronjobs for Lead Generation..."

# Pfad zum Skript anpassen
SCRIPT_DIR="/home/dein-user/lead-generation"
PYTHON_BIN="/usr/bin/python3"

# Log-Verzeichnis erstellen
mkdir -p "$SCRIPT_DIR/logs"

# Cronjob-Einträge
CRON_CAMPAIGN="0 9 * * 1-5 cd $SCRIPT_DIR && $PYTHON_BIN lead_generation.py --campaign >> logs/campaign.log 2>&1"
CRON_FOLLOWUP="0 14 * * * cd $SCRIPT_DIR && $PYTHON_BIN lead_generation.py --followup >> logs/followup.log 2>&1"
CRON_STATS="0 18 * * 5 cd $SCRIPT_DIR && $PYTHON_BIN lead_generation.py --stats >> logs/stats.log 2>&1"

# Füge Cronjobs hinzu
(crontab -l 2>/dev/null; echo "$CRON_CAMPAIGN") | crontab -
(crontab -l 2>/dev/null; echo "$CRON_FOLLOWUP") | crontab -
(crontab -l 2>/dev/null; echo "$CRON_STATS") | crontab -

echo "✅ Cronjobs installiert:"
echo ""
echo "📧 Kampagne: Montag-Freitag, 9:00 Uhr"
echo "📬 Follow-ups: Täglich, 14:00 Uhr"
echo "📊 Statistiken: Freitag, 18:00 Uhr"
echo ""
echo "Logs verfügbar unter: $SCRIPT_DIR/logs/"
echo ""
echo "Aktuelle Cronjobs anzeigen:"
echo "  crontab -l"
echo ""
echo "Cronjobs entfernen:"
echo "  crontab -e  # und entsprechende Zeilen löschen"

# Erstelle Log-Rotation
cat > /etc/logrotate.d/lead-generation << EOF
$SCRIPT_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 $USER $USER
}
EOF

echo "✅ Log-Rotation konfiguriert (30 Tage)"
