# AI-Powered Manim Video Iterative Improvement System

An automated system that uses Google's Gemini Pro to iteratively improve Manim mathematical animations until they reach professional quality.

## 🎯 What It Does

1. **Renders** your Manim animation
2. **Analyzes** the video using Gemini Pro AI (visual quality, pacing, pedagogical effectiveness, etc.)
3. **Generates** improved code based on detailed feedback
4. **Re-renders** and repeats until quality target is achieved (default: 8/10)

## 📁 Project Structure

```
manim/
├── test.py                      # Your Manim script (will be modified)
├── video_improver.py            # Main orchestrator script
├── utils.py                     # Helper utilities
├── setup_api.py                 # API setup helper
├── Dockerfile                   # Docker container for Manim
├── prompts/
│   ├── video_analysis_prompt.txt      # Gemini analysis prompt
│   └── code_improvement_prompt.txt    # Gemini code improvement prompt
├── iterations/                  # History of all iterations
│   ├── iteration_01/
│   │   ├── test.py             # Code snapshot
│   │   ├── video_v01.mp4       # Rendered video
│   │   ├── feedback.json       # Analysis feedback
│   │   └── metadata.json       # Iteration metadata
│   └── summary.json            # Overall improvement summary
└── rendered_videos/             # All rendered videos
    ├── video_iteration_01.mp4
    ├── video_iteration_02.mp4
    └── ...
```

## 🚀 Setup

### Prerequisites

1. **Python 3.8+**
2. **Docker** (recommended) or **Manim installed locally**
3. **Gemini API Key** (free from Google AI Studio)

### Step 1: Get Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Create a new API key (it's free!)
3. Copy your API key

### Step 2: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY='your-api-key-here'
```

**Windows Command Prompt:**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**For permanent setup:** Add to Windows System Environment Variables

### Step 3: Install Python Dependencies

```bash
pip install google-generativeai
```

### Step 4: Build Docker Image (if using Docker)

```bash
cd manim
docker build -t manim-container .
```

### Step 5: Test Setup

```bash
python setup_api.py
```

You should see:
```
✓ GEMINI_API_KEY is set in environment
✓ API connection successful!
```

## 📖 Usage

### Basic Usage (with Docker)

```bash
python video_improver.py
```

### Custom Options

```bash
# Specify different script
python video_improver.py --script my_animation.py

# Set max iterations
python video_improver.py --max-iterations 10

# Set target quality score
python video_improver.py --target-score 9.0

# Use local Manim instead of Docker
python video_improver.py --no-docker
```

### Full Example

```bash
python video_improver.py --script test.py --max-iterations 5 --target-score 8.0
```

## 🎬 What Happens During Execution

```
======================================================================
  🚀 STARTING ITERATIVE VIDEO IMPROVEMENT
======================================================================

📹 Rendering video...
  ✓ Video rendered: media/videos/test/480p15/IntegralExplanation.mp4

🔍 Analyzing video with Gemini Pro...
  Uploading video to Gemini...
  Generating analysis...
  ✓ Analysis complete
  Overall score: 6.5/10
  Satisfactory: False

🔧 Generating improved code with Gemini...
  ✓ Improved code generated and validated
  ✓ Script updated for next iteration

======================================================================
  ITERATION 2/5
  Quality Score: 7.2/10
  Progress: [████████████████████████████░░░░░░░░░░░░] 72%
======================================================================

... (continues until satisfied or max iterations)

🎉 Target quality achieved!
   Final score: 8.3/10

======================================================================
  📊 IMPROVEMENT SUMMARY
======================================================================
  Total iterations: 3
  Final score: 8.3/10
  Improvement: +1.8
  Satisfied: True
======================================================================
```

## 📊 Analysis Criteria

Gemini evaluates videos on five dimensions (0-10 scale):

1. **Visual Clarity** - Text readability, color choices, visual organization
2. **Pacing** - Animation speed, transition smoothness, timing
3. **Pedagogical Effectiveness** - Educational clarity, logical progression
4. **Technical Quality** - Animation smoothness, professional appearance
5. **Completeness** - Story completeness, necessary steps shown

## 🔧 Configuration

### Modify Analysis Criteria

Edit `prompts/video_analysis_prompt.txt` to adjust what Gemini looks for in videos.

### Modify Improvement Style

Edit `prompts/code_improvement_prompt.txt` to change how Gemini rewrites code.

### Change Target Score

Default is 8.0/10. Adjust with `--target-score`:
- 7.0 = Good quality (faster)
- 8.0 = Professional quality (balanced)
- 9.0 = Excellent quality (slower, more iterations)

### Max Iterations

Default is 5. Adjust with `--max-iterations`:
- More iterations = more chances to improve
- But diminishing returns after ~5-7 iterations

## 📂 Output Files

### Iterations Directory

Each iteration saves:
- `test.py` - Code snapshot
- `video_vXX.mp4` - Rendered video
- `feedback.json` - Detailed analysis
- `metadata.json` - Score, timestamp, satisfaction status

### Rendered Videos Directory

All rendered videos in one place for easy comparison.

### Summary Report

`iterations/summary.json` contains:
```json
{
  "iterations": [...],
  "total": 3,
  "final_score": 8.3,
  "improvement": 1.8,
  "satisfied": true
}
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"

Run `python setup_api.py` to check your API key setup.

### "Docker rendering failed"

1. Ensure Docker is running
2. Check if image is built: `docker images | grep manim-container`
3. Try building again: `docker build -t manim-container .`

### "Could not find rendered video"

The script looks in `media/` directory. If Manim outputs elsewhere, check your Manim config.

### "Generated code has syntax errors"

Gemini occasionally produces invalid code. The system will:
1. Validate syntax automatically
2. Skip to next iteration if invalid
3. You can manually fix `test.py` and re-run

### "Analysis failed"

- Check internet connection
- Ensure API key is valid
- Video file might be too large (Gemini has limits)

## 🎓 Tips for Best Results

1. **Start with a working script** - The system improves existing code, not broken code
2. **Use descriptive comments** - Helps Gemini understand your intent
3. **Keep scenes modular** - Easier for AI to improve specific parts
4. **Monitor first iteration** - See what kind of feedback Gemini gives
5. **Adjust prompts** - Customize analysis criteria for your needs

## 🔄 Workflow Examples

### Quick Iteration
```bash
# Fast, 3 iterations, target 7.5
python video_improver.py --max-iterations 3 --target-score 7.5
```

### High Quality
```bash
# Thorough, 10 iterations, target 9.0
python video_improver.py --max-iterations 10 --target-score 9.0
```

### Local Development
```bash
# No Docker, use local Manim
python video_improver.py --no-docker
```

## 📈 Performance Notes

- **Time per iteration**: ~2-5 minutes (depends on video complexity)
- **API costs**: Gemini Pro is free for reasonable usage
- **Storage**: Each iteration ~5-20MB (video + code + feedback)

## 🤝 Contributing

Improve the system by:
1. Enhancing prompts in `prompts/`
2. Adding validation in `utils.py`
3. Extending analysis criteria
4. Adding retry logic for failed code generation

## 📝 License

MIT - Use freely for educational and commercial projects

## 🆘 Support

Issues? Check:
1. `python setup_api.py` - API setup
2. Docker logs - `docker logs [container-id]`
3. Iteration feedback - `iterations/iteration_XX/feedback.json`

---

**Built with ❤️ for the Manim community**

Powered by Google Gemini Pro & Manim Community Edition
