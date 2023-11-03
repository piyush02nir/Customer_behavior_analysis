# Customer_behavior_analysis
In this Project, We created the webapp using streamlit which will deliver the KPI's, basic Dashboard and Marketing optimization strategy.
## Data description
CustomerID: Unique id for each customer.  
VisitDate: Dates on which customer made a purchase.  
TotalSpend: Total amount spend by the customer.  
ProductCategory: Product Category.  
We created a Dummy dataset of 1000 rows using Faker and used this data to create a dashboad.

## Observation
These are  the observation based on the default dataset which we have created using Faker, If users choose different datasets then results will vary.

* The average spending per customer is: 984.75.  
**Top 10 customer with the maximum spending**
![customer_avg_spending](https://github.com/piyush02nir/Customer_behavior_analysis/assets/107622595/7a161afa-46e5-4d1c-bfaf-bcc86ff93f62)
**Top 10 most frequent customer**
![frequent_customers](https://github.com/piyush02nir/Customer_behavior_analysis/assets/107622595/4005e24c-360c-4257-b4c2-873165f955fc)

**Product Category:** Most Popular Product Category is Sports, with total number of sales: 121

**Product Category vs total revenue**
![product_catagory](https://github.com/piyush02nir/Customer_behavior_analysis/assets/107622595/c0d6386f-f8bd-4c86-8612-eb36c04d94e7)

**Product Category vs total sales**
![product_vs_total_sales](https://github.com/piyush02nir/Customer_behavior_analysis/assets/107622595/99083b0d-bba0-4b31-bb34-d2835ca32e36)

**Monthly revenue growth**
* Maximum Revenue Month: 2023-03

* Minimum Revenue Month: 2023-11

* Average Monthly Revenue: 109317.42
![total_spending](https://github.com/piyush02nir/Customer_behavior_analysis/assets/107622595/7e336cb7-b58f-43f1-b4bd-0342d83409af)


## How to Use the app
* step 1 : To clone the repository 'git clone repository-https://github.com/piyush02nir/Customer_behavior_analysis'
* step 2 : create an environment (streamlit) and install all packages from requirement.txt
* step3 : Open terminal and write command 'streamlit run app.py'
* After step3 a streamlit dashboard will open where you have two options: 1. Upload Custom dataset or 2. Use Default Dataset.
* If you choose option 1, you will get the option to upload your dataset. (make sure your dataset have same feature name)
* If you choose 2 options, the dashboards with kpi's will be shown.
* And At the end, you have to choose at what spending category you belong to and based on that you will get suitable discounts.
