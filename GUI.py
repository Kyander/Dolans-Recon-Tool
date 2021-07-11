import tkinter as tk
import tkinter.ttk as ttk
import subprocess
from tkinter.messagebox import showwarning
import nmap3
import argparse
import os
import threading
from ftplib import FTP
from bs4 import BeautifulSoup, Comment
import requests
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from functools import partial



'''
CHECK BOX CUSTOM CLASS
'''

check_nu = b'iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TRZEWB4uIOGSoTi2IijpKFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi4uqk6CIl/i8ptIjx4Lgf7+497t4BQqPCVLNrHFA1y0jFY2I2tyr2vCKAIAYRwYzETD2RXszAc3zdw8fXuyjP8j735wgqeZMBPpF4jumGRbxBPL1p6Zz3iUOsJCnE58QRgy5I/Mh12eU3zkWHBZ4ZMjKpeeIQsVjsYLmDWclQiaeIw4qqUb6QdVnhvMVZrdRY6578hYG8tpLmOs0RxLGEBJIQIaOGMiqwEKVVI8VEivZjHv5hx58kl0yuMhg5FlCFCsnxg//B727NwuSEmxSIAd0vtv0xCvTsAs26bX8f23bzBPA/A1da219tALOfpNfbWvgI6N8GLq7bmrwHXO4AQ0+6ZEiO5KcpFArA+xl9Uw4YuAX61tzeWvs4fQAy1NXyDXBwCIwVKXvd4929nb39e6bV3w/0UXLbKEvbjQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+MMDRctIGmzOYIAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAALElEQVQoz2M0Njb+z0AiYGFgYGA4c+YMI7EaTExM/jMxkAFGNQ1jTYzkpD0ATtMHS/nRiQwAAAAASUVORK5CYII='
check_nc = b'iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TRZEWB4uIOGSoTi2IijpKFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi4uqk6CIl/i8ptIjx4Lgf7+497t4BQqPCVLNrHFA1y0jFY2I2tyr2vCKAIAYRwYzETD2RXszAc3zdw8fXuyjP8j735wgqeZMBPpF4jumGRbxBPL1p6Zz3iUOsJCnE58QRgy5I/Mh12eU3zkWHBZ4ZMjKpeeIQsVjsYLmDWclQiaeIw4qqUb6QdVnhvMVZrdRY6578hYG8tpLmOs0RxLGEBJIQIaOGMiqwEKVVI8VEivZjHv5hx58kl0yuMhg5FlCFCsnxg//B727NwuSEmxSIAd0vtv0xCvTsAs26bX8f23bzBPA/A1da219tALOfpNfbWvgI6N8GLq7bmrwHXO4AQ0+6ZEiO5KcpFArA+xl9Uw4YuAX61tzeWvs4fQAy1NXyDXBwCIwVKXvd4929nb39e6bV3w/0UXLbKEvbjQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+MMDRctDrVlNE0AAAAjdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVAgd2l0aCBsb3ZlyGW0XgAAAJdJREFUKM+d0rENAyEMBdDvKA1zeART07MIGzAFE7EDK1B5CMqf7pIUlyP3JZdP+rItZkb8mScAjDFkF8QY+cCNbCF3R86ZvXduIXdHKYWqipSSXKJP0FqTEMK7Xu+dOWe6+yU4UEpJVBWlFLr7TwAAYmYcY8haC7VWzjkBAGfga+UhBLTWRFVPwREzI0nsjpndO67c+b0XBDxvkWRMW24AAAAASUVORK5CYII='


