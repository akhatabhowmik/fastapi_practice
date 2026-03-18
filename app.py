import streamlit as st
import requests
import pandas as pd

# The URL where your FastAPI server is running
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Patient Management System", layout="wide")
st.title("🏥 Patient Management System")

# Sidebar for Navigation
menu = ["View Patients", "Add Patient", "Edit Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- HELPER FUNCTIONS ---
def get_all_patients():
    response = requests.get(f"{BASE_URL}/view")
    return response.json()

# --- 1. VIEW PATIENTS ---
if choice == "View Patients":
    st.subheader("All Registered Patients")
    
    # Sorting Options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort By", ["bmi", "height", "weight"])
    with col2:
        order = st.radio("Order", ["asc", "desc"], horizontal=True)

    if st.button("Apply Sort"):
        response = requests.get(f"{BASE_URL}/sort?sort_by={sort_by}&order={order}")
        data = response.json()
    else:
        data = get_all_patients()

    if data:
        # Check if the data is a list (from /sort) or a dict (from /view)
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            # Format for the nested dictionary from /view
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index.name = 'Patient ID'
        
        st.dataframe(df, use_container_width=True) # st.dataframe is scrollable and looks cleaner than st.table
    else:
        st.info("No patients found.")

# --- 2. ADD PATIENT ---
elif choice == "Add Patient":
    st.subheader("Register New Patient")
    with st.form("add_form"):
        p_id = st.text_input("Patient ID (e.g., P013)")
        name = st.text_input("Full Name")
        city = st.text_input("City")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["male", "female", "others"])
        height = st.number_input("Height (metres)", min_value=0.1, max_value=2.5, value=1.7, step=0.01)
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
        
        submitted = st.form_submit_button("Add Patient")
        if submitted:
            payload = {
                "id": p_id, "name": name, "city": city, "age": age,
                "gender": gender, "height": height, "weight": weight
            }
            res = requests.post(f"{BASE_URL}/create", json=payload)
            if res.status_code == 201:
                st.success("Patient added successfully!")
            else:
                st.error(f"Error: {res.json().get('detail')}")

# --- 3. EDIT PATIENT ---
elif choice == "Edit Patient":
    st.subheader("Update Patient Records")
    patient_id = st.text_input("Enter Patient ID to Edit (e.g., P001)")
    
    if patient_id:
        # Check if patient exists
        check_res = requests.get(f"{BASE_URL}/patient/{patient_id}")
        if check_res.status_code == 200:
            p_data = check_res.json()
            st.info(f"Currently Editing: **{p_data['name']}**")
            
            # Using columns to make the form look cleaner
            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Name", value=p_data['name'])
                    new_city = st.text_input("City", value=p_data['city'])
                    new_age = st.number_input("Age", min_value=1, max_value=120, value=int(p_data['age']))
                
                with col2:
                    # Find index of current gender to set as default
                    gender_options = ['male', 'female', 'others']
                    current_gender_idx = gender_options.index(p_data['gender']) if p_data['gender'] in gender_options else 0
                    new_gender = st.selectbox("Gender", gender_options, index=current_gender_idx)
                    
                    new_height = st.number_input("Height (m)", min_value=10.0, max_value=250, value=float(p_data['height']), step=0.01)
                    new_weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=float(p_data['weight']), step=0.1)
                
                save_changes = st.form_submit_button("Update All Records")
                
                if save_changes:
                    # Construct payload with all fields
                    update_payload = {
                        "name": new_name,
                        "city": new_city,
                        "age": new_age,
                        "gender": new_gender,
                        "height": new_height,
                        "weight": new_weight
                    }
                    
                    res = requests.put(f"{BASE_URL}/edit/{patient_id}", json=update_payload)
                    
                    if res.status_code == 200:
                        st.success(f"Successfully updated records for {patient_id}!")
                        # Optional: refresh the data to show updated BMI/Verdict
                        st.rerun() 
                    else:
                        error_detail = res.json().get('detail', 'Unknown error')
                        st.error(f"Failed to update: {error_detail}")
        else:
            st.error("Patient ID not found in database.")

# --- 4. DELETE PATIENT ---
elif choice == "Delete Patient":
    st.subheader("Delete Patient")
    del_id = st.text_input("Enter Patient ID to Remove")
    if st.button("Confirm Delete"):
        res = requests.delete(f"{BASE_URL}/delete/{del_id}")
        if res.status_code == 200:
            st.success(f"Patient {del_id} deleted.")
        else:
            st.error("Patient not found.")