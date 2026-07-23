import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Udhaar & Tax System", layout="wide")

# Print CSS Rules
st.markdown("""
    <style>
    @media print {
        body * {
            visibility: hidden;
        }
        .printable-area, .printable-area * {
            visibility: visible;
        }
        .printable-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            padding: 20px;
            background-color: white !important;
            color: black !important;
        }
        header, footer, button, .stTabs {
            display: none !important;
        }
    }
    .tax-box {
        border: 2px solid #1e88e5;
        padding: 20px;
        border-radius: 10px;
        background-color: #f4f7f6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Client Profile, Udhaar & Income Tax Management System")

# Session States initialization
if "clients" not in st.session_state:
    st.session_state.clients = {}
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "tax_records" not in st.session_state:
    st.session_state.tax_records = {}

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 1. Client Profile", 
    "💸 2. Payment Entry", 
    "🔍 3. Grid & Search", 
    "🖨️ 4. Payment Receipt",
    "📑 5. Computing Taxable Income"
])

# ==================== TAB 1: CLIENT PROFILE ====================
with tab1:
    st.header("👤 Naye Client Ki Profile Banayein")
    col1, col2 = st.columns(2)
    with col1:
        c_mobile = st.text_input("📱 Mobile Number (Unique Key):", key="c_mob")
        c_name = st.text_input("👤 Client ka Poora Naam:", key="c_name")
        c_father = st.text_input("👨 Pita ka Naam:", key="c_f")
        c_pan = st.text_input("💳 PAN Number:", key="c_pan")
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
                    "PAN": c_pan.upper(),
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
        client_options = {mob: f"{data['Name']} ({mob})" for mob, data in st.session_state.clients.items()}
        selected_mob = st.selectbox("Client Select Karein:", options=list(client_options.keys()), format_func=lambda x: client_options[x], key="pay_mob")
        client_data = st.session_state.clients[selected_mob]
        
        st.info(f"**Selected Client:** {client_data['Name']} | **PAN:** {client_data.get('PAN', 'N/A')} | **Aadhaar:** {client_data['Aadhaar']}")
        
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
    search_q = st.text_input("🔎 Search (Mobile / Name / PAN / Aadhaar):", "").lower().strip()
    if st.session_state.clients:
        grid_cols = st.columns(3)
        idx = 0
        for mob, profile in st.session_state.clients.items():
            if search_q and (search_q not in mob and search_q not in profile["Name"].lower() and search_q not in profile.get("PAN", "").lower() and search_q not in profile["Aadhaar"].lower()):
                continue
            
            c_trans = [t for t in st.session_state.transactions if t["Mobile"] == mob]
            dena_sum = sum(t["Amount"] for t in c_trans if t["Type"] == "Dena Hai (Given / Udhaar)")
            lena_sum = sum(t["Amount"] for t in c_trans if t["Type"] == "Lena Hai (Received / Payment)")
            
            col = grid_cols[idx % 3]
            with col:
                st.markdown(f"""
                <div style="background-color:#ffffff; border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:15px;">
                    <h4 style="margin:0; color:#1e88e5;">👤 {profile['Name']}</h4>
                    <p style="margin:2px 0;"><b>📱 Mobile:</b> {profile['Mobile']}</p>
                    <p style="margin:2px 0;"><b>💳 PAN:</b> {profile.get('PAN', 'N/A')}</p>
                    <p style="margin:2px 0;"><b>🪪 Aadhaar:</b> {profile['Aadhaar']}</p>
                    <hr style="margin:8px 0;">
                    <p style="margin:2px 0; color:#d32f2f;"><b>🔴 Kul Dena:</b> ₹{dena_sum}</p>
                    <p style="margin:2px 0; color:#2e7d32;"><b>🟢 Kul Lena:</b> ₹{lena_sum}</p>
                </div>
                """, unsafe_allow_html=True)
            idx += 1
    else:
        st.info("Abhi koi Client Profile nahi hai.")

# ==================== TAB 4: PRINT RECEIPT ====================
with tab4:
    st.header("🖨️ Payment Slip / Form Print")
    if st.session_state.transactions:
        trans_options = [f"ID #{t['Trans_ID']} - {t['Client_Name']} - ₹{t['Amount']} ({t['Type']})" for t in st.session_state.transactions]
        selected_t_idx = st.selectbox("Print karne ke liye Transaction chunein:", range(len(trans_options)), format_func=lambda x: trans_options[x])
        
        t_data = st.session_state.transactions[selected_t_idx]
        p_data = st.session_state.clients.get(t_data["Mobile"], {})
        
        st.markdown(f"""
        <div class="printable-area" style="border: 2px solid #333; padding: 25px; border-radius: 8px;">
            <h2 style="text-align: center;">🧾 PAYMENT RECEIPT</h2>
            <hr>
            <p><b>Date:</b> {t_data['Date']} &nbsp;|&nbsp; <b>ID:</b> #{t_data['Trans_ID']}</p>
            <p><b>Name:</b> {t_data['Client_Name']}</p>
            <p><b>Mobile:</b> {t_data['Mobile']} &nbsp;|&nbsp; <b>PAN:</b> {p_data.get('PAN', 'N/A')}</p>
            <p><b>Aadhaar:</b> {p_data.get('Aadhaar', 'N/A')}</p>
            <p><b>Amount:</b> ₹{t_data['Amount']}</p>
            <p><b>Note:</b> {t_data['Remarks']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.components.v1.html("""<button onclick="window.print()" style="padding:10px 20px; background:#2196F3; color:white; border:none; border-radius:5px; margin-top:10px;">🖨️ Print Slip</button>""", height=60)
    else:
        st.info("Koi transaction record nahi hai.")

# ==================== TAB 5: COMPUTING TAXABLE INCOME ====================
with tab5:
    st.header("📑 Computation of Taxable Income Sheet")
    
    if not st.session_state.clients:
        st.warning("Pehle Client Profile banayein.")
    else:
        client_options_tax = {mob: f"{data['Name']} ({mob})" for mob, data in st.session_state.clients.items()}
        tax_mob = st.selectbox("Client Select Karein:", options=list(client_options_tax.keys()), format_func=lambda x: client_options_tax[x], key="tax_mob")
        
        c_info = st.session_state.clients[tax_mob]
        
        st.subheader(f"📊 Income & Deduction Form - {c_info['Name']}")
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("### 💰 Income Head Details")
            salary_income = st.number_input("1. Income from Salary (₹):", min_value=0, step=5000, value=0)
            house_income = st.number_input("2. Income from House Property (Rent) (₹):", step=5000, value=0)
            business_income = st.number_input("3. Profits & Gains of Business/Profession (₹):", step=5000, value=0)
            capital_gains = st.number_input("4. Capital Gains (₹):", min_value=0, step=5000, value=0)
            other_income = st.number_input("5. Income from Other Sources (Interest, Dividend) (₹):", min_value=0, step=1000, value=0)
            
            gross_total_income = salary_income + house_income + business_income + capital_gains + other_income
            st.markdown(f"#### **Gross Total Income (GTI): ₹{gross_total_income:,.2f}**")

        with col_t2:
            st.markdown("### 📉 Deductions under Chapter VI-A")
            sec_80c = st.number_input("Section 80C (PPF, LIC, ELSS etc. Max 1.5L) (₹):", min_value=0, max_value=150000, step=5000, value=0)
            sec_80d = st.number_input("Section 80D (Health Insurance) (₹):", min_value=0, max_value=100000, step=1000, value=0)
            sec_80tta = st.number_input("Section 80TTA / 80TTB (Interest Deduction) (₹):", min_value=0, max_value=50000, step=1000, value=0)
            other_deductions = st.number_input("Other Deductions (80E, 80G etc.) (₹):", min_value=0, step=1000, value=0)
            
            total_deductions = sec_80c + sec_80d + sec_80tta + other_deductions
            if total_deductions > gross_total_income:
                total_deductions = gross_total_income
                
            taxable_income = gross_total_income - total_deductions
            st.markdown(f"#### **Total Deductions: ₹{total_deductions:,.2f}**")
            st.markdown(f"### **Net Taxable Income: ₹{taxable_income:,.2f}**")

        st.markdown("---")
        
        # Computation Sheet View (Printable)
        st.subheader("📄 Printable Tax Computation Sheet")
        
        ay_year = st.text_input("Assessment Year (e.g. 2026-27):", "2026-27")
        
        st.markdown(f"""
        <div class="printable-area tax-box">
            <h2 style="text-align: center; margin-bottom:0;">STATEMENT OF COMPUTATION OF TOTAL INCOME</h2>
            <p style="text-align: center; margin-top:2px;"><b>Assessment Year:</b> {ay_year}</p>
            <hr>
            <table style="width:100%; font-size:15px; border-collapse:collapse;">
                <tr><td><b>Client Name:</b> {c_info['Name']}</td><td><b>Mobile:</b> {c_info['Mobile']}</td></tr>
                <tr><td><b>Father's Name:</b> {c_info['Father Name']}</td><td><b>PAN No:</b> {c_info.get('PAN', 'N/A')}</td></tr>
                <tr><td><b>Aadhaar No:</b> {c_info['Aadhaar']}</td><td><b>Address:</b> {c_info.get('Address', 'N/A')}</td></tr>
            </table>
            <br>
            <table style="width:100%; border:1px solid #333; border-collapse:collapse; padding:8px;">
                <tr style="background-color:#eee; border-bottom:1px solid #333;">
                    <th style="padding:8px; text-align:left;">Particulars / Particulars of Income</th>
                    <th style="padding:8px; text-align:right;">Amount (₹)</th>
                </tr>
                <tr><td style="padding:6px;">1. Income from Salary</td><td style="text-align:right;">{salary_income:,.2f}</td></tr>
                <tr><td style="padding:6px;">2. Income from House Property</td><td style="text-align:right;">{house_income:,.2f}</td></tr>
                <tr><td style="padding:6px;">3. Profits and Gains of Business / Profession</td><td style="text-align:right;">{business_income:,.2f}</td></tr>
                <tr><td style="padding:6px;">4. Capital Gains</td><td style="text-align:right;">{capital_gains:,.2f}</td></tr>
                <tr><td style="padding:6px;">5. Income from Other Sources</td><td style="text-align:right;">{other_income:,.2f}</td></tr>
                <tr style="font-weight:bold; border-top:1px solid #333; border-bottom:1px solid #333;">
                    <td style="padding:8px;">GROSS TOTAL INCOME (GTI)</td>
                    <td style="text-align:right;">{gross_total_income:,.2f}</td>
                </tr>
                <tr><td style="padding:6px;">Less: Deductions under Chapter VI-A (80C, 80D, etc.)</td><td style="text-align:right;">-{total_deductions:,.2f}</td></tr>
                <tr style="font-weight:bold; background-color:#e8f5e9; border-top:2px solid #333;">
                    <td style="padding:10px; font-size:16px;">NET TAXABLE INCOME</td>
                    <td style="text-align:right; font-size:16px;">₹{taxable_income:,.2f}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.components.v1.html("""
            <button onclick="window.print()" style="padding:12px 28px; font-size:16px; background-color:#2196F3; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">
                🖨️ Tax Statement Print / Save PDF
            </button>
        """, height=60)
