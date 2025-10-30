#!/bin/bash
# Automatisches Setup-Skript für Lead Generation Workflow
# Usage: chmod +x install.sh && ./install.sh

set -e  # Exit bei Fehler

echo "🚀 Lead Generation Workflow - Installation"
echo "=========================================="
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funktion für farbige Ausgabe
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Prüfe Root-Rechte
if [[ $EUID -eq 0 ]]; then
   print_error "Dieses Skript sollte NICHT als root ausgeführt werden"
   exit 1
fi

# 1. System-Voraussetzungen prüfen
echo "📋 Prüfe System-Voraussetzungen..."
echo ""

# Python 3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python3 gefunden: $PYTHON_VERSION"
else
    print_error "Python3 nicht gefunden"
    echo "Installation: sudo apt install python3 python3-pip"
    exit 1
fi

# PostgreSQL
if command -v psql &> /dev/null; then
    PSQL_VERSION=$(psql --version)
    print_success "PostgreSQL gefunden: $PSQL_VERSION"
else
    print_warning "PostgreSQL nicht gefunden"
    read -p "PostgreSQL installieren? (j/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        sudo apt update
        sudo apt install -y postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        print_success "PostgreSQL installiert"
    else
        print_error "PostgreSQL wird benötigt"
        exit 1
    fi
fi

# Git
if command -v git &> /dev/null; then
    print_success "Git gefunden"
else
    print_warning "Git nicht gefunden - installiere..."
    sudo apt install -y git
fi

echo ""

# 2. Projekt-Verzeichnis erstellen
echo "📁 Erstelle Projekt-Verzeichnis..."
PROJECT_DIR="$HOME/lead-generation"

if [ -d "$PROJECT_DIR" ]; then
    print_warning "Verzeichnis existiert bereits: $PROJECT_DIR"
    read -p "Überschreiben? (j/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Jj]$ ]]; then
        print_error "Installation abgebrochen"
        exit 1
    fi
    rm -rf "$PROJECT_DIR"
fi

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
print_success "Verzeichnis erstellt: $PROJECT_DIR"

# 3. Python Virtual Environment
echo ""
echo "🐍 Erstelle Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual Environment aktiviert"

# 4. Dependencies installieren
echo ""
echo "📦 Installiere Python-Packages..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installiert"

# 5. Datenbank Setup
echo ""
echo "🗄️ Datenbank-Setup..."
echo ""
read -p "PostgreSQL Datenbank erstellen? (j/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Jj]$ ]]; then
    read -p "Datenbankname [lead_generation]: " DB_NAME
    DB_NAME=${DB_NAME:-lead_generation}
    
    read -p "Benutzer [postgres]: " DB_USER
    DB_USER=${DB_USER:-postgres}
    
    echo ""
    echo "Erstelle Datenbank '$DB_NAME'..."
    
    # Datenbank erstellen
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || print_warning "Datenbank existiert bereits"
    
    # Schema importieren
    sudo -u postgres psql -d "$DB_NAME" -f database_schema.sql
    
    print_success "Datenbank '$DB_NAME' erstellt und Schema importiert"
fi

# 6. Environment Variables
echo ""
echo "🔐 Konfiguration..."
echo ""

if [ ! -f .env ]; then
    cp .env.example .env
    print_success ".env Datei erstellt"
    
    echo ""
    echo "Bitte trage deine API-Keys in die .env Datei ein:"
    echo ""
    echo "  nano .env"
    echo ""
    echo "Benötigte Keys:"
    echo "  - GOOGLE_MAPS_API_KEY"
    echo "  - OPENAI_API_KEY"
    echo "  - SMTP Credentials"
    echo ""
    
    read -p "Möchtest du die .env Datei jetzt bearbeiten? (j/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    print_warning ".env existiert bereits"
fi

# 7. Cronjobs (Optional)
echo ""
read -p "Cronjobs für Automatisierung einrichten? (j/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Jj]$ ]]; then
    chmod +x setup_cronjobs.sh
    ./setup_cronjobs.sh
    print_success "Cronjobs eingerichtet"
fi

# 8. Test-Durchlauf
echo ""
echo "🧪 Test-Durchlauf..."
echo ""
read -p "Möchtest du einen Test-Durchlauf starten? (j/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Jj]$ ]]; then
    print_warning "Stelle sicher, dass deine API-Keys in .env konfiguriert sind!"
    sleep 2
    
    # Test mit --stats (ungefährlich)
    python lead_generation.py --stats
    
    if [ $? -eq 0 ]; then
        print_success "Test erfolgreich!"
    else
        print_error "Test fehlgeschlagen - prüfe deine Konfiguration"
    fi
fi

# 9. Dashboard Setup (Optional)
echo ""
read -p "Dashboard-API starten? (j/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo ""
    echo "Starte API im Hintergrund..."
    nohup python api.py > api.log 2>&1 &
    API_PID=$!
    print_success "API läuft (PID: $API_PID)"
    print_success "Dashboard verfügbar unter: file://$PROJECT_DIR/dashboard.html"
    print_success "API verfügbar unter: http://localhost:5000"
    
    # PID speichern
    echo $API_PID > api.pid
fi

# 10. Zusammenfassung
echo ""
echo "=========================================="
echo "✅ Installation abgeschlossen!"
echo "=========================================="
echo ""
echo "📍 Projekt-Verzeichnis: $PROJECT_DIR"
echo ""
echo "🚀 Nächste Schritte:"
echo ""
echo "1. API-Keys konfigurieren:"
echo "   cd $PROJECT_DIR"
echo "   nano .env"
echo ""
echo "2. Kampagne starten:"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   python lead_generation.py --campaign"
echo ""
echo "3. Dashboard öffnen:"
echo "   file://$PROJECT_DIR/dashboard.html"
echo ""
echo "4. n8n Workflow importieren:"
echo "   n8n-Oberfläche → Import → neukoelln_lead_workflow.json"
echo ""
echo "📚 Dokumentation:"
echo "   - README.md - Vollständige Dokumentation"
echo "   - SETUP_ANLEITUNG.md - Detaillierte Schritt-für-Schritt Anleitung"
echo "   - QUICK_REFERENCE.md - Schnell-Referenz"
echo ""
echo "💡 Hilfe & Support:"
echo "   - GitHub Issues: [Dein Repo]"
echo "   - E-Mail: martin@celox.io"
echo ""
echo "⚠️ Wichtig:"
echo "   - Prüfe rechtliche Hinweise in README.md"
echo "   - Teste zuerst mit kleiner Menge (5-10 Leads)"
echo "   - Backup deiner Datenbank regelmäßig durchführen"
echo ""
echo "Viel Erfolg! 🎯"
echo ""

# Deaktiviere Virtual Environment
deactivate
