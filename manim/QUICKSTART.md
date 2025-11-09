# 🚀 Quick Start Guide

Get the video improvement system running in 5 minutes!

## Step 1: Get Gemini API Key (2 minutes)

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 2: Set API Key (30 seconds)

Open PowerShell in this directory and run:

```powershell
$env:GEMINI_API_KEY='paste-your-key-here'
```

## Step 3: Install Dependencies (1 minute)

```powershell
pip install google-generativeai
```

## Step 4: Build Docker Image (1-2 minutes)

```powershell
docker build -t manim-container .
```

## Step 5: Test Setup (30 seconds)

```powershell
python setup_api.py
```

You should see "✓ API connection successful!"

## Step 6: Run the System! 🎉

```powershell
python video_improver.py
```

That's it! The system will now:
- Render your video
- Analyze it with AI
- Improve the code
- Repeat until satisfied

## What to Expect

- First iteration: ~2-3 minutes
- Total time: 10-15 minutes for 5 iterations
- All videos saved in `rendered_videos/`
- All history saved in `iterations/`

## Troubleshooting

**API key not found?**
```powershell
python setup_api.py
```

**Docker not working?**
```powershell
# Use local Manim instead
python video_improver.py --no-docker
```

**Want faster results?**
```powershell
python video_improver.py --max-iterations 3 --target-score 7.5
```

## Next Steps

Read `README_VIDEO_IMPROVER.md` for:
- Full documentation
- Configuration options
- Advanced usage
- Troubleshooting

---

**Happy animating! 🎬✨**
