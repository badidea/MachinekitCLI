# MachinekitCLI
Command Line Interface for LinuxCNC

machine   on/off        :Turns Machine On/Off
estop     on/off        :On = Estop or Off = Resets Estop State
state					:Responds with current Estop or Machine power state (ie Estop, Estop Reset, Machine Off, Machine On)


mdi XXX					:Sets to MDI Mode and Runs command
open XXX                :Selects the file for Auto mode XXX must be full path (default is \home\machinekit\gcode\program.nc)
run X					:Sets to Auto Mode and Runs selected file.  If X is blank program will run from line 0, else will run from the line you choose.
pause					:Pause Auto Program running.
resume					:Resumes paused program.
step					:Single block (one step) through program
pos	X		    		:Outputs Axis Positions.  If X is left blank all axis will be displayed, else only the one you choose will be displayed.
home X					:Sets or starts Homing on axis (X is the axis number)
unhome X				:Unhomes an axis

To use:
copy mkcli.py to \home\machinekit\machinekit-dev\bin\mkcli
in your .ini:
Comment out the current DISPLAY (#DISPLAY = axis or tkemc)
add DISPLAY = mkcli
or:
I have been told that it can run independently and works.

Minor issues:
You may have to run dos2unix and chmod +x to get this to be executable.  

TODO:
-Name your axis (axis.0 = x, axis.1 = y) without changing the code.  For now you will need to open file in test editor and change it. 


