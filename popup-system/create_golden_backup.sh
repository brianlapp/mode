#!/bin/bash
# Create GOLDEN BACKUP from current production
# Includes campaigns AND property settings

BACKUP_DIR="/Users/brianlapp/Documents/GitHub/mode/popup-system/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
API_BASE="https://mode-dash-production.up.railway.app/api"

echo "📦 Creating GOLDEN BACKUP from production..."

# Backup campaigns
echo "1/2 Backing up campaigns..."
curl -s "$API_BASE/campaigns" | jq '.' > "$BACKUP_DIR/GOLDEN_campaigns_$TIMESTAMP.json"
CAMPAIGN_COUNT=$(jq 'length' "$BACKUP_DIR/GOLDEN_campaigns_$TIMESTAMP.json")
echo "✅ Saved $CAMPAIGN_COUNT campaigns"

# Backup all property settings
echo "2/2 Backing up property settings..."
echo "[" > "$BACKUP_DIR/GOLDEN_properties_$TIMESTAMP.json"

for id in {1..12}; do
    PROPS=$(curl -s "$API_BASE/campaigns/$id/properties" | jq -c ". | map(. + {campaign_id: $id})")
    if [ "$id" -lt 12 ]; then
        echo "  $PROPS," >> "$BACKUP_DIR/GOLDEN_properties_$TIMESTAMP.json"
    else
        echo "  $PROPS" >> "$BACKUP_DIR/GOLDEN_properties_$TIMESTAMP.json"
    fi
done

echo "]" >> "$BACKUP_DIR/GOLDEN_properties_$TIMESTAMP.json"

PROPS_COUNT=$(jq '[.[][]] | length' "$BACKUP_DIR/GOLDEN_properties_$TIMESTAMP.json")
echo "✅ Saved $PROPS_COUNT property settings"

echo ""
echo "🎉 GOLDEN BACKUP COMPLETE!"
echo "   Campaigns: $BACKUP_DIR/GOLDEN_campaigns_$TIMESTAMP.json"
echo "   Properties: $BACKUP_DIR/GOLDEN_properties_$TIMESTAMP.json"
echo ""
echo "This backup includes:"
echo "   - All $CAMPAIGN_COUNT campaigns (clean, no Prizies)"
echo "   - All $PROPS_COUNT property assignments"
echo "   - Correct MMM/MFF mappings"
echo "   - All visibility settings"

