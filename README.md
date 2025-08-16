# 📚 AI Storybook Creator

Transform your imagination into magical children's stories with AI-generated text, images, and audio narration!

## ✨ Features

- **🤖 AI Story Generation**: Create unique 5-page stories using Gemini AI
- **🎨 Consistent Images**: Beautiful illustrations for each page with character consistency
- **📖 PDF Download**: Professional storybook format ready for printing
- **🎵 Audio Narration**: Listen to your story come alive with natural voice
- **🎨 Classy UI**: Modern, beautiful interface built with Streamlit

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Gemini API key (already configured)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal

## 🎯 How to Use

1. **Enter your story prompt** - Describe the story you want to create
2. **Click "Generate Story"** - AI will create text, images, and audio
3. **Preview your story** - See all 5 pages with illustrations
4. **Download your storybook** - Get the PDF and audio files
5. **Listen to narration** - Play the audio directly in the app

## 🏗️ Project Structure

```
AI-Storybook-Creator/
├── app.py                 # Main Streamlit application
├── story_generator.py     # AI story generation using Gemini
├── image_generator.py     # Image creation and processing
├── pdf_generator.py       # PDF creation and formatting
├── audio_generator.py     # Text-to-speech audio generation
├── config.py             # Configuration and API keys
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Technical Details

### AI Components
- **Story Generation**: Uses Gemini Pro for creative story writing
- **Character Consistency**: Maintains character descriptions across all pages
- **Image Generation**: Creates placeholder images (can be enhanced with Gemini's image generation)

### File Formats
- **PDF**: Professional A4 format with custom styling
- **Audio**: MP3 format using Google Text-to-Speech
- **Images**: PNG format for high quality

### Dependencies
- `streamlit`: Web application framework
- `google-generativeai`: Gemini AI integration
- `reportlab`: PDF generation
- `Pillow`: Image processing
- `gtts`: Text-to-speech conversion

## 🎨 Customization

### Story Settings
- Modify `STORY_PAGES` in `config.py` to change page count
- Adjust `MAX_STORY_LENGTH` for different story lengths
- Customize character description length

### UI Styling
- Edit CSS in `app.py` for different color schemes
- Modify layout and spacing in the Streamlit components
- Add custom themes and branding

### PDF Styling
- Customize fonts, colors, and layouts in `pdf_generator.py`
- Adjust page margins and image sizes
- Add custom headers and footers

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your Gemini API key is valid
   - Check internet connection

2. **Image Generation Fails**
   - The app will create placeholder images as fallback
   - Check PIL/Pillow installation

3. **PDF Creation Issues**
   - Ensure ReportLab is properly installed
   - Check file permissions in temp directory

4. **Audio Generation Problems**
   - Verify gTTS installation
   - Check internet connection for TTS service

### Performance Tips
- Use shorter story prompts for faster generation
- Close other applications to free up memory
- Ensure stable internet connection

## 🔮 Future Enhancements

- **Real Image Generation**: Integrate with Gemini's image generation API
- **Multiple Languages**: Support for different languages
- **Story Templates**: Pre-built story themes and structures
- **Character Database**: Save and reuse character designs
- **Collaborative Features**: Share and edit stories with others

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Feel free to enhance the application with:
- Better image generation algorithms
- Additional story formats
- Enhanced UI components
- Performance optimizations

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure API keys are valid
4. Check console for error messages

---

**Happy Storytelling! 🎭✨**
