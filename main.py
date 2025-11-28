"""
Universal Mobile Scraper - Main Demo
Scrapes mobile phone data from GSMArena, 91mobiles, and Kimovil without proxies.
"""

import json
import os
from function.scrapers.gsmarena import GSMArenaScraper
from function.scrapers.mobiles91 import Mobiles91Scraper
from function.scrapers.kimovil import KimovilScraper


def save_to_json(phones, filename):
    """Save scraped phone data to JSON file."""
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump([phone.to_dict() for phone in phones], f, indent=2, ensure_ascii=False)
    
    print(f"[SAVED] Saved {len(phones)} phones to {filepath}")


def demo_gsmarena():
    """Demo GSMArena scraping."""
    print("\n" + "="*60)
    print("[WEB] GSMArena Scraper Demo")
    print("="*60 + "\n")
    
    scraper = GSMArenaScraper()
    
    # Example: Search for Samsung Galaxy S23
    phones = scraper.search_phones("Samsung Galaxy S23", max_results=3)
    
    if phones:
        save_to_json(phones, 'gsmarena_results.json')
        print(f"\n[INFO] Sample phone: {phones[0]}")


def demo_91mobiles():
    """Demo 91mobiles scraping."""
    print("\n" + "="*60)
    print("[WEB] 91mobiles Scraper Demo")
    print("="*60 + "\n")
    
    print("[WARNING]  Note: 91mobiles has bot detection. Success rate may vary.")
    print("    Try using direct product URLs instead of search.\n")
    
    scraper = Mobiles91Scraper()
    
    # Example: Search for iPhone 15
    phones = scraper.search_phones("iPhone 15", max_results=3)
    
    if phones:
        save_to_json(phones, '91mobiles_results.json')
        print(f"\n[INFO] Sample phone: {phones[0]}")
    else:
        print("\n[WARNING]  No results. 91mobiles may be blocking automated requests.")
        print("    See ANTI_BOT_NOTES.md for workarounds.")


def demo_kimovil():
    """Demo Kimovil scraping."""
    print("\n" + "="*60)
    print("[WEB] Kimovil Scraper Demo")
    print("="*60 + "\n")
    
    print("[WARNING]  Note: Kimovil uses Cloudflare protection.")
    print("    This scraper may be blocked. See ANTI_BOT_NOTES.md for solutions.\n")
    
    scraper = KimovilScraper()
    
    # Example: Search for OnePlus 12
    phones = scraper.search_phones("OnePlus 12", max_results=3)
    
    if phones:
        save_to_json(phones, 'kimovil_results.json')
        print(f"\n[INFO] Sample phone: {phones[0]}")
    else:
        print("\n[WARNING]  No results. Kimovil is blocking automated requests (Cloudflare).")
        print("    Consider using Selenium or see ANTI_BOT_NOTES.md for alternatives.")


def demo_specific_urls():
    """Demo scraping specific phone URLs."""
    print("\n" + "="*60)
    print("[*] Scraping Specific URLs")
    print("="*60 + "\n")
    
    # GSMArena example
    gsmarena = GSMArenaScraper()
    phone1 = gsmarena.scrape_phone("https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php")
    if phone1:
        print(f"[SUCCESS] {phone1}")
    
    # 91mobiles example (you'll need to update with actual URL)
    # mobiles91 = Mobiles91Scraper()
    # phone2 = mobiles91.scrape_phone("https://www.91mobiles.com/...")
    
    # Kimovil example (you'll need to update with actual URL)
    # kimovil = KimovilScraper()
    # phone3 = kimovil.scrape_phone("https://www.kimovil.com/...")


def main():
    """Main function - run all demos."""
    print("""
============================================================
         Universal Mobile Scraper                               
         GSMArena | 91mobiles | Kimovil                        
                                                                
         [*] No Proxies Required!                                
         Uses realistic browser headers to avoid blocking      
============================================================

[WARNING]  IMPORTANT: Some sites use Cloudflare/bot detection
   - GSMArena: [*] Working well
   - 91mobiles: [WARNING] May be blocked (try direct URLs)
   - Kimovil: [WARNING] Often blocked (Cloudflare protection)
   
   See ANTI_BOT_NOTES.md for solutions and workarounds.
    """)
    
    # Run demos
    try:
        demo_gsmarena()
    except Exception as e:
        print(f"[FAILED] GSMArena demo failed: {e}")
    
    try:
        demo_91mobiles()
    except Exception as e:
        print(f"[FAILED] 91mobiles demo failed: {e}")
    
    try:
        demo_kimovil()
    except Exception as e:
        print(f"[FAILED] Kimovil demo failed: {e}")
    
    print("\n" + "="*60)
    print("[SUCCESS] Demo completed!")
    print("="*60)
    print("\n[TIP] Tips:")
    print("   • GSMArena works best - comprehensive phone specs")
    print("   • For blocked sites, try direct product URLs")
    print("   • See ANTI_BOT_NOTES.md for Selenium/proxy solutions")
    print("   • Check 'data' folder for any successful results\n")


if __name__ == "__main__":
    main()
