import mysql.connector
from flask import Flask

mydb = mysql.connector.connect(
    host="dbtest.cg0s9ns2wzns.us-east-1.rds.amazonaws.com",
    user="admin",
    password="g0j;Y]YO6.%()G,to}G6"
)

app = Flask(__name__)

mycursor = mydb.cursor()

@app.route('/')
def hello():
    mycursor.execute("SELECT * FROM Schema.Anime")
    myresult = mycursor.fetchall()
    y = []

    for x in myresult:
        y.append(x[1])

    return y


@app.route('/add/<arg>')
def wanted(arg):
    sql = "UPDATE Schema.Anime SET Wanted = 1 WHERE Anime_Name = \"%s\"" % arg

    mycursor.execute(sql)

    mydb.commit()

    return arg + " set as wanted"


@app.route('/remove/<arg>')
def dontwant(arg):
    sql = "UPDATE Schema.Anime SET Wanted = 0 WHERE Anime_Name = \"%s\"" % arg
    mycursor.execute(sql)
    mydb.commit()
    return arg + " removed"

if __name__ == “__main__”:
       app.run()