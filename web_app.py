#!/usr/bin/env python3
"""
Universal Mobile Phone Scraper - Web Interface
A Flask web application for searching mobile phones across multiple websites.
"""

from flask import Flask, render_template, request, jsonify, Response
import json
import os
from pathlib import Path
from universal_search import UniversalSearch
from format_results import format_detailed_results, print_detailed_phone
import threading
import time

app = Flask(__name__)

# Global variables for search status
search_results = {}
search_status = {"status": "idle", "progress": 0, "message": ""}

# Create templates directory
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Create static directory
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

# Create CSS directory
css_dir = static_dir / "css"
css_dir.mkdir(exist_ok=True)

# Create JS directory
js_dir = static_dir / "js"
js_dir.mkdir(exist_ok=True)


def create_html_template():
    """Create the main HTML template."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Mobile Phone Scraper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-mobile-alt"></i> Universal Phone Scraper
            </a>
            <span class="navbar-text">
                Search across GSMArena, 91mobiles & Kimovil
            </span>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-8 mx-auto">
                <div class="card shadow">
                    <div class="card-header bg-light">
                        <h4 class="mb-0"><i class="fas fa-search"></i> Phone Search</h4>
                    </div>
                    <div class="card-body">
                        <form id="searchForm">
                            <div class="mb-3">
                                <label for="query" class="form-label">Search for phones:</label>
                                <input type="text" class="form-control form-control-lg" id="query"
                                       placeholder="e.g., Samsung Galaxy S24, iPhone 15, OnePlus..." required>
                            </div>

                            <div class="row">
                                <div class="col-md-4">
                                    <label class="form-label">Search Mode:</label>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="mode" id="basic" value="basic" checked>
                                        <label class="form-check-label" for="basic">
                                            Basic Search
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="mode" id="detailed" value="detailed">
                                        <label class="form-check-label" for="detailed">
                                            Detailed Search
                                        </label>
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <label for="maxResults" class="form-label">Max Results per Site:</label>
                                    <select class="form-select" id="maxResults">
                                        <option value="3">3</option>
                                        <option value="5" selected>5</option>
                                        <option value="10">10</option>
                                        <option value="15">15</option>
                                    </select>
                                </div>

                                <div class="col-md-4">
                                    <label class="form-label">Sites to Search:</label>
                                    <div class="form-check">
                                        <input class="form-check-input site-checkbox" type="checkbox" id="gsmarena" checked>
                                        <label class="form-check-label" for="gsmarena">
                                            GSMArena
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input site-checkbox" type="checkbox" id="91mobiles" checked>
                                        <label class="form-check-label" for="91mobiles">
                                            91mobiles
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input site-checkbox" type="checkbox" id="kimovil" checked>
                                        <label class="form-check-label" for="kimovil">
                                            Kimovil
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class="d-grid mt-4">
                                <button type="submit" class="btn btn-primary btn-lg" id="searchBtn">
                                    <i class="fas fa-search"></i> Search Phones
                                </button>
                            </div>
                        </form>

                        <!-- Progress Bar -->
                        <div id="progressContainer" class="mt-4" style="display: none;">
                            <div class="progress">
                                <div class="progress-bar progress-bar-striped progress-bar-animated"
                                     role="progressbar" style="width: 0%" id="progressBar"></div>
                            </div>
                            <p class="text-center mt-2" id="progressText">Initializing search...</p>
                        </div>
                    </div>
                </div>

                <!-- Results Container -->
                <div id="resultsContainer" class="mt-4" style="display: none;">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="fas fa-list"></i> Search Results</h5>
                            <button class="btn btn-sm btn-outline-primary" id="exportBtn">
                                <i class="fas fa-download"></i> Export JSON
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="resultsContent"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="mt-5 py-4 bg-light">
        <div class="container text-center">
            <p class="mb-0 text-muted">
                <i class="fas fa-code"></i> Built with Python & Flask |
                <i class="fas fa-database"></i> Data from GSMArena, 91mobiles & Kimovil
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>"""
    return html_content


def create_css_styles():
    """Create CSS styles."""
    css_content = """body {
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    border: none;
    border-radius: 10px;
}

.card-header {
    border-radius: 10px 10px 0 0 !important;
}

.form-control:focus, .form-select:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
    background: linear-gradient(45deg, #0d6efd, #6610f2);
    border: none;
}

.btn-primary:hover {
    background: linear-gradient(45deg, #0b5ed7, #5c0fc8);
}

.progress {
    height: 25px;
    border-radius: 15px;
}

.phone-card {
    transition: transform 0.2s;
    border-radius: 10px;
    margin-bottom: 20px;
}

.phone-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.spec-table {
    font-size: 0.9em;
}

.spec-table th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.rating-stars {
    color: #ffc107;
}

.price-tag {
    font-size: 1.2em;
    font-weight: bold;
    color: #28a745;
}

.site-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 10;
}

@media (max-width: 768px) {
    .container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .phone-card {
        margin-bottom: 15px;
    }
}

/* Loading animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}"""
    return css_content


