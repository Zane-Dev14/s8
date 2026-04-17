#!/usr/bin/env python3
"""Test SSE streaming endpoint"""
import requests
import sys

url = "http://localhost:8000/api/stream/teach/test-concept-1?user_level=beginner"

print(f"Testing streaming endpoint: {url}")
print("=" * 60)

try:
    with requests.get(url, stream=True, timeout=10) as response:
        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        print("✅ Connection established, receiving stream...")
        print("-" * 60)
        
        count = 0
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                print(decoded)
                count += 1
                if count >= 20:  # Show first 20 events
                    print("\n... (stopping after 20 events)")
                    break
        
        print("-" * 60)
        print(f"✅ Received {count} events successfully!")
        
except requests.exceptions.Timeout:
    print("❌ Request timed out")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Made with Bob
