#!/usr/bin/env python3
"""
🍛 Biryani Express Market Intelligence Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Real-time competitive analysis, SEO optimization recommendations,
and digital marketing strategy insights powered by Claude AI.
"""

import json
from typing import Any
from datetime import datetime
import anthropic

# Market Intelligence Database
MARKET_DATA = {
    "competitors": {
        "tier_1": {
            "Biryani By Kilo": {
                "founded": 2015,
                "revenue_2026": "₹100+ Cr",
                "growth_strategy": "Menu specialization, franchise model",
                "strengths": ["Strong brand", "Pan-India presence", "Digital marketing"],
                "weaknesses": ["High operational costs", "Complex menu"],
                "delivery_time": "30-45 min",
            },
            "Behrouz Biryani": {
                "founded": 2016,
                "revenue_2026": "₹1,660 Cr",
                "growth_strategy": "Premium positioning, dine-in focus",
                "strengths": ["Premium brand", "High AOV", "Established"],
                "weaknesses": ["Dine-in dependent", "Higher prices", "Slower delivery"],
                "delivery_time": "45-60 min",
            },
            "House of Biryan": {
                "founded": 2022,
                "revenue_2024": "₹33.90 Cr",
                "revenue_2026_target": "₹100 Cr",
                "growth_strategy": "Rapid expansion (22→40+ stores)",
                "stores": 22,
                "per_kitchen_revenue": "₹2.5 Cr/year (~₹20L/month)",
                "strengths": ["Customization focus", "Fast growth", "Micro-cafe model"],
                "weaknesses": ["New brand", "Limited scale"],
                "delivery_time": "30-45 min",
            },
        },
    },
    "market_metrics": {
        "cloud_kitchen_market_2026": "$1.1B USD",
        "projected_2032": "$2.95B USD",
        "cagr": "12-16.63%",
        "india_qsr_market_2030": "₹43.5B",
        "qsr_cagr": "9.36%",
    },
    "seo_opportunities": {
        "hyperlocal_seo": {
            "potential_growth": "40-50% in 30 days",
            "case_study": "Mumbai kitchen achieved 48% surge in organic orders",
            "actions": [
                "Optimize Google Business Profile",
                "Create location-specific landing pages",
                "Build local backlinks",
            ],
        },
        "paid_advertising": {
            "benchmark_roi": "3.2x",
            "example": "₹15,000 spent = ₹48,000 earned in 7 days",
            "optimal_radius": "3-7 km",
        },
        "influencer_marketing": {
            "best_performers": "Micro-influencers (1K-10K followers)",
            "engagement_multiplier": "7x vs macro-influencers",
            "example": "10 influencers = 200+ orders in 1 week",
        },
    },
    "financial_benchmarks": {
        "monthly_per_kitchen": "₹20 Lakh (~$2,400)",
        "average_order_value": "₹500-800",
        "optimal_aov_target": "₹650-900",
        "customer_acquisition_cost": "<₹150 optimal",
    },
}

def create_agent():
    """Initialize the Biryani Express Market Intelligence Agent."""
    client = anthropic.Anthropic()

    system_prompt = """You are the Biryani Express Market Intelligence Agent, an expert in cloud kitchen business strategy, SEO optimization, and digital marketing for the Indian food delivery market.

Your expertise:
- Cloud kitchen industry dynamics (2026 market data)
- Competitive landscape analysis (Biryani By Kilo, Behrouz, House of Biryan, etc.)
- SEO strategy for food delivery businesses
- Digital marketing tactics (paid ads, influencer marketing, social media)
- Financial benchmarking and unit economics
- Local market dynamics and customization strategies

You have access to comprehensive market intelligence about:
1. Competitor analysis (Tier 1 market leaders)
2. Market metrics and growth projections
3. SEO opportunities and benchmarks
4. Digital marketing strategies that work
5. Financial benchmarks for cloud kitchens

When analyzing queries:
- Provide data-backed insights with specific numbers
- Reference successful case studies and benchmarks
- Give actionable recommendations with timelines
- Identify quick wins vs. long-term strategies
- Consider Biryani Express's competitive positioning
- Suggest metrics to track success

Always structure responses clearly with:
- Key Insights (data-backed)
- Competitive Advantage Opportunities
- Recommended Actions (with timelines)
- Expected ROI/Impact
- Success Metrics
"""

    tools = [
        {
            "name": "query_market_data",
            "description": "Query the market intelligence database for competitor info, market metrics, SEO opportunities, or financial benchmarks",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query_type": {
                        "type": "string",
                        "enum": ["competitors", "market_metrics", "seo", "financials", "all"],
                        "description": "Type of market data to retrieve",
                    },
                    "focus_area": {
                        "type": "string",
                        "description": "Specific area within query_type (e.g., 'hyperlocal_seo', 'House of Biryan', 'paid_advertising')",
                    },
                },
                "required": ["query_type"],
            },
        },
        {
            "name": "competitive_analysis",
            "description": "Analyze Biryani Express competitive positioning against specific competitors",
            "input_schema": {
                "type": "object",
                "properties": {
                    "competitor": {
                        "type": "string",
                        "enum": ["Biryani By Kilo", "Behrouz Biryani", "House of Biryan", "all"],
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["strengths", "weaknesses", "opportunities", "threats"],
                    },
                },
                "required": ["competitor"],
            },
        },
        {
            "name": "seo_recommendation",
            "description": "Get SEO strategy recommendations tailored for Biryani Express",
            "input_schema": {
                "type": "object",
                "properties": {
                    "focus": {
                        "type": "string",
                        "enum": ["local", "organic", "technical", "content", "all"],
                        "description": "SEO focus area",
                    },
                    "timeline": {
                        "type": "string",
                        "enum": ["30_days", "90_days", "6_months"],
                    },
                },
                "required": ["focus"],
            },
        },
    ]

    return client, system_prompt, tools, MARKET_DATA


