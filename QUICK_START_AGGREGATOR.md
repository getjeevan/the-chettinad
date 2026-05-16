# 🚀 Quick Start - Data Aggregator
**Biryani Express Live Data Collection**

---

## 📋 What You Just Got

A complete **automated data aggregation system** that pulls live data from:
- ✅ **Swiggy Ads** — Campaign performance, spend, ROI
- ✅ **Zomato Ads** — Ad metrics, conversions, delivery performance
- ✅ **Google Search Console** — Keyword rankings, traffic, CTR
- ✅ **Instagram Graph API** — Post engagement, reach, saves, followers
- ✅ **Competitor Websites** — Pricing, menus, reviews (via scraping)

**Runs automatically every day** and stores data locally on your Hermes server.

---

## 🎯 In 3 Steps:

### Step 1: SSH to On-Prem Server
```bash
ssh getjeevan@100.112.118.83
# Password: 1234bcbc9
```

### Step 2: Run Setup Script
```bash
cd /path/to/biryani-express-repo
sudo bash setup_hermes_aggregator.sh
```

### Step 3: Add Your Credentials
```bash
sudo nano /opt/hermes/config/credentials.json
```

**That's it!** Data collection starts tomorrow at 2:00 AM.

---

## 📊 What Gets Collected (Daily)

**Swiggy Ads:**
- Campaign names & performance
- Impressions, clicks, conversions
- Spend & ROI
- CTR & CPA

**Zomato Ads:**
- All campaign metrics
- Delivery performance
- Ad group performance

**Google SEO:**
- Top 50 keyword rankings
- Impressions & click data
- CTR by keyword
- Device breakdown

**Instagram:**
- Post reach & impressions
- Engagement rates
- Saves & shares
- Follower growth

**Competitors:**
- House of Biryan metrics
- Biryani By Kilo data
- Behrouz Biryani stats

---

## 💾 Where Data Lives

**Database:**
```
/opt/hermes/data/biryani-express/biryani_metrics.db
```

**Daily Reports:**
```
/opt/hermes/data/biryani-express/daily_report_2026-05-17.json
/opt/hermes/data/biryani-express/daily_report_2026-05-18.json
...
```

**Logs:**
```
/var/log/hermes/biryani_aggregator.log
```

---

## 🔌 Access Data

### Via HTTP API
```bash
# Get latest Swiggy metrics
curl http://192.168.1.168:9119/api/metrics/swiggy/latest

# Get SEO keywords
curl http://192.168.1.168:9119/api/metrics/seo/keywords

# Get Instagram insights
curl http://192.168.1.168:9119/api/metrics/instagram/insights

# Get all competitor data
curl http://192.168.1.168:9119/api/metrics/competitors/all
```

### Via Database
```bash
sqlite3 /opt/hermes/data/biryani-express/biryani_metrics.db
SELECT * FROM swiggy_ads ORDER BY timestamp DESC LIMIT 5;
SELECT * FROM instagram_metrics WHERE date = '2026-05-17';
```

### Via JSON Reports
```bash
cat /opt/hermes/data/biryani-express/daily_report_latest.json | jq .
```

---

## 📝 Required Credentials

You need to provide these API keys:

| Platform | Where to Get | Notes |
|----------|-------------|-------|
| **Swiggy API Key** | Swiggy Partner Dashboard → API Keys | Required for ads data |
| **Swiggy Restaurant ID** | Same dashboard | Your restaurant's ID |
| **Zomato API Key** | Zomato Partner → API Keys | Required for ads data |
| **Zomato Restaurant ID** | Same dashboard | Your restaurant's ID |
| **Google Property ID** | Google Search Console | Usually: https://yoursite.com |
| **Google Credentials JSON** | Google Cloud Console → OAuth 2.0 | Download as JSON file |
| **Instagram Business Account ID** | Instagram Settings → Business Info | Your account ID |
| **Instagram Access Token** | Instagram Graph API Explorer | 60-day token |

---

## ✅ Verify Installation

```bash
# Check database created
ls -lh /opt/hermes/data/biryani-express/biryani_metrics.db

# Check cron job scheduled
crontab -l | grep hermes_data_aggregator

# Check logs
tail -f /var/log/hermes/biryani_aggregator.log

# Check tables created
sqlite3 /opt/hermes/data/biryani-express/biryani_metrics.db ".tables"
```

---

## 🔄 Manual Runs (Test)

```bash
# Run aggregator manually (one-time)
python3 /opt/hermes/bin/hermes_data_aggregator.py

# Expected output:
# ============================================================
# 🍛 BIRYANI EXPRESS DAILY DATA AGGREGATION
# ============================================================
# ✅ Database initialized
# 🔗 Fetching Swiggy Ads data...
# ✅ Swiggy data fetched and stored
# ... (and so on for other platforms)
# ✅ AGGREGATION COMPLETE
```

---

## 🛠️ Troubleshooting

**"API Key Invalid"**
→ Check credentials file: `cat /opt/hermes/config/credentials.json`

**"Database Locked"**
→ Kill existing process: `pkill -f hermes_data_aggregator`

**"Permission Denied"**
→ Fix permissions: `sudo chmod +x /opt/hermes/bin/hermes_data_aggregator.py`

**"No data showing"**
→ Check logs: `tail -f /var/log/hermes/biryani_aggregator.log`

---

## 📅 Scheduling

**Default:** Daily at 2:00 AM  
**Change time:**
```bash
# Edit crontab
crontab -e

# Change time (e.g., 6:00 AM):
0 6 * * * /usr/bin/python3 /opt/hermes/bin/hermes_data_aggregator.py >> /var/log/hermes/biryani_aggregator.log 2>&1
```

---

## 🎯 Files Included

| File | Purpose |
|------|---------|
| `hermes_data_aggregator.py` | Main aggregator script |
| `hermes_platform_apis.py` | Platform-specific API modules |
| `credentials_template.json` | Template for your API keys |
| `setup_hermes_aggregator.sh` | One-command setup script |
| `HERMES_ONPREM_DEPLOYMENT.md` | Detailed deployment guide |
| `QUICK_START_AGGREGATOR.md` | This file |

---

## 📞 Next Steps

1. **SSH to server** (via Tailscale: `ssh getjeevan@100.112.118.83`)
2. **Run setup script** (`sudo bash setup_hermes_aggregator.sh`)
3. **Add credentials** to `/opt/hermes/config/credentials.json`
4. **Wait for first run** (tomorrow at 2:00 AM)
5. **Check data** in database or via API

---

**Everything is ready to go!** 🚀

Just add your credentials and the system will automatically pull live data every day.

Check logs with:
```bash
tail -f /var/log/hermes/biryani_aggregator.log
```