class CustomCheckboxText(tk.Frame):
    def __init__(self, parent, colour, text, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.checkbox = CustomCheckbox(self, colour, *args, **kwargs)
        self.checkbox.grid(row=0, column=0)
        self.label = tk.Label(self, text=text)
        self.label.grid(row=0, column=1)

        self.label.bind("<Enter>", self.checkbox.focus_in)
        self.label.bind("<Leave>", self.checkbox.focus_out)
        self.label.bind("<Button-1>", self.on_label_click)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def on_label_click(self, event=None):
        if self.checkbox.variable.get() == self.checkbox['onvalue']:
            self.checkbox.variable.set(self.checkbox['offvalue'])
        else:
            self.checkbox.variable.set(self.checkbox['onvalue'])
        self.checkbox.focus_update()

    def select(self):
        self.checkbox.select()

    def get(self):
        return self.checkbox.variable.get()


class CustomCheckbox(tk.Checkbutton):
    def __init__(self, parent, colour, *args, **kwargs):
        default_kwargs = {'image': None, 'selectimage': None, 'indicatoron': False,
                          'onvalue': 1, 'offvalue': 0, 'variable': None, 'offrelief': 'sunken'}
        for key, value in default_kwargs.items():
            if key not in kwargs:
                kwargs[key] = value

        self.colour = colour
        self.curr_colour = "black"
        self.hover = False
        if kwargs['variable'] is None:
            self.variable = kwargs['variable'] = tk.IntVar(value=1)
        else:
            self.variable = kwargs['variable']
        print(kwargs, kwargs['variable'].get())
        if kwargs['variable'].get() == 0:
            if kwargs['image'] is None:
                self.off_image = kwargs['image'] = tk.PhotoImage(data=check_nu)
            else:
                self.off_image = kwargs['image']
            if kwargs['selectimage'] is None:
                self.on_image = tk.PhotoImage(data=check_nc)
            else:
                self.on_image = kwargs['selectimage']
        else:
            if kwargs['image'] is None:
                self.on_image = kwargs['image'] = tk.PhotoImage(data=check_nc)
            else:
                self.on_image = kwargs['image']
            if kwargs['selectimage'] is None:
                self.off_image = tk.PhotoImage(data=check_nu)
            else:
                self.off_image = kwargs['selectimage']

        tk.Checkbutton.__init__(self, parent, *args, **kwargs)
        self.bind("<Enter>", self.focus_in)
        self.bind("<Leave>", self.focus_out)
        self.variable.trace("w", self.focus_update)

    def select(self):
        """Put the button in on-state."""
        self.tk.call(self._w, 'select')

    def edit_check(self, colour, image):
        image.put((colour,), to=(0, 0, 1, 13))  # LEFT
        image.put((colour,), to=(0, 0, 13, 1))  # TOP
        image.put((colour,), to=(12, 0, 13, 13))  # RIGHT
        image.put((colour,), to=(0, 12, 13, 13))  # BOTTOM

    def focus_in(self, event=None):
        image = self.on_image if self.variable.get() == self['onvalue'] else self.off_image
        self.edit_check(self.colour, image)
        self.curr_colour = self.colour
        self.configure(image=image)
        self.image = image
        self.hover = True

    def focus_out(self, event=None):
        image = self.on_image if self.variable.get() == self['onvalue'] else self.off_image
        self.edit_check("black", image)
        self.curr_colour = "black"
        self.configure(image=image)
        self.image = image
        self.hover = False

    def focus_update(self, *args):

        if self.variable.get() == self['onvalue']:
            image = self.on_image
        else:
            image = self.off_image
        self.configure(image=image)
        self.image = image
        if self.hover:
            self.focus_in()


'''
TOOLTIP CLASS
'''


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


global ibuster, inikto
ibuster = 0
inikto = 0

global busterList, niktoList
niktoList = []
busterList = []

global smbCheckCmd
global bruteSMBcmd
global bruteFTPcmd
global bruteSSHcmd


def nikto_switcher(frame):
    global inikto
    if inikto > 3:
        inikto = 0
    else:
        pass
    raise_frame(frame["nikto"][inikto])
    inikto += 1


def buster_switcher(frame):
    global ibuster
    if ibuster > 3:
        ibuster = 0
    else:
        pass
    raise_frame(frame["buster"][ibuster])
    ibuster += 1


def raise_frame(frame):
    frame.tkraise()


class MenuHandler:
    def __init__(self, tkobj):
        self.tkobj = tkobj
        self.menu_creation()

    def menu_creation(self):
        self.menu_dict = {}
        for name in ('nikto', 'buster', 'brute_smb', 'brute_ssh', 'brute_ftp', 'spray_show', 'smb_checker'):
            m = Menu(self.tkobj, tearoff=0)
            m.add_command(label="Force Stop", command=partial(option_selected, 'fs', name))
            m.add_command(label="Force Restart", command=partial(option_selected, 'fr', name))
            self.menu_dict[name] = m

    def nikto_event(self, event):
        self.menu_dict['nikto'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['nikto'].focus_set()


class MainWindow:
    def __init__(self, tkobj, root_dir):

        self.root_dir = root_dir
        self.tkObj = tkobj

        self.tkObj.protocol("WM_DELETE_WINDOW", self.on_exit)  # Overwrite exit function for tkinter

        # build ui
        self.create_styles()
        self.create_frames()
        self.create_buttons()
        self.get_frames_id()
        self.create_menus()
        self.create_menus_binds()


        self.funcDict = {"smb_checker":self.smb_check,"brute_smb":self.brute_smb,"brute_ftp":self.brute_ftp,"brute_ssh":self.brute_ssh,"spray_show":self.spraying_show, "nikto":self.nikto, "dirbuster":self.dirbuster}
        # Main widget
        self.b_spray_show.pack_forget()
        self.spList = {}
        self.niktoList = []
        self.dirbustList = [] # subprocess list so we can end each of them on exit.
        self.spNothingList = []
        self.spawn_xterms()

    def create_menus(self):
        self.menu_dict = {}
        for name in ('nikto', 'buster', 'brute_smb', 'brute_ssh', 'brute_ftp', 'spray_show', 'smb_checker'):
            m = Menu(self.tkObj, tearoff=0)
            m.add_command(label="Force Stop", command=partial(self.option_selected, 'fs', name))
            m.add_command(label="Force Restart", command=partial(self.option_selected, 'fr', name))
            self.menu_dict[name] = m

    def option_selected(self, mode, name):
        print("MODE : {}\nNAME : {}".format(mode, name))

        if mode == "fr":
            if name == "nikto":
                for service in self.niktoList:
                    service.terminate()
                self.funcDict["nikto"]()
            elif name == "buster":
                for service in self.dirbustList:
                    service.terminate()
                self.funcDict["dirbuster"]()
            for srv in self.spList:
                if srv == name:
                    self.spList[srv].terminate()
                    self.funcDict[srv]()
                else:
                    pass
        elif mode == "fs":
            if name == "nikto":
                for service in self.niktoList:
                    service.terminate()
            elif name == "buster":
                for service in self.dirbustList:
                    service.terminate()
            for srv in self.spList:
                if srv == name:
                    self.spList[srv].terminate()
                else:
                    pass

    '''
    Need to find a way to dynamically create the _event functions!
    '''
    def spray_show_event(self, event):
        self.menu_dict['spray_show'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['spray_show'].focus_set()

    def nikto_event(self, event):
        self.menu_dict['nikto'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['nikto'].focus_set()

    def dirbust_event(self, event):
        self.menu_dict['buster'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['buster'].focus_set()

    def smb_checker_event(self, event):
        self.menu_dict['smb_checker'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['smb_checker'].focus_set()

    def brute_smb_event(self, event):
        self.menu_dict['brute_smb'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['brute_smb'].focus_set()

    def brute_ftp_event(self, event):
        self.menu_dict['brute_ftp'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['brute_ftp'].focus_set()

    def brute_ssh_event(self, event):
        self.menu_dict['brute_ssh'].tk_popup(event.x_root, event.y_root)
        self.menu_dict['brute_ssh'].focus_set()

    def create_menus_binds(self):
        for btn, func in zip([self.b_dirbust, self.b_smb_checker, self.b_brute_smb, self.b_brute_ssh, self.b_brute_ftp,
                              self.b_nikto, self.b_spray_show],
                             [self.dirbust_event, self.smb_checker_event, self.brute_smb_event, self.brute_ssh_event,
                              self.brute_ftp_event, self.nikto_event, self.spray_show_event]):
            btn.bind("<Button-3>", func)

    def get_frames_id(self):
        self.niktoFrames = [self.frame_dict['nikto1'], self.frame_dict['nikto2'], self.frame_dict['nikto3'],
                            self.frame_dict['nikto4']]
        self.busterFrames = [self.frame_dict['buster1'], self.frame_dict['buster2'], self.frame_dict['buster3'],
                             self.frame_dict['buster4']]
        self.frameDict = {"nikto": self.niktoFrames, "buster": self.busterFrames}
        self.idListBuster = [self.frame_dict['buster1'].winfo_id(), self.frame_dict['buster2'].winfo_id(),
                             self.frame_dict['buster3'].winfo_id(), self.frame_dict['buster4'].winfo_id()]
        self.idListNikto = [self.frame_dict['nikto1'].winfo_id(), self.frame_dict['nikto2'].winfo_id(),
                            self.frame_dict['nikto3'].winfo_id(), self.frame_dict['nikto4'].winfo_id()]
        self.frame_id_dict = {}
        for frame in ('creds_write', 'spray_show', 'smb_checker', 'brute_smb', 'brute_ftp', 'brute_ssh', 'read_nmap'):
            id = self.frame_dict[frame].winfo_id()
            self.frame_id_dict[frame] = id

    def create_styles(self):
        bactionstyle = ttk.Style()
        bactionstyle.configure("Mine.TButton", background="red")

    def create_frames(self):

        self.frame_dict = {}

        self.mainFrame = ttk.Frame()
        self.mainFrame.configure(height='200', width='200')
        self.mainFrame.pack(side='top')

        self.btn_frame = ttk.Frame(self.mainFrame)
        self.btn_frame.configure(height='200', width='200')
        self.btn_frame.grid(column='0', row='1')

        for name in ('creds_write', 'smb_checker', 'spray_show', 'nikto1', 'nikto2', 'nikto3',
                     'nikto4', 'buster1', 'buster2', 'buster3', 'buster4', 'brute_ssh', 'brute_ftp',
                     'brute_smb', 'read_nmap'):
            frame = ttk.Frame(self.mainFrame)
            frame.configure(height='600', width='600')
            frame.grid(column='1', row='1')
            self.frame_dict[name] = frame

    def spawn_xterms(self):
        self.nikto()
        self.dirbuster()
        self.read_nmap()
        self.brute_smb()
        self.smb_check()
        self.brute_ssh()
        self.brute_ftp()

    def nikto(self):
        try:
            print("Starting Nikto\n")
            i = 0
            for cmd in niktoList:
                self.niktoList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idListNikto[i]), "-geometry", "100x100", "-hold", "-e",
                     "{} & wait".format(cmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                i += 1
            if i < 4:
                newi = 4 - i
                for notAv in range(0, newi):
                    if i == 5:
                        break
                    else:
                        pass
                    self.niktoList.append(subprocess.Popen(
                        ["xterm", "-into", str(self.idListNikto[i]), "-geometry", "100x100", "-hold", "-e",
                         "echo '[!] Nothing here!'"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                    i += 1
        except:
            self.b_nikto.pack_forget()

    def smb_check(self):
        global smbCheckCmd
        try:
            print("Starting SmbCheck\n")
            self.spList["smb_checker"] = subprocess.Popen(
                ["xterm", "-into", str(self.frame_id_dict['smb_checker']), "-geometry", "100x100", "-hold", "-e",
                 "{} & wait".format(smbCheckCmd)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except:
            self.b_smb_checker.pack_forget()

    def brute_smb(self):
        global bruteSMBcmd
        try:
            print("Starting SmbBrute\n")
            self.spList["brute_smb"] = subprocess.Popen(
                ["xterm", "-into", str(self.frame_id_dict['brute_smb']), "-geometry", "100x100", "-hold", "-e",
                 "{} & wait".format(bruteSMBcmd)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except:
            self.b_brute_smb.pack_forget()

    def brute_ftp(self):
        global bruteFTPcmd
        try:
            print("Starting FtpBrute\n")
            self.spList["brute_ftp"] = subprocess.Popen(
                ["xterm", "-into", str(self.frame_id_dict['brute_ftp']), "-geometry", "100x100", "-hold", "-e",
                 "{} & wait".format(bruteFTPcmd)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except Exception as e:
            print(e)
            self.b_brute_ftp.pack_forget()

    def brute_ssh(self):
        global bruteSSHcmd
        try:
            print("Starting SshBrute\n")
            self.spList["brute_ssh"] = subprocess.Popen(
                ["xterm", "-into", str(self.frame_id_dict['brute_ssh']), "-geometry", "100x100", "-hold", "-e",
                 "{} & wait".format(bruteSSHcmd)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except:
            self.b_brute_ssh.pack_forget()

    def read_nmap(self):
        try:
            self.spNothingList.append(subprocess.Popen(
                ["xterm", "-into", str(self.frame_id_dict['read_nmap']), "-geometry", "100x100", "-hold", "-e",
                 "cat {}/nmap/nmap_scan.txt".format(self.root_dir)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE))
        except:
            pass

    def dirbuster(self):
        try:
            print("Starting Dirbuster\n")
            i = 0
            for cmd in busterList:
                self.dirbustList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idListBuster[i]), "-geometry", "100x100", "-hold", "-e",
                     "{} & wait".format(cmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                # print(cmd)
                i += 1
            if i < 4:
                newi = 4 - i
                for notAv in range(0, newi):
                    if i == 5:
                        break
                    else:
                        pass
                    self.dirbustList.append(subprocess.Popen(
                        ["xterm", "-into", str(self.idListBuster[i]), "-geometry", "100x100", "-hold", "-e",
                         "echo '[!] Nothing here!'"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                    i += 1
        except:
            self.b_dirbust.pack_forget()

    def create_buttons(self):
        # Sadly cant use a for loop here
        self.b_nmap_read = ttk.Button(self.btn_frame)
        self.b_nmap_read.configure(text='View NMAP')
        self.b_nmap_read.configure(command=lambda: raise_frame(self.frame_dict['read_nmap']))
        self.b_nmap_read.pack(side='top')

        self.b_actions = ttk.Button(self.btn_frame, style="Mine.TButton")
        self.b_actions.configure(text='Actions')
        self.b_actions.pack(pady='50', side='bottom')
        self.b_actions.configure(command=self.action_window)

        self.b_spray_show = ttk.Button(self.btn_frame)
        self.b_spray_show.configure(text='Spraying')
        self.b_spray_show.pack(side='top')
        self.b_spray_show.configure(command=lambda: raise_frame(self.frame_dict['spray_show']))

        self.b_nikto = ttk.Button(self.btn_frame)
        self.b_nikto.configure(text='Nikto')
        self.b_nikto.pack(side='top')
        self.b_nikto.configure(command=lambda: nikto_switcher(self.frameDict))

        self.b_brute_ssh = ttk.Button(self.btn_frame)
        self.b_brute_ssh.configure(text='SSH Brute')
        self.b_brute_ssh.configure(command=lambda: raise_frame(self.frame_dict['brute_ssh']))
        self.b_brute_ssh.pack(side='top')

        self.b_brute_ftp = ttk.Button(self.btn_frame)
        self.b_brute_ftp.configure(text='FTP Brute')
        self.b_brute_ftp.configure(command=lambda: raise_frame(self.frame_dict['brute_ftp']))
        self.b_brute_ftp.pack(side='top')

        self.b_brute_smb = ttk.Button(self.btn_frame)
        self.b_brute_smb.configure(text='SMB Brute')
        self.b_brute_smb.configure(command=lambda: raise_frame(self.frame_dict['brute_smb']))
        self.b_brute_smb.pack(side='top')

        self.b_dirbust = ttk.Button(self.btn_frame)
        self.b_dirbust.configure(text='Dirbuster')
        self.b_dirbust.configure(command=lambda: buster_switcher(self.frameDict))
        self.b_dirbust.pack(side='top')

        self.b_smb_checker = ttk.Button(self.btn_frame)
        self.b_smb_checker.configure(text='SMBCheck')
        self.b_smb_checker.configure(command=lambda: raise_frame(self.frame_dict['smb_checker']))
        self.b_smb_checker.pack(side='top')

    def spraying_show(self):
        self.b_spray_show.pack()
        self.mainFrame.lift()
        # print("Running sprayingShow")
        try:
            self.sprayingCmd = sprayingCmd
        except:
            messagebox.showerror("Error", message="You need to set the credentials first.")
            self.action_window.lift()
        # print(self.sprayingCmd)
        try:
            self.spList["spray_show"] = subprocess.Popen(
                ["xterm", "-into", str(self.frame_id_dict['spray_show']), "-geometry", "100x100", "-hold", "-e",
                 "{} & wait".format(self.sprayingCmd)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except:
            self.b_spray_show.pack_forget()

    def on_exit(self):
        for service in self.spList:
            self.spList[service].terminate()
        for service in self.spNothingList:
            service.terminate()
        for service in self.dirbustList:
            service.terminate()
        for service in self.niktoList:
            service.terminate()



    def action_window(self):
        global action_window
        # Toplevel object which will
        # be treated as a new window
        try:
            if action_window.state() == "normal":
                action_window.lift()
        except:
            action_window = Toplevel(self.mainFrame)
            action_window.frame2 = ttk.Frame(action_window)
            action_window.atctions = ttk.Label(action_window.frame2)
            action_window.atctions.configure(text='Action Launcher')
            action_window.atctions.pack(side='top')
            action_window.separatorLine = ttk.Separator(action_window.frame2)
            action_window.separatorLine.configure(orient='horizontal')
            action_window.separatorLine.pack(fill='x', side='top')
            action_window.frame2.configure(height='22', width='500')
            action_window.frame2.pack(side='top')
            action_window.frame2.pack_propagate(0)
            action_window.frame4 = ttk.Frame(action_window)
            action_window.bspray = ttk.Button(action_window.frame4)
            action_window.bspray.configure(text='Sprayer')
            action_window.bspray.configure(command=self.spraying_show)
            action_window.bspray.pack(pady='20', side='top')
            action_window.bCredsWrite = ttk.Button(action_window.frame4)
            action_window.bCredsWrite.configure(text='Write Credentials')
            action_window.bCredsWrite.configure(command=self.writeCredsWindows)
            action_window.bCredsWrite.pack(pady='20', side='top')
            action_window.button4 = ttk.Button(action_window.frame4)
            action_window.button4.configure(state='disabled', text='Launch owasp zap')
            action_window.button4.pack(side='top')
            action_window.frame4.configure(height='200', width='500')
            action_window.frame4.pack(side='bottom')
            action_window.frame4.pack_propagate(0)
            self.action_window = action_window

    def writeCredsWindows(self):
        global writeCredsWindow
        global sprayMode
        self.mode = tk.IntVar()
        if os.path.exists("{}/credsWrite.txt".format(self.root_dir)):
            with open("{}/credsWrite.txt".format(self.root_dir), "r") as d:
                data = d.read()
        else:
            data = '''admin\nroot\nuser\npassword'''
        try:
            if self.writeCredsWindow.state() == "normal": self.writeCredsWindow.lift()
        except:
            self.writeCredsWindow = Toplevel(self.action_window)
            self.writeCredsWindow.frame4 = ttk.Frame(self.writeCredsWindow)
            self.writeCredsWindow.frame5 = ttk.Frame(self.writeCredsWindow.frame4)
            self.writeCredsWindow.sprayList = tk.Text(self.writeCredsWindow.frame5)
            self.writeCredsWindow.sprayList.configure(height='10', width='50')
            _text_ = data
            self.writeCredsWindow.sprayList.insert('0.0', _text_)
            self.writeCredsWindow.sprayList.grid(column='0', row='0')
            self.writeCredsWindow.frame8 = ttk.Frame(self.writeCredsWindow.frame5)
            self.writeCredsWindow.checkPassOnly = CustomCheckboxText(self.writeCredsWindow.frame8, "black",
                                                                     "Password Only", onvalue=1, variable=self.mode)
            # self.writeCredsWindow.checkPassOnly.configure(text='Password Only')
            self.writeCredsWindow.checkPassOnly.pack(side='bottom')
            self.writeCredsWindow.checkuserOnly = CustomCheckboxText(self.writeCredsWindow.frame8, "black",
                                                                     "Username Only", onvalue=2, variable=self.mode)
            # self.writeCredsWindow.checkuserOnly.configure(text='Username Only')
            self.writeCredsWindow.checkuserOnly.pack(side='bottom')
            self.writeCredsWindow.checkCombo = CustomCheckboxText(self.writeCredsWindow.frame8, "black",
                                                                  "Combo Mode (user:pass)", onvalue=3,
                                                                  variable=self.mode)
            # self.writeCredsWindow.checkCombo.configure(text='Combo Mode (user:pass)')
            self.writeCredsWindow.checkCombo.pack(side='bottom')
            self.writeCredsWindow.checkLP = CustomCheckboxText(self.writeCredsWindow.frame8, "black",
                                                               "User as passowrd", onvalue=4, variable=self.mode)
            # self.writeCredsWindow.checkLP.configure(text='User as passowrd')
            self.writeCredsWindow.checkLP.pack(side='bottom')
            ttpUserOnly = CreateToolTip(self.writeCredsWindow.checkuserOnly,
                                        "This will use the usernames you provide and our wordlist as passwords")
            ttpPassOnly = CreateToolTip(self.writeCredsWindow.checkPassOnly,
                                        "This will use the passwords you provide and our wordlist as usernames")
            self.writeCredsWindow.label2 = ttk.Label(self.writeCredsWindow.frame8)
            self.writeCredsWindow.label2.configure(text='Spraying Options')
            self.writeCredsWindow.label2.pack(side='top')
            self.writeCredsWindow.separator1 = ttk.Separator(self.writeCredsWindow.frame8)
            self.writeCredsWindow.separator1.configure(orient='horizontal')
            self.writeCredsWindow.separator1.pack(fill='x', pady='10', side='top')
            self.writeCredsWindow.frame8.configure(height='200', width='200')
            self.writeCredsWindow.frame8.grid(column='1', row='0')
            self.writeCredsWindow.frame5.configure(height='200', width='200')
            self.writeCredsWindow.frame5.pack(side='top')
            self.writeCredsWindow.frame7 = ttk.Frame(self.writeCredsWindow.frame4)
            self.writeCredsWindow.Bsave = ttk.Button(self.writeCredsWindow.frame7)
            self.writeCredsWindow.Bsave.configure(text='Save')
            self.writeCredsWindow.Bsave.configure(command=self.save)
            self.writeCredsWindow.Bsave.grid(column='0', padx='20', pady='5', row='0')
            self.writeCredsWindow.frame7.configure(height='200', width='200')
            self.writeCredsWindow.frame7.pack(side='top')
            self.writeCredsWindow.frame4.configure(height='200', width='200')
            self.writeCredsWindow.frame4.pack(side='right')
            try:
                if sprayMode == "passOnly":
                    self.writeCredsWindow.checkPassOnly.select()
                elif sprayMode == "userOnly":
                    self.writeCredsWindow.checkuserOnly.select()
                elif sprayMode == "comboMode":
                    self.writeCredsWindow.checkCombo.select()
                elif sprayMode == "User as Password":
                    self.writeCredsWindow.checkLP.select()
                else:
                    pass
            except:
                pass

    def on_exit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit? Stuff might break"):
            for service in self.spList:
                self.spList[service].terminate()
            for service in self.spNothingList:
                service.terminate()
            for service in self.dirbustList:
                service.terminate()
            for service in self.niktoList:
                service.terminate()
            self.tkObj.destroy()

    def save(self):
        global sprayMode
        global result
        if self.mode.get() == 0:
            messagebox.showerror("Missing Parameters", message="Please select 1 spraying mode.")
            self.writeCredsWindow.lift()
        else:
            if self.mode.get() == 1:
                sprayMode = "passOnly"
            elif self.mode.get() == 2:
                sprayMode = "userOnly"
            elif self.mode.get() == 3:
                sprayMode = "comboMode"
            elif self.mode.get() == 4:
                sprayMode = "User as Password"
            else:
                messagebox.showerror("Error", message="Something wrong happened.")
                self.writeCredsWindow.lift()
            result.createCommandSpraying()
            with open("{}/credsWrite.txt".format(self.root_dir), "w+") as f:
                f.write(self.writeCredsWindow.sprayList.get("1.0", END))
                f.close()

    def lol(self):
        pass

    def run(self):
        self.mainFrame.mainloop()


def doNikto(logfile, url):
    global niktoList
    newlogfile = logfile.replace('dirbust', 'nikto')
    rootfile = logfile.split("dirbust")[0]
    # print(rootfile)
    # print(newlogfile)
    try:
        os.mkdir("{}/nikto".format(rootfile))
    except:
        pass
    # cords =cordsManager("nikto")
    command = "nikto -host={} -o {}".format(url, newlogfile)
    niktoList.append(command)
    # os.system("xterm -T 'Nikto!' -geometry {} -e {}".format(cords,command))


def commentGrabber(logfile, host, dir):
    global commentsExists
    try:
        os.mkdir("{}/html".format(dir))  # Creates the "HTML" directory
    except:
        pass
    fileComments = os.path.join("{}/html/".format(dir), "comments.txt")  # the comments.txt path

    with open(logfile) as a:  # Puts every gobusted findings from the file inside a list
        content = a.readlines()

    content = [x.strip() for x in content]
    urls = []

    for file in content:  # Creates the urls (appends gobusted findings to url) for requests
        fileFormat = file.split(' ')[0]
        urls.append("{}{}".format(host, fileFormat))

    if commentsExists == False:
        f = open(fileComments, "w+")  # Creates the comments.txt file
        f.write("ALL THE COMMENTS EXTRACTED :\n\n")
        f.close()
        commentsExists = True
    else:
        pass
    for url in urls:  # Grabs all comments and writes it to comments.txt
        r = requests.get(url, verify=False)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        f = open(fileComments, "a")
        f.write("{} :\n\n".format(url))
        f.close()
        for x in soup.findAll(text=lambda text: isinstance(text, Comment)):
            f = open(fileComments, "a")
            f.write(x)
            f.close()


def bust(url, wordlist, logfile, dir):  # THIS IS THE THREADED FUNCTION
    global busterList
    command = "python3 ./busterScript.py --url {} --wordlist {} --output {} --rootDir {}".format(url, wordlist, logfile,
                                                                                                 dir)
    busterList.append(command)
    # cords = cordsManager("dirbust")
    # os.system("xterm -T 'dirbuster!' -geometry {} -e {}".format(cords,command))


def dirbuster(urls, wordlist, logfiles, dir):  # This starts the threads, passing it all it needs.
    i = 0
    for url in urls:
        tnikto = threading.Thread(target=doNikto, args=(logfiles[i], url,))  # FOR NIKTO!
        tdirbust = threading.Thread(target=bust, args=(url, wordlist, logfiles[i], dir))  # FOR DIRBUST!
        tdirbust.start()
        tnikto.start()
        i += 1


def smbCheck(host, rootDir):
    global smbCheckCmd
    command = "python3 smbCheck.py --host {} --output {}".format(host, rootDir)
    smbCheckCmd = command
    # os.system("xterm -T 'SMB Checker!' -geometry 90x30+0+1080 -hold -e {}".format(command))


class nmapScan:
    '''
    __INIT__ :
    Initiate the nmap3 object and host variable.
    Do an -sV scan and save it to self.result.
    Format the result into a list self.openPorts.

    '''

    def __init__(self, host, root_dir, *args, **kwargs):
        global debug  # Boolean to skip nmap scan
        try:
            os.mkdir(os.path.join(root_dir, "nmap"))
        except:
            pass
        self.root_dir = root_dir  # This is where all the files of the scan will be outputed
        # self.webServices = ["Microsoft IIS httpd", "Apache httpd", "nginx", "Apache Tomcat", "MiniServ",
        #                   "lighttpd","Microsoft HTTPAPI httpd","http-proxy",'httpd','http']
        self.webServices = ["http-proxy", 'httpd', 'http']
        # Let's only do common webservices.
        self.host = host
        self.nmap = nmap3.Nmap()
        if debug == 1:
            self.result = {'192.168.89.55': {'osmatch': {}, 'ports': [{'protocol': 'tcp', 'portid': '21', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'ftp', 'product': 'FileZilla ftpd', 'version': '0.9.41 beta', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '80', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.43', 'extrainfo': '(Win64) OpenSSL/1.1.1g PHP/7.4.6', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.43'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '135', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '139', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'netbios-ssn', 'product': 'Microsoft Windows netbios-ssn', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '443', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.43', 'extrainfo': '(Win64) OpenSSL/1.1.1g PHP/7.4.6', 'tunnel': 'ssl', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.43'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '445', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'microsoft-ds', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '3306', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'mysql', 'servicefp': 'SF-Port3306-TCP:V=7.91%I=7%D=7/1%Time=60DE0494%P=x86_64-pc-linux-gnu%r(NULL04Host);', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '5040', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'unknown', 'method': 'table', 'conf': '3'}, 'scripts': []}], 'hostname': [], 'macaddress': None, 'state': {'state': 'up', 'reason': 'echo-reply', 'reason_ttl': '127'}}, 'stats': {'scanner': 'nmap', 'args': '/usr/bin/nmap -oX - -sV -p- -oN /home/Kyand/testing/reconScript/nmap/nmap_scan.txt 192.168.55.55', 'start': '1625162777', 'startstr': 'Thu Jul  1 14:06:17 2021', 'version': '7.91', 'xmloutputversion': '1.05'}, 'runtime': {'time': '1625163065', 'timestr': 'Thu Jul  1 14:11:05 2021', 'summary': 'Nmap done at Thu Jul  1 14:11:05 2021; 1 IP address (1 host up) scanned in 287.67 seconds', 'elapsed': '287.67', 'exit': 'success'}}
        else:
            print("[!] nmap scan is running...\n")
            self.result = self.nmap.nmap_version_detection(self.host, args="-p- -oN {}/nmap/nmap_scan.txt".format(
                root_dir))  # -sV -p- -oN (rootDir/nmap_scant.txt) scan
            print(self.result)
            print("[!] nmap scan has completed!\n")
            # print(self.result)
        self.openPorts = []
        for ports in self.result[self.host]["ports"]:
            self.openPorts.append(ports)

    def createCommandSpraying(self):
        global sprayingCmd
        global sprayMode
        services = []
        for port in self.openPorts:
            try:  # If dictionary does not have "product" key, skip. (Theres probably a better way to do this)
                services.append(port['service']['name'])
            except:
                pass
        stringServices = ""
        for service in services:
            stringServices += "{},".format(service)

        sprayingCmd = "python3 sprayer.py {}/credsWrite.txt {} {} {} '{}'".format(root_dir, self.host, stringServices,
                                                                                  root_dir, sprayMode)

    def tbruteSMB(self):
        global bruteSMBcmd
        try:
            os.mkdir("{}/brute".format(root_dir))  # Creates the "brute" directory
        except:
            pass
        bruteSMBcmd = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} smb -o {}/brute/SMB.txt -I".format(
            host, root_dir)
        # print(bruteSMBcmd)
        # os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords, command))

    def tsmbCheck(self):
        global smbCheckCmd
        smbCheckCmd = "python3 smbCheck.py --host {} --output {}".format(self.host, self.root_dir)

    '''
    Runs funct
    '''

    def check(self, dWordList):
        global SSL
        global allBrute
        for port in self.result[self.host]['ports']:
            print(port)
            number = port['portid']
            if number == "443":
                SSL = True
            else:
                SSL = False

        self.dirbust(dWordList)  # Does dirbust AND extracts comments
        for port in self.result[self.host]['ports']:
            number = port['portid']
            try:
                if number == "21" or port['service']['name'].lower() == 'ftp':
                    self.checkFTP(port['portid'])
                elif number == "22":
                    if allBrute == 1:
                        self.tBruteSSH()
                    else:
                        answ = input("[!] Do you wish to bruteforce SSH? (y/n)\n")
                        if answ == "y":
                            self.tBruteSSH()
                        else:
                            pass
                    pass

                elif number == "445":
                    if allBrute == 1:
                        self.tbruteSMB()
                    else:
                        answ = input("[!] Do you wish to bruteforce SMB? (y/n)\n")
                        if answ == "y":
                            self.tbruteSMB()
                        else:
                            pass
                    self.tsmbCheck()
                    pass
                else:
                    pass
            except:
                pass

    '''
    portScan:
    Simply returns the list of openPorts

    Example use :

    host = "10.10.10.204"
    result = nmapScan(host).listOpenPorts()
    for r in result:
        print(r)    
    '''

    def listOpenPorts(self):
        return self.openPorts

    def tBruteSSH(self):
        global bruteSSHcmd
        try:
            os.mkdir("{}/brute".format(self.root_dir))  # Creates the "brute" directory
        except:
            pass
        bruteSSHcmd = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} ssh -o {}/brute/SSH.txt -I".format(
            self.host, self.root_dir)
        # os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords, command))

    def tBruteFTP(self, port):
        global bruteFTPcmd
        try:
            os.mkdir("{}/brute".format(self.root_dir))  # Creates the "brute" directory
        except:
            pass
        bruteFTPcmd = "hydra -s {} -t 20 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ftp://{} -o {}/brute/FTP.txt -I ".format(
            str(port),self.host, self.root_dir)
        # print(bruteFTPcmd)
        # os.system("xterm -T 'bruteforcing FTP!' -geometry 90x30+1920+1080 -e {}".format(command))

    '''
    Do regular FTP checks (check anon login, check perms)

    '''

    def checkFTP(self, port):
        global allBrute
        # print("ALLBRUTE : {}".format(allBrute))
        rootDir = os.path.join(self.root_dir, "ftp")  # /ftp directory
        try:
            os.mkdir(os.path.join(self.root_dir, "ftp"))  # Create /ftp directory
        except:
            pass
        f = open("{}/results.txt".format(rootDir), "w+")  # Create results.txt file
        ftp = FTP()  # initate ftp object
        ftp.connect(self.host, int(port))
        try:  # Check anonymous login
            ftp.login()
            f.write("Ftp anonymous : [WORKS]\n")
            f.close()
            if allBrute == 1:

                self.tBruteFTP(int(port))
            else:
                answ = input("[!] FTP anonymous works, do you still want to bruteforce it? (y/n)\n")
                if answ == "y":
                    self.tBruteFTP()
                else:
                    pass
            try:  # test file upload (creates test.jpg, trys to upload it, removes it, writes in results.txt)
                fileTest = open('test.jpg', 'w+')
                ftp.storbinary('STOR kitten.jpg', fileTest)
                fileTest.close()
                os.remove('test.jpg')
                f = open("{}/results.txt".format(rootDir), "a")
                f.write("File upload : [WORKS]\n")
                f.close()

            except:
                f = open("{}/results.txt".format(rootDir), "a")
                f.write("File upload : [FAILED]\n")
                f.close()



        except Exception as e:
            if allBrute == 1:
                self.tBruteFTP(int(port))
            else:
                answ = input("[!] FTP anonymous works, do you still want to bruteforce it? (y/n)\n")
                if answ == "y":
                    self.tBruteFTP(int(port))
                else:
                    pass
            f.write("Ftp anonymous : [FAILED]\n")
            f.close()
            pass

    '''
    Returns dictionary of PORT:SERVICE_NAME

    Example use :

    host = "10.10.10.204"
    result = nmapScan(host).services()
    print(result)
    '''

    def listServices(self):
        self.servicesDict = {}
        for port in self.openPorts:
            try:  # If dictionary does not have "product" key, skip. (Theres probably a better way to do this)
                self.servicesDict[port['portid']] = port['service']['name']
            except:
                pass
        return self.servicesDict  # dictionary PORT:SERVICE_NAME

    '''
    Used by dirbust function, creates log files. (Full path + name which is PORT_dirbust.txt)

    '''

    def createLogFiles(self, dir):
        self.logFiles = []  # list of full path
        try:
            os.mkdir(os.path.join(dir, "dirbust"))
        except:
            pass
        for url in self.urls:  # Creates full path
            if SSL == True:
                port = "SSL"
            else:
                port = url.split(":")[2]
            name = "{}.txt".format(port)
            self.logFiles.append("{}/dirbust/{}".format(dir, name))
        return self.logFiles  # Return list

    '''
    This is the function that when called, will run a dirbuster on each webservice.

    It needs a wordlist file, thats it!

    Needs https support to be added.
    '''

    def dirbust(self, wordfile):
        self.webServicePorts = []  # list of ports that are running http services
        self.urls = []  # list of url + port ready to dirbust.
        serviceList = self.listServices()  # Gets a list of the services.
        for port in serviceList:
            if serviceList[port] in self.webServices:  # If service_name is a web service
                self.webServicePorts.append(port)  # append the port to list
            else:
                pass
        for port in self.webServicePorts:  # Create url for dirbust.
            if SSL == True:
                if port == "80":
                    url = "https://{}".format(self.host)
                else:
                    url = "https://{}:{}".format(self.host, port)
            else:
                url = "http://{}:{}".format(self.host, port)
            self.urls.append(url)
        logFiles = self.createLogFiles(self.root_dir)  # Creates logFile Paths
        dirbuster(self.urls, wordfile, logFiles, self.root_dir)  # Starts the threads


if __name__ == '__main__':
    global allBrute
    global host
    global debug
    global result
    '''
    Argparse stuff (Comment out when debugging)

    '''

    parser = argparse.ArgumentParser(description="ReconScript")
    parser.add_argument('-I', '--host', type=str, metavar='', required=True, help='IP Address of the host')
    parser.add_argument('-o', '--output', type=str, metavar='', required=True,
                        help='Output directory for scan (Full Path) (Example : /home/user/)')
    parser.add_argument('-w', '--wordlist', type=str, metavar='', required=True, help='Wordlist to use for dirbust')
    parser.add_argument('-a', '--all', action="store_true", required=False,
                        help='--all if you want to bruteforce all (Does not prompt)')
    parser.add_argument('-d', '--debug', action="store_true", required=False,
                        help='--debug to skip nmap (requires hardcoded nmap dict)')
    args = parser.parse_args()
    if args.all:
        allBrute = 1
        print("[!] Will bruteforce everything that is bruteforcable! Good luck :)\n")
    else:
        allBrute = 0

    if args.debug:
        debug = 1
        print("[!!!] Debug mode enabled\n")
    else:
        debug = 0

    host = args.host
    root_dir = os.path.join(args.output, "reconScript")  # path to create directory
    try:  # Check if it exists (THeres a better way to do it!)
        os.mkdir(root_dir)
    except:
        print("[!] {} Already exists, will output everything there.\n".format(root_dir))
        pass
    wordlist = args.wordlist
    result = nmapScan(host, root_dir)
    result.check(wordlist)  # Regular portScan

    import tkinter as tk

    root = tk.Tk()
    app = MainWindow(root, root_dir)
    app.run()
