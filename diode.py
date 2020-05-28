import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import Menu
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog as fd
import create_menu
import sqlite3

def save_diode(val1=0,val2=0,val3=0,val4=0,val5=0,val6=0,val7=0,val8=0,val9=0):
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    column_name_diode = ['ID','Donor_concn', 'Acceptor_concn', 'Area', 'Intrinsic_concn', 'Holes_life','Electron_life','Holes_diff','Electron_diff','Temp']
    command='INSERT INTO DIODE1(Donor_concn,Acceptor_concn,Area,Intrinsic_concn,Holes_life,Electron_life,Holes_diff,Electron_diff,Temp) VALUES('
    command=command+str(val1)+','+str(val2)+','+str(val3)+','+str(val4)+','+str(val5)+','+str(val6)+','+str(val7)+','+str(val8)+','+str(val9)+');'
    print(command)
    db_conn.execute(command)
    db_conn.commit()
    db_conn.close()

def plot_diode():

    def graph_diode():
        try:
            cnt=0
            if(f_bias.get()):
                cnt+=1
            if(r_bias.get()):
                cnt+=1
            q=1.6*pow(10,-19)
            k=1.38*pow(10,-23)
            e=2.72
            a=Area.get()*pow(10,pow_Area.get())
            ni=intrinsic.get()*pow(10,pow_intrinsic.get())
            nd=Donor_concn.get()*pow(10,pow_Donor_concn.get())
            na=acceptor_concn.get()*pow(10,pow_acceptor_concn.get())
            dp=diffusion_holes.get()*pow(10,pow_diffusion_holes.get())
            dn=diffusion_electron.get()*pow(10,pow_diffusion_electron.get())
            tp=holes_life.get()*pow(10,pow_holes_life.get())
            tn=electron_life.get()*pow(10,pow_electron_life.get())
            t=temp.get()*pow(10,pow_temp.get())

            holes=(math.sqrt(dp/tp))/nd
            electron=(math.sqrt(dn/tn))/na
            I0=q*a*ni*ni*(holes+electron)


            #I0=0.001

            pow_coe=(q)/(t*k)
            print(q,k,e,a,ni,nd,na,dp,dn,tp,tn,t,holes,electron,pow_coe,I0)
            current=[]
            v=[]

            max_vol=scale_factor.get()
            for i in range(1,max_vol,1):
                volt=i/100
                hel=pow_coe*volt
                sec_num=pow(e,hel)
                val=I0*(sec_num-1)
                current.append(val)
                v.append(volt)

            r_voltage=[]
            r_current=[]
            for i in range(1,max_vol,1):
                volt=-(i/100)
                hel=pow_coe*volt
                sec_num=pow(e,hel)
                val=I0*(sec_num-1)
                r_current.append(val)
                r_voltage.append(volt)

            print(v)
            print(current)
            fig.clf()
            inc=1
            if(f_bias.get()):
                axis = fig.add_subplot(1, cnt, inc)
                axis.plot(v, current)
                axis.set_xlabel('voltage(Volt)')
                axis.set_ylabel('Currnet(Amp)')
                axis.set_title('Current Vs Voltage')
                axis.grid(linestyle='-')
                inc+=1
            if(r_bias.get()):
                carrier_graph = fig.add_subplot(1, cnt, inc)
                carrier_graph.plot(r_current, r_voltage)
                carrier_graph.set_xlabel('voltage(Volt)')
                carrier_graph.set_ylabel('Currnet(Amp)')
                carrier_graph.set_title('Current Vs Voltage')
                carrier_graph.grid(linestyle='-')
                inc+=1



            canvas = FigureCanvasTkAgg(fig, master=diode_window)
            canvas._tkcanvas.grid(row=12, column=0, columnspan=4, sticky=tk.EW)
            # Amp_sig=Amp_c.get()*(1+(Amp_sen.get()*Amp_m.get())*(cos()))
            diode_window.update()
            save_diode(int(nd), int(na), int(a), int(ni), int(tp), int(tn), float(dp), float(dn), float(t))
        except:
            msg.showerror('Input Entry Error','Please Enter Valid Number')


    diode_window = tk.Tk(className='Diode Simulation')
    # icon_background(modulation_window,photo)
    diode_window.configure(background='MintCream')
    fig = Figure(figsize=(10, 4), facecolor='HoneyDew', edgecolor='PowderBlue', linewidth=1)
    canvas = FigureCanvasTkAgg(fig, master=diode_window)
    create_menu.create_menu_bar1(diode_window, canvas)
    diode_window.resizable(False, False)


    Donor_concn = tk.DoubleVar(diode_window)
    pow_Donor_concn=tk.IntVar(diode_window)
    pow_Donor_concn.set(20)
    Donor_concn.set(1)

    acceptor_concn=tk.DoubleVar(diode_window)
    pow_acceptor_concn=tk.IntVar(diode_window)
    pow_acceptor_concn.set(20)
    acceptor_concn.set(1)

    Area=tk.DoubleVar(diode_window)
    pow_Area=tk.IntVar(diode_window)
    pow_Area.set(4)
    Area.set(1.25)

    intrinsic=tk.DoubleVar(diode_window)
    pow_intrinsic=tk.IntVar(diode_window)
    pow_intrinsic.set(17)
    intrinsic.set(1)

    holes_life=tk.DoubleVar(diode_window)
    pow_holes_life = tk.IntVar(diode_window)
    pow_holes_life.set(-6)
    holes_life.set(1)

    electron_life=tk.DoubleVar(diode_window)
    pow_electron_life = tk.IntVar(diode_window)
    pow_electron_life.set(-6)
    electron_life.set(1)


    voltage=tk.DoubleVar(diode_window)
    pow_voltage = tk.IntVar(diode_window)
    pow_voltage.set(0)
    voltage.set(10)

    diffusion_holes=tk.DoubleVar(diode_window)
    pow_diffusion_holes = tk.IntVar(diode_window)
    pow_diffusion_holes.set(-4)
    diffusion_holes.set(4.5)


    diffusion_electron=tk.DoubleVar(diode_window)
    pow_diffusion_electron = tk.IntVar(diode_window)
    pow_diffusion_electron.set(-4)
    diffusion_electron.set(22.5)

    temp=tk.DoubleVar(diode_window)
    pow_temp = tk.IntVar(diode_window)
    pow_temp.set(0)
    temp.set(300)





    ttk.Label(diode_window, text='Donor Concenteration At N-Side ').grid(row=0, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=Donor_concn).grid(row=0, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_Donor_concn).grid(row=0, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Acceptor Concenteration At P-Side ').grid(row=1, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=acceptor_concn).grid(row=1, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_acceptor_concn).grid(row=1, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Cross Section Area ').grid(row=2, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=Area).grid(row=2, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_Area).grid(row=2, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Intrinsic Carrier Concenteration ').grid(row=3, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=intrinsic).grid(row=3, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_intrinsic).grid(row=3, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Lifetime Of Holes ').grid(row=4, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=holes_life).grid(row=4, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_holes_life).grid(row=4, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Lifetime Of Electron ').grid(row=5, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=electron_life).grid(row=5, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_electron_life).grid(row=5, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Diffusion Constant Of Holes').grid(row=6, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=diffusion_holes).grid(row=6, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_diffusion_holes).grid(row=6, column=2, sticky=tk.W)

    ttk.Label(diode_window, text='Diffusion Constant Of Electron').grid(row=7, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=diffusion_electron).grid(row=7, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_diffusion_electron).grid(row=7, column=2, sticky=tk.W)

    #tk.Label(diode_window, text='Applied Voltage ').grid(row=8, column=0, sticky=tk.W)
    #Entry(diode_window, textvariable=voltage).grid(row=8, column=1, sticky=tk.W)
    #Entry(diode_window, textvariable=pow_voltage).grid(row=8, column=2, sticky=tk.W)

    tk.Label(diode_window, text='Temperature ').grid(row=9, column=0, sticky=tk.W)
    Entry(diode_window, textvariable=temp).grid(row=9, column=1, sticky=tk.W)
    Entry(diode_window, textvariable=pow_temp).grid(row=9, column=2, sticky=tk.W)

    scale_factor = tk.IntVar(diode_window)
    ttk.Label(diode_window, text='scale_factor :').grid(row=10, column=0, sticky=tk.E)
    scaleing = Scale(diode_window, from_=0, to=1000, variable=scale_factor, orient=HORIZONTAL).grid(row=10, column=1,
                                                                                                        sticky=tk.EW)

    action = ttk.Button(diode_window, command=graph_diode, text='Plot Graph').grid(row=11, column=0, sticky=tk.E)



    tk.Label(diode_window, text='Select to plot Graph').grid(row=0, column=3, sticky=tk.W)
    f_bias = tk.IntVar(diode_window)
    check1 = tk.Checkbutton(diode_window, text="Forward Bias", variable=f_bias)
    f_bias.set(1)
    check1.grid(row=1, column=3, sticky=tk.W)
    r_bias = tk.IntVar(diode_window)
    check2 = tk.Checkbutton(diode_window, text="Reverse Bias", variable=r_bias)
    check2.deselect()
    check2.grid(row=2, column=3, sticky=tk.W)

