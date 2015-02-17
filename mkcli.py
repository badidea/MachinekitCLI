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
    prompt = '(CNC Command) '
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
        s.poll()
        self.stdout.write(s.position)

    def do_file(self, arg, opts=None):
        file_n = ''.join(arg)
        if os.path.exists(file_n):
            prog_file = file_n
            self.stdout.write(file_n + ' ' + 'is selected for auto mode.' + '\n')
        else:
            self.stdout.write('File not found.' + '\n')

    def do_auto(self, arg, opts=None):
        program_start_line = 0
        """Open File and run in Auto"""
        c.mode(linuxcnc.MODE_AUTO)
        c.wait_complete()
        c.program_open(self.prog_file)
        c.auto(linuxcnc.AUTO_RUN, program_start_line)
        c.wait_complete()


    def do_home(self, arg, opts=None):
        home_n = ''.join(arg)
        if home_n == "0":
            self.stdout.write('Homing Axis.0' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(0)
            c.wait_complete()
        if home_n  == "1":
            self.stdout.write('Homing Axis.1' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(1)
            c.wait_complete()
        if home_n  == "2":
            self.stdout.write('Homing Axis.2' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(2)
            c.wait_complete()
        if home_n  == "3":
            self.stdout.write('Homing Axis.3' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(3)
            c.wait_complete()
        if home_n  == "4":
            self.stdout.write('Homing Axis.4' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(4)
            c.wait_complete()
        if home_n  == "5":
            self.stdout.write('Homing Axis.5' + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(5)
            c.wait_complete()
 

    # ----- basic cnc state commands -----
    def do_machine(self, arg, opts=None):
        """Turn Machine On/Off."""
        mach = ''.join(arg)
        if mach == "on":
            self.stdout.write('Machine On' + '\n')
            c.state(linuxcnc.STATE_ON)
        if mach == "off":
            self.stdout.write('Machine Off' + '\n')
            c.state(linuxcnc.STATE_OFF)
    def do_estop(self, arg, opts=None):
        """Turn Estop On/Off"""
        es = ''.join(arg)
        if es == "on":
            self.stdout.write('E-Stop On' + '\n')
            c.state(linuxcnc.STATE_ESTOP)
        if es == "off":
            self.stdout.write('E-Stop Off' + '\n')
            c.state(linuxcnc.STATE_ESTOP_RESET)
    def do_exit(self, arg, opts=None):
        "Exit"


mk = MachinekitCLI()
mk.cmdloop()
