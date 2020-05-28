from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog as fd
import tkinter as tk
import prac
import sqlite3
#from PIL import Image,ImageTk
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def icon_background(wind,photo):

    wind.iconphoto(True, photo)
    wind.configure(background='MintCream')

def _create_check(modulation_window):
    # creating 3 checkbuttons
    check_=0
    tk.Label(modulation_window,text='Select to plot Graph').grid(row=0,column=2,sticky=tk.W)
    mod_sig = tk.IntVar(modulation_window)
    check1 = tk.Checkbutton(modulation_window, text="Modulating Signal", variable=mod_sig)#,state='disabled')
    check1.deselect()
    check1.grid(row=1, column=2,sticky=tk.W)
    car_sig = tk.IntVar(modulation_window)
    check2 = tk.Checkbutton(modulation_window, text="Carrier Signal", variable=car_sig)
    check2.deselect()
    check2.grid(row=2, column=2,sticky=tk.W)
    mes_sig = tk.IntVar(modulation_window)
    check3 = tk.Checkbutton(modulation_window, text='Message Signal', variable=mes_sig)
    check3.select()
    check3.grid(row=3, column=2,sticky=tk.W)
    check_=0
    if (mod_sig.get()):
        check_ += 1
    if (car_sig.get()):
        check_ += 1
    if (mes_sig.get()):
        check_ += 1
    return mod_sig.get(),car_sig.get(),mes_sig.get(),check_

def create_menu_bar(main_window):
    def _quit():
        ans = msg.askyesnocancel('Quit Window', 'Do You Want to Quit ?')
        if (ans):
            # main_window.quit()
            #main_window.destroy()
            main_window.after(2000, main_window.destroy)
    def _saveas():
        ans = msg.askyesno('show info', 'Do You Want to Save ?')
        if (ans):
            msg.showerror('Input error','There is Nothing to Save')

    menu_bar = Menu(main_window, bd=3, fg='red', bg='pink')
    filemenu = Menu(menu_bar, tearoff=0)
    filemenu.add_command(label='New', command='')
    filemenu.add_command(label='Open', command='')
    filemenu.add_command(label='Save', command=_saveas)
    filemenu.add_command(label='Save_as', command=_saveas)
    filemenu.add_command(label='Close', command=_quit)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=_quit)
    menu_bar.add_cascade(label='File', menu=filemenu)

    editmenu = Menu(menu_bar, tearoff=0)
    editmenu.add_command(label='Cut', command='')
    editmenu.add_command(label='Copy', command='')
    editmenu.add_command(label='Paste', command='')
    editmenu.add_command(label='Select All', command='')
    menu_bar.add_cascade(label='Edit', menu=editmenu)

    helpmenu = Menu(menu_bar, tearoff=0)
    helpmenu.add_command(label='Help Index', command='')
    helpmenu.add_command(label='About...', command='')
    menu_bar.add_cascade(label='Help', menu=helpmenu)

    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    column_name_mod = ['ID', 'Carrier_Amp', 'Carrier_Freq', 'Modulating_Amp', 'Modulating_Fre',
                       'sensitivity', 'Mod_type']
    command = 'CREATE TABLE IF NOT EXISTS modulation (ID INTEGER PRIMARY KEY AUTOINCREMENT,Carrier_Amp int, Carrier_Fre int,Modulating_Amp int, Modulating_Fre int,sensitivity float real,Mod_type VARCHAR);'
    db_conn.execute(command)
    db_conn.commit()

    column_name_diode = ['ID', 'Donor_concn', 'Acceptor_concn', 'Area', 'Intrinsic_concn', 'Holes_life',
                         'Electron_life', 'Holes_diff', 'Electron_diff', 'Temp']
    command = 'CREATE TABLE IF NOT EXISTS DIODE1 (ID INTEGER PRIMARY KEY AUTOINCREMENT,Donor_concn float real, Acceptor_concn float real, Area float real,Intrinsic_concn float real, Holes_life float real,Electron_life float real, Holes_diff float real,Electron_diff float real, Temp float real);'


    db_conn.execute(command)
    db_conn.commit()

    column_name_resistance = ['ID', 'Resist']
    command = 'CREATE TABLE IF NOT EXISTS Resistance (ID INTEGER PRIMARY KEY AUTOINCREMENT,Resist float real);'

    db_conn.execute(command)
    db_conn.commit()


    db_conn.close()


    history_menu = Menu(menu_bar, tearoff=0)
    history_menu.add_command(label='Modulation Input History',
                             command=lambda: prac.show_history(column_name_mod, 'modulation'))
    history_menu.add_command(label='Diode input History', command=lambda: prac.show_history(column_name_diode, 'diode1'))
    history_menu.add_command(label='Resistor input History', command=lambda : prac.show_history(column_name_resistance,'Resistance'))
    menu_bar.add_cascade(label='History', menu=history_menu)


    main_window.config(menu=menu_bar)


