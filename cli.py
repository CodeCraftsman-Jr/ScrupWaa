#!/usr/bin/env python3
"""
Universal Mobile Phone Scraper - Command Line Interface
A comprehensive CLI for searching mobile phones across multiple websites.
"""

import argparse
import sys
import json
from pathlib import Path
from universal_search import UniversalSearch
from format_results import format_detailed_results, print_detailed_phone, save_detailed_results
from models.phone import Phone


def create_parser():
    """Create argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Universal Mobile Phone Scraper - Search phones across GSMArena, 91mobiles, and Kimovil",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Samsung Galaxy S24"                    # Basic search
  %(prog)s "iPhone 15" --detailed                  # Detailed search with full specs
  %(prog)s "OnePlus" --sites gsmarena 91mobiles    # Search specific sites
  %(prog)s "Xiaomi" --max-results 10 --output json # Limit results and save to JSON
  %(prog)s "Google Pixel" --compare                # Compare phones side by side
        """
    )

    parser.add_argument(
        'query',
        nargs='*',
        help='Search query for mobile phones'
    )

    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Get detailed specifications, offers, and images'
    )

    parser.add_argument(
        '-s', '--sites',
        nargs='+',
        choices=['gsmarena', '91mobiles', 'kimovil'],
        default=['gsmarena', '91mobiles', 'kimovil'],
        help='Specify which sites to search (default: all)'
    )

    parser.add_argument(
        '-m', '--max-results',
        type=int,
        default=5,
        help='Maximum results per site (default: 5)'
    )

    parser.add_argument(
        '-o', '--output',
        choices=['console', 'json', 'both'],
        default='console',
        help='Output format (default: console)'
    )

    parser.add_argument(
        '-f', '--output-file',
        type=str,
        help='Output file path (default: auto-generated)'
    )

    parser.add_argument(
        '-c', '--compare',
        action='store_true',
        help='Compare phones side by side'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--list-sites',
        action='store_true',
        help='List available search sites'
    )

    return parser


def list_sites():
    """List available search sites."""
    print("Available search sites:")
    print("  • gsmarena   - GSMArena.com (most comprehensive specs)")
    print("  • 91mobiles  - 91mobiles.com (Indian market focus)")
    print("  • kimovil    - Kimovil.com (global coverage)")
    print("\nUsage: python cli.py 'Samsung' --sites gsmarena 91mobiles")


def search_phones(query, sites, max_results, detailed=False, verbose=False):
    """Perform phone search across specified sites."""
    if verbose:
        print(f"🔍 Searching for: {query}")
        print(f"📍 Sites: {', '.join(sites)}")
        print(f"📊 Max results per site: {max_results}")
        print(f"📋 Detailed mode: {detailed}")
        print("-" * 50)

    searcher = UniversalSearch()

    # Map site names to scraper classes
    site_mapping = {
        'gsmarena': 'gsmarena',
        '91mobiles': '91mobiles',
        'kimovil': 'kimovil'
    }

    # Filter sites
    enabled_sites = [site_mapping[site] for site in sites if site in site_mapping]

    search_results = searcher.search_all(query, max_results_per_site=max_results, sites=enabled_sites)
    
    # Extract phones from the search results structure for basic display
    results = {}
    for site_name, site_data in search_results['scrapers'].items():
        if site_data['status'] == 'success':
            # Convert dict phones back to Phone objects for compatibility
            phones = []
            for phone_dict in site_data['phones']:
                phone = Phone(
                    brand=phone_dict.get('brand', ''),
                    model=phone_dict.get('model', ''),
                    url=phone_dict.get('url', ''),
                    price=phone_dict.get('price'),
                    original_price=phone_dict.get('original_price'),
                    currency=phone_dict.get('currency', 'USD'),
                    discounted=phone_dict.get('discounted', False),
                    in_stock=phone_dict.get('in_stock', True),
                    specs=phone_dict.get('specs', {}),
                    detailed_specs=phone_dict.get('detailed_specs', []),
                    images=phone_dict.get('images', []),
                    all_images=phone_dict.get('all_images', []),
                    thumbnail=phone_dict.get('thumbnail'),
                    rating=phone_dict.get('rating'),
                    reviews_count=phone_dict.get('reviews_count'),
                    highlights=phone_dict.get('highlights', []),
                    description=phone_dict.get('description'),
                    seller_name=phone_dict.get('seller_name'),
                    seller_rating=phone_dict.get('seller_rating'),
                    f_assured=phone_dict.get('f_assured', False),
                    offers=phone_dict.get('offers', []),
                    bank_offers=phone_dict.get('bank_offers', []),
                    exchange_offers=phone_dict.get('exchange_offers', []),
                    launch_year=phone_dict.get('launch_year'),
                    launch_date=phone_dict.get('launch_date'),
                    dimensions=phone_dict.get('dimensions', {}),
                    weight=phone_dict.get('weight'),
                    colors=phone_dict.get('colors', []),
                    variants=phone_dict.get('variants', []),
                    warranty=phone_dict.get('warranty'),
                    warranty_summary=phone_dict.get('warranty_summary'),
                    service_type=phone_dict.get('service_type'),
                    source=phone_dict.get('source', ''),
                    total_results=phone_dict.get('total_results'),
                    query_params=phone_dict.get('query_params', {})
                )
                phones.append(phone)
            results[site_name] = phones
        else:
            results[site_name] = []

    if verbose:
        total_results = sum(len(site_results) for site_results in results.values())
        print(f"✅ Found {total_results} phones across {len(results)} sites")

    return results, search_results


