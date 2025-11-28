"""Quick test to check if GSMArena is accessible"""
import requests
import time

url = "https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=samsung s24"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print(f"Testing GSMArena search...")
print(f"URL: {url}")
print()

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS - GSMArena is accessible!")
        print(f"Response length: {len(response.text)} bytes")
    elif response.status_code == 429:
        print("❌ RATE LIMITED - Your IP is still blocked")
        print("Wait 10-15 minutes before trying again")
    elif response.status_code == 403:
        print("❌ FORBIDDEN - Bot detection active")
    else:
        print(f"⚠️  Unexpected status: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nWaiting 5 seconds before second test...")
time.sleep(5)

# Test phone detail page
url2 = "https://www.gsmarena.com/samsung_galaxy_s24-12771.php"
print(f"\nTesting phone detail page...")
print(f"URL: {url2}")

try:
    response = requests.get(url2, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS - Detail page accessible!")
        # Check for title
        if "Galaxy S24" in response.text:
            print("✅ Content looks correct!")
    elif response.status_code == 429:
        print("❌ RATE LIMITED")
    
except Exception as e:
    print(f"❌ Error: {e}")
