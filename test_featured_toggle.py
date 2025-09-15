import io
from fastapi.testclient import TestClient

from popup-system.api.main import app

client = TestClient(app)

def _percent_diff(a: bytes, b: bytes) -> float:
    from PIL import Image, ImageChops
    ia = Image.open(io.BytesIO(a)).convert('RGBA')
    ib = Image.open(io.BytesIO(b)).convert('RGBA')
    if ia.size != ib.size:
        return 100.0
    diff = ImageChops.difference(ia, ib)
    # Count non-zero pixels
    bbox = diff.getbbox()
    if not bbox:
        return 0.0
    # Rough estimate: proportion of bounding box area over full
    area_box = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    total = ia.size[0] * ia.size[1]
    return (area_box / total) * 100.0

def test_email_ad_png_600x400_visual_regression(tmp_path):
    # Generate current image
    r = client.get("/api/email/ad.png?property=mff&w=600&h=400&send=test-seed&debug=0")
    assert r.status_code == 200
    current = r.content

    # Load baseline if exists, else write it
    baseline_path = tmp_path / "baseline_600x400.png"
    if not baseline_path.exists():
        baseline_path.write_bytes(current)
        # First run establishes baseline
        return

    baseline = baseline_path.read_bytes()
    drift = _percent_diff(baseline, current)
    assert drift <= 0.5, f"Visual drift too high: {drift:.3f}%"

def test_email_ad_png_300x250_visual_regression(tmp_path):
    r = client.get("/api/email/ad.png?property=mff&w=300&h=250&send=test-seed&debug=0")
    assert r.status_code == 200
    current = r.content
    baseline_path = tmp_path / "baseline_300x250.png"
    if not baseline_path.exists():
        baseline_path.write_bytes(current)
        return
    baseline = baseline_path.read_bytes()
    drift = _percent_diff(baseline, current)
    assert drift <= 0.5, f"Visual drift too high: {drift:.3f}%"

 