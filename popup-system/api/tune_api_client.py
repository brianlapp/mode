#!/usr/bin/env python3
"""
🎯 TUNE API CLIENT
Get real analytics data from Tune - Mike's authoritative source
No more Railway volume mount headaches!
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class TuneAPIClient:
    def __init__(self, api_key: str = "NETfeRuo7FOO72yOcwOXj5jK0aCYve"):
        self.api_key = api_key
        self.base_url = "https://api.modemobile.com"  # Mike's Tune network
        
    def get_stats_report(self, 
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        affiliate_id: int = 43045) -> Dict:
        """
        Get Mike's real analytics data from Tune
        Returns data matching the dashboard format
        """
        
        # Default to last 30 days
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # Tune API parameters
        params = {
            'NetworkToken': self.api_key,
            'Target': 'Report',
            'Method': 'getStats',
            'fields[]': [
                'Offer.name',           # Campaign name
                'Stat.impressions',     # Impressions
                'Stat.clicks',          # Clicks  
                'Stat.conversions',     # Real conversions
                'Stat.payout',          # Affiliate payout
                'Stat.revenue',         # Network revenue (if available)
                'Stat.date',            # Date
                'Stat.affiliate_id'     # Affiliate ID
            ],
            'filters[Stat.affiliate_id][conditional]': 'EQUAL_TO',
            'filters[Stat.affiliate_id][values]': affiliate_id,
            'filters[Stat.date][conditional]': 'BETWEEN',
            'filters[Stat.date][values]': f'{start_date}..{end_date}',
            'data_start': start_date,
            'data_end': end_date,
            'totals': 'true'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('response', {}).get('status') == 1:
                return self._format_for_dashboard(data['response']['data'], start_date, end_date)
            else:
                print(f"❌ Tune API error: {data}")
                return self._empty_response(start_date, end_date)
                
        except Exception as e:
            print(f"❌ Tune API request failed: {e}")
            return self._empty_response(start_date, end_date)
    
    def _format_for_dashboard(self, tune_data: Dict, start_date: str, end_date: str) -> Dict:
        """Format Tune data to match our dashboard API format"""
        
        # Extract data and totals
        campaigns = tune_data.get('data', [])
        totals = tune_data.get('totals', {})
        
        formatted_campaigns = []
        
        for campaign in campaigns:
            # Map Mike's offers to friendly names
            offer_name = campaign.get('Offer', {}).get('name', 'Unknown')
            
            # Extract stats
            impressions = int(campaign.get('Stat', {}).get('impressions', 0))
            clicks = int(campaign.get('Stat', {}).get('clicks', 0))
            conversions = int(campaign.get('Stat', {}).get('conversions', 0))
            payout = float(campaign.get('Stat', {}).get('payout', 0))
            
            # Calculate metrics
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            revenue = payout  # For affiliates, payout = revenue
            rpm = (revenue / impressions * 1000) if impressions > 0 else 0
            rpc = (revenue / clicks) if clicks > 0 else 0
            
            formatted_campaigns.append({
                'offer': offer_name,
                'partner': 'tune',  # Tune is the partner
                'campaign': 'tune_campaign',
                'creative': 'tune_creative', 
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'payout': payout,
                'cpm': 0.0,  # Calculate if needed
                'revenue': revenue,
                'rpm': round(rpm, 2),
                'rpc': round(rpc, 2),
                'profit': round(revenue - payout, 2) if revenue != payout else 0,
                'ctr': round(ctr, 2)
            })
        
        # Calculate summary from totals or aggregate campaigns
        total_impressions = totals.get('impressions', sum(c['impressions'] for c in formatted_campaigns))
        total_clicks = totals.get('clicks', sum(c['clicks'] for c in formatted_campaigns))
        total_revenue = totals.get('payout', sum(c['revenue'] for c in formatted_campaigns))
        
        return {
            'success': True,
            'period': f'{start_date} to {end_date}',
            'data': formatted_campaigns,
            'summary': {
                'total_campaigns': len(formatted_campaigns),
                'total_impressions': int(total_impressions),
                'total_clicks': int(total_clicks),
                'total_revenue': round(float(total_revenue), 2),
                'avg_ctr': round((total_clicks / total_impressions * 100) if total_impressions > 0 else 0, 2),
                'avg_rpm': round((total_revenue / total_impressions * 1000) if total_impressions > 0 else 0, 2),
                'avg_rpc': round((total_revenue / total_clicks) if total_clicks > 0 else 0, 2)
            }
        }
    
    def _empty_response(self, start_date: str, end_date: str) -> Dict:
        """Return empty response in dashboard format"""
        return {
            'success': False,
            'period': f'{start_date} to {end_date}',
            'data': [],
            'summary': {
                'total_campaigns': 0,
                'total_impressions': 0,
                'total_clicks': 0,
                'total_revenue': 0,
                'avg_ctr': 0,
                'avg_rpm': 0,
                'avg_rpc': 0
            }
        }
    
    def get_performance_metrics(self) -> Dict:
        """Get today's performance metrics from Tune"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_data = self.get_stats_report(start_date=today, end_date=today)
        
        if today_data['success']:
            summary = today_data['summary']
            best_campaign = {}
            
            # Find best performing campaign
            if today_data['data']:
                best_campaign = max(today_data['data'], key=lambda x: x['revenue'])
                best_campaign = {
                    'name': best_campaign['offer'],
                    'clicks': best_campaign['clicks'],
                    'impressions': best_campaign['impressions'],
                    'ctr': best_campaign['ctr']
                }
            
            return {
                'success': True,
                'today': {
                    'today_impressions': summary['total_impressions'],
                    'today_clicks': summary['total_clicks'],
                    'today_revenue': summary['total_revenue']
                },
                'best_campaign': best_campaign,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': False,
                'today': {
                    'today_impressions': 0,
                    'today_clicks': 0,
                    'today_revenue': 0
                },
                'best_campaign': {},
                'timestamp': datetime.now().isoformat()
            }

# Test the API client
if __name__ == "__main__":
    client = TuneAPIClient()
    
    print("🎯 Testing Tune API Client...")
    
    # Test stats report
    stats = client.get_stats_report()
    print(f"📊 Stats Report: {json.dumps(stats, indent=2)}")
    
    # Test performance metrics
    metrics = client.get_performance_metrics()
    print(f"📈 Performance Metrics: {json.dumps(metrics, indent=2)}")