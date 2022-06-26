from databaseconnection import *

def dbsent(address):
    con = sqlite3.connect("addresses.db")
    cursor = con.cursor()
    
    response1 = cursor.execute("SELECT Balance FROM address_table WHERE Address=?",(address,))
    current_balance = response1.fetchone()[0]
    
    response2 = cursor.execute("SELECT Sent FROM address_table WHERE Address=?",(address,))
    current_sent = response2.fetchone()[0]

    difference = current_balance - current_sent

    if difference:
        #buraya avax transferi gelecek. current balance - current sent kadar para gönderecek. 
        cursor.execute("UPDATE address_table SET Sent = ? where Address = ?",(current_balance,address))
        con.commit()
    else:
        print("value up to date")

