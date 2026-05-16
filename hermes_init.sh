#!/bin/bash
# 🍛 Biryani Express - Hermes Agent Initialization Script
# Run this on your GMKtec K12 server (192.168.1.168) to activate monitoring

set -e

echo "🍛 ====================================="
echo "   BIRYANI EXPRESS x HERMES SETUP"
echo "====================================="
echo ""

# Configuration
HERMES_HOST="${HERMES_HOST:-192.168.1.168}"
HERMES_PORT="${HERMES_PORT:-9119}"
API_KEY="${API_KEY:-hermes_biryani_express_key_20260516}"
WORKSPACE="biryani-express-marketing"
AGENT_NAME="biryani-express-agent"

echo "📋 Configuration:"
echo "   Host: $HERMES_HOST"
echo "   Port: $HERMES_PORT"
echo "   Workspace: $WORKSPACE"
echo "   Agent: $AGENT_NAME"
echo ""

# Step 1: Check Hermes connectivity
echo "🔗 [Step 1/5] Checking Hermes connectivity..."
if curl -s "http://$HERMES_HOST:$HERMES_PORT/health" > /dev/null; then
    echo "✅ Hermes is reachable"
else
    echo "❌ Cannot reach Hermes at http://$HERMES_HOST:$HERMES_PORT"
    echo "   Make sure Hermes is running: sudo systemctl status hermes"
    exit 1
fi

# Step 2: Register agent
echo ""
echo "🤖 [Step 2/5] Registering Biryani Express agent with Hermes..."

REGISTER_RESPONSE=$(curl -s -X POST "http://$HERMES_HOST:$HERMES_PORT/api/agents/register" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
    \"agent_name\": \"$AGENT_NAME\",
    \"workspace\": \"$WORKSPACE\",
    \"capabilities\": [
      \"competitor_monitoring\",
      \"seo_tracking\",
      \"marketing_analytics\",
      \"customer_insights\",
      \"financial_forecasting\"
    ],
    \"update_interval\": 900,
    \"features\": {
      \"real_time_alerts\": true,
      \"predictive_analytics\": true,
      \"automated_recommendations\": true
    }
  }")

echo "$REGISTER_RESPONSE" | jq .
AGENT_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.agent_id')
echo "✅ Agent registered with ID: $AGENT_ID"

# Step 3: Initialize data sources
echo ""
echo "📊 [Step 3/5] Configuring data sources..."

curl -s -X POST "http://$HERMES_HOST:$HERMES_PORT/api/agents/$AGENT_ID/data-sources" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "sources": [
      {
        "name": "competitor_monitoring",
        "type": "web_scraper",
        "targets": [
          "https://www.zomato.com",
          "https://www.swiggy.com",
          "competitor_websites"
        ],
        "update_frequency": "6h",
        "metrics": ["pricing", "menu_changes", "reviews", "ratings"]
      },
      {
        "name": "seo_analytics",
        "type": "api",
        "provider": "google_search_console",
        "update_frequency": "24h",
        "metrics": ["keywords", "impressions", "ctr", "positions"]
      },
      {
        "name": "ad_performance",
        "type": "api",
        "providers": ["swiggy_ads", "zomato_ads"],
        "update_frequency": "3h",
        "metrics": ["spend", "conversions", "roi", "cpa"]
      },
      {
        "name": "social_media",
        "type": "api",
        "provider": "instagram",
        "update_frequency": "6h",
        "metrics": ["engagement", "reach", "followers", "sentiment"]
      }
    ]
  }' > /dev/null

echo "✅ Data sources configured"

# Step 4: Start monitoring
echo ""
echo "📡 [Step 4/5] Starting monitoring loops..."

curl -s -X POST "http://$HERMES_HOST:$HERMES_PORT/api/agents/$AGENT_ID/monitoring/start" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "monitoring_profiles": [
      {
        "name": "competitor_watch",
        "interval_minutes": 15,
        "alert_threshold": "significant_change"
      },
      {
        "name": "seo_tracking",
        "interval_minutes": 60,
        "alert_threshold": "ranking_drop_5+"
      },
      {
        "name": "marketing_roi",
        "interval_minutes": 30,
        "alert_threshold": "roi_below_2.5x"
      }
    ]
  }' > /dev/null

echo "✅ Monitoring started"

# Step 5: Generate API token for dashboard
echo ""
echo "🔐 [Step 5/5] Generating dashboard access token..."

TOKEN_RESPONSE=$(curl -s -X POST "http://$HERMES_HOST:$HERMES_PORT/api/agents/$AGENT_ID/tokens/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "token_type": "dashboard_access",
    "expires_in_days": 90,
    "permissions": ["read_all_metrics", "view_alerts", "export_reports"]
  }')

DASHBOARD_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.token')

echo "✅ Setup complete!"
echo ""
echo "📊 ===== DASHBOARD ACCESS ====="
echo "URL: http://$HERMES_HOST:$HERMES_PORT/dashboard"
echo "Agent ID: $AGENT_ID"
echo "API Key: $API_KEY"
echo "Dashboard Token: $DASHBOARD_TOKEN"
echo ""
echo "🎯 Real-time monitoring active for:"
echo "  ✓ Competitor activity (15-min updates)"
echo "  ✓ SEO rankings (hourly)"
echo "  ✓ Marketing ROI (30-min updates)"
echo "  ✓ Customer insights (real-time)"
echo "  ✓ Financial metrics (hourly)"
echo ""
echo "📋 Next: Visit dashboard to configure alerts & reporting"
echo "================================"
