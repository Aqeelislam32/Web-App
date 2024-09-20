import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from datetime import datetime
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import io
import random 
import string
 
# Define file paths for storing user data
USER_DATA_FILE = "user_data.pkl"
USER_DATA_FILE = 'user_data.csv'
PRODUCT_DATA_FILE = "product_data.csv"
EXPENSE_DATA_FILE = "expense_data.csv"
INVENTORY_DATA_FILE = "inventory_data.csv"
CUSTOMER_DATA_FILE = "customer_data.csv"

# Function to load data from a file
def load_data(file_path, default_data):
    if os.path.exists(file_path):
       with open(file_path, "rb") as file:
            return pickle.load(file)
    else:
        return default_data

# Function to save data to a file
def save_data(file_path, data):
    with open(file_path, "wb") as file:
        pickle.dump(data, file) 
# User Database
if 'user_data' not in st.session_state:
    st.session_state.user_data = pd.DataFrame(columns=['First Name', 'Last Name', 'Email', 'Phone Number', 'Password'])



 


# Initialize or load sample data
if 'product_data' not in st.session_state:
    st.session_state.product_data = pd.DataFrame({
        'Auction Branch': np.random.choice(['Branch A', 'Branch B', 'Branch C'], 100),
        'Product': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
        'Quantity': np.random.randint(1, 10, 100),
        'Purchase Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Price': np.random.uniform(1000, 10000, 100),  # Prices in PKR
        'Payment Method': np.random.choice(['Credit', 'Cash', 'Online'], 100)
    })
    st.session_state.product_data['Total'] = st.session_state.product_data['Quantity'] * st.session_state.product_data['Price']
    st.session_state.product_data = load_data(PRODUCT_DATA_FILE, st.session_state.product_data)

if 'expense_data' not in st.session_state:
    st.session_state.expense_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Category': np.random.choice(['Rent', 'Electricity Bill', 'Water Bill', 'Gas Bill', 'Inventory', 'Misc'], 100),
        'Amount': np.random.uniform(500, 5000, 100)  # Amounts in PKR
    }) 
    st.session_state.expense_data = load_data(EXPENSE_DATA_FILE,st.session_state.expense_data)
#
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C'],
        'Stock': [100, 150, 80],
        'Restock Date': pd.to_datetime(['2024-02-01', '2024-02-15', '2024-03-01'])
    })
    st.session_state.inventory_data = load_data(INVENTORY_DATA_FILE,st.session_state.inventory_data)

if 'customer_data' not in st.session_state:
    st.session_state.customer_data = pd.DataFrame({
        'Customer Name': np.random.choice(['Customer A', 'Customer B', 'Customer C'], 100),
        'Contact Number': np.random.choice(['03001234567', '03101234567', '03201234567'], 100),
        'Sale Product Name': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
        'Quantity': np.random.randint(1, 10, 100),
        'Shop Name': np.random.choice(['Shop A', 'Shop B', 'Shop C'], 100),
        'Purchase Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Payment Method': np.random.choice(['Credit', 'Cash', 'Online'], 100)
    })
    st.session_state.customer_data = load_data(CUSTOMER_DATA_FILE, st.session_state.customer_data)

# Function to save all session data
def save_all_data():
    save_data(PRODUCT_DATA_FILE, st.session_state.product_data)
    save_data(EXPENSE_DATA_FILE, st.session_state.expense_data)
    save_data(INVENTORY_DATA_FILE, st.session_state.inventory_data)
    save_data(CUSTOMER_DATA_FILE, st.session_state.customer_data)

