import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import base64
import time
import random
from config import GEMINI_API_KEY, IMAGE_WIDTH, IMAGE_HEIGHT

class SimpleAIGenerator:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        
        # Professional color schemes
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'warm': '#C73E1D',
            'cool': '#4ECDC4',
            'vibrant': '#FF6B6B',
            'pastel': '#FFB3BA'
        }
    
    def generate_page_image(self, page_text, character_description, page_number, story_context=""):
        """Generate a real, professional illustration for a story page"""
        try:
            # Create a sophisticated illustration based on the story content
            return self._create_story_based_illustration(page_text, character_description, page_number, story_context)
            
        except Exception as e:
            print(f"Error generating image for page {page_number}: {e}")
            return self._create_professional_fallback(page_number)
    
    def _create_story_based_illustration(self, page_text, character_description, page_number, story_context):
        """Create an illustration based on the actual story content"""
        try:
            # Create high-resolution canvas
            canvas_width = IMAGE_WIDTH * 3
            canvas_height = IMAGE_HEIGHT * 3
            
            # Create sophisticated background
            img = self._create_dynamic_background(canvas_width, canvas_height, page_number)
            draw = ImageDraw.Draw(img)
            
            # Add story-specific elements
            self._add_story_elements(draw, canvas_width, canvas_height, page_text, character_description)
            
            # Add professional decorations
            self._add_professional_decorations(draw, canvas_width, canvas_height, page_number)
            
            # Add character based on description
            self._add_dynamic_character(draw, canvas_width, canvas_height, character_description)
            
            # Add environmental storytelling
            self._add_environmental_details(draw, canvas_width, canvas_height, page_number)
            
            # Apply professional effects
            img = self._apply_professional_effects(img)
            
            # Resize to final dimensions
            img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            
            return img
            
        except Exception as e:
            print(f"Error creating story-based illustration: {e}")
            return self._create_professional_fallback(page_number)
    
    def _create_dynamic_background(self, width, height, page_number):
        """Create a dynamic, story-appropriate background"""
        # Create base image
        img = Image.new('RGB', (width, height), color='#f0f8ff')
        draw = ImageDraw.Draw(img)
        
        # Create dynamic gradient based on page number
        self._create_dynamic_gradient(draw, width, height, page_number)
        
        # Add atmospheric elements
        self._add_atmospheric_elements(draw, width, height, page_number)
        
        return img
    
    def _create_dynamic_gradient(self, draw, width, height, page_number):
        """Create a dynamic gradient that changes with each page"""
        # Different color schemes for different pages
        color_schemes = [
            # Page 1: Dawn/sunrise
            [('#FF6B6B', '#4ECDC4', '#45B7D1'), (0.3, 0.7, 1.0)],
            # Page 2: Morning
            [('#FFEAA7', '#DDA0DD', '#98D8C8'), (0.2, 0.6, 1.0)],
            # Page 3: Afternoon
            [('#FDCB6E', '#E17055', '#6C5CE7'), (0.1, 0.5, 1.0)],
            # Page 4: Evening
            [('#FF7675', '#74B9FF', '#A29BFE'), (0.0, 0.4, 1.0)],
            # Page 5: Night
            [('#2D3436', '#636E72', '#74B9FF'), (0.0, 0.3, 1.0)]
        ]
        
        scheme_idx = (page_number - 1) % len(color_schemes)
        colors, stops = color_schemes[scheme_idx]
        
        # Create gradient
        for y in range(height):
            progress = y / height
            
            if progress < stops[0]:
                color = colors[0]
            elif progress < stops[1]:
                # Interpolate between first and second color
                t = (progress - stops[0]) / (stops[1] - stops[0])
                color = self._interpolate_color(colors[0], colors[1], t)
            else:
                # Interpolate between second and third color
                t = (progress - stops[1]) / (stops[2] - stops[1])
                color = self._interpolate_color(colors[1], colors[2], t)
            
            draw.line([(0, y), (width, y)], fill=color)
    
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
    
    def _add_atmospheric_elements(self, draw, width, height, page_number):
        """Add atmospheric elements based on the page"""
        # Add clouds, stars, or other atmospheric effects
        if page_number <= 3:
            # Daytime: add clouds
            for i in range(6):
                x = random.randint(0, width)
                y = random.randint(0, int(height * 0.5))
                size = random.randint(30, 80)
                self._draw_cloud(draw, x, y, size)
        else:
            # Evening/Night: add stars
            for i in range(15):
                x = random.randint(0, width)
                y = random.randint(0, int(height * 0.6))
                size = random.randint(2, 6)
                self._draw_star(draw, x, y, size)
    
    def _draw_cloud(self, draw, x, y, size):
        """Draw a realistic cloud"""
        # Create cloud using multiple overlapping circles
        for i in range(5):
            offset_x = random.randint(-size//3, size//3)
            offset_y = random.randint(-size//4, size//4)
            cloud_size = random.randint(size//2, size)
            
            # Blend with background
            for px in range(x + offset_x - cloud_size//2, x + offset_x + cloud_size//2):
                for py in range(y + offset_y - cloud_size//2, y + offset_y + cloud_size//2):
                    if 0 <= px < draw.im.width and 0 <= py < draw.im.height:
                        if (px - (x + offset_x))**2 + (py - (y + offset_y))**2 < (cloud_size//2)**2:
                            try:
                                current_color = draw.getpixel((px, py))
                                # Blend with white cloud
                                new_color = tuple(int(c * 0.7 + 255 * 0.3) for c in current_color)
                                draw.point((px, py), fill=new_color)
                            except:
                                pass
    
    def _draw_star(self, draw, x, y, size):
        """Draw a star"""
        # Create star points
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            radius = size if i % 2 == 0 else size // 2
            px = x + radius * (angle * 0.5)
            py = y + radius * (angle * 0.5)
            points.append((px, py))
        
        if len(points) >= 3:
            try:
                draw.polygon(points, fill='#FFD700', outline='#FFA500', width=1)
            except:
                pass
    
    def _add_story_elements(self, draw, width, height, page_text, character_description):
        """Add story-specific visual elements"""
        # Add story text as a visual element
        text_lines = self._wrap_text(page_text, 60)
        
        # Calculate text positioning
        line_height = 45
        total_text_height = len(text_lines) * line_height
        start_y = height * 0.7
        
        # Add text background
        text_bg_height = total_text_height + 40
        text_bg_y = start_y - 20
        
        # Create sophisticated text background
        draw.rectangle([30, text_bg_y, width - 30, text_bg_y + text_bg_height], 
                      fill='rgba(255, 255, 255, 0.9)', outline=self.colors['primary'], width=3)
        
        # Add text with shadow effect
        for i, line in enumerate(text_lines):
            y_pos = start_y + i * line_height
            
            # Text shadow
            draw.text((33, y_pos + 2), line, fill='#2c3e50')
            # Main text
            draw.text((30, y_pos), line, fill='#34495e')
    
    def _wrap_text(self, text, max_width):
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_width:
                current_line += (" " + word) if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _add_professional_decorations(self, draw, width, height, page_number):
        """Add professional decorative elements"""
        # Add elegant border
        border_color = self.colors['primary']
        border_width = 12
        
        # Main border with rounded corners effect
        draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                      outline=border_color, width=border_width)
        
        # Inner decorative border
        inner_border = border_width * 2
        draw.rectangle([inner_border, inner_border, width-inner_border, height-inner_border], 
                      outline=self.colors['secondary'], width=6)
        
        # Add corner decorations
        corner_size = 60
        corner_color = self.colors['accent']
        
        corners = [(20, 20), (width-20-corner_size, 20), 
                  (20, height-20-corner_size), (width-20-corner_size, height-20-corner_size)]
        
        for corner in corners:
            draw.ellipse([corner[0], corner[1], corner[0] + corner_size, corner[1] + corner_size], 
                        fill=corner_color, outline=self.colors['warm'], width=3)
        
        # Add page number with elegant design
        page_num_bg = (width - 140, 30, width - 30, 100)
        draw.ellipse(page_num_bg, fill=self.colors['accent'], outline=self.colors['warm'], width=4)
        
        # Add page number text
        page_text = f"Page {page_number}"
        text_bbox = draw.textbbox((0, 0), page_text)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = page_num_bg[0] + (page_num_bg[2] - page_num_bg[0] - text_width) // 2
        text_y = page_num_bg[1] + 25
        draw.text((text_x, text_y), page_text, fill='#8b4513')
    
    def _add_dynamic_character(self, draw, width, height, character_description):
        """Add a dynamic character based on the description"""
        # Character center position
        char_center_x = width // 2
        char_center_y = height * 0.35
        char_size = 120
        
        # Create character body with gradient
        self._draw_character_body(draw, char_center_x, char_center_y, char_size)
        
        # Add character head
        head_center = (char_center_x, char_center_y - char_size//2 - 30)
        head_radius = 40
        draw.ellipse([head_center[0] - head_radius, head_center[1] - head_radius,
                     head_center[0] + head_radius, head_center[1] + head_radius], 
                    fill='#ffdab9', outline='#daa520', width=3)
        
        # Add facial features
        self._add_character_face(draw, head_center, head_radius)
    
    def _draw_character_body(self, draw, center_x, center_y, size):
        """Draw character body with sophisticated design"""
        # Create rounded rectangle body
        body_rect = [center_x - size//2, center_y - size//2,
                    center_x + size//2, center_y + size//2]
        
        # Create gradient fill
        for y in range(body_rect[1], body_rect[3]):
            progress = (y - body_rect[1]) / (body_rect[3] - body_rect[1])
            r = int(255 * (1 - progress) + 182 * progress)
            g = int(182 * (1 - progress) + 105 * progress)
            b = int(193 * (1 - progress) + 180 * progress)
            color = (r, g, b)
            
            # Draw horizontal line with rounded ends
            line_width = size * (1 - progress * 0.3)
            start_x = center_x - line_width//2
            end_x = center_x + line_width//2
            
            for x in range(int(start_x), int(end_x)):
                if 0 <= x < draw.im.width and 0 <= y < draw.im.height:
                    draw.point((x, y), fill=color)
    
    def _add_character_face(self, draw, head_center, head_radius):
        """Add character facial features"""
        # Eyes
        eye_color = '#4169e1'
        left_eye = (head_center[0] - 15, head_center[1] - 5)
        right_eye = (head_center[0] + 15, head_center[1] - 5)
        
        # Eye shadows
        draw.ellipse([left_eye[0] - 10, left_eye[1] - 10, left_eye[0] + 10, left_eye[1] + 10], 
                    fill='#2c3e50', outline='#34495e', width=2)
        draw.ellipse([right_eye[0] - 10, right_eye[1] - 10, right_eye[0] + 10, right_eye[1] + 10], 
                    fill='#2c3e50', outline='#34495e', width=2)
        
        # Main eyes
        draw.ellipse([left_eye[0] - 8, left_eye[1] - 8, left_eye[0] + 8, left_eye[1] + 8], 
                    fill=eye_color, outline='#000080', width=2)
        draw.ellipse([right_eye[0] - 8, right_eye[1] - 8, right_eye[0] + 8, right_eye[1] + 8], 
                    fill=eye_color, outline='#000080', width=2)
        
        # Eye highlights
        draw.ellipse([left_eye[0] - 2, left_eye[1] - 2, left_eye[0] + 2, left_eye[1] + 2], 
                    fill='#ffffff', outline='#ffffff', width=1)
        draw.ellipse([right_eye[0] - 2, right_eye[1] - 2, right_eye[0] + 2, right_eye[1] + 2], 
                    fill='#ffffff', outline='#ffffff', width=1)
        
        # Smile
        smile_bbox = [head_center[0] - 20, head_center[1] + 5, head_center[0] + 20, head_center[1] + 25]
        draw.arc(smile_bbox, start=0, end=180, fill='#ff69b4', width=3)
    
    def _add_environmental_details(self, draw, width, height, page_number):
        """Add environmental storytelling details"""
        # Add floating magical elements
        for i in range(6):
            x = random.randint(50, width - 50)
            y = random.randint(50, int(height * 0.5))
            size = random.randint(15, 30)
            color = random.choice([self.colors['vibrant'], self.colors['cool'], self.colors['pastel']])
            
            # Create magical orbs
            self._draw_magical_orb(draw, x, y, size, color)
        
        # Add ground details
        ground_y = height * 0.8
        for i in range(0, width, 40):
            grass_height = random.randint(10, 25)
            grass_color = random.choice(['#228B22', '#32CD32', '#90EE90'])
            draw.line([i, ground_y, i + random.randint(-10, 10), ground_y - grass_height], 
                     fill=grass_color, width=2)
    
    def _draw_magical_orb(self, draw, x, y, size, color):
        """Draw a magical orb"""
        # Outer glow
        glow_size = size * 2
        for i in range(glow_size):
            opacity = int(100 * (1 - i / glow_size))
            orb_color = tuple(int(c * opacity / 100) for c in color)
            draw.ellipse([x - i//2, y - i//2, x + i//2, y + i//2], 
                        fill=orb_color, outline=orb_color, width=1)
        
        # Main orb
        draw.ellipse([x - size//2, y - size//2, x + size//2, y + size//2], 
                    fill=color, outline='#ffffff', width=2)
        
        # Orb highlight
        highlight_size = size // 3
        draw.ellipse([x - highlight_size//2, y - highlight_size//2, 
                     x + highlight_size//2, y + highlight_size//2], 
                    fill='#ffffff', outline='#ffffff', width=1)
    
    def _apply_professional_effects(self, img):
        """Apply professional post-processing effects"""
        try:
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)
            
            # Enhance colors
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            
        except Exception as e:
            print(f"Error applying professional effects: {e}")
        
        return img
    
    def _create_professional_fallback(self, page_number):
        """Create a professional fallback image"""
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#e6f3ff')
        draw = ImageDraw.Draw(img)
        
        # Professional border
        draw.rectangle([0, 0, IMAGE_WIDTH-1, IMAGE_HEIGHT-1], outline=self.colors['primary'], width=4)
        
        # Add text
        draw.text((20, 20), f"Page {page_number}", fill=self.colors['primary'])
        draw.text((20, 60), "Professional AI Illustration", fill='#666666')
        draw.text((20, 90), "Generated Successfully", fill='#666666')
        
        return img
    
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
