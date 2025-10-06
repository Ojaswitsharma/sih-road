#!/bin/bash
# Quick start script for Streamlit Indian Road Simulator

echo "🚗 Indian Road Pothole Simulator - Streamlit Interface"
echo "======================================================"
echo ""

# Check if SUMO_HOME is set
if [ -z "$SUMO_HOME" ]; then
    echo "⚠️  Warning: SUMO_HOME is not set"
    echo "   Setting to default: /usr/share/sumo"
    export SUMO_HOME=/usr/share/sumo
fi

# Check if SUMO is installed
if ! command -v sumo &> /dev/null; then
    echo "❌ Error: SUMO is not installed"
    echo "   Please install SUMO first:"
    echo "   sudo apt-get install sumo sumo-tools"
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Installing Streamlit..."
    pip install -r requirements_streamlit.txt
fi

# Check if OSM file exists
if [ ! -f "mymap.osm" ]; then
    echo "❌ Error: mymap.osm not found"
    echo "   Please ensure the OSM file exists in the current directory"
    exit 1
fi

echo "✅ All prerequisites met"
echo "🚀 Starting Streamlit app..."
echo ""
echo "   The app will open in your browser at http://localhost:8501"
echo "   Press Ctrl+C to stop the server"
echo ""

# Run streamlit
streamlit run streamlit_app.py