# Sign-up form
def sign_up():
    st.title("Welcome To Auction Web App")
    st.header("Sign Up")
    with st.form("signup_form"):
        email = st.text_input("Email")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")

        col1, col2 = st.columns([1, 1])
        with col1:
            sign_up_button = st.form_submit_button("Sign Up")
        with col2:
            login_button = st.form_submit_button("Login")

        if sign_up_button:
            if not email or not first_name or not last_name or not phone or not password or not password_confirm:
                st.error("Please enter the form.")
            elif password != password_confirm:
                st.error("Passwords do not match!")
            else:
                user_data = {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "password": password
                }
                save_data(USER_DATA_FILE, user_data)
                st.success("Sign-up successful! Please log in.")
                st.session_state.signed_up = True
        
        if login_button:
            st.session_state.signed_up = True

# Login form
def login():
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            user_data = load_data(USER_DATA_FILE, None)
            if user_data and user_data["email"] == email and user_data["password"] == password:
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Invalid email or password.")
                if st.button("Forgot Password?"):
                    st.session_state.show_forgot_password = True

# Main App Logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "signed_up" not in st.session_state:
    st.session_state.signed_up = False


if not st.session_state.signed_up:
    sign_up()
elif not st.session_state.logged_in:
    login()
#elif st.session_state.forgot_password_requested:
    #forgot_password()
#elif not st.session_state.verified:
    #st.warning("Email address or phone number not verified.") 
else:

# Sidebar navigation
 st.sidebar.title("Navigation")
 section = st.sidebar.radio("Go to", ["Dashboard", "Product Management", "Expense Management", "Inventory Management", "Customer Management", "Reporting", "Budgeting & Forecasting"])

 

# Dashboard Overview
 if section == "Dashboard":
     st.title("Dashboard Overview")
    
    # User inputs total sales and total expenses
     st.subheader("Enter Total Sales and Expenses")
     total_sales = st.number_input("Enter Total Sales (PKR)", min_value=0.0, format="%.2f")
     total_expenses = st.number_input("Enter Total Expenses (PKR)", min_value=0.0, format="%.2f")
    
     if st.button("Calculate Profit/Loss"):
         profit_loss = total_sales - total_expenses
         st.metric("Profit/Loss", f"PKR {profit_loss:,.2f}", delta=profit_loss)
    
    # Cash Flow Summary (using dummy data for now)
     st.subheader("Cash Flow Summary")
     cash_flow_chart = alt.Chart(st.session_state.product_data).mark_line().encode(
         x='Purchase Date:T',
         y='Total:Q'
    ).properties(
        width=700,
        height=400
    )
     st.altair_chart(cash_flow_chart)

# Sales Management
 elif section == "Product Management":
    st.title("Product Management")
    
    # Add Sales
    st.subheader("Add Product")
    with st.form("Add  Product"):
        auction_branch = st.text_input("Auction Branch")  # User can enter the auction branch
        product_name = st.text_input("Product Name")  # User can enter the product name
        quantity = st.number_input("Quantity", min_value=1)
        purchase_date = st.date_input("Purchase Date")
        price = st.number_input("Price (PKR)", min_value=0.0, format="%.2f")
        payment_method = st.selectbox("Payment Method", ['Credit', 'Cash', 'Online'])
        if st.form_submit_button("Add Sale"):
            # Add the new sale to the sales_data DataFrame
            new_sale = pd.DataFrame({
                'Auction Branch': [auction_branch],
                'Product': [product_name],
                'Quantity': [quantity],
                'Purchase Date': [pd.to_datetime(purchase_date)],
                'Price': [price],
                'Payment Method': [payment_method],
                'Total': [quantity * price]
            })
            st.session_state.product_data = pd.concat([st.session_state.product_data, new_sale], ignore_index=True)
            st.success("Product Added")
    
    # View Sales History
    st.subheader("View Product History")
    st.dataframe(st.session_state.product_data)

    #Save Product Data
    if st.button("Save Product Data"):
        save_data(PRODUCT_DATA_FILE, st.session_state.product_data)
        st.success("Product Data Saved")


    
    # Clear Sales History
    if st.button("Clear Product History"):
        st.session_state.product_data = pd.DataFrame(columns=['Auction Branch', 'Product', 'Quantity', 'Purchase Date', 'Price', 'Payment Method', 'Total'])
        st.success("Sales History Cleared")
     

     # Product Analysis
    st.subheader("Product Analysis")
    product_analysis_chart = px.histogram(st.session_state.product_data, x='Product', y='Total', color='Payment Method', barmode='group')
    st.plotly_chart(product_analysis_chart) 

