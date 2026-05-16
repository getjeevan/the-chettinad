# 🇳🇴 Biryani Express Oslo - Data Aggregator Setup
**Nordic Market Intelligence System**

---

## ✅ What Changed

| Component | India Setup | Oslo Setup |
|-----------|------------|-----------|
| **Primary Delivery Platform** | Swiggy Ads | **Foodora** |
| **Secondary Platform** | Zomato Ads | **Wolt** |
| **Region** | Pan-India | **Oslo, Norway** |
| **Domain** | biryaniexpress.in | **biryaniexpress.no** |
| **Competitors** | Indian biryani brands | **Nordic Indian restaurants** |

---

## 📊 Data Collection Platforms

### **Foodora** (Nordic Delivery Leader)
- API: `https://api.foodora.com/v2`
- What we track:
  - Campaign performance (spend, ROI, conversions)
  - Restaurant analytics
  - Order metrics
  - Delivery performance

### **Wolt** (Nordic Delivery Platform)
- API: `https://api.wolt.com/v1`
- What we track:
  - Marketing campaigns
  - Campaign analytics
  - Delivery performance
  - Customer insights

### **Google Search Console**
- Property: `https://biryaniexpress.no`
- What we track:
  - Organic keyword rankings
  - Search impressions & clicks
  - CTR by keyword
  - Device breakdown

### **Instagram Graph API**
- Business Account ID: `[Your Instagram Business Account]`
- What we track:
  - Post engagement
  - Follower growth
  - Reach & impressions
  - Content performance

---

## 🏪 Nordic Competitors Tracked

We monitor these Oslo-based Indian restaurants:

| Competitor | Website | Foodora | Wolt |
|-----------|---------|---------|------|
| **Curry in Hurry** | curryinharry.no | ✅ Tracked | ✅ Tracked |
| **Spice Kitchen** | spicekitchen.no | ✅ Tracked | ✅ Tracked |
| **Mumbai Masala** | mumbaimasala.no | ✅ Tracked | ✅ Tracked |
| **Desi Kitchen Oslo** | desikitchen.no | ✅ Tracked | ✅ Tracked |

---

## 🔑 Required Credentials

You need to get these from your Nordic accounts:

### **1. Foodora API Credentials**
Where to get:
- Log in to: https://www.foodora.no/restaurant/
- Settings → API Keys → Create New Key
- Copy: API Key + Restaurant ID

### **2. Wolt API Credentials**
Where to get:
- Log in to: https://hub.wolt.com/
- Settings → Business API → Create Token
- Copy: API Key + Restaurant ID

### **3. Google Search Console**
Where to get:
- https://search.google.com/search-console/
- Add property: `https://biryaniexpress.no`
- Download OAuth credentials JSON

### **4. Instagram Business Account**
Where to get:
- Instagram Business Settings → Apps and Websites
- Generate access token via Graph API Explorer
- Copy: Account ID + Access Token

---

## 🚀 Setup Instructions (3 Steps)

### **Step 1: SSH to Server**
```bash
ssh getjeevan@100.112.118.83
# Password: 1234bcbc9
```

### **Step 2: Run Setup**
```bash
cd /path/to/biryani-express
sudo bash setup_hermes_aggregator.sh
```

### **Step 3: Add Nordic Credentials**
```bash
sudo nano /opt/hermes/config/credentials.json
```

Add your Foodora, Wolt, Google, and Instagram credentials.

---

## 📊 Daily Data Collection

**Time:** 2:00 AM (configurable)  
**Frequency:** Daily  
**Duration:** ~5-10 minutes

### **What Gets Collected**

**Foodora (Daily):**
- Campaign spend (NOK)
- Impressions & clicks
- Order conversions
- ROI metrics
- Delivery time data

**Wolt (Daily):**
- Marketing campaign metrics
- Customer acquisition data
- Order value trends
- Delivery performance
- Peak order times

**Google SEO:**
- Keyword rankings for: "biryani oslo", "indian food oslo", etc.
- Organic search traffic
- Click-through rates
- Device breakdown

**Instagram:**
- Post engagement metrics
- Follower growth rate
- Story performance
- Save & share counts

**Competitors:**
- Curry in Hurry: Pricing, ratings, delivery time
- Spice Kitchen: Menu changes, reviews
- Mumbai Masala: Order volume indicators
- Desi Kitchen: Competitive positioning

---

## 💾 Data Storage Locations

```
Database (SQLite):
  /opt/hermes/data/biryani-express/biryani_metrics.db

Tables:
  ✓ foodora_ads          (daily campaign metrics)
  ✓ wolt_ads             (daily campaign metrics)
  ✓ google_seo           (keyword rankings & traffic)
  ✓ instagram_metrics    (social engagement)
  ✓ competitor_data      (competitor intelligence)
  ✓ raw_json_data        (backup of all API responses)

Daily Reports (JSON):
  /opt/hermes/data/biryani-express/daily_report_YYYY-MM-DD.json

Logs:
  /var/log/hermes/biryani_aggregator.log
```

---

## 🔌 Accessing Your Data

### **Via HTTP API**
```bash
# Foodora performance
curl http://192.168.1.168:9119/api/metrics/foodora/latest

# Wolt performance
curl http://192.168.1.168:9119/api/metrics/wolt/latest

# SEO keywords
curl http://192.168.1.168:9119/api/metrics/seo/keywords

# Instagram insights
curl http://192.168.1.168:9119/api/metrics/instagram/insights

# Competitor data
curl http://192.168.1.168:9119/api/metrics/competitors/all
```

