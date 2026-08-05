
import streamlit as st
import requests
import pandas as pd

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Create input fields for the user
st.header("Enter Product and Store Details")

# Collect data from stores
product_weight = st.number_input("Product Weight", min_value=0.0, step=0.1)
sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
allocated_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, step=0.01)
mrp = st.number_input("Product MRP", min_value=0.0, step=1.0)

store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Food Mart", "Departmental Store", "Supermarket Type1", "Supermarket Type2"])

product_id_char = st.selectbox("Product ID Prefix", ["FD", "DR", "NC"])
age = st.number_input("Store Age (Years)", min_value=0, step=1)
category = st.selectbox("Product Category", ["Perishables", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': sugar_content,
    'Product_Allocated_Area': allocated_area,
    'Product_MRP': mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': age,
    'Product_Type_Category': category
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict Sales", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient='records')[0]) # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Sales']
        st.success(f"Predicted Total Sales: ${prediction:,.2f}")
    else:
        st.error(f"Error: Backend returned status code {response.status_code}")
