# 🎯 Appwrite Deployment - Quick Reference

## 📦 What You Have Now

✅ **Backend Function** - Serverless Python scraper (no Flask)  
✅ **Frontend Site** - Static HTML/CSS/JS in `web/` folder  
✅ **Docker Configuration** - Ready for Appwrite deployment  
✅ **Simplified Dependencies** - HTTP client only  
✅ **Complete Documentation** - See APPWRITE_DEPLOY.md

---

## 🚀 Deploy in 6 Commands

```bash
# 1. Install CLI
npm install -g appwrite-cli

# 2. Login
appwrite login

# 3. Initialize (from project directory)
cd z:\D\ScrupWaa
appwrite init project

# 4. Update appwrite.json with Project ID
# Edit file and add your project ID

# 5. Deploy backend
appwrite deploy function

# 6. Deploy frontend via Console
# Upload web/ folder at cloud.appwrite.io
```

---

## ⚙️ Before Deployment

### 1. Update appwrite.json
```json
{
  "projectId": "YOUR_PROJECT_ID_HERE",  ← Add this!
  ...
}
```

### 2. After Backend Deploys
Update `web/js/config.js`:
```javascript
functionUrl: 'YOUR_APPWRITE_FUNCTION_URL_HERE'  ← Add this!
```

---

## 🌐 Appwrite Provides These URLs

**No domain purchase needed!**

1. **Function API**: `https://cloud.appwrite.io/v1/functions/[ID]/executions`
2. **Website**: `https://[your-site-name].appwrite.global`

---

## ✅ Post-Deployment Checklist

### Backend
- [ ] Function deployed (green status in Console)
- [ ] CORS enabled (Settings → CORS → add `*`)
- [ ] Test with curl (see APPWRITE_DEPLOY.md)

### Frontend  
- [ ] Site deployed and live
- [ ] Function URL updated in `web/js/config.js`
- [ ] Search form works
- [ ] Results display correctly

---

## 🧪 Quick Test

```bash
# Test backend
curl -X POST "YOUR_FUNCTION_URL/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"iPhone 15","mode":"basic","max_results":3,"sites":["gsmarena"]}'

# Expected: {"success":true,"data":{...}}
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `function_main.py` | Appwrite Function handler |
| `Dockerfile` | Container configuration |
| `appwrite.json` | Deployment settings |
| `web/` | Static frontend files |
| `web/js/config.js` | **UPDATE THIS!** |
| `requirements.txt` | Python dependencies |

---

## 🔧 Common Issues

### "Function build failed"
→ Check Dockerfile and requirements.txt syntax

### "CORS error"  
→ Enable CORS in Function settings

### "API URL not configured"
→ Update `web/js/config.js` with Function URL

### "No results"
→ Check Function logs (Console → Functions → Logs)

---

## 📚 Documentation

- **Full Guide**: `APPWRITE_DEPLOY.md`
- **Summary**: `DEPLOYMENT_README.md`
- **Appwrite Docs**: https://appwrite.io/docs

---

## 💰 Free Tier Limits

- ✅ 75K function executions/month
- ✅ 10GB bandwidth
- ✅ Unlimited static hosting
- ✅ No credit card required

**Perfect for testing and small projects!**

---

## 🎉 You're Ready!

Follow the 6 commands above, update the 2 config files, and you're live!

**Need help?** See `APPWRITE_DEPLOY.md` for detailed walkthrough.
