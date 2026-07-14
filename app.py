import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Page Title
st.title("AI Customer 360° Assistant")

# Load CSV files
crm = pd.read_csv("crm.csv")
support = pd.read_csv("support.csv")
email = pd.read_csv("email.csv")
product = pd.read_csv("product.csv")
slack = pd.read_csv("slack.csv")

# Customer Selection
customer = st.selectbox(
    "Select a Customer",
    crm["Customer"]
)

# Get customer data
crm_data = crm[crm["Customer"] == customer]
support_data = support[support["Customer"] == customer]
email_data = email[email["Customer"] == customer]
product_data = product[product["Customer"] == customer]
slack_data = slack[slack["Customer"] == customer]

# Display customer information
st.header("Customer Overview")

st.subheader("CRM Information")
st.dataframe(crm_data)

st.subheader("Support Information")
st.dataframe(support_data)

st.subheader("Email Information")
st.dataframe(email_data)

st.subheader("Product Usage")
st.dataframe(product_data)

st.subheader("Slack Notes")
st.dataframe(slack_data)

prompt = f"""
Customer Information

CRM:
{crm_data.to_string(index=False)}

Support:
{support_data.to_string(index=False)}

Emails:
{email_data.to_string(index=False)}

Product Usage:
{product_data.to_string(index=False)}

Slack Notes:
{slack_data.to_string(index=False)}

You are an experienced Customer Success Manager.

Analyze the customer information.

Generate:

1. Executive Summary

2. Risks

3. Opportunities

4. Next Best Action

Keep your answer professional and easy to understand.
"""
if st.button("Generate AI Summary"):

    company = crm_data.iloc[0]["Company"]
    deal = crm_data.iloc[0]["DealValue"]
    owner = crm_data.iloc[0]["Owner"]

    tickets = support_data.iloc[0]["OpenTickets"]
    priority = support_data.iloc[0]["Priority"]

    usage = product_data.iloc[0]["FeatureUsage"]
    email_text = email_data.iloc[0]["LastEmail"]
    notes = slack_data.iloc[0]["Notes"]

    st.subheader("AI Customer Summary")

    st.markdown(f"""
### Executive Summary
**{customer}** from **{company}** has a deal value of **${deal}** and is managed by **{owner}**.

### Risks
- Open Support Tickets: **{tickets}**
- Ticket Priority: **{priority}**

### Opportunities
- Product Usage: **{usage}**
- Recent Email: {email_text}

### Next Best Action
- Resolve outstanding support issues.
- Contact the customer regarding: **{email_text}**
- Review internal note: **{notes}**
- Schedule a follow-up meeting.
""")

    