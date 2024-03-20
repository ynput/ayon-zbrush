# Zbrush Addon

This adds integration to Pixologic ZBrush. Pixologic ZBrush is a digital sculpting software which users can do 3D/2.5D modeling, texturing and painting.

## Settings
Path to Zbrush executable must be set in the Ayon Setting in `Applications` addon (`ayon+settings://applications/applications/zbrush`) and added in `Anatomy`.`Attributes` for particular project to be visible in the Launcher.

### Implemented workflows
Currently supports importing/exporting models and saving/opening/publishing workfiles in Zbrush integration. All the associated data would be stored in `.zbrushmetadata` folder

## How to start
There is a `create_package.py` python file which contains logic how to create the addon from AYON codebase. Just run the code.
```shell
python ./create_package.py


