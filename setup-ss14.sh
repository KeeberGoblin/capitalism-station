#!/bin/bash
# Setup script for pushing Space Station 14 content to capitalism-station repository

echo "Setting up repository for Space Station 14 content..."

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS is not installed. Please install it first:"
    echo "   Ubuntu/Debian: sudo apt install git-lfs"
    echo "   Arch Linux: sudo pacman -S git-lfs"
    echo "   macOS: brew install git-lfs"
    exit 1
fi

# Initialize Git LFS
echo "🔧 Initializing Git LFS..."
git lfs install

# Check if space-station-14 folder exists in the current directory
if [ -d "space-station-14" ]; then
    echo "✅ Found space-station-14 folder"
    
    # Add the folder
    echo "📁 Adding space-station-14 folder to git..."
    git add space-station-14/
    
    # Check for any issues
    git status
    
    echo ""
    echo "Ready to commit and push!"
    echo "Run the following commands:"
    echo "  git commit -m 'Add space-station-14 content'"
    echo "  git push origin $(git branch --show-current)"
else
    echo "❌ space-station-14 folder not found in current directory"
    echo "Please copy your space-station-14 folder to: $(pwd)"
    exit 1
fi