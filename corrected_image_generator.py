import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import io
import base64
import time
import random
from config import GEMINI_API_KEY, IMAGE_WIDTH, IMAGE_HEIGHT

class CorrectedImageGenerator:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Professional color schemes for children's books
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'warm': '#C73E1D',
            'cool': '#4ECDC4',
            'vibrant': '#FF6B6B',
            'pastel': '#FFB3BA',
            'sky': '#87CEEB',
            'grass': '#90EE90',
            'sun': '#FFD700'
        }
    
    def generate_page_image(self, page_text, character_description, page_number, story_context=""):
        """Generate ONLY an illustration (no text) for a story page"""
        try:
            # Create a clean illustration without any text
            return self._create_clean_illustration(page_text, character_description, page_number)
            
        except Exception as e:
            print(f"Error generating image for page {page_number}: {e}")
            return self._create_simple_fallback(page_number)
    
    def _create_clean_illustration(self, page_text, character_description, page_number):
        """Create a clean illustration without text - only visual elements"""
        try:
            # Create the main canvas
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Add professional border
            self._add_professional_border(draw, IMAGE_WIDTH, IMAGE_HEIGHT)
            
            # Create the main illustration area (full image minus border)
            illustration_x = 20
            illustration_y = 20
            illustration_width = IMAGE_WIDTH - 40
            illustration_height = IMAGE_HEIGHT - 40
            
            # Generate the illustration content
            self._create_page_illustration(draw, illustration_x, illustration_y, 
                                        illustration_width, illustration_height, 
                                        page_text, character_description, page_number)
            
            # Add page number (small, unobtrusive)
            self._add_page_number(draw, IMAGE_WIDTH, IMAGE_HEIGHT, page_number)
            
            # Apply professional effects
            img = self._apply_professional_effects(img)
            
            return img
            
        except Exception as e:
            print(f"Error creating clean illustration: {e}")
            return self._create_simple_fallback(page_number)
    
    def _add_professional_border(self, draw, width, height):
        """Add professional border to the image"""
        border_color = self.colors['primary']
        border_width = 3
        
        # Main border
        draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=border_width)
        
        # Inner decorative border
        inner_border = border_width * 2
        draw.rectangle([inner_border, inner_border, width-inner_border, height-inner_border], 
                      outline=self.colors['secondary'], width=2)
    
    def _create_page_illustration(self, draw, x, y, width, height, page_text, character_description, page_number):
        """Create the main illustration content without text"""
        try:
            # Create background for illustration area
            draw.rectangle([x, y, x + width, y + height], 
                          fill='#ffffff', outline=self.colors['accent'], width=2)
            
            # Add dynamic background based on page number
            self._create_dynamic_background(draw, x + 5, y + 5, width - 10, height - 10, page_number)
            
            # Add character based on description
            char_center_x = x + width // 2
            char_center_y = y + height // 2
            self._add_sophisticated_character(draw, char_center_x, char_center_y, character_description)
            
            # Add environmental elements
            self._add_environmental_elements(draw, x, y, width, height, page_number)
            
            # Add magical elements
            self._add_magical_elements(draw, x, y, width, height)
            
        except Exception as e:
            print(f"Error creating page illustration: {e}")
            # Add simple fallback illustration
            self._add_simple_illustration(draw, x, y, width, height, page_number)
    
    def _create_dynamic_background(self, draw, x, y, width, height, page_number):
        """Create a dynamic background that changes with each page"""
        # Different color schemes for different pages
        color_schemes = [
            # Page 1: Dawn/sunrise
            [('#FFE4E1', '#FFB6C1', '#87CEEB'), (0.3, 0.7, 1.0)],
            # Page 2: Morning
            [('#F0E68C', '#98FB98', '#87CEEB'), (0.2, 0.6, 1.0)],
            # Page 3: Afternoon
            [('#FFD700', '#FFA500', '#32CD32'), (0.1, 0.5, 1.0)],
            # Page 4: Evening
            [('#FF69B4', '#9370DB', '#4169E1'), (0.0, 0.4, 1.0)],
            # Page 5: Night
            [('#191970', '#4B0082', '#8A2BE2'), (0.0, 0.3, 1.0)]
        ]
        
        scheme_idx = (page_number - 1) % len(color_schemes)
        colors, stops = color_schemes[scheme_idx]
        
        # Create gradient background
        for i in range(height):
            progress = i / height
            
            if progress < stops[0]:
                color = colors[0]
            elif progress < stops[1]:
                t = (progress - stops[0]) / (stops[1] - stops[0])
                color = self._interpolate_color(colors[0], colors[1], t)
            else:
                t = (progress - stops[1]) / (stops[2] - stops[1])
                color = self._interpolate_color(colors[1], colors[2], t)
            
            draw.line([(x, y + i), (x + width, y + i)], fill=color)
    
    def _interpolate_color(self, color1, color2, t):
        """Interpolate between two colors"""
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        return (r, g, b)
    
    def _add_sophisticated_character(self, draw, center_x, center_y, character_description):
        """Add a sophisticated character based on the description"""
        try:
            # Create character body
            char_size = 60
            body_rect = [center_x - char_size//2, center_y - char_size//2,
                        center_x + char_size//2, center_y + char_size//2]
            
            # Create gradient body
            for y_pos in range(body_rect[1], body_rect[3]):
                progress = (y_pos - body_rect[1]) / (body_rect[3] - body_rect[1])
                r = int(255 * (1 - progress) + 182 * progress)
                g = int(182 * (1 - progress) + 105 * progress)
                b = int(193 * (1 - progress) + 180 * progress)
                color = (r, g, b)
                
                line_width = char_size * (1 - progress * 0.3)
                start_x = center_x - line_width//2
                end_x = center_x + line_width//2
                
                draw.line([(start_x, y_pos), (end_x, y_pos)], fill=color, width=2)
            
            # Add character head
            head_center = (center_x, center_y - char_size//2 - 20)
            head_radius = 25
            draw.ellipse([head_center[0] - head_radius, head_center[1] - head_radius,
                         head_center[0] + head_radius, head_center[1] + head_radius], 
                        fill='#ffdab9', outline='#daa520', width=2)
            
            # Add facial features
            self._add_character_face(draw, head_center, head_radius)
            
        except Exception as e:
            print(f"Error adding character: {e}")
    
    def _add_character_face(self, draw, head_center, head_radius):
        """Add character facial features"""
        try:
            # Eyes
            eye_color = '#4169e1'
            left_eye = (head_center[0] - 10, head_center[1] - 2)
            right_eye = (head_center[0] + 10, head_center[1] - 2)
            
            # Eye shadows
            draw.ellipse([left_eye[0] - 6, left_eye[1] - 6, left_eye[0] + 6, left_eye[1] + 6], 
                        fill='#2c3e50', outline='#34495e', width=1)
            draw.ellipse([right_eye[0] - 6, right_eye[1] - 6, right_eye[0] + 6, right_eye[1] + 6], 
                        fill='#2c3e50', outline='#34495e', width=1)
            
            # Main eyes
            draw.ellipse([left_eye[0] - 4, left_eye[1] - 4, left_eye[0] + 4, left_eye[1] + 4], 
                        fill=eye_color, outline='#000080', width=1)
            draw.ellipse([right_eye[0] - 4, right_eye[1] - 4, right_eye[0] + 4, right_eye[1] + 4], 
                        fill=eye_color, outline='#000080', width=1)
            
            # Smile
            smile_bbox = [head_center[0] - 12, head_center[1] + 2, head_center[0] + 12, head_center[1] + 15]
            draw.arc(smile_bbox, start=0, end=180, fill='#ff69b4', width=2)
            
        except Exception as e:
            print(f"Error adding character face: {e}")
    
    def _add_environmental_elements(self, draw, x, y, width, height, page_number):
        """Add environmental storytelling elements"""
        try:
            # Add clouds or stars based on page number
            if page_number <= 3:
                # Daytime: add clouds
                for i in range(3):
                    cloud_x = x + random.randint(10, width - 30)
                    cloud_y = y + random.randint(10, height // 3)
                    self._draw_simple_cloud(draw, cloud_x, cloud_y, random.randint(15, 25))
            else:
                # Evening/Night: add stars
                for i in range(8):
                    star_x = x + random.randint(10, width - 10)
                    star_y = y + random.randint(10, height // 2)
                    self._draw_simple_star(draw, star_x, star_y, random.randint(2, 4))
            
            # Add ground
            ground_y = y + height - 20
            for i in range(0, width, 20):
                grass_height = random.randint(8, 15)
                grass_color = random.choice(['#228B22', '#32CD32', '#90EE90'])
                draw.line([(x + i, ground_y), (x + i + random.randint(-5, 5), ground_y - grass_height)], 
                         fill=grass_color, width=2)
                
        except Exception as e:
            print(f"Error adding environmental elements: {e}")
    
    def _draw_simple_cloud(self, draw, x, y, size):
        """Draw a simple cloud"""
        try:
            # Create cloud using overlapping circles
            for i in range(3):
                offset_x = random.randint(-size//3, size//3)
                offset_y = random.randint(-size//4, size//4)
                cloud_size = random.randint(size//2, size)
                draw.ellipse([x + offset_x - cloud_size//2, y + offset_y - cloud_size//2,
                             x + offset_x + cloud_size//2, y + offset_y + cloud_size//2], 
                            fill='#ffffff', outline='#e0e0e0', width=1)
        except Exception as e:
            print(f"Error drawing cloud: {e}")
    
    def _draw_simple_star(self, draw, x, y, size):
        """Draw a simple star"""
        try:
            # Create star points
            points = []
            for i in range(8):
                angle = i * 45 * 3.14159 / 180
                radius = size if i % 2 == 0 else size // 2
                px = x + radius * (angle * 0.5)
                py = y + radius * (angle * 0.5)
                points.append((px, py))
            
            if len(points) >= 3:
                draw.polygon(points, fill='#FFD700', outline='#FFA500', width=1)
        except Exception as e:
            print(f"Error drawing star: {e}")
    
    def _add_magical_elements(self, draw, x, y, width, height):
        """Add magical elements to the illustration"""
        try:
            # Add floating magical orbs
            for i in range(4):
                orb_x = x + random.randint(20, width - 20)
                orb_y = y + random.randint(20, height // 2)
                orb_size = random.randint(8, 15)
                orb_color = random.choice([self.colors['vibrant'], self.colors['cool'], self.colors['pastel']])
                
                # Orb glow
                draw.ellipse([orb_x - orb_size, orb_y - orb_size, orb_x + orb_size, orb_y + orb_size], 
                            fill=orb_color, outline='#ffffff', width=1)
                
                # Orb highlight
                highlight_size = orb_size // 3
                draw.ellipse([orb_x - highlight_size, orb_y - highlight_size, 
                             orb_x + highlight_size, orb_y + highlight_size], 
                            fill='#ffffff', outline='#ffffff', width=1)
                
        except Exception as e:
            print(f"Error adding magical elements: {e}")
    
    def _add_simple_illustration(self, draw, x, y, width, height, page_number):
        """Add a simple fallback illustration"""
        try:
            # Simple character
            char_x = x + width // 2
            char_y = y + height // 2
            draw.ellipse([char_x-20, char_y-20, char_x+20, char_y+20], 
                        fill='#ffdab9', outline='#daa520', width=2)
            
            # Simple decorations
            for i in range(3):
                dec_x = x + random.randint(20, width - 20)
                dec_y = y + random.randint(20, height - 20)
                dec_size = random.randint(8, 12)
                dec_color = random.choice([self.colors['vibrant'], self.colors['cool']])
                draw.ellipse([dec_x-dec_size, dec_y-dec_size, dec_x+dec_size, dec_y+dec_size], 
                            fill=dec_color, outline='#ffffff', width=1)
                
        except Exception as e:
            print(f"Error adding simple illustration: {e}")
    
    def _add_page_number(self, draw, width, height, page_number):
        """Add page number to the bottom right (small and unobtrusive)"""
        try:
            # Page number background
            page_num_bg = (width - 60, height - 30, width - 20, height - 20)
            draw.ellipse(page_num_bg, fill=self.colors['accent'], outline=self.colors['warm'], width=2)
            
            # Page number text
            page_text = f"{page_number}"
            text_bbox = draw.textbbox((0, 0), page_text)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = page_num_bg[0] + (page_num_bg[2] - page_num_bg[0] - text_width) // 2
            text_y = page_num_bg[1] + 5
            draw.text((text_x, text_y), page_text, fill='#8b4513')
            
        except Exception as e:
            print(f"Error adding page number: {e}")
    
    def _apply_professional_effects(self, img):
        """Apply professional post-processing effects"""
        try:
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.05)
            
        except Exception as e:
            print(f"Error applying professional effects: {e}")
        
        return img
    
    def _create_simple_fallback(self, page_number):
        """Create a very simple fallback image"""
        try:
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#f0f8ff')
            draw = ImageDraw.Draw(img)
            
            # Simple border
            draw.rectangle([0, 0, IMAGE_WIDTH-1, IMAGE_HEIGHT-1], outline='#4a90e2', width=2)
            
            # Simple text
            draw.text((20, 20), f"Page {page_number}", fill='#4a90e2')
            draw.text((20, 60), "Story Illustration", fill='#666666')
            
            return img
            
        except Exception as e:
            print(f"Error creating simple fallback: {e}")
            # Return a basic colored image
            return Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#e6f3ff')
    
    def save_image(self, image, filename):
        """Save image with maximum quality"""
        try:
            image.save(filename, 'PNG', quality=100, optimize=False)
            return True
        except Exception as e:
            print(f"Error saving image {filename}: {e}")
            return False
    
    def image_to_base64(self, image):
        """Convert image to high-quality base64"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG', quality=100, optimize=False)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return None
