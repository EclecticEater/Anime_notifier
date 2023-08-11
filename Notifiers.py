#note this is not my latest script. had to swap libraries due to issues with C code in Lambda

import requests
from bs4 import BeautifulSoup
import mysql.connector
import boto3

print("working")

Updated_anime = []

r = requests.get('https://4anime.gg/home')

r = BeautifulSoup(r.text, 'lxml')

body = r.body

recently_updated = body.contents[5].contents[7].contents[1].contents[3]

swiper_wrapper = recently_updated.contents[3].contents[1].contents[3].contents[1]

for anime in swiper_wrapper.find_all(class_="anime_name headingA1 text-cut"):
    Updated_anime.append(str(anime.contents[0].string))
print(Updated_anime)
anime_exist = 0

mydb = mysql.connector.connect(
    host="dbtest.cg0s9ns2wzns.us-east-1.rds.amazonaws.com",
    user="admin",
    password=""
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Schema.Anime")
myresult = mycursor.fetchall()

for anime in Updated_anime:
    anime_exist = 0
    for row in myresult:
        print(myresult)
        if row[1] == anime:
            anime_exist = 1
            if row[2] == 1:
                print("sending an email for: " + anime)
                client = boto3.client('sesv2')
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
