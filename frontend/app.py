"""
Frontend Service - UI and User Interface
Handles all user interactions, image uploads, and displays results
"""
from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Backend API configuration
BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://localhost:5001')

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_sample_images():
    """Return sample images for the gallery"""
    return [
        {
            'name': 'Calendar',
            'url': 'https://raw.githubusercontent.com/hcompai/hai-cookbook/445d2017fcc8a0867081ea4786c34f87ed7053eb/data/calendar_example.jpg',
            'description': 'Calendar booking interface'
        },
        {
            'name': 'Receipt',
            'url': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400',
            'description': 'Restaurant receipt'
        },
        {
            'name': 'Web Page',
            'url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400',
            'description': 'Web page screenshot'
        },
        {
            'name': 'Mobile App',
            'url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400',
            'description': 'Mobile app interface'
        }
    ]

@app.route('/')
def index():
    """Render the main page"""
    sample_images = get_sample_images()
    return render_template('index.html', 
                         sample_images=sample_images,
                         backend_api_url=BACKEND_API_URL)

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read image
        image_bytes = file.read()
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to base64 for display
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_str}',
            'width': image.width,
            'height': image.height
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/config')
def get_config():
    """Get frontend configuration"""
    return jsonify({
        'backend_api_url': BACKEND_API_URL
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("FRONTEND UI SERVER")
    print("=" * 60)
    print("Server running at: http://localhost:5000")
    print(f"Backend API URL: {BACKEND_API_URL}")
    print("=" * 60 + "\n")
    print("⚠️  Make sure the backend server is running at port 5001")
    print("=" * 60 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

