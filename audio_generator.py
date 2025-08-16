from gtts import gTTS
import os
import tempfile
from config import AUDIO_LANGUAGE

class AudioGenerator:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.audio_files = []
    
    def generate_story_audio(self, story_pages, story_title="My Storybook"):
        """Generate audio narration for the entire storybook"""
        try:
            # Create full story text
            full_story = self._combine_story_text(story_pages, story_title)
            
            # Generate audio file
            audio_filename = os.path.join(self.temp_dir, f"{story_title.replace(' ', '_')}_audio.mp3")
            
            # Create TTS object
            tts = gTTS(text=full_story, lang=AUDIO_LANGUAGE, slow=False)
            
            # Save audio file
            tts.save(audio_filename)
            
            self.audio_files.append(audio_filename)
            return audio_filename
            
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
    
    def generate_page_audio(self, page_text, page_number):
        """Generate audio for a single page"""
        try:
            audio_filename = os.path.join(self.temp_dir, f"page_{page_number}_audio.mp3")
            
            # Create TTS object for the page
            tts = gTTS(text=page_text, lang=AUDIO_LANGUAGE, slow=False)
            
            # Save audio file
            tts.save(audio_filename)
            
            self.audio_files.append(audio_filename)
            return audio_filename
            
        except Exception as e:
            print(f"Error generating page audio: {e}")
            return None
    
    def _combine_story_text(self, story_pages, story_title):
        """Combine all story pages into one text for full audio narration"""
        full_text = f"Welcome to {story_title}. "
        full_text += "Let's begin our magical story. "
        
        for i, page_text in enumerate(story_pages, 1):
            full_text += f"Page {i}: {page_text} "
        
        full_text += "The end. Thank you for reading with us!"
        return full_text
    
    def get_audio_file_path(self, filename):
        """Get the full path to an audio file"""
        return os.path.join(self.temp_dir, filename)
    
    def cleanup_audio_files(self):
        """Clean up temporary audio files"""
        try:
            for audio_file in self.audio_files:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            self.audio_files.clear()
        except Exception as e:
            print(f"Error cleaning up audio files: {e}")
    
    def get_audio_duration_estimate(self, text):
        """Estimate audio duration based on text length (rough estimate)"""
        # Average speaking rate is about 150 words per minute
        words = len(text.split())
        minutes = words / 150
        return minutes
    
    def create_audio_controls_html(self, audio_file_path):
        """Create HTML audio controls for the Streamlit app"""
        if not audio_file_path or not os.path.exists(audio_file_path):
            return ""
        
        html_code = f"""
        <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #007bff;">
            <h4 style="margin: 0 0 10px 0; color: #007bff;">🎵 Story Audio Narration</h4>
            <audio controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{self._file_to_base64(audio_file_path)}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            <p style="margin: 10px 0 0 0; font-size: 12px; color: #666;">
                Listen to the complete story narration
            </p>
        </div>
        """
        return html_code
    
    def _file_to_base64(self, file_path):
        """Convert audio file to base64 for HTML embedding"""
        try:
            import base64
            with open(file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                return base64.b64encode(audio_data).decode('utf-8')
        except Exception as e:
            print(f"Error converting audio file to base64: {e}")
            return ""
