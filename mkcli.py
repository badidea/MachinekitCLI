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
from cmd2 import Cmd, make_option, options
import linuxcnc



class MachinekitCLI(Cmd):
    intro = 'Welcome to the test version of MachinekitCLI.   Type help or ? to list commands.\n'
    prompt = '(CNC Command) '
    Cmd.shortcuts.update({'&': 'cnccmd'})
    file = None
    prog_file = ("/home/machinekit/gcode/program.nc")

    @options([make_option('-m', '--machine', type="string", help="Machine On/Off"),
          make_option('-e', '--estop', type="string", help="Estop On/Off"),
          make_option('-f', '--file', type="string", help="File to Run in Auto")
            ])
 
    def __init__(self):
        Cmd.__init__(self)
        self.c = linuxcnc.command()
        self.s = linuxcnc.stat()
 
    def do_mdi(self, arg, opts=None):
        """execute MDI command"""
        mdi = ''.join(arg)
        self.c.mode(linuxcnc.MODE_MDI)
        c.wait_complete()
        self.c.mdi(mdi)
        c.wait_complete()
 
    def do_pos(self, arg, opts=None):
        self.s.poll()
        self.stdout.write(self.s.position)

    def do_file(self, args, opts=None):
        file_n = ''.join(arg)
        prog_file = opts.file

    def do_auto(self, arg, opts=None):
        program_start_line = 0
        """Open File and run in Auto"""
        c.mode(linuxcnc.MODE_AUTO)
        c.wait_complete()
        c.program_open(prog_file)
        c.auto(linuxcnc.AUTO_RUN, program_start_line)
        c.wait_complete()
 

    # ----- basic cnc state commands -----
    def do_machine(self, arg, opts=None):
        """Turn Machine On/Off."""
        arg = ''.join(arg)
        if opts.machine == "on":
            self.stdout.write('Machine On')
            self.stdout.write('\n')
            c.state(linuxcnc.STATE_ON)
        if opts.machine == "off":
            self.stdout.write('Machine Off')
            self.stdout.write('\n')
            c.state(linuxcnc.STATE_OFF)
    def do_estop(self, arg, opts=None):
        """Turn Estop On/Off"""
        arg = ''.join(arg)
        if opts.estop == "on":
            self.stdout.write('E-Stop On')
            self.stdout.write('\n')
            c.state(linuxcnc.STATE_ESTOP)
        if opts.estop == "off":
            self.stdout.write('E-Stop Off')
            self.stdout.write('\n')
            c.state(linuxcnc.STATE_ESTOP_RESET)
            

mk = MachinekitCLI()
mk.cmdloop()
