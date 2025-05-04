import pandas as pd
import re

# Load raw CSV
df = pd.read_csv(r"C:\Users\Henri\Documents\GitHub\Saudi_Arabic_Flash_Cards\data\raw_vocab.csv", sep=',', encoding="utf-8")

# Function to remove parenthesis and their content
def extract_arabic_word(full_text):
    if pd.isnull(full_text):
        return ''
    # Remove anything in parentheses
    return re.sub(r'\s*\(.*?\)', '', full_text).strip()

# Apply to create new column
df['arabic_word'] = df['arabic_full'].apply(extract_arabic_word)

# Save to new CSV
df.to_csv(r"C:\Users\Henri\Documents\GitHub\Saudi_Arabic_Flash_Cards\data\vocab.csv", index=False)

print("✅ Preprocessing complete! Saved as vocab.csv.")
