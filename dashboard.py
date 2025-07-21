#!/usr/bin/env python3
"""
Mode Optimization Dashboard
Simple terminal-based status view for quick project overview
"""

import json
import os
from datetime import datetime
from pathlib import Path

class ModeOptimizationDashboard:
    def __init__(self):
        self.memory_file = "memory-bank/project-memories.json"
        self.load_project_data()
    
    def load_project_data(self):
        """Load project data from memory bank"""
        try:
            with open(self.memory_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("⚠️  Memory bank not found. Run from project root directory.")
            self.data = {}
    
    def show_header(self):
        """Display dashboard header"""
        print("\n" + "="*60)
        print("🚀 MODE OPTIMIZATION DASHBOARD")
        print("="*60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def show_property_status(self):
        """Display status of all properties"""
        print("🏢 PROPERTY STATUS")
        print("-" * 40)
        
        if 'properties' not in self.data:
            print("No property data found.")
            return
            
        properties = self.data['properties']
        
        # MFF Status
        mff = properties.get('mode_free_finds', {})
        print(f"📈 ModeFreeFinds.com")
        print(f"   CPL: {mff.get('meta_cpl', 'N/A')} ✅")
        print(f"   Revenue: {mff.get('monthly_revenue', 'N/A')}")
        print(f"   Status: {mff.get('status', 'Unknown')}")
        print()
        
        # MMM Status  
        mmm = properties.get('mode_market_munchies', {})
        print(f"📊 ModeMarketMunchies.com")
        print(f"   CPL: {mmm.get('meta_cpl', 'N/A')} ⚠️")
        print(f"   Target: {mmm.get('target_cpl', 'N/A')}")
        print(f"   Status: {mmm.get('status', 'Unknown')}")
        print()
        
        # MCAD Status
        mcad = properties.get('mode_class_actions', {})
        print(f"⚖️  ModeClassActionsDaily.com")
        print(f"   Status: {mcad.get('status', 'Unknown')} 🔨")
        print()
        
        # MMD Status  
        mmd = properties.get('mode_mobile_daily', {})
        print(f"📱 ModeMobileDaily.com")
        print(f"   Status: {mmd.get('status', 'Unknown')} 🔨")
        print()
    
    def show_priorities(self):
        """Display immediate priorities"""
        print("🎯 IMMEDIATE PRIORITIES")
        print("-" * 40)
        
        if 'immediate_priorities' not in self.data:
            print("No priorities data found.")
            return
            
        for priority in self.data['immediate_priorities']:
            priority_num = priority.get('priority', '?')
            task = priority.get('task', 'Unknown task')
            timeline = priority.get('timeline', 'No timeline')
            impact = priority.get('impact', 'Unknown impact')
            
            print(f"{priority_num}. {task}")
            print(f"   ⏰ {timeline}")
            print(f"   💰 {impact}")
            print()
    
    def show_daily_checklist(self):
        """Display daily optimization checklist"""
        print("✅ TODAY'S OPTIMIZATION CHECKLIST")
        print("-" * 40)
        print("[ ] Check MMM CPL performance")
        print("[ ] Review MFF conversion metrics")
        print("[ ] Update daily log with discoveries")
        print("[ ] Log any code snippets created")
        print("[ ] Validate attribution tracking")
        print("[ ] Document optimization wins")
        print()
    
    def show_quick_stats(self):
        """Display quick stats summary"""
        print("📊 QUICK STATS")
        print("-" * 40)
        print("Total Email Subscribers: 3.4M+")
        print("Properties Under Management: 4")
        print("Monthly Revenue (MFF): ~$40k")
        print("Target CPL: $0.45")
        print("Current Focus: MMM CPL Optimization")
        print()
    
    def show_memory_bank_status(self):
        """Show memory bank file status"""
        print("🧠 MEMORY BANK STATUS")
        print("-" * 40)
        
        # Check for daily logs
        daily_logs_dir = Path("memory-bank/daily-logs")
        if daily_logs_dir.exists():
            log_files = list(daily_logs_dir.glob("*.md"))
            print(f"Daily Logs: {len(log_files)} files")
        else:
            print("Daily Logs: Directory not found")
        
        # Check for optimization wins
        wins_dir = Path("memory-bank/optimization-wins")
        if wins_dir.exists():
            win_files = list(wins_dir.glob("*"))
            print(f"Optimization Wins: {len(win_files)} files")
        else:
            print("Optimization Wins: Directory not found")
            
        print()
    
    def run(self):
        """Run the dashboard display"""
        self.show_header()
        self.show_property_status()
        self.show_priorities()
        self.show_daily_checklist()
        self.show_quick_stats()
        self.show_memory_bank_status()
        
        print("💡 QUICK COMMANDS:")
        print("   python dashboard.py              - Show this dashboard")
        print("   code memory-bank/daily-logs/     - Open daily logs")
        print("   code memory-bank/project-memories.json - Edit memory bank")
        print()

def main():
    dashboard = ModeOptimizationDashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 