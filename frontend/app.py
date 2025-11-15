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

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', 
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

@app.route('/api/process', methods=['POST'])
def proxy_process():
    """Proxy requests to backend API"""
    import requests
    try:
        # Forward request to backend (internal connection)
        response = requests.post(
            f'{BACKEND_API_URL}/api/process',
            json=request.json,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({'error': f'Backend connection failed: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def proxy_health():
    """Proxy health check to backend API"""
    import requests
    try:
        response = requests.get(f'{BACKEND_API_URL}/health', timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({'error': f'Backend not available: {str(e)}'}), 500

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
    print("Server running at: http://localhost:8081")
    print(f"Backend API URL: {BACKEND_API_URL}")
    print("=" * 60 + "\n")
    print("⚠️  Make sure the backend server is running at port 5001")
    print("=" * 60 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8081
    )

