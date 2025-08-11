# capitalism-station
A test branch for SS14.

## Pushing Space Station 14 Content

This repository is configured to handle Space Station 14 content properly. To push your local `space-station-14` folder:

### Prerequisites
1. Make sure Git LFS is installed: `git lfs install`
2. Ensure you're on the correct branch

### Steps to Push
1. Copy your `space-station-14` folder into the root of this repository
2. Add the files: `git add space-station-14/`
3. Commit the changes: `git commit -m "Add space-station-14 content"`
4. Push to the repository: `git push origin [branch-name]`

### Large File Handling
This repository is configured with Git LFS to handle:
- Image files (.png, .jpg, .jpeg)
- Audio files (.ogg, .wav, .mp3)
- Resource files (.rsi)
- Binary files (.exe, .dll, .so, .dylib)

### Common Issues
- If you get "file too large" errors, make sure Git LFS is installed and initialized
- Build artifacts are automatically ignored - only source content will be tracked
- Some RobustToolbox resources are ignored to prevent conflicts
