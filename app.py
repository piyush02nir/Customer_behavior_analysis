import streamlit as st
import pandas as pd

# Create containers
header = st.container()
datasets = st.container()
kpis = st.container()

# Define functions for displaying KPIs and suggestions
def display_average_spending(selected_dataset):
    '''
    This function will display the average spending per customer for each transaction.
    '''
    st.subheader("Average Customer Spending")
    avg_spending = selected_dataset["TotalSpend"].mean()
    st.write(f'The average spending per customer is: {avg_spending:.2f}')

def display_top_customers(selected_dataset):
    '''
    This function will Plot the bar graph of the top 10 customers with maximum average spending.
    '''
    st.subheader("Average Spending of Top 10 Customers")
    customer_spent = selected_dataset.groupby('CustomerID')['TotalSpend'].mean().reset_index()
    top_10_customers = customer_spent.sort_values('TotalSpend', ascending=False)[:10]
    st.write(top_10_customers)
    st.bar_chart(top_10_customers, x = 'CustomerID', y = 'TotalSpend')

def display_customer_recall(selected_dataset):
    '''
    This function will plot bar graph of top 10 most frequent customers.
    '''
    st.subheader("Top 10 Most Frequent Customers")
    customer_recall = selected_dataset.groupby('CustomerID').agg(frequency=('CustomerID', 'count'), total_amount=('TotalSpend', 'sum')).reset_index()
    top_10_recall = customer_recall.sort_values('frequency', ascending=False)[:10]
    st.write(top_10_recall)
    st.bar_chart(top_10_recall, x = 'CustomerID', y = 'frequency')

def display_customer_spending(selected_dataset):
    '''
    This function will Plot the bar graph of the top 10 customers with maximum total spending.
    '''
    st.subheader("Top 10 Customers Based on Total Amount Spent")
    customer_total_spent = selected_dataset.groupby('CustomerID').agg(total_amount=('TotalSpend', 'sum')).reset_index()
    top_10_total_spent = customer_total_spent.sort_values('total_amount', ascending=False)[:10]
    st.write(top_10_total_spent)
    st.bar_chart(top_10_total_spent, x = 'CustomerID', y = 'total_amount')

def display_product_category(selected_dataset):
    '''
    This funtion will return the total sales and total price spent on each product category
    '''
    st.subheader("Product Category")
    category_stats = selected_dataset.groupby('ProductCategory').agg(product_sales=('CustomerID', 'count'), Total_Price=('TotalSpend', 'sum')).reset_index()
    most_popular = category_stats['ProductCategory'][category_stats['product_sales'] == category_stats['product_sales'].max()].values[0]
    st.write(f'Most Popular Product Category is {most_popular}, with total number of sales: {category_stats["product_sales"].max()}')
    st.write("Total price spent, product sales categorywise")
    

    # category wise revenue
    st.write("Product Category  vs Total Revenue")
    category_revenue = category_stats.sort_values('Total_Price', ascending = False).reset_index()
    top_10_category_revenue = category_revenue.iloc[:10]
    st.bar_chart(data= top_10_category_revenue, x = 'ProductCategory', y='Total_Price', color="#ffaa00")

    # Categorywise sales
    st.write("Product Category  vs Total Sales")
    category_sales = category_stats.sort_values('product_sales', ascending = False).reset_index()
    top_10_category_sales = category_sales.iloc[:10]
    st.bar_chart(data= top_10_category_sales, x = 'ProductCategory', y='Total_Price', color="#ffaa00")
   
    return category_stats


def display_monthly_revenue_growth(selected_dataset):

    #This will plot the line chart for monthly revenue growth.
   
    st.subheader("Monthly Revenue Growth")
    selected_dataset['VisitDate'] = pd.to_datetime(selected_dataset['VisitDate'])
    monthly_revenue = selected_dataset.groupby(selected_dataset['VisitDate'].dt.strftime('%Y-%m'))['TotalSpend'].sum().reset_index()
    # Calculate the monthly growth percentage
    monthly_revenue['MonthlyGrowth'] = monthly_revenue['TotalSpend'].pct_change() * 100
    max_month = monthly_revenue[monthly_revenue['TotalSpend'] == monthly_revenue['TotalSpend'].max()]['VisitDate'].values[0]
    min_month = monthly_revenue[monthly_revenue['TotalSpend'] == monthly_revenue['TotalSpend'].min()]['VisitDate'].values[0]
    # Calculate the average monthly revenue
    average_monthly_revenue = monthly_revenue['TotalSpend'].mean()
    # Create a line chart to visualize monthly revenue growth and highlight max and min months
    st.line_chart(monthly_revenue, x='VisitDate', y='TotalSpend', use_container_width=True)
    #st.line_chart(monthly_revenue, x='VisitDate', y='MonthlyGrowth', use_container_width=True)
    st.write(f"Maximum Revenue Month: {max_month}")
    st.write(f"Minimum Revenue Month: {min_month}")
    st.write(f"Average Monthly Revenue: {average_monthly_revenue:.2f}")
   


def display_optimization_suggestions(categorical_stats,selected_dataset):
    '''
    This function will give the optimization suggestions based on the product and customer category
    '''
    st.subheader("Optimization Suggestions")
    most_recommend = categorical_stats.sort_values('product_sales', ascending=False)
    st.write("   Most recommended products are:")
    st.write(most_recommend['ProductCategory'].iloc[:3])
    percentile_75 = selected_dataset['TotalSpend'].quantile(0.75)
    median = selected_dataset['TotalSpend'].quantile(0.5)
    percentile_25 = selected_dataset['TotalSpend'].quantile(0.25)

    st.write("Customer category based on spending amounts")
    text = f"""
    A: if spend > {percentile_75}\n
    B: if spend between {percentile_75} and {median}\n 
    C: if spend between {percentile_25} and {median}\n 
    D: if spend less than{percentile_25}
    """
    st.write(text)
    customer_category = st.radio('Choose the customer category:',["A","B","C","D"])
    if (customer_category == "A") or (customer_category == "B"):
        st.write("Please avail the discount for 10% on following categories:")
        st.write(most_recommend['ProductCategory'].iloc[-3:])      

    elif customer_category == "C":
        st.write("Please avail 20% discount on following categories:")
        st.write(most_recommend['ProductCategory'].iloc[:3])

        st.write("Please avail the discount for 10% on following categories:")
        st.write(most_recommend['ProductCategory'].iloc[-3:]) 

    elif customer_category == "D":
        st.write("Please avail 30% discount on following categories:")
        st.write(most_recommend['ProductCategory'].iloc[:3])

        st.write("Please avail the discount for 20% on following categories:")
        st.write(most_recommend['ProductCategory'].iloc[-3:])  


# Streamlit app sections
with header:
    st.title("Customer Behavior Analysis")

with datasets:
    st.subheader("Select a Dataset")
    choice = st.radio("Choose a dataset option:", ["Upload Custom Dataset", "Use Default Dataset"])
    if choice == "Use Default Dataset":
        selected_dataset = pd.read_csv('Customer_segmentation_dummy1.csv').iloc[:, 1:]
    elif choice == "Upload Custom Dataset":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            selected_dataset = pd.read_csv(uploaded_file)
    st.write(selected_dataset.head())

with kpis:
    display_average_spending(selected_dataset)
    display_top_customers(selected_dataset)
    display_customer_recall(selected_dataset)
    display_customer_spending(selected_dataset)
    most_recommended = display_product_category(selected_dataset)
    display_monthly_revenue_growth(selected_dataset)
    display_optimization_suggestions(most_recommended,selected_dataset)