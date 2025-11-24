# 🚀 Appwrite Deployment - Console-Based Method

## ⚠️ CLI Issue Detected

The Appwrite CLI appears to have installation issues on your system. **No worries!** You can deploy everything through the **Appwrite Console** (web interface) instead.

---

## 🌐 Deploy via Appwrite Console (Recommended)

### Step 1: Create Appwrite Account

1. Go to [cloud.appwrite.io](https://cloud.appwrite.io)
2. Click **"Sign Up"** or **"Get Started"**
3. Create your account (free tier includes 75K executions/month)
4. Verify your email

---

### Step 2: Create a New Project

1. After logging in, click **"Create Project"**
2. Enter project name: **ScrupWaa**
3. Click **"Create"**
4. **Note your Project ID** (shown in the project settings)

---

### Step 3: Deploy Backend Function

#### 3.1: Create Function

1. In your project dashboard, click **"Functions"** in the left sidebar
2. Click **"Create Function"**
3. Configure:
   - **Name**: `phone-scraper`
   - **Runtime**: Select **Python 3.11**
   - **Execute Access**: Select **Any** (or configure as needed)
   - **Timeout**: `300` seconds
4. Click **"Create"**

#### 3.2: Upload Function Code

**Option A: Manual Upload**

1. Create a ZIP file of your function code:
   ```powershell
   # In PowerShell, run from your project directory
   Compress-Archive -Path function_main.py,universal_search.py,format_results.py,config.py,requirements.txt,models,scrapers,utils -DestinationPath function.zip
   ```

2. In the Function settings, go to **"Deployments"** tab
3. Click **"Create Deployment"**
4. **Upload** the `function.zip` file
5. Set **Entrypoint**: `function_main.py`
6. Set **Commands**: `pip install -r requirements.txt`
7. Click **"Deploy"**
8. Wait 3-5 minutes for build to complete

**Option B: GitHub Integration** (if you have code in GitHub)

1. Go to **"Settings"** → **"Git Integration"**
2. Connect your GitHub repository
3. Select branch and configure auto-deploy
4. Set build settings as above

#### 3.3: Configure CORS

1. In the function, go to **"Settings"** → **"CORS"**
2. Add allowed origin: `*` (for testing) or your specific domain
3. Save changes

#### 3.4: Get Function URL

1. Go to function **"Settings"**
2. Copy the **Function URL**:
   ```
   https://cloud.appwrite.io/v1/functions/[FUNCTION_ID]/executions
   ```
3. **Save this URL** - you'll need it for the frontend!

---

### Step 4: Test Backend Function

Use PowerShell or any REST client:

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    query = "Samsung Galaxy S24"
    mode = "basic"
    max_results = 3
    sites = @("gsmarena")
} | ConvertTo-Json

Invoke-RestMethod -Uri "YOUR_FUNCTION_URL/search" -Method Post -Headers $headers -Body $body
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

### Step 5: Deploy Frontend (Static Hosting)

#### 5.1: Update API Configuration

1. Open `web/js/config.js`
2. Replace `YOUR_APPWRITE_FUNCTION_URL_HERE` with your actual Function URL:
   ```javascript
   const API_CONFIG = {
       functionUrl: 'https://cloud.appwrite.io/v1/functions/abc123/executions'
   };
   ```
3. Save the file

#### 5.2: Create Static Site

1. In Appwrite Console, click **"Hosting"** in the left sidebar
2. Click **"Create Site"**
3. Enter site name: `scrupwaa` (or any name you like)
4. Click **"Create"**

#### 5.3: Upload Frontend Files

1. In the site settings, click **"Upload Files"**
2. **Drag and drop** or select the entire `web/` folder contents:
   - `index.html`
   - `css/` folder
   - `js/` folder
3. Click **"Upload"**
4. Wait for upload to complete

#### 5.4: Configure Root Document

1. In site **"Settings"**
2. Set **"Root Document"**: `index.html`
3. Save settings

#### 5.5: Get Your Website URL

Your site is now live at:
```
https://scrupwaa.appwrite.global
```

(Replace `scrupwaa` with your chosen site name)

---

## ✅ Verification

### Test the Complete Flow

1. **Open your website URL** in a browser
2. **Enter a search query** (e.g., "iPhone 15")
3. **Select search mode** (Basic or Detailed)
4. **Choose sites** to search
5. **Click "Search Phones"**
6. **Verify results** display correctly
7. **Try exporting JSON** to test export functionality

### Check Function Logs

