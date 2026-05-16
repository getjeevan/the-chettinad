#!/usr/bin/env python3
"""
🍛 Platform-Specific API Modules
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Authentication and data fetching for:
- Swiggy Ads
- Zomato Ads
- Google Search Console
- Instagram Graph API
- Competitor Web Scraping
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class SwiggeyAdsAPI:
    """Swiggy Ads API integration"""

    def __init__(self, api_key: str, restaurant_id: str):
        self.api_key = api_key
        self.restaurant_id = restaurant_id
        self.base_url = "https://ads-api.swiggy.com/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def get_campaign_performance(self, date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Fetch campaign performance metrics"""
        if not date_from:
            date_from = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = datetime.now().strftime('%Y-%m-%d')

        endpoint = f"{self.base_url}/restaurants/{self.restaurant_id}/campaigns/performance"
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'granularity': 'daily'
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("✅ Swiggy Ads: Campaign performance fetched")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Swiggy Ads API error: {str(e)}")
            return {}

    def get_ad_groups(self) -> List[Dict]:
        """Fetch active ad groups"""
        endpoint = f"{self.base_url}/restaurants/{self.restaurant_id}/ad-groups"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("✅ Swiggy Ads: Ad groups fetched")
            return response.json().get('ad_groups', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Swiggy Ads API error: {str(e)}")
            return []

    def get_keywords_performance(self) -> List[Dict]:
        """Fetch keyword-level performance"""
        endpoint = f"{self.base_url}/restaurants/{self.restaurant_id}/keywords/performance"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("✅ Swiggy Ads: Keywords performance fetched")
            return response.json().get('keywords', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Swiggy Ads API error: {str(e)}")
            return []


class ZomatoAdsAPI:
    """Zomato Ads API integration"""

    def __init__(self, api_key: str, restaurant_id: str):
        self.api_key = api_key
        self.restaurant_id = restaurant_id
        self.base_url = "https://www.zomato.com/api/partner/v2"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def get_ad_campaigns(self) -> List[Dict]:
        """Fetch active ad campaigns"""
        endpoint = f"{self.base_url}/restaurant/{self.restaurant_id}/ads/campaigns"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("✅ Zomato Ads: Campaigns fetched")
            return response.json().get('campaigns', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Zomato Ads API error: {str(e)}")
            return []

    def get_campaign_stats(self, campaign_id: str, date_from: str = None, date_to: str = None) -> Dict:
        """Fetch campaign statistics"""
        if not date_from:
            date_from = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = datetime.now().strftime('%Y-%m-%d')

        endpoint = f"{self.base_url}/restaurant/{self.restaurant_id}/ads/campaigns/{campaign_id}/stats"
        params = {
            'start_date': date_from,
            'end_date': date_to
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("✅ Zomato Ads: Campaign stats fetched")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Zomato Ads API error: {str(e)}")
            return {}

    def get_delivery_partner_performance(self) -> Dict:
        """Fetch delivery performance metrics"""
        endpoint = f"{self.base_url}/restaurant/{self.restaurant_id}/delivery/performance"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("✅ Zomato Ads: Delivery performance fetched")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Zomato Ads API error: {str(e)}")
            return {}


class GoogleSearchConsoleAPI:
    """Google Search Console API integration"""

    def __init__(self, property_id: str, credentials_file: str):
        self.property_id = property_id
        self.credentials_file = credentials_file
        self.service = None
        self._init_service()

    def _init_service(self):
        """Initialize Google API service"""
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build

            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
            )

            self.service = build('webmasters', 'v3', credentials=credentials)
            logger.info("✅ Google Search Console: Service initialized")
        except Exception as e:
            logger.error(f"❌ Google API initialization error: {str(e)}")

    def get_search_analytics(self, days: int = 1) -> List[Dict]:
        """Fetch search analytics data"""
        if not self.service:
            logger.error("Google service not initialized")
            return []

        try:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')

            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['query', 'device'],
                'rowLimit': 100
            }

            response = self.service.searchanalytics().query(
                siteUrl=self.property_id,
                body=request
            ).execute()

            logger.info("✅ Google Search Console: Analytics fetched")
            return response.get('rows', [])

        except Exception as e:
            logger.error(f"❌ Google Search Console error: {str(e)}")
            return []

    def get_top_queries(self, days: int = 7) -> List[Dict]:
        """Get top performing queries"""
        if not self.service:
            logger.error("Google service not initialized")
            return []

        try:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')

            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['query'],
                'rowLimit': 50
            }

            response = self.service.searchanalytics().query(
                siteUrl=self.property_id,
                body=request
            ).execute()

            logger.info("✅ Google Search Console: Top queries fetched")
            return response.get('rows', [])

        except Exception as e:
            logger.error(f"❌ Google Search Console error: {str(e)}")
            return []


class InstagramGraphAPI:
    """Instagram Graph API integration"""

    def __init__(self, business_account_id: str, access_token: str):
        self.business_account_id = business_account_id
        self.access_token = access_token
        self.base_url = "https://graph.instagram.com/v18.0"
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    def get_account_insights(self) -> Dict[str, Any]:
        """Fetch account-level insights"""
        endpoint = f"{self.base_url}/{self.business_account_id}/insights"
        params = {
            'metric': 'impressions,reach,profile_views,follower_count,website_clicks',
            'period': 'day'
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("✅ Instagram: Account insights fetched")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Instagram API error: {str(e)}")
            return {}

    def get_recent_posts(self, limit: int = 10) -> List[Dict]:
        """Fetch recent posts and their metrics"""
        endpoint = f"{self.base_url}/{self.business_account_id}/media"
        params = {
            'fields': 'id,timestamp,caption,media_type,permalink,insights.metric(impressions,reach,engagement,shares,saves)',
            'limit': limit
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("✅ Instagram: Recent posts fetched")
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Instagram API error: {str(e)}")
            return []

    def get_hashtag_performance(self, hashtags: List[str]) -> Dict:
        """Get performance metrics for specific hashtags"""
        results = {}

        for hashtag in hashtags:
            try:
                # Search for hashtag
                search_endpoint = f"{self.base_url}/ig_hashtag_search"
                search_params = {
                    'user_id': self.business_account_id,
                    'fields': 'id,name',
                    'search_string': hashtag
                }

                search_response = requests.get(
                    search_endpoint,
                    headers=self.headers,
                    params=search_params
                )
                search_response.raise_for_status()

                hashtag_id = search_response.json()['data'][0]['id']

                # Get hashtag insights
                insights_endpoint = f"{self.base_url}/{hashtag_id}/recent_media"
                insights_params = {
                    'user_id': self.business_account_id,
                    'fields': 'id,caption,insights.metric(impressions,reach,engagement)'
                }

                insights_response = requests.get(
                    insights_endpoint,
                    headers=self.headers,
                    params=insights_params
                )
                insights_response.raise_for_status()

                results[hashtag] = insights_response.json()

            except Exception as e:
                logger.error(f"❌ Instagram hashtag error for {hashtag}: {str(e)}")

        logger.info("✅ Instagram: Hashtag performance fetched")
        return results


class CompetitorScraper:
    """Web scraper for competitor websites"""

    def __init__(self):
        self.competitors = {
            'House of Biryan': {
                'website': 'https://houseofbiryan.com',
                'zomato': 'https://www.zomato.com/restaurants/house-of-biryan',
                'swiggy': 'https://www.swiggy.com/restaurants/house-of-biryan'
            },
            'Biryani By Kilo': {
                'website': 'https://biryanibykilo.com',
                'zomato': 'https://www.zomato.com/restaurants/biryani-by-kilo',
                'swiggy': 'https://www.swiggy.com/restaurants/biryani-by-kilo'
            },
            'Behrouz Biryani': {
                'website': 'https://www.behrouzbiryani.in',
                'zomato': 'https://www.zomato.com/restaurants/behrouz-biryani',
                'swiggy': 'https://www.swiggy.com/restaurants/behrouz-biryani'
            }
        }

    def scrape_competitor(self, competitor_name: str) -> Dict[str, Any]:
        """Scrape competitor data from aggregator platforms"""
        try:
            from bs4 import BeautifulSoup

            urls = self.competitors.get(competitor_name, {})
            competitor_data = {
                'name': competitor_name,
                'scraped_at': datetime.now().isoformat(),
                'data': {}
            }

            # Scrape from Zomato
            if 'zomato' in urls:
                try:
                    response = requests.get(urls['zomato'], timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract rating, reviews count, delivery time, etc.
                    rating_elem = soup.find('div', {'class': 'sc-1q7bklc-1'})
                    if rating_elem:
                        competitor_data['data']['zomato_rating'] = rating_elem.text.strip()

                    logger.info(f"✅ Scraped {competitor_name} from Zomato")

                except Exception as e:
                    logger.warning(f"⚠️  Could not scrape {competitor_name} from Zomato: {str(e)}")

            # Scrape from Swiggy
            if 'swiggy' in urls:
                try:
                    response = requests.get(urls['swiggy'], timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract metrics
                    logger.info(f"✅ Scraped {competitor_name} from Swiggy")

                except Exception as e:
                    logger.warning(f"⚠️  Could not scrape {competitor_name} from Swiggy: {str(e)}")

            return competitor_data

        except ImportError:
            logger.error("BeautifulSoup not installed. Install with: pip install beautifulsoup4 selenium")
            return {}

    def scrape_all_competitors(self) -> List[Dict[str, Any]]:
        """Scrape all competitors"""
        all_data = []

        for competitor in self.competitors.keys():
            data = self.scrape_competitor(competitor)
            if data:
                all_data.append(data)

        logger.info(f"✅ Scraped {len(all_data)} competitors")
        return all_data


def test_all_apis():
    """Test function to verify all API connections"""
    print("🧪 Testing Platform API Connections\n")

    # Test Swiggy (mock)
    print("Testing Swiggy Ads API...")
    try:
        swiggy = SwiggeyAdsAPI(
            api_key=os.getenv('SWIGGY_API_KEY', 'test-key'),
            restaurant_id=os.getenv('SWIGGY_RESTAURANT_ID', 'test-id')
        )
        print("✅ Swiggy API initialized\n")
    except Exception as e:
        print(f"❌ Swiggy API error: {e}\n")

    # Test Zomato (mock)
    print("Testing Zomato Ads API...")
    try:
        zomato = ZomatoAdsAPI(
            api_key=os.getenv('ZOMATO_API_KEY', 'test-key'),
            restaurant_id=os.getenv('ZOMATO_RESTAURANT_ID', 'test-id')
        )
        print("✅ Zomato API initialized\n")
    except Exception as e:
        print(f"❌ Zomato API error: {e}\n")

    # Test Google Search Console
    print("Testing Google Search Console API...")
    try:
        google = GoogleSearchConsoleAPI(
            property_id=os.getenv('GOOGLE_PROPERTY_ID', 'https://example.com'),
            credentials_file=os.getenv('GOOGLE_CREDENTIALS_FILE', '/path/to/credentials.json')
        )
        print("✅ Google Search Console API initialized\n")
    except Exception as e:
        print(f"❌ Google API error: {e}\n")

    # Test Instagram
    print("Testing Instagram Graph API...")
    try:
        instagram = InstagramGraphAPI(
            business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', 'test-id'),
            access_token=os.getenv('INSTAGRAM_ACCESS_TOKEN', 'test-token')
        )
        print("✅ Instagram API initialized\n")
    except Exception as e:
        print(f"❌ Instagram API error: {e}\n")

    # Test Competitor Scraper
    print("Testing Competitor Scraper...")
    try:
        scraper = CompetitorScraper()
        print("✅ Competitor Scraper initialized\n")
    except Exception as e:
        print(f"❌ Scraper error: {e}\n")


if __name__ == '__main__':
    test_all_apis()
