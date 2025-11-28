"""
Flask Web App for Universal Phone Scraper - Local Version
Run this locally to avoid cloud platform IP blocks
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'function'))

from universal_search import UniversalSearch
from format_results import format_detailed_results

# Flask app with custom template and static folders
app = Flask(__name__, 
            static_folder='web',
            static_url_path='')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    """Serve the main page"""
    return send_from_directory('web', 'index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """Handle phone search requests"""
    try:
        data = request.get_json()
        
        # Extract parameters
        query = data.get('query', '').strip()
        mode = data.get('mode', 'basic')
        max_results = int(data.get('max_results', 999))  # High default to get all
        sites = data.get('sites', ['gsmarena'])  # Default to GSMArena only
        
        # Validate query
        if not query:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Query parameter is required'
            }), 400
        
        # Validate max_results
        if max_results < 1 or max_results > 20:
            return jsonify({
                'error': 'Bad Request',
                'message': 'max_results must be between 1 and 20'
            }), 400
        
        print(f"[SEARCH] Query: {query}, Mode: {mode}, Sites: {sites}")
        
        # Perform search
        searcher = UniversalSearch()
        detailed = (mode == 'detailed')
        
        if detailed:
            # For detailed mode, search all and format
            results = searcher.search_all(
                query=query,
                max_results_per_site=max_results,
                sites=sites
            )
        else:
            # For basic mode, use search_all and flatten results
            results = searcher.search_all(
                query=query,
                max_results_per_site=max_results,
                sites=sites
            )
        
        print(f"[RESULTS] Search completed")
        
        # Format response
        if detailed:
            formatted_results = format_detailed_results(results)
        else:
            # Flatten results from all scrapers
            all_phones = []
            if isinstance(results, dict) and 'scrapers' in results:
                for site, site_results in results['scrapers'].items():
                    if site_results.get('success') and site_results.get('phones'):
                        all_phones.extend(site_results['phones'])
            
            formatted_results = {
                'query': query,
                'total_results': len(all_phones),
                'phones': [
                    {
                        'name': f"{phone.brand} {phone.model}",
                        'brand': phone.brand,
                        'price': phone.price,
                        'rating': phone.rating,
                        'url': phone.url,
                        'image_url': phone.thumbnail or (phone.images[0] if phone.images else None),
                        'source': phone.source
                    }
                    for phone in all_phones
                ]
            }
        
        return jsonify({
            'success': True,
            'data': formatted_results
        })
    
    except ValueError as e:
        return jsonify({
            'error': 'Bad Request',
            'message': str(e)
        }), 400
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Internal Server Error',
            'message': f'Search failed: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Universal Phone Scraper API is running locally'
    })

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║     Universal Phone Scraper - Local Web Server          ║
║                                                          ║
║  Running locally to avoid cloud platform IP blocks!     ║
╚══════════════════════════════════════════════════════════╝

[*] Server starting on http://localhost:5000
[*] Open http://localhost:5000 in your browser
[*] API endpoint: http://localhost:5000/api/search
[*] Press Ctrl+C to stop
    """)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
