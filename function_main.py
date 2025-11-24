#!/usr/bin/env python3
"""
Appwrite Function Handler for Universal Phone Scraper
Entry point for serverless function deployment
"""

import json
import os
from universal_search import UniversalSearch
from format_results import format_detailed_results


def main(context):
    """
    Main handler for Appwrite Function
    
    Args:
        context: Appwrite function context with req and res objects
    
    Returns:
        Function response with status and body
    """
    try:
        # Parse request
        req = context.req
        res = context.res
        
        # Get path and method
        path = req.path if hasattr(req, 'path') else req.url
        method = req.method
        
        # Handle different routes
        if method == 'GET' and '/health' in path:
            return res.json({
                'status': 'ok',
                'message': 'Universal Phone Scraper API is running'
            })
        
        elif method == 'POST' and '/search' in path:
            return handle_search(req, res)
        
        elif method == 'GET' and '/' in path:
            return res.json({
                'message': 'Universal Phone Scraper API',
                'version': '1.0.0',
                'endpoints': {
                    'POST /search': 'Search for phones',
                    'GET /health': 'Health check'
                }
            })
        
        else:
            return res.json({
                'error': 'Not Found',
                'message': f'Endpoint {path} not found'
            }, 404)
    
    except Exception as e:
        return res.json({
            'error': 'Internal Server Error',
            'message': str(e)
        }, 500)


def handle_search(req, res):
    """Handle phone search requests"""
    try:
        # Parse request body
        if hasattr(req, 'body'):
            body = req.body if isinstance(req.body, dict) else json.loads(req.body)
        else:
            body = json.loads(req.bodyRaw)
        
        # Extract parameters
        query = body.get('query', '').strip()
        mode = body.get('mode', 'basic')
        max_results = int(body.get('max_results', 5))
        sites = body.get('sites', ['gsmarena', '91mobiles', 'kimovil'])
        
        # Validate query
        if not query:
            return res.json({
                'error': 'Bad Request',
                'message': 'Query parameter is required'
            }, 400)
        
        # Validate max_results
        if max_results < 1 or max_results > 20:
            return res.json({
                'error': 'Bad Request',
                'message': 'max_results must be between 1 and 20'
            }, 400)
        
        # Perform search
        searcher = UniversalSearch()
        detailed = (mode == 'detailed')
        
        results = searcher.search(
            query=query,
            detailed=detailed,
            max_results=max_results,
            sites=sites
        )
        
        # Format response
        if detailed:
            formatted_results = format_detailed_results(results)
        else:
            formatted_results = {
                'query': query,
                'total_results': len(results),
                'phones': [
                    {
                        'name': phone.name,
                        'brand': phone.brand,
                        'price': phone.price,
                        'rating': phone.rating,
                        'url': phone.url,
                        'image_url': phone.image_url,
                        'source': phone.source
                    }
                    for phone in results
                ]
            }
        
        return res.json({
            'success': True,
            'data': formatted_results
        })
    
    except ValueError as e:
        return res.json({
            'error': 'Bad Request',
            'message': str(e)
        }, 400)
    
    except Exception as e:
        return res.json({
            'error': 'Internal Server Error',
            'message': f'Search failed: {str(e)}'
        }, 500)
