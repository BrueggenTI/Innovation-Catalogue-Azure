# Additional API routes for image generation
from flask import request, jsonify
from app import app, csrf
import os
import uuid
import time
from werkzeug.utils import secure_filename
from PIL import Image

@app.route('/api/generate-image', methods=['POST'])
@csrf.exempt
def generate_image():
    """API endpoint for generating AI images for trends"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        prompt = data.get('prompt', '').strip()
        one_line_summary = data.get('one_line_summary', 'Business Trend')
        aspect_ratio = data.get('aspect_ratio', '16:9')
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400
        
        # Use the generate_image_tool to generate the image
        try:
            from tools.image_generation import generate_image_tool
            
            result = generate_image_tool(
                prompt=prompt,
                one_line_summary=one_line_summary,
                aspect_ratio=aspect_ratio
            )
            
            return jsonify({
                'success': True,
                'image_url': result.get('image_path'),
                'message': 'Image generated successfully'
            })
            
        except Exception as e:
            app.logger.error(f'Image generation failed: {str(e)}')
            return jsonify({
                'success': False,
                'error': 'Image generation failed. Please try again.'
            }), 500
        
    except Exception as e:
        app.logger.error(f'Generate image API error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'An error occurred while generating the image'
        }), 500

def save_uploaded_image(image_file):
    """Save uploaded image and return filename"""
    if not image_file or image_file.filename == '':
        return None
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if not ('.' in image_file.filename and 
            image_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return None
    
    # Generate unique filename
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:8]
    filename = f"trend_{timestamp}_{unique_id}.{image_file.filename.rsplit('.', 1)[1].lower()}"
    
    # Ensure directory exists
    images_dir = os.path.join('static', 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(images_dir, filename)
    
    try:
        # Resize and optimize image
        img = Image.open(image_file.stream)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = (800, 600)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image
        img.save(file_path, 'JPEG', quality=85, optimize=True)
        
        return filename
        
    except Exception as e:
        app.logger.error(f'Error saving image: {str(e)}')
        return None