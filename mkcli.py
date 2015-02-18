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
    intro = 'Welcome to the test version of MachinekitCLI.   Type help or ? to list commands.\n'
    prompt = '(CNC) '
    file = None
    prog_file = ("/home/machinekit/gcode/program.nc")
 
    def do_mdi(self, arg, opts=None):
        """execute MDI command"""
        mdi = ''.join(arg)
        c.mode(linuxcnc.MODE_MDI)
        c.wait_complete()
        c.mdi(mdi)
        c.wait_complete()
 
    def do_pos(self, arg, opts=None):
        pos_n = ''.join(arg)
        s.poll()
        if pos_n is None:
            pos = str(s.position)
            self.stdout.write(pos + '\n')
        else:
            pos_ask = int(pos_n)
            pos = str(s.axis[pos_ask]['output'])
            self.stdout.write(pos)

    def do_open(self, arg, opts=None):
        file_n = ''.join(arg)
        if os.path.exists(file_n):
            prog_file = file_n
            self.stdout.write(file_n + ' ' + 'is selected for auto mode.' + '\n')
        else:
            self.stdout.write('File not found.' + '\n')

    def do_run(self, arg, opts=None):
        p_line = int(''.join(arg))
        if p_line >= 1:
            program_start_line = p_line
        else:
            program_start_line = 0
        """Open File and run in Auto"""
        c.mode(linuxcnc.MODE_AUTO)
        c.wait_complete()
        c.program_open(self.prog_file)
        c.auto(linuxcnc.AUTO_RUN, program_start_line)
        c.wait_complete()
        
    def do_pause(self, arg, opts=None):
        c.auto(linuxcnc.AUTO_PAUSE)
        c.wait_complete()
        
    def do_resume(self, arg, opts=None):
        c.auto(linuxcnc.AUTO_RESUME)
        c.wait_complete()
        
    def do_step(self, arg, opts=None):
        c.auto(linuxcnc.AUTO_STEP)
        c.wait_complete()

    def do_home(self, arg, opts=None):
        home_n = ''.join(arg)
        home_it = int(home_n)
        self.stdout.write('Homing Axis' + home_n + '\n')
        c.mode(linuxcnc.MODE_MANUAL)
        c.wait_complete()
        c.home(home_it)
        c.wait_complete()

    def do_unhome(self, arg, opts=None):
        unhome_n = ''.join(arg)
        unhome_it = int(home_n)
        self.stdout.write('Axis' + home_n + 'Unhomed' + '\n')
        c.mode(linuxcnc.MODE_MANUAL)
        c.wait_complete()
        c.unhome(unhome_it)
        c.wait_complete()
 

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
        if es == "on":
            c.state(linuxcnc.STATE_ESTOP)
        if es == "off":
            c.state(linuxcnc.STATE_ESTOP_RESET)
    def do_state(self, arg, opts=None):
        s.poll()
        state = str(s.task_state)
        if state == "1":
            self.stdout.write("Estop" + '\n')
        if state == "2":
            self.stdout.write("Estop is Reset" + '\n')
        if state == "3":
            self.stdout.write("Machine is Off" + '\n')
        if state == "4":
            self.stdout.write("Machine is On" + '\n')



            
    def do_exit(self, line): return True
    def do_quit(self, line): return True


mk = MachinekitCLI()
mk.cmdloop()
