import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import Menu
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import create_menu
import Modulation_package as mod
import diode
from time import sleep
from PIL import Image, ImageTk
import sqlite3


'''
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        padx=247
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

def run_progressbar():
    progress_bar['maximum']=100
    for i in range(101):
        sleep(0.02)
        progress_bar['value']=i
        progress_bar.update()
    #root.destroy()

root = tk.Tk(className='Starting Simulator')
app=FullScreenApp(root)

image = Image.open("av.jpg")
photo = ImageTk.PhotoImage(image)
create_menu.icon_background(root,photo)

canvas = Canvas(root, width = 850, height = 500)
canvas.pack()
#img = PhotoImage(file="ball.ppm")
canvas.create_image(0,0, anchor=NW, image=photo)
Label(root,text='PREPARING SIMULATOR....',font='Didot',bg='AntiqueWhite1',fg='RED').pack()

progress_bar=ttk.Progressbar(root,orient='horizontal',length=500,mode='determinate')
progress_bar.pack(padx=20,pady=10,ipadx=10,ipady=1)
Label(root,text="",font='Didot',bg='AntiqueWhite1',fg='RED',command=run_progressbar())

for i in range(5):
    sleep(.10)
Label(root,text="WELCOME for Simulation",font='Didot',bg='AntiqueWhite1',fg='green').pack(padx=20,pady=3)


root.after(230,lambda: root.destroy())
root.mainloop()

'''




main_window=tk.Tk(className='Device Simulator')
main_window.configure(background='MintCream')

main_window.resizable(False,False)
create_menu.create_menu_bar(main_window)

def save_resistance(val1=0):
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    print("connection established")
    front_='INSERT INTO Resistance (Resist) '
    front_+='VALUES ('+str(val1)+');'
    print(front_)
    db_conn.execute(front_)
    db_conn.commit()
    db_conn.close()



def plot_resistor():
    def click_me():
        try:
            volt = []
            current = []
            resistance = resist.get()
            if(resistance==0):
                msg.showerror('Division by Zero', 'Enter resitance value greater than 0')
                return
            sc_x = scale_factor_x.get()
            for i in range(0,int(sc_x),1):
                hel=i/resistance
                volt.append(i)
                current.append(hel)

            print(volt,current)
            fig = Figure(figsize=(5,4), facecolor='HoneyDew', edgecolor='green', linewidth=5)
            axis = fig.add_subplot(1, 1, 1)
            axis.plot(volt, current)
            axis.set_xlabel('voltage')
            axis.set_ylabel('current')
            plt.title('Current vs Voltage graph')
            axis.grid(linestyle='-')
            canvas = FigureCanvasTkAgg(fig, master=resistor_window)
            canvas._tkcanvas.grid(row=4,column=0,columnspan=2,sticky=tk.EW)
            save_resistance(resist.get())

        except:
            msg.showerror('Input Entry Error', 'Please Enter Valid Number')

    resistor_window=tk.Tk(className='Resistor I-V plotting')
    resistor_window.configure(background='AntiqueWhite1')
    ttk.Label(resistor_window,text='Enter Resistance value :').grid(row=0,column=0,padx=3,pady=3,sticky=tk.E)
    resist=tk.DoubleVar(resistor_window)
    resist.set(1)
    r_entered=Entry(resistor_window,textvariable=resist).grid(row=0,column=1,padx=3,pady=3,sticky=tk.W)
    #r_entered.focus()
    action = ttk.Button(resistor_window, text="plot graph",command=click_me).grid(row=3, column=0,padx=3,pady=3,sticky=tk.E)
    scale_factor_y = DoubleVar(resistor_window)
    scale_factor_x = DoubleVar(resistor_window)
    ttk.Label(resistor_window,text='scaling factor x: ').grid(row=1,column=0,sticky=tk.E)

    scale_x = Scale(resistor_window, variable=scale_factor_x, from_=0, to=1000, orient=HORIZONTAL).grid(row=1,column=1,sticky=tk.EW, columnspan=3)
    #button = Button(resistor_window, text="Get Scale Value", command=sel).grid(row=2,column=1)

    resistor_window.mainloop()
def plot_modulation():
    mod.Plot_Amplitude_Modulation()
def plot_frequency_modulation():
    mod.Plot_Frequency_Modulation()
def Plot_Phase_Modulation():
    mod.Plot_Phase_Modulation()
def diode_plot():
    diode.plot_diode()
def show_():
    msg.showinfo('Be patience','Developement is in beta mode.'
                               ' COMING SOON...')



plot_detail=tk.LabelFrame(main_window,text='Modulation',font='Didot',width=450,highlightcolor='pink',highlightbackground='pink',bd=10,bg='HoneyDew')
plot_detail.grid(row=0,column=0,padx=20,pady=10)
Label(plot_detail,text='Choose Any One to Plot Graph',bg='HoneyDew',fg='RED',font='Didot').grid(row=0,column=0,pady=10,padx=10)
#button1=tk.Button(plot_detail,bg='LightSlateGray',command=plot_resistor,font='Courier',activebackground='blue',activeforeground='red',text='resistor',width=20,height=2).grid(row=1,column=0,padx=5,pady=5)
button1=tk.Button(plot_detail,bg='LightSlateGray',command=plot_modulation,font='courier',activebackground='blue',activeforeground='red',text='Amplitude Modulation',width=20,height=2).grid(row=1,column=0,padx=5,pady=5)
button2=tk.Button(plot_detail,bg='LightSlateGray',command=plot_frequency_modulation,font='courier',activebackground='blue',activeforeground='red',text='Frequency Modulation',width=20,height=2).grid(row=2,column=0,padx=5,pady=5)
button3=tk.Button(plot_detail,bg='LightSlateGray',command=Plot_Phase_Modulation,font='courier',activebackground='blue',activeforeground='red',text='Phase Modulation',width=20,height=2).grid(row=3,column=0,padx=5,pady=5)

plot_device=tk.LabelFrame(main_window,text='Solid State Device',font='Didot',width=350,highlightcolor='pink',highlightbackground='pink',bd=10,bg='HoneyDew')
plot_device.grid(row=0,column=1,padx=20,pady=10)
Label(plot_device,text='Choose Any One to Plot characetristics',bg='HoneyDew',fg='RED',font='Didot').grid(row=0,column=0,padx=10,pady=10)
button1=tk.Button(plot_device,bg='LightSlateGray',command=plot_resistor,font='Courier',activebackground='blue',activeforeground='red',text='Resistor',width=20,height=2).grid(row=1,column=0,padx=5,pady=5)
button2=tk.Button(plot_device,bg='LightSlateGray',command=diode_plot,font='Courier',activebackground='blue',activeforeground='red',text='Diode',width=20,height=2).grid(row=2,column=0,padx=5,pady=5)
button3=tk.Button(plot_device,bg='LightSlateGray',command=show_,font='Courier',activebackground='blue',activeforeground='red',text='Transistor',width=20,height=2).grid(row=3,column=0,padx=5,pady=5)


padx = 145
pady = 720
main_window.geometry(
"{0}x{1}+0+0".format(main_window.winfo_screenwidth()-760, main_window.winfo_screenheight()-550))

main_window.mainloop()
