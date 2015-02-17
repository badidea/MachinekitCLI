# MachinekitCLI
Command Line Interface for LinuxCNC

-m, machine, --machine on/off  : Turns Machine On/Off
-e, estop, --estop on/off   : Estops or Resets Estop State
-f XXX, file XXX, --file XXX   : Selects the file for Auto mode XXX must be full 
					   path (default is \home\machinekit\gcode\program.nc)
mdi XXX					:Sets to MDI Mode and Runs command
auto					:Sets to Auto Mode and Runs selected file from line 0
pos						:Outputs Axis Positions

TODO:
-Add ability to pick which line of program you want to start from in Auto
-Have pos only output axis that exist with axis names (i.e. axis.0=X then readout would be POS X=0.000)


