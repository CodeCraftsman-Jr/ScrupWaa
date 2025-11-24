# 🚀 Appwrite Deployment Guide - ScrupWaa Phone Scraper

Complete guide to deploy the Universal Phone Scraper on Appwrite Functions and Static Hosting.

## 📋 Prerequisites

1. **Appwrite Account**: Sign up at [cloud.appwrite.io](https://cloud.appwrite.io)
2. **Appwrite CLI**: Install the CLI tool
   ```bash
   npm install -g appwrite-cli
   ```
3. **Git** (optional): For version control

---

## 🎯 Architecture Overview

- **Backend**: Appwrite Function (Python 3.11) - Handles scraping logic
- **Frontend**: Appwrite Static Hosting - Serves the web interface
- **No Database**: Stateless operations, results returned directly

**URLs Provided by Appwrite:**
- Function: `https://cloud.appwrite.io/v1/functions/[FUNCTION_ID]/executions`
- Static Site: `https://[PROJECT_NAME].appwrite.global`

---

## 📦 Part 1: Deploy Backend Function

### Step 1: Login to Appwrite CLI

```bash
appwrite login
```

Follow the prompts to authenticate with your Appwrite account.

### Step 2: Initialize Appwrite Project

```bash
# Navigate to your project directory
cd z:\D\ScrupWaa

# Initialize project (or link to existing)
appwrite init project
```

When prompted:
- Select or create a project
- Note your **Project ID** (you'll need this)

### Step 3: Update appwrite.json

Open `appwrite.json` and add your project ID:

```json
{
  "projectId": "YOUR_PROJECT_ID_HERE",
  "projectName": "ScrupWaa",
  ...
}
```

### Step 4: Deploy the Function

```bash
# Deploy function from the project root
appwrite deploy function
```

Select the `phone-scraper` function when prompted.

**Build Process:**
- Appwrite will build a Docker image using the `Dockerfile`
- Install dependencies from `requirements.txt`
- Deploy the function with Python 3.11 runtime

**Deployment Time:** ~3-5 minutes

### Step 5: Get Function URL

After deployment:

1. Go to [Appwrite Console](https://cloud.appwrite.io/console)
2. Navigate to **Functions** → **phone-scraper**
3. Copy the **Function URL**:
   ```
   https://cloud.appwrite.io/v1/functions/[FUNCTION_ID]/executions
   ```

### Step 6: Configure CORS (Important!)

To allow the frontend to call the function:

1. In Appwrite Console → **Functions** → **phone-scraper**
2. Go to **Settings** → **CORS**
3. Add allowed origins:
   - `*` (for testing - allows all origins)
   - Or specific: `https://your-site-name.appwrite.global`
4. Save changes

### Step 7: Test the Function

Test via curl or Postman:

```bash
curl -X POST "https://cloud.appwrite.io/v1/functions/YOUR_FUNCTION_ID/executions/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Samsung Galaxy S24",
    "mode": "basic",
    "max_results": 3,
    "sites": ["gsmarena"]
  }'
```

Expected response:
```json
{
  "success": true,
  "data": {
    "query": "Samsung Galaxy S24",
    "total_results": 3,
    "phones": [...]
  }
}
```

---

## 🌐 Part 2: Deploy Frontend (Static Hosting)

### Step 1: Prepare Static Files

All frontend files are ready in the `web/` directory:
```
web/
├── index.html
├── css/
│   └── style.css
└── js/
    ├── config.js
    └── app.js
```

### Step 2: Update API Configuration

Edit `web/js/config.js` and replace the placeholder:

```javascript
const API_CONFIG = {
    functionUrl: 'https://cloud.appwrite.io/v1/functions/YOUR_FUNCTION_ID/executions'
};
```

**Example:**
```javascript
const API_CONFIG = {
    functionUrl: 'https://cloud.appwrite.io/v1/functions/6789abcd1234/executions'
};
```

### Step 3: Deploy to Appwrite Static Hosting

**Option A: Via Appwrite Console (Easiest)**

1. Go to [Appwrite Console](https://cloud.appwrite.io/console)
2. Select your project
3. Navigate to **Hosting** → **Add site**
4. Enter site name (e.g., `scrupwaa`)
5. Upload the `web/` folder:
   - Drag and drop the entire `web` folder
   - Or use "Upload files" button
6. Set `index.html` as the root document
7. Click **Deploy**

**Option B: Via CLI**

```bash
# From project root
appwrite deploy collection

# When prompted, select "Static Site"
# Choose the web/ directory
```

### Step 4: Access Your Site

After deployment, your site will be available at:
```
https://scrupwaa.appwrite.global
```

(Replace `scrupwaa` with your chosen site name)

---

## ✅ Verification Checklist

### Backend Function
- [ ] Function deploys without errors
- [ ] Test endpoint responds with 200 OK
- [ ] CORS is configured correctly
- [ ] Function logs show successful requests (check Console → Functions → Logs)

### Frontend Static Site
- [ ] Site loads correctly in browser
- [ ] API URL is configured in `config.js`
- [ ] Search form is visible
- [ ] No console errors (press F12 to check)

### End-to-End Test
- [ ] Perform a search from the web interface
- [ ] Results display correctly
- [ ] Export JSON works
- [ ] Mobile responsive design works

---

## 🔧 Configuration Options

### Environment Variables (Optional)

Add environment variables in Function settings:

1. Go to **Functions** → **phone-scraper** → **Settings** → **Environment Variables**
2. Add:
   - `SCRAPER_MIN_DELAY`: `1` (minimum delay between requests)
   - `SCRAPER_MAX_DELAY`: `3` (maximum delay between requests)
   - `HTTP_TIMEOUT`: `30` (HTTP request timeout)

### Function Timeout

Default: 300 seconds (5 minutes)

To change:
1. Edit `appwrite.json` → `functions[0].timeout`
2. Redeploy: `appwrite deploy function`

### Rate Limiting

Modify `config.py` in your code to adjust:
- Request delays
- Retry attempts
- Timeout values

---

## 🐛 Troubleshooting

### Issue: Function Returns 500 Error

**Cause:** Missing dependencies or code error

**Solution:**
1. Check function logs: Console → Functions → Logs
2. Verify `requirements.txt` includes all dependencies
3. Test locally first: `python function_main.py`

### Issue: CORS Error in Browser

**Cause:** CORS not configured

**Solution:**
1. Add `*` or your site URL to Function CORS settings
2. Ensure response headers include `Access-Control-Allow-Origin`

### Issue: "API URL Not Configured" Alert

**Cause:** Frontend config not updated

**Solution:**
1. Edit `web/js/config.js`
2. Replace `YOUR_APPWRITE_FUNCTION_URL_HERE` with actual URL
3. Redeploy static site

### Issue: Scraping Returns No Results

**Cause:** Target sites may block requests

**Solution:**
1. Check function logs for errors
2. Verify HTTP client is working: test with curl
3. Consider adding delays or using different user agents
4. Some sites may require more sophisticated bypass methods

### Issue: Function Timeout

**Cause:** Scraping takes too long

**Solution:**
1. Reduce `max_results` parameter
2. Search fewer sites at once
3. Increase function timeout in `appwrite.json`

---

## 📊 Monitoring & Logs

### View Function Logs

```bash
# Via CLI
appwrite functions get [FUNCTION_ID] --logs

# Or in Console
Functions → phone-scraper → Logs
```

### Performance Metrics

Monitor in Appwrite Console:
- Execution time
- Success/error rate
- Total executions
- Resource usage

---

## 🚀 Optimization Tips

1. **Caching**: Consider implementing response caching for frequent searches
2. **CDN**: Appwrite automatically serves static assets via CDN
3. **Compression**: Enable gzip for faster page loads
4. **Lazy Loading**: Load images on demand to improve performance
5. **Rate Limiting**: Implement client-side throttling to avoid hitting limits

---

## 🔒 Security Best Practices

1. **API Keys**: Never expose Appwrite API keys in frontend code
2. **CORS**: Set specific origins instead of `*` in production
3. **Rate Limiting**: Implement rate limiting on function side
4. **Input Validation**: Function validates all inputs
5. **HTTPS Only**: Appwrite enforces HTTPS by default

---

## 🆙 Updating the Deployment

### Update Function Code

```bash
# After making code changes
appwrite deploy function

# Select phone-scraper
```

### Update Frontend

**Via Console:**
1. Go to Hosting → Your Site
2. Click "Upload New Version"
3. Upload modified files

**Via CLI:**
```bash
appwrite deploy collection
```

---

## 💰 Pricing Considerations

**Appwrite Cloud Free Tier:**
- 75K function executions/month
- 10GB bandwidth
- Unlimited static hosting

**Usage Estimates:**
- Each search = 1 function execution
- Average execution time: 10-30 seconds
- Static hosting: minimal bandwidth usage

**Monitor Usage:**
- Console → Project Settings → Usage

---

## 🎉 You're Done!

Your phone scraper is now live on Appwrite! 

**Function URL:** `https://cloud.appwrite.io/v1/functions/[FUNCTION_ID]/executions`  
**Website URL:** `https://[YOUR_SITE].appwrite.global`

Share your website and start searching for phones! 🔍📱

---

## 📚 Additional Resources

- [Appwrite Functions Docs](https://appwrite.io/docs/products/functions)
- [Appwrite Static Hosting](https://appwrite.io/docs/products/storage)
- [Python Runtime Guide](https://appwrite.io/docs/products/functions/runtimes)
- [Appwrite CLI Reference](https://appwrite.io/docs/tooling/command-line/commands)

---

## 🆘 Need Help?

- **Appwrite Discord**: [discord.gg/appwrite](https://discord.gg/appwrite)
- **GitHub Issues**: [github.com/appwrite/appwrite](https://github.com/appwrite/appwrite/issues)
- **Documentation**: [appwrite.io/docs](https://appwrite.io/docs)

---

**Note:** No custom domain required! Appwrite provides both function and hosting URLs automatically. You can add a custom domain later if desired through the Appwrite Console.
