#!/bin/bash
# EMERGENCY ROLLBACK for utm_source implementation
# Run this if the site breaks after implementing utm_source

echo "🚨 ROLLING BACK utm_source changes..."

cd /Users/brianlapp/Documents/GitHub/mode

# Revert to last working commit
git revert HEAD --no-edit

# Push rollback
git push

echo "⏳ Waiting 60 seconds for Railway deployment..."
sleep 60

# Restore campaigns (they always get wiped)
curl -X POST -s "https://mode-dash-production.up.railway.app/api/db/force-init" > /dev/null
sleep 3
curl -X POST -s "https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns"

sleep 3

# Test
echo ""
echo "🧪 Testing rollback..."
CAMPAIGNS=$(curl -s "https://mode-dash-production.up.railway.app/api/campaigns" | jq 'length')
POPUP=$(curl -s "https://mode-dash-production.up.railway.app/api/campaigns/mff" | jq 'length')

echo "Admin campaigns: $CAMPAIGNS"
echo "Popup campaigns: $POPUP"

if [ "$CAMPAIGNS" == "12" ] && [ "$POPUP" == "6" ]; then
    echo "✅ ROLLBACK SUCCESSFUL - Site is working again!"
else
    echo "❌ ROLLBACK FAILED - May need manual intervention"
fi

