from send_email import send_mail
from tkinter import *
from tkinter import ttk
from billing import gen_bill
from send_image import send_image
from printing import print_pdf
import sqlite3
import threading
from datetime import date
import csv
from db_init import initializedb

conn = sqlite3.connect('attitude.db')
initializedb()

global count
count = 0
apparels = {'y':'SHIRT','b':'BELT','t':'TSHIRT','j':'JEANS','p':'PANTS','i':'INNERWEAR','o':'SHORTS','u':'TRACK PANT'}


root = Tk()
root.title('Attitude')
root.geometry("600x600")

'''

main_frame = Frame(rt)
main_frame.pack(fill=BOTH,expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

my_scrollbar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

root = Frame(my_canvas)

my_canvas.create_window((0,0),window=root,anchor='nw')
'''

frametree = Frame(root)
frametree.pack(pady=10)

tree = ttk.Treeview(frametree)
tree.pack(side='left')

vsb = ttk.Scrollbar(frametree, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')

tree.configure(yscrollcommand=vsb.set)


tree['columns'] = ('Particulars','Rate')

tree.column('#0',width=0,stretch=NO)
tree.column('Particulars',anchor=W,width=180,minwidth=25)
tree.column('Rate',anchor=CENTER,width=120,minwidth=25)

tree.heading('#0',text='',anchor=W)
tree.heading('Particulars',text='Particulars',anchor=CENTER)
tree.heading('Rate',text='Rate',anchor=CENTER)

frametot = Frame(root)
frametot.pack(pady=5)

disclabel = Label(frametot,text=f'DISC : {0}')
disclabel.pack(side='right')
totallabel = Label(frametot,text=f'TOTAL : {0}')
totallabel.pack(side='right')

frame2 = Frame(root)
frame2.pack(pady=10)

pl = Label(frame2,text='Particulars')
pl.grid(row=1,column=1)

rl = Label(frame2,text='Rate')
rl.grid(row=1,column=2)

pe = Entry(frame2)
pe.grid(row=2,column=1)

pe.focus_set()

re = Entry(frame2)
re.grid(row=2,column=2)

def particular_entry_bind(event=''):
    x = pe.get()
    if apparels.get(x.lower(),-1)!=-1:
        pe.delete(0, END)
        pe.insert(END, apparels[x.lower()])
    re.focus_set()

def add_item(event=''):
    global count
    if not (pe.get().strip()=='' or re.get().strip()==''):
        rate = int(''.join([k for k in re.get().split() if k.isdigit()]))
        tree.insert(parent='',index='end',iid=count,text='',values=(pe.get(),rate))
        count+=1
        pe.delete(0, END)
        re.delete(0, END)
        disc_price()
    pe.focus_set()

pe.bind('<Return>',particular_entry_bind)
re.bind('<Return>', add_item)
pe.bind('<Down>',lambda event:phonee.focus_set())
re.bind('<Down>',lambda event:phonee.focus_set())
pe.bind('<Left>',lambda event:disce.focus_set())
re.bind('<Left>',lambda event:pe.focus_set())
    
def remove_item(event=''):
    x = tree.selection()
    for i in x:
        tree.delete(i)
    disc_price()
        
def remove_all():
    for i in tree.get_children():
        tree.delete(i)
    totallabel.config(text=f'TOTAL : {0}')
    disclabel.config(text=f'DISC : {0}')
    disce.delete(0, END)
    disce.insert(END, '0')
    pe.delete(0, END)
    re.delete(0, END)
    phonee.delete(0, END)
    namee.delete(0,END)
    dobe.delete(0,END)
    pe.focus_set()

def checkphone():
    number = phonee.get()
    cursor = conn.execute(f'''SELECT * FROM CUSTOMER WHERE PHONE="{number}"''')
    if len(cursor.fetchall())==0:
        return False
    else:
        cursor1 = conn.execute(f'''SELECT NAME,DOB FROM CUSTOMER WHERE PHONE="{number}"''')
        return cursor1.fetchone()
        
def create_bill(bill_no,sent):
    my_list = []
    number = phonee.get()
    for line in tree.get_children():
        record = []
        for value in tree.item(line)['values']:
            record.append(value)
        my_list.append(record)
    if checkphone()==False:
        nam = namee.get()
        do = dobe.get()
        conn.execute(f'''INSERT INTO CUSTOMER VALUES({number},'{nam}','{do}')''')
        conn.commit()
    else:
        nam = namee.get()
        do = dobe.get()
        conn.execute(f'''UPDATE CUSTOMER SET NAME='{nam}', DOB='{do}' WHERE PHONE="{number}"''')
        conn.commit()
    date_today = date.today().strftime("%d-%m-%Y")
    total = gen_bill(my_list,int(disce.get()),bill_no)
    if total!=False:
        conn.execute(f'''INSERT INTO BILLS VALUES({bill_no},{number},{total},"{date_today}",{sent},{0})''')
        conn.commit()

def next_bill_no():
    cursor = conn.execute(f'''SELECT * FROM BILLS''')
    if len(cursor.fetchall())==0:
        return 0
    else:
        cursor1 = conn.execute(f'''SELECT MAX(BILLNO) FROM BILLS''')
        x = cursor1.fetchone()
        return (x[0]+1)
    
def last_bill_no():
    cursor = conn.execute(f'''SELECT * FROM BILLS''')
    if len(cursor.fetchall())==0:
        return -1
    else:
        cursor1 = conn.execute(f'''SELECT MAX(BILLNO) FROM BILLS WHERE SENT=1''')
        x = cursor1.fetchone()
        return x[0]
        
def print_bill(event=''):
    bill_no = next_bill_no()
    create_bill(bill_no,1)
    print_pdf(str(bill_no))
    count = 0
    remove_all()

def save_bill(event=''):
    bill_no = next_bill_no()
    create_bill(bill_no,0)
    count = 0
    remove_all()

def send_prev(event=''):
    bill_no = last_bill_no()
    if bill_no==-1:
        return
    else:
        data = conn.execute(f'''SELECT BILLNO,PHONE FROM BILLS WHERE BILLNO='{bill_no}' ''').fetchall()
        for i in data:
            try:
                processThread = threading.Thread(target=send_image, args=(str(i[1]), str(i[0])))
                processThread.start()
            except:
                print('INTERNET DOWN!!')
    

def send_saved_bills(event=''):
    conn1 = sqlite3.connect('attitude.db')
    data = conn1.execute('''SELECT BILLNO,PHONE FROM BILLS WHERE SENT=0''').fetchall()
    for i in data:
        try:
            send_image(str(i[1]), str(i[0]))
            conn1.execute(f'''UPDATE BILLS SET SENT=1 WHERE BILLNO={i[0]}''')
            conn1.commit()
        except:
            print('INTERNET DOWN!!')
        
def whatsapp_bill(event=''):
    bill_no = next_bill_no()
    create_bill(bill_no,1)
    try:
        processThread = threading.Thread(target=send_image, args=(str(phonee.get()), str(bill_no)))
        processThread.start()
        count = 0
        remove_all()
    except:
        print_pdf(str(bill_no))
        count = 0
        remove_all()

def send_ca(event=''):
    cur = conn.cursor()
    data = cur.execute('''SELECT BILLNO,BILLDATE,TOTAL FROM BILLS WHERE SENT_CA=0''').fetchall()

    with open('bill_records.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['BILLNO','DATE','TOTAL'])
        writer.writerows(data)

    send_mail()

    for i in data:
        try:
            conn.execute(f'''UPDATE BILLS SET SENT_CA=1 WHERE BILLNO={i[0]}''')
            conn.commit()
        except:
            print('DB ERROR!!')

custframe = Frame(root)
custframe.pack(pady=20)

phonel = Label(custframe,text='Phone Number : ')
phonel.grid(row=0,column=0)

phonee = Entry(custframe)
phonee.grid(row=0,column=1)

def after_phone(event=''):
    x = checkphone()
    if x==False:
        namee.focus_set()
    else:
        dobe.delete(0, END)
        dobe.insert(END, x[1])
        namee.delete(0, END)
        namee.insert(END,x[0])
        disce.focus_set()

phonee.bind('<Return>', after_phone)

root.bind('<Control_L><w>',whatsapp_bill)
root.bind('<Control_L><p>',print_bill)
root.bind('<Control_L><s>',save_bill)
root.bind('Delete',remove_item)

namel = Label(custframe,text='Name : ')
namel.grid(row=0,column=3)

namee = Entry(custframe)
namee.grid(row=0,column=4)
namee.bind('<Return>', lambda event:dobe.focus_set())

dobl = Label(custframe,text='DOB : ')
dobl.grid(row=1,column=0)

dobe = Entry(custframe)
dobe.grid(row=1,column=1)
dobe.bind('<Return>', lambda event:disce.focus_set())

discl = Label(custframe,text='Discount : ')
discl.grid(row=1,column=3)
disce = Entry(custframe)
disce.grid(row=1,column=4)
disce.insert(END, '0')

def disc_price(event=''):
    my_list = []
    for line in tree.get_children():
        record = []
        for value in tree.item(line)['values']:
            record.append(value)
        my_list.append(record)
    sum_items = 0
    for i in my_list:
        try:
            sum_items+=int(i[1])
        except:
            sum_items+=int(''.join([k for k in i[1].split() if k.isdigit()]))
        totallabel.config(text=f"TOTAL : {sum_items}")
    if (disce.get()).isnumeric() and disce.get()!='0':
        disclabel.config(text=f"DISC : {round((sum_items - sum_items*int(disce.get())/100)/10)*10}")
    else:
        disclabel.config(text=f"DISC : {sum_items}")
    pe.focus_set()

disce.bind('<Return>',disc_price)

frame3 = Frame(root)
frame3.pack(pady=2)

addbtn = Button(frame3,text='ADD ITEM',command=add_item)
addbtn.grid(row=2,column=0,padx=5)

rembtn = Button(frame3,text='REMOVE SELECTED',command=remove_item)
rembtn.grid(row=2,column=1,padx=5)

send_saved_billsbtn = Button(frame3,text='SEND UNSENT',command=send_saved_bills)
send_saved_billsbtn.grid(row=2,column=2,padx=5)

send_cabtn = Button(frame3,text='SEND TO CA',command=send_ca)
send_cabtn.grid(row=2,column=3,padx=5)

frame4 = Frame(root)
frame4.pack(pady=10)

printbillbtn = Button(frame4,text='PRINT BILL',command=print_bill)
printbillbtn.grid(row=0,column=1,padx=5)

whatsappbillbtn = Button(frame4,text='WHATSAPP BILL',command=whatsapp_bill)
whatsappbillbtn.grid(row=0,column=2,padx=5)

save_billbtn = Button(frame4,text='SAVE BILL',command=save_bill)
save_billbtn.grid(row=0,column=3,padx=5)

send_prevbtn = Button(frame4,text='SEND PREV',command=send_prev)
send_prevbtn.grid(row=0,column=4,padx=5)

root.mainloop()
