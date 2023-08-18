import pymysql as mysql
from flask import Flask, render_template
import boto3

ENDPOINT = "dbtest.cg0s9ns2wzns.us-east-1.rds.amazonaws.com"
PORT = 3306
USER = "iam"
REGION = "us-east-1"
DB_NAME = "dbtest"

application = Flask(__name__)

rdsclient = boto3.client('rds')

token = rdsclient.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

mydb = mysql.connect(host=ENDPOINT, user=USER, password=token, port=PORT, ssl_ca="global-bundle.pem")

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Schema.Anime")
myresult = mycursor.fetchall()

@application.route('/')
def hello():
    return render_template('basic_table.html', title='Basic Table', users=myresult)


@application.route('/add/<arg>')
def wanted(arg):
    sql = "UPDATE Schema.Anime SET Wanted = 1 WHERE Anime_Name = \"%s\"" % arg

    mycursor.execute(sql)

    mydb.commit()

    return arg + " set as wanted"


@application.route('/remove/<arg>')
def dontwant(arg):
    sql = "UPDATE Schema.Anime SET Wanted = 0 WHERE Anime_Name = \"%s\"" % arg
    mycursor.execute(sql)
    mydb.commit()
    return arg + " removed"



if __name__ == '__main__':
    application.run(port=8000)