def process_tool_call(tool_name: str, tool_input: dict, market_data: dict) -> str:
    """Process tool calls and return market intelligence."""

    if tool_name == "query_market_data":
        query_type = tool_input.get("query_type", "all")
        focus_area = tool_input.get("focus_area")

        if query_type == "all":
            return json.dumps(market_data, indent=2)
        elif query_type in market_data:
            data = market_data[query_type]
            if focus_area and focus_area in data:
                return json.dumps({focus_area: data[focus_area]}, indent=2)
            return json.dumps(data, indent=2)

    elif tool_name == "competitive_analysis":
        competitor = tool_input.get("competitor")
        analysis_type = tool_input.get("analysis_type", "all")

        if competitor == "all":
            competitors = market_data["competitors"]["tier_1"]
            return json.dumps(competitors, indent=2)
        elif competitor in market_data["competitors"]["tier_1"]:
            comp_data = market_data["competitors"]["tier_1"][competitor]
            if analysis_type != "all" and analysis_type in comp_data:
                return json.dumps({competitor: {analysis_type: comp_data[analysis_type]}}, indent=2)
            return json.dumps({competitor: comp_data}, indent=2)

    elif tool_name == "seo_recommendation":
        focus = tool_input.get("focus", "all")
        timeline = tool_input.get("timeline", "90_days")

        if focus == "all" or focus in market_data["seo_opportunities"]:
            seo_data = market_data["seo_opportunities"]
            return json.dumps(
                {
                    "seo_focus": focus,
                    "timeline": timeline,
                    "opportunities": seo_data,
                },
                indent=2,
            )

    return json.dumps({"error": "Tool not found or invalid parameters"})


def run_agent_chat(user_query: str):
    """Run the agent with a user query."""
    client, system_prompt, tools, market_data = create_agent()

    print(f"\n{'='*70}")
    print(f"🍛 BIRYANI EXPRESS MARKET INTELLIGENCE AGENT")
    print(f"{'='*70}")
    print(f"\n📋 Query: {user_query}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'-'*70}\n")

    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )

        # Check if we need to process tool calls
        if response.stop_reason == "tool_use":
            # Process each tool call
            assistant_message = {"role": "assistant", "content": response.content}
            messages.append(assistant_message)

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Processing: {block.name}")
                    print(f"   Input: {json.dumps(block.input, indent=2)}\n")

                    result = process_tool_call(block.name, block.input, market_data)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            messages.append({"role": "user", "content": tool_results})

        else:
            # Final response
            for block in response.content:
                if hasattr(block, "text"):
                    print("🎯 INTELLIGENCE REPORT:\n")
                    print(block.text)
            break

    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    # Example queries
    queries = [
        "What are Biryani Express's competitive advantages against House of Biryan and how should we position ourselves?",
        "Give me a 30-day SEO action plan with expected ROI for Biryani Express in the Indian market.",
        "Compare financial metrics: what's the monthly revenue potential for a cloud kitchen like Biryani Express based on market benchmarks?",
    ]

    # Run first query as demonstration
    run_agent_chat(queries[0])
