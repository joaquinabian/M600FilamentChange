# RewriteM600

Implement M600 for printers that can't support M600 by default.
M600 will stop the print and wait until you change and press resume.

This is a fork from a fork from the original [Octoprint plugin](https://plugins.octoprint.org/plugins/RewriteM600/) by Gustavo Cevallos.
The original code is not actually working and seems abandoned.
A fork from [rottev](https://github.com/rottev/RewriteM600) solved some original problems, and this repository is forked from there.

The code is being cleaned and pythonized.  
Currently, it does what I wanted from it in a Snapmaker:
- The print goes normal until it finds a M600 inserted with Cura (or manually).
- Retract few millimeters and moves z 10 mm to separate from the object.
- Inmediately moves to a parking position and retracts 55 mm of filament
  (In the snapmaker this is enough for extracting the filament from the printing head).
- Now you can put another filament, extrude using the Octoprint control to remove any residue from the old filament, and press continue in Octoprint.
- The head moves to the last position and continues printing


## Setup

For the moment the way I am considering is to replace the files from a canonical installation in Octoprint.

## Screenshots

![Screenshot](https://github.com/wgcv/plugins.octoprint.org/raw/gh-pages/assets/img/plugins/RewriteM600/M600-in-action.png
)

## Support

You can help this project by reporting issues, making PR.
