# MachinekitCLI
Command Line Interface for LinuxCNC

View instructions.txt for how to use this command line ui.  Most commands match linuxcncrsh.


To install as display:
copy mkcli.py to \home\machinekit\machinekit-dev\bin\mkcli
in your .ini:
Comment out the current DISPLAY (#DISPLAY = axis or tkemc)
add DISPLAY = mkcli

Added bonus:
To help clear up error clutter comment out:
#INTRO_GRAPHIC = XXXX
#INTRO_TIME = 5
This gets rid of the cannot start xsession error in the linuxcnc boot.

or:
I have been told that it can run seperately with another display already running.

Minor issues:
You may have to run dos2unix and chmod +x to get this to be executable.  



