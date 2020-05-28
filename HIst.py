from tkinter import *
import sqlite3
import tkinter as tk
import create_menu
import tkinter.scrolledtext as st
import tkinter.scrolledtext as st


'''This part is connecting to the database, creating the tables, and adding data.
You can change this part by connecting to a different database, making different tables,
columns, datatypes, and inputs. But this is the basic format.'''

def print_hist():
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    column_name_mod = ['ID', 'Carrier_Ampl', 'Carrier_Freq', 'Modulating_Amp', 'Modulating_Fre',
                       'sensitivity', 'Mod_type']

    command='CREATE TABLE IF NOT EXISTS history_mod3(ID INTEGER PRIMARY KEY AUTOINCREMENT,Carrier_Amplitude int, Carrier_Frequency int,Modulating_Amplitude int, Modulating_Frequency int,sensitivity float real);'
    db_conn.execute(command)
    db_conn.commit()
    print("connection established")
    for i in range(30):
        db_conn.execute('INSERT INTO history_mod3(Carrier_Amplitude,Carrier_Frequency,Modulating_Amplitude,Modulating_Frequency,sensitivity,Mod_type) VALUES(100,10000,100,10000,10.0,"A.m");')
        db_conn.commit()
        db_conn.execute('INSERT INTO history_mod3(Carrier_Amplitude,Carrier_Frequency,Modulating_Amplitude,Modulating_Frequency,sensitivity,Mod_type) VALUES(100,10000,100,10000,10,"p.m");')
        db_conn.commit()
    command='select * from history_mod3'
    c.execute(command)
    rows=c.fetchall()
    hist_window1 = tk.Tk(className='Diode Simulation')
    # icon_background(modulation_window,photo)
    hist_window1.configure(background='AntiqueWhite1')
    create_menu.create_menu_bar(hist_window1)
    hist_window1.resizable(False, False)

    tk.Label(hist_window1,text="ScrolledText Widget Example",font=("Times New Roman", 15),background='green',foreground="white").grid(column=0,row=0)

    # Creating scrolled text area
    # widget with Read only by
    # disabling the state
    text_area = st.ScrolledText(hist_window1,width=100,height=16,font=("Times New Roman",15))
    text_area.grid(column=0, pady=10, padx=10)

    for x in column_name:
        text_area.insert(tk.INSERT,x+'    ')

    for row in rows:
        for x in row:
            text_area.insert(tk.INSERT,x+'      ')

hist_window = tk.Tk(className='Diode Simulation')
# icon_background(modulation_window,photo)
hist_window.configure(background='AntiqueWhite1')
create_menu.create_menu_bar(hist_window)
hist_window.resizable(False, False)
button1=tk.Button(hist_window,bg='LightSlateGray',command=print_hist,font='Courier',activebackground='blue',activeforeground='red',text='Resistor',width=20,height=2).grid(row=1,column=0,padx=5,pady=5)

hist_window.mainloop()