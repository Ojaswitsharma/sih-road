#!/bin/bash
# Install all dependencies for the Streamlit SUMO simulator

echo "🔧 Installing dependencies for SUMO Streamlit App"
echo "=================================================="
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install Python pip first."
    exit 1
fi

# Install Streamlit
echo "📦 Installing Streamlit..."
pip install streamlit

# Install TraCI
echo "📦 Installing TraCI..."
pip install traci

# Check SUMO installation
echo ""
echo "🔍 Checking SUMO installation..."
if command -v sumo-gui &> /dev/null; then
    echo "✅ SUMO is installed: $(which sumo-gui)"
else
    echo "❌ SUMO not found. Please install SUMO:"
    echo "   sudo apt-get install sumo sumo-tools"
fi

# Check SUMO_HOME
echo ""
echo "🔍 Checking SUMO_HOME..."
if [ -z "$SUMO_HOME" ]; then
    echo "⚠️  SUMO_HOME not set. Setting to default..."
    export SUMO_HOME=/usr/share/sumo
    echo "   export SUMO_HOME=/usr/share/sumo"
    echo ""
    echo "💡 To make this permanent, add to ~/.bashrc:"
    echo "   echo 'export SUMO_HOME=/usr/share/sumo' >> ~/.bashrc"
else
    echo "✅ SUMO_HOME is set: $SUMO_HOME"
fi

# Verify installations
echo ""
echo "🧪 Verifying installations..."
echo ""

echo -n "Streamlit: "
if python3 -c "import streamlit" 2>/dev/null; then
    echo "✅ Installed"
else
    echo "❌ Not found"
fi

echo -n "TraCI: "
if python3 -c "import traci" 2>/dev/null; then
    echo "✅ Installed"
else
    echo "❌ Not found"
fi

echo ""
echo "=================================================="
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Run: streamlit run streamlit_app.py"
echo "2. Configure parameters in the sidebar"
echo "3. Click 'Generate Simulation Files'"
echo "4. Click 'Run Simulation'"
echo "5. Look for SUMO GUI window (opens separately)"
echo ""
