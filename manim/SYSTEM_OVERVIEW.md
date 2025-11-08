# System Overview: AI-Powered Manim Video Improvement

## 🎯 Purpose

Automatically improve Manim mathematical animations through iterative AI-powered analysis and code generation until professional quality is achieved.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO IMPROVER LOOP                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │   1. RENDER VIDEO                 │
        │   - Docker or Local Manim         │
        │   - Generate MP4 from test.py     │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │   2. ANALYZE WITH GEMINI PRO      │
        │   - Upload video                  │
        │   - Get structured feedback       │
        │   - Score: 0-10 on 5 criteria     │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │   3. CHECK SATISFACTION           │
        │   - Score >= 8.0? → DONE ✓        │
        │   - Max iterations? → DONE ⚠      │
        │   - Otherwise → Continue          │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │   4. IMPROVE CODE WITH GEMINI     │
        │   - Send current code + feedback  │
        │   - Get complete rewritten code   │
        │   - Validate syntax & structure   │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │   5. UPDATE SCRIPT                │
        │   - Write new code to test.py     │
        │   - Save iteration history        │
        └───────────────┬───────────────────┘
                        │
                        └──────> LOOP BACK TO STEP 1
```

## 📦 Components

### Core Scripts

1. **`video_improver.py`** (445 lines)
   - Main orchestrator
   - Manages the entire improvement loop
   - Handles rendering, analysis, and code improvement
   - CLI interface with argparse

2. **`utils.py`** (250 lines)
   - Helper functions
   - Code validation (syntax, structure)
   - JSON extraction from text
   - File management utilities
   - Progress display

3. **`setup_api.py`** (83 lines)
   - API key verification
   - Connection testing
   - Setup instructions

### Prompt Templates

4. **`prompts/video_analysis_prompt.txt`**
   - Instructs Gemini how to analyze videos
   - Defines 5 analysis criteria
   - Specifies JSON output format

5. **`prompts/code_improvement_prompt.txt`**
   - Instructs Gemini how to rewrite code
   - Emphasizes syntax correctness
   - Maintains educational intent

### Documentation

6. **`README_VIDEO_IMPROVER.md`** (308 lines)
   - Comprehensive documentation
   - Setup instructions
   - Usage examples
   - Troubleshooting guide

7. **`QUICKSTART.md`** (86 lines)
   - 5-minute setup guide
   - Essential commands only
   - Quick troubleshooting

8. **`SYSTEM_OVERVIEW.md`** (this file)
   - Architecture overview
   - Component descriptions
   - Data flow diagrams

## 📊 Data Flow

```
INPUT: test.py (Manim script)
   │
   ├─> Docker/Manim ─> video.mp4
   │
   ├─> Gemini Pro ─> feedback.json
   │                  {
   │                    "overall_score": 6.5,
   │                    "visual_clarity": {...},
   │                    "priority_improvements": [...]
   │                  }
   │
   ├─> Gemini Pro ─> improved_code.py
   │
   └─> Write back to test.py
       │
       └─> LOOP
```

## 🗂️ Directory Structure

```
manim/
├── Core Scripts
│   ├── video_improver.py      # Main orchestrator
│   ├── utils.py                # Helper functions
│   └── setup_api.py            # API setup tool
│
├── Configuration
│   ├── Dockerfile              # Manim container
│   ├── .devcontainer/          # VS Code devcontainer
│   └── prompts/                # AI prompt templates
│       ├── video_analysis_prompt.txt
│       └── code_improvement_prompt.txt
│
├── Documentation
│   ├── README_VIDEO_IMPROVER.md
│   ├── QUICKSTART.md
│   └── SYSTEM_OVERVIEW.md
│
├── Working Files
│   └── test.py                 # Manim script (modified in-place)
│
├── Output (git-ignored)
│   ├── media/                  # Manim rendering output
│   ├── rendered_videos/        # Copies of all videos
│   │   ├── video_iteration_01.mp4
│   │   ├── video_iteration_02.mp4
│   │   └── ...
│   └── iterations/             # Complete history
│       ├── iteration_01/
│       │   ├── test.py         # Code snapshot
│       │   ├── video_v01.mp4   # Video copy
│       │   ├── feedback.json   # AI analysis
│       │   └── metadata.json   # Timestamp, score
│       └── summary.json        # Overall report
│
└── Cache (git-ignored)
    ├── __pycache__/
    └── .cache/
