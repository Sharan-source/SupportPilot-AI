import pandas as pd
import re

# 1. Load the raw dataset
print("Loading dataset...")
df = pd.read_csv('customer_support_tickets.csv')
print(f"Initial shape: {df.shape[0]} rows, {df.shape[1]} columns\n")

# ----------------------------------------------------
# Step 2: Fix the '{product_purchased}' placeholder bug
# ----------------------------------------------------
def fill_product_placeholder(row):
    desc = str(row['Ticket Description'])
    prod = str(row['Product Purchased']) if pd.notna(row['Product Purchased']) else 'product'
    return desc.replace('{product_purchased}', prod)

df['Ticket Description'] = df.apply(fill_product_placeholder, axis=1)

# ----------------------------------------------------
# Step 3: Text Cleaning Function
# ----------------------------------------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()                         # Convert to lowercase
    text = re.sub(r'[\r\n\t]+', ' ', text)           # Remove line breaks & tabs
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)       # Remove punctuation/special chars
    text = re.sub(r'\s+', ' ', text).strip()         # Remove redundant spaces
    return text

# Apply text cleaning
df['clean_subject'] = df['Ticket Subject'].apply(clean_text)
df['clean_description'] = df['Ticket Description'].apply(clean_text)

# Combine Subject and Description for stronger NLP feature representation
df['full_ticket_text'] = df['clean_subject'] + " " + df['clean_description']

# ----------------------------------------------------
# Step 4: Handle Missing Values (Imputation)
# ----------------------------------------------------
# If a ticket is unresolved, fill the Resolution column with a standard placeholder
df['Resolution'] = df['Resolution'].fillna('No resolution provided / Unresolved')

# Fill missing Customer Satisfaction Rating with the median score or 0 (unrated)
df['Customer Satisfaction Rating'] = df['Customer Satisfaction Rating'].fillna(0)

# ----------------------------------------------------
# Step 5: Convert Date/Time columns
# ----------------------------------------------------
date_columns = ['Date of Purchase', 'First Response Time', 'Time to Resolution']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# ----------------------------------------------------
# Step 6: Remove Duplicates
# ----------------------------------------------------
initial_count = len(df)
df = df.drop_duplicates(subset=['Ticket ID'])
print(f"Removed {initial_count - len(df)} duplicate records.")

# ----------------------------------------------------
# Step 7: Export Cleaned Dataset
# ----------------------------------------------------
cleaned_file_path = 'cleaned_customer_support_tickets.csv'
df.to_csv(cleaned_file_path, index=False)
print(f"\n✅ Cleaned dataset successfully saved to: {cleaned_file_path}")
print(f"Final shape: {df.shape}")