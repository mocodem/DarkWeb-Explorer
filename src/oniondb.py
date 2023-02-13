import peewee
from peewee import *
import datetime
import sqlite3


def drop():
    sure = input("Sure to drop all data?")
    if sure == "y":
        connection = sqlite3.connect('onion.db')
        connection.execute("DROP TABLE Onion")
        print("data dropped")
        connection.close()


db = SqliteDatabase('onion.db')


class BaseModel(Model):
    class Meta:
        database = db


class Onion(BaseModel):
    url = CharField()
    source = CharField()
    url_version = CharField(null=True)
    title = CharField(null=True)
    status = IntegerField(null=True)
    connect = CharField(null=True)
    captcha = BooleanField(null=True)
    captcha_type = CharField(null=True)
    first_itc = DateTimeField()
    last_itc = DateTimeField(default=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    class Meta:
        primary_key = CompositeKey('url', 'source')


def init_db():
    db.connect()
    Onion.create_table()
    db.close()


def add_onion(url: str, source: str, title: str = None):
    # bulk insert
    try:
        query = Onion.create(url=url, source=source, first_itc=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), last_itc=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        query.url_version = check_url_verison(url)
        query.save()
        return True
    except peewee.IntegrityError as e:
        query = get_onion_source(url=url, source=source)
        query.last_itc = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        query.save()
        return True


def sanitize_url(url: str) -> str:
    if len(url.split(".onion/")) > 1:
        return url.split(".onion/")[0] + ".onion"
    elif ".onion" not in url:
        return url + ".onion"
    else:
        return url


def check_url_verison(url: str) -> str:
    url_version = url
    if ".onion" in url_version:
        url_version = url_version.split(".onion")[0]
    if "http://" in url_version:
        url_version = url_version.split("http://")[1]
    elif "https://" in url_version:
        url_version = url_version.split("https://")[1]
    if "www." in url_version:
        url_version = url_version.split("www.")[1]
    if len(url_version) == 56:
        url_version = "v3"
    elif len(url_version) == 16:
        url_version = "v2"
    else:
        url_version = "unknown"
    return url_version


def get_onion(url: str):
    return Onion.get(Onion.url == url)


def get_onion_source(url: str, source: str):
    return Onion.get(Onion.url == url, Onion.source == source)


def update_onion(url: str, key: str, value):
    query = Onion.get(Onion.url == url)
    query.key = value
    query.save()
    return True


init_db()
