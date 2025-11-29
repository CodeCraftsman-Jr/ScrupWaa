"""
MongoDB client for storing scraped phone data
"""

from pymongo import MongoClient
from typing import List, Dict, Optional
from datetime import datetime
import os


class MongoDBClient:
    """MongoDB client for storing phone scraping results."""
    
    def __init__(self):
        """Initialize MongoDB connection."""
        # Get credentials from environment
        username = os.environ.get('MONGO_DB_USERNAME')
        password = os.environ.get('MONGO_DB_PASSWORD')
        database = os.environ.get('MONGO_DB_DATABASE_NAME')
        domain = os.environ.get('MONGO_DB_DOMAIN_NAME')
        
        if not all([username, password, database, domain]):
            raise ValueError("MongoDB credentials not found in environment variables")
        
        # Construct connection string
        self.connection_string = f"mongodb+srv://{username}:{password}@{domain}.mongodb.net/?retryWrites=true&w=majority"
        
        self.client = None
        self.db = None
        self.collection = None
        self.database_name = database
        self.collection_name = "phone_scraped_data"
        
        self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB."""
        try:
            print(f"[MONGODB] Connecting to database: {self.database_name}")
            self.client = MongoClient(self.connection_string)
            
            # Test connection
            self.client.server_info()
            
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            
            print(f"[MONGODB] ✅ Connected successfully")
            print(f"[MONGODB] Collection: {self.collection_name}")
            
        except Exception as e:
            print(f"[MONGODB] ❌ Connection failed: {e}")
            raise
    
    def save_scrape_results(self, query: str, phones: List[Dict], method: str = "headless_browser", source: str = "GSMArena") -> Optional[str]:
        """
        Save scraping results to MongoDB with proper organization.
        
        Args:
            query: Search query used
            phones: List of phone data dictionaries (each should have 'source' as first field)
            method: Scraping method used
            source: Source website name
            
        Returns:
            Inserted document ID or None if failed
        """
        try:
            # Organize document structure
            document = {
                'query': query,
                'source': source,
                'timestamp': datetime.utcnow(),
                'method': method,
                'total_results': len(phones),
                'phones': phones,  # Array of phones with source as first field
                'created_at': datetime.utcnow()
            }
            
            result = self.collection.insert_one(document)
            
            print(f"[MONGODB] ✅ Saved {len(phones)} phones to collection")
            print(f"[MONGODB] Document ID: {result.inserted_id}")
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"[MONGODB] ❌ Failed to save: {e}")
            return None
    
    def save_phone(self, query: str, phone_data: Dict, method: str = "headless_browser") -> Optional[str]:
        """
        Save a single phone to MongoDB as one document.
        
        Args:
            query: Search query used
            phone_data: Phone data dictionary (should have 'source' field)
            method: Scraping method used
            
        Returns:
            Inserted document ID or None if failed
        """
        try:
            # Create document with metadata and phone data at same level
            document = {
                'query': query,
                'method': method,
                'scraped_at': datetime.utcnow(),
                **phone_data  # Spread phone data fields (includes 'source' as first field)
            }
            
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"[MONGODB] ❌ Failed to save phone: {e}")
            return None
    
    def get_recent_scrapes(self, limit: int = 10) -> List[Dict]:
        """
        Get recent scraping results.
        
        Args:
            limit: Number of results to return
            
        Returns:
            List of scraping result documents
        """
        try:
            results = list(
                self.collection
                .find()
                .sort('timestamp', -1)
                .limit(limit)
            )
            
            # Convert ObjectId to string
            for result in results:
                result['_id'] = str(result['_id'])
            
            return results
            
        except Exception as e:
            print(f"[MONGODB] ❌ Failed to fetch: {e}")
            return []
    
    def search_phones(self, query: str) -> List[Dict]:
        """
        Search for phones by query in stored data.
        
        Args:
            query: Search query
            
        Returns:
            List of matching phone documents
        """
        try:
            results = list(
                self.collection.find({
                    '$or': [
                        {'query': {'$regex': query, '$options': 'i'}},
                        {'phones.brand': {'$regex': query, '$options': 'i'}},
                        {'phones.model': {'$regex': query, '$options': 'i'}}
                    ]
                })
            )
            
            # Convert ObjectId to string
            for result in results:
                result['_id'] = str(result['_id'])
            
            return results
            
        except Exception as e:
            print(f"[MONGODB] ❌ Search failed: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection."""
        try:
            # Now each document is one phone, so just count documents
            count = self.collection.count_documents({})
            
            return {
                'total_documents': count,
                'collection': self.collection_name,
                'database': self.database_name
            }
            
        except Exception as e:
            print(f"[MONGODB] ❌ Stats failed: {e}")
            return {}
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("[MONGODB] Connection closed")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
