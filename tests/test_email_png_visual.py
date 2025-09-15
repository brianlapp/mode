import io
from fastapi.testclient import TestClient
from pathlib import Path

from popup-system.api.main import app

client = TestClient(app)

def _percent_diff_bytes(a: bytes, b: bytes) -> float:
    from PIL import Image, ImageChops
    ia = Image.open(io.BytesIO(a)).convert('RGBA')
    ib = Image.open(io.BytesIO(b)).convert('RGBA')
    if ia.size != ib.size:
        return 100.0
    diff = ImageChops.difference(ia, ib)
    # Count all non-zero pixels
    bbox = diff.getbbox()
    if not bbox:
        return 0.0
    # Approximate ratio by area of bbox (conservative upper bound)
    area_box = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    total = ia.size[0] * ia.size[1]
    return (area_box / total) * 100.0

def _baselines_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "tests" / "baselines"

def test_visual_600x400_baseline(tmp_path):
    r = client.get("/api/email/ad.png?property=mff&w=600&h=400&send=visual-seed-600")
    assert r.status_code == 200
    current = r.content
    baseline_dir = _baselines_dir()
    baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = baseline_dir / "email_ad_600x400.png"
    if not baseline_path.exists():
        baseline_path.write_bytes(current)
        return
    drift = _percent_diff_bytes(baseline_path.read_bytes(), current)
    assert drift <= 0.5, f"600x400 drift {drift:.3f}% exceeds 0.5%"

def test_visual_300x250_baseline(tmp_path):
    r = client.get("/api/email/ad.png?property=mff&w=300&h=250&send=visual-seed-300")
    assert r.status_code == 200
    current = r.content
    baseline_dir = _baselines_dir()
    baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = baseline_dir / "email_ad_300x250.png"
    if not baseline_path.exists():
        baseline_path.write_bytes(current)
        return
    drift = _percent_diff_bytes(baseline_path.read_bytes(), current)
    assert drift <= 0.5, f"300x250 drift {drift:.3f}% exceeds 0.5%"


