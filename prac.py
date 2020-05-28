import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import create_menu

def insert_data(table_name,value,column_name):
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    command = 'INSERT INTO ' + str(table_name) + '('
    for i in range(1,len(column_name),1):
        command=command+column_name[i]
        if(i!=(len(column_name)-1)):
            command+=','
    command+=') '
    command+='VALUES'

    for i in range(0, len(value), 1):
        command = command +str(value[i])
        if (i != (len(value) - 1)):
            command += ','
    command+=');'

    print(command)
    db_conn.execute(command)
    db_conn.commit()
    db_conn.close()

def delete_all_data(table_name):
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    command = 'DELETE from '+table_name+' where ID>0;'
    db_conn.execute(command)
    db_conn.commit()

def show_table(win,table_name,val,value,column_name):
    sear=' WHERE '+str(val.get())+' >= '+str(value.get())
    db_conn = sqlite3.connect('History.db')
    c = db_conn.cursor()
    command='select * from '+str(table_name)+''+sear+';'
    print(command)
    c.execute(command)
    rows=c.fetchall()

    frn = Frame(win)
    frn.grid(row=3, column=0,columnspan=2)

    if (len(column_name) == 7):
        tv = ttk.Treeview(frn, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height=10)
        tv.pack()
        for i in range(len(column_name)):
            tv.heading(i + 1, text=column_name[i])
            tv.column(str(i + 1), minwidth=10, width=120)
        for i in rows:
            tv.insert('', 'end', values=i)

    elif (len(column_name) == 10):
        tv = ttk.Treeview(frn, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), show='headings', height=10)
        tv.pack()
        for i in range(len(column_name)):
            tv.heading(i + 1, text=column_name[i])
            tv.column(str(i + 1), minwidth=10, width=120)
        for i in rows:
            tv.insert('', 'end', values=i)
    elif (len(column_name) == 2):
        tv = ttk.Treeview(frn, columns=(1, 2), show='headings', height=10)
        tv.pack()
        for i in range(len(column_name)):
            tv.heading(i + 1, text=column_name[i])
            tv.column(str(i + 1), minwidth=10, width=120)
        for i in rows:
            tv.insert('', 'end', values=i)

    #tv = ttk.Treeview(frn, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height=10)
    #tv.pack()
    '''for i in range(len(column_name)):
        tv.heading(i+1,text=column_name[i])
        tv.column(str(i + 1), minwidth=10, width=120)'''

    '''for i in rows:
        tv.insert('','end',values=i)'''
    win.title('history')


def show_history(column_name,table_name):
    hist_window = tk.Tk(className='Input History')
    hist_window.configure(background='MintCream')
    create_menu.create_menu_bar(hist_window)
    hist_window.resizable(False, False)


    Label(hist_window, text='Search by:').grid(row=0,column=0,padx=4,pady=3,sticky=tk.E)
    val=tk.StringVar(hist_window)
    val.set(column_name[0])
    val_search=ttk.Combobox(hist_window,width=25,textvariable=val)
    val_search['values']=column_name
    val_search.grid(row=0,column=1,padx=20,pady=15,sticky=tk.W)

    Label(hist_window, text='Minimum Value :').grid(row=1,column=0,padx=4,pady=3,sticky=tk.E)
    value=IntVar(hist_window)
    value.set(0)
    Entry(hist_window, textvariable=value).grid(row=1, column=1,padx=20,pady=15,sticky=tk.W)
    button = tk.Button(hist_window, bg='LightSlateGray', command=lambda :show_table(hist_window,table_name,val,value,column_name),
                       activebackground='blue', activeforeground='red', text='SEARCH ', width=20, height=2).grid(row=2,column=0,padx=20,pady=15)
    button1 = tk.Button(hist_window, bg='LightSlateGray',
                       command=lambda: delete_all_data(table_name),
                       activebackground='blue', activeforeground='red', text='DELETE ALL HISTORY', width=20, height=2).grid(row=2,
                                                                                                                column=1,
                                                                                                                padx=20,
                                                                                                                pady=15)
    frn = Frame(hist_window)
    frn.grid(row=3, column=0, columnspan=2)
    if(len(column_name)==7):
        tv = ttk.Treeview(frn, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height=10)
        tv.pack()
        for i in range(len(column_name)):
            tv.heading(i + 1, text=column_name[i])
            tv.column(str(i+1),minwidth=10,width=120)

    elif(len(column_name)==10):
        tv = ttk.Treeview(frn, columns=(1, 2, 3, 4,5,6,7,8,9,10), show='headings', height=10)
        tv.pack()
        for i in range(len(column_name)):
            tv.heading(i + 1, text=column_name[i])
            tv.column(str(i+1),minwidth=10,width=120)
    elif (len(column_name) == 2):
        tv = ttk.Treeview(frn, columns=(1, 2), show='headings', height=10)
        tv.pack()
        for i in range(len(column_name)):
            tv.heading(i + 1, text=column_name[i])
            tv.column(str(i + 1), minwidth=10, width=120)
