# GitHub Actions Scraper with Appwrite Proxies

This project uses GitHub Actions to scrape phone data using proxies from Appwrite database.

## Setup

1. **Appwrite Database Structure**
   
   Your proxy collection should have documents with these fields:
   ```json
   {
     "proxy_url": "http://proxy-ip:port",
     "http_proxy": "http://proxy-ip:port",  // alternative
     "https_proxy": "https://proxy-ip:port", // alternative
     "username": "proxy_username",  // optional
     "password": "proxy_password",  // optional
     "active": true  // optional, default true
   }
   ```

2. **GitHub Secrets** (Optional - currently hardcoded in workflow)
   
   For better security, move these to GitHub Secrets:
   - `APPWRITE_ENDPOINT`
   - `APPWRITE_PROJECT_ID`
   - `APPWRITE_DATABASE_ID`
   - `APPWRITE_COLLECTION_ID`
   - `APPWRITE_API_KEY`

## Running the Workflow

### Manual Trigger

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Scrape Phone Data" workflow
4. Click "Run workflow"
5. Enter:
   - Search query (e.g., "Samsung S24")
   - Max results (0 for all, or specific number like 20)
6. Click "Run workflow"

### View Results

After the workflow completes:
1. Go to the workflow run
2. Download the "scrape-results" artifact
3. Extract the JSON files with scraped data

## Files

- `.github/workflows/scrape-phones.yml` - GitHub Actions workflow
- `github_scraper.py` - Main scraper script with proxy support
- `data/` - Output directory for scraped results

## How It Works

1. Workflow fetches proxies from Appwrite database
2. Scraper rotates through proxies for each request
3. Rate limiting is bypassed using different IPs
4. Results are saved as JSON artifacts
5. Optionally commits results back to repository

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export APPWRITE_ENDPOINT="https://cloud.appwrite.io/v1"
export APPWRITE_PROJECT_ID="68a227de003201ae2463"
export APPWRITE_DATABASE_ID="68a227fb00180c4a541a"
export APPWRITE_COLLECTION_ID="68a2280e0039af9b6a24"
export APPWRITE_API_KEY="your_key_here"
export SEARCH_QUERY="Samsung S24"
export MAX_RESULTS="20"

# Run scraper
python github_scraper.py
```

## Proxy Rotation

The scraper automatically:
- Fetches all active proxies from Appwrite
- Randomly selects a proxy for each request
- Falls back to direct connection if proxies fail
- Logs which proxy is being used

## Scheduled Runs (Optional)

Uncomment the schedule section in the workflow to run automatically:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```
