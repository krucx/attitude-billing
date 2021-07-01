import sqlite3
import csv

conn = sqlite3.connect('attitude.db')

#conn.text_factory = str

cur = conn.cursor()
data = cur.execute('''SELECT * FROM CUSTOMER''').fetchall()

with open('customers.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['PHONE','NAME','DOB'])
    writer.writerows(data)

cur1 = conn.cursor()
data1 = cur1.execute('''SELECT * FROM BILLS''').fetchall()

with open('bills.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['BILLNO','PHONE','TOTAL','DATE','SENT','SENT_CA'])
    writer.writerows(data1)


 