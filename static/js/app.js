// Universal Phone Scraper Web Interface

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
});