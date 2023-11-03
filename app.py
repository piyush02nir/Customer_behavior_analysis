import streamlit as st
import pandas as pd

# Create page sections
st.set_page_config(page_title="Customer Behavior Analysis", page_icon="📈", layout="wide")

# Create sections
st.title("Customer Behavior Analysis")

st.header("Select a Dataset")
choice = st.radio("Choose a dataset option:", ["Use Default Dataset", "Upload Custom Dataset"])
if choice == "Use Default Dataset":
    selected_dataset = pd.read_csv('Customer_segmentation_dummy1.csv').iloc[:, 1:]
else:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        selected_dataset = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file.")
        st.stop()

st.subheader("Preview of Selected Dataset")
st.write(selected_dataset.head())

# Define functions for displaying KPIs and suggestions
def display_kpis(selected_dataset):
    col1, col2, col3 = st.columns(3)
    
    # KPI 1: Average Spending
    avg_spending = selected_dataset["TotalSpend"].mean()
    with col1:
        st.metric(label="Average Spending", value=f"${avg_spending:.2f}")

    # KPI 2: Top 10 Customers by Average Spending
    customer_spent = selected_dataset.groupby('CustomerID')['TotalSpend'].mean().reset_index()
    top_10_customers = customer_spent.sort_values('TotalSpend', ascending=False)[:10]
    with col2:
        st.subheader("Top 10 Customers by Average Spending")
        st.bar_chart(top_10_customers, x='CustomerID', y='TotalSpend')

    # KPI 3: Top 10 Most Frequent Customers
    customer_recall = selected_dataset['CustomerID'].value_counts().reset_index()
    customer_recall.columns = ['CustomerID', 'Frequency']
    top_10_recall = customer_recall.sort_values('Frequency', ascending=False)[:10]
    with col3:
        st.subheader("Top 10 Most Frequent Customers")
        st.bar_chart(top_10_recall, x='CustomerID', y='Frequency')

display_kpis(selected_dataset)

# Product Category Analysis
st.header("Product Category Analysis")

def display_product_category(selected_dataset):
    category_stats = selected_dataset.groupby('ProductCategory').agg(
        ProductSales=('CustomerID', 'count'),
        TotalPrice=('TotalSpend', 'sum')
    ).reset_index()
    
    st.subheader("Most Popular Product Category")
    most_popular = category_stats[category_stats['ProductSales'] == category_stats['ProductSales'].max()]['ProductCategory'].values[0]
    st.write(f"Most Popular Product Category: {most_popular} (Total Sales: {category_stats['ProductSales'].max()})")

    # Categorywise revenue
    st.subheader("Product Category vs Total Revenue")
    category_revenue = category_stats.sort_values('TotalPrice', ascending=False).iloc[:10]
    st.bar_chart(data=category_revenue, x='ProductCategory', y='TotalPrice', color="#ffaa00")

    # Categorywise sales
    st.subheader("Product Category vs Total Sales")
    category_sales = category_stats.sort_values('ProductSales', ascending=False).iloc[:10]
    st.bar_chart(data=category_sales, x='ProductCategory', y='ProductSales', color="#ffaa00")

    return category_stats

most_recommended = display_product_category(selected_dataset)

# Monthly Revenue Growth
st.header("Monthly Revenue Growth")

def display_monthly_revenue_growth(selected_dataset):
    selected_dataset['VisitDate'] = pd.to_datetime(selected_dataset['VisitDate'])
    monthly_revenue = selected_dataset.groupby(selected_dataset['VisitDate'].dt.strftime('%Y-%m'))['TotalSpend'].sum().reset_index()
    monthly_revenue['MonthlyGrowth'] = monthly_revenue['TotalSpend'].pct_change() * 100

    st.subheader("Monthly Revenue Growth")
    st.line_chart(monthly_revenue, x='VisitDate', y='TotalSpend', use_container_width=True)

    max_month = monthly_revenue[monthly_revenue['TotalSpend'] == monthly_revenue['TotalSpend'].max()]['VisitDate'].values[0]
    min_month = monthly_revenue[monthly_revenue['TotalSpend'] == monthly_revenue['TotalSpend'].min()]['VisitDate'].values[0]
    average_monthly_revenue = monthly_revenue['TotalSpend'].mean()

    st.write(f"Maximum Revenue Month: {max_month}")
    st.write(f"Minimum Revenue Month: {min_month}")
    st.write(f"Average Monthly Revenue: ${average_monthly_revenue:.2f}")

display_monthly_revenue_growth(selected_dataset)

# Optimization Suggestions
st.header("Optimization Suggestions")

percentile_75 = selected_dataset['TotalSpend'].quantile(0.75)
percentile_25 = selected_dataset['TotalSpend'].quantile(0.25)

st.write("Customer Category Based on Spending Amounts:")
text = f"""
- A: Spend > ${percentile_75}
- B: Spend between ${percentile_75} and ${percentile_25}
- C: Spend < ${percentile_25}
"""
st.write(text)

customer_category = st.radio('Choose the customer category:', ["A", "B", "C"])
suggested_discounts = most_recommended.sort_values('ProductSales', ascending=False)['ProductCategory']

if customer_category == "A":
    st.write("Suggested Discounts: 10% on the following categories")
    st.write(suggested_discounts.iloc[-3:])
elif customer_category == "B":
    st.write("Suggested Discounts: 20% on the following categories")
    st.write(suggested_discounts.iloc[:3])
    st.write("Suggested Discounts: 10% on the following categories")
    st.write(suggested_discounts.iloc[-3:])
elif customer_category == "C":
    st.write("Suggested Discounts: 30% on the following categories")
    st.write(suggested_discounts.iloc[:3])
    st.write("Suggested Discounts: 20% on the following categories")
    st.write(suggested_discounts.iloc[-3:])
