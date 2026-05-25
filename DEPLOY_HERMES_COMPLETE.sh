#!/bin/bash
#🍛 BIRYANI EXPRESS - COMPLETE HERMES DEPLOYMENT
# This script does EVERYTHING - just run it once and it handles everything
# Usage: sudo bash DEPLOY_HERMES_COMPLETE.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════╗"
echo "║  🍛 BIRYANI EXPRESS HERMES COMPLETE DEPLOY      ║"
echo "║     Full Automated Setup & Configuration        ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
   echo -e "${RED}❌ This script must be run with sudo${NC}"
   exit 1
fi

REPO_DIR="/home/user/the-chettinad"
HERMES_HOME="/opt/hermes"
BIN_DIR="$HERMES_HOME/bin"
CONFIG_DIR="$HERMES_HOME/config"
DATA_DIR="$HERMES_HOME/data/biryani-express"
LOG_DIR="/var/log/hermes"

echo -e "${BLUE}Step 1/10: Verifying prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version | awk '{print $2}')${NC}"

if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 available${NC}"

echo -e "${BLUE}Step 2/10: Creating directories...${NC}"
mkdir -p "$BIN_DIR" "$CONFIG_DIR" "$DATA_DIR" "$LOG_DIR"
echo -e "${GREEN}✅ Directories created${NC}"

echo -e "${BLUE}Step 3/10: Installing Python dependencies...${NC}"
pip3 install -q requests schedule beautifulsoup4 selenium google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo -e "${BLUE}Step 4/10: Copying aggregator files...${NC}"
if [ -f "$REPO_DIR/hermes_data_aggregator.py" ]; then
    cp "$REPO_DIR/hermes_data_aggregator.py" "$BIN_DIR/"
    chmod +x "$BIN_DIR/hermes_data_aggregator.py"
    echo -e "${GREEN}✅ Data aggregator copied${NC}"
else
    echo -e "${RED}❌ hermes_data_aggregator.py not found${NC}"
    exit 1
fi

if [ -f "$REPO_DIR/hermes_platform_apis.py" ]; then
    cp "$REPO_DIR/hermes_platform_apis.py" "$BIN_DIR/"
    echo -e "${GREEN}✅ Platform APIs module copied${NC}"
else
    echo -e "${RED}❌ hermes_platform_apis.py not found${NC}"
    exit 1
fi

echo -e "${BLUE}Step 5/10: Setting up credentials...${NC}"
if [ ! -f "$CONFIG_DIR/credentials.json" ]; then
    if [ -f "$REPO_DIR/credentials_template.json" ]; then
        cp "$REPO_DIR/credentials_template.json" "$CONFIG_DIR/credentials.json"
        chmod 600 "$CONFIG_DIR/credentials.json"
        echo -e "${YELLOW}⚠️  Credentials template created${NC}"
        echo -e "${YELLOW}📝 Location: $CONFIG_DIR/credentials.json${NC}"
        echo -e "${YELLOW}⚠️  YOU MUST EDIT THIS FILE AND ADD YOUR API KEYS${NC}"
        echo -e "${YELLOW}   Then re-run: python3 $BIN_DIR/hermes_data_aggregator.py${NC}"
        exit 0
    fi
fi
echo -e "${GREEN}✅ Credentials configured${NC}"

echo -e "${BLUE}Step 6/10: Initializing database...${NC}"
python3 "$BIN_DIR/hermes_data_aggregator.py"
if [ -f "$DATA_DIR/biryani_metrics.db" ]; then
    echo -e "${GREEN}✅ Database initialized${NC}"
else
    echo -e "${RED}❌ Database initialization failed${NC}"
    exit 1
fi

echo -e "${BLUE}Step 7/10: Verifying tables...${NC}"
TABLES=$(sqlite3 "$DATA_DIR/biryani_metrics.db" ".tables" | wc -w)
echo -e "${GREEN}✅ Database has $TABLES tables${NC}"

echo -e "${BLUE}Step 8/10: Setting up daily cron job...${NC}"
CRON_ENTRY="0 2 * * * /usr/bin/python3 $BIN_DIR/hermes_data_aggregator.py >> $LOG_DIR/biryani_aggregator.log 2>&1"
if ! crontab -l 2>/dev/null | grep -q "hermes_data_aggregator.py"; then
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo -e "${GREEN}✅ Cron job created (2:00 AM daily)${NC}"
else
    echo -e "${GREEN}✅ Cron job already exists${NC}"
fi

echo -e "${BLUE}Step 9/10: Setting permissions...${NC}"
chown -R root:root "$HERMES_HOME" 2>/dev/null || true
chmod -R 755 "$HERMES_HOME" 2>/dev/null || true
chmod 600 "$CONFIG_DIR/credentials.json" 2>/dev/null || true
echo -e "${GREEN}✅ Permissions set${NC}"

echo -e "${BLUE}Step 10/10: Final verification...${NC}"
echo -e "${GREEN}✅ Aggregator script: $(ls -lh $BIN_DIR/hermes_data_aggregator.py | awk '{print $5}')${NC}"
echo -e "${GREEN}✅ Database: $(ls -lh $DATA_DIR/biryani_metrics.db | awk '{print $5}')${NC}"
echo -e "${GREEN}✅ Config: $(ls -lh $CONFIG_DIR/credentials.json | awk '{print $5}')${NC}"
echo -e "${GREEN}✅ Cron: Scheduled daily at 2:00 AM${NC}"

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════╗"
echo "║           ✅ DEPLOYMENT COMPLETE               ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📍 Next Steps:${NC}"
echo "1. Edit credentials file:"
echo "   sudo nano $CONFIG_DIR/credentials.json"
echo ""
echo "2. Add your API keys:"
echo "   - Foodora: API Key + Restaurant ID"
echo "   - Wolt: API Key + Restaurant ID"
echo "   - Google: Credentials JSON path"
echo "   - Instagram: Business Account ID + Access Token"
echo ""
echo "3. Test the aggregator:"
echo "   python3 $BIN_DIR/hermes_data_aggregator.py"
echo ""
echo "4. Check logs:"
echo "   tail -f $LOG_DIR/biryani_aggregator.log"
echo ""
echo -e "${BLUE}📊 Data will be stored at:${NC}"
echo "   Database: $DATA_DIR/biryani_metrics.db"
echo "   Reports: $DATA_DIR/daily_report_*.json"
echo "   Logs: $LOG_DIR/biryani_aggregator.log"
echo ""
echo -e "${GREEN}🎉 First data collection: Tomorrow at 2:00 AM${NC}"
echo ""
