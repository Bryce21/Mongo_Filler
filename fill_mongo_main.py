# This code is used to quickly fill up a Mongodb collection with dummy data.
# Necessary for it to work:
#     Mongodb installed and running.
#     This program listening on the correct host and port.
#     Pymongo package installed.
#     A db and collection set up. Will have to do that manually.
#         Make sure the name listed below is correct to what you set up.
#     Useful links: https://api.mongodb.com/python/current/index.html,
#     https://docs.mongodb.com/manual/installation/ (I used homebrew for installation, made it a lot easier)
#     Couple Notes:
#           This program never empties db before adding to it. So if run a lot will keep adding data.
#               Can manually empty if necessary.
#           It is possible to get a duplicate entry but very unlikely. Not sure how Mongo would handle that.

import random
import string
from pymongo import MongoClient
import sys

# For generating words. Part of github code I found.
VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

# In order for this to work have to have a database and a collection set up.
# Data Fields:
db_name = "campus_db"
collection_name = "data_set"
how_many_to_insert = 20
port_to_use = 27017
host_to_use = "localhost"
name_length = 6

class Entry():
    def __init__(self):
        s_level = ["Undergraduate", "TA", "Teacher", "Admin"]
        self.name = generate_word(name_length) + " " + generate_word(name_length)
        self.age = random.randint(18, 55)
        self.grade = s_level[random.randint(0, 3)]

    def print_fields(self):
        print("Name: " + self.name + ", Age: " + str(self.age) + ", Grade: " + self.grade)

    def get_dictionary(self):
        return self.__dict__


# Name generation taken from github file: I didn't write.
def generate_word(length):
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def establish_connection_db(host, port):
    return MongoClient(host, port)


if __name__ == "__main__":
    try:
        client = establish_connection_db(host_to_use, port_to_use)
        db = client[db_name]
        collection = db[collection_name]
    except Exception as e:
        print("Error establishing connection to database. Is it running? Error: {}".format(e))
        sys.exit(1)
    data = []
    for i in range(how_many_to_insert):
        data.append(Entry().get_dictionary())
    try:
        collection.insert_many(data)
    except Exception as e:
        print("Error pushing data to db. Is it running? Error: {}".format(e))
        sys.exit(1)
    print("Program ran through, data should have been added.")
