# Zbrush Addon

This adds integration to Pixologic ZBrush. Pixologic ZBrush is a digital sculpting software which users can do 3D/2.5D modeling, texturing and painting.

## Settings
Path to Zbrush executable must be set in the Ayon Setting in `Applications` addon (`ayon+settings://applications/applications/zbrush`) and added in `Anatomy`.`Attributes` for particular project to be visible in the Launcher.

### Implemented workflows
Currently supports importing/exporting models and saving/opening/publishing workfiles in Zbrush integration. All the associated data would be stored in `.zbrushmetadata` folder

## Steps for current installation
1. Copy `.ayon_zbrush` to `./client/ayon_core/hosts` in the core addon
2. Copy `.server` to `.server_addon/zbrush` in the core addon.
3. Create packages for core addon and server_addon respectively
4. Install the zbrush addon and the latest core addon
5. Edit `Applications` addon (`ayon+settings://applications/applications/zbrush`) to set the path to Zbrush executable.
