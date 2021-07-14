import sqlite3

def initializedb():

    try:

        conn = sqlite3.connect('attitude.db')

        conn.execute('''CREATE TABLE CUSTOMER
                    (PHONE NUMERIC(10,0) PRIMARY KEY,
                    NAME VARCHAR(100) ,
                    DOB VARCHAR(100)
                    )
        ''')

        conn.execute('''CREATE TABLE BILLS
                    (BILLNO INT PRIMARY KEY,
                    PHONE NUMERIC(10,0),
                    TOTAL INT NOT NULL,
                    BILLDATE VARCHAR(100) NOT NULL,
                    SENT INT NOT NULL,
                    SENT_CA INT NOT NULL
                    )        
        ''')
    except:
        return


#initializedb()
