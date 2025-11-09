"""
Intelligent Render Caching System

Implements code-based asset caching to avoid redundant renders.
Uses SHA-256 hashing of source code to detect if re-rendering is needed.
"""

import hashlib
import json
import shutil
from pathlib import Path
from typing import Optional, Dict


class RenderCache:
    """Manages cached renders based on code hashes."""
    
    def __init__(self, cache_dir: str = "render_cache"):
        """
        Initialize render cache.
        
        Args:
            cache_dir: Directory to store cache metadata
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "cache_index.json"
        self.cache_index = self._load_cache_index()
    
    def _load_cache_index(self) -> Dict:
        """Load cache index from disk."""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache_index(self):
        """Save cache index to disk."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache_index, f, indent=2)
    
    def compute_code_hash(self, code: str) -> str:
        """
        Compute SHA-256 hash of code.
        
        Args:
            code: Python code as string
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(code.encode('utf-8')).hexdigest()
    
    def get_cached_video(self, code: str, scene_name: str) -> Optional[str]:
        """
        Check if a cached video exists for this code.
        
        Args:
            code: Python code as string
            scene_name: Name of the scene
            
        Returns:
            Path to cached video or None if not found
        """
        code_hash = self.compute_code_hash(code)
        cache_key = f"{scene_name}_{code_hash}"
        
        if cache_key in self.cache_index:
            cached_path = self.cache_index[cache_key]["video_path"]
            if Path(cached_path).exists():
                print(f"✓ Cache HIT! Using cached video: {cached_path}")
                return cached_path
            else:
                # Cache entry exists but video missing - clean up
                del self.cache_index[cache_key]
                self._save_cache_index()
        
        print(f"✗ Cache MISS. Need to render.")
        return None
    
    def store_cached_video(self, code: str, scene_name: str, video_path: str) -> str:
        """
        Store a newly rendered video in cache.
        
        Args:
            code: Python code as string
            scene_name: Name of the scene
            video_path: Path to rendered video
            
        Returns:
            Path where video was cached
        """
        code_hash = self.compute_code_hash(code)
        cache_key = f"{scene_name}_{code_hash}"
        
        # Copy video to cache directory
        cached_video_path = self.cache_dir / f"{cache_key}.mp4"
        shutil.copy2(video_path, cached_video_path)
        
        # Update cache index
        self.cache_index[cache_key] = {
            "scene_name": scene_name,
            "code_hash": code_hash,
            "video_path": str(cached_video_path),
            "original_path": video_path
        }
        self._save_cache_index()
        
        print(f"✓ Video cached: {cached_video_path}")
        return str(cached_video_path)
    
    def clear_cache(self):
        """Clear all cached videos and index."""
        for cache_entry in self.cache_index.values():
            video_path = Path(cache_entry["video_path"])
            if video_path.exists():
                video_path.unlink()
        
        self.cache_index = {}
        self._save_cache_index()
        print("✓ Cache cleared")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        total_entries = len(self.cache_index)
        valid_entries = sum(
            1 for entry in self.cache_index.values()
            if Path(entry["video_path"]).exists()
        )
        
        total_size = sum(
            Path(entry["video_path"]).stat().st_size
            for entry in self.cache_index.values()
            if Path(entry["video_path"]).exists()
        )
        
        return {
            "total_entries": total_entries,
            "valid_entries": valid_entries,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cache_hits_potential": valid_entries
        }


# CLI for cache management
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage render cache")
    parser.add_argument("--clear", action="store_true", help="Clear cache")
    parser.add_argument("--stats", action="store_true", help="Show cache statistics")
    
    args = parser.parse_args()
    
    cache = RenderCache()
    
    if args.clear:
        cache.clear_cache()
    elif args.stats:
        stats = cache.get_cache_stats()
        print("\n" + "="*50)
        print("RENDER CACHE STATISTICS")
        print("="*50)
        print(f"Total entries: {stats['total_entries']}")
        print(f"Valid entries: {stats['valid_entries']}")
        print(f"Total size: {stats['total_size_mb']} MB")
        print(f"Potential cache hits: {stats['cache_hits_potential']}")
        print("="*50)
    else:
        print("Use --stats to view cache info or --clear to clear cache")
