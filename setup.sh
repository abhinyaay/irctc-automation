#!/bin/bash

# IRCTC Automation Bot Setup Script
echo "🚂 IRCTC Tatkal Booking Bot Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment (optional but recommended)
read -p "Do you want to create a virtual environment? (y/N): " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run setup test
echo "🧪 Running setup tests..."
python3 test_setup.py

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit config.py with your IRCTC credentials and journey details"
echo "2. Run the bot: python3 main.py"
echo "3. Or test the setup: python3 test_setup.py"
echo ""
echo "📚 For more information, check README.md"
echo ""
echo "⚠️  Legal Reminder: Use this bot responsibly and in compliance with IRCTC's terms of service."
