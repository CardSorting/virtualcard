import sqlite3
import pandas as pd

# Define the database and excel file paths
DATABASE_PATH = 'cards.db'
EXCEL_TEMPLATE_PATH = '/mnt/data/Final_YuGiOh_Card_Listing_with_Correct_Descriptors_v2.xlsx'
EXPORT_PATH = 'exported_collection.xlsx'

# Placeholder value for fields that are not directly mapped
PLACEHOLDER = ''

# Default placeholder values for specific columns
DEFAULT_VALUES = {
    '*Action(SiteID=US|Country=US|Currency=USD|Version=941)': 'Add',
    'CustomLabel': 'YGO-001',
    '*Category': '183454',  # Example category ID for Yu-Gi-Oh!
    'StoreCategory': '',
    '*Title': 'Yu-Gi-Oh! Blue-Eyes White Dragon',  # Example title
    'Subtitle': 'Limited Edition',
    'Relationship': '',
    'RelationshipDetails': '',
    '*ConditionID': '4000',
    'Condition Descriptor Name 1': 'Condition Descriptor',
    'Condition Descriptor Value 1': '40001',
    'CD:Professional Grader - (ID: 27501)': '',
    'CD:Grade - (ID: 27502)': '',
    'CDA:Certification Number - (ID: 27503)': '',
    'CD:Card Condition - (ID: 40001)': '40001',
    '*C:Franchise': 'Yu-Gi-Oh!',
    'C:Set': 'Legend of Blue Eyes White Dragon',
    'C:Manufacturer': 'Konami',
    'C:Year Manufactured': '2002',
    'C:Character': 'Blue-Eyes White Dragon',
    'C:TV Show': 'Yu-Gi-Oh!',
    'C:Autograph Authentication': '',
    'C:Grade': 'Limited Edition',
    'C:Features': '',
    'C:Parallel/Variety': '',
    'C:Featured Person/Artist': '',
    'C:Autographed': 'No',
    'C:Type': 'Trading Card',
    'C:Card Number': 'LOB-001',
    'C:Card Name': 'Blue-Eyes White Dragon',
    'C:Movie': '',
    'C:Age Level': '10+',
    'C:Signed By': '',
    'C:Material': 'Card Stock',
    'C:Genre': 'Collectible Card Game',
    'C:Graded': 'No',
    'C:Card Size': 'Standard',
    'C:Language': 'English',
    'C:Manufacturered in': 'Japan',
    'P:UPC': '',
    'Start Price': '20.00',
    'Quantity': '1',
    'Item photo URL': 'https://www.example.com/image.jpg',
    'P:EAN': '',
    'Shipping Profile Name': 'Shipping-Default',
    'Return Profile Name': 'Return-Default',
    'Payment Profile Name': 'Payment-Policy-Default',
    'ShippingType': 'Flat',
    'ShippingService': 'USPSFirstClass',
    'ShippingServiceCost': '3.50',
    'ShippingServiceAdditionalCost': '0.50',
    'ShippingServicePriority': '1',
    'Max Dispatch Time': '1',
    'Returns Accepted Option': 'ReturnsAccepted',
    'Returns Within Option': 'Days_30',
    'Refund Option': 'MoneyBack',
    'Return Shipping Cost Paid By': 'Buyer',
    'ListingDuration': 'Days_7',
    'Location': 'New York, NY',
    'Description': 'This is a limited edition Yu-Gi-Oh! Blue-Eyes White Dragon card from the Legend of Blue Eyes White Dragon set.'
}

# Field mapping between database and Excel
FIELD_MAPPING = {
    'Card_Name': 'C:Card Name',
    'Set': 'C:Set',
    'Rarity': 'C:Grade',
    'Condition': 'CD:Card Condition - (ID: 40001)',
    'Price': 'Start Price',
    'Inventory_Count': 'Quantity'
}

def fetch_data_from_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql('SELECT * FROM cards', conn)
    conn.close()
    return df

def map_fields(df):
    # Rename DataFrame columns based on the field mapping
    df = df.rename(columns=FIELD_MAPPING)

    # Add columns that are missing from the DataFrame with default values
    for column in template_columns:
        if column not in df.columns:
            df[column] = DEFAULT_VALUES.get(column, PLACEHOLDER)

    # Ensure the DataFrame columns are in the same order as the template
    df = df[template_columns]

    return df

def export_to_excel(df):
    # Load the Excel template to get the correct column order
    with pd.ExcelFile(EXCEL_TEMPLATE_PATH) as xls:
        sheet_name = xls.sheet_names[0]
        template_df = pd.read_excel(xls, sheet_name=sheet_name)

    # Get the columns from the template
    global template_columns
    template_columns = template_df.columns

    # Ensure the DataFrame has all necessary columns in the correct order
    df = map_fields(df)

    # Export the mapped DataFrame to a new Excel file
    with pd.ExcelWriter(EXPORT_PATH, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)

    return EXPORT_PATH