# Expense Management
 elif section == "Expense Management":
    st.title("Expense Management")
    
    # Add Expenses
    st.subheader("Add Expenses")
    with st.form("Add Expenses"):
        category = st.selectbox("Category", ['Rent', 'Electricity Bill', 'Water Bill', 'Gas Bill', 'Inventory اسٹاک یا مال', 'Misc مختلف چھوٹے اخراجات'])
        amount = st.number_input("Amount (PKR)", min_value=0.0, format="%.2f")
        date = st.date_input("Date")
        if st.form_submit_button("Add Expense"):
            # Add the new expense to the expense_data DataFrame
            new_expense = pd.DataFrame({
                'Date': [pd.to_datetime(date)],
                'Category': [category],
                'Amount': [amount]
            })
            st.session_state.expense_data = pd.concat([st.session_state.expense_data, new_expense], ignore_index=True)
            st.success("Expense Added")
    
    # View Expense History
    st.subheader("View Expense History")
    st.dataframe(st.session_state.expense_data)

    if st.button("Save Expense Data"):
        save_data( EXPENSE_DATA_FILE , st.session_state.expense_data)
        st.success("Expense Data Saved")
    
    # Clear Expense History
    if st.button("Clear Expense History"):
        st.session_state.expense_data = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
        st.success("Expense History Cleared")
    
    # Calculate and Display Totals for Each Category
    st.subheader("Category Totals")
    if st.button("Calculate Totals"):
        category_totals = st.session_state.expense_data.groupby('Category')['Amount'].sum().reset_index()
        st.write(category_totals)
    
    # Expense Analysis
    st.subheader("Expense Analysis")
    expense_analysis_chart = px.pie(st.session_state.expense_data, names='Category', values='Amount')
    st.plotly_chart(expense_analysis_chart)

# Inventory Management
 elif section == "Inventory Management":
    st.title("Inventory Management")
    
    # Add Inventory
    st.subheader("Add Inventory")
    with st.form("Add Inventory"):
        product_name = st.text_input("Product Name")  # User can enter the product name
        stock = st.number_input("Stock", min_value=0)
        restock_date = st.date_input("Restock Date")
        if st.form_submit_button("Add Inventory"):
            # Add the new inventory to the inventory_data DataFrame
            new_inventory = pd.DataFrame({
                'Product': [product_name],
                'Stock': [stock],
                'Restock Date': [pd.to_datetime(restock_date)]
            })
            st.session_state.inventory_data = pd.concat([st.session_state.inventory_data, new_inventory], ignore_index=True)
            st.success("Inventory Added")
    
    # View Inventory
    st.subheader("View Inventory")
    st.dataframe(st.session_state.inventory_data)

    if st.button("Save Inventory Data"):
        save_data(INVENTORY_DATA_FILE , st.session_state.inventory_data)
        st.success("Inventory Data Saved")
    
    # Clear Inventory
    if st.button("Clear Inventory"):
        st.session_state.inventory_data = pd.DataFrame(columns=['Product', 'Stock', 'Restock Date'])
        st.success("Inventory Cleared")
    
    # Low Stock Alerts
    st.subheader("Low Stock Alerts")
    low_stock = st.session_state.inventory_data[st.session_state.inventory_data['Stock'] < 100]
    st.dataframe(low_stock)
    
    # Inventory Valuation
    st.subheader("Inventory Valuation")
    total_value = st.session_state.inventory_data['Stock'].sum()
    st.metric("Total Inventory Value", f"PKR {total_value:,.2f}")

 
