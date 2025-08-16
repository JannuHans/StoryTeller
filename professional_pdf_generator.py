from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import io

class ProfessionalPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_professional_styles()
        self._setup_custom_fonts()
    
    def _setup_custom_fonts(self):
        """Setup custom fonts for professional appearance"""
        try:
            # Try to register custom fonts if available
            # Fallback to default fonts if custom fonts not found
            pass
        except:
            pass
    
    def _setup_professional_styles(self):
        """Setup professional paragraph styles for the storybook"""
        
        # Professional title style
        self.title_style = ParagraphStyle(
            'ProfessionalTitle',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=HexColor('#2E86AB'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=40,
            spaceBefore=20
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'ProfessionalSubtitle',
            parent=self.styles['Normal'],
            fontSize=18,
            textColor=HexColor('#666666'),
            spaceAfter=25,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=22
        )
        
        # Page text style - crisp and clear
        self.page_style = ParagraphStyle(
            'ProfessionalPage',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=HexColor('#2C3E50'),
            spaceAfter=20,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=24,
            firstLineIndent=20,
            leftIndent=20,
            rightIndent=20
        )
        
        # Page number style
        self.page_num_style = ParagraphStyle(
            'ProfessionalPageNum',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=HexColor('#7F8C8D'),
            spaceAfter=15,
            alignment=TA_RIGHT,
            fontName='Helvetica-Oblique',
            leading=18
        )
        
        # Character description style
        self.character_style = ParagraphStyle(
            'ProfessionalCharacter',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=HexColor('#34495E'),
            spaceAfter=15,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=20,
            leftIndent=30,
            rightIndent=30,
            backColor=HexColor('#F8F9FA'),
            borderWidth=1,
            borderColor=HexColor('#E9ECEF'),
            borderPadding=10
        )
        
        # Decorative text style
        self.decorative_style = ParagraphStyle(
            'ProfessionalDecorative',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=HexColor('#95A5A6'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique',
            leading=16
        )
    
    def create_storybook_pdf(self, story_pages, image_paths, output_filename, story_title="My Storybook", character_description=""):
        """Create a professional PDF storybook with crisp text and beautiful layout"""
        try:
            # Use A4 size for better international compatibility
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                rightMargin=25*mm,
                leftMargin=25*mm,
                topMargin=30*mm,
                bottomMargin=25*mm
            )
            
            story_content = []
            
            # Add professional title page
            story_content.extend(self._create_professional_title_page(story_title, character_description))
            
            # Add story pages with professional layout
            for i, (page_text, image_path) in enumerate(zip(story_pages, image_paths), 1):
                story_content.extend(self._create_professional_story_page(page_text, image_path, i, len(story_pages)))
            
            # Add professional back cover
            story_content.extend(self._create_professional_back_cover(story_title))
            
            # Build the PDF with professional quality
            doc.build(story_content)
            
            # Apply additional professional enhancements
            self._apply_professional_enhancements(output_filename)
            
            return True
            
        except Exception as e:
            print(f"Error creating professional PDF: {e}")
            return False
    
    def _create_professional_title_page(self, title, character_description):
        """Create a professional title page"""
        content = []
        
        # Add decorative top border
        content.append(Spacer(1, 20*mm))
        
        # Add title with professional styling
        title_para = Paragraph(title, self.title_style)
        content.append(title_para)
        
        # Add subtitle
        subtitle = Paragraph("A Magical Children's Story", self.subtitle_style)
        content.append(subtitle)
        
        # Add decorative separator
        content.append(Spacer(1, 40*mm))
        
        # Add character description if available
        if character_description:
            char_desc = f"<b>Meet the Characters:</b><br/>{character_description}"
            char_para = Paragraph(char_desc, self.character_style)
            content.append(char_para)
            content.append(Spacer(1, 30*mm))
        
        # Add author and creation info
        author_info = """
        <b>Created with AI Storybook Creator</b><br/>
        Powered by Gemini AI and Professional Design
        """
        author_para = Paragraph(author_info, self.decorative_style)
        content.append(author_para)
        
        # Add page break
        content.append(PageBreak())
        
        return content
    
    def _create_professional_story_page(self, page_text, image_path, page_number, total_pages):
        """Create a single professional story page"""
        content = []
        
        # Add page number with professional styling
        page_num = Paragraph(f"Page {page_number}", self.page_num_style)
        content.append(page_num)
        
        # Add professional image if available
        if image_path and os.path.exists(image_path):
            try:
                # Calculate optimal image dimensions
                img_width = 5*inch
                img_height = 3.5*inch
                
                # Create professional image with caption
                img = RLImage(image_path, width=img_width, height=img_height)
                content.append(img)
                content.append(Spacer(1, 15*mm))
                
            except Exception as e:
                print(f"Error adding image to page {page_number}: {e}")
        
        # Add story text with professional formatting
        # Clean and format the text for better readability
        formatted_text = self._format_story_text(page_text)
        story_para = Paragraph(formatted_text, self.page_style)
        content.append(story_para)
        
        # Add decorative bottom element
        content.append(Spacer(1, 20*mm))
        
        # Add page break (except for last page)
        if page_number < total_pages:
            content.append(PageBreak())
        
        return content
    
    def _format_story_text(self, text):
        """Format story text for professional appearance"""
        # Clean up the text
        text = text.strip()
        
        # Add proper paragraph breaks
        text = text.replace('. ', '.<br/>')
        
        # Add emphasis to key words
        words = text.split()
        formatted_words = []
        
        for word in words:
            # Capitalize first letter of sentences
            if word.endswith('.'):
                word = word.capitalize()
            # Add emphasis to character names and important words
            elif word.lower() in ['the', 'and', 'but', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']:
                word = word.lower()
            else:
                # Capitalize important words
                if len(word) > 3 and not word.startswith('the'):
                    word = word.capitalize()
            
            formatted_words.append(word)
        
        return ' '.join(formatted_words)
    
    def _create_professional_back_cover(self, story_title):
        """Create a professional back cover"""
        content = []
        
        content.append(PageBreak())
        content.append(Spacer(1, 40*mm))
        
        # Add back cover title
        back_title = Paragraph("The End", self.title_style)
        content.append(back_title)
        
        content.append(Spacer(1, 30*mm))
        
        # Add story summary
        summary_text = f"""
        <b>About This Story:</b><br/>
        {story_title} is a magical adventure created especially for young readers. 
        Each page brings new discoveries and wonderful lessons about friendship, courage, and imagination.
        """
        summary_para = Paragraph(summary_text, self.page_style)
        content.append(summary_para)
        
        content.append(Spacer(1, 40*mm))
        
        # Add closing message
        closing_text = """
        <b>Thank you for reading!</b><br/>
        May your imagination continue to soar and your adventures never end.
        """
        closing_para = Paragraph(closing_text, self.decorative_style)
        content.append(closing_para)
        
        return content
    
    def _apply_professional_enhancements(self, pdf_filename):
        """Apply additional professional enhancements to the PDF"""
        try:
            # This method can be used to add watermarks, headers, footers, etc.
            # For now, we'll focus on the content quality
            pass
        except Exception as e:
            print(f"Error applying professional enhancements: {e}")
    
    def create_enhanced_storybook_pdf(self, story_pages, image_paths, output_filename, story_title, character_description):
        """Create an enhanced version with additional professional features"""
        try:
            # Create the base PDF
            success = self.create_storybook_pdf(story_pages, image_paths, output_filename, story_title, character_description)
            
            if success:
                # Apply additional enhancements
                self._add_professional_headers_footers(output_filename)
                self._optimize_pdf_quality(output_filename)
            
            return success
            
        except Exception as e:
            print(f"Error creating enhanced PDF: {e}")
            return False
    
    def _add_professional_headers_footers(self, pdf_filename):
        """Add professional headers and footers to the PDF"""
        try:
            # This would add running headers and footers
            # Implementation depends on specific requirements
            pass
        except Exception as e:
            print(f"Error adding headers/footers: {e}")
    
    def _optimize_pdf_quality(self, pdf_filename):
        """Optimize PDF quality for professional printing"""
        try:
            # This would optimize the PDF for high-quality printing
            # Implementation depends on specific requirements
            pass
        except Exception as e:
            print(f"Error optimizing PDF quality: {e}")
    
    def create_print_ready_pdf(self, story_pages, image_paths, output_filename, story_title, character_description):
        """Create a print-ready PDF with professional standards"""
        try:
            # Use higher resolution and print-optimized settings
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=25*mm,
                bottomMargin=20*mm
            )
            
            story_content = []
            
            # Add print-optimized title page
            story_content.extend(self._create_print_title_page(story_title, character_description))
            
            # Add print-optimized story pages
            for i, (page_text, image_path) in enumerate(zip(story_pages, image_paths), 1):
                story_content.extend(self._create_print_story_page(page_text, image_path, i, len(story_pages)))
            
            # Build the print-ready PDF
            doc.build(story_content)
            
            return True
            
        except Exception as e:
            print(f"Error creating print-ready PDF: {e}")
            return False
    
    def _create_print_title_page(self, title, character_description):
        """Create a print-optimized title page"""
        content = []
        
        content.append(Spacer(1, 15*mm))
        
        # Print-optimized title
        title_para = Paragraph(title, self.title_style)
        content.append(title_para)
        
        content.append(Spacer(1, 30*mm))
        
        # Print-optimized subtitle
        subtitle = Paragraph("A Magical Children's Story", self.subtitle_style)
        content.append(subtitle)
        
        content.append(Spacer(1, 35*mm))
        
        # Character description for print
        if character_description:
            char_desc = f"<b>Characters:</b><br/>{character_description}"
            char_para = Paragraph(char_desc, self.character_style)
            content.append(char_para)
        
        content.append(PageBreak())
        
        return content
    
    def _create_print_story_page(self, page_text, image_path, page_number, total_pages):
        """Create a print-optimized story page"""
        content = []
        
        # Add page number
        page_num = Paragraph(f"Page {page_number}", self.page_num_style)
        content.append(page_num)
        
        # Add high-quality image
        if image_path and os.path.exists(image_path):
            try:
                # Print-optimized image dimensions
                img_width = 5.5*inch
                img_height = 4*inch
                
                img = RLImage(image_path, width=img_width, height=img_height)
                content.append(img)
                
                content.append(Spacer(1, 10*mm))
                
            except Exception as e:
                print(f"Error adding print image to page {page_number}: {e}")
        
        # Add print-optimized text
        formatted_text = self._format_story_text(page_text)
        story_para = Paragraph(formatted_text, self.page_style)
        content.append(story_para)
        
        if page_number < total_pages:
            content.append(PageBreak())
        
        return content
