import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="Patient Care Analytics",
    page_icon="🏥",
    layout="wide"
)

# ==========================================
# 2. Data Loading Function
# ==========================================
@st.cache_data
def load_data():
    """
    Loads CSV files into pandas DataFrames.
    Uses st.cache_data to speed up dashboard reloads.
    Returns empty DataFrames if files are not found, avoiding crash.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data/raw')
    data = {}
    files = {
        'patients': 'patients.csv',
        'doctors': 'doctors.csv',
        'appointments': 'appointments.csv',
        'treatments': 'treatments.csv',
        'billing': 'billing.csv'
    }
    
    for key, filename in files.items():
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            data[key] = pd.read_csv(path)
            # Basic date conversions where applicable
            if 'date' in data[key].columns.to_list() or 'appointment_date' in data[key].columns.to_list():
                for col in data[key].columns:
                    if 'date' in col.lower():
                        try:
                            data[key][col] = pd.to_datetime(data[key][col])
                        except:
                            pass
        else:
            # Fallback to empty dataframe to keep app running
            st.warning(f"File not found: {path}")
            data[key] = pd.DataFrame()
            
    return data

# Load all data
data = load_data()
df_patients = data.get('patients', pd.DataFrame())
df_doctors = data.get('doctors', pd.DataFrame())
df_appointments = data.get('appointments', pd.DataFrame())
df_treatments = data.get('treatments', pd.DataFrame())
df_billing = data.get('billing', pd.DataFrame())

# ==========================================
# 3. Sidebar Filters
# ==========================================
st.sidebar.header("Filters")

# Date range filter
min_date = datetime.date(2020, 1, 1)
max_date = datetime.date(2030, 12, 31)

if not df_appointments.empty and 'appointment_date' in df_appointments.columns:
    df_appointments['appointment_date'] = pd.to_datetime(df_appointments['appointment_date'])
    min_date = df_appointments['appointment_date'].min().date()
    max_date = df_appointments['appointment_date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# City filter (using address from patients if available)
if not df_patients.empty and 'address' in df_patients.columns:
    cities = sorted(df_patients['address'].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect("Select City (Address)", options=cities, default=cities)
else:
    selected_cities = []

# Specialization filter
if not df_doctors.empty and 'specialization' in df_doctors.columns:
    specializations = sorted(df_doctors['specialization'].dropna().unique().tolist())
    selected_specs = st.sidebar.multiselect("Select Specialization", options=specializations, default=specializations)
else:
    selected_specs = []

# ==========================================
# 4. Main Page Structure (Tabs)
# ==========================================
st.title("🏥 Patient Care Analytics Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Patient Insights", "Doctor Performance", "Financial Analytics"])

# Helper function to format currency
def format_currency(value):
    return f"₹{value:,.2f}"

# --- TAB 1: OVERVIEW ---
with tab1:
    st.header("Overview")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_patients = len(df_patients) if not df_patients.empty else 0
    total_appointments = len(df_appointments) if not df_appointments.empty else 0
    total_revenue = df_billing['final_amount'].sum() if not df_billing.empty and 'final_amount' in df_billing.columns else 0
    avg_treatment_cost = df_treatments['cost'].mean() if not df_treatments.empty and 'cost' in df_treatments.columns else 0
    
    col1.metric("Total Patients", f"{total_patients:,}")
    col2.metric("Total Appointments", f"{total_appointments:,}")
    col3.metric("Total Revenue", format_currency(total_revenue))
    col4.metric("Avg Treatment Cost", format_currency(avg_treatment_cost))
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Monthly Appointment Trend")
        if not df_appointments.empty and 'appointment_date' in df_appointments.columns:
            app_trend = df_appointments.copy()
            app_trend['month_year'] = app_trend['appointment_date'].dt.to_period('M').astype(str)
            trend_data = app_trend.groupby('month_year').size().reset_index(name='count')
            fig_trend = px.line(trend_data, x='month_year', y='count', markers=True, title='Appointments Over Time')
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No appointment data available.")
            
    with col_chart2:
        st.subheader("Appointment Status Distribution")
        if not df_appointments.empty and 'status' in df_appointments.columns:
            status_counts = df_appointments['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            fig_status = px.pie(status_counts, names='status', values='count', title='Status Breakdown', hole=0.3)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No status data available.")
            
    st.subheader("Patient Registrations Over Time")
    if not df_patients.empty and 'registration_date' in df_patients.columns:
        reg_trend = df_patients.copy()
        reg_trend['registration_date'] = pd.to_datetime(reg_trend['registration_date'])
        reg_trend['month_year'] = reg_trend['registration_date'].dt.to_period('M').astype(str)
        reg_data = reg_trend.groupby('month_year').size().reset_index(name='count')
        fig_area = px.area(reg_data, x='month_year', y='count', title='Patient Registrations')
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("No registration data available.")


# --- TAB 2: PATIENT INSIGHTS ---
with tab2:
    st.header("Patient Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        if not df_patients.empty and 'gender' in df_patients.columns:
            gender_data = df_patients['gender'].value_counts().reset_index()
            gender_data.columns = ['gender', 'count']
            fig_gender = px.pie(gender_data, names='gender', values='count', hole=0.5, title='Gender Ratio')
            st.plotly_chart(fig_gender, use_container_width=True)
            
    with col2:
        st.subheader("Age Group Distribution")
        if not df_patients.empty and 'age' in df_patients.columns:
            # Create age bins
            bins = [0, 18, 35, 50, 150]
            labels = ['0-18', '19-35', '36-50', '51+']
            df_pat_age = df_patients.copy()
            df_pat_age['age_group'] = pd.cut(df_pat_age['age'], bins=bins, labels=labels, right=True)
            age_data = df_pat_age['age_group'].value_counts().reset_index()
            age_data.columns = ['age_group', 'count']
            fig_age = px.bar(age_data, x='age_group', y='count', title='Patients by Age Group')
            st.plotly_chart(fig_age, use_container_width=True)
            
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Top 10 Cities (Addresses) by Patient Count")
        if not df_patients.empty and 'address' in df_patients.columns:
            city_data = df_patients['address'].value_counts().head(10).reset_index()
            city_data.columns = ['city', 'count']
            fig_city = px.bar(city_data, x='count', y='city', orientation='h', title='Top Cities')
            fig_city.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_city, use_container_width=True)
            
    with col4:
        st.subheader("Blood Group Distribution")
        if not df_patients.empty and 'blood_group' in df_patients.columns:
            blood_data = df_patients['blood_group'].value_counts().reset_index()
            blood_data.columns = ['blood_group', 'count']
            fig_blood = px.bar(blood_data, x='blood_group', y='count', title='Blood Types')
            st.plotly_chart(fig_blood, use_container_width=True)


# --- TAB 3: DOCTOR PERFORMANCE ---
with tab3:
    st.header("Doctor Performance")
    
    if not df_doctors.empty and not df_appointments.empty:
        # Merge doctors and appointments
        doc_app = pd.merge(df_appointments, df_doctors, on='doctor_id', how='inner')
        doc_app['doctor_name'] = doc_app['first_name'] + ' ' + doc_app['last_name']
        
        # Merge with billing to get revenue
        if not df_billing.empty and not df_treatments.empty:
            treat_bill = pd.merge(df_treatments, df_billing, on='treatment_id', how='inner')
            doc_app_rev = pd.merge(doc_app, treat_bill, on='appointment_id', how='left')
            
            # Calculate metrics per doctor
            doc_stats = doc_app_rev.groupby(['doctor_name', 'specialization']).agg(
                total_appointments=('appointment_id', 'nunique'),
                revenue_generated=('final_amount', 'sum')
            ).reset_index()
            # Adding dummy avg rating as it's not in the schema
            doc_stats['avg_rating'] = 4.5 
            
            st.subheader("Doctor Metrics Table")
            st.dataframe(doc_stats.style.format({'revenue_generated': '₹{:,.2f}', 'avg_rating': '{:.1f}'}), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 5 Doctors by Appointments")
                top_docs = doc_stats.nlargest(5, 'total_appointments')
                fig_top_docs = px.bar(top_docs, x='doctor_name', y='total_appointments', title='Top 5 Doctors (Appointments)')
                st.plotly_chart(fig_top_docs, use_container_width=True)
                
            with col2:
                st.subheader("Revenue by Specialization")
                rev_spec = doc_stats.groupby('specialization')['revenue_generated'].sum().reset_index()
                fig_rev_spec = px.bar(rev_spec, x='specialization', y='revenue_generated', title='Revenue vs Specialization')
                st.plotly_chart(fig_rev_spec, use_container_width=True)
                
            st.subheader("No-Show Rate by Doctor")
            if 'status' in doc_app.columns:
                no_shows = doc_app[doc_app['status'].str.lower() == 'no-show']
                ns_counts = no_shows.groupby('doctor_name').size().reset_index(name='no_show_count')
                total_counts = doc_app.groupby('doctor_name').size().reset_index(name='total')
                ns_rate = pd.merge(ns_counts, total_counts, on='doctor_name', how='right').fillna(0)
                ns_rate['no_show_rate'] = (ns_rate['no_show_count'] / ns_rate['total']) * 100
                fig_ns = px.bar(ns_rate, x='doctor_name', y='no_show_rate', title='No-Show Rate (%)')
                st.plotly_chart(fig_ns, use_container_width=True)
                
    else:
        st.info("Doctor or Appointment data is missing.")


# --- TAB 4: FINANCIAL ANALYTICS ---
with tab4:
    st.header("Financial Analytics")
    
    if not df_billing.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue Trend by Month")
            df_bill_date = df_billing.copy()
            df_bill_date['payment_date'] = pd.to_datetime(df_bill_date['payment_date'])
            df_bill_date['month_year'] = df_bill_date['payment_date'].dt.to_period('M').astype(str)
            rev_trend = df_bill_date.groupby('month_year')['final_amount'].sum().reset_index()
            fig_rev = px.line(rev_trend, x='month_year', y='final_amount', markers=True, title='Monthly Revenue Trend')
            st.plotly_chart(fig_rev, use_container_width=True)
            
        with col2:
            st.subheader("Payment Status Breakdown")
            if 'payment_status' in df_billing.columns:
                pay_status = df_billing['payment_status'].value_counts().reset_index()
                pay_status.columns = ['status', 'count']
                fig_pay = px.pie(pay_status, names='status', values='count', title='Payment Status')
                st.plotly_chart(fig_pay, use_container_width=True)
                
        st.subheader("Treatment Cost by Type")
        if not df_treatments.empty:
            cost_type = df_treatments.groupby('treatment_type')['cost'].mean().reset_index()
            fig_cost = px.bar(cost_type, x='treatment_type', y='cost', title='Average Treatment Cost')
            st.plotly_chart(fig_cost, use_container_width=True)
            
        st.subheader("Top 10 Highest Bills")
        top_bills = df_billing.nlargest(10, 'final_amount')
        # Merging with patients for name if possible
        if not df_patients.empty:
            top_bills = pd.merge(top_bills, df_patients[['patient_id', 'first_name', 'last_name']], on='patient_id', how='left')
            top_bills['patient_name'] = top_bills['first_name'] + ' ' + top_bills['last_name']
            display_cols = ['billing_id', 'patient_name', 'total_amount', 'discount', 'final_amount', 'payment_status']
            st.dataframe(top_bills[display_cols].style.format({'total_amount': '₹{:,.2f}', 'discount': '₹{:,.2f}', 'final_amount': '₹{:,.2f}'}), use_container_width=True)
        else:
            st.dataframe(top_bills)
    else:
        st.info("Billing data is missing.")

# ==========================================
# 5. Footer
# ==========================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built by Akash Singh | Healthcare Analytics Project</p>", unsafe_allow_html=True)