def create_menu_bar1(main_window,canvas):
    def _quit():
        ans = msg.askyesnocancel('Quit Window', 'Do You Want to Quit ?')
        if (ans):
            # main_window.quit()
            #main_window.destroy()
            main_window.after(2000, main_window.destroy)
    def _saveas():
        ans = msg.askyesno('Show Information', 'Do You Want to Save ?')
        if (ans):
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Images', '*.jpg')]
            file = fd.asksaveasfilename(defaultextension='.png')
            if file:
                try:
                    print(main_window.winfo_children())
                    canvas.print_png(file)
                except:
                    print("nope")
            else:
                msg.showerror('Input Error','Please Write Valid Name')

    menu_bar = Menu(main_window, bd=3, fg='red', bg='pink')
    filemenu = Menu(menu_bar, tearoff=0)
    filemenu.add_command(label='New', command='')
    filemenu.add_command(label='Open', command='')
    filemenu.add_command(label='Save', command=_saveas)
    filemenu.add_command(label='Save_as', command=_saveas)
    filemenu.add_command(label='Close', command=_quit)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=_quit)
    menu_bar.add_cascade(label='File', menu=filemenu)

    editmenu = Menu(menu_bar, tearoff=0)
    editmenu.add_command(label='Cut', command='')
    editmenu.add_command(label='Copy', command='')
    editmenu.add_command(label='Paste', command='')
    editmenu.add_command(label='Select All', command='')
    menu_bar.add_cascade(label='Edit', menu=editmenu)

    helpmenu = Menu(menu_bar, tearoff=0)
    helpmenu.add_command(label='Help Index', command='')
    helpmenu.add_command(label='About...', command='')
    menu_bar.add_cascade(label='Help', menu=helpmenu)


    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    column_name_mod = ['ID', 'Carrier_Ampl', 'Carrier_Freq', 'Modulating_Amp', 'Modulating_Fre',
                   'sensitivity','Mod_type']
    command = 'CREATE TABLE IF NOT EXISTS modulation (ID INTEGER PRIMARY KEY AUTOINCREMENT,Carrier_Amp int, Carrier_Fre int,Modulating_Amp int, Modulating_Fre int,sensitivity float real,Mod_type VARCHAR);'
    db_conn.execute(command)
    db_conn.commit()

    column_name_diode = ['ID','Donor_concn', 'Acceptor_concn', 'Area', 'Intrinsic_concn', 'Holes_life','Electron_life','Holes_diff','Electron_diff','Temp']
    command = 'CREATE TABLE IF NOT EXISTS DIODE1 (ID INTEGER PRIMARY KEY AUTOINCREMENT,Donor_concn float real, Acceptor_concn float real, Area float real,Intrinsic_concn float real, Holes_life float real,Electron_life float real, Holes_diff float real,Electron_diff float real, Temp float real);'
    db_conn.execute(command)
    db_conn.commit()

    column_name_resistance = ['ID', 'Resist']
    command = 'CREATE TABLE IF NOT EXISTS Resistance (ID INTEGER PRIMARY KEY AUTOINCREMENT,Resist float real);'

    db_conn.close()


    history_menu = Menu(menu_bar, tearoff=0)
    history_menu.add_command(label='Modulation Input History', command=lambda: prac.show_history(column_name_mod,'modulation'))
    history_menu.add_command(label='Diode input History', command=lambda: prac.show_history(column_name_diode,'DIODE1'))
    history_menu.add_command(label='Resistor input History', command=lambda : prac.show_history(column_name_resistance,'Resistance'))
    menu_bar.add_cascade(label='History', menu=history_menu)

    main_window.config(menu=menu_bar)




