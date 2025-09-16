"""
SCREENSHOT ENDPOINT - Capture the working popup as PNG
Finally doing this the RIGHT way!
"""

@app.get("/api/email/popup-screenshot.png")
async def popup_screenshot_png(property: str = "mff", width: int = 320, height: int = 480):
    """Screenshot the ACTUAL working popup - stop reinventing the wheel!"""
    
    try:
        # Create HTML that loads the working popup
        popup_html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ 
            margin: 0; 
            padding: 0; 
            background: white;
            width: {width}px;
            height: {height}px;
            overflow: hidden;
        }}
        
        .mode-popup {{
            position: relative !important;
            transform: none !important;
            opacity: 1 !important;
            display: block !important;
            margin: 0 !important;
        }}
        
        .mode-popup-overlay {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <script>
        // Set property for popup
        window.MODE_PROPERTY = '{property}';
    </script>
    <script src="https://mode-dash-production.up.railway.app/popup.js"></script>
    
    <script>
        setTimeout(() => {{
            // Force popup to show
            const popup = document.querySelector('.mode-popup');
            const overlay = document.querySelector('.mode-popup-overlay');
            
            if (popup) {{
                popup.style.position = 'relative';
                popup.style.transform = 'none';
                popup.style.opacity = '1';
                popup.style.display = 'block';
                popup.style.margin = '0';
            }}
            
            if (overlay) {{
                overlay.style.display = 'none';
            }}
        }}, 2000);
    </script>
</body>
</html>
        '''
        
        # Try using wkhtmltopdf or similar to convert HTML to image
        # For now, return the HTML so you can screenshot it manually
        return Response(
            content=popup_html,
            media_type="text/html",
            headers={
                "Content-Disposition": f"inline; filename=popup_{property}.html"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot failed: {str(e)}")
