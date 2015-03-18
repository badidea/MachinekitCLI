#!/usr/bin/python


## MachinekitCLI is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by the
## Free Software Foundation; either version 2 of the License, or (at your
## option) any later version.  MachinekitCLI is distributed in the hope 
## that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
## the GNU General Public License for more details.  You should have
## received a copy of the GNU General Public License along with MachinekitCLI;
## if not, write to the Free Software Foundation, Inc., 59 Temple Place,
## Suite 330, Boston, MA 02111-1307 USA
## 
## MachinekitClI is Copyright (C) David Marquart <dmarquart@gmail.com>
##

import sys, os
from cmd import Cmd
import linuxcnc

c = linuxcnc.command()
s = linuxcnc.stat()


class MachinekitCLI(Cmd):
    intro = 'Welcome to MachinekitCLI.   Type help or ? to list commands.\n'
    prompt = '(CNC) '
    file = None
    prog_file = ("/home/machinekit/gcode/program.ngc")
 
    def do_mdi(self, arg, opts=None):
        """Execute MDI command
               mdi (gcode here)"""
        mdi = ''.join(arg)
        c.mode(linuxcnc.MODE_MDI)
        c.wait_complete()
        c.mdi(mdi)
        c.wait_complete()
 
    def do_pos(self, arg, opts=None):
        """Outputs current absolute position.
              pos # outputs axis #
              pos   outputs all axis"""
        pos_n = ''.join(arg)
        s.poll()
        if pos_n is None:
            pos = str(s.position)
            self.stdout.write(pos + '\n')
        else:
            pos_ask = int(pos_n)
            pos = str(s.axis[pos_ask]['output'] + '\n')
            self.stdout.write(pos)

    def do_open(self, arg, opts=None):
        """Selects a file for execution.
                open /home/machinekit/gcode/program.ngc"""
        file_n = ''.join(arg)
        if os.path.exists(file_n):
            prog_file = file_n
        else:
            self.stdout.write('File not found.' + '\n')

    def do_program(self, arg, opts=None):
        """States currently open program."""
        self.stdout.write(prog_file + ' ' + 'is selected for auto mode.' + '\n')

    def do_program_status(self, arg, opts=None):
        """States current program status."""
        s.poll()
        status = s.interp_state
        if status == 1:
            self.stdout.write("IDLE" + '\n')
        if status == 2:
            self.stdout.write("READING" + '\n')
        if status == 3:
            self.stdout.write("PAUSED" + '\n')
        if status == 4:
            self.stdout.write("WAITING" + '\n')

    def do_program_line(self, arg, opts=None):
        """States current program line."""
        s.poll()
        read_line = str(s.read_line)
        self.stdout.write( read_line + ' is current line.' + '\n')
        
    def do_run(self, arg, opts=None):
        """Runs open file in auto.
               run # starts the program from the selected line number.
               run   starts from the first line."""
        p_line = int(''.join(arg))
        if p_line is None:
            program_start_line = 0
        else:
            program_start_line = p_line
        c.mode(linuxcnc.MODE_AUTO)
        c.wait_complete()
        c.program_open(self.prog_file)
        c.auto(linuxcnc.AUTO_RUN, program_start_line)
        c.wait_complete()
        
    def do_pause(self, arg, opts=None):
        """Pause program."""
        c.auto(linuxcnc.AUTO_PAUSE)
        c.wait_complete()
        
    def do_resume(self, arg, opts=None):
        """Resume program."""
        c.auto(linuxcnc.AUTO_RESUME)
        c.wait_complete()
        
    def do_step(self, arg, opts=None):
        """Execute single line of program."""
        c.auto(linuxcnc.AUTO_STEP)
        c.wait_complete()

    def do_home(self, arg, opts=None):
        """Starts homing of selected axis.
               home #    homes selected axis.
               home all  homes all axis."""
        home_n = ''.join(arg)
        if home_n is None:
            self.stdout.write('Which axis to home?  Use- axis #' + '\n')
        if home_n is 'all':
            self.stdout.write('Homing All Axis' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(0)
            c.home(1)
            c.home(2)
            c.home(3)
            c.home(4)
            c.home(5)
            c.home(6)
            c.home(7)
            c.home(8)
            c.wait_complete()
        else:    
            home_it = int(home_n)
            self.stdout.write('Homing Axis' + home_n + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(home_it)
            c.wait_complete()

    def do_unhome(self, arg, opts=None):
        """Unhomes selected axis.
               unhome #    unhomes selected axis.
               unhome all  unhomes all axis."""
        unhome_n = ''.join(arg)
        if unhome_n is None:
            self.stdout.write('Which axis to unhome?  Use- axis #' + '\n')
        if unhome_n is 'all':
            self.stdout.write('Unhoming All Axis' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.unhome(0)
            c.unhome(1)
            c.unhome(2)
            c.unhome(3)
            c.unhome(4)
            c.unhome(5)
            c.unhome(6)
            c.unhome(7)
            c.unhome(8)
            c.wait_complete()
        else:   
            unhome_it = int(home_n)
            self.stdout.write('Axis' + home_n + 'Unhomed' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.unhome(unhome_it)
            c.wait_complete()

    def do_feed_override(self, arg, opts=None):
        """Feed Override Percent 0-100."""
        f_ovr = int(''.join(arg))
        c.set_feed_override(f_ovr)
        
    def do_spindle_override(self, arg, opts=None):
        """Spindle Override Percent 0-100."""
        s_ovr = int(''.join(arg))
        c.set_spindle_override(s_ovr)

    # ----- basic cnc state commands -----
    def do_machine(self, arg, opts=None):
        """Turn Machine On/Off."""
        mach = ''.join(arg)
        if mach == "on":
            c.state(linuxcnc.STATE_ON)
        if mach == "off":
            c.state(linuxcnc.STATE_OFF)
            
    def do_estop(self, arg, opts=None):
        """Turn Estop On/Off"""
        es = ''.join(arg)
        if es == 'on':
            c.state(linuxcnc.STATE_ESTOP)
        if es == 'off':
            c.state(linuxcnc.STATE_ESTOP_RESET)
            
    def do_state(self, arg, opts=None):
        """Current Estop/Machine state."""
        s.poll()
        state = s.task_state
        if state == 1:
            self.stdout.write("Estop" + '\n')
        if state == 2:
            self.stdout.write("Estop is Reset" + '\n')
        if state == 3:
            self.stdout.write("Machine is Off" + '\n')
        if state == 4:
            self.stdout.write("Machine is On" + '\n')

    def do_set_mode(self, arg, opts=None):
        """Change mode to mdi, auto, or manual.
               set_mode mdi     sets to MDI
               set_mode manual  sets to MANUAL
               set_mode auto    sets to AUTO"""
        mode = ''.join(arg)
        if mode == 'auto':
            c.mode(linuxcnc.MODE_AUTO)
        if mode == 'manual':
            c.mode(linuxcnc.MODE_MANUAL)
        if mode == 'mdi':
            c.mode(linuxcnc.MODE_MDI)

    def do_get_mode(self, arg, opts=None):
        """States current mode."""
        s.poll()
        g_mode = s.task_mode
        if g_mode == 1:
            self.stdout.write("MANUAL" + '\n')
        if g_mode == 2:
            self.stdout.write("AUTO" + '\n')
        if g_mode == 3:
            self.stdout.write("MDI" + '\n')

    def do_studder(self, arg, opts=None):
        """AutoStartup, Home, and warmup"""
        c.state(linuxcnc.STATE_ON)
        c.mode(linuxcnc.MODE_MANUAL)
        c.wait_complete()
        c.home(0)
        c.home(1)
        c.home(2)
        c.home(3)
        c.home(4)
        c.home(5)
        c.home(6)
        c.home(7)
        c.home(8)
        c.wait_complete()
        c.mode(linuxcnc.MODE_MDI)
        c.wait_complete()
        c.mdi(m104 p210)
        c.wait_complete()
        c.mode(linuxcnc.MODE_AUTO)
        c.wait_complete()
        c.program_open(self.prog_file)
        c.auto(linuxcnc.AUTO_RUN, 0)
        c.wait_complete()
        c.mode(linuxcnc.MODE_MDI)
        c.wait_complete()
        c.mdi(x0 y0 z0)
        c.wait_complete()

            
    def do_exit(self, line): return True
    def do_quit(self, line): return True


mk = MachinekitCLI()
mk.cmdloop()
