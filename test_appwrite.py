"""
Test Appwrite proxy database connection
"""

import os
from appwrite.client import Client
from appwrite.services.databases import Databases

# Configuration
APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
APPWRITE_PROJECT_ID = "68a227de003201ae2463"
APPWRITE_DATABASE_ID = "68a227fb00180c4a541a"
APPWRITE_COLLECTION_ID = "68a2280e0039af9b6a24"
APPWRITE_API_KEY = "standard_07fb15b720e462b3836f463480a1806e1bdff6395d21e97cb0d835c7403329923073329e7fb76ee8de3f42e732d391583be826c2a91afe6014c7e248cf14b64880e9597257eec3ad82c78bf1b13b99b9ecb8bc7357fab9284afa73e8e245788449418dcc468499870fd5da6ebbd5b1148370260ab2dc82431cd5ad5b2df32621"

def test_appwrite_connection():
    """Test connection to Appwrite and fetch proxies"""
    print("=" * 60)
    print("Testing Appwrite Proxy Database Connection")
    print("=" * 60)
    
    try:
        # Initialize client
        print("\n[1] Initializing Appwrite client...")
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_API_KEY)
        print("✅ Client initialized")
        
        # Get databases service
        print("\n[2] Connecting to database service...")
        databases = Databases(client)
        print("✅ Connected to database service")
        
        # Fetch documents
        print(f"\n[3] Fetching documents from collection: {APPWRITE_COLLECTION_ID}")
        result = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_COLLECTION_ID
        )
        
        print(f"✅ Fetched {result['total']} documents")
        
        # Display proxy information
        print("\n" + "=" * 60)
        print("PROXY LIST")
        print("=" * 60)
        
        if result['total'] == 0:
            print("⚠️  No proxies found in database!")
            print("\nExpected document structure:")
            print("""
{
  "proxy_url": "http://proxy-ip:port",
  "username": "optional_username",
  "password": "optional_password",
  "active": true
}
            """)
        else:
            for idx, doc in enumerate(result['documents'], 1):
                print(f"\n[Proxy {idx}]")
                print(f"  ID: {doc['$id']}")
                
                # Check for different field names
                proxy_url = doc.get('proxy_url') or doc.get('http_proxy') or doc.get('url')
                username = doc.get('username') or doc.get('user')
                password = doc.get('password') or doc.get('pass')
                active = doc.get('active', True)
                
                print(f"  URL: {proxy_url}")
                print(f"  Username: {username if username else 'None'}")
                print(f"  Password: {'***' if password else 'None'}")
                print(f"  Active: {active}")
                
                # Show all available fields
                print(f"  Available fields: {list(doc.keys())}")
        
        print("\n" + "=" * 60)
        print("CONNECTION TEST SUCCESSFUL")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Check if API key has correct permissions (read access to database)")
        print("2. Verify project ID, database ID, and collection ID are correct")
        print("3. Ensure the collection exists and has documents")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_appwrite_connection()
    exit(0 if success else 1)
