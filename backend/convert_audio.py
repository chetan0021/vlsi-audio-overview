"""
Convert MP4 video files to MP3 audio files
Extracts audio track from video files in voice_samples/zoya/
Uses pydub which is already installed
"""
from pathlib import Path
from pydub import AudioSegment

def convert_mp4_to_mp3(input_path: str, output_path: str):
    """Convert MP4 video to MP3 audio using pydub"""
    try:
        print(f"Converting {input_path}...")
        # Load the video file (pydub can extract audio)
        audio = AudioSegment.from_file(input_path, format="mp4")
        # Export as MP3
        audio.export(output_path, format="mp3", bitrate="192k")
        print(f"✅ Converted to {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error converting {input_path}: {e}")
        print(f"   Note: pydub requires ffmpeg to be installed")
        return False

def main():
    """Convert all MP4 files in voice_samples/zoya/ to MP3"""
    voice_samples_dir = Path("voice_samples/zoya")
    
    if not voice_samples_dir.exists():
        print(f"❌ Directory not found: {voice_samples_dir}")
        return
    
    # Find all MP4 files
    mp4_files = list(voice_samples_dir.glob("*.mp4"))
    
    if not mp4_files:
        print("✅ No MP4 files found to convert")
        # List all audio files
        audio_files = list(voice_samples_dir.glob("*.mp3")) + list(voice_samples_dir.glob("*.wav"))
        print(f"\n📁 Found {len(audio_files)} audio files in {voice_samples_dir}:")
        for f in audio_files:
            print(f"   - {f.name}")
        return
    
    print(f"Found {len(mp4_files)} MP4 files to convert\n")
    
    converted = 0
    skipped = 0
    failed = 0
    
    for mp4_file in mp4_files:
        # Create output filename (replace .mp4 with .mp3)
        mp3_file = mp4_file.with_suffix('.mp3')
        
        # Skip if MP3 already exists
        if mp3_file.exists():
            print(f"⏭️  Skipping {mp4_file.name} (MP3 already exists)")
            skipped += 1
            continue
        
        # Convert
        if convert_mp4_to_mp3(str(mp4_file), str(mp3_file)):
            converted += 1
        else:
            failed += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Converted: {converted}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   ❌ Failed: {failed}")
    print(f"\n📁 Audio files location: {voice_samples_dir}")
    
    # List all audio files
    audio_files = list(voice_samples_dir.glob("*.mp3")) + list(voice_samples_dir.glob("*.wav"))
    print(f"\n🎵 Total audio files: {len(audio_files)}")

if __name__ == "__main__":
    main()
