# Importing Libraries
import pandas as pd
import time
from credentials import User_Details
import getpass


class User_Verification:

    def __init__(self, data = None):

        self._data = data


    # Function for New User to Sign Up
    def signup(self):

        print()
        print()
        print()
        print("=" * 90)
        print("🌍  Welcome to OffBeat Destinations!  ✈️".center(90))
        print("=" * 90)
        print("👒 Please sign up to book your magical holidays 🏖️".center(90))
        print("=" * 90)

        # Sign Up Console for New User
        user = input("👤  Username : ")
        pwd = getpass.getpass("🔑  Password : ")
        email = input("📧  Email ID : ")
        address = input("📮  Address  : ")
        phone = input("☎️   Contact Details : ")

        new_details = User_Details(username = user, password = pwd, mail = email, address_details = address, contact = phone)
        new_details.add_user_to_backend()
        
        time.sleep(2)
        print()
        print("=" * 90)
        print("😁  Account Successfully Created!  😁".center(90))
        print("=" * 90)        
        print()
        time.sleep(2)
        print("=" * 90)
        print("🌍  Welcome to OffBeat Destinations!  ✈️".center(90))
        print("=" * 90)
        print()
        print("=" * 90)
        print("⭐ Please Login using your Credentials ⭐".center(90))
        print("=" * 90)

        # Login Console for New User
        user_check = input("👤  Username : ")
        pwd_check = getpass.getpass("🔑  Password : ")

        self._data = new_details.authenticate_user(check_user=user_check, check_password=pwd_check)

        time.sleep(1)

        print("=" * 90)
        print("🌍  Welcome to OffBeat Destinations!  ✈️".center(90))
        print("=" * 90)
        print("Discover unique stays and hidden gems across the globe.".center(90))
        print("=" * 90)
        print("\n🏡  Book your next offbeat stay now and explore like never before!")
        print("🌐  Visit: www.offbeatdestinations.com")
        print("📧  Contact: hello@offbeatdestinations.com")
        print("=" * 90)
        print("© 2025 OffBeat Destinations. All rights reserved.".center(90))
        print("=" * 90)
        print()
        print("📍      Featured Destinations:      📍".center(90))
        print()

        return self._data






#test = User_Verification()
#data = test.signup()
#print(data)
