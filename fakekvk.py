# Company Info Streamlit Web App
import streamlit as st
import json
import time

# Function to save company data to JSON file
def save_company_to_file(company, filename="company_data.json"):
    with open(filename, "w") as f:
        json.dump(company, f, indent=2)

# Page configuration
st.set_page_config(page_title="Company Info", page_icon="🏢", layout="centered")

# Custom CSS
st.markdown(
    """
    <style>
    body, .stApp {
        background: #f7fafd !important;
    }
    .modern-container {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 4px 32px rgba(0,0,0,0.08);
        padding: 3rem 2rem 2rem 2rem;  /* extra top padding for title */
        max-width: 420px;
        margin: 3rem auto 2rem auto;
        border: 1.5px solid #e0e7ef;
    }
    .modern-title {
        color: #3a3a5a;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.7rem;
        text-align: center;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    .modern-desc {
        color: #5a6a7a;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2.2rem;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    .stTextInput > div > input, 
    .stNumberInput > div > input, 
    .stTextArea > div > textarea, 
    .stSelectbox > div {
        background: #f3f7fa;
        border: 1.5px solid #b3c7e6;
        border-radius: 7px;
        color: #2a3a4a !important;
    }
    .stTextInput > div > input::placeholder, 
    .stNumberInput > div > input::placeholder, 
    .stTextArea > div > textarea::placeholder {
        color: #b3c7e6 !important;
        opacity: 1;
    }
    .stTextInput > label, 
    .stNumberInput > label, 
    .stTextArea > label, 
    .stSelectbox > label {
        color: #3a3a5a;
        font-weight: 600;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }

    /* Save button base style */
    .stFormSubmitButton  > button {
        background: linear-gradient(90deg, #6ec1e4 0%, #0077C8 100%);
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
        border-radius: 7px;
        font-weight: 700;
        border: none;
        padding: 0.8rem 2.5rem;
        margin-top: 1.2rem;
        transition: background 0.2s;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 1.15rem;
        width: 100%;
        box-shadow: 0 2px 8px rgba(0,119,200,0.08);
        letter-spacing: 1px;
    }

    /* Force white text on hover, focus, active */
    .stFormSubmitButton  > button:hover,
    .stFormSubmitButton  > button:focus,
    .stFormSubmitButton  > button:active,
    .stFormSubmitButton  > button:focus-visible {
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
    }

    /* Optional focus ring */
    .stFormSubmitButton  > button:focus {
        outline: none !important;
        box-shadow: 0 0 0 4px rgba(0,119,200,0.12) !important;
    }

    /* Disabled button */
    .stFormSubmitButton  > button[disabled] {
        color: rgba(255,255,255,0.6) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.6) !important;
    }

    .stForm {
        color: #222;
    }
    .stAlert, .stSuccess {
        background: #eaf6fb !important;
        color: #0077C8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and description inside the white box
st.markdown('<div class="modern-title">Company Info</div>', unsafe_allow_html=True)
st.markdown('<div class="modern-desc">Easily update and save your company details below.</div>', unsafe_allow_html=True)

# Initialize session state
if 'company' not in st.session_state:
    st.session_state.company = {
        "companyName": "Acme Corp",
        "employees": 42,
        "activity": "Manufacturing gadgets",
        "revenue": 100000,
        "kvk": "12345678",
        "legalForm": "Sole Proprietorship",
    }

# Form
with st.form("edit_company"):
    company = st.session_state.company
    company["companyName"] = st.text_input("Company Name", value=company["companyName"])
    company["employees"] = st.number_input("Number of Employees", min_value=1, value=int(company["employees"]))
    company["activity"] = st.text_area("Business Activity", value=company["activity"])
    company["revenue"] = st.number_input("Revenue", min_value=0.0, value=float(company.get("revenue", 0)), step=1.0, format="%.2f")
    company["kvk"] = st.text_input("KVK Number", value=company["kvk"])
    company["legalForm"] = st.selectbox(
        "Legal Form",
        ["Sole Proprietorship", "Partnership", "BV", "NV"],
        index=["Sole Proprietorship", "Partnership", "BV", "NV"].index(company["legalForm"])
    )
    save = st.form_submit_button("Save")

# Handle Save with auto-dismiss after 5 seconds
if save:
    st.session_state.company = company
    save_company_to_file(company)
    st.session_state.saved_time = time.time()
    st.session_state.show_saved = True

if st.session_state.get("show_saved", False):
    st.success("Saved")
    # Check if 5 seconds have passed
    if time.time() - st.session_state.get("saved_time", 0) > 5:
        st.session_state.show_saved = False
        st.experimental_rerun()

# Close container
st.markdown('</div>', unsafe_allow_html=True)