def display_results(results, raw_results, detailed=False, compare=False):
    """Display search results."""
    if not results:
        print("❌ No results found.")
        return

    total_results = sum(len(site_results) for site_results in results.values())

    if not detailed and not compare:
        # Simple list view
        print(f"\n📱 Found {total_results} phones:\n")

        for site, phones in results.items():
            if phones:
                print(f"🔸 {site.upper()}:")
                for i, phone in enumerate(phones, 1):
                    print(f"  {i}. {phone.brand} {phone.model}")
                    if phone.price:
                        print(f"     Price: {phone.price}")
                    if phone.rating:
                        print(f"     Rating: {phone.rating}/10")
                    print()

    elif detailed:
        # Detailed view - convert to Flipkart format first
        print(f"\n📋 Detailed Results ({total_results} phones):\n")

        # Convert results to Flipkart format for detailed display
        detailed_formatted = format_detailed_results(raw_results)

        if detailed_formatted.get('result'):
            for phone_data in detailed_formatted['result']:
                print_detailed_phone(phone_data)
        else:
            print("❌ No detailed results available.")

    elif compare:
        # Comparison view
        all_phones = []
        for phones in results.values():
            all_phones.extend(phones)

        if len(all_phones) < 2:
            print("❌ Need at least 2 phones to compare. Found only", len(all_phones))
            return

        print(f"\n⚖️  Comparing {len(all_phones)} phones:\n")

        # Compare basic specs
        print("📊 BASIC COMPARISON:")
        print("-" * 100)
        print("<15")
        print("-" * 100)

        for phone in all_phones:
            name = f"{phone.brand} {phone.model}"
            name = name[:25] + "..." if len(name) > 25 else name
            price = phone.price or "N/A"
            rating = f"{phone.rating}/10" if phone.rating else "N/A"
            print("<15")

        print()

        # Compare key specs if available
        if any(phone.specs for phone in all_phones):
            print("🔧 KEY SPECIFICATIONS:")
            print("-" * 100)

            specs_to_compare = ['Display', 'Platform', 'Memory', 'Main Camera', 'Battery']

            for spec_category in specs_to_compare:
                print(f"\n{spec_category}:")
                for phone in all_phones:
                    name = f"{phone.brand} {phone.model}"
                    name = name[:20] + "..." if len(name) > 20 else name
                    spec_value = "N/A"

                    if phone.specs and spec_category in phone.specs:
                        spec_data = phone.specs[spec_category]
                        if isinstance(spec_data, dict):
                            # Get first meaningful spec
                            for key, value in spec_data.items():
                                if value and str(value).lower() not in ['n/a', 'none', '']:
                                    spec_value = f"{key}: {value}"
                                    break
                        elif isinstance(spec_data, str):
                            spec_value = spec_data

                    print("<20")


def save_results(results, output_file=None, detailed=False):
    """Save results to file."""
    if not results:
        return

    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    if not output_file:
        timestamp = UniversalSearch._get_timestamp()
        query_part = "_".join(sys.argv[1:3]) if len(sys.argv) > 1 else "search"
        query_part = query_part.replace(" ", "_").replace("-", "_")[:20]
        output_file = f"data/cli_{query_part}_{timestamp}.json"

    if detailed:
        formatted_results = format_detailed_results(results)
        save_detailed_results(formatted_results, output_file)
    else:
        # Save raw results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"💾 Results saved to: {output_file}")


def interactive_mode():
    """Run CLI in interactive mode."""
    print("🚀 Universal Mobile Phone Scraper - Interactive Mode")
    print("=" * 55)

    while True:
        try:
            query = input("\n🔍 What phone are you looking for? (or 'quit' to exit): ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not query:
                continue

            # Get search options
            detailed = input("📋 Detailed search? (y/n) [n]: ").strip().lower() == 'y'
            max_results = input("📊 Max results per site? [5]: ").strip()
            max_results = int(max_results) if max_results.isdigit() else 5

            sites_input = input("📍 Sites (gsmarena,91mobiles,kimovil) [all]: ").strip()
            if sites_input:
                sites = [s.strip() for s in sites_input.split(',')]
            else:
                sites = ['gsmarena', '91mobiles', 'kimovil']

            # Perform search
            results = search_phones(query, sites, max_results, detailed, verbose=True)

            # Display results
            display_results(results, detailed=detailed)

            # Ask to save
            save = input("\n💾 Save results to file? (y/n) [y]: ").strip().lower()
            if save != 'n':
                save_results(results, detailed=detailed)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle special cases
    if args.list_sites:
        list_sites()
        return

    # If no query provided, enter interactive mode
    if not args.query:
        interactive_mode()
        return

    query = " ".join(args.query)

    # Perform search
    results, raw_results = search_phones(query, args.sites, args.max_results, args.detailed, args.verbose)

    # Display results
    display_results(results, raw_results, detailed=args.detailed, compare=args.compare)

    # Save results if requested
    if args.output in ['json', 'both']:
        save_results(raw_results if args.detailed else results, args.output_file, args.detailed)

    if args.output in ['console', 'both']:
        pass  # Already displayed above


if __name__ == "__main__":
    main()