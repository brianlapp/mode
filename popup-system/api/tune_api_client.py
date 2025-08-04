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
import calendar

class TuneAPIClient:
    def __init__(self, api_key: str = "NETfeRuo7FOO72yOcwOXj5jK0aCYve"):
        self.api_key = api_key
        self.base_url = "https://api.modemobile.com"  # Mike's Tune network
        
    @staticmethod
    def get_date_range(preset: str = "last_7_days") -> tuple:
        """Get start and end dates for common presets"""
        today = datetime.now()
        
        if preset == "today":
            return (today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        
        elif preset == "yesterday":
            yesterday = today - timedelta(days=1)
            return (yesterday.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d'))
        
        elif preset == "last_7_days":
            start = today - timedelta(days=7)
            return (start.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        
        elif preset == "last_30_days":
            start = today - timedelta(days=30)
            return (start.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        
        elif preset == "this_month":
            start = today.replace(day=1)
            return (start.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        
        elif preset == "last_month":
            first_this_month = today.replace(day=1)
            last_month_end = first_this_month - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            return (last_month_start.strftime('%Y-%m-%d'), last_month_end.strftime('%Y-%m-%d'))
        
        else:
            # Default to last 7 days
            start = today - timedelta(days=7)
            return (start.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        
    def get_stats_report(self, 
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        preset: Optional[str] = None,
                        affiliate_id: int = 43045) -> Dict:
        """
        Get Mike's real analytics data from Tune
        Returns data matching the dashboard format exactly
        """
        
        # Handle date presets or defaults
        if preset:
            start_date, end_date = self.get_date_range(preset)
        elif not start_date or not end_date:
            # Default to last 7 days (Mike's preference)
            start_date, end_date = self.get_date_range("last_7_days")
            
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
            # Extract data exactly like Mike's Tune dashboard
            offer_name = campaign.get('Offer', {}).get('name', 'Unknown Offer')
            
            # Extract stats (handle different Tune API response formats)
            stats = campaign.get('Stat', {})
            impressions = int(stats.get('impressions', 0))
            clicks = int(stats.get('clicks', 0))
            conversions = int(stats.get('conversions', 0))
            payout = float(stats.get('payout', 0))
            
            # Map Mike's offer names to proper partners/properties
            partner_mapping = {
                'Trading Tips': 'MMM',
                'Behind The Markets': 'MFF', 
                'Brownstone': 'MCAD',
                'Hotsheets': 'MMD',
                'Best Gold': 'MFF'
            }
            partner = partner_mapping.get(offer_name, 'Mode')
            
            # Calculate metrics exactly like Tune
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            revenue = payout  # For affiliate view, payout = revenue
            rpm = (revenue / impressions * 1000) if impressions > 0 else 0
            rpc = (revenue / clicks) if clicks > 0 else 0
            cpm = (payout / impressions * 1000) if impressions > 0 else 0
            
            # Match Mike's screenshot columns exactly
            formatted_campaigns.append({
                'offer': offer_name,
                'partner': partner,
                'campaign': f"{offer_name.replace(' ', '')}_Banner",  # Creative filename style
                'creative': f"{offer_name.replace(' ', '')}_Creative.png",  # Image filename
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'payout': round(payout, 2),
                'cpm': round(cpm, 2),
                'revenue': round(revenue, 2),
                'rpm': round(rpm, 2),
                'rpc': round(rpc, 2),
                'profit': round(revenue - payout, 2) if revenue != payout else round(revenue * 0.1, 2),  # Assume 10% margin
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