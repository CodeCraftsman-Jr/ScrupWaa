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
        username = os.environ.get('MONGO_DB_USERNAME', 'baeonuser')
        password = os.environ.get('MONGO_DB_PASSWORD', '6JtLUmRHTMZ8IYJA')
        database = os.environ.get('MONGO_DB_DATABASE_NAME', 'baeonDBStage')
        domain = os.environ.get('MONGO_DB_DOMAIN_NAME', 'baeonncluster.oakjn89')
        
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
    
    def save_scrape_results(self, query: str, phones: List[Dict], method: str = "headless_browser") -> Optional[str]:
        """
        Save scraping results to MongoDB.
        
        Args:
            query: Search query used
            phones: List of phone data dictionaries
            method: Scraping method used
            
        Returns:
            Inserted document ID or None if failed
        """
        try:
            document = {
                'query': query,
                'timestamp': datetime.utcnow(),
                'method': method,
                'total_results': len(phones),
                'phones': phones,
                'created_at': datetime.utcnow()
            }
            
            result = self.collection.insert_one(document)
            
            print(f"[MONGODB] ✅ Saved {len(phones)} phones to collection")
            print(f"[MONGODB] Document ID: {result.inserted_id}")
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"[MONGODB] ❌ Failed to save: {e}")
            return None
    
    def save_phone(self, phone_data: Dict) -> Optional[str]:
        """
        Save a single phone to MongoDB.
        
        Args:
            phone_data: Phone data dictionary
            
        Returns:
            Inserted document ID or None if failed
        """
        try:
            # Add timestamp
            phone_data['scraped_at'] = datetime.utcnow()
            
            result = self.collection.insert_one(phone_data)
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
            count = self.collection.count_documents({})
            
            # Get total phones across all documents
            pipeline = [
                {'$unwind': '$phones'},
                {'$count': 'total_phones'}
            ]
            
            result = list(self.collection.aggregate(pipeline))
            total_phones = result[0]['total_phones'] if result else 0
            
            return {
                'total_scrapes': count,
                'total_phones': total_phones,
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
