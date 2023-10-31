from faker import Faker 
import pandas as pd
import random
from datetime import datetime, timedelta

# Task is to create a dataset having features are {CustomerID, VisitDate,TotalSpend,ProductCategory}

def customer_ids(number_of_points =1000):
    ''' 
    This function returns 1000 records of customers where each customer can do multiple transactions.
    '''
    random.seed(0)
    # Defining the range of 4-digit integers (from 1000 to 9999)
    low = 1000
    high = 9999

    # Create a list of integers (customer IDs) with different frequencies
    integer_counts = [random.randint(1, 10) for _ in range(number_of_points)]

    # Flatten the list to generate the integers
    customer_ids = [i for i, count in enumerate(integer_counts, start=low) for _ in range(count)]

    # Shuffle the list to randomize the order
    random.shuffle(customer_ids)

    # Print the generated customer IDs
    return customer_ids[:1000]


def customer_visit_date():
    '''
    This will generate a random date between last 100 days
    ''' 
    fake = Faker()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    return fake.date_between(start_date=start_date, end_date=end_date)

def generate_customer_data(customer_id):
    fake = Faker()
    visit_date = customer_visit_date()
    total_spend = round(random.uniform(10, 2000), 2)  # Random total spend between $10 and $2000
    product_category = fake.random_element(elements=('Electronics', 'Clothing', 'Home', 'Books', 'Toys', 'Sports', 'Furniture', 'Jewelry','Healthcare','Beauty'))
    
    return [customer_id, visit_date, total_spend, product_category]

def main():
    '''
    This function will create the dummy dataset 
    '''
    
    # Lets fix the output file
    random.seed(0)

    fake = Faker()
    # storing all the features name in list
    
    features = ['CustomerID', 'VisitDate','TotalSpend','ProductCategory']



    # generating 1000 records for customer id
    customer_id = customer_ids()

    # create all features for the customer
    data_points = []
    for ele in customer_id:
        data_points.append(generate_customer_data(ele))
    
    df = pd.DataFrame(data_points, columns= features)

    df.to_csv('Customer_segmentation_dummy1.csv')

if __name__ == '__main__':
    main()


