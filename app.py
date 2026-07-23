import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Udhaar & Payment Manager", layout="wide")

# Custom CSS for Colorful Styling & Cards Grid
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .dena-card {
        background-color: #ffebee;
        border-left: 5px solid #ef5350;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .lena-card {
        background-color: #e8f5e9;
        border-left: 5px solid #66bb6a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }
    .badge-dena {
        background-color: #e53935;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
    }
    .badge-lena {
        background-color: #43a047;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌈 Colorful Udhaar & Payment Manager")

# Session state initialization
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Sidebar - Entry Form
st.sidebar.header("📝 Nayi Entry Karein")

trans_type = st.sidebar.radio("Transaction Type:", ["Dena Hai (Udhaar)", "Lena Hai (Payment)"])
full_name = st.sidebar.text_input("Grahak ka Naam (Client Name):")
father_name = st.sidebar.text_input("Pita ka Naam (Father's Name):")
mobile_no = st.sidebar.text_input("Mobile Number:")
aadhaar_no = st.sidebar.text_input("Aadhaar Card Number:")
address = st.sidebar.text_area("Pata (Address):")

amount = st.sidebar.number_input("Rashi / Amount (₹):", min_value=0, step=100)
remarks = st.sidebar.text_input("Vivran (Note / Description):")

# Photo Capture Option
camera_photo = st.sidebar.camera_input("📸 Grahak ki photo kheinchein")

if st.sidebar.button("💾 Save Entry"):
    if full_name and mobile_no and amount > 0:
        new_entry = {
            "ID": len(st.session_state.transactions) + 1,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Type": trans_type,
            "Name": full_name,
            "Father Name": father_name,
            "Mobile": mobile_no,
            "Aadhaar": aadhaar_no,
            "Address": address,
            "Amount": amount,
            "Remarks": remarks,
            "Photo": camera_photo
        }
        st.session_state.transactions.append(new_entry)
        st.sidebar.success("Entry Successfully Add Ho Gayi!")
    else:
        st.sidebar.error("Kripya Naam, Mobile aur Amount zaroor bharein.")

# --- Main Dashboard ---
tab1, tab2 = st.tabs(["🔲 Grid Records & Search", "🧾 Print Form / Slip"])

with tab1:
    # Top Stats
    if st.session_state.transactions:
        df_temp = pd.DataFrame(st.session_state.transactions)
        dena_total = df_temp[df_temp["Type"] == "Dena Hai (Udhaar)"]["Amount"].sum()
        lena_total = df_temp[df_temp["Type"] == "Lena Hai (Payment)"]["Amount"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("🔴 Kul Dena Hai", f"₹{dena_total}")
        c2.metric("🟢 Kul Lena Hai", f"₹{lena_total}")
        c3.metric("📊 Total Entries", len(st.session_state.transactions))
        st.markdown("---")

    # Search Bar Section
    st.subheader("🔍 Search Records")
    search_query = st.text_input("📱 Mobile Number ya Naam se search karein:", "").strip().lower()

    # Filtering logic
    filtered_list = st.session_state.transactions
    if search_query:
        filtered_list = [
            t for t in st.session_state.transactions 
            if search_query in t["Mobile"].lower() or search_query in t["Name"].lower() or search_query in t["Aadhaar"].lower()
        ]

    st.subheader("📋 Records Grid View")
    
    if filtered_list:
        # Display as Grid Layout (3 Columns per row)
        cols = st.columns(3)
        for idx, item in enumerate(filtered_list):
            col = cols[idx % 3]
            card_class = "dena-card" if item["Type"] == "Dena Hai (Udhaar)" else "lena-card"
            badge_class = "badge-dena" if item["Type"] == "Dena Hai (Udhaar)" else "badge-lena"
            
            with col:
                st.markdown(f"""
                <div class="{card_class}">
                    <span class="{badge_class}">{item['Type']}</span>
                    <div class="card-title" style="margin-top:8px;">👤 {item['Name']}</div>
                    <p style="margin: 2px 0;"><b>Pita:</b> {item['Father Name']}</p>
                    <p style="margin: 2px 0;"><b>📱 Mobile:</b> {item['Mobile']}</p>
                    <p style="margin: 2px 0;"><b>🪪 Aadhaar:</b> {item['Aadhaar']}</p>
                    <p style="margin: 2px 0; font-size: 18px; color:#d32f2f;"><b>Amount: ₹{item['Amount']}</b></p>
                    <p style="margin: 2px 0; font-size:12px; color:#666;">🗓️ {item['Date']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if item["Photo"]:
                    st.image(item["Photo"], width=120)
    else:
        st.info("Koi record nahi mila.")

with tab2:
    st.subheader("🖨️ Receipt / Slip Print")
    if st.session_state.transactions:
        record_names = [f"{t['Name']} ({t['Mobile']}) - ₹{t['Amount']}" for t in st.session_state.transactions]
        selected_index = st.selectbox("Print Karne Ke Liye Select Karein:", range(len(st.session_state.transactions)), format_func=lambda x: record_names[x])
        
        selected_item = st.session_state.transactions[selected_index]
        
        # Printable Receipt Layout
        st.markdown("---")
        rec_col1, rec_col2 = st.columns([2, 1])
        
        with rec_col1:
            st.markdown(f"## 🧾 **Payment / Udhaar Slip**")
            st.write(f"**Slip Date:** {selected_item['Date']}")
            st.write(f"**Transaction Type:** {selected_item['Type']}")
            st.write(f"**Grahak Name:** {selected_item['Name']}")
            st.write(f"**Pita ka Naam:** {selected_item['Father Name']}")
            st.write(f"**Mobile:** {selected_item['Mobile']}")
            st.write(f"**Aadhaar Number:** {selected_item['Aadhaar']}")
            st.write(f"**Address:** {selected_item['Address']}")
            st.write(f"**Rashi (Amount):** ₹{selected_item['Amount']}")
            st.write(f"**Note:** {selected_item['Remarks']}")
            
        with rec_col2:
            if selected_item['Photo']:
                st.image(selected_item['Photo'], caption="Grahak Photo", width=180)
            else:
                st.write("📷 Photo upload nahi ki gayi")

        st.markdown("---")
        
        # Print Button
        st.components.v1.html(
            """
            <button onclick="window.print()" style="padding:12px 28px; font-size:16px; background-color:#ff4b4b; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">
                🖨️ Form Print / PDF Save Karein
            </button>
            """,
            height=60,
        )
    else:
        st.info("Print karne ke liye koi record nahi hai.")
