from flask import Flask, request, render_template, send_from_directory
import os
from flask import flash , redirect, url_for, send_file
import pandas as pd
import pyodbc


def read_database(sql):


    server = ""
    database = ""
    username = ""
    password = ""
    driver = '{ODBC Driver 17 for SQL Server}'
    connect = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    db = connect.cursor()
    db.execute(sql)
    data = db.fetchall()

    # Stopping the connection
    db.close()
    return data


# Starting a flask app
app = Flask(__name__)

# Saving file settings

data = list(read_database("select * from lastReport"))

places = []
cities = []
time = []
usually =[]
live = []
usually_height = []
live_height = []

for i in data:
    places.append(i[0])
    cities.append(i[1].replace(" ", ""))
    time.append(i[2])
    usually.append(i[3])
    live.append(i[4])
    usually_height.append(i[5])
    live_height.append(i[6])
live_table = pd.DataFrame({"עיר": cities, "מקום":places, "זמן":time, "בדרך כלל":usually, "דוח חי":live, 'ציון עומס בד"כ':usually_height, "ציון בזמן אמת":live_height})

def filter(name):
    name = live_table["עיר"] == name
    return name

kiriyat_gat = live_table[filter("KriyatGat")]
ashkelon = live_table[filter("Ashkelon")]
Netivot = live_table[filter("Netivot")]
Ofakim = live_table[filter("Ofakim")]
BeerSheva = live_table[filter("BeerSheva")]
KriyatMalachi = live_table[filter("KriyatMalachi")]
Sderot = live_table[filter("Sderot")]

kiriyat_gat = kiriyat_gat.to_html(index=None).replace("...","")
ashkelon = ashkelon.to_html(index=None).replace("...","")
Netivot = Netivot.to_html(index=None).replace("...","")
Ofakim = Ofakim.to_html(index=None).replace("...","")
BeerSheva = BeerSheva.to_html(index=None).replace("...","")
KriyatMalachi = KriyatMalachi.to_html(index=None).replace("...","")
Sderot = Sderot.to_html(index=None).replace("...","")


# Flask webapp index page

@app.route('/')
def my_form():
    return render_template('index.html', table_kiriyat=kiriyat_gat, table_ashkelon=ashkelon, table_beersheeva=BeerSheva, table_ofakim=Ofakim, table_netivot=Netivot, table_malachi=KriyatMalachi, table_sderot=Sderot)



# Running the app
if __name__ == "__main__":
    app.run(port=3500, debug=True)
print("site up")