### **Via Database**
```bash
sqlite3 /opt/hermes/data/biryani-express/biryani_metrics.db

# View Foodora data
SELECT * FROM foodora_ads ORDER BY timestamp DESC LIMIT 10;

# View Wolt data
SELECT * FROM wolt_ads ORDER BY timestamp DESC LIMIT 10;

# View SEO rankings
SELECT keyword, position, impressions FROM google_seo 
  WHERE date = '2026-05-17' ORDER BY position ASC;

# View Instagram engagement
SELECT post_type, engagement_rate, reach FROM instagram_metrics 
  WHERE date = '2026-05-17' ORDER BY engagement_rate DESC;

# View competitor ratings
SELECT competitor_name, metric_name, metric_value FROM competitor_data 
  WHERE date = '2026-05-17';
```

---

## 📈 Key Metrics Tracked

### **Foodora**
- Daily spend (NOK)
- Impressions & CTR
- Conversions & ROI
- Customer acquisition cost
- Average order value

### **Wolt**
- Campaign performance
- Order count
- Revenue generated
- Delivery time performance
- Customer ratings

### **SEO (Google)**
- Keyword rankings (top 50)
- Organic traffic
- Click-through rate
- Impression share
- Device performance

### **Instagram**
- Engagement rate
- Reach & impressions
- Save rate
- Share rate
- Follower growth

### **Competitors**
- Menu pricing comparison
- Rating trends
- Delivery time benchmarks
- Review sentiment
- Promotional activity

---

## 🎯 Nordic Market Context

### **Oslo Foodservice Market**
- Growing demand for international cuisine
- Delivery platforms: Foodora, Wolt dominant
- Price-sensitive market (NOK ~200-350 per meal)
- High social media influence

### **Indian Food Trend**
- Increasing popularity in Oslo
- Premium positioning possible
- Customer base: Expats + local food enthusiasts
- High engagement on social media

### **Biryani Express Advantage**
- First-mover in Oslo (biryaniexpress.no)
- Authentic Indian cuisine
- Customization focus (spice levels, proteins)
- Strong Nordic delivery platform presence

---

## 📋 Configuration Checklist

- [ ] SSH access via Tailscale working
- [ ] Python 3.8+ installed on server
- [ ] Foodora API credentials obtained
- [ ] Wolt API credentials obtained
- [ ] Google Search Console property set up (biryaniexpress.no)
- [ ] Google OAuth credentials JSON downloaded
- [ ] Instagram Business Account ID + Token obtained
- [ ] Setup script run successfully
- [ ] Test execution passed
- [ ] Cron job scheduled
- [ ] First daily run completed (tomorrow at 2 AM)

---

## 📊 Expected Data Points (First Month)

- **1,500+ Foodora metrics** (spend, ROI, conversions)
- **1,500+ Wolt metrics** (campaign data, performance)
- **1,500+ SEO records** (keyword rankings, traffic)
- **300+ Instagram metrics** (post engagement)
- **200+ Competitor data points** (pricing, ratings)
- **30 Daily JSON reports** (full snapshot per day)

**Total: ~5,000 data points for historical analysis**

---

## 🔄 Daily Workflow

```
2:00 AM
  ↓
Aggregator wakes up
  ↓
Connects to Foodora API → Pulls campaign data
Connects to Wolt API → Pulls marketing data
Queries Google Search Console → Gets SEO data
Calls Instagram Graph API → Gets engagement data
Scrapes Nordic competitors → Gets pricing/ratings
  ↓
Stores all data in SQLite
  ↓
Exports daily JSON report
  ↓
Logs completion
  ↓
Next run: Tomorrow 2:00 AM
```

---

## 🎬 Next Steps

1. **Get your Nordic credentials**
   - Foodora API key + Restaurant ID
   - Wolt API key + Restaurant ID
   - Google credentials JSON
   - Instagram Account ID + Token

2. **SSH to on-prem server** (via Tailscale)

3. **Run setup script**
   ```bash
   sudo bash setup_hermes_aggregator.sh
   ```

4. **Fill in credentials**
   ```bash
   sudo nano /opt/hermes/config/credentials.json
   ```

5. **Monitor first run** (tomorrow at 2 AM)
   ```bash
   tail -f /var/log/hermes/biryani_aggregator.log
   ```

---

## 💡 Nordic-Specific Insights

Data will help you track:
- ✅ Performance vs Curry in Hurry, Spice Kitchen, Mumbai Masala
- ✅ Seasonal trends in Oslo (summer vs winter demand)
- ✅ Foodora vs Wolt platform performance comparison
- ✅ SEO visibility for "biryani oslo", "indian food", etc.
- ✅ Instagram content performance in Nordic market
- ✅ Optimal pricing for Oslo market (NOK)
- ✅ Delivery time benchmarks
- ✅ Customer acquisition trends

---

**Status:** Ready to deploy on Oslo server  
**Market:** Norway (biryaniexpress.no)  
**Platforms:** Foodora + Wolt  
**Competitors:** 4 Oslo-based Indian restaurants  

🚀 Ready to start collecting Nordic market intelligence!
