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

'''
CHECK BOX CUSTOM CLASS
'''

check_nu = b'iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TRZEWB4uIOGSoTi2IijpKFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi4uqk6CIl/i8ptIjx4Lgf7+497t4BQqPCVLNrHFA1y0jFY2I2tyr2vCKAIAYRwYzETD2RXszAc3zdw8fXuyjP8j735wgqeZMBPpF4jumGRbxBPL1p6Zz3iUOsJCnE58QRgy5I/Mh12eU3zkWHBZ4ZMjKpeeIQsVjsYLmDWclQiaeIw4qqUb6QdVnhvMVZrdRY6578hYG8tpLmOs0RxLGEBJIQIaOGMiqwEKVVI8VEivZjHv5hx58kl0yuMhg5FlCFCsnxg//B727NwuSEmxSIAd0vtv0xCvTsAs26bX8f23bzBPA/A1da219tALOfpNfbWvgI6N8GLq7bmrwHXO4AQ0+6ZEiO5KcpFArA+xl9Uw4YuAX61tzeWvs4fQAy1NXyDXBwCIwVKXvd4929nb39e6bV3w/0UXLbKEvbjQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+MMDRctIGmzOYIAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAALElEQVQoz2M0Njb+z0AiYGFgYGA4c+YMI7EaTExM/jMxkAFGNQ1jTYzkpD0ATtMHS/nRiQwAAAAASUVORK5CYII='
check_nc = b'iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TRZEWB4uIOGSoTi2IijpKFYtgobQVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi4uqk6CIl/i8ptIjx4Lgf7+497t4BQqPCVLNrHFA1y0jFY2I2tyr2vCKAIAYRwYzETD2RXszAc3zdw8fXuyjP8j735wgqeZMBPpF4jumGRbxBPL1p6Zz3iUOsJCnE58QRgy5I/Mh12eU3zkWHBZ4ZMjKpeeIQsVjsYLmDWclQiaeIw4qqUb6QdVnhvMVZrdRY6578hYG8tpLmOs0RxLGEBJIQIaOGMiqwEKVVI8VEivZjHv5hx58kl0yuMhg5FlCFCsnxg//B727NwuSEmxSIAd0vtv0xCvTsAs26bX8f23bzBPA/A1da219tALOfpNfbWvgI6N8GLq7bmrwHXO4AQ0+6ZEiO5KcpFArA+xl9Uw4YuAX61tzeWvs4fQAy1NXyDXBwCIwVKXvd4929nb39e6bV3w/0UXLbKEvbjQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+MMDRctDrVlNE0AAAAjdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVAgd2l0aCBsb3ZlyGW0XgAAAJdJREFUKM+d0rENAyEMBdDvKA1zeART07MIGzAFE7EDK1B5CMqf7pIUlyP3JZdP+rItZkb8mScAjDFkF8QY+cCNbCF3R86ZvXduIXdHKYWqipSSXKJP0FqTEMK7Xu+dOWe6+yU4UEpJVBWlFLr7TwAAYmYcY8haC7VWzjkBAGfga+UhBLTWRFVPwREzI0nsjpndO67c+b0XBDxvkWRMW24AAAAASUVORK5CYII='


