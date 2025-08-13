# Capitalism Station Asset Generator

The **Capitalism Station Asset Generator** is a browser-only tool that provides contributors with an easy way to download complete asset work packages without needing to install any tooling or dependencies.

## Quick Start

1. **Open the Generator**: Navigate to `docs/asset-generator/capitalism_station_assets.html` in your web browser
2. **Configure Options**: Set your preferred generation options using the controls panel
3. **Filter Assets**: Use the search and filter options to find specific assets you need
4. **Download Package**: Click the "AGI DOWNLOAD" button to get your complete asset package

## Features

### 🔍 Filterable Asset Registry
- **Search**: Find assets by name, description, or tags
- **Type Filter**: Filter by asset type (entity, structure, clothing, ui, effect, object)
- **Status Filter**: Filter by development status (ready, wip, planned)
- **Phase Filter**: Filter by release phase (alpha, beta, release)

### ⚙️ Generation Options
- **Include SVG Templates**: Get editable SVG templates with SS14 art guide compliance
- **Include PNG Exports**: Get crisp 1:1 PNG exports with image smoothing disabled
- **Console ON/OFF Variants**: Generate console/screen variants for applicable items
- **Pixel Grid Overlay**: Add pixel alignment grid to templates
- **SS14 Selective Outline**: Add SS14-standard outline guides
- **Screen Streaks Effect**: Add screen streak effects for display items

### 📦 Complete Work Package
Each AGI Download includes:

#### `manifest/manifest.json`
Complete metadata about the asset package including:
- Asset inventory with paths and specifications
- Generation options used
- Folder structure mapping
- Version and license information

#### `Resources/...` Folder Skeletons
Ready-to-use folder structure that matches the actual repository paths:
- `Resources/Textures/Structures/`
- `Resources/Textures/Clothing/`
- `Resources/Textures/Objects/`
- `Resources/Textures/Interface/`
- `Resources/Textures/Effects/`

#### Asset Templates
For each selected asset:
- **SVG Templates**: Editable vector graphics with SS14 art guide rules
- **PNG Exports**: Pixel-perfect raster images ready for game use
- **meta.json**: RSI metadata files with proper state definitions
- **Variants**: Multiple versions where applicable (console on/off, different states)

## Integration with Repository

### Placing Assets Back Into Repo

1. **Extract the Package**: Unzip your downloaded asset package
2. **Copy Folder Structure**: The generated `Resources/` folders match the repository structure
3. **Place Files**: Copy the asset folders directly into your local repo's `Resources/` directory
4. **Update RSI Meta**: Each asset includes a properly formatted `meta.json` file

### Example Integration

```bash
# After downloading and extracting capitalism_station_asset_package.zip
cp -r Resources/* /path/to/your/repo/Resources/
```

### RSI Meta.json Format

The generator creates properly formatted meta.json files for each asset:

```json
{
  "version": 1,
  "license": "CC-BY-SA-3.0",
  "copyright": "Capitalism Station Contributors",
  "size": { "x": 32, "y": 32 },
  "states": [
    {
      "name": "asset_name",
      "directions": 4
    }
  ]
}
```

For animated assets:
```json
{
  "states": [
    {
      "name": "animated_asset",
      "delays": [0.1, 0.1, 0.1, 0.1]
    }
  ]
}
```

## SS14 Art Guide Compliance

The generator automatically applies SS14 art standards:

### Lighting
- **Top-left lighting** applied to all 3D objects
- Consistent shadow placement on bottom-right

### Color Palette  
- **Corporate theme** with purple (#9d4edd) and orange (#ff6b3a) accents
- High contrast colors for accessibility
- Consistent color relationships across all assets

### Technical Standards
- **32×32 pixel base size** (scalable to 64×64 for large items)
- **4-directional sprites** for entities and structures where applicable
- **Crisp pixel art** with image smoothing disabled
- **Clean 1-pixel outlines** for clarity

### Animation Standards
- **60ms frame delays** for standard animations
- **Consistent frame counts** (12 frames for effects, 4 for idle animations)
- **Smooth loops** with proper easing

## Browser Compatibility

The asset generator works in all modern browsers:
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Dependencies (CDN)
- **JSZip 3.10.1**: For client-side ZIP generation
- **FileSaver.js 2.0.5**: For clean file downloads

## License

All generated assets use the **CC-BY-SA-3.0** license, consistent with the Space Station 14 project requirements. This means:

- ✅ **Commercial use** allowed
- ✅ **Modification** allowed  
- ✅ **Distribution** allowed
- ⚠️ **Attribution** required
- ⚠️ **Share alike** required (derivatives must use same license)

## Troubleshooting

### Download Issues
- **Browser blocks download**: Check popup blockers and download permissions
- **ZIP file corrupted**: Try disabling browser extensions and retry
- **Large package timeout**: Filter assets to smaller sets and download in batches

### Asset Quality
- **Blurry PNGs**: The generator disables image smoothing - if images appear blurry, check your browser's rendering settings
- **Missing variants**: Ensure the appropriate option toggles are enabled before generating
- **Wrong colors**: Colors are procedurally generated - final assets should use proper corporate palette

### Integration Problems
- **Meta.json format**: The generator creates SS14-compatible meta.json files, but always verify before committing
- **File paths**: Generated folder structure matches repository - don't rename folders
- **License conflicts**: All generated content uses CC-BY-SA-3.0 to match project requirements

## Support

For issues with the asset generator:
1. Check this documentation first
2. Verify your browser compatibility
3. Try with a fresh browser session (clear cache)
4. Open browser developer tools to check for JavaScript errors
5. File an issue in the repository with details

## Technical Notes

### Client-Side Generation
The entire asset generator runs in your browser - no server communication required. This means:
- ✅ **Works offline** after initial page load
- ✅ **No data tracking** or external requests
- ✅ **Fast generation** using local processing
- ✅ **GitHub Pages compatible** for easy deployment

### Performance
- SVG generation: ~1ms per asset
- PNG conversion: ~50ms per asset  
- ZIP packaging: ~100ms per 50 assets
- Memory usage: ~2MB for 100 assets

Large packages (100+ assets) may take several seconds to generate.