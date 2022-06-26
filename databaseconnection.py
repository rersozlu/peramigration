import sqlite3

con = sqlite3.connect("addresses.db")
cursor = con.cursor()

#sql table creation //adresin claim etmeye müsait olup olmadığı sorgulandıktan sonra bu tabloya eklenmeli 
def create_table():
    con = sqlite3.connect("addresses.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS address_table (Address TEXT, Balance INT, Sent INT, Date TEXT)") 
    con.commit()
    con.close()

def add_data(address, balance, date):
    con = sqlite3.connect("addresses.db")
    cursor = con.cursor()
    response = cursor.execute("SELECT EXISTS(SELECT 1 FROM address_table WHERE Address=?)", (address, ))
    fetched = response.fetchone()[0]
    if fetched:
        cursor.execute("UPDATE address_table SET Balance = ? , Date = ? where Address = ?",(balance, date, address))
        con.commit()
    else:
        cursor.execute("Insert into address_table Values(?,?,?,?)",(address,balance, 0 ,date))
        con.commit()
    con.close()