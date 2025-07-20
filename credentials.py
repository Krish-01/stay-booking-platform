from pymongo.mongo_client import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore
import pandas as pd
import getpass
import time

class User_Details:

    # Class Attribute

    ID = 'sudip1987roy'
    KEY = 'ioRjmSqnyTfxSZJA'
    CLUSTER = 'ClusterLearnMDB'

    # Initializing username and password
    def __init__(self, username, password, mail, address_details, contact, client=None):

        self._user = username
        self._password = password
        self._mail = mail
        self._address_details = address_details
        self._contact = contact
        self._client = client


    # Getter for username
    @property
    def username(self):

        return self._user


    # Getter for password
    @property
    def password(self):

        return self._password
    

    # Getter for mail
    @property
    def address_details(self):

        return self._address_details


    # Getter for address
    @property
    def mail(self):

        return self._mail
    

    # Getter for contact
    @property
    def contact(self):

        return self._contact


    # Creating connection to MongoDB Server
    def set_server_connection(self):

        # MongoDB url
        url = "mongodb+srv://" + User_Details.ID + ":" + User_Details.KEY + "@clusterlearnmdb.d10pyi5.mongodb.net/?retryWrites=true&w=majority&appName=" + User_Details.CLUSTER

        # Create a new client and connect to the server
        new_client = MongoClient(url, server_api=ServerApi('1'))

        self._client = new_client

        # Send a ping to confirm a successful connection
        try:
            self._client.admin.command('ping')
            print("=" * 90)
            print("👤  Creating your Account!  👤".center(90))
            print("=" * 90)
        except Exception as e:
            print(e)


    # Function to add New User to Backend
    def add_user_to_backend(self):

        self.set_server_connection()
        db = self._client.authenticate_user
        collection = db.details

        # Insert Details
        new_user = {
                    "username" : self.username,
                    "password" : self.password,
                    "email_id" : self.mail,
                    "address" : self.address_details,
                    "phone_no" : self.contact

                    }

        result = collection.insert_one(new_user)


    # Function to authenticate user details
    def authenticate_user(self, check_user, check_password):

        #print(check_user, self._user, check_password, self._password)

        while check_user != self._user or check_password != self._password:

            print("=" * 90)
            print("                               🕵️  Autheticating User", end=' ', flush=True)
            for _ in range(5):
                print(".", end=' ', flush=True)
                time.sleep(1)
            
            print()

            print("=" * 90)
            print("❌  Your Login credentials are incorrect. Please Try Again!  ❌".center(90))
            print("=" * 90)
            

            check_user = input("👤  Username : ")
            check_password = getpass.getpass("🔑  Password : ")


        print("=" * 90)
        print("                               🕵️  Autheticating User", end=' ', flush=True)
        for _ in range(5):
            print(".", end=' ', flush=True)
            time.sleep(1)
        
        


        # Access database and collection
        db = self._client["sample_airbnb"]
        collection = db["listingsAndReviews"]

        # Fetch all documents
        cursor = collection.find()

        # Convert to DataFrame
        df = pd.DataFrame(list(cursor))

        # Optional: Drop MongoDB's default _id column
        df.drop(columns=["_id"], inplace=True, errors='ignore')

        print()
        print("=" * 90)
        print()

        print("=" * 90)
        print("✅  User Autheticated  ✅".center(90))
        print("=" * 90)

        return df