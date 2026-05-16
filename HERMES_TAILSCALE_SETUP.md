# 🔗 Hermes Setup via Tailscale (Recommended)

Since you're using Tailscale, here's how to activate monitoring without needing SSH to your Mac.

---

## ✅ Step 1: Run Setup from GMKtec K12 Server

SSH to your on-prem server via Tailscale (no Mac needed):

```bash
# From anywhere with Tailscale access:
ssh getjeevan@100.112.118.83

# Password: 1234bcbc9
```

---

## 📋 Step 2: Deploy the Agent

Once connected to the on-prem server:

```bash
# Navigate to Hermes directory
cd /opt/hermes

# Copy the agent files
wget https://your-repo/biryani_express_agent.py
wget https://your-repo/hermes_monitoring_config.json
wget https://your-repo/hermes_init.sh

# Make script executable
chmod +x hermes_init.sh

# Run initialization
./hermes_init.sh
```

---

## 🎯 Step 3: Verify Connection

```bash
# Test Hermes connectivity
curl http://192.168.1.168:9119/health

# Should return:
# {"status": "healthy", "version": "1.0.0"}
```

---

## 📊 Step 4: Access Dashboard

Once agent is running, access via Tailscale:

```
http://100.112.118.83:9119/dashboard

Or locally:
http://192.168.1.168:9119/dashboard
```

---

## 🔄 Real-Time Monitoring Active

After setup, you'll have:

### ✅ Competitor Monitoring (15-min updates)
- House of Biryan pricing & menu changes
- Biryani By Kilo promotional campaigns
- Behrouz Biryani review sentiment
- Market share estimates

### ✅ SEO Tracking (hourly updates)
- Keyword ranking changes (top 50)
- Organic traffic trends
- Local search visibility
- Backlink monitoring

### ✅ Marketing Analytics (30-min updates)
- Swiggy/Zomato ad ROI
- Instagram engagement metrics
- Influencer campaign performance
- Cost per acquisition trends

### ✅ Customer Insights (real-time)
- Order patterns by time/location
- Customization preferences
- Retention rate tracking
- Revenue forecasts

### ✅ Financial Metrics (hourly)
- Daily revenue tracking
- Average order value trends
- Direct ordering percentage
- Margin improvement tracking

---

## 📧 Daily Intelligence Briefing

Starting tomorrow at 6 AM, you'll receive:

**Subject:** 🍛 Biryani Express Daily Intelligence Report

**Content:**
```
📊 DAILY DIGEST
═══════════════════════════════════

🔴 CRITICAL ALERTS (if any)
- [Alert 1]
- [Alert 2]

💰 FINANCIAL SNAPSHOT
- Revenue (24h): ₹X,XX,XXX
- Orders: XXX
- AOV: ₹XXX
- Margin: XX%

🎯 MARKETING PERFORMANCE
- Paid ads ROI: X.Xx
- Direct orders: XX%
- Organic orders: XX%

🏆 COMPETITIVE WATCH
- House of Biryan: [Activity]
- Biryani By Kilo: [Activity]
- Behrouz: [Activity]

📈 SEO MOVEMENTS
- New keywords ranked: X
- Lost keywords: X
- Top mover: [Keyword]

🌟 RECOMMENDED ACTIONS
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

---

## 🔧 Manual Controls

Once active, you can trigger:

```bash
# Trigger competitor scan
curl -X POST http://100.112.118.83:9119/api/scan/competitors

# Generate forecast
curl -X POST http://100.112.118.83:9119/api/forecast/6-month

# Export weekly report
curl -X GET http://100.112.118.83:9119/api/reports/weekly -o weekly_report.pdf

# Get competitor alerts
curl http://100.112.118.83:9119/api/alerts/competitors
```

---

## 🚨 Status Check

To verify monitoring is running:

```bash
# Check agent status
curl http://100.112.118.83:9119/api/agent/status

# Expected response:
{
  "agent_id": "biryani-express-agent",
  "status": "active",
  "uptime": "2h 45m",
  "last_update": "2026-05-16T14:32:00Z",
  "monitoring_profiles": [
    "competitor_monitoring: active",
    "seo_tracking: active",
    "marketing_analytics: active",
    "customer_insights: active",
    "financial_metrics: active"
  ]
}
```

---

## 📱 Mobile Access

Access Hermes dashboard from phone:

1. Install Tailscale app on phone
2. Connect to Tailscale network
3. Open: `http://100.112.118.83:9119/dashboard`
4. View real-time monitoring

---

## ⚠️ Troubleshooting

**Agent not starting?**
```bash
# Check logs
tail -f /var/log/hermes/agent.log

# Restart Hermes
sudo systemctl restart hermes

# Check port is open
netstat -tlnp | grep 9119
```

**No data showing?**
```bash
# Verify data source connections
curl -X GET http://100.112.118.83:9119/api/data-sources/status

# Check API keys for each data source
cat /opt/hermes/config/api_keys.env
```

**Dashboard not loading?**
```bash
# Check dashboard service
curl http://100.112.118.83:9119/dashboard/health

# Restart dashboard
docker restart hermes-dashboard
```

---

## 🎉 You're Live!

Monitoring is now active. Hermes will:
- ✅ Track competitors every 15 minutes
- ✅ Update SEO rankings hourly
- ✅ Monitor ad performance every 30 minutes
- ✅ Watch customer behavior in real-time
- ✅ Forecast revenue daily
- ✅ Send you insights daily/weekly/monthly

**Next Step:** Go to dashboard and configure your alert preferences!

```
Dashboard: http://100.112.118.83:9119/dashboard
```

---

*Setup Time: ~15 minutes*  
*Monitoring Latency: Real-time*  
*Data Retention: 24 months*
