# ⚡ Quick Action Guide - What to Do Next

## 🎯 Right Now - Test Your System

### 1. Test Locally (5 minutes)

**Step 1:** Make sure backend is running
```bash
# Check if running
curl http://localhost:8000/health

# If not, start it:
.\start_backend.bat
```

**Step 2:** Open frontend
- Double-click `frontend/index.html` in your browser

**Step 3:** Get a test audio file
- Use any MP3 file you have
- Or download a sample from the competition

**Step 4:** Convert to Base64
```powershell
# In PowerShell:
[Convert]::ToBase64String([IO.File]::ReadAllBytes("your_audio.mp3"))
```

**Step 5:** Test in UI
- Paste Base64 in "Audio Base64 Format" field
- Select language (e.g., "English")
- Enter API key: `sk_test_123456789`
- Endpoint: `http://localhost:8000/api/voice-detection`
- Click "Analyze Voice"

**Expected Result:**
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED" or "HUMAN",
  "confidenceScore": 0.85,
  "explanation": "..."
}
```

---

## 🚀 Next: Deploy to Production

### Recommended: Railway (Easiest)

**Step 1:** Push to GitHub
```bash
git init
git add .
git commit -m "AI Voice Detection System"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

**Step 2:** Deploy on Railway
1. Go to https://railway.app
2. Sign up/login (use GitHub)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway auto-detects Python

**Step 3:** Configure
- **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variable:** `API_KEY=guvi-hcl-voice-ai-2026` (or your key)

**Step 4:** Get your URL
- Railway gives you: `https://your-app.up.railway.app`
- Your API endpoint: `https://your-app.up.railway.app/api/voice-detection`

**Step 5:** Test deployed API
```bash
curl -X POST https://your-app.up.railway.app/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: guvi-hcl-voice-ai-2026" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "YOUR_BASE64_HERE"
  }'
```

---

## 📝 Create Procfile (For Railway/Heroku)

Create a file named `Procfile` in the root directory:

```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## ✅ Final Checklist Before Submission

- [ ] Backend runs locally ✅
- [ ] API responds correctly ✅
- [ ] Base64 audio works ✅
- [ ] API key authentication works ✅
- [ ] Returns correct JSON format ✅
- [ ] Classification works (AI_GENERATED/HUMAN) ✅
- [ ] Confidence score between 0.0-1.0 ✅
- [ ] Explanation provided ✅
- [ ] All 5 languages supported ✅
- [ ] Deployed to production ✅
- [ ] Deployed endpoint tested ✅

---

## 🎯 Submission Format

When submitting to the evaluation portal:

1. **Endpoint URL:**
   ```
   https://your-app.up.railway.app/api/voice-detection
   ```

2. **API Key:**
   ```
   guvi-hcl-voice-ai-2026
   ```
   (Or whatever key you're assigned)

3. **Test with sample audio:**
   - Use the Base64 audio provided in the tester
   - Should return proper classification

---

## 🔧 Quick Fixes

**If backend won't start:**
```bash
cd backend
python main.py
```

**If dependencies missing:**
```bash
.\install_dependencies.bat
```

**If API returns error:**
- Check logs: Look at terminal output
- Check API key matches
- Check Base64 format is correct
- Check audio is valid MP3

**If deployment fails:**
- Check `Procfile` exists
- Check environment variable `API_KEY` is set
- Check start command is correct
- Check logs in Railway dashboard

---

## 📞 Need Help?

1. **Check logs:**
   - Local: Terminal output
   - Railway: Dashboard → Logs tab

2. **Test endpoints:**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # API test
   python test_api.py audio.mp3 English
   ```

3. **Verify installation:**
   ```bash
   python verify_installation.py
   ```

---

## 🎉 You're Ready!

1. ✅ System built
2. ✅ Tested locally
3. ✅ Deployed to production
4. ✅ Ready for evaluation

**Next:** Submit your endpoint URL in the evaluation portal!

Good luck! 🚀



