// Global state
let currentImageData = null;
const BACKEND_API_URL = 'http://localhost:5001';

// DOM Elements
const fileInput = document.getElementById('fileInput');
const previewPlaceholder = document.getElementById('previewPlaceholder');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const previewLabel = document.getElementById('previewLabel');
const closeBtn = document.getElementById('closeBtn');
const taskInput = document.getElementById('taskInput');
const processBtn = document.getElementById('processBtn');
const resultsSection = document.getElementById('resultsSection');
const resultCanvas = document.getElementById('resultCanvas');
const loadingOverlay = document.getElementById('loadingOverlay');
const coordinatesDisplay = document.getElementById('coordinatesDisplay');
const resultPrompt = document.getElementById('resultPrompt');
const resultMeta = document.getElementById('resultMeta');
const coordPosition = document.getElementById('coordPosition');
const coordNormalized = document.getElementById('coordNormalized');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkBackendConnection();
});

function setupEventListeners() {
    // File upload
    previewPlaceholder.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    previewPlaceholder.addEventListener('dragover', handleDragOver);
    previewPlaceholder.addEventListener('drop', handleDrop);
    
    // Close button
    closeBtn.addEventListener('click', clearImage);
    
    // Process button
    processBtn.addEventListener('click', handleProcess);
    
    // Task input enter key
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleProcess();
    });
}

// Check backend connection
async function checkBackendConnection() {
    try {
        const response = await fetch(`${BACKEND_API_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('✓ Backend connected:', data);
            showToast('Backend connected', 'success');
        } else {
            showToast('Backend not responding', 'warning');
        }
    } catch (error) {
        console.error('✗ Backend connection failed:', error);
        showToast('Cannot connect to backend. Make sure it\'s running on port 5001', 'error');
    }
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        loadImage(file);
    } else {
        showToast('Please select a valid image file', 'error');
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
}

// Handle drop
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        loadImage(file);
    } else {
        showToast('Please drop a valid image file', 'error');
    }
}

// Load image
function loadImage(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        currentImageData = e.target.result;
        previewImage.src = currentImageData;
        previewLabel.textContent = file.name.split('.')[0] || 'Image';
        
        // Show preview
        previewPlaceholder.style.display = 'none';
        previewContainer.style.display = 'flex';
        
        // Hide results
        resultsSection.style.display = 'none';
        
        showToast('Image loaded', 'success');
    };
    
    reader.readAsDataURL(file);
}

// Clear image
function clearImage() {
    currentImageData = null;
    previewImage.src = '';
    previewContainer.style.display = 'none';
    previewPlaceholder.style.display = 'block';
    resultsSection.style.display = 'none';
    fileInput.value = '';
}

// Handle process
async function handleProcess() {
    if (!currentImageData) {
        showToast('Please upload an image first', 'warning');
        return;
    }
    
    const task = taskInput.value.trim();
    if (!task) {
        showToast('Please enter a task description', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        const startTime = Date.now();
        
        console.log('Sending request to backend...');
        
        // Call backend API
        const response = await fetch(`${BACKEND_API_URL}/api/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: currentImageData,
                task: task,
                task_type: 'click'
            })
        });
        
        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }
        
        const data = await response.json();
        const elapsed = Date.now() - startTime;
        
        console.log('Backend response:', data);
        
        if (data.success) {
            displayResults(data.result, elapsed);
            showToast('Processing complete!', 'success');
        } else {
            showToast(data.error || 'Processing failed', 'error');
        }
    } catch (error) {
        console.error('Processing error:', error);
        showToast('Failed to process: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Display results
function displayResults(result, responseTime) {
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update info panel
    resultPrompt.textContent = result.task || taskInput.value;
    resultMeta.textContent = `Response time: ${responseTime}ms`;
    
    // Draw result on canvas
    if (result.processed_image && result.coordinates) {
        drawResultWithMarker(
            result.processed_image,
            result.coordinates,
            result.image_width,
            result.image_height
        );
        
        // Show coordinates
        coordinatesDisplay.style.display = 'block';
        coordPosition.textContent = `(${Math.round(result.coordinates.x_pixel)}, ${Math.round(result.coordinates.y_pixel)})`;
        coordNormalized.textContent = `(${result.coordinates.x}, ${result.coordinates.y})`;
    }
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Draw result with marker
function drawResultWithMarker(imageData, coordinates, imageWidth, imageHeight) {
    const img = new Image();
    
    img.onload = () => {
        // Set canvas size
        resultCanvas.width = imageWidth;
        resultCanvas.height = imageHeight;
        
        const ctx = resultCanvas.getContext('2d');
        
        // Draw image
        ctx.drawImage(img, 0, 0, imageWidth, imageHeight);
        
        // Draw marker
        const x = coordinates.x_pixel;
        const y = coordinates.y_pixel;
        
        // Draw blue circle (matching the reference image)
        ctx.strokeStyle = '#4a90e2';
        ctx.fillStyle = 'rgba(74, 144, 226, 0.2)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        
        // Draw center dot
        ctx.fillStyle = '#4a90e2';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    };
    
    img.src = imageData;
}

// Show/hide loading
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// Show toast notification
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    if (type === 'warning') icon = 'fa-exclamation-triangle';
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
