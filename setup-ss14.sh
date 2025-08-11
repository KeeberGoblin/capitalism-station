#!/bin/bash
# Setup script for pushing Space Station 14 content to capitalism-station repository

echo "🚀 Setting up repository for Space Station 14 content..."

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS is not installed. Please install it first:"
    echo "   Ubuntu/Debian: sudo apt install git-lfs"
    echo "   Arch Linux: sudo pacman -S git-lfs"
    echo "   CentOS/RHEL: sudo yum install git-lfs"
    echo "   macOS: brew install git-lfs"
    echo "   Windows: Download from https://git-lfs.github.io/"
    exit 1
fi

# Initialize Git LFS
echo "🔧 Initializing Git LFS..."
git lfs install

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"

# Check if space-station-14 folder exists in the current directory
if [ -d "space-station-14" ]; then
    echo "✅ Found space-station-14 folder"
    
    # Show folder size
    FOLDER_SIZE=$(du -sh space-station-14 | cut -f1)
    echo "📏 Folder size: $FOLDER_SIZE"
    
    # Add the folder
    echo "📁 Adding space-station-14 folder to git..."
    git add space-station-14/
    
    # Show what will be committed
    echo ""
    echo "📋 Files to be committed:"
    git status --porcelain | grep space-station-14
    
    echo ""
    echo "🎉 Ready to commit and push!"
    echo "Run the following commands:"
    echo "  git commit -m 'Add space-station-14 content'"
    echo "  git push origin $CURRENT_BRANCH"
    echo ""
    echo "💡 Tip: If you encounter large file errors, make sure Git LFS is properly configured."
    
else
    echo "❌ space-station-14 folder not found in current directory"
    echo "Please copy your space-station-14 folder to: $(pwd)"
    echo ""
    echo "Example:"
    echo "  cp -r /path/to/your/space-station-14 ./"
    echo "  ./setup-ss14.sh"
    exit 1
fi