1. Go to **Functions** → **phone-scraper** → **Logs**
2. Monitor execution logs
3. Check for any errors

---

## 🔧 Alternative: Manual Function Creation

If ZIP upload doesn't work, you can create the function manually:

### Create Individual Files in Console

1. In Function → **Deployments** → **Create Deployment**
2. Choose **"Manual"** option
3. Create each file individually:
   - `function_main.py`
   - `requirements.txt`
   - `universal_search.py`
   - etc.
4. Copy-paste code from your local files

---

## 📦 Creating the ZIP File

### PowerShell Method (Windows)

```powershell
# Navigate to project directory
cd Z:\D\ScrupWaa

# Create ZIP with all necessary files
$files = @(
    "function_main.py",
    "universal_search.py",
    "format_results.py",
    "config.py",
    "requirements.txt",
    "models",
    "scrapers",
    "utils"
)

Compress-Archive -Path $files -DestinationPath function.zip -Force
```

### Verify ZIP Contents

```powershell
# List contents of ZIP
Expand-Archive -Path function.zip -DestinationPath temp_check
Get-ChildItem temp_check -Recurse
Remove-Item temp_check -Recurse -Force
```

Should contain:
```
function_main.py
universal_search.py
format_results.py
config.py
requirements.txt
models/
  __init__.py
  phone.py
scrapers/
  __init__.py
  gsmarena.py
  kimovil.py
  mobiles91.py
utils/
  __init__.py
  adaptive_client.py
  http_client.py
```

---

## 🐛 Troubleshooting

### Function Build Fails

**Check logs**: Functions → phone-scraper → Logs → Build Logs

**Common issues**:
- Missing `requirements.txt`
- Wrong Python version (must be 3.11)
- Import errors (check all files are included)

**Solution**: Recreate ZIP ensuring all files are included

### CORS Errors

**Symptom**: Browser console shows CORS error

**Solution**:
1. Function Settings → CORS
2. Add `*` or your specific domain
3. Save and wait 1-2 minutes

### "API URL Not Configured" Alert

**Symptom**: Alert when clicking search

**Solution**:
1. Edit `web/js/config.js`
2. Add your Function URL
3. Re-upload to Hosting

### Function Times Out

**Symptom**: Request takes too long and fails

**Solutions**:
- Reduce `max_results` in search
- Search fewer sites at once
- Increase timeout in Function Settings

---

## 🔄 Updating Your Deployment

### Update Backend

1. Make changes to your code locally
2. Create new ZIP file
3. Go to Functions → phone-scraper → Deployments
4. Click **"Create Deployment"**
5. Upload new ZIP
6. Deploy

### Update Frontend

1. Edit files in `web/` folder
2. Go to Hosting → Your Site
3. Click **"Upload New Version"**
4. Upload modified files
5. Changes are live immediately!

---

## 💰 Pricing (Free Tier)

Appwrite Cloud Free Tier includes:
- ✅ 75,000 function executions/month
- ✅ 10GB bandwidth
- ✅ Unlimited static hosting
- ✅ SSL certificates (HTTPS)
- ✅ Global CDN

**Enough for:**
- ~2,500 searches per day
- Serving thousands of page views

---

## 🎯 Quick Command Reference

### Create ZIP
```powershell
Compress-Archive -Path function_main.py,universal_search.py,format_results.py,config.py,requirements.txt,models,scrapers,utils -DestinationPath function.zip -Force
```

### Test Function
```powershell
Invoke-RestMethod -Uri "YOUR_FUNCTION_URL/search" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"query":"iPhone 15","mode":"basic","max_results":3,"sites":["gsmarena"]}'
```

---

## 📞 Need Help?

- **Appwrite Docs**: [appwrite.io/docs](https://appwrite.io/docs)
- **Discord**: [discord.gg/appwrite](https://discord.gg/appwrite)
- **Console**: [cloud.appwrite.io/console](https://cloud.appwrite.io/console)

---

## ✨ Summary

**You don't need the CLI!** Everything can be done through the web console:

1. ✅ Create account at cloud.appwrite.io
2. ✅ Create project
3. ✅ Create function → Upload ZIP → Deploy
4. ✅ Configure CORS
5. ✅ Update `web/js/config.js` with Function URL
6. ✅ Create static site → Upload `web/` folder
7. ✅ Done! Your app is live 🎉

**Your URLs:**
- Backend: `https://cloud.appwrite.io/v1/functions/[ID]/executions`
- Frontend: `https://[site-name].appwrite.global`

No custom domain needed - Appwrite provides both URLs automatically!