def create_js_script():
    """Create JavaScript for the web interface."""
    js_content = """// Universal Phone Scraper Web Interface

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchBtn = document.getElementById('searchBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsContent = document.getElementById('resultsContent');
    const exportBtn = document.getElementById('exportBtn');

    let currentResults = null;

    // Handle form submission
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const query = document.getElementById('query').value.trim();
        if (!query) {
            alert('Please enter a search query');
            return;
        }

        const mode = document.querySelector('input[name="mode"]:checked').value;
        const maxResults = document.getElementById('maxResults').value;

        // Get selected sites
        const sites = [];
        document.querySelectorAll('.site-checkbox:checked').forEach(cb => {
            sites.push(cb.id);
        });

        if (sites.length === 0) {
            alert('Please select at least one site to search');
            return;
        }

        // Start search
        startSearch(query, mode, maxResults, sites);
    });

    // Handle export
    exportBtn.addEventListener('click', function() {
        if (!currentResults) return;

        const dataStr = JSON.stringify(currentResults, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);

        const exportFileDefaultName = `phone_search_${Date.now()}.json`;

        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    });

    function startSearch(query, mode, maxResults, sites) {
        // Show progress
        progressContainer.style.display = 'block';
        resultsContainer.style.display = 'none';
        searchBtn.disabled = true;
        searchBtn.innerHTML = '<span class="loading"></span> Searching...';

        // Reset progress
        progressBar.style.width = '0%';
        progressText.textContent = 'Initializing search...';

        // Make API request
        fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                mode: mode,
                max_results: parseInt(maxResults),
                sites: sites
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                currentResults = data.results;
                displayResults(data.results, mode);
            } else {
                throw new Error(data.message || 'Search failed');
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            alert('Search failed: ' + error.message);
        })
        .finally(() => {
            progressContainer.style.display = 'none';
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search"></i> Search Phones';
        });

        // No need to poll for progress since search is synchronous now
    }

    function displayResults(results, mode) {
        resultsContainer.style.display = 'block';

        let html = '';

        if (mode === 'detailed') {
            html = displayDetailedResults(results);
        } else {
            html = displayBasicResults(results);
        }

        resultsContent.innerHTML = html;
    }

    function displayBasicResults(results) {
        let html = '';
        let totalCount = 0;

        for (const [site, phones] of Object.entries(results)) {
            if (phones && phones.length > 0) {
                html += `<div class="site-section mb-4">
                    <h4 class="text-primary mb-3">
                        <i class="fas fa-globe"></i> ${site.toUpperCase()} (${phones.length} results)
                    </h4>`;

                phones.forEach(phone => {
                    totalCount++;
                    const phoneName = phone.brand + ' ' + phone.model;
                    const rating = phone.rating ? `<span class="rating-stars">${'★'.repeat(Math.floor(phone.rating/2))}</span> ${phone.rating}/10` : '';
                    const price = phone.price ? `<div class="price-tag">${phone.price}</div>` : '';

                    html += `
                    <div class="card phone-card position-relative">
                        <span class="badge bg-primary site-badge">${site}</span>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <h5 class="card-title">${phoneName}</h5>
                                    ${price}
                                    <p class="text-muted mb-2">${rating}</p>
                                    ${phone.specs ? `<p class="mb-0">${Object.keys(phone.specs).slice(0, 3).join(' • ')}</p>` : ''}
                                </div>
                                <div class="col-md-4 text-end">
                                    <a href="${phone.url}" target="_blank" class="btn btn-outline-primary btn-sm">
                                        <i class="fas fa-external-link-alt"></i> View Details
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>`;
                });

                html += '</div>';
            }
        }

        if (totalCount === 0) {
            html = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> No phones found matching your search.</div>';
        }

        return html;
    }

    function displayDetailedResults(results) {
        let html = '';

        if (results && results.result && results.result.length > 0) {
            html += `<div class="alert alert-success mb-4">
                <i class="fas fa-check-circle"></i> Found ${results.total_result} phones
            </div>`;

            results.result.forEach(phone => {
                const highlights = phone.highlights ? phone.highlights.map(h => `<span class="badge bg-light text-dark me-1">${h}</span>`).join('') : '';
                const offers = phone.offers ? phone.offers.map(o => `<li>${o.description}</li>`).join('') : '';

                html += `
                <div class="card phone-card mb-4">
                    <div class="card-header bg-light">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h4 class="mb-1">${phone.name}</h4>
                                <div class="d-flex gap-3">
                                    ${phone.current_price ? `<span class="price-tag">${phone.current_price}</span>` : ''}
                                    ${phone.original_price ? `<span class="text-muted text-decoration-line-through">${phone.original_price}</span>` : ''}
                                    ${phone.rating ? `<span><i class="fas fa-star text-warning"></i> ${phone.rating}</span>` : ''}
                                </div>
                            </div>
                            <a href="${phone.link}" target="_blank" class="btn btn-primary">
                                <i class="fas fa-external-link-alt"></i> View Original
                            </a>
                        </div>
                    </div>

                    <div class="card-body">
                        ${highlights ? `<div class="mb-3">${highlights}</div>` : ''}

                        ${phone.specs && phone.specs.length > 0 ? `
                        <div class="mb-3">
                            <h6><i class="fas fa-cogs"></i> Specifications</h6>
                            <div class="accordion" id="specs-${phone.name.replace(/[^a-zA-Z0-9]/g, '')}">
                                ${phone.specs.map((spec, index) => `
                                <div class="accordion-item">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button ${index > 0 ? 'collapsed' : ''}" type="button"
                                                data-bs-toggle="collapse" data-bs-target="#spec-${index}">
                                            ${spec.title}
                                        </button>
                                    </h2>
                                    <div id="spec-${index}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}">
                                        <div class="accordion-body">
                                            <table class="table table-sm spec-table">
                                                <tbody>
                                                    ${spec.details.map(detail => `
                                                    <tr>
                                                        <th style="width: 40%">${detail.property}</th>
                                                        <td>${detail.value}</td>
                                                    </tr>
                                                    `).join('')}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                                `).join('')}
                            </div>
                        </div>
                        ` : ''}

                        ${offers ? `
                        <div class="mb-3">
                            <h6><i class="fas fa-tags"></i> Offers & Deals</h6>
                            <ul class="list-unstyled">${offers}</ul>
                        </div>
                        ` : ''}

                        ${phone.all_thumbnails && phone.all_thumbnails.length > 0 ? `
                        <div class="mb-3">
                            <h6><i class="fas fa-images"></i> Images (${phone.all_thumbnails.length})</h6>
                            <div class="row">
                                ${phone.all_thumbnails.slice(0, 6).map(img => `
                                <div class="col-4 col-md-2 mb-2">
                                    <img src="${img}" class="img-fluid rounded" style="height: 60px; width: 100%; object-fit: cover;" onclick="window.open(this.src)">
                                </div>
                                `).join('')}
                            </div>
                        </div>
                        ` : ''}
                    </div>
                </div>`;
            });
        } else {
            html = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> No detailed results found.</div>';
        }

        return html;
    }
});"""
    return js_content


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for phone search."""
    global search_results, search_status

    try:
        data = request.get_json()

        query = data.get('query', '').strip()
        mode = data.get('mode', 'basic')
        max_results = data.get('max_results', 5)
        sites = data.get('sites', ['gsmarena', '91mobiles', 'kimovil'])

        if not query:
            return jsonify({'status': 'error', 'message': 'Query is required'})

        # Reset status
        search_status = {"status": "running", "progress": 0, "message": "Initializing search..."}

        # Perform search synchronously for simplicity
        try:
            search_status = {"status": "running", "progress": 25, "message": "Searching sites..."}
            searcher = UniversalSearch()
            results = searcher.search_all(query, max_results_per_site=max_results, sites=sites)

            search_status = {"status": "running", "progress": 75, "message": "Processing results..."}
            
            if mode == 'detailed':
                # Format as detailed results
                formatted = format_detailed_results(results)
                search_results = formatted
            else:
                # Convert to simple format for basic mode
                basic_results = {}
                for site_name, site_data in results['scrapers'].items():
                    if site_data['status'] == 'success':
                        basic_results[site_name] = site_data['phones']
                    else:
                        basic_results[site_name] = []
                search_results = basic_results

            search_status = {"status": "completed", "progress": 100, "message": "Search completed"}
            
            return jsonify({
                'status': 'success',
                'message': 'Search completed',
                'results': search_results
            })

        except Exception as e:
            search_status = {"status": "error", "progress": 0, "message": str(e)}
            return jsonify({'status': 'error', 'message': str(e)})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/api/progress')
def api_progress():
    """Get search progress."""
    return jsonify(search_status)


@app.route('/api/results')
def api_results():
    """Get search results."""
    return jsonify(search_results)


@app.route('/favicon.ico')
def favicon():
    """Return empty favicon to avoid 404 errors."""
    return '', 204


def create_templates():
    """Create HTML templates."""
    # Create base template
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(create_html_template())

    # Create CSS
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(create_css_styles())

    # Create JS
    with open('static/js/app.js', 'w', encoding='utf-8') as f:
        f.write(create_js_script())


def main():
    """Main function to run the web interface."""
    print("🚀 Starting Universal Phone Scraper Web Interface...")
    print("📁 Creating templates and static files...")

    # Create templates and static files
    create_templates()

    print("✅ Files created successfully!")
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("❌ Press Ctrl+C to stop the server")

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()