"""
Property Data Management
Handles loading and managing property data from JSON files
"""

import json
from pathlib import Path

def load_project_data():
    """Load project data from memory bank JSON files"""
    try:
        with open("memory-bank/project-memories-corrected.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        try:
            with open("memory-bank/project-memories.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            # Return default structure if no files found
            data = {"properties": {}}
    
    return data

def get_properties_data():
    """Get properties data from loaded project data"""
    data = load_project_data()
    return data.get('properties', {})

def get_property_data(property_key):
    """Get data for a specific property"""
    properties = get_properties_data()
    return properties.get(property_key, {})

# Property data constants
PROPERTY_URLS = {
    "mff": "https://modefreefinds.com/",
    "mmm": "https://modemarketmunchies.com/",
    "mmd": "https://modemobiledaily.com/",
    "mcad": "https://modeclassactionsdaily.com/"
}

PROPERTY_LOGOS = {
    "mff": "https://i0.wp.com/modefreefinds.com/wp-content/uploads/2024/11/FreeFinds-Large.png?fit=1171%2C355&ssl=1",
    "mmm": "https://modemarketmunchies.com/wp-content/uploads/2025/04/market-munchies-logo-1.webp",
    "mmd": "https://modemobiledaily.com/wp-content/uploads/2025/06/cropped-Daily-2a.png",
    "mcad": "https://modeclassactionsdaily.com/wp-content/uploads/2025/04/class-actions-logo.png"
}

PROPERTY_SCREENSHOTS = {
    "mff": {
        "landing": "https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-0a7816aa-1b1a-4781-ac06-385c92c7d392.png",
        "thankyou": "https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-bf2ee1ba-8bed-4078-96d4-b4c1c43992ba.png"
    },
    "mmm": {
        "landing": "https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-7c9f0495-1873-43d5-b051-e6b193b2254e.png"
    },
    "mmd": {
        "landing": "https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-84e981c0-206b-4370-83a1-f2b2e5540d90.png"
    },
    "mcad": {
        "landing": "https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-f7d2b138-0af0-4778-ab6e-b208a2cd45f1.png"
    }
} 