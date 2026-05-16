# 🚀 Hermes On-Prem Deployment Guide
**Biryani Express Data Aggregator**

---

## 📋 Prerequisites

- On-prem server: GMKtec K12 (192.168.1.168)
- Hermes running: `sudo systemctl status hermes` (should show active)
- Python 3.8+: `python3 --version`
- pip installed: `pip3 --version`
- Internet connectivity for API access

---

## ✅ Step 1: SSH to On-Prem Server

**Via Tailscale (Recommended):**
```bash
ssh getjeevan@100.112.118.83
# Password: 1234bcbc9
```

**Or locally:**
```bash
ssh getjeevan@192.168.1.168
# Password: 1234bcbc9
```

---

## 📦 Step 2: Clone Repository & Setup

```bash
# Navigate to Hermes directory
cd /opt/hermes

# Clone/copy the aggregator files
# If from git:
git clone <your-repo-url> biryani-express
cd biryani-express

# Or copy files directly
cp hermes_data_aggregator.py /opt/hermes/bin/
cp hermes_platform_apis.py /opt/hermes/bin/
```

---

## 🔐 Step 3: Configure Credentials

### Create Credentials File

```bash
# Create config directory if it doesn't exist
sudo mkdir -p /opt/hermes/config
sudo chmod 755 /opt/hermes/config

# Copy and edit credentials template
sudo cp credentials_template.json /opt/hermes/config/credentials.json
sudo nano /opt/hermes/config/credentials.json
```

### Fill in Your Credentials

**You'll need to fill in:**

1. **Swiggy Ads API Key**
   - Get from: Swiggy Partner Dashboard → Settings → API Keys
   - Location in JSON: `swiggy.api_key`

2. **Zomato API Key**
   - Get from: Zomato Partner → Settings → API Keys
   - Location in JSON: `zomato.api_key`

3. **Google Search Console**
   - Get credentials JSON from: Google Cloud Console
   - Save to: `/opt/hermes/config/google-credentials.json`
   - Location in JSON: `google.credentials_file`

4. **Instagram Business Account**
   - Get from: Instagram Business Settings → Apps and Websites
   - Location in JSON: `instagram.business_account_id` and `instagram.access_token`

---

## 📝 Example Credentials Setup

```bash
# Set environment variables (alternative to file)
export SWIGGY_API_KEY="your-swiggy-api-key"
export SWIGGY_RESTAURANT_ID="your-swiggy-restaurant-id"
export ZOMATO_API_KEY="your-zomato-api-key"
export ZOMATO_RESTAURANT_ID="your-zomato-restaurant-id"
export GOOGLE_PROPERTY_ID="https://biryaniexpress.no"
export GOOGLE_CREDENTIALS_FILE="/opt/hermes/config/google-credentials.json"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your-instagram-account-id"
export INSTAGRAM_ACCESS_TOKEN="your-instagram-access-token"

# Make persistent by adding to ~/.bashrc
echo 'export SWIGGY_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📚 Step 4: Install Dependencies

```bash
# Install required Python packages
sudo pip3 install requests schedule beautifulsoup4 selenium google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Or use requirements file
cat > /tmp/requirements.txt << EOF
requests>=2.28.0
schedule>=1.1.0
beautifulsoup4>=4.11.0
selenium>=4.0.0
google-auth>=2.20.0
google-auth-oauthlib>=0.7.0
google-auth-httplib2>=0.1.1
google-api-python-client>=2.80.0
EOF

sudo pip3 install -r /tmp/requirements.txt
```

---

## 🧪 Step 5: Test the Aggregator

```bash
# Make script executable
chmod +x /opt/hermes/bin/hermes_data_aggregator.py

# Run a test (single execution)
python3 /opt/hermes/bin/hermes_data_aggregator.py

# Expected output:
# ✅ Database initialized
# ✅ Credentials loaded from file
# 🍛 BIRYANI EXPRESS DAILY DATA AGGREGATION
# 🔗 Fetching Swiggy Ads data...
# ✅ Swiggy data fetched and stored
# ... (and so on)
```

---

## ⏰ Step 6: Schedule Daily Execution

### Option A: Using Cron (Recommended)

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM:
0 2 * * * /usr/bin/python3 /opt/hermes/bin/hermes_data_aggregator.py --schedule 2 0 >> /var/log/hermes/aggregator.log 2>&1
```

### Option B: Using Systemd Timer

```bash
# Create service file
sudo nano /etc/systemd/system/biryani-aggregator.service
```

Add:
```ini
[Unit]
Description=Biryani Express Data Aggregator
After=network.target

[Service]
Type=simple
User=hermes
WorkingDirectory=/opt/hermes
ExecStart=/usr/bin/python3 /opt/hermes/bin/hermes_data_aggregator.py --schedule 2 0
Restart=on-failure
RestartSec=300

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable biryani-aggregator.service
sudo systemctl start biryani-aggregator.service

# Check status
sudo systemctl status biryani-aggregator.service
```

---

## 🔄 Step 7: Data Storage & Location

Data is stored in SQLite database at:
```
/opt/hermes/data/biryani-express/biryani_metrics.db
```

