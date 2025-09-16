#!/usr/bin/env python3
"""
SCREENSHOT THE WORKING POPUP - Stop reinventing the wheel!
"""

import subprocess
import time
import os

def capture_working_popup():
    """Use browser automation to capture the actual working popup"""
    
    # Create a simple test page that loads the working popup
    html_content = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Working Popup Test</title>
    <style>
        body { margin: 0; padding: 20px; background: white; }
        .test-container { 
            width: 320px; 
            height: 480px; 
            margin: 0 auto; 
            position: relative;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="test-container" id="popup-target">
        <p>Loading popup...</p>
    </div>
    
    <!-- Load the working popup script -->
    <script src="https://mode-dash-production.up.railway.app/popup.js"></script>
    
    <script>
        // Wait for script to load, then force popup to show
        setTimeout(() => {
            // Try to trigger the popup
            const event = new CustomEvent('modePopupTrigger', {
                detail: { property: 'mff' }
            });
            document.dispatchEvent(event);
            
            // Alternative - check for popup functions
            if (typeof window.initModePopup === 'function') {
                window.initModePopup();
            }
            
            // Force show any hidden popups
            setTimeout(() => {
                const popups = document.querySelectorAll('.mode-popup, [class*="popup"], [id*="popup"]');
                popups.forEach(popup => {
                    popup.style.display = 'block';
                    popup.style.opacity = '1';
                    popup.style.position = 'relative';
                    popup.style.transform = 'none';
                });
                
                // Hide overlays
                const overlays = document.querySelectorAll('.mode-popup-overlay, [class*="overlay"]');
                overlays.forEach(overlay => {
                    overlay.style.display = 'none';
                });
            }, 2000);
        }, 1000);
    </script>
</body>
</html>
    '''
    
    # Write test file
    with open('popup_test.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Created popup_test.html")
    print("🌐 Open this file in your browser:")
    print(f"file://{os.path.abspath('popup_test.html')}")
    print("\n📸 Then use browser dev tools to screenshot the popup!")
    print("Or use browser screenshot extension to capture just the popup area")

if __name__ == "__main__":
    capture_working_popup()
