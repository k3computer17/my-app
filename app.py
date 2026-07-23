import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Udhaar & Payment System", layout="wide")

st.title("💼 Client Profile & Payment Management System")

# Session States for database
if "clients" not in st.session_state:
    st.session_state.clients = {}  # Mobile number as Key
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Main Tabs for Clean Workflow
tab1, tab2, tab3, tab4 = st.tabs([
    "👤 1. Client Profile Banayein", 
    "💸 2. Payment Entry Karein", 
    "🔍 3. Grid View & Search", 
    "🖨️ 4. Print Receipt / Form"
])

# ==================== TAB 1: CLIENT PROFILE ====================
with tab1:
    st.header("👤 Naye Client Ki Profile Banayein")
    
    col1, col2 = st.columns(2)
    
    with col1:
        c_mobile = st.text_input("📱 Mobile Number (Unique Key):", key="c_mob")
        c_name = st.text_input("👤 Client ka Poora Naam:", key="c_name")
        c_father = st.text_input("👨 Pita ka Naam:", key="c_f")
        c_aadhaar = st.text_input("🪪 Aadhaar Card Number:", key="c_adh")
        c_address = st.text_area("🏠 Pata (Address):", key="c_add")
        
    with col2:
        st.subheader("📸 Live Photo Capture")
        c_photo = st.camera_input("Client ki photo kheinchein", key="c_cam")
        
        if st.button("💾 Save Client Profile", type="primary"):
            if c_mobile and c_name:
                st.session_state.clients[c_mobile] = {
                    "Name": c_name,
                    "Father Name": c_father,
                    "Mobile": c_mobile,
                    "Aadhaar": c_aadhaar,
                    "Address": c_address,
                    "Photo": c_photo,
                    "Created_At": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.success(f"Profile saved successfully for {c_name}!")
            else:
                st.error("Mobile Number aur Naam bharna zaroori hai.")

# ==================== TAB 2: PAYMENT ENTRY ====================
with tab2:
    st.header("💸 Payment / Udhaar Entry Karein")
    
    if not st.session_state.clients:
        st.warning("Pehle Tab 1 me jaakar kam se kam ek Client Profile banayein.")
    else:
        # Select Client
        client_options = {mob: f"{data['Name']} ({mob})" for mob, data in st.session_state.clients.items()}
        selected_mob = st.selectbox("Client Select Karein:", options=list(client_options.keys()), format_func=lambda x: client_options[x])
        
        client_data = st.session_state.clients[selected_mob]
        
        # Display selected client summary
        st.info(f"**Selected Client:** {client_data['Name']} | **Pita:** {client_data['Father Name']} | **Aadhaar:** {client_data['Aadhaar']}")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            pay_type = st.radio("Transaction Type:", ["Dena Hai (Given / Udhaar)", "Lena Hai (Received / Payment)"])
            amount = st.number_input("Rashi / Amount (₹):", min_value=1, step=100)
            remarks = st.text_input("Vivran (Note / Description):")
            
            if st.button("💾 Transaction Save Karein", type="primary"):
                trans_entry = {
                    "Trans_ID": len(st.session_state.transactions) + 1,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Mobile": selected_mob,
                    "Client_Name": client_data["Name"],
                    "Type": pay_type,
                    "Amount": amount,
                    "Remarks": remarks
                }
                st.session_state.transactions.append(trans_entry)
                st.success("Payment entry successfully save ho gayi!")

# ==================== TAB 3: GRID VIEW & SEARCH ====================
with tab3:
    st.header("🔍 Search & Client Ledger Grid")
    
    search_q = st.text_input("🔎 Search (Mobile / Name / Aadhaar):", "").lower().strip()
    
    if st.session_state.clients:
        grid_cols = st.columns(3)
        idx = 0
        
        for mob, profile in st.session_state.clients.items():
            # Search Filter Logic
            if search_q and (search_q not in mob and search_q not in profile["Name"].lower() and search_q not in profile["Aadhaar"].lower()):
                continue
            
            # Calculate Total Dena / Lena for this client
            c_trans = [t for t in st.session_state.transactions if t["Mobile"] == mob]
            dena_sum = sum(t["Amount"] for t in c_trans if t["Type"] == "Dena Hai (Given / Udhaar)")
            lena_sum = sum(t["Amount"] for t in c_trans if t["Type"] == "Lena Hai (Received / Payment)")
            
            col = grid_cols[idx % 3]
            with col:
                st.markdown(f"""
                <div style="background-color:#ffffff; border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:15px; box-shadow:2px 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="margin:0; color:#1e88e5;">👤 {profile['Name']}</h4>
                    <p style="margin:3px 0;"><b>📱 Mobile:</b> {profile['Mobile']}</p>
                    <p style="margin:3px 0;"><b>👨 Pita:</b> {profile['Father Name']}</p>
                    <p style="margin:3px 0;"><b>🪪 Aadhaar:</b> {profile['Aadhaar']}</p>
                    <hr style="margin:8px 0;">
                    <p style="margin:3px 0; color:#d32f2f;"><b>🔴 Kul Dena:</b> ₹{dena_sum}</p>
                    <p style="margin:3px 0; color:#2e7d32;"><b>🟢 Kul Lena:</b> ₹{lena_sum}</p>
                </div>
                """, unsafe_allow_html=True)
                if profile["Photo"]:
                    st.image(profile["Photo"], width=100)
            idx += 1
    else:
        st.info("Abhi koi Client Profile nahi hai.")

# ==================== TAB 4: PRINT RECEIPT ====================
with tab4:
    st.header("🖨️ Payment Slip / Form Print")
    
    if st.session_state.transactions:
        # Choose transaction to print
        trans_options = [f"ID #{t['Trans_ID']} - {t['Client_Name']} - ₹{t['Amount']} ({t['Type']})" for t in st.session_state.transactions]
        selected_t_idx = st.selectbox("Print karne ke liye Transaction chunein:", range(len(trans_options)), format_func=lambda x: trans_options[x])
        
        t_data = st.session_state.transactions[selected_t_idx]
        p_data = st.session_state.clients.get(t_data["Mobile"], {})
        
        # Printable Receipt Design
        st.markdown("---")
        rc1, rc2 = st.columns([2, 1])
        
        with rc1:
            st.markdown("## 🧾 **PAYMENT RECEIPT**")
            st.write(f"**Receipt Date:** {t_data['Date']}")
            st.write(f"**Transaction ID:** #{t_data['Trans_ID']}")
            st.write(f"**Transaction Type:** {t_data['Type']}")
            st.write(f"**Grahak Name:** {t_data['Client_Name']}")
            st.write(f"**Pita ka Naam:** {p_data.get('Father Name', 'N/A')}")
            st.write(f"**Mobile:** {t_data['Mobile']}")
            st.write(f"**Aadhaar Number:** {p_data.get('Aadhaar', 'N/A')}")
            st.write(f"**Address:** {p_data.get('Address', 'N/A')}")
            st.write(f"**Rashi (Amount):** ₹{t_data['Amount']}")
            st.write(f"**Note:** {t_data['Remarks']}")
            
        with rc2:
            if p_data.get("Photo"):
                st.image(p_data["Photo"], caption="Grahak Photo", width=180)
            else:
                st.write("📷 Photo upload nahi hai")

        st.markdown("---")
        
        st.components.v1.html(
            """
            <button onclick="window.print()" style="padding:12px 28px; font-size:16px; background-color:#2196F3; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">
                🖨️ Form / Slip Print Karein
            </button>
            """,
            height=60,
        )
    else:
        st.info("Print karne ke liye abhi koi transaction entry nahi hai.")
