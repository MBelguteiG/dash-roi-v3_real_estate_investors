import streamlit as st 

st.title("Dash_ROI_Pro_V3")

# A widget - this value survives reruns automatically
price = st.number_input("Purchase Price", value=300000, step = 1000)

# Plain Python - recomputed from scratch every rerun 
down_payment = price * 0.20

st.write("Downpayment payment (20%)", down_payment)
st.write("This whole script just re-run top to bottom")