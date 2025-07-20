# Importing Libraries
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from server_connection import User_Verification
from bson.decimal128 import Decimal128 #type:ignore
import ast
import warnings
warnings.filterwarnings("ignore")


class DataCleansing:

    def __init__(self, data=None):

        self._data = data


    # Get Data from MongoDB Server After User Verification
    def get_data(self):

        test = User_Verification()
        self._data = test.signup()
        return self._data
    

    # Clean data for further Analysis
    def perform_data_engineering(self):

        actual_data = self.get_data()
        actual_data = self.get_review_scores(actual_data)

        self._data = actual_data

        return self._data

    
    # Data Cleansing and Feature Extraction
    def get_review_scores(self, actual_data):

        actual_data['review_scores'] = actual_data['review_scores'].map(str)
        actual_data = actual_data[actual_data['review_scores'] != '{}']
        actual_data['review_scores'] = actual_data['review_scores'].apply(ast.literal_eval)
        actual_data['review_scores_cleanliness'] = actual_data['review_scores'].apply(self.get_review_scores_cleanliness)
        actual_data['review_scores_location'] = actual_data['review_scores'].apply(self.get_review_scores_location)
        actual_data['review_scores_rating'] = actual_data['review_scores'].apply(self.get_review_scores_rating)
        actual_data['address'] = actual_data['address'].map(str)
        actual_data['address'] = actual_data['address'].apply(self.clean_address_column)
        actual_data['city'] = actual_data['address'].apply(self.get_city)
        actual_data['suburb'] = actual_data['address'].apply(self.get_suburb)
        actual_data['days_active'] = (actual_data['last_review'] - actual_data['first_review'])/pd.Timedelta(days=365.25)
        actual_data = actual_data[actual_data['suburb'] != '']
        actual_data = actual_data[actual_data['city'] != '']
        def convert_price(x):

            try:

                return float(x.to_decimal()) if isinstance(x, Decimal128) else float(x)
            
            except (ValueError, TypeError):

                return None

        actual_data["price"] = actual_data["price"].apply(convert_price)

        def create_price_categories(value):

            if value < 100:

                return '< $100'
            
            elif value >= 100 and value <= 200:

                return '$100 - $200'
            
            else:

                return '> $200'

        actual_data['price_range'] = actual_data['price'].apply(create_price_categories)


        def review_score_categories(value):

            if value < 70:

                return '< 70'
            
            elif value >= 70 and value <= 80:

                return '>= 70 & <= 80'
            
            elif value >= 80 and value <= 90:

                return '>= 80 & <= 90'
            
            else:

                return '> 90'

        actual_data['review_score_category'] = actual_data['review_scores_rating'].apply(review_score_categories)

        actual_data.drop(columns=['summary', 'space', 'neighborhood_overview', 'notes', 'transit', 'access', 'interaction',
       'house_rules', 'availability', 'first_review', 'last_review', 'minimum_nights', 'maximum_nights', 'room_type', 'bed_type',
       'last_scraped', 'calendar_last_scraped', 'security_deposit', 'cleaning_fee', 'extra_people', 'guests_included', 'images', 
       'host', 'address', 'review_scores', 'reviews', 'weekly_price','monthly_price', 'reviews_per_month'], inplace=True)

        self._data = actual_data

        return self._data
        

    # Function to Get Review Scores based on cleanliness
    def get_review_scores_cleanliness(self, value):

        if 'review_scores_cleanliness' in value.keys():

            return value['review_scores_cleanliness']
        
        else:
            
            return 0
        

    # Function to Get Review Scores based on location
    def get_review_scores_location(self, value):

        if 'review_scores_location' in value.keys():

            return value['review_scores_location']
        
        else:
            
            return 0


    # Function to Get Review Scores based on rating      
    def get_review_scores_rating(self, value):

        if 'review_scores_rating' in value.keys():

            return value['review_scores_rating']
        
        else:
            
            return 0


    # Function to clean Address column
    def clean_address_column(self, value):

        if isinstance(value, str):

            value = value.replace("\\", "")

            try:

                return ast.literal_eval(value)
            
            except Exception as e:

                print(f"Could not convert: {value} due to the following Error : {e}")

                return None
            
        return value


    # Function to extract City details out of Address column
    def get_city(self, value):

        if 'market' in value.keys():

            return value['market']
        
        else:
            
            return 'Not Available'


    # Function to extract Suburb details out of Address column
    def get_suburb(self, value):

        if 'suburb' in value.keys():

            return value['suburb']
        
        else:
            
            return 'Not Available'
        
    
        
    
        
    
        


#dc = DataCleansing()
#output = dc.perform_data_engineering()
#output.to_excel('output.xlsx', index=False)
        
    
        
    
        
    



        
