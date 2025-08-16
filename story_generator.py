import google.generativeai as genai
from config import GEMINI_API_KEY, STORY_PAGES, MAX_STORY_LENGTH, MAX_CHARACTER_DESCRIPTION

class StoryGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_story(self, prompt):
        """Generate a complete 5-page children's story based on the prompt"""
        try:
            story_prompt = f"""
            Create a delightful 5-page children's story based on this prompt: "{prompt}"
            
            Requirements:
            - Write exactly {STORY_PAGES} pages
            - Each page should be 2-3 sentences, suitable for children aged 4-8
            - Include engaging characters and a clear plot
            - Make it educational and entertaining
            - Use simple, clear language
            
            Format the response as:
            PAGE 1: [story text]
            PAGE 2: [story text]
            PAGE 3: [story text]
            PAGE 4: [story text]
            PAGE 5: [story text]
            
            Keep each page under {MAX_STORY_LENGTH} characters.
            """
            
            response = self.model.generate_content(story_prompt)
            return self._parse_story_pages(response.text)
            
        except Exception as e:
            print(f"Error generating story: {e}")
            return None
    
    def generate_character_description(self, story_text):
        """Generate consistent character descriptions for image generation"""
        try:
            character_prompt = f"""
            Based on this children's story, create a brief character description for image generation:
            
            Story: {story_text[:500]}...
            
            Provide a clear, consistent description of the main characters that can be used to generate images.
            Focus on:
            - Physical appearance (clothing, colors, features)
            - Character personality traits
            - Any distinctive features
            
            Keep it under {MAX_CHARACTER_DESCRIPTION} characters and make it suitable for consistent image generation.
            """
            
            response = self.model.generate_content(character_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating character description: {e}")
            return "A friendly character with bright colors and a warm smile"
    
    def _parse_story_pages(self, story_text):
        """Parse the generated story into individual pages"""
        pages = []
        lines = story_text.split('\n')
        
        for line in lines:
            if line.startswith('PAGE') and ':' in line:
                page_text = line.split(':', 1)[1].strip()
                if page_text:
                    pages.append(page_text)
        
        # Ensure we have exactly 5 pages
        while len(pages) < STORY_PAGES:
            pages.append("The story continues with more adventures...")
        
        return pages[:STORY_PAGES]
