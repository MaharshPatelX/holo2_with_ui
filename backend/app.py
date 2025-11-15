"""
Backend API Service - Vision Model Processing
Handles all AI model operations and image processing
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
from io import BytesIO
from PIL import Image
import time

# Load environment variables
load_dotenv()

# Import model functions
from model import initialize_model, process_image_task

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Configuration from environment
PORT = int(os.getenv('PORT', 5001))
HOST = os.getenv('HOST', '0.0.0.0')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

# Initialize model on startup (only once, not in reloader process)
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not DEBUG:
    print("=" * 60)
    print("BACKEND API - Initializing Vision Model...")
    print("=" * 60)
    model, processor = initialize_model()
    print("✓ Model initialized successfully!")
    print("=" * 60)
else:
    # Set dummy values for the initial load (before reloader)
    model, processor = None, None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'backend-api',
        'model': 'Holo2-4B'
    })

@app.route('/api/process', methods=['POST'])
def process_image():
    """
    Process image with vision model
    
    Expected JSON payload:
    {
        "image": "base64_encoded_image",
        "task": "task description",
        "task_type": "click"
    }
    """
    global model, processor
    
    # Ensure model is loaded (in case of reloader)
    if model is None or processor is None:
        print("Loading model in worker process...")
        model, processor = initialize_model()
    
    try:
        start_time = time.time()
        
        # Get request data
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        image_data = data.get('image', '')
        task = data.get('task', '')
        task_type = data.get('task_type', 'click')
        
        # Validate inputs
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        if not task:
            return jsonify({'error': 'No task provided'}), 400
        
        # Decode base64 image
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
        except Exception as e:
            return jsonify({'error': f'Invalid image data: {str(e)}'}), 400
        
        print(f"Processing request: task='{task}', image_size={image.size}")
        
        # Process with model
        result = process_image_task(model, processor, image, task, task_type)
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)  # in milliseconds
        
        if 'error' in result:
            print(f"✗ Processing failed: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error'],
                'processing_time': processing_time
            }), 500
        
        print(f"✓ Processing completed in {processing_time}ms")
        
        return jsonify({
            'success': True,
            'result': result,
            'processing_time': processing_time
        })
    
    except Exception as e:
        print(f"✗ Error in process_image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    return jsonify({
        'model_name': 'Holo2-4B',
        'model_type': 'Vision-Language Model',
        'capabilities': [
            'GUI Element Localization',
            'Click Coordinate Prediction',
            'Visual Understanding'
        ],
        'status': 'ready'
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("BACKEND API SERVER")
    print("=" * 60)
    print(f"Server running at: http://{HOST}:{PORT}")
    print(f"Health check: http://localhost:{PORT}/health")
    print(f"API endpoint: http://localhost:{PORT}/api/process")
    print("=" * 60 + "\n")
    
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT,
        threaded=True
    )

