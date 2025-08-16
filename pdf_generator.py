from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from config import PDF_PAGE_WIDTH, PDF_PAGE_HEIGHT, PDF_MARGIN
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the storybook"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#2E86AB'),
            spaceAfter=20,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold'
        )
        
        # Page text style
        self.page_style = ParagraphStyle(
            'CustomPage',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=HexColor('#333333'),
            spaceAfter=15,
            alignment=0,  # Left alignment
            fontName='Helvetica',
            leading=20
        )
        
        # Page number style
        self.page_num_style = ParagraphStyle(
            'CustomPageNum',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=HexColor('#666666'),
            spaceAfter=10,
            alignment=2,  # Right alignment
            fontName='Helvetica-Oblique'
        )
    
    def create_storybook_pdf(self, story_pages, image_paths, output_filename, story_title="My Storybook"):
        """Create a PDF storybook with text and images"""
        try:
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=letter,
                rightMargin=PDF_MARGIN,
                leftMargin=PDF_MARGIN,
                topMargin=PDF_MARGIN,
                bottomMargin=PDF_MARGIN
            )
            
            story_content = []
            
            # Add title page
            story_content.extend(self._create_title_page(story_title))
            
            # Add story pages
            for i, (page_text, image_path) in enumerate(zip(story_pages, image_paths), 1):
                story_content.extend(self._create_story_page(page_text, image_path, i))
            
            # Build the PDF
            doc.build(story_content)
            return True
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return False
    
    def _create_title_page(self, title):
        """Create the title page for the storybook"""
        content = []
        
        # Add title
        title_para = Paragraph(title, self.title_style)
        content.append(title_para)
        
        # Add some spacing
        content.append(Spacer(1, 2*inch))
        
        # Add subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=HexColor('#666666'),
            alignment=1
        )
        subtitle = Paragraph("A Magical Children's Story", subtitle_style)
        content.append(subtitle)
        
        # Add decorative elements
        content.append(Spacer(1, 3*inch))
        
        # Add author info
        author_style = ParagraphStyle(
            'Author',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=HexColor('#888888'),
            alignment=1
        )
        author = Paragraph("Created with AI Storybook Creator", author_style)
        content.append(author)
        
        # Add page break
        content.append(Spacer(1, 0.5*inch))
        
        return content
    
    def _create_story_page(self, page_text, image_path, page_number):
        """Create a single story page with text and image"""
        content = []
        
        # Add page number
        page_num = Paragraph(f"Page {page_number}", self.page_num_style)
        content.append(page_num)
        
        # Add image if available
        if image_path and os.path.exists(image_path):
            try:
                # Calculate image dimensions to fit on page
                img_width = 4*inch
                img_height = 3*inch
                
                img = RLImage(image_path, width=img_width, height=img_height)
                content.append(img)
                content.append(Spacer(1, 0.3*inch))
                
            except Exception as e:
                print(f"Error adding image to page {page_number}: {e}")
        
        # Add story text
        story_para = Paragraph(page_text, self.page_style)
        content.append(story_para)
        
        # Add spacing between pages
        content.append(Spacer(1, 0.5*inch))
        
        return content
    
    def add_page_break(self):
        """Add a page break to the story"""
        return Spacer(1, 0.1*inch)
