import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import Menu
import numpy as np
import math
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog as fd
import create_menu
from tkinter import *
import sqlite3

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        padx=145
        pady=720
        self._geom='200x200+0+0'
        #master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.geometry("{0}x{1}+360+40".format(master.winfo_screenwidth() - pady, master.winfo_screenheight() - padx))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom




def save_mod(val1=0,val2=0,val3=0,val4=0,val5=0,val6='AM'):
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    print("connection established")
    front_='INSERT INTO modulation (Carrier_Amp,Carrier_Fre,Modulating_Amp,Modulating_Fre,sensitivity,Mod_type) '
    back='VALUES ('+str(val1)+','+str(val2)+','+str(val3)+','+str(val4)+','+str(val5)+','
    if(val6=='AM'):
        back+='"AM"'
    if (val6 == 'FM'):
        back += '"FM"'
    if(val6=='PM'):
        back+='"PM"'
    back+=');'

    front_+=back
    #print(front_)
    db_conn.execute(front_)
    db_conn.commit()
    db_conn.close()



#from PIL import Image,ImageTk
def icon_background(wind,photo):
    #wind.iconphoto(False, photo)
    wind.configure(background='MintCream')

def Plot_Amplitude_Modulation():
    def plot_AM():
        save_mod(Amp_c.get(), fre_c.get(), Amp_m.get(), fre_m.get(), Amp_sen.get(), 'AM')
        try:
            check_ = 0
            if (mod_sig.get()):
                check_ += 1
            if (car_sig.get()):
                check_ += 1
            if (mes_sig.get()):
                check_ += 1
            inc_=1
            Amplitde=[]
            Amplitude_carrier = []
            Amplitude_send=[]
            time_ = []
            m_f = fre_m.get()
            time_period=((1/m_f)*(scale_factor.get()/10))/100000
            for i in range(1,100000,1):
                time_.append(time_period*i)
                Amplitde.append(Amp_m.get()*(np.cos(2*math.pi*m_f*(time_period*i))))
                Amplitude_carrier.append(Amp_c.get()*(np.cos((2*math.pi*fre_c.get()*(time_period*i)))))
                Amplitude_send.append(Amplitude_carrier[i-1]*Amp_sen.get()*Amplitde[i-1]+Amplitude_carrier[i-1])
                #Amplitude_send.append(Amp_c.get()*(1+(Amp_sen.get()*Amp_m.get()*(np.cos(2*3.14*m_f*(time_period*i)))))*(np.cos(2*3.14*fre_c.get()*(time_period*i))))
            max_y_lev=max(Amplitude_send)
            #fig = Figure(figsize=(15, 6), facecolor='pink', edgecolor='green', linewidth=1)
            fig.clf()
            if(mod_sig.get()):
                axis = fig.add_subplot(1, check_, inc_)
                axis.plot(time_,Amplitde)
                axis.set_xlabel('time(Sec)')
                axis.set_ylabel('Amplitude(Volt)')
                axis.set_title('Amplitude Vs Time of modulating signal')
                axis.grid(linestyle='-')
                inc_+=1
            if(car_sig.get()):
                carrier_graph = fig.add_subplot(1, check_, inc_)
                carrier_graph.plot(time_, Amplitude_carrier)
                carrier_graph.set_xlabel('time(Sec)')
                carrier_graph.set_ylabel('Amplitude(Volt)')
                carrier_graph.set_title('Amplitude Vs Time of carrier signal')
                carrier_graph.grid(linestyle='-')
                inc_+=1
            if(mes_sig.get()):
                sender_graph=fig.add_subplot(1, check_, inc_)
                sender_graph.plot(time_, Amplitude_send)
                sender_graph.set_xlabel('time(Sec)')
                sender_graph.set_ylabel('Amplitude(Volt)')
                sender_graph.set_title('Amplitude Vs Time of message signal')
                sender_graph.grid(linestyle='-')
                inc_+=1

            #axis.set_ylim(-max_y_lev-10, max_y_lev+10)
            #carrier_graph.set_ylim(-max_y_lev-10, max_y_lev+10)
            #sender_graph.set_ylim(-max_y_lev-10, max_y_lev+10)

            #axis.set_xlim(-10, max_range + 10)

            canvas = FigureCanvasTkAgg(fig, master=modulation_window)
            canvas._tkcanvas.grid(row=7, column=0, columnspan=3, sticky=tk.EW)
            #Amp_sig=Amp_c.get()*(1+(Amp_sen.get()*Amp_m.get())*(cos()))

            modulation_window.update()
        except:
          msg.showerror('Input Entry Error','Please Enter Valid Number')

    modulation_window = tk.Tk(className='Amplitude Modulation')
    #icon_background(modulation_window,photo)
    modulation_window.configure(background='MintCream')


    fig = Figure(figsize=(13, 4), facecolor='HoneyDew', edgecolor='green', linewidth=1)
    canvas = FigureCanvasTkAgg(fig, master=modulation_window)
    create_menu.create_menu_bar1(modulation_window, canvas)

    modulation_window.resizable(False, False)

    Amp_c = tk.DoubleVar(modulation_window)
    fre_c=tk.DoubleVar(modulation_window)
    Amp_m=tk.DoubleVar(modulation_window)
    fre_m=tk.DoubleVar(modulation_window)
    Amp_sen = tk.DoubleVar(modulation_window)
    ttk.Label(modulation_window, text='Carrier Signal Amplitude :').grid(row=0, column=0,sticky=tk.E)
    Entry(modulation_window,textvariable=Amp_c).grid(row=0, column=1, sticky=tk.W)
    ttk.Label(modulation_window,text='Carrier Signal Frequency :').grid(row=1, column=0,sticky=tk.E)
    Entry(modulation_window,textvariable=fre_c).grid(row=1,column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Modulating Signal Amplitude :').grid(row=2, column=0, sticky=tk.E)
    Entry(modulation_window, textvariable=Amp_m).grid(row=2, column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Modulating Signal Frequency :').grid(row=3, column=0, sticky=tk.E)
    Entry(modulation_window, textvariable=fre_m).grid(row=3, column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Amplitude Sensitivity :').grid(row=4, column=0, sticky=tk.E)
    Entry(modulation_window, textvariable=Amp_sen).grid(row=4, column=1,sticky=tk.W)
    scale_factor=tk.DoubleVar(modulation_window)
    ttk.Label(modulation_window,text='scale_factor :').grid(row=5,column=0,sticky=tk.E)
    scaleing=Scale(modulation_window,from_=0,to=100,variable=scale_factor,orient=HORIZONTAL).grid(row=5,column=1,sticky=tk.EW)
    # check box making
    tk.Label(modulation_window, text='Select to plot Graph').grid(row=0, column=2, sticky=tk.W)
    mod_sig = tk.IntVar(modulation_window)
    check1 = tk.Checkbutton(modulation_window, text="Modulating Signal", variable=mod_sig)  # ,state='disabled')
    check1.deselect()
    check1.grid(row=1, column=2, sticky=tk.W)
    car_sig = tk.IntVar(modulation_window)
    check2 = tk.Checkbutton(modulation_window, text="Carrier Signal", variable=car_sig)
    check2.deselect()
    check2.grid(row=2, column=2, sticky=tk.W)
    mes_sig = tk.IntVar(modulation_window)
    check3 = tk.Checkbutton(modulation_window, text='Message Signal', variable=mes_sig)
    check3.select()
    check3.grid(row=3, column=2, sticky=tk.W)
    action=ttk.Button(modulation_window,command=plot_AM,text='Plot Graph').grid(row=6,column=0,sticky=tk.E)

def Plot_Frequency_Modulation():
    def plot_FM():
        save_mod(Amp_c.get(), fre_c.get(), Amp_m.get(), fre_m.get(), fre_sen.get(), 'FM')
        try:
            check_ = 0
            inc_=1
            if (mod_sig.get()):
                check_ += 1
            if (car_sig.get()):
                check_ += 1
            if (mes_sig.get()):
                check_ += 1
            Amplitde=[]
            Amplitude_carrier = []
            Amplitude_send=[]
            time_ = []
            m_f = fre_m.get()

            time_period=((1/m_f)*scale_factor.get()/10)/10000
            for i in range(1,10000,1):
                time_.append(time_period*i)
                Amplitde.append(Amp_m.get()*(np.cos(2*math.pi*m_f*(time_period*i))))
                Amplitude_carrier.append(Amp_c.get()*(np.cos(2*math.pi*fre_c.get()*(time_period*i))))
                Amplitude_send.append(Amp_c.get()*(np.cos(2*math.pi*fre_c.get()*(time_period*i)+(fre_sen.get()*Amp_m.get()/fre_m.get())*(np.sin(2*math.pi*fre_m.get()*(time_period*i))))))
                #Amplitude_phase.append(Amp_c.get()*(np.cos(2*math.pi*fre_c.get()*(time_period*i)+(fre_sen.get()*Amp_m.get())*(np.cos(2*math.pi*m_f*(time_period*i))))))


            #fig = Figure(figsize=(15, 6), facecolor='pink', edgecolor='green', linewidth=1)
            fig.clf()
            if (mod_sig.get()):
                axis = fig.add_subplot(1, check_, inc_)
                axis.plot(time_, Amplitde)
                axis.set_xlabel('time(Sec)')
                axis.set_ylabel('Amplitude(Volt)')
                axis.set_title('Amplitude Vs Time of modulating signal')
                axis.grid(linestyle='-')
                inc_ += 1
            if (car_sig.get()):
                carrier_graph = fig.add_subplot(1, check_, inc_)
                carrier_graph.plot(time_, Amplitude_carrier)
                carrier_graph.set_xlabel('time(Sec)')
                carrier_graph.set_ylabel('Amplitude(Volt)')
                carrier_graph.set_title('Amplitude Vs Time of carrier signal')
                carrier_graph.grid(linestyle='-')
                inc_ += 1
            if (mes_sig.get()):
                sender_graph = fig.add_subplot(1, check_, inc_)
                sender_graph.plot(time_, Amplitude_send)
                sender_graph.set_xlabel('time(Sec)')
                sender_graph.set_ylabel('Amplitude(Volt)')
                sender_graph.set_title('Amplitude Vs Time of message signal')
                sender_graph.grid(linestyle='-')
                inc_ += 1
            #Amplitude_ph = fig.add_subplot(2, 2, 4)
            #Amplitude_ph.plot(time_, Amplitude_phase)
            #Amplitude_ph.set_xlabel('time(Sec)')
            #Amplitude_ph.set_ylabel('Amplitude(Volt)')
            #sender_graph.title('Amplitude Vs Time of sender signal')
            #axis.set_ylim(-10, 1 * sc_y + 10)
            #axis.set_xlim(-10, max_range + 10)

            canvas = FigureCanvasTkAgg(fig, master=modulation_window)
            canvas._tkcanvas.grid(row=7, column=0, columnspan=3, sticky=tk.EW)
            #modulation_window.update()
        except:
            msg.showerror('Input Entry Error','Please Enter Valid Number')

    modulation_window = tk.Tk(className='Frequency Modulation')

    fig = Figure(figsize=(13, 4), facecolor='HoneyDew', edgecolor='green', linewidth=1)
    canvas = FigureCanvasTkAgg(fig, master=modulation_window)
    create_menu.create_menu_bar1(modulation_window, canvas)

    modulation_window.configure(background='MintCream')

    modulation_window.resizable(False, False)
    Amp_c = tk.DoubleVar(modulation_window)
    fre_c=tk.DoubleVar(modulation_window)
    Amp_m=tk.DoubleVar(modulation_window)
    fre_m=tk.DoubleVar(modulation_window)
    fre_sen = tk.DoubleVar(modulation_window)
    ttk.Label(modulation_window, text='Carrier Signal Amplitude :').grid(row=0, column=0,sticky=tk.E)
    Entry(modulation_window,textvariable=Amp_c).grid(row=0, column=1,sticky=tk.W)
    ttk.Label(modulation_window,text='Carrier Signal Frequency :').grid(row=1, column=0, sticky=tk.E)
    Entry(modulation_window,textvariable=fre_c).grid(row=1,column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Modulating Signal Amplitude :').grid(row=2, column=0, sticky=tk.E)
    Entry(modulation_window, textvariable=Amp_m).grid(row=2, column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Modulating Signal Frequency :').grid(row=3, column=0,sticky=tk.E)
    Entry(modulation_window, textvariable=fre_m).grid(row=3, column=1, sticky=tk.W)
    ttk.Label(modulation_window, text='frequency Sensitivity :').grid(row=4, column=0,sticky=tk.E)
    Entry(modulation_window, textvariable=fre_sen).grid(row=4, column=1,sticky=tk.W)
    scale_factor = tk.DoubleVar(modulation_window)
    ttk.Label(modulation_window, text='scaling factor : ').grid(row=5, column=0, sticky=tk.E)
    scale_y = Scale(modulation_window, variable=scale_factor, from_=0, to=100, orient=HORIZONTAL).grid(row=5,
                                                                                                     column=1,
                                                                                                       sticky=tk.EW)
    # check box making
    tk.Label(modulation_window, text='Select to plot Graph').grid(row=0, column=2, sticky=tk.W)
    mod_sig = tk.IntVar(modulation_window)
    check1 = tk.Checkbutton(modulation_window, text="Modulating Signal", variable=mod_sig)  # ,state='disabled')
    check1.deselect()
    check1.grid(row=1, column=2, sticky=tk.W)
    car_sig = tk.IntVar(modulation_window)
    check2 = tk.Checkbutton(modulation_window, text="Carrier Signal", variable=car_sig)
    check2.deselect()
    check2.grid(row=2, column=2, sticky=tk.W)
    mes_sig = tk.IntVar(modulation_window)
    check3 = tk.Checkbutton(modulation_window, text='Message Signal', variable=mes_sig)
    check3.select()
    check3.grid(row=3, column=2, sticky=tk.W)

    action=ttk.Button(modulation_window,command=plot_FM,text='Plot Graph').grid(row=6,column=0,sticky=tk.E)

def Plot_Phase_Modulation():
    def plot_PM():
        save_mod(Amp_c.get(), fre_c.get(), Amp_m.get(), fre_m.get(), phase_sen.get(), 'PM')
        try:
            check_ = 0
            inc_=1
            if (mod_sig.get()):
                check_ += 1
            if (car_sig.get()):
                check_ += 1
            if (mes_sig.get()):
                check_ += 1

            Amplitde=[]
            Amplitude_carrier = []
            Amplitude_send=[]
            time_ = []
            m_f = fre_m.get()

            time_period=((1/m_f)*scale_factor.get()/10)/10000
            for i in range(1,10000,1):
                time_.append(time_period*i)
                Amplitde.append(Amp_m.get()*(np.cos(2*math.pi*m_f*(time_period*i))))
                Amplitude_carrier.append(Amp_c.get()*(np.cos(2*math.pi*fre_c.get()*(time_period*i))))
                Amplitude_send.append(Amp_c.get()*(np.cos(2*math.pi*fre_c.get()*(time_period*i)+(phase_sen.get()*Amp_m.get())*(np.cos(2*math.pi*m_f*(time_period*i))))))

            #fig = Figure(figsize=(15, 6), facecolor='HoneyDew', edgecolor='green', linewidth=1)
            fig.clf()
            if (mod_sig.get()):
                axis = fig.add_subplot(1, check_, inc_)
                axis.plot(time_, Amplitde)
                axis.set_xlabel('time(Sec)')
                axis.set_ylabel('Amplitude(Volt)')
                axis.set_title('Amplitude Vs Time of modulating signal')
                axis.grid(linestyle='-')
                inc_ += 1
            if (car_sig.get()):
                carrier_graph = fig.add_subplot(1, check_, inc_)
                carrier_graph.plot(time_, Amplitude_carrier)
                carrier_graph.set_xlabel('time(Sec)')
                carrier_graph.set_ylabel('Amplitude(Volt)')
                carrier_graph.set_title('Amplitude Vs Time of carrier signal')
                carrier_graph.grid(linestyle='-')
                inc_ += 1
            if (mes_sig.get()):
                sender_graph = fig.add_subplot(1, check_, inc_)
                sender_graph.plot(time_, Amplitude_send)
                sender_graph.set_xlabel('time(Sec)')
                sender_graph.set_ylabel('Amplitude(Volt)')
                sender_graph.set_title('Amplitude Vs Time of message signal')
                sender_graph.grid(linestyle='-')
                inc_ += 1

            #Amplitude_ph = fig.add_subplot(2, 2, 4)
            #Amplitude_ph.plot(time_, Amplitude_phase)
            #Amplitude_ph.set_xlabel('time(Sec)')
            #Amplitude_ph.set_ylabel('Amplitude(Volt)')
            #sender_graph.title('Amplitude Vs Time of sender signal')
            #axis.set_ylim(-10, 1 * sc_y + 10)
            #axis.set_xlim(-10, max_range + 10)
            #axis.grid(linestyle='-')
            #sender_graph.grid(linestyle='-')
            #carrier_graph.grid(linestyle='-')
            #Amplitude_ph.grid(linestyle='-')

            canvas = FigureCanvasTkAgg(fig, master=modulation_window)
            canvas._tkcanvas.grid(row=7, column=0, columnspan=3, sticky=tk.EW)
            modulation_window.update()
        except:
            msg.showerror('Input Entry Error','Please Enter Valid Number')
    modulation_window = tk.Tk(className='Phase Modulation')

    fig = Figure(figsize=(13, 4), facecolor='HoneyDew', edgecolor='green', linewidth=1)
    canvas = FigureCanvasTkAgg(fig, master=modulation_window)
    create_menu.create_menu_bar1(modulation_window, canvas)

    #icon_background(modulation_window,photo)
    #modulation_window.iconbitmap(photo)

    modulation_window.configure(background='MintCream')
    modulation_window.resizable(False, False)
    Amp_c = tk.DoubleVar(modulation_window)
    fre_c=tk.DoubleVar(modulation_window)
    Amp_m=tk.DoubleVar(modulation_window)
    fre_m=tk.DoubleVar(modulation_window)
    phase_sen = tk.DoubleVar(modulation_window)
    ttk.Label(modulation_window, text='Carrier Signal Amplitude :').grid(row=0, column=0,sticky=tk.E)
    Entry(modulation_window,textvariable=Amp_c).grid(row=0, column=1,sticky=tk.W)
    ttk.Label(modulation_window,text='Carrier Signal Frequency :').grid(row=1, column=0,sticky=tk.E)
    Entry(modulation_window,textvariable=fre_c).grid(row=1,column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Modulating Signal Amplitude :').grid(row=2, column=0,sticky=tk.E)
    Entry(modulation_window, textvariable=Amp_m).grid(row=2, column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Modulating Signal Frequency :').grid(row=3, column=0,sticky=tk.E)
    Entry(modulation_window, textvariable=fre_m).grid(row=3, column=1,sticky=tk.W)
    ttk.Label(modulation_window, text='Phase Sensitivity :').grid(row=4, column=0,sticky=tk.E)
    Entry(modulation_window, textvariable=phase_sen).grid(row=4, column=1,sticky=tk.W)
    scale_factor = tk.DoubleVar(modulation_window)
    ttk.Label(modulation_window, text='scaling factor : ').grid(row=5, column=0, sticky=tk.E)
    scale_y = Scale(modulation_window, variable=scale_factor, from_=0, to=100, orient=HORIZONTAL).grid(row=5,
                                                                                                       column=1,
                                                                                                       sticky=tk.EW)
    # check box making
    tk.Label(modulation_window, text='Select to plot Graph').grid(row=0, column=2, sticky=tk.W)
    mod_sig = tk.IntVar(modulation_window)
    check1 = tk.Checkbutton(modulation_window, text="Modulating Signal", variable=mod_sig)  # ,state='disabled')
    check1.deselect()
    check1.grid(row=1, column=2, sticky=tk.W)
    car_sig = tk.IntVar(modulation_window)
    check2 = tk.Checkbutton(modulation_window, text="Carrier Signal", variable=car_sig)
    check2.deselect()
    check2.grid(row=2, column=2, sticky=tk.W)
    mes_sig = tk.IntVar(modulation_window)
    check3 = tk.Checkbutton(modulation_window, text='Message Signal', variable=mes_sig)
    check3.select()
    check3.grid(row=3, column=2, sticky=tk.W)

    action=ttk.Button(modulation_window,command=plot_PM,text='Plot Graph').grid(row=6,column=0,sticky=tk.E)
