import streamlit as st
import pandas as pd
from b2sdk.v2 import InMemoryAccountInfo, B2Api

class CardGallery:
    B2_KEY_ID = "005b2784557c8a40000000011"
    B2_APPLICATION_KEY = "K005Z6XVNlsFScgLAeNsdvEz/RiA6x0"
    B2_BUCKET_ID = "8b82772864c595e78cf80a14"
    B2_BUCKET_NAME = "playmore"

    def initialize_b2(self):
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", self.B2_KEY_ID, self.B2_APPLICATION_KEY)
        return b2_api.get_bucket_by_id(self.B2_BUCKET_ID)

    def upload_image_to_b2(self, image_data, image_name):
        try:
            bucket = self.initialize_b2()
            bucket.upload_bytes(image_data, image_name)
            return f"https://f005.backblazeb2.com/file/{self.B2_BUCKET_NAME}/{image_name}"
        except Exception as e:
            st.error(f"Error uploading image to B2: {e}")
            return None

    def display_card_gallery(self, data):
        st.write("Displaying card gallery")
        if not data.empty:
            columns = st.columns(3)  # Create 3 columns for the grid layout
            for idx, row in data.iterrows():
                col = columns[idx % 3]
                with col:
                    image_url = row.get('Image URL', '')
                    if not image_url:
                        st.image("https://via.placeholder.com/150", caption="No Image", use_column_width=True)
                    else:
                        st.image(image_url, use_column_width=True)
                    st.write(f"**{row.get('Card Name', 'Unknown')}**")
                    st.write(f"{row.get('Set', 'Unknown Set')}")
                    st.write(f"{row.get('Type', 'Unknown Type')}")

                    if row.get('Type') not in ['Spell', 'Trap']:
                        st.write(f"Level: {row.get('Level', 'N/A')}")
                        st.write(f"Attribute: {row.get('Attribute', 'N/A')}")
                        st.write(f"ATK: {row.get('ATK', 'N/A')}")
                        st.write(f"DEF: {row.get('DEF', 'N/A')}")

                    st.write(f"Rarity: {row.get('Rarity', 'N/A')}")
                    st.write(f"Condition: {row.get('Condition', 'N/A')}")
                    st.write(f"Effect: {row.get('Card Effect', 'N/A')}")
                    st.write(f"Price: **${row.get('Price', 0.0)}**")
                    st.write(f"Inventory Count: {row.get('Inventory Count', 'N/A')}")

    def apply_filters(self, data, card_types, price_sort, quantity_sort, alphabetical_sort):
        st.write("Applying filters...")
        st.write("Selected card types:", card_types)

        required_columns = [
            'Card Name', 'Set', 'Type', 'Level', 'Attribute', 'Rarity', 'Condition', 
            'Card Effect', 'ATK', 'DEF', 'Price', 'Inventory Count', 'Image URL'
        ]

        if data.empty or not all(col in data.columns for col in required_columns):
            st.write("Data is empty or missing required columns.")
            return pd.DataFrame()

        if 'Price' not in data.columns:
            data['Price'] = 0

        if 'Inventory Count' not in data.columns:
            data['Inventory Count'] = 0

        if 'Image URL' not in data.columns:
            data['Image URL'] = ""

        if 'Market Price' not in data.columns:
            data['Market Price'] = 0

        filtered_data = data[data['Type'].isin(card_types)]
        st.write("Filtered data based on card types:")
        st.write(filtered_data)

        if price_sort == "Ascending":
            filtered_data = filtered_data.sort_values(by="Price", ascending=True)
        elif price_sort == "Descending":
            filtered_data = filtered_data.sort_values(by="Price", ascending=False)

        if quantity_sort == "Ascending":
            filtered_data = filtered_data.sort_values(by="Inventory Count", ascending=True)
        elif quantity_sort == "Descending":
            filtered_data = filtered_data.sort_values(by="Inventory Count", descending=False)

        if alphabetical_sort == "A-Z":
            filtered_data = filtered_data.sort_values(by="Card Name", ascending=True)
        elif alphabetical_sort == "Z-A":
            filtered_data = filtered_data.sort_values(by="Card Name", descending=False)

        st.write("Filtered and sorted data:")
        st.write(filtered_data)

        return filtered_data

# Example usage
data = pd.DataFrame({
    'Card Name': ['Drakloak', 'Dreepy', 'Munkidori', 'Bug Catching Set', 'Twilight Masquerade Booster Box'],
    'Set': ['SV06: Twilight Masquerade'] * 5,
    'Type': ['Common', 'Common', 'Rare', 'Uncommon', 'Booster'],
    'Level': [3, 1, 2, None, None],
    'Attribute': ['Dark', 'Dark', 'Psychic', 'None', 'None'],
    'Rarity': ['Common', 'Common', 'Rare', 'Uncommon', 'Rare'],
    'Condition': ['New', 'New', 'New', 'New', 'New'],
    'Card Effect': ['Recon Directive', 'Petty Grudge', 'Athena Brain', 'Draw 2 Cards', 'Contains 10 Packs'],
    'ATK': [70, 40, 60, None, None],
    'DEF': [50, 20, 30, None, None],
    'Price': [0.25, 0.01, 0.17, 0.15, 102.95],
    'Inventory Count': [335, 475, 316, 264, 87],
    'Image URL': ['', '', '', '', '']
})

gallery = CardGallery()
gallery.display_card_gallery(data)