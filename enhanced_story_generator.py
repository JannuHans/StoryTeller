import google.generativeai as genai
from config import GEMINI_API_KEY, STORY_PAGES, MAX_STORY_LENGTH, MAX_CHARACTER_DESCRIPTION
import random

class EnhancedStoryGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Story themes and elements for variety
        self.story_themes = [
            "friendship and cooperation", "bravery and courage", "kindness and empathy",
            "curiosity and discovery", "perseverance and determination", "imagination and creativity",
            "family and love", "nature and environment", "learning and growth", "adventure and exploration"
        ]
        
        self.story_settings = [
            "enchanted forest", "magical garden", "floating islands", "undersea kingdom",
            "cloud city", "crystal cave", "rainbow valley", "starlight meadow",
            "whispering woods", "golden desert", "frozen wonderland", "tropical paradise"
        ]
        
        self.character_types = [
            "brave little mouse", "curious rabbit", "friendly dragon", "wise owl",
            "playful kitten", "adventurous squirrel", "gentle giant", "magical unicorn",
            "clever fox", "kind bear", "imaginative child", "talking tree"
        ]
    
    def generate_story(self, prompt):
        """Generate a high-quality 5-page children's story based on the prompt"""
        try:
            # Create a comprehensive story prompt
            story_prompt = self._create_comprehensive_story_prompt(prompt)
            
            # Generate the story
            response = self.model.generate_content(story_prompt)
            
            if response and response.text:
                return self._parse_and_enhance_story(response.text, prompt)
            else:
                return self._generate_fallback_story(prompt)
                
        except Exception as e:
            print(f"Error generating story: {e}")
            return self._generate_fallback_story(prompt)
    
    def _create_comprehensive_story_prompt(self, user_prompt):
        """Create a detailed, structured prompt for high-quality story generation"""
        
        # Select random elements for variety
        theme = random.choice(self.story_themes)
        setting = random.choice(self.story_settings)
        character_type = random.choice(self.character_types)
        
        prompt = f"""
        Create a delightful, engaging 5-page children's story that will captivate young readers aged 4-8.
        
        USER REQUEST: "{user_prompt}"
        
        STORY REQUIREMENTS:
        - Theme: {theme}
        - Setting: {setting}
        - Main Character: {character_type}
        - Exactly {STORY_PAGES} pages with clear progression
        - Each page: 3-4 sentences, engaging and descriptive
        - Include dialogue, action, and emotional moments
        - Educational elements woven naturally into the story
        - Positive messages and happy ending
        - Rich vocabulary suitable for children
        
        STORY STRUCTURE:
        PAGE 1: Introduction - Introduce character and setting, establish the situation
        PAGE 2: Challenge - Present a problem or adventure to overcome
        PAGE 3: Action - Show character taking action and meeting helpers
        PAGE 4: Resolution - Character solves the problem or reaches the goal
        PAGE 5: Conclusion - Happy ending with a lesson learned
        
        WRITING STYLE:
        - Vivid descriptions that paint pictures in the mind
        - Engaging dialogue that brings characters to life
        - Rhythmic language with repetition for young readers
        - Emotional moments that children can relate to
        - Magical and whimsical elements that spark imagination
        
        FORMAT YOUR RESPONSE EXACTLY AS:
        PAGE 1: [story text]
        PAGE 2: [story text]
        PAGE 3: [story text]
        PAGE 4: [story text]
        PAGE 5: [story text]
        
        Make each page memorable, educational, and filled with wonder!
        """
        
        return prompt
    
    def _parse_and_enhance_story(self, story_text, original_prompt):
        """Parse the generated story and enhance it if needed"""
        pages = []
        lines = story_text.split('\n')
        
        for line in lines:
            if line.startswith('PAGE') and ':' in line:
                page_text = line.split(':', 1)[1].strip()
                if page_text:
                    # Enhance the page text
                    enhanced_text = self._enhance_page_text(page_text)
                    pages.append(enhanced_text)
        
        # Ensure we have exactly 5 pages
        while len(pages) < STORY_PAGES:
            pages.append(self._generate_fallback_page(len(pages) + 1, original_prompt))
        
        return pages[:STORY_PAGES]
    
    def _enhance_page_text(self, page_text):
        """Enhance individual page text for better quality"""
        # Add more descriptive language if the text is too short
        if len(page_text) < 50:
            enhanced = self._add_descriptive_elements(page_text)
            return enhanced
        return page_text
    
    def _add_descriptive_elements(self, text):
        """Add descriptive elements to make text more engaging"""
        descriptive_phrases = [
            "with bright, twinkling eyes",
            "in a soft, gentle voice",
            "with a warm, friendly smile",
            "in the golden, glowing light",
            "with a sparkle of magic",
            "in the cool, refreshing breeze",
            "with a heart full of joy",
            "in the peaceful, quiet moment"
        ]
        
        if len(text) < 40:
            phrase = random.choice(descriptive_phrases)
            return f"{text} {phrase}."
        
        return text
    
    def _generate_fallback_page(self, page_number, original_prompt):
        """Generate a fallback page if AI generation fails"""
        fallback_pages = [
            f"Once upon a time, in a magical world, there was a brave little hero who dreamed of great adventures. The sun shone brightly overhead, casting golden rays across the land.",
            f"The hero set off on a journey, meeting friendly creatures along the way. Each step brought new discoveries and wonderful surprises that filled the heart with joy.",
            f"Through challenges and obstacles, the hero showed courage and determination. Friends appeared to help, teaching valuable lessons about teamwork and kindness.",
            f"With wisdom and bravery, the hero overcame the final challenge. The victory was sweet, and the whole world celebrated this amazing achievement.",
            f"From that day forward, the hero's story inspired others to follow their dreams. And they all lived happily ever after, in a world filled with magic and wonder."
        ]
        
        if page_number <= len(fallback_pages):
            return fallback_pages[page_number - 1]
        else:
            return "The story continues with more magical adventures and wonderful discoveries."
    
    def generate_character_description(self, story_text, story_prompt):
        """Generate detailed, consistent character descriptions for image generation"""
        try:
            character_prompt = f"""
            Based on this children's story, create a detailed character description for consistent image generation across all pages.
            
            STORY PROMPT: "{story_prompt}"
            STORY TEXT: {story_text[:800]}...
            
            CHARACTER DESCRIPTION REQUIREMENTS:
            - Physical appearance: colors, clothing, size, distinctive features
            - Personality traits: expressions, body language, character quirks
            - Consistent design elements that can be maintained across all illustrations
            - Child-friendly and appealing design
            - Clear enough for an artist to draw consistently
            
            Focus on:
            - Main character's appearance and personality
            - Supporting characters if mentioned
            - Any magical or special features
            - Color scheme and style preferences
            
            Keep the description under {MAX_CHARACTER_DESCRIPTION} characters but make it detailed and specific.
            """
            
            response = self.model.generate_content(character_prompt)
            if response and response.text:
                return response.text.strip()
            else:
                return self._generate_fallback_character_description()
                
        except Exception as e:
            print(f"Error generating character description: {e}")
            return self._generate_fallback_character_description()
    
    def _generate_fallback_character_description(self):
        """Generate a fallback character description"""
        fallback_descriptions = [
            "A friendly, round-faced character with bright blue eyes, wearing colorful clothing in warm tones. Always smiling with a cheerful expression, medium-sized with soft, rounded features.",
            "A brave little hero with golden fur, bright green eyes, and a red cape. Small and determined, with a confident stance and friendly, encouraging smile.",
            "A magical creature with sparkly wings, pastel colors, and a gentle, wise expression. Medium-sized with flowing, ethereal features and warm, inviting eyes."
        ]
        
        return random.choice(fallback_descriptions)
    
    def generate_story_title(self, story_pages, original_prompt):
        """Generate an engaging title for the story"""
        try:
            title_prompt = f"""
            Create an engaging, memorable title for this children's story.
            
            STORY PROMPT: "{original_prompt}"
            STORY CONTENT: {story_pages[0][:200]}...
            
            TITLE REQUIREMENTS:
            - Catchy and memorable
            - Appropriate for children aged 4-8
            - Reflects the main theme or adventure
            - 3-8 words maximum
            - Include the main character's name if possible
            - Make it sound magical and exciting
            
            Return only the title, nothing else.
            """
            
            response = self.model.generate_content(title_prompt)
            if response and response.text:
                title = response.text.strip()
                # Clean up the title
                title = title.replace('"', '').replace("'", "").strip()
                if len(title) > 50:
                    title = title[:50] + "..."
                return title
            else:
                return self._generate_fallback_title(original_prompt)
                
        except Exception as e:
            print(f"Error generating title: {e}")
            return self._generate_fallback_title(original_prompt)
    
    def _generate_fallback_title(self, original_prompt):
        """Generate a fallback title based on the prompt"""
        words = original_prompt.split()[:5]
        title = " ".join(words).capitalize()
        if len(title) > 40:
            title = title[:40] + "..."
        return title or "A Magical Adventure"
