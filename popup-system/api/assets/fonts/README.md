# Font Assets

## DejaVu Fonts

This directory contains DejaVu fonts, which are open source fonts based on the Vera fonts.

**License:** DejaVu fonts are released under a Free license.
- **Source:** https://github.com/dejavu-fonts/dejavu-fonts
- **Version:** 2.37
- **License:** https://github.com/dejavu-fonts/dejavu-fonts/blob/master/LICENSE

## Font Usage

The fonts are used by the email ad generation system to ensure consistent, professional typography across all generated images.

### Available Fonts:
- `DejaVuSans.ttf` - Regular weight
- `DejaVuSans-Bold.ttf` - Bold weight  
- `DejaVuSans-Oblique.ttf` - Italic weight
- `DejaVuSans-BoldOblique.ttf` - Bold italic weight
- Additional condensed and mono variants

### Font Loading Priority:
1. Bundled DejaVu fonts (primary)
2. System fonts (fallback)
3. PIL default font (emergency fallback)

This ensures the "FONTS MISSING" error is eliminated on Railway deployments.