Daily reports are saved as JSON:
```
/opt/hermes/data/biryani-express/daily_report_YYYY-MM-DD.json
```

Tables created:
- `swiggy_ads` — Swiggy ad performance
- `zomato_ads` — Zomato ad performance
- `google_seo` — Google Search Console data
- `instagram_metrics` — Instagram insights
- `competitor_data` — Scraped competitor data
- `raw_json_data` — Raw API responses for backup

---

## 📊 Step 8: Verify Data Collection

```bash
# Check database
sqlite3 /opt/hermes/data/biryani-express/biryani_metrics.db

# View tables
.tables

# Check latest Swiggy data
SELECT * FROM swiggy_ads ORDER BY timestamp DESC LIMIT 5;

# Check latest report
cat /opt/hermes/data/biryani-express/daily_report_*.json | jq .
```

---

## 🔍 Step 9: Monitor Logs

```bash
# Real-time log monitoring
tail -f /var/log/hermes/biryani_aggregator.log

# Check for errors
grep "ERROR" /var/log/hermes/biryani_aggregator.log

# Check for successful runs
grep "AGGREGATION COMPLETE" /var/log/hermes/biryani_aggregator.log
```

---

## 📡 Step 10: API Endpoint to Access Data

Once running, access data via HTTP:

```bash
# Get latest Swiggy data
curl http://192.168.1.168:9119/api/metrics/swiggy/latest

# Get latest Zomato data
curl http://192.168.1.168:9119/api/metrics/zomato/latest

# Get SEO keywords
curl http://192.168.1.168:9119/api/metrics/seo/keywords

# Get Instagram insights
curl http://192.168.1.168:9119/api/metrics/instagram/insights

# Get competitor data
curl http://192.168.1.168:9119/api/metrics/competitors/all

# Get today's report
curl http://192.168.1.168:9119/api/reports/daily/latest
```

---

## 🧹 Troubleshooting

### API Authentication Fails
```bash
# Verify credentials file exists
cat /opt/hermes/config/credentials.json

# Check for syntax errors
python3 -c "import json; json.load(open('/opt/hermes/config/credentials.json'))"

# Verify API keys are correct
echo $SWIGGY_API_KEY
```

### Database Locked
```bash
# Kill any existing connections
pkill -f hermes_data_aggregator

# Reset database if corrupted
rm /opt/hermes/data/biryani-express/biryani_metrics.db

# Aggregator will recreate it on next run
```

### Permission Denied
```bash
# Fix permissions
sudo chown hermes:hermes /opt/hermes/data/biryani-express/
sudo chmod 755 /opt/hermes/data/biryani-express/

# For log directory
sudo mkdir -p /var/log/hermes
sudo chown hermes:hermes /var/log/hermes
sudo chmod 755 /var/log/hermes
```

### Network Issues
```bash
# Test API connectivity
curl -I https://ads-api.swiggy.com/v1
curl -I https://www.zomato.com/api/partner/v2
curl -I https://graph.instagram.com/v18.0

# Check firewall
sudo ufw status
sudo ufw allow 443/tcp  # HTTPS for APIs
```

---

## 📈 Expected Data Flow

```
Daily at 2:00 AM
        ↓
Aggregator runs
        ↓
┌───────────────────────────────────┐
│ Fetches from:                     │
│ ✓ Swiggy Ads API                 │
│ ✓ Zomato Ads API                 │
│ ✓ Google Search Console          │
│ ✓ Instagram Graph API            │
│ ✓ Competitor websites (scrape)   │
└───────────────────────────────────┘
        ↓
Stores in SQLite
        ↓
├─ swiggy_ads table
├─ zomato_ads table
├─ google_seo table
├─ instagram_metrics table
├─ competitor_data table
└─ raw_json_data table
        ↓
Exports JSON report
        ↓
/opt/hermes/data/biryani-express/daily_report_YYYY-MM-DD.json
        ↓
Available via HTTP API
```

---

## ✅ Deployment Checklist

- [ ] SSH to on-prem server via Tailscale
- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip3 install`)
- [ ] Credentials file created and filled with actual API keys
- [ ] Google credentials JSON downloaded
- [ ] Test run successful (one-time execution)
- [ ] Cron or systemd scheduled
- [ ] Logs showing no errors
- [ ] Database created with tables
- [ ] HTTP API responding with data
- [ ] Daily execution verified (check logs tomorrow)

---

## 🎯 First Run Checklist

1. **SSH to server** (via Tailscale)
2. **Copy files** to `/opt/hermes/bin/`
3. **Create credentials** at `/opt/hermes/config/credentials.json`
4. **Install dependencies** with pip3
5. **Run test** with one-time execution
6. **Verify output** in database and logs
7. **Schedule** with cron or systemd
8. **Monitor** logs for first scheduled run

---

## 📞 Support

If any step fails:
1. Check logs: `tail -f /var/log/hermes/biryani_aggregator.log`
2. Verify credentials are correct
3. Test API connectivity manually
4. Check firewall/network issues

---

**Status:** Ready to deploy  
**Estimated setup time:** 20-30 minutes  
**First data collection:** Tomorrow at 2:00 AM (or at your scheduled time)

Go ahead and run the setup! 🚀
