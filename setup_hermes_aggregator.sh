#!/bin/bash
# 🍛 Biryani Express Hermes Aggregator - One-Command Setup
# Run on on-prem server (192.168.1.168)

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║  🍛 BIRYANI EXPRESS HERMES SETUP               ║"
echo "║     Data Aggregator Installation               ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
HERMES_HOME="/opt/hermes"
BIN_DIR="$HERMES_HOME/bin"
CONFIG_DIR="$HERMES_HOME/config"
DATA_DIR="$HERMES_HOME/data/biryani-express"
LOG_DIR="/var/log/hermes"

echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
   echo -e "${RED}❌ This script must be run with sudo${NC}"
   exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Install with: sudo apt install python3${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version)${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found. Install with: sudo apt install python3-pip${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 installed${NC}"

# Check if Hermes running
if ! systemctl is-active hermes &> /dev/null; then
    echo -e "${YELLOW}⚠️  Hermes service not active. Start with: sudo systemctl start hermes${NC}"
fi

echo ""
echo -e "${BLUE}📁 Creating directories...${NC}"

# Create necessary directories
sudo mkdir -p "$BIN_DIR"
sudo mkdir -p "$CONFIG_DIR"
sudo mkdir -p "$DATA_DIR"
sudo mkdir -p "$LOG_DIR"

echo -e "${GREEN}✅ Directories created${NC}"

echo ""
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"

# Install Python packages
pip3 install -q requests schedule beautifulsoup4 selenium google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

echo -e "${GREEN}✅ Dependencies installed${NC}"

echo ""
echo -e "${BLUE}📂 Copying aggregator files...${NC}"

# Copy aggregator scripts
if [ -f "hermes_data_aggregator.py" ]; then
    sudo cp hermes_data_aggregator.py "$BIN_DIR/"
    sudo chmod +x "$BIN_DIR/hermes_data_aggregator.py"
    echo -e "${GREEN}✅ Data aggregator copied${NC}"
else
    echo -e "${RED}❌ hermes_data_aggregator.py not found in current directory${NC}"
    exit 1
fi

if [ -f "hermes_platform_apis.py" ]; then
    sudo cp hermes_platform_apis.py "$BIN_DIR/"
    echo -e "${GREEN}✅ Platform APIs module copied${NC}"
else
    echo -e "${RED}❌ hermes_platform_apis.py not found in current directory${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}🔐 Setting up credentials...${NC}"

# Check if credentials file exists
if [ ! -f "$CONFIG_DIR/credentials.json" ]; then
    if [ -f "credentials_template.json" ]; then
        sudo cp credentials_template.json "$CONFIG_DIR/credentials.json"
        sudo chmod 600 "$CONFIG_DIR/credentials.json"
        echo -e "${YELLOW}⚠️  Credentials template created${NC}"
        echo -e "${YELLOW}   Location: $CONFIG_DIR/credentials.json${NC}"
        echo -e "${YELLOW}   Please edit and add your API keys!${NC}"
    else
        echo -e "${RED}❌ credentials_template.json not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Credentials file exists${NC}"
fi

echo ""
echo -e "${BLUE}🧪 Running test execution...${NC}"

# Test run
python3 "$BIN_DIR/hermes_data_aggregator.py"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Test execution successful${NC}"
else
    echo -e "${RED}❌ Test execution failed. Check logs.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}⏰ Setting up daily schedule...${NC}"

# Create cron job
CRON_ENTRY="0 2 * * * /usr/bin/python3 $BIN_DIR/hermes_data_aggregator.py >> $LOG_DIR/biryani_aggregator.log 2>&1"

# Check if cron entry already exists
if ! crontab -l 2>/dev/null | grep -q "hermes_data_aggregator.py"; then
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo -e "${GREEN}✅ Cron job created (runs daily at 2:00 AM)${NC}"
else
    echo -e "${GREEN}✅ Cron job already exists${NC}"
fi

echo ""
echo -e "${BLUE}🔍 Verifying setup...${NC}"

# Verify files
if [ -f "$BIN_DIR/hermes_data_aggregator.py" ]; then
    echo -e "${GREEN}✅ Aggregator script present${NC}"
fi

if [ -f "$BIN_DIR/hermes_platform_apis.py" ]; then
    echo -e "${GREEN}✅ Platform APIs module present${NC}"
fi

if [ -f "$CONFIG_DIR/credentials.json" ]; then
    echo -e "${GREEN}✅ Credentials file present${NC}"
fi

if [ -d "$DATA_DIR" ]; then
    echo -e "${GREEN}✅ Data directory present${NC}"
fi

if [ -f "$DATA_DIR/biryani_metrics.db" ]; then
    echo -e "${GREEN}✅ Database created${NC}"

    # Show table count
    TABLES=$(sqlite3 "$DATA_DIR/biryani_metrics.db" ".tables" | wc -w)
    echo -e "${GREEN}   Tables: $TABLES${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║           ✅ SETUP COMPLETE                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}📍 Next Steps:${NC}"
echo "  1. Edit credentials file:"
echo "     ${YELLOW}sudo nano $CONFIG_DIR/credentials.json${NC}"
echo "  2. Add your API keys (Swiggy, Zomato, Google, Instagram)"
echo "  3. Aggregator will run tomorrow at 2:00 AM"
echo "  4. Monitor logs:"
echo "     ${YELLOW}tail -f $LOG_DIR/biryani_aggregator.log${NC}"
echo ""
echo -e "${BLUE}📊 Data Storage:${NC}"
echo "  Database: ${YELLOW}$DATA_DIR/biryani_metrics.db${NC}"
echo "  Daily reports: ${YELLOW}$DATA_DIR/daily_report_*.json${NC}"
echo "  Logs: ${YELLOW}$LOG_DIR/biryani_aggregator.log${NC}"
echo ""
echo -e "${BLUE}🔗 Access Data:${NC}"
echo "  API: http://192.168.1.168:9119/api/metrics/..."
echo "  Dashboard: http://192.168.1.168:9119/dashboard"
echo ""
echo -e "${GREEN}🎉 Ready to go! Add credentials and daily monitoring starts.${NC}"
echo ""
