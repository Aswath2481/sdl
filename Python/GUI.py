# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:20:41 2019
task : GUI approach
@author: Zero
"""

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import serial,datetime

from tkinter import scrolledtext
#global variables
name=''    

window = Tk()
window.title("GUI for serial data reception and logging")
window.geometry("490x275")
#
#dataw = Tk()
#dataw.title("Data Reception")
#dataw.geometry("500x600")

a_lbl=Label(window, text="Enter the name:  ",font=("Times New Roman",14))
a_lbl.grid(column=0,row=1,sticky=W+E+N+S,padx=7)
#
b_lbl=Label(window, text="file is waiting to be created...  ",font=("Times New Roman",14),foreground="red")
b_lbl.grid(column=1,row=5)

status_label=Label(window, text="Status :  ",font=("Times New Roman bold",14))
status_label.grid(row=5,sticky=E)

txt=Entry(window,width=20)
txt.grid(column=1,row=1)
#txt.focus()

#combo box
combo=Combobox(window)   
combo.grid(column=1,row=3)

baud_rate=Combobox(window)   
baud_rate.grid(column=0,row=3,sticky=S,padx=7)
baud_rate['values']=[9600,115200]
baud_rate.current(0)

#text area
txtbox=scrolledtext.ScrolledText(window,width=57,height=10,bg='black',fg='light green')
txtbox.grid(column=0,row=4,columnspan=3,sticky=W+E+N+S,padx=7,pady=7)

#check box
chk_state=IntVar()
chk_state.set(0)
chk=Checkbutton(window,text="Autoscroll",var=chk_state)
chk.grid(column=2,row=6)

def scanports(): 
    ports=['COM%s' % (i+1) for i in range(256) ]
    result=[]
    combo['values']=[]
    for port in ports:
        try: 
            s=serial.Serial(port)
            s.close()
            result.append(port)
        except(OSError, serial.SerialException):
            pass
    try:
#        print(result)
        combo['values']=result 
        combo.current(0)
    except:
        messagebox.showerror('Error','no valid ports')
        print('no ports')
#        combo['values']=[]
def clear():
    txtbox.delete(1.0,END)
    
def core():
    try:
        ser=serial.Serial(combo.get(),baud_rate.get())
        f1=open(name,"a")
        line=ser.readline();
        line=line.decode('utf-8') 
        line=line.replace('\n','')
        x=datetime.datetime.now()
        timestamp=x.strftime("%d/%m/%Y %H:%M:%S")
        f1.write(timestamp+","+line)
        b_lbl.configure(text='Logging....',foreground="green")      
        print(line)
        txtbox.insert(INSERT,timestamp)
        txtbox.insert(INSERT," : ")
        txtbox.insert(INSERT,line)
        txtbox.insert(INSERT,"\n")
        if chk.instate(['selected']):
            txtbox.see(END)
        window.after(40,core)
    except:
        print("Plugged out...")
        b_lbl.configure(text='Plugged out',foreground="red")
    finally:
        f1.close()
        ser.close()

def start_clicked():
    b_lbl.configure(text='processing....',foreground="orange")
    global name
    name=txt.get()
    try:
        x=datetime.datetime.now()
        name=name+"_"+x.strftime("%d_%b_%Y_%H.%M.%S")+".csv"
        print("file name : "+name+"\n")     
        file_l=Label(window, text=name,font=("Arial",7))
        file_l.grid(row=6,sticky=W,columnspan=2)
        core()
    except:
        print("Plugged out...")
        b_lbl.configure(text='No Valid Port....',foreground="red")

   
        
log_btn=Button(window,text="Start logging",command=start_clicked)
log_btn.grid(column=2,row=1)

scan_btn=Button(window,text="Scan Ports",command=scanports)
scan_btn.grid(column=2,row=3)

clr_btn=Button(window,text="Clear",command=clear)
clr_btn.grid(column=2,row=5)

scanports()
window.mainloop()