class custom_checkbox_text(tk.Frame):
    def __init__(self, parent, colour, text, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.checkbox = custom_checkbox(self, colour, *args, **kwargs)
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


class custom_checkbox(tk.Checkbutton):
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
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
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
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


global ibuster,inikto
ibuster = 0
inikto = 0

global busterList,niktoList
niktoList = []
busterList = []

global smbCheckCmd
global bruteSMBcmd
global bruteFTPcmd
global bruteSSHcmd
global rootDir


def btnAlotNikto(frame):
    global inikto
    if inikto > 3:
        inikto = 0
    else:
        pass
    #print(inikto)
    #print(frame["nikto"][inikto])
    raise_frame(frame["nikto"][inikto])
    inikto += 1


def btnAlotBuster(frame):
    global ibuster
    if ibuster > 3:
        ibuster = 0
    else:
        pass
    #print(ibuster)
    #print(frame["buster"][ibuster])
    raise_frame(frame["buster"][ibuster])
    ibuster += 1

def raise_frame(frame):
    frame.tkraise()

class NewprojectApp:
    def __init__(self,listing, master=None):
        global rootDir
        global spList
        # build ui
        self.mainFrame = ttk.Frame(master)
        self.BtnFrame = ttk.Frame(self.mainFrame)
        style = ttk.Style()
        style.configure("Mine.TButton", background="red")
        self.bactions = ttk.Button(self.BtnFrame, style="Mine.TButton")
        self.bactions.configure(text='Actions')
        self.bactions.pack(pady='50', side='bottom')
        self.bactions.configure(command=self.actionWindow)
        self.bsprayShow = ttk.Button(self.BtnFrame)
        self.bsprayShow.configure(text='Spraying')
        self.bsprayShow.pack(side='top')
        self.bsprayShow.configure(command=lambda: raise_frame(self.fsprayShow))
        self.bcredsWrite = ttk.Button(self.BtnFrame)
        #self.bcredsWrite.configure(text='Write Creds')
        #self.bcredsWrite.pack(side='top')
        #self.bcredsWrite.configure(command=lambda:raise_frame(self.fcredsWrite))
        self.bnikto = ttk.Button(self.BtnFrame)
        self.bnikto.configure(text='Nikto')
        self.bnikto.pack(side='top')
        self.bnikto.configure(command=lambda:btnAlotNikto(self.frameDict))
        self.bsshBrute = ttk.Button(self.BtnFrame)
        self.bsshBrute.configure(text='SSH Brute')
        self.bsshBrute.configure(command=lambda:raise_frame(self.fsshBrute))
        self.bsshBrute.pack(side='top')
        self.bftpBrute = ttk.Button(self.BtnFrame)
        self.bftpBrute.configure(text='FTP Brute')
        self.bftpBrute.configure(command=lambda:raise_frame(self.fFtpBrute))
        self.bftpBrute.pack(side='top')
        self.bsmbBrute = ttk.Button(self.BtnFrame)
        self.bsmbBrute.configure(text='SMB Brute')
        self.bsmbBrute.configure(command=lambda:raise_frame(self.fsmbBrute))
        self.bsmbBrute.pack(side='top')
        self.bdirbuster = ttk.Button(self.BtnFrame)
        self.bdirbuster.configure(text='Dirbuster')
        self.bdirbuster.configure(command=lambda:btnAlotBuster(self.frameDict))
        self.bdirbuster.pack(side='top')
        self.bsmbCheck = ttk.Button(self.BtnFrame)
        self.bsmbCheck.configure(text='SMBCheck')
        self.bsmbCheck.configure(command=lambda:raise_frame(self.fSmbChecker))
        self.bsmbCheck.pack(side='top')
        self.bNmapView = ttk.Button(self.BtnFrame)
        self.bNmapView.configure(text='View NMAP')
        self.bNmapView.configure(command=lambda:raise_frame(self.fNmap))
        self.bNmapView.pack(side='top')
        self.BtnFrame.configure(height='200', width='200')
        self.BtnFrame.grid(column='0', row='1')
        self.fcredsWrite = ttk.Frame(self.mainFrame)
        self.fcredsWrite.configure(height='600', width='600')
        self.fcredsWrite.grid(column='1', row='1')
        self.fSmbChecker = ttk.Frame(self.mainFrame)
        self.fSmbChecker.configure(height='600', width='600')
        self.fSmbChecker.grid(column='1', row='1')
        self.fsprayShow = ttk.Frame(self.mainFrame)
        self.fsprayShow.configure(height='600', width='600')
        self.fsprayShow.grid(column='1', row='1')
        self.fNikto1 = ttk.Frame(self.mainFrame)
        self.fNikto1.configure(height='600', width='600')
        self.fNikto1.grid(column='1', row='1')
        self.fNikto2 = ttk.Frame(self.mainFrame)
        self.fNikto2.configure(height='600', width='600')
        self.fNikto2.grid(column='1', row='1')
        self.fNikto3 = ttk.Frame(self.mainFrame)
        self.fNikto3.configure(height='600', width='600')
        self.fNikto3.grid(column='1', row='1')
        self.fNikto4 = ttk.Frame(self.mainFrame)
        self.fNikto4.configure(height='600', width='600')
        self.fNikto4.grid(column='1', row='1')
        self.fbuster1= ttk.Frame(self.mainFrame)
        self.fbuster1.configure(height='600', width='600')
        self.fbuster1.grid(column='1', row='1')
        self.fbuster2 = ttk.Frame(self.mainFrame)
        self.fbuster2.configure(height='600', width='600')
        self.fbuster2.grid(column='1', row='1')
        self.fbuster3 = ttk.Frame(self.mainFrame)
        self.fbuster3.configure(height='600', width='600')
        self.fbuster3.grid(column='1', row='1')
        self.fbuster4 = ttk.Frame(self.mainFrame)
        self.fbuster4.configure(height='600', width='600')
        self.fbuster4.grid(column='1', row='1')
        self.fsshBrute = ttk.Frame(self.mainFrame)
        self.fsshBrute.configure(height='600', width='600')
        self.fsshBrute.grid(column='1', row='1')
        self.fFtpBrute = ttk.Frame(self.mainFrame)
        self.fFtpBrute.configure(height='600', width='600')
        self.fFtpBrute.grid(column='1', row='1')
        self.fsmbBrute = ttk.Frame(self.mainFrame)
        self.fsmbBrute.configure(height='600', width='600')
        self.fsmbBrute.grid(column='1', row='1')
        self.mainFrame.configure(height='200', width='200')
        self.mainFrame.pack(side='top')
        self.fNmap = ttk.Frame(self.mainFrame)
        self.fNmap.configure(height='600', width='600')
        self.fNmap.grid(column='1', row='1')
        self.niktoFrames = [self.fNikto1,self.fNikto2,self.fNikto3,self.fNikto4]
        self.busterFrames = [self.fbuster1,self.fbuster2,self.fbuster3,self.fbuster4]
        self.frameDict = {"nikto":self.niktoFrames,"buster":self.busterFrames}
        self.idListBuster = [self.fbuster1.winfo_id(),self.fbuster2.winfo_id(),self.fbuster3.winfo_id(),self.fbuster4.winfo_id()]
        self.idListNikto = [self.fNikto1.winfo_id(),self.fNikto2.winfo_id(),self.fNikto3.winfo_id(),self.fNikto4.winfo_id()]
        self.idCredsWrite = self.fcredsWrite.winfo_id()
        self.idSprayShow = self.fsprayShow.winfo_id()
        self.idSmbCheck = self.fSmbChecker.winfo_id()
        self.idSmbBrute = self.fsmbBrute.winfo_id()
        self.idFtpBrute = self.fFtpBrute.winfo_id()
        self.idSshBrute = self.fsshBrute.winfo_id()
        self.idNamp = self.fNmap.winfo_id()
        # Main widget
        self.mainwindow = self.mainFrame
        self.bsprayShow.pack_forget()
        spList = [] # subprocess list so we can end each of them on exit.
        print("BUSTER : {}\n".format(self.idListBuster))
        print("NIKTO : {}\n".format(self.idListNikto))
        print("CredsWrite : {}\n".format(self.idCredsWrite))
        print("SprayShow : {}\n".format(self.idSprayShow))
        print("SmbCheck : {}\n".format(self.idSmbCheck))
        print("SmbBrute : {}\n".format(self.idSmbBrute))
        print("FtpBrute : {}\n".format(self.idFtpBrute))
        print("SshBrute : {}\n".format(self.idSshBrute))


        '''
        Creds Write
        '''

        try:
            print("Starting CredsWrite\n")
            spList.append( subprocess.Popen(
                ["xterm", "-into", str(self.idCredsWrite), "-geometry", "100x100", "-hold", "-e",
                 "nano {}/credsWrite.txt".format(rootDir)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        except:
            self.bsmbCheck.pack_forget()



        '''
        DIRBUSTER 
        '''

        try:
            print("Starting Dirbuster\n")
            i = 0
            for cmd in busterList:
                spList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idListBuster[i]), "-geometry", "100x100","-hold","-e","{} & wait".format(cmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                #print(cmd)
                i += 1
            if i < 4:
                newI = 4 - i
                for notAv in range(0,newI):
                    if i == 5:
                        break
                    else:
                        pass
                    spList.append(subprocess.Popen(
                        ["xterm", "-into", str(self.idListBuster[i]), "-geometry", "100x100", "-hold", "-e",
                         "echo '[!] Nothing here!'"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                    i +=1
            '''
            DIRBUSTER ^^^^^
            '''

            '''
            NIKTO 
            '''

            try:
                print("Starting Nikto\n")
                i = 0
                for cmd in niktoList:
                    spList.append(subprocess.Popen(
                        ["xterm", "-into", str(self.idListNikto[i]), "-geometry", "100x100", "-hold", "-e",
                         "{} & wait".format(cmd)],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                    i += 1
                if i < 4:
                    newI = 4 - i
                    for notAv in range(0, newI):
                        if i == 5:
                            break
                        else:
                            pass
                        spList.append(subprocess.Popen(
                            ["xterm", "-into", str(self.idListNikto[i]), "-geometry", "100x100", "-hold", "-e",
                             "echo '[!] Nothing here!'"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                        i += 1
            except:
                pass


            '''
            NIKTO ^^^^
            '''

            '''
            SMBCHECK
            '''
            global smbCheckCmd
            try:
                print("Starting SmbCheck\n")
                spList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idSmbCheck), "-geometry", "100x100", "-hold", "-e", "{} & wait".format(smbCheckCmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            except:
                self.bsmbCheck.pack_forget()

            '''
            SMB BRUTE
            '''

            global bruteSMBcmd
            try:
                print("Starting SmbBrute\n")
                spList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idSmbBrute), "-geometry", "100x100", "-hold", "-e", "{} & wait".format(bruteSMBcmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            except Exception as e:
                #print(e)
                self.bsmbBrute.pack_forget()

            '''
            FTP BRUTE
            '''

            global bruteFTPcmd
            try:
                print("Starting FtpBrute\n")
                spList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idFtpBrute), "-geometry", "100x100", "-hold", "-e",
                     "{} & wait".format(bruteFTPcmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            except Exception as e:
                #print(e)
                self.bftpBrute.pack_forget()

            '''
            SSH BRUTE
            '''

            global bruteSSHcmd
            try:
                print("Starting SshBrute\n")
                spList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idSshBrute), "-geometry", "100x100", "-hold", "-e",
                     "{} & wait".format(bruteSSHcmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            except:
                self.bsshBrute.pack_forget()

            '''
            NMAP READ
            '''
            try:
                 spList.append(subprocess.Popen(
                    ["xterm", "-into", str(self.idNamp), "-geometry", "100x100", "-hold", "-e", "cat {}/nmap/nmap_scan.txt".format(rootDir)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            except:
                pass
            self.spList = spList # subprocess list so we can end each of them on exit.
            '''
            p2 = subprocess.Popen(
                ["xterm", "-into", str(self.idList[1]), "-geometry", "100x100","-hold", "-e", "ping -c 4 localhost"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p3 = subprocess.Popen(
                ["xterm", "-into", str(self.idList[2]), "-geometry", "100x100"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p4 = subprocess.Popen(
                ["xterm", "-into", str(self.idList[3]), "-geometry", "100x100", "-e", "ping localhost"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            '''
        except FileNotFoundError:
            showwarning("Error", "xterm is not installed")
            raise SystemExit

    def sprayingShow(self):
        self.bsprayShow.pack()
        self.mainwindow.lift()
        #print("Running sprayingShow")
        global sprayingCmd
        try:
            self.sprayingCmd = sprayingCmd
        except:
            messagebox.showerror("Error",message="You need to set the credentials first.")
            self.actionWindow.lift()
        #print(self.sprayingCmd)
        try:
            spList.append(subprocess.Popen(
                ["xterm", "-into", str(self.idSprayShow), "-geometry", "100x100", "-hold", "-e",
                 "{} & wait".format(self.sprayingCmd)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE))
        except:
            self.bsshBrute.pack_forget()

    def onExit(self):
        for service in self.spList:
            service.terminate()

    def actionWindow(self):
        global actionWindow
        # Toplevel object which will
        # be treated as a new window
        try:
            if actionWindow.state() == "normal": actionWindow.lift()
        except:
            actionWindow = Toplevel(self.mainwindow)
            actionWindow.frame2 = ttk.Frame(actionWindow)
            actionWindow.atctions = ttk.Label(actionWindow.frame2)
            actionWindow.atctions.configure(text='Action Launcher')
            actionWindow.atctions.pack(side='top')
            actionWindow.separatorLine = ttk.Separator(actionWindow.frame2)
            actionWindow.separatorLine.configure(orient='horizontal')
            actionWindow.separatorLine.pack(fill='x', side='top')
            actionWindow.frame2.configure(height='22', width='500')
            actionWindow.frame2.pack(side='top')
            actionWindow.frame2.pack_propagate(0)
            actionWindow.frame4 = ttk.Frame(actionWindow)
            actionWindow.bspray = ttk.Button(actionWindow.frame4)
            actionWindow.bspray.configure(text='Sprayer')
            actionWindow.bspray.configure(command=self.sprayingShow)
            actionWindow.bspray.pack(pady='20', side='top')
            actionWindow.bCredsWrite = ttk.Button(actionWindow.frame4)
            actionWindow.bCredsWrite.configure(text='Write Credentials')
            actionWindow.bCredsWrite.configure(command=self.writeCredsWindows)
            actionWindow.bCredsWrite.pack(pady='20',side='top')
            actionWindow.button4 = ttk.Button(actionWindow.frame4)
            actionWindow.button4.configure(state='disabled', text='Launch owasp zap')
            actionWindow.button4.pack(side='top')
            actionWindow.frame4.configure(height='200', width='500')
            actionWindow.frame4.pack(side='bottom')
            actionWindow.frame4.pack_propagate(0)
            self.actionWindow = actionWindow

    def writeCredsWindows(self):
        global writeCredsWindow
        global rootDir
        global sprayMode
        self.mode = tk.IntVar()
        if os.path.exists("{}/credsWrite.txt".format(rootDir)):
            with open("{}/credsWrite.txt".format(rootDir), "r") as d:
                data = d.read()
        else:
            data = '''admin\nroot\nuser\npassword'''
        try:
            if self.writeCredsWindow.state() == "normal": self.writeCredsWindow.lift()
        except:
            self.writeCredsWindow = Toplevel(self.actionWindow)
            self.writeCredsWindow.frame4 = ttk.Frame(self.writeCredsWindow)
            self.writeCredsWindow.frame5 = ttk.Frame(self.writeCredsWindow.frame4)
            self.writeCredsWindow.sprayList = tk.Text(self.writeCredsWindow.frame5)
            self.writeCredsWindow.sprayList.configure(height='10', width='50')
            _text_ = data
            self.writeCredsWindow.sprayList.insert('0.0', _text_)
            self.writeCredsWindow.sprayList.grid(column='0', row='0')
            self.writeCredsWindow.frame8 = ttk.Frame(self.writeCredsWindow.frame5)
            self.writeCredsWindow.checkPassOnly = custom_checkbox_text(self.writeCredsWindow.frame8,"black","Password Only",onvalue=1,variable=self.mode)
            #self.writeCredsWindow.checkPassOnly.configure(text='Password Only')
            self.writeCredsWindow.checkPassOnly.pack(side='bottom')
            self.writeCredsWindow.checkuserOnly = custom_checkbox_text(self.writeCredsWindow.frame8,"black","Username Only",onvalue=2,variable=self.mode)
            #self.writeCredsWindow.checkuserOnly.configure(text='Username Only')
            self.writeCredsWindow.checkuserOnly.pack(side='bottom')
            self.writeCredsWindow.checkCombo = custom_checkbox_text(self.writeCredsWindow.frame8,"black","Combo Mode (user:pass)",onvalue=3,variable=self.mode)
            #self.writeCredsWindow.checkCombo.configure(text='Combo Mode (user:pass)')
            self.writeCredsWindow.checkCombo.pack(side='bottom')
            self.writeCredsWindow.checkLP = custom_checkbox_text(self.writeCredsWindow.frame8,"black","User as passowrd",onvalue=4,variable=self.mode)
            #self.writeCredsWindow.checkLP.configure(text='User as passowrd')
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


    def save(self):
        global rootDir
        global sprayMode
        global result
        if self.mode.get() == 0:
            messagebox.showerror("Missing Parameters",message="Please select 1 spraying mode.")
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
            with open("{}/credsWrite.txt".format(rootDir), "w+") as f:
                f.write(self.writeCredsWindow.sprayList.get("1.0", END))
                f.close()


    def lol(self):
        pass

    def run(self):
        self.mainwindow.mainloop()


def on_exit(root):
    global spList
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? Stuff might break"):
        for service in spList:
            service.terminate()
        root.destroy()

def doNikto(logfile, url):
    global niktoList
    newlogfile = logfile.replace('dirbust','nikto')
    rootfile = logfile.split("dirbust")[0]
    #print(rootfile)
    #print(newlogfile)
    try:
        os.mkdir("{}/nikto".format(rootfile))
    except:
        pass
    #cords =cordsManager("nikto")
    command = "nikto -host={} -o {}".format(url,newlogfile)
    niktoList.append(command)
    #os.system("xterm -T 'Nikto!' -geometry {} -e {}".format(cords,command))

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
    command = "python3 ./busterScript.py --url {} --wordlist {} --output {} --rootDir {}".format(url, wordlist, logfile,dir)
    busterList.append(command)
    #cords = cordsManager("dirbust")
    #os.system("xterm -T 'dirbuster!' -geometry {} -e {}".format(cords,command))


def dirbuster(urls, wordlist, logfiles, dir):  # This starts the threads, passing it all it needs.
    i = 0
    for url in urls:
        tnikto = threading.Thread(target=doNikto, args=(logfiles[i], url,))  # FOR NIKTO!
        tdirbust = threading.Thread(target=bust, args=(url, wordlist, logfiles[i], dir)) # FOR DIRBUST!
        tdirbust.start()
        tnikto.start()
        i += 1
'''
def bruteSSH(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    cords = cordsManager("brute")
    command = "hydra -s 22 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V ssh://{} -o {}/brute/SSH.txt -I ".format(
        host, rootDir)
    os.system("xterm -T 'bruteforcing SSH!' -geometry {} -e {}".format(cords,command))

def bruteSMB(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    cords = cordsManager("brute")
    command = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} smb -o {}/brute/SMB.txt -I".format(host,rootDir)
    os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords,command))

'''
def smbCheck(host,rootDir):
    global smbCheckCmd
    command = "python3 smbCheck.py --host {} --output {}".format(host,rootDir)
    smbCheckCmd = command
    #os.system("xterm -T 'SMB Checker!' -geometry 90x30+0+1080 -hold -e {}".format(command))
'''
def bruteFTP(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    command = "hydra -s 21 -t 20 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ftp://{} -o {}/brute/FTP.txt -I ".format(host,rootDir)
    os.system("xterm -T 'bruteforcing FTP!' -geometry 90x30+1920+1080 -e {}".format(command))

'''

class nmapScan:
    '''
    __INIT__ :
    Initiate the nmap3 object and host variable.
    Do an -sV scan and save it to self.result.
    Format the result into a list self.openPorts.

    '''

    def __init__(self, host, rootDir, *args, **kwargs):
        global debug  # Boolean to skip nmap scan
        try:
            os.mkdir(os.path.join(rootDir, "nmap"))
        except:
            pass
        self.rootDir = rootDir  # This is where all the files of the scan will be outputed
        #self.webServices = ["Microsoft IIS httpd", "Apache httpd", "nginx", "Apache Tomcat", "MiniServ",
         #                   "lighttpd","Microsoft HTTPAPI httpd","http-proxy",'httpd','http']
        self.webServices = ["http-proxy",'httpd','http']
        # Let's only do common webservices.
        self.host = host
        self.nmap = nmap3.Nmap()
        if debug == 1:
            self.result = {'192.168.174.55': {'osmatch': {}, 'ports': [{'protocol': 'tcp', 'portid': '21', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'ftp', 'product': 'FileZilla ftpd', 'version': '0.9.41 beta', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '80', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.43', 'extrainfo': '(Win64) OpenSSL/1.1.1g PHP/7.4.6', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.43'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '135', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '139', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'netbios-ssn', 'product': 'Microsoft Windows netbios-ssn', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '443', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.43', 'extrainfo': '(Win64) OpenSSL/1.1.1g PHP/7.4.6', 'tunnel': 'ssl', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.43'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '445', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'microsoft-ds', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '3306', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'mysql', 'servicefp': 'SF-Port3306-TCP:V=7.91%I=7%D=6/1%Time=60B66D74%P=x86_64-pc-linux-gnu%r(RTSPRequest,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.174\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server")%r(DNSStatusRequestTCP,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.174\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server")%r(Help,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.174\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server")%r(TLSSessionReq,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.174\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server");', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '5040', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'unknown', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '7680', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'tcpwrapped', 'method': 'probed', 'conf': '8'}, 'scripts': []}], 'hostname': [], 'macaddress': None, 'state': {'state': 'up', 'reason': 'echo-reply', 'reason_ttl': '127'}}, 'stats': {'scanner': 'nmap', 'args': '/usr/bin/nmap -oX - -sV -p- -oN /home/Kyand/testing/reconScript/nmap/nmap_scan.txt 192.168.174.55', 'start': '1622568153', 'startstr': 'Tue Jun  1 13:22:33 2021', 'version': '7.91', 'xmloutputversion': '1.05'}, 'runtime': {'time': '1622568463', 'timestr': 'Tue Jun  1 13:27:43 2021', 'summary': 'Nmap done at Tue Jun  1 13:27:43 2021; 1 IP address (1 host up) scanned in 309.55 seconds', 'elapsed': '309.55', 'exit': 'success'}}
        else:
            print("[!] nmap scan is running...\n")
            self.result = self.nmap.nmap_version_detection(self.host, args="-p- -oN {}/nmap/nmap_scan.txt".format(
                rootDir))  # -sV -p- -oN (rootDir/nmap_scant.txt) scan
            print(self.result)
            print("[!] nmap scan has completed!\n")
            #print(self.result)
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
            stringServices+="{},".format(service)
        #print(stringServices)

        #print(services)
        sprayingCmd = "python3 sprayer.py {}/credsWrite.txt {} {} {} '{}'".format(rootDir,self.host,stringServices,rootDir,sprayMode)
        print(sprayingCmd)
        #print(sprayingCmd)

    def tbruteSMB(self):
        global bruteSMBcmd
        try:
            os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
        except:
            pass
        bruteSMBcmd = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} smb -o {}/brute/SMB.txt -I".format(
            host, rootDir)
        #print(bruteSMBcmd)
        #os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords, command))

    def tsmbCheck(self):
        global smbCheckCmd
        smbCheckCmd = "python3 smbCheck.py --host {} --output {} 2>/dev/null".format(self.host, self.rootDir)

    '''
    Runs funct
    '''

    def check(self, dWordList):
        global SSL
        global allBrute
        for port in self.result[self.host]['ports']:
            number = port['portid']
            if number == "443":
                SSL = True
            else:
                SSL = False

        self.dirbust(dWordList)  # Does dirbust AND extracts comments
        for port in self.result[self.host]['ports']:
            number = port['portid']
            if number == "21":
                self.checkFTP()
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
            os.mkdir("{}/brute".format(self.rootDir))  # Creates the "brute" directory
        except:
            pass
        bruteSSHcmd = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} ssh -o {}/brute/SSH.txt -I".format(
            self.host, self.rootDir)
        #os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords, command))

    def tBruteFTP(self):
        global bruteFTPcmd
        try:
            os.mkdir("{}/brute".format(self.rootDir))  # Creates the "brute" directory
        except:
            pass
        bruteFTPcmd = "hydra -s 21 -t 20 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ftp://{} -o {}/brute/FTP.txt -I ".format(
            self.host, self.rootDir)
        #print(bruteFTPcmd)
        #os.system("xterm -T 'bruteforcing FTP!' -geometry 90x30+1920+1080 -e {}".format(command))
    '''
    Do regular FTP checks (check anon login, check perms)

    '''

    def checkFTP(self):
        global allBrute
        #print("ALLBRUTE : {}".format(allBrute))
        rootDir = os.path.join(self.rootDir, "ftp")  # /ftp directory
        try:
            os.mkdir(os.path.join(self.rootDir, "ftp"))  # Create /ftp directory
        except:
            pass
        f = open("{}/results.txt".format(rootDir), "w+")  # Create results.txt file
        ftp = FTP(self.host)  # initate ftp object
        try:  # Check anonymous login
            ftp.login()
            f.write("Ftp anonymous : [WORKS]\n")
            f.close()
            if allBrute == 1:

                self.tBruteFTP()
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
                self.tBruteFTP()
            else:
                answ = input("[!] FTP anonymous works, do you still want to bruteforce it? (y/n)\n")
                if answ == "y":
                    self.tBruteFTP()
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
        logFiles = self.createLogFiles(self.rootDir)  # Creates logFile Paths
        dirbuster(self.urls, wordfile, logFiles, self.rootDir)  # Starts the threads


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
    rootDir = os.path.join(args.output, "reconScript")  # path to create directory
    try:  # Check if it exists (THeres a better way to do it!)
        os.mkdir(rootDir)
    except:
        print("[!] {} Already exists, will output everything there.\n".format(rootDir))
        pass
    wordlist = args.wordlist
    result = nmapScan(host, rootDir)
    result.check(wordlist)# Regular portScan



    import tkinter as tk
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda arg=root: on_exit(arg)) # Overwrite exit function for tkinter
    app = NewprojectApp(root)
    app.run()

