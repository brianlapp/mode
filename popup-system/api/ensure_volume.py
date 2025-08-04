#!/usr/bin/env python3
"""
🛡️ RAILWAY VOLUME INSURANCE SCRIPT
Ensure volume mount directory exists and is writable
Based on Railway community solutions
"""

import os
import sys

def ensure_railway_volume():
    """Ensure Railway volume mount exists and is writable"""
    
    # Railway volume mount path from railway.toml
    volume_path = "/app/popup-system/api/data"
    
    print(f"🔍 Checking Railway volume mount: {volume_path}")
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(volume_path, exist_ok=True)
        print(f"✅ Volume directory ensured: {volume_path}")
    except Exception as e:
        print(f"❌ Failed to create volume directory: {e}")
        return False
    
    # Test write permissions
    try:
        test_file = os.path.join(volume_path, "railway_volume_test.tmp")
        with open(test_file, 'w') as f:
            f.write("Railway volume write test")
        
        # Read it back
        with open(test_file, 'r') as f:
            content = f.read()
            
        # Clean up
        os.remove(test_file)
        
        if "Railway volume write test" in content:
            print(f"✅ Volume is writable: {volume_path}")
            return True
        else:
            print(f"❌ Volume write test failed: {volume_path}")
            return False
            
    except Exception as e:
        print(f"❌ Volume write test failed: {e}")
        return False

if __name__ == "__main__":
    success = ensure_railway_volume()
    if not success:
        print("🚨 VOLUME MOUNT FAILED - DATABASE WILL NOT PERSIST!")
        sys.exit(1)
    else:
        print("🎉 Volume mount ready for persistent data!")