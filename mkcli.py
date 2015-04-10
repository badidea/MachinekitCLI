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

import sys, os, threading
from time import sleep
from cmd import Cmd
import linuxcnc

c = linuxcnc.command()
s = linuxcnc.stat()

"""Change the following for auto start/shutdown"""
studder_start = 0
kill_at_complete = 0
prog_file = ("/home/machinekit/gcode/program.ngc")

class MachinekitCLI(Cmd):
    intro = 'Welcome to MachinekitCLI.   Type help or ? to list commands.\n'
    prompt = '(CNC) '
 
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
        s.poll()
        pos_n = ''.join(arg)
        try:
            int(pos_n)
            pos_ask = int(pos_n)
            pos = str(s.axis[pos_ask]['output'])
            self.stdout.write("Axis " + pos_n + "=" + " " + pos + '\n')
        except ValueError:
            if pos_n is '':
                pos0 = str(s.axis[0]['output'])
                pos1 = str(s.axis[1]['output'])
                pos2 = str(s.axis[2]['output'])
                pos3 = str(s.axis[3]['output'])
                pos4 = str(s.axis[4]['output'])
                pos5 = str(s.axis[5]['output'])
                pos6 = str(s.axis[6]['output'])
                pos7 = str(s.axis[7]['output'])
                self.stdout.write("Axis 0=" + pos0 + '\n')
                self.stdout.write("Axis 1=" + pos1 + '\n')
                self.stdout.write("Axis 2=" + pos2 + '\n')
                self.stdout.write("Axis 3=" + pos3 + '\n')
                self.stdout.write("Axis 4=" + pos4 + '\n')
                self.stdout.write("Axis 5=" + pos5 + '\n')
                self.stdout.write("Axis 6=" + pos6 + '\n')
                self.stdout.write("Axis 7=" + pos7 + '\n')
            else:
                if pos_n == 'all':
                    pos = str(s.position)
                    self.stdout.write(pos + '\n')
                else:
                    self.stdout.write('Invalid Position Command' + '\n')

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
        if s.interp_state == 1: self.stdout.write("IDLE" + '\n')
        if s.interp_state == 2: self.stdout.write("READING" + '\n')
        if s.interp_state == 3: self.stdout.write("PAUSED" + '\n')
        if s.interp_state == 4: self.stdout.write("WAITING" + '\n')

    def do_exec_state(self, arg, opts=None):
        """States task execution state."""
        s.poll()
        if s.exec_state == 1: self.stdout.write("Exec Error" + '\n')
        if s.exec_state == 2: self.stdout.write("Exec Done" + '\n')
        if s.exec_state == 3: self.stdout.write("Exec Waiting for Motion" + '\n')
        if s.exec_state == 4: self.stdout.write("Exec Waiting for Queue" + '\n')
        if s.exec_state == 5: self.stdout.write("Exec Waiting for Pause" + '\n')
        if s.exec_state == 6: self.stdout.write("Exec Waiting for Motion and IO" + '\n')
        if s.exec_state == 7: self.stdout.write("Exec Waiting for Delay" + '\n')
        if s.exec_state == 8: self.stdout.write("Exec Waiting for System CMD" + '\n')

    def do_program_line(self, arg, opts=None):
        """States current program line."""
        s.poll()
        read_line = str(s.read_line)
        self.stdout.write( read_line + ' is current line.' + '\n')
        
    def do_run(self, arg, opts=None):
        """Runs open file in auto.
               run # starts the program from the selected line number.
               run   starts from the first line."""
        p_line = ''.join(arg)
        try:
            int(p_line)
            program_start_line = int(p_line)
        except ValueError:
            if p_line == '':
                program_start_line = 0
            else:
                self.stdout.write('Invalid Program Start Command' + '\n')
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

    def do_abort(self, arg, opts=None):
        """Abort program."""
        c.abort()
        c.wait_complete()

    def do_reset(self, arg, opts=None):
        """Reset Interpreter"""
        c.reset_interpreter()
        c.wait_complete()

    def do_opstop(self, arg, opts=None):
        """Turn Optional Stop on/off"""
        op = ''.join(arg)
        if op == 'on':
            c.optional_stop(1)
            c.wait_complete()
        if op == 'off':
            c.optional_stop(0)
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
        try:
            int(home_n)
            home_it = int(home_n)
            self.stdout.write('Homing Axis ' + home_n + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.home(home_it)
            c.wait_complete()
        except ValueError:
            if home_n is '':
                self.stdout.write('Which axis to home?  Use- axis # or all' + '\n')
            else:
                if home_n == 'all':
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
                else:
                    self.stdout.write('Invalid Homing Command' + '\n')

    def do_unhome(self, arg, opts=None):
        """Unhomes selected axis.
               unhome #    unhomes selected axis.
               unhome all  unhomes all axis."""
        home_n = ''.join(arg)
        try:
            int(home_n)
            home_it = int(home_n)
            self.stdout.write('Unhoming Axis ' + home_n + '\n')
            c.mode(linuxcnc.MODE_MANUAL)
            c.wait_complete()
            c.unhome(home_it)
            c.wait_complete()
        except ValueError:
            if home_n is '':
                self.stdout.write('Which axis to unhome?  Use- axis # or all' + '\n')
            else:
                if home_n == 'all':
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
                else:
                    self.stdout.write('Invalid Unhoming Command' + '\n')
                    
    def do_feed_override(self, arg, opts=None):
        """Feed Override Percent 0-100."""
        f_ovr = ''.join(arg)
        try:
            int(f_ovr)
            c.set_feed_override(f_ovr)
        except ValueError:
            self.stdout.write('Invalid Feed Override Command' + '\n')
        
        
    def do_spindle_override(self, arg, opts=None):
        """Spindle Override Percent 0-100."""
        s_ovr = ''.join(arg)
        try:
            int(s_ovr)
            c.set_spindle_override(s_ovr)
        except ValueError:
            self.stdout.write('Invalid Spindle Override Command' + '\n')

    # ----- basic cnc state commands -----
    def do_machine(self, arg, opts=None):
        """Turn Machine On/Off."""
        mach = ''.join(arg)
        if mach == "on": c.state(linuxcnc.STATE_ON)
        if mach == "off": c.state(linuxcnc.STATE_OFF)
            
    def do_estop(self, arg, opts=None):
        """Turn Estop On/Off"""
        es = ''.join(arg)
        if es == 'on': c.state(linuxcnc.STATE_ESTOP)
        if es == 'off': c.state(linuxcnc.STATE_ESTOP_RESET)
            
    def do_state(self, arg, opts=None):
        """Current Estop/Machine state."""
        s.poll()
        if s.task_state == 1: self.stdout.write("Estop" + '\n')
        if s.task_state == 2: self.stdout.write("Estop is Reset" + '\n')
        if s.task_state == 3: self.stdout.write("Machine is Off" + '\n')
        if s.task_state == 4: self.stdout.write("Machine is On" + '\n')

    def do_set_mode(self, arg, opts=None):
        """Change mode to mdi, auto, or manual.
               set_mode mdi     sets to MDI
               set_mode manual  sets to MANUAL
               set_mode auto    sets to AUTO"""
        mode = ''.join(arg)
        if mode == 'auto': c.mode(linuxcnc.MODE_AUTO)
        if mode == 'manual': c.mode(linuxcnc.MODE_MANUAL)
        if mode == 'mdi': c.mode(linuxcnc.MODE_MDI)

    def do_get_mode(self, arg, opts=None):
        """States current mode."""
        s.poll()
        if s.task_mode == 1: self.stdout.write("MANUAL" + '\n')
        if s.task_mode == 2: self.stdout.write("AUTO" + '\n')
        if s.task_mode == 3: self.stdout.write("MDI" + '\n')

    def do_studder(self, arg, opts=None):
        """AutoStartup, Home, and warmup"""
        file_n = ''.join(arg)
        if os.path.exists(file_n):
            prog_file = file_n
        else:
            self.stdout.write('File not found.' + '\n')
        c.state(linuxcnc.STATE_ON)
        c.wait_complete()
        self.do_home('all')
        while s.axis[0]['homed'] == 0 or s.axis[1]['homed'] == 0 or s.axis[2]['homed'] == 0:
            sleep(2)
            s.poll()
        self.do_mdi('m104 p210')
        s.poll()
        while s.interp_state == 2:
            sleep(2)
            s.poll()
        self.do_run('')

            
    def do_exit(self, line): return True
    def do_quit(self, line): return True


mk = MachinekitCLI()
if studder_start == 1:
    mk.do_studder(prog_file)
    if kill_at_complete == 0:
        mk.cmdloop()
    else:
        mk.do_exit()
else:
    mk.cmdloop()
