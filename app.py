import streamlit as st
import os
import tempfile
import time
from datetime import datetime
import base64
import io

# Import our custom modules
from enhanced_story_generator import EnhancedStoryGenerator
from corrected_image_generator import CorrectedImageGenerator
from professional_pdf_generator import ProfessionalPDFGenerator
from audio_generator import AudioGenerator
from config import STORY_PAGES

# Page configuration
st.set_page_config(
    page_title="AI Storybook Creator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for classy design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .story-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .page-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    .generate-btn {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'story_generated' not in st.session_state:
        st.session_state.story_generated = False
    if 'story_pages' not in st.session_state:
        st.session_state.story_pages = []
    if 'images' not in st.session_state:
        st.session_state.images = []
    if 'pdf_path' not in st.session_state:
        st.session_state.pdf_path = None
    if 'audio_path' not in st.session_state:
        st.session_state.audio_path = None
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 AI Storybook Creator</h1>
        <p>Transform your imagination into magical children's stories with AI-generated text, images, and audio narration!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h3>✨ Features</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🤖 AI Story Generation</h4>
            <p>Create unique stories with Gemini AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🎨 Consistent Images</h4>
            <p>Beautiful illustrations for each page</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>📖 PDF Download</h4>
            <p>Professional storybook format</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🎵 Audio Narration</h4>
            <p>Listen to your story come alive</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**How to use:**")
        st.markdown("1. Enter your story prompt")
        st.markdown("2. Click 'Generate Story'")
        st.markdown("3. Download your PDF")
        st.markdown("4. Listen to audio narration")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Story prompt input
        st.markdown("### 🎯 Your Story Prompt")
        story_prompt = st.text_area(
            "Describe the story you want to create...",
            placeholder="Example: A brave little mouse who discovers a magical garden and makes friends with talking flowers",
            height=100,
            help="Be as descriptive as you want! The AI will create a 5-page children's story based on your prompt."
        )
        
        # Generate button
        if st.button("🚀 Generate Story", type="primary", use_container_width=True):
            if story_prompt.strip():
                generate_story(story_prompt)
            else:
                st.error("Please enter a story prompt!")
    
    with col2:
        # Quick tips
        st.markdown("### 💡 Quick Tips")
        st.markdown("- Be specific about characters")
        st.markdown("- Include setting details")
        st.markdown("- Mention any themes")
        st.markdown("- Keep it child-friendly")
        
        # Story stats
        if st.session_state.story_generated:
            st.markdown("### 📊 Story Stats")
            st.metric("Pages", STORY_PAGES)
            st.metric("Characters", len(''.join(story_prompt.split())))
            st.metric("Status", "✅ Complete")
    
    # Display generated story
    if st.session_state.story_generated:
        display_story()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎨 Created with ❤️ using Streamlit, Gemini AI, and Python</p>
        <p>Transform your ideas into magical stories!</p>
    </div>
    """, unsafe_allow_html=True)

def generate_story(prompt):
    """Generate the complete story with progress indicators"""
    with st.spinner("🤖 AI is crafting your magical story..."):
        # Initialize generators
        story_gen = EnhancedStoryGenerator()
        image_gen = CorrectedImageGenerator()
        pdf_gen = ProfessionalPDFGenerator()
        audio_gen = AudioGenerator()
        
        # Step 1: Generate story text
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📝 Generating story text...")
        story_pages = story_gen.generate_story(prompt)
        progress_bar.progress(20)
        
        if not story_pages:
            st.error("Failed to generate story text. Please try again.")
            return
        
        # Step 2: Generate character description and title
        status_text.text("🎭 Creating character descriptions and title...")
        character_desc = story_gen.generate_character_description(' '.join(story_pages), prompt)
        story_title = story_gen.generate_story_title(story_pages, prompt)
        progress_bar.progress(40)
        
        # Step 3: Generate images
        status_text.text("🎨 Creating beautiful illustrations...")
        images = []
        image_paths = []
        
        temp_dir = tempfile.mkdtemp()
        
        for i, page_text in enumerate(story_pages):
            # Pass story context for better image generation
            story_context = f"Story: {prompt[:100]}... Character: {character_desc[:100]}..."
            img = image_gen.generate_page_image(page_text, character_desc, i + 1, story_context)
            images.append(img)
            
            # Save image
            img_path = os.path.join(temp_dir, f"page_{i+1}.png")
            image_gen.save_image(img, img_path)
            image_paths.append(img_path)
            
            progress_bar.progress(40 + (i + 1) * 10)
        
        # Step 4: Generate PDF
        status_text.text("📖 Creating your storybook PDF...")
        pdf_filename = f"storybook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        success = pdf_gen.create_enhanced_storybook_pdf(
            story_pages, 
            image_paths, 
            pdf_path, 
            story_title,
            character_desc
        )
        
        if not success:
            st.error("Failed to create PDF. Please try again.")
            return
        
        progress_bar.progress(80)
        
        # Step 5: Generate audio
        status_text.text("🎵 Creating audio narration...")
        audio_path = audio_gen.generate_story_audio(story_pages, f"Story: {prompt[:30]}...")
        progress_bar.progress(100)
        
        # Update session state
        st.session_state.story_generated = True
        story_state = st.session_state.story_pages = story_pages
        st.session_state.images = images
        st.session_state.pdf_path = pdf_path
        st.session_state.audio_path = audio_path
        st.session_state.temp_dir = temp_dir
        st.session_state.story_title = story_title
        st.session_state.character_desc = character_desc
        
        status_text.text("✨ Your storybook is ready!")
        st.success("🎉 Story generated successfully! Scroll down to view and download your storybook.")
        
        # Auto-refresh to show the story
        st.rerun()

def display_story():
    """Display the generated story with download options"""
    st.markdown("## 📚 Your Generated Storybook")
    
    # Story preview
    for i, (page_text, image) in enumerate(zip(st.session_state.story_pages, st.session_state.images)):
        with st.expander(f"📖 Page {i+1}", expanded=True):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"**{page_text}**")
            
            with col2:
                if image:
                    # Convert image to base64 for display
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    st.image(f"data:image/png;base64,{img_str}", use_container_width=True)
    
    # Download section
    st.markdown("## 📥 Download Your Storybook")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
            with open(st.session_state.pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                st.download_button(
                    label="📖 Download PDF Storybook",
                    data=pdf_data,
                    file_name=f"storybook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
    
    with col2:
        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            with open(st.session_state.audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
                st.download_button(
                    label="🎵 Download Audio Narration",
                    data=audio_data,
                    file_name=f"story_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                    mime="audio/mp3",
                    use_container_width=True,
                    type="secondary"
                )
    
    # Audio player
    if st.session_state.audio_path:
        st.markdown("## 🎵 Listen to Your Story")
        st.audio(st.session_state.audio_path, format="audio/mp3")
    
    # Generate new story button
    if st.button("🔄 Create Another Story", use_container_width=True):
        # Clean up temporary files
        if 'temp_dir' in st.session_state and os.path.exists(st.session_state.temp_dir):
            import shutil
            shutil.rmtree(st.session_state.temp_dir)
        
        # Reset session state
        st.session_state.story_generated = False
        st.session_state.story_pages = []
        st.session_state.images = []
        st.session_state.pdf_path = None
        st.session_state.audio_path = None
        
        st.rerun()

if __name__ == "__main__":
    main()
