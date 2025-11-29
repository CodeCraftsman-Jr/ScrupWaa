"""Test what content is being flagged as bot detection"""
from playwright.sync_api import sync_playwright

url = "https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=Samsung+S24"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
    print(f"Loading: {url}")
    response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
    
    # Don't wait for networkidle, just give it a moment
    page.wait_for_timeout(3000)
    
    content = page.content()
    
    print(f"\nStatus: {response.status}")
    print(f"Content length: {len(content)}")
    print(f"\nFirst 2000 chars:")
    print(content[:2000])
    
    # Save full content
    with open('test_page.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n✅ Saved to test_page.html")
    
    browser.close()
