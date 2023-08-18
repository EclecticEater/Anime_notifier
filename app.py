import requests
from bs4 import BeautifulSoup
import pymysql as mysql
import boto3

ENDPOINT = "dbtest.cg0s9ns2wzns.us-east-1.rds.amazonaws.com"
PORT = 3306
USER = "iam"
REGION = "us-east-1"
DB_NAME = "dbtest"


def lambda_handler(event, context):
    print("working")
    client = boto3.client('sesv2')
    rdsclient = boto3.client('rds')

    print("connecting to DB")

    token = rdsclient.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

    mydb = mysql.connect(host=ENDPOINT, user=USER, password=token, port=PORT, ssl_ca="global-bundle.pem")

    Updated_anime = []

    print("going to website")

    r = requests.get('https://4anime.gg/home')

    r = BeautifulSoup(r.text, 'html.parser')

    body = r.body

    recently_updated = body.contents[5].contents[7].contents[1].contents[3]

    swiper_wrapper = recently_updated.contents[3].contents[1].contents[3].contents[1]

    for anime in swiper_wrapper.find_all(class_="anime_name headingA1 text-cut"):
        Updated_anime.append(str(anime.contents[0].string))
        print(anime.contents[0].string)

    print("fetching DB contents")

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Schema.Anime")
    myresult = mycursor.fetchall()

    print("Checking if anime is in DB")

    for anime in Updated_anime:
        anime_exist = 0
        for row in myresult:
            if row[1] == anime:
                anime_exist = 1
                if row[2] == 1:
                    Subject = anime + " has a new episode released"
                    response = client.send_email(
                        FromEmailAddress='justinpop24@gmail.com',
                        Destination={'ToAddresses': ['justinpop24@gmail.com']},
                        ReplyToAddresses=['justinpop24@gmail.com'],
                        Content={
                            'Simple': {
                                'Subject': {
                                    'Data': Subject
                                },
                                'Body': {
                                    'Text': {
                                        'Data': 'Enjoy!'
                                    },
                                }
                            },
                        },
                    )

        if anime_exist == 0:
            print(anime + " not found in DB")
            sql = "INSERT INTO Schema.Anime (Anime_Name, Wanted) VALUES (%s, %s)"
            val = (anime, "0")
            mycursor.execute(sql, val)

    mydb.commit()

lambda_handler(1, 1)