# Customer Management
 elif section == "Customer Management":
    st.title("Customer Management")
    
    # Add Sales
    st.subheader("Add History")
    with st.form("Add History"):
        Customer_name = st.text_input("Customer Name")  # User can enter the customer name
        Contact_info = st.text_input('Contact Number')
        Shop_name = st.text_input('Shop Name')
        product_name = st.text_input("Product Name")  # User can enter the product name
        quantity = st.number_input("Quantity", min_value=1)
        purchase_date = st.date_input("Sale Date")
        price = st.number_input("Price (PKR)", min_value=0.0, format="%.2f")
        payment_method = st.selectbox("Payment Method", ['Credit', 'Cash', 'Online'])
        if st.form_submit_button("Add Sale"):
            # Add the new sale to the customer_data DataFrame
            new_sale = pd.DataFrame({
                'Customer Name': [Customer_name],
                'Contact Number': [Contact_info],
                'Shop Name': [Shop_name],
                'Product Name': [product_name],
                'Quantity': [quantity],
                'Purchase Date': [pd.to_datetime(purchase_date)],
                'Price (PKR)': [price],
                'Payment Method': [payment_method],
                'Total': [quantity * price]
            })
            st.session_state.customer_data = pd.concat([st.session_state.customer_data, new_sale], ignore_index=True)
            st.success("Sale Added")
    
    # Display Customer Data History
    st.subheader("Customer Data History")
    if not st.session_state.customer_data.empty:
        st.dataframe(st.session_state.customer_data)
    else:
        st.info("No customer data available yet.")

    if st.button("Save Customer Data"):
        save_data(CUSTOMER_DATA_FILE, st.session_state.customer_data)
        st.success("Customer Data Saved")



    # Clear Customer History
    if st.button("Clear Customer History"):
        st.session_state.customer_data = pd.DataFrame(columns=[
            'Customer Name', 'Contact Number', 'Shop Name', 'Product Name', 'Quantity', 'Purchase Date', 'Price (PKR)', 'Payment Method', 'Total'
        ])
             
     # Retrieve Customer History
    st.subheader("Retrieve Customer History")
    customer_search = st.text_input("Enter Customer Name to Search")
    if st.button("Search"):
        customer_history = st.session_state.customer_data[st.session_state.customer_data['Customer Name'].str.contains(customer_search, case=False)]
        if not customer_history.empty:
            st.dataframe(customer_history)
        else:
            st.info("No records found for the entered customer name.")    
    
  # Reporting
 elif section == "Reporting":
    st.title("Reporting")
    
    # Generate financial reports
    st.subheader("Generate Financial Report")
    if st.button("Generate Report"):
        total_sales = st.session_state.customer_data['Total'].sum()
        total_expenses = st.session_state.expense_data['Amount'].sum()
        profit = max(total_sales - total_expenses, 0)
        loss = max(total_expenses - total_sales, 0)
        
        st.write(f"**Total Sales:** PKR {total_sales:,.2f}")
        st.write(f"**Total Expenses:** PKR {total_expenses:,.2f}")
        st.write(f"**Total Profit:** PKR {profit:,.2f}")
        st.write(f"**Total Loss:** PKR {loss:,.2f}")
        
        # Plot Pie Chart
        fig, ax = plt.subplots()
        labels = ['Total Sales', 'Total Expenses', 'Total Profit', 'Total Loss']
        sizes = [total_sales, total_expenses, profit, loss]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        st.subheader("Pie Chart")
        st.pyplot(fig)

        # Plot Bar Plot
        fig, ax = plt.subplots()
        categories = ['Total Sales', 'Total Expenses', 'Total Profit', 'Total Loss']
        values = [total_sales, total_expenses, profit, loss]
        sns.barplot(x=categories, y=values, ax=ax, palette='viridis')
        ax.set_ylabel('Amount (PKR)')
        ax.set_title('Financial Breakdown')
        
        st.subheader("Bar Plot")
        st.pyplot(fig)
        
        # Prepare data for download
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        
        st.subheader("Download Charts")
        st.download_button(
            label="Download Pie and Bar Charts",
            data=buf,
            file_name="financial_charts.png",
            mime="image/png"
        )

        # Generate CSV report
        st.subheader("Download Report")
        report_data = {
            'Total Sales': total_sales,
            'Total Expenses': total_expenses,
            'Total Profit': profit,
            'Total Loss': loss
        }
        report_df = pd.DataFrame([report_data])
        st.download_button(
            label="Download Report as CSV",
            data=report_df.to_csv(index=False),
            file_name='financial_report.csv',
            mime='text/csv'
        ) 
 # Budgeting & Forecasting
 

 elif section == "Budgeting & Forecasting":
     st.title("Budgeting & Forecasting")
    
    # Set Budget Automatically
     st.subheader("Set Budget Automatically")
     if st.button("Calculate Budget"):
        # Check if necessary data is available
        if 'customer_data' in st.session_state and 'expense_data' in st.session_state:
            # Calculate total sales and expenses
            total_sales = st.session_state.customer_data['Total'].sum()
            total_expenses = st.session_state.expense_data['Amount'].sum()
            
            # Set budget based on total sales
            yearly_budget = total_sales * 0.2  # Assuming budget is 20% of total sales
            monthly_budget = yearly_budget / 12    # Monthly budget is yearly budget divided by 12
            
            st.session_state.budget = {'Monthly': monthly_budget, 'Yearly': yearly_budget}
            st.success(f"Calculated Monthly Budget: PKR {monthly_budget:,.2f}")
            st.success(f"Calculated Yearly Budget: PKR {yearly_budget:,.2f}")
            
            # Plot Pie Chart
            fig, ax = plt.subplots()
            labels = ['Total Sales', 'Total Expenses', 'Yearly Budget']
            sizes = [total_sales, total_expenses, yearly_budget]
            colors = ['#ff9999','#66b3ff','#99ff99']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            
            st.subheader("Pie Chart")
            st.pyplot(fig)

            # Plot Bar Plot
            fig, ax = plt.subplots()
            categories = ['Total Sales', 'Total Expenses', 'Yearly Budget']
            values = [total_sales, total_expenses, yearly_budget]
            sns.barplot(x=categories, y=values, ax=ax, palette='viridis')
            ax.set_ylabel('Amount (PKR)')
            ax.set_title('Budget and Expense Breakdown')
            
            st.subheader("Bar Plot")
            st.pyplot(fig)
            
            # Prepare data for download
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            st.subheader("Download Charts")
            st.download_button(
                label="Download Pie and Bar Charts",
                data=buf,
                file_name="charts.png",
                mime="image/png"
            )
        else:
            st.error("Required data is missing.")
    
    # Forecasting Section
     st.subheader("Forecasting")
     if st.button("Generate Forecast"):
        if 'customer_data' in st.session_state:
            total_sales = st.session_state.customer_data['Total'].sum()
            future_sales_prediction = total_sales * 1.1  # Assuming a 10% increase
            
            st.write(f"**Total Sales:** PKR {total_sales:,.2f}")
            st.write(f"**Future Sales Prediction:** PKR {future_sales_prediction:,.2f}")
        
        # Calculate and display budget differences
        if 'budget' in st.session_state:
            monthly_budget = st.session_state.budget.get('Monthly', 0)
            yearly_budget = st.session_state.budget.get('Yearly', 0)
            monthly_expenses = st.session_state.expense_data['Amount'].sum() / 12
            yearly_expenses = st.session_state.expense_data['Amount'].sum()

            budget_difference_monthly = monthly_budget - monthly_expenses
            budget_difference_yearly = yearly_budget - yearly_expenses

            st.write(f"**Monthly Budget Difference:** PKR {budget_difference_monthly:,.2f}")
            st.write(f"**Yearly Budget Difference:** PKR {budget_difference_yearly:,.2f}")