```

## 🔄 Iteration Lifecycle

### Iteration N

```
START
  │
  ├─ Read current test.py
  │
  ├─ Render video → media/
  │
  ├─ Copy video → rendered_videos/video_iteration_N.mp4
  │
  ├─ Upload video to Gemini
  │
  ├─ Get feedback (JSON)
  │
  ├─ Save iteration data:
  │   ├─ iterations/iteration_N/test.py
  │   ├─ iterations/iteration_N/video_vN.mp4
  │   ├─ iterations/iteration_N/feedback.json
  │   └─ iterations/iteration_N/metadata.json
  │
  ├─ Check score >= target? 
  │   YES → END (success)
  │   NO  → Continue
  │
  ├─ Check iteration >= max?
  │   YES → END (max reached)
  │   NO  → Continue
  │
  ├─ Send code + feedback to Gemini
  │
  ├─ Get improved code
  │
  ├─ Validate syntax & structure
  │   FAIL → END (validation error)
  │   PASS → Continue
  │
  ├─ Write improved code to test.py
  │
  └─ NEXT ITERATION
```

## 🎛️ Configuration Options

### Command Line Arguments

```bash
--script <path>           # Path to Manim script (default: test.py)
--max-iterations <int>    # Max iterations (default: 5)
--target-score <float>    # Target quality 0-10 (default: 8.0)
--no-docker               # Use local Manim instead of Docker
```

### Environment Variables

```bash
GEMINI_API_KEY            # Required: Google Gemini API key
```

### Prompt Templates

- Edit `prompts/video_analysis_prompt.txt` to change analysis criteria
- Edit `prompts/code_improvement_prompt.txt` to change improvement style

## 📈 Quality Metrics

### Analysis Dimensions (0-10 each)

1. **Visual Clarity**
   - Text readability
   - Color choices
   - Visual organization

2. **Pacing**
   - Animation speed
   - Transition smoothness
   - Timing balance

3. **Pedagogical Effectiveness**
   - Educational clarity
   - Logical progression
   - Student comprehension

4. **Technical Quality**
   - Animation smoothness
   - No glitches/overlaps
   - Professional appearance

5. **Completeness**
   - Complete story
   - All necessary steps
   - Proper conclusion

**Overall Score** = Average of 5 dimensions

**Satisfactory** = Overall score ≥ 8.0

## 🔐 Security Considerations

1. **API Key Storage**
   - Stored in environment variables only
   - Never committed to git
   - Not logged or printed in full

2. **Code Validation**
   - All generated code validated before execution
   - Syntax checking via Python AST
   - Structure validation (required imports, classes)

3. **Docker Isolation**
   - Manim runs in isolated container
   - Limited file system access
   - No network access during rendering

## 🚀 Performance Characteristics

### Time Complexity

- **Per Iteration**: 2-5 minutes
  - Rendering: 30-120 seconds (depends on complexity)
  - Upload: 10-30 seconds (depends on video size)
  - Analysis: 20-60 seconds
  - Code generation: 20-60 seconds

- **Full Run (5 iterations)**: 10-25 minutes

### Space Complexity

- **Per Iteration**: 5-20 MB
  - Video: 3-15 MB
  - Code: <100 KB
  - Feedback JSON: <50 KB

- **Full Run (5 iterations)**: 25-100 MB

### API Costs

- **Gemini Pro**: Free tier (as of 2024)
  - 60 requests per minute
  - 1,500 requests per day
  - Sufficient for ~750 videos per day

## 🔧 Extension Points

### Adding New Analysis Criteria

1. Edit `prompts/video_analysis_prompt.txt`
2. Add new criterion to JSON schema
3. Update `utils.py` if needed for new validations

### Supporting Multiple Scene Classes

1. Modify `video_improver.py` to accept scene name parameter
2. Update Docker command to use scene name
3. Update validation in `utils.py`

### Adding Retry Logic

1. Add retry decorator to `improve_code()` method
2. Implement fix-up prompts for common errors
3. Add exponential backoff for API calls

### Integration with CI/CD

```yaml
# Example GitHub Action
- name: Improve Video
  run: python video_improver.py --max-iterations 3
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

## 🐛 Error Handling

### Graceful Degradation

1. **Rendering fails** → Stop iteration, save progress
2. **Analysis fails** → Stop iteration, save progress
3. **Code generation fails** → Stop iteration, keep current code
4. **Validation fails** → Skip iteration, try again
5. **Max iterations reached** → End with best result

### Recovery Mechanisms

- All iterations saved incrementally
- Can restart from any iteration
- Original code preserved in `iteration_01/`

## 📊 Success Metrics

### System Success

- ✓ Score improvement over iterations
- ✓ Reaches target score (8.0+)
- ✓ No syntax errors in generated code
- ✓ All iterations saved correctly

### Video Success

- ✓ Improved visual clarity
- ✓ Better pacing and timing
- ✓ Enhanced educational value
- ✓ Professional appearance

## 🎓 Design Principles

1. **Iterative Improvement** - Small improvements compound
2. **Explicit Validation** - Validate everything before use
3. **Complete History** - Never lose work
4. **Graceful Failure** - Save progress before failing
5. **Clear Feedback** - User always knows what's happening
6. **Configurability** - Easy to adjust to needs

---

**System Version**: 1.0  
**Last Updated**: 2024-11  
**Maintainer**: Eidolon Project
