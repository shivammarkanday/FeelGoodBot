#!/bin/bash

echo "🔧 Setting up Python virtual environment for macOS..."

# Create virtual environment
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete. To activate the environment, run: source venv/bin/activate"
