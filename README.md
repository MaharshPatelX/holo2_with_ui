# Vision Navigator - Moondream-Style UI

A microservices-based Flask application with a **Moondream-inspired dark UI** for localizing GUI elements using vision-language models.

## 🎨 UI Design

The interface is carefully crafted to match the Moondream aesthetic:
- **Pure black background** with subtle contrasts
- **Minimalist design** with clean lines
- **Card-based layout** for content organization
- **Pill-style buttons** for actions and filters
- **Single-column flow** with clear visual hierarchy

## 🏗️ Architecture

```
┌─────────────────────┐          ┌─────────────────────┐
│   Frontend UI       │          │   Backend API       │
│   (Port 5000)       │  HTTP    │   (Port 5001)       │
│                     │ ───────> │                     │
│ - Moondream UI      │  API     │ - AI Model          │
│ - Image Upload      │          │ - Processing        │
│ - User Input        │          │ - Predictions       │
└─────────────────────┘          └─────────────────────┘
```

## 📁 Project Structure

```
.
├── backend/                    # Backend API Service
│   ├── app.py                 # Flask API (Port 5001)
│   ├── model.py               # AI model integration
│   └── requirements.txt       # Backend dependencies
│
├── frontend/                   # Frontend UI Service
│   ├── app.py                 # Flask server (Port 5000)
│   ├── templates/
│   │   └── index.html        # Moondream-style UI
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Dark theme styling
│   │   └── js/
│   │       └── main.js       # Frontend logic + API calls
│   └── requirements.txt       # Frontend dependencies
│
├── UI_ANALYSIS.md             # Detailed UI design analysis
├── README.md                  # This file
├── QUICKSTART.md              # Quick start guide
└── ARCHITECTURE.md            # Architecture documentation
```

## 🚀 Quick Start

### Step 1: Start Backend API

Open **Terminal 1**:

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python app.py
```

**Wait for**: `✓ Model initialized successfully!`

Backend: **http://localhost:5001**

### Step 2: Start Frontend UI

Open **Terminal 2**:

```bash
cd frontend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start frontend
python app.py
```

Frontend: **http://localhost:5000**

### Step 3: Use the Application

1. Open browser to: **http://localhost:5000**
2. **Upload an image** (click or drag & drop)
3. **Select mode**: Query, Caption, **Point**, or Detect
4. **Enter task**: e.g., "Click the login button"
5. **Click the arrow** button to process
6. **View results** with visual marker

## 🎯 Features

### UI Features
✅ **Moondream-inspired Design** - Dark, minimalist, professional  
✅ **Drag & Drop Upload** - Easy image uploading  
✅ **Mode Selection** - Query, Caption, Point, Detect  
✅ **Real-time Processing** - Live results with loading states  
✅ **Visual Markers** - Blue circle markers on results  
✅ **Responsive Layout** - Works on all screen sizes  
✅ **Toast Notifications** - User-friendly feedback  

### Technical Features
✅ **Microservices Architecture** - Separate frontend and backend  
✅ **RESTful API** - Clean API communication  
✅ **AI-Powered** - Holo2-4B vision-language model  
✅ **Coordinate Prediction** - Accurate GUI element localization  

## 🔌 API Endpoints

### Backend API (Port 5001)

#### `GET /health`
Check backend status

#### `POST /api/process`
Process image with AI model

**Request:**
```json
{
  "image": "data:image/png;base64,...",
  "task": "Click the button",
  "task_type": "click"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "task": "Click the button",
    "coordinates": {
      "x": 500,
      "y": 300,
      "x_pixel": 400.5,
      "y_pixel": 240.8
    },
    "processed_image": "data:image/png;base64,...",
    "image_width": 800,
    "image_height": 600
  },
  "processing_time": 376
}
```

## 🎨 UI Components

### Navigation
- **Top Bar**: Logo, theme toggles
- **Sidebar**: Playground, API Keys, Usage, Billing

### Main Content
- **Upload Area**: Click or drag & drop
- **Mode Buttons**: Query, Caption, Point, Detect
- **Task Input**: Text input with arrow button
- **Results Panel**: Split view with image and info

### Results Display
- **Left**: Annotated image with marker
- **Right**: Info panel with:
  - Mode badge (POINTING)
  - Task prompt
  - Response time
  - Coordinates (pixel and normalized)

## 🐛 Troubleshooting

### Cannot connect to backend
1. Check backend terminal for `✓ Model initialized`
2. Visit http://localhost:5001/health
3. Should return: `{"status": "healthy"}`

### Port already in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Model download fails
- Check internet connection
- Model is ~8GB, takes 10-15 minutes first time
- Check HuggingFace access

## 📦 Dependencies

### Backend
- Flask + Flask-CORS
- PyTorch + Transformers
- Pillow, Pydantic
- **~8GB model download on first run**

### Frontend
- Flask
- Pillow
- Requests
- **No AI model needed**

## 🔧 Configuration

### Change Backend URL

Edit `frontend/static/js/main.js`:
```javascript
const BACKEND_API_URL = 'http://localhost:5001'; // Change this
```

### Change Ports

**Backend**: Edit `backend/app.py`
```python
app.run(port=5001)
```

**Frontend**: Edit `frontend/app.py`
```python
app.run(port=5000)
```

## 📊 Performance

- **Backend**: GPU recommended (2-5x faster)
- **Frontend**: Lightweight, minimal resources
- **Response Time**: 300-1000ms (GPU), 2-5s (CPU)
- **Model**: Holo2-4B (~8GB)

## 🔄 Development

### Customize UI

**Colors**: Edit `frontend/static/css/style.css`
```css
/* Change colors at the top of the file */
background-color: #000000; /* Pure black */
color: #ffffff; /* White text */
```

**Layout**: Edit `frontend/templates/index.html`

**Behavior**: Edit `frontend/static/js/main.js`

### Add New Modes

The UI has 4 modes: Query, Caption, Point, Detect

Currently, only **Point** mode is connected to the backend.

To add other modes, implement them in `backend/model.py`

## 📸 Screenshots

The UI closely matches the Moondream interface:
- Dark, professional design
- Clean typography
- Blue accent colors for markers
- Minimal, distraction-free layout

## 📄 License

Provided as-is for educational and research purposes.

## 🙏 Credits

- **UI Design**: Inspired by Moondream
- **Model**: Holo2-4B by Hcompany
- **Framework**: Flask + PyTorch + Transformers

---

**Enjoy the Moondream-style interface!** 🌙

*Built with attention to design details*
