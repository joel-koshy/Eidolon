# Voiceover Setup Guide

## Quick Start

Add AI-generated voiceover narration to your Manim videos using Gemini + ElevenLabs.

## Prerequisites

### 1. Install Python Packages
```bash
pip install elevenlabs google-generativeai
```

### 2. Install ffmpeg
**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Manual):**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH

**Verify installation:**
```bash
ffmpeg -version
```

### 3. Get ElevenLabs API Key
1. Go to https://elevenlabs.io
2. Sign up (free tier available)
3. Go to Profile → API Keys
4. Copy your API key

### 4. Set Environment Variable
```powershell
# Add to Eidolon/.env file
ELEVENLABS_API_KEY=your_key_here

# Or set temporarily
$env:ELEVENLABS_API_KEY="your_key_here"
```

## Usage

### Basic Usage
```bash
python voiceover_generator.py --script test.py --video rendered_videos/video_iteration_01.mp4
```

### Custom Output Directory
```bash
python voiceover_generator.py --script cnn_math_detailed.py --video rendered_videos/video_iteration_01.mp4 --output my_voiceover
```

### Different Voice
```bash
python voiceover_generator.py --script test.py --video video.mp4 --voice pNInz6obpgDQGcFmaJgB
```

## Available Voices

Common professional voices:
- `JBFqnCBsd6RMkjVDRZzb` - George (default, calm narrator)
- `pNInz6obpgDQGcFmaJgB` - Adam (deep, authoritative)
- `EXAVITQu4vr4xnSDxMaL` - Bella (clear, friendly)
- `TxGEqnHWrfWFTfGW9XjX` - Josh (energetic, young)

Find more: https://elevenlabs.io/voice-library

## Pipeline Steps

The system automatically:

1. **Analyzes Manim Code** - Reads your Python script
2. **Generates Script** - Uses Gemini to create narration
3. **Generates Audio** - Uses ElevenLabs to synthesize speech
4. **Merges with Video** - Uses ffmpeg to combine audio + video

## Output Files

```
voiceover_output/
├── narration_script.txt    # Generated script
├── narration_audio.mp3     # Generated audio
└── final_with_voiceover.mp4  # Final video with voiceover
```

## Example Workflow

```bash
# 1. Render your Manim video
python video_improver_mobject.py --script cnn_math_detailed.py --max-iterations 1

# 2. Add voiceover to the rendered video
python voiceover_generator.py \
  --script cnn_math_detailed.py \
  --video rendered_videos/video_iteration_01.mp4 \
  --output cnn_voiceover

# 3. Watch the final video (auto-opens)
# Output: cnn_voiceover/final_with_voiceover.mp4
```

## Programmatic Usage

```python
from voiceover_generator import VoiceoverGenerator

# Initialize
generator = VoiceoverGenerator()

# Optional: Change voice
generator.set_voice("pNInz6obpgDQGcFmaJgB")  # Adam

# Generate voiceover
final_video = generator.generate_voiceover_for_video(
    script_path="test.py",
    video_path="rendered_videos/video_iteration_01.mp4",
    output_dir="my_output"
)

print(f"Final video: {final_video}")
```

## Troubleshooting

### "ELEVENLABS_API_KEY not found"
- Make sure you set the environment variable
- Check `.env` file in Eidolon directory
- Verify with: `echo $env:ELEVENLABS_API_KEY` (PowerShell)

### "ffmpeg not found"
- Install ffmpeg (see Prerequisites)
- Verify: `ffmpeg -version`
- Restart your terminal after installation

### Audio too fast/slow
- The simple version generates continuous narration
- For precise timing, we'll implement the advanced version with per-section synchronization

### Poor audio quality
- Try different voices with `--voice` parameter
- Upgrade to ElevenLabs paid tier for better quality
- Check your internet connection (API calls)

## Cost Estimate

**ElevenLabs Free Tier:**
- 10,000 characters/month
- ~7 minutes of audio
- Good for testing

**Gemini:**
- Free tier: 60 requests/minute
- Script generation costs negligible

## Next Steps

This is the **simple version**. Future enhancements:
- [ ] Precise timing synchronization with `wait()` calls
- [ ] Per-section narration generation
- [ ] Integration into video_improver_mobject.py
- [ ] Background music support
- [ ] Multiple language support
