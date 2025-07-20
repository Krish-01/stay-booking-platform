# Importing Libraries

from data_cleansing import DataCleansing
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import time
import warnings
warnings.filterwarnings("ignore")


class DataAnalysis:


    def __init__(self, data=None):

        self._data = data



    # Fetch Data Frame for Analysis
    def fetch_final_data(self):


        dc = DataCleansing()
        self._data = dc.perform_data_engineering()

        return self._data
    

    # Print Suburb Selected
    def print_suburb_selected(self, top_12, city_selected):

        print()
        print(f"📍      Featured Suburbs in {city_selected}:      📍".center(90))
        print()

        print("-" * 90)

        j = 1

        for i in range(0, len(top_12), 2):
            row = top_12[i:i+2]
            line = []
            for suburb in row:
                line.append(f"{j}. {suburb}".center(45))
                j += 1
            print(" | ".join(line))
            print("-" * 90)

        print()

        choice = None
        valid_input = False

        print("=" * 90)
        while not valid_input:
            user_input = input("                       Enter the number of your suburb (1 to 12) :")
            print("=" * 90)
            if user_input.isdigit():
                choice = int(user_input)
                if 1 <= choice <= len(top_12):
                    valid_input = True
                else:
                    print("❌ Invalid choice. Please select a number from the list.".center(90))
                    print("=" * 90)
            else:
                print("❌ Please enter a valid number (1 to 12).".center(90))
                print("=" * 90)

        
        print(f"✅ You selected: {top_12[choice - 1]}".center(90))
        print("=" * 90)

        return top_12[choice - 1]
    





    # Print Suburb Details
    def print_property_details(self, filtered_data, property_list, city_selected, pdf, page_num):

 
        # Size of the Chart
        fig = plt.figure(figsize=(20, 8))

        # Plotting the Count Plot
        #ax = sns.countplot(x=filtered_data[filtered_data["suburb"] == selected_suburb]['property_type'])
        ax = sns.countplot(x=filtered_data[(filtered_data["city"] == city_selected) & (filtered_data["property_type"].isin(property_list))]['property_type'], 
                            order = filtered_data[(filtered_data["city"] == city_selected) & (filtered_data["property_type"].isin(property_list))]['property_type'].value_counts().index,
                            linewidth = 0.5)

        # Displaying values corresponding to each bar
        ax.bar_label(ax.containers[0])

        # Setting Title Name
        #ax.set_title(f'Type of Properties in {selected_suburb}, {city_selected}', fontsize =10, fontweight ='bold')
        ax.set_title(f'Page {page_num}: Type of Properties in {city_selected}', fontsize=16, fontweight='bold')           

        # Save Chart
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)


    # Print Price Details
    def print_price_details(self, filtered_data, selected_property, city_selected, pdf, page_num):

 
        # Size of the Chart
        fig = plt.figure(figsize=(10,6))

        # Plotting the Count Plot
        #ax = sns.countplot(x=filtered_data[filtered_data["suburb"] == selected_suburb]['property_type'])
        ax = sns.countplot(x=filtered_data['price_range'], order=filtered_data['price_range'].value_counts().index, linewidth=0.5)

        # Displaying values corresponding to each bar
        ax.bar_label(ax.containers[0])

        # Setting Title Name
        #ax.set_title(f'Type of Properties in {selected_suburb}, {city_selected}', fontsize =10, fontweight ='bold')
        ax.set_title(f'Page {page_num}: Price Range of {selected_property} in {city_selected}', fontsize=16, fontweight='bold')           

        # Save Chart
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)



    # Print Rating Details
    def print_rating_details(self, filtered_data, selected_price, selected_property, city_selected, pdf, page_num):

 
        # Size of the Chart
        fig = plt.figure(figsize=(10,6))

        # Plotting the Count Plot
        #ax = sns.countplot(x=filtered_data[filtered_data["suburb"] == selected_suburb]['property_type'])
        ax = sns.countplot(x=filtered_data['review_score_category'], order=filtered_data['review_score_category'].value_counts().index, linewidth=0.5)

        # Displaying values corresponding to each bar
        ax.bar_label(ax.containers[0])

        # Setting Title Name
        #ax.set_title(f'Type of Properties in {selected_suburb}, {city_selected}', fontsize =10, fontweight ='bold')
        ax.set_title(f'Page {page_num}: Ratings of {selected_property} in {city_selected} for Price: {selected_price}', fontsize=16, fontweight='bold')            

        # Save Chart
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)


    def add_dataframe_to_pdf(self, filtered_data, rating_selected, price_selected, property_selected, city_selected, pdf, page_num=4, rows_per_page=8):
        import matplotlib.pyplot as plt

        total_rows = len(filtered_data)
        num_pages = (total_rows + rows_per_page - 1) // rows_per_page

        for i in range(num_pages):
            start = i * rows_per_page
            end = min(start + rows_per_page, total_rows)
            df_chunk = filtered_data.iloc[start:end]

            
            fig = plt.figure(figsize=(12, 2 + 0.5 * len(df_chunk)))
            ax = fig.add_subplot(111)
            ax.axis('off')

            # Title
            ax.set_title(
                f'Page {page_num + i}: {property_selected} in {city_selected} | Price: {price_selected} | Rating: {rating_selected}',
                fontsize=14, fontweight='bold', loc='center', pad=20
            )

            # Table
            table = ax.table(
                cellText=df_chunk.values,
                colLabels=df_chunk.columns,
                cellLoc='center',
                loc='center',
                colColours=['#f2f2f2'] * len(df_chunk.columns)
            )
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.1, 1.4)

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)


    def add_report_cover(self, pdf, report_title="OffBeat Destination Analysis Report"):

        fig = plt.figure(figsize=(11, 8))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Report Title
        plt.text(0.5, 0.75, report_title, fontsize=24, fontweight='bold', ha='center')

        # Subtitle
        plt.text(0.5, 0.6, "Prepared for: OffBeat Destinations", fontsize=16, ha='center')
        plt.text(0.5, 0.55, f"Date: {datetime.today().strftime('%B %d, %Y')}", fontsize=12, ha='center')



        pdf.savefig(fig)
        plt.close(fig)



    # Print Property Selected
    def print_property_selected(self, all_property_type, city_selected, filtered_data):

        print()
        #print(f"📍  Featured Properties in {suburb_selected}, {city_selected}: 📍".center(90))
        print(f"📍  Featured Property Type and Listed options in {city_selected}: 📍".center(90))
        print()
        print("-" * 90)

        j = 97  # ASCII value for 'a'
        list_index = []

        # Display property types in rows of 2 with lettered options
        for i in range(0, len(all_property_type), 2):
            row = all_property_type[i:i+2]
            line = []
            for property in row:
                letter = chr(j)
                line.append(f"{letter}. {property} ({len(filtered_data[filtered_data['property_type'] == property])} options)".center(45))
                list_index.append(letter)
                j += 1
            print(" | ".join(line))
            print("-" * 90)

        print()

        # Ask user to select a property type using a alphabet (a to p etc.)
        choice = None
        valid_input = False

        print("=" * 90)
        while not valid_input:
            user_input = input(f"                   Enter the alphabet of your Property Type (a to {list_index[-1]}) : ").lower()
            print("=" * 90)
            if user_input in list_index:
                choice = list_index.index(user_input)
                valid_input = True
            else:
                print(f"❌ Invalid input. Please select a alphabet from the list (a to {list_index[-1]}).".center(90))
                print("=" * 90)

        # Once input is valid
        print(f"✅ You selected: {all_property_type[choice]}".center(90))
        print("=" * 90)

        return all_property_type[choice]
    


    # Print Price Selected
    def print_price_selected(self, price_list, property_selected, city_selected, filtered_data):

        print()
        #print(f"📍  Featured Properties in {suburb_selected}, {city_selected}: 📍".center(90))
        print(f"📍  Price Range Options for {property_selected} in {city_selected}: 📍".center(90))
        print()
        print("-" * 90)

        j = 97  # ASCII value for 'a'
        list_index = []

        # Display Price Range in rows of 2 with lettered options
        for i in range(0, len(price_list), 3):
            row = price_list[i:i+3]
            line = []
            for price_type in row:
                letter = chr(j)
                line.append(f"{letter}. {price_type} ({len(filtered_data[filtered_data['price_range'] == price_type])})".center(30))
                list_index.append(letter)
                j += 1
            print(" | ".join(line))
            print("-" * 90)

        print()

        # Ask user to select a price range using a alphabet (a to c etc.)
        choice = None
        valid_input = False

        print("=" * 90)
        while not valid_input:
            user_input = input(f"                   Enter the alphabet of your Price Range (a to {list_index[-1]}) : ").lower()
            print("=" * 90)
            if user_input in list_index:
                choice = list_index.index(user_input)
                valid_input = True
            else:
                print(f"❌ Invalid input. Please select a alphabet from the list (a to {list_index[-1]}).".center(90))
                print("=" * 90)

        
        print(f"✅ You selected Price Range: {price_list[choice]}".center(90))
        print("=" * 90)

        return price_list[choice]
    


    # Print Rating Selected
    def print_rating_selected(self, rating_list, price_selected, property_selected, city_selected, filtered_data):

        print()
        #print(f"📍  Featured Properties in {suburb_selected}, {city_selected}: 📍".center(90))
        print(f"📍  Ratings for {property_selected} in {city_selected} for Price Range - {price_selected}: 📍".center(90))
        print()
        print("-" * 90)

        j = 97  # ASCII value for 'a'
        list_index = []

        # Display Rating Range in rows of 2 with lettered options
        for i in range(0, len(rating_list), 2):
            row = rating_list[i:i+2]
            line = []
            for rating_type in row:
                letter = chr(j)
                line.append(f"{letter}. {rating_type} ({len(filtered_data[filtered_data['review_score_category'] == rating_type])})".center(45))
                list_index.append(letter)
                j += 1
            print(" | ".join(line))
            print("-" * 90)

        print()

        # Ask user to select a rating range using a alphabet (a to d etc.)
        choice = None
        valid_input = False

        print("=" * 90)
        while not valid_input:
            user_input = input(f"                   Enter the alphabet of your Rating Type (a to {list_index[-1]}) : ").lower()
            print("=" * 90)
            if user_input in list_index:
                choice = list_index.index(user_input)
                valid_input = True
            else:
                print(f"❌ Invalid input. Please select a alphabet from the list (a to {list_index[-1]}).".center(90))
                print("=" * 90)

        
        print(f"✅ You selected Rating Type: {rating_list[choice]}".center(90))
        print("=" * 90)

        return rating_list[choice]
    

    # Transpose DataFrame for User
    def transpose_data(self, filtered_data):

        

        parameter = []
        value = []

        for i in range(len(filtered_data)):

            parameter.append(f'Property' + str(i+1))
            value.append('-- Details --')

            for j in range(filtered_data.shape[1]):

                parameter.append(filtered_data.columns[j])
                value.append(filtered_data.iloc[i, j])

            parameter.append('*'*50)
            value.append('*'*50)


        result = pd.DataFrame({'Parameter': parameter, 'Value': value})

        return result
    


    def final_message(self):

        time.sleep(2)
        print("📊 Your Search History report has been emailed! 📊".center(90))
        print("=" * 90)
        time.sleep(2)
        print(" To confirm your bookings please visit us or contact - ".center(90))
        print("🌐  Visit: www.offbeatdestinations.com".center(90))
        print("📧  Contact: hello@offbeatdestinations.com".center(90))
        print("=" * 90)
        print("🫶  Thank you for choosing Offbeat Destination as your travel partner 🫶".center(90))
        print("=" * 90)




    def start_analysis(self):

        df = self.fetch_final_data()
        df.to_excel('data.xlsx')
        #df["price"] = df["price"].apply(lambda x: float(x) if isinstance(x, Decimal128) else x)

        # Updated list of cities
        cities = [
            "New York", "Montreal", "Barcelona", "Sydney", 
            "Hong Kong", "Rio De Janeiro", "Oahu", "Istanbul", 
            "Maui", "The Big Island", "Kauai", "The Long Island"
        ]

        print("-" * 90)

        j = 1

        for i in range(0, len(cities), 3):
            row = cities[i:i+3]
            line = []
            for city in row:
                line.append(f"{j}. {city}".center(30))
                j += 1
            print(" | ".join(line))
            print("-" * 90)

        print()

        choice = None
        valid_input = False

        print("=" * 90)
        while not valid_input:
            user_input = input("                    Enter the number of your destination (1 to 12) :")
            print("=" * 90)
            if user_input.isdigit():
                choice = int(user_input)
                if 1 <= choice <= len(cities):
                    valid_input = True
                else:
                    print("❌ Invalid choice. Please select a number from the list.".center(90))
                    print("=" * 90)
            else:
                print("❌ Please enter a valid number (1 to 12).".center(90))
                print("=" * 90)


        print(f"✅ You selected: {cities[choice - 1]}".center(90))
        print("=" * 90)

        df1 = df[df['city'] == cities[choice-1]]

        print(f'🏡 We have {len(df1)} listed options in {cities[choice - 1]}'.center(90))
        print("=" * 90)

        #top_12_suburb = df['suburb'].value_counts()[:12].index

        #suburb_selected = self.print_suburb_selected(top_12_suburb, cities[choice - 1])
        #self.print_property_details(suburb_selected, df, cities[choice - 1])
        
        #df = df[df['suburb'] == suburb_selected]

        top_property = df1['property_type'].value_counts().sort_values(ascending=False)[:12].index
        
        #property_type_selected = self.print_property_selected(top_property, suburb_selected, cities[choice - 1])
        property_type_selected = self.print_property_selected(top_property, cities[choice - 1], df1)
        #self.print_price_details(property_type_selected, df, suburb_selected, cities[choice - 1])
        df2 = df1[df1['property_type'] == property_type_selected]

        price_options = df2['price_range'].value_counts().index
        price_range_selected = self.print_price_selected(price_options, property_type_selected, cities[choice - 1], df2)


        df3 = df2[df2['price_range'] == price_range_selected]
        rating_options = df3['review_score_category'].value_counts().index

        rating_range_selected = self.print_rating_selected(rating_options, price_range_selected, property_type_selected, cities[choice - 1], df3)

        df4 = df3[df3['review_score_category'] == rating_range_selected]

        #df4.to_excel('final.xlsx')

        df4 = df4[['name','suburb','listing_url','price','accommodates','review_scores_rating']]

        final_df = self.transpose_data(df4)



        
        # Export Analysis Report
        with PdfPages("Analysis_Report.pdf") as pdf:

            self.add_report_cover(pdf)
            self.print_property_details(df1, top_property, cities[choice - 1], pdf, page_num=2)
            self.print_price_details(df2, property_type_selected, cities[choice - 1], pdf, page_num=3)
            self.print_rating_details(df3, price_range_selected, property_type_selected, cities[choice - 1], pdf, page_num=4)
            self.add_dataframe_to_pdf(final_df, rating_range_selected, price_range_selected, property_type_selected, cities[choice - 1], pdf, page_num=5)


            metadata = pdf.infodict()
            metadata['Title'] = 'OffBeat Destinations Report'
            metadata['Author'] = 'Sudip Roy'
            metadata['Subject'] = 'Customer Booking Report'


        self.final_message()
       
        
        





da = DataAnalysis()
da.start_analysis()