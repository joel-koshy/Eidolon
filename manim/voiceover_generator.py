"""
Voiceover Generator for Manim Videos
Generates narration script and adds ElevenLabs voiceover to videos
"""

import os
import json
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import subprocess
from pathlib import Path


class VoiceoverGenerator:
    def __init__(self, gemini_api_key=None, elevenlabs_api_key=None):
        """Initialize with API keys"""
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found")
        if not self.elevenlabs_api_key:
            raise ValueError("ELEVENLABS_API_KEY not found")
        
        # Initialize Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        # Initialize ElevenLabs
        self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
        
        # Default voice (can be changed)
        self.voice_id = "JBFqnCBsd6RMkjVDRZzb"  # George - calm, professional narrator
        
        print("✓ VoiceoverGenerator initialized")
        print(f"  Gemini: gemini-2.0-flash-exp")
        print(f"  ElevenLabs: Voice ID {self.voice_id}")
    
    def analyze_manim_code(self, script_path):
        """Read and return Manim code for analysis"""
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return code
    
    def generate_narration_script(self, manim_code, topic=None):
        """Use Gemini to generate narration script from Manim code"""
        print("\n🤖 Generating narration script with Gemini...")
        
        prompt = f"""You are an expert educational narrator creating voiceover scripts for mathematical animation videos.

Analyze this Manim code and generate a natural, engaging narration script that explains what's happening in the video.

REQUIREMENTS:
1. Write in a conversational, educational tone (like 3Blue1Brown)
2. Explain the mathematical concepts clearly
3. Match the flow of the code sections
4. Keep it concise but informative
5. Use natural pauses for comprehension
6. Don't mention "the animation" or "the video" - speak as if teaching directly
7. Focus on the math/concepts, not the code

MANIM CODE:
{manim_code}

Generate a complete narration script that flows naturally from start to finish. Write only the narration text, nothing else."""

        response = self.gemini_model.generate_content(prompt)
        script = response.text.strip()
        
        print(f"✓ Generated {len(script)} characters of narration")
        return script
    
    def save_script(self, script, output_path):
        """Save narration script to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✓ Script saved: {output_path}")
    
    def generate_audio(self, script, output_path):
        """Generate audio from script using ElevenLabs"""
        print(f"\n🎙️ Generating audio with ElevenLabs...")
        print(f"  Voice ID: {self.voice_id}")
        print(f"  Text length: {len(script)} characters")
        
        try:
            # Use text_to_speech.convert method
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=script,
                model_id="eleven_turbo_v2_5"  # Free tier model
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)
            
            # Save audio
            with open(output_path, 'wb') as f:
                f.write(audio_bytes)
            
            print(f"✓ Audio generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Audio generation failed: {e}")
            return False
    
    def merge_audio_video(self, video_path, audio_path, output_path):
        """Merge audio with video using ffmpeg"""
        print(f"\n🎬 Merging audio with video...")
        print(f"  Video: {video_path}")
        print(f"  Audio: {audio_path}")
        
        # Check if ffmpeg is available
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ ffmpeg not found. Please install ffmpeg:")
            print("  Windows: choco install ffmpeg  (or download from ffmpeg.org)")
            return False
        
        # Merge command
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",  # Copy video codec (no re-encode)
            "-c:a", "aac",   # Encode audio as AAC
            "-map", "0:v:0", # Use video from first input
            "-map", "1:a:0", # Use audio from second input
            "-shortest",     # End when shortest stream ends
            "-y",            # Overwrite output
            output_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✓ Video with voiceover: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ ffmpeg failed: {e.stderr}")
            return False
    
    def generate_voiceover_for_video(self, script_path, video_path, output_dir="voiceover_output"):
        """Complete pipeline: generate script, audio, and merge with video"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # File paths
        script_file = output_dir / "narration_script.txt"
        audio_file = output_dir / "narration_audio.mp3"
        final_video = output_dir / f"final_with_voiceover.mp4"
        
        print("="*70)
        print("  🎙️ VOICEOVER GENERATION PIPELINE")
        print("="*70)
        
        # Step 1: Analyze Manim code
        print("\n📄 Step 1: Analyzing Manim code...")
        manim_code = self.analyze_manim_code(script_path)
        print(f"✓ Read {len(manim_code)} characters of code")
        
        # Step 2: Generate narration script
        print("\n📝 Step 2: Generating narration script...")
        script = self.generate_narration_script(manim_code)
        self.save_script(script, script_file)
        
        # Step 3: Generate audio
        print("\n🎵 Step 3: Generating audio...")
        audio_success = self.generate_audio(script, audio_file)
        if not audio_success:
            return None
        
        # Step 4: Merge with video
        print("\n🎬 Step 4: Merging audio with video...")
        merge_success = self.merge_audio_video(video_path, audio_file, final_video)
        if not merge_success:
            return None
        
        print("\n" + "="*70)
        print("  ✅ VOICEOVER GENERATION COMPLETE")
        print("="*70)
        print(f"\n📁 Output files:")
        print(f"  Script: {script_file}")
        print(f"  Audio: {audio_file}")
        print(f"  Final Video: {final_video}")
        
        return str(final_video)
    
    def set_voice(self, voice_id):
        """Change the ElevenLabs voice"""
        self.voice_id = voice_id
        print(f"✓ Voice changed to: {voice_id}")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Add ElevenLabs voiceover to Manim videos")
    parser.add_argument("--script", required=True, help="Path to Manim script (.py)")
    parser.add_argument("--video", required=True, help="Path to rendered video (.mp4)")
    parser.add_argument("--output", default="voiceover_output", help="Output directory")
    parser.add_argument("--voice", default="JBFqnCBsd6RMkjVDRZzb", help="ElevenLabs voice ID")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = VoiceoverGenerator()
    generator.set_voice(args.voice)
    
    # Generate voiceover
    final_video = generator.generate_voiceover_for_video(
        script_path=args.script,
        video_path=args.video,
        output_dir=args.output
    )
    
    if final_video:
        print(f"\n🎉 Success! Open video: {final_video}")
        
        # Auto-open video
        import platform
        if platform.system() == "Windows":
            os.startfile(final_video)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", final_video])
        else:  # Linux
            subprocess.run(["xdg-open", final_video])


if __name__ == "__main__":
    main()
