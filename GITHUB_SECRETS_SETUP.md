# GitHub Secrets Setup

This document explains how to configure GitHub repository secrets for the phone scraper to work in GitHub Actions.

## Required Secrets

Navigate to your repository settings to add these secrets:
**GitHub Repository** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### MongoDB Credentials

Add the following 4 secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `MONGO_DB_USERNAME` | `baeonuser` | MongoDB Atlas username |
| `MONGO_DB_PASSWORD` | `6JtLUmRHTMZ8IYJA` | MongoDB Atlas password |
| `MONGO_DB_DATABASE_NAME` | `baeonDBStage` | Database name |
| `MONGO_DB_DOMAIN_NAME` | `baeonncluster.oakjn89` | MongoDB cluster domain |

## Step-by-Step Instructions

1. **Go to Repository Settings**
   - Navigate to: `https://github.com/CodeCraftsman-Jr/ScrupWaa/settings/secrets/actions`

2. **Add Each Secret**
   - Click **"New repository secret"**
   - Enter the **Name** (exactly as shown above)
   - Enter the **Value** 
   - Click **"Add secret"**

3. **Repeat for All 4 Secrets**
   - MONGO_DB_USERNAME
   - MONGO_DB_PASSWORD
   - MONGO_DB_DATABASE_NAME
   - MONGO_DB_DOMAIN_NAME

4. **Verify Setup**
   - Go to **Actions** tab
   - Click **"Scrape Phone Data"** workflow
   - Click **"Run workflow"**
   - Enter search query (e.g., "Samsung S24")
   - Click **"Run workflow"** button
   - Wait for the workflow to complete

## Testing Locally

To test locally before pushing, set environment variables:

### Windows PowerShell
```powershell
$env:MONGO_DB_USERNAME="baeonuser"
$env:MONGO_DB_PASSWORD="6JtLUmRHTMZ8IYJA"
$env:MONGO_DB_DATABASE_NAME="baeonDBStage"
$env:MONGO_DB_DOMAIN_NAME="baeonncluster.oakjn89"
$env:SEARCH_QUERY="Samsung S24"
$env:MAX_RESULTS="2"
python github_scraper.py
```

### Linux/Mac
```bash
export MONGO_DB_USERNAME="baeonuser"
export MONGO_DB_PASSWORD="6JtLUmRHTMZ8IYJA"
export MONGO_DB_DATABASE_NAME="baeonDBStage"
export MONGO_DB_DOMAIN_NAME="baeonncluster.oakjn89"
export SEARCH_QUERY="Samsung S24"
export MAX_RESULTS="2"
python github_scraper.py
```

## Security Notes

- ✅ Secrets are encrypted and not visible in logs
- ✅ Only repository collaborators with write access can add/modify secrets
- ✅ Secrets are not passed to forked repositories
- ✅ Workflow logs will show `***` instead of actual secret values

## Troubleshooting

### Error: "MONGO_DB_USERNAME not found"
- Check that all 4 secrets are added exactly as shown
- Secret names are case-sensitive
- No quotes needed around the secret names in GitHub UI

### Error: "MongoDB connection failed"
- Verify MongoDB credentials are correct
- Check if MongoDB Atlas allows connections from GitHub Actions IPs (0.0.0.0/0)
- Ensure database and collection exist

### Workflow not running
- Check if workflow file is committed: `.github/workflows/scrape-phones.yml`
- Verify GitHub Actions are enabled in repository settings
- Check workflow syntax is valid YAML

## MongoDB Document Structure

Each phone is saved as a separate document:

```json
{
  "query": "Samsung S24",
  "method": "headless_browser",
  "scraped_at": "2025-11-29T09:15:35Z",
  "source": "GSMArena",
  "brand": "Samsung",
  "model": "Galaxy S24 Ultra",
  "url": "https://www.gsmarena.com/...",
  "image": "...",
  "display": {...},
  "performance": {...},
  "camera": {...},
  "battery": {...},
  "network": {...}
}
```

- **1 scrape = N documents** (1 document per phone)
- **1 row = 1 phone** (not an array of phones)
