# MachinekitCLI
Command Line Interface for LinuxCNC

machine   on/off        : Turns Machine On/Off
estop     on/off        : On = Estop or Off = Resets Estop State

mdi XXX					:Sets to MDI Mode and Runs command
file  XXX               : Selects the file for Auto mode XXX must be full path (default is \home\machinekit\gcode\program.nc)
auto					:Sets to Auto Mode and Runs selected file from line 0
pos						:Outputs Axis Positions
home X					:Sets or starts Homing on axis (X is the axis number not name)

To use:
copy mkcli.py to \home\machinekit\machinekit-dev\bin\mkcli
in your .ini:
Comment out the current DISPLAY (#DISPLAY = axis or tkemc)
add DISPLAY = mkcli

TODO:
-Add ability to pick which line of program you want to start from in Auto
-Have pos only output axis that exist with axis names (i.e. axis.0=X then readout would be POS X=0.000)
-Add ability to home axis by name instead of number (i.e. home x = home.0 home y = home.1 etc)


