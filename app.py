import streamlit as st
import pandas as pd
from data_loader import DataLoader
from data_validator import DataValidator
from database import Database
from card_gallery import CardGallery

# Set page configuration for better layout
st.set_page_config(layout="wide")
st.write("Page configuration set.")

# Load the CSS in Streamlit
st.markdown("""
    <style>
    .main { background-color: #121212; color: #e0e0e0; }
    .sidebar .sidebar-content { background-color: #1e1e1e; }
    .stButton>button { background-color: #bb86fc; color: white; border: none; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
    .stButton>button:hover { background-color: #3700b3; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title('Virtual Card Collection Album')

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Upload File", "Card Gallery", "Export Collection"])

# File uploader allowing multiple files
uploaded_files = st.sidebar.file_uploader("Upload your Excel files", type=["xlsx"], accept_multiple_files=True)

# Initialize classes
database = Database()
data_loader = DataLoader()
data_validator = DataValidator()
card_gallery = CardGallery()

# Required columns for validation
required_columns = [
    'Card Name', 'Set', 'Type', 'Archetype', 'Level', 'Attribute',
    'Rarity', 'Condition', 'Card Effect', 'ATK', 'DEF',
    'Spell Category', 'Trap Category', 'Price', 'Inventory Count'
]

data_uploaded = False

if uploaded_files:
    try:
        # Load and validate data
        all_data = data_loader.load_and_validate_data(uploaded_files, required_columns)

        if all_data.empty:
            st.stop()

        # Display the uploaded data for debugging purposes
        st.write("Uploaded Data")
        st.write(all_data)

        # Load data into the database
        database.load_data_to_db(all_data)
        data_uploaded = True

        st.success("Data successfully uploaded and stored in the database.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if data_uploaded:
    # Retrieve data from the database for display
    all_data = database.retrieve_data_from_db()
    st.write("Data retrieved from database:")
    st.write(all_data)
else:
    all_data = pd.DataFrame()

# Sidebar for filters
st.sidebar.header("Filters")
card_types = st.sidebar.multiselect("Card Type", options=["Monsters", "Spells", "Traps"], default=["Monsters", "Spells", "Traps"])
price_sort = st.sidebar.radio("Sort by Price", options=["Ascending", "Descending"])
quantity_sort = st.sidebar.radio("Sort by Quantity", options=["Ascending", "Descending"])
alphabetical_sort = st.sidebar.radio("Sort Alphabetically", options=["A-Z", "Z-A"])

# Apply filters
filtered_data = card_gallery.apply_filters(all_data, card_types, price_sort, quantity_sort, alphabetical_sort)

if options == "Card Gallery":
    st.header("Card Gallery")
    st.write("Explore your card collection visually.")
    if filtered_data.empty:
        st.write("No cards match the selected filters.")
    else:
        card_gallery.display_card_gallery(filtered_data)
elif options == "Export Collection":
    st.header("Export Collection")
    st.write("Export your card collection to an Excel file.")

    if st.button("Export to Excel"):
        df = database.fetch_data_from_db()
        export_path = database.export_to_excel(df)

        with open(export_path, 'rb') as file:
            st.download_button(
                label="Download Exported Collection",
                data=file,
                file_name='exported_collection.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
else:
    st.sidebar.write("Please upload Excel files to proceed.")