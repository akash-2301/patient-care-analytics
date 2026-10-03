import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up visual style for professional charts
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def load_data():
    """
    Load data from CSV files and print summary statistics.
    Designed to handle missing files gracefully for a robust pipeline.
    """
    data_dir = '../data/raw/'
    files = ['patients.csv', 'doctors.csv', 'appointments.csv', 'treatments.csv', 'billing.csv']
    
    dfs = {}
    for file in files:
        path = os.path.join(data_dir, file)
        if os.path.exists(path):
            dfs[file.split('.')[0]] = pd.read_csv(path)
            print(f"--- Summary for {file} ---")
            print(dfs[file.split('.')[0]].info())
            print(dfs[file.split('.')[0]].describe(include='all'))
            print("\n")
        else:
            print(f"Warning: {path} not found.")
            
    return dfs

def create_and_save_plots(dfs):
    """
    Create 6 requested charts and save them in the docs/ folder.
    """
    docs_dir = '../docs'
    os.makedirs(docs_dir, exist_ok=True)
    
    subtitle = "Built by Akash Singh"
    
    # 1. monthly_appointments.png - Monthly appointment trend
    if 'appointments' in dfs:
        df_app = dfs['appointments'].copy()
        df_app['appointment_date'] = pd.to_datetime(df_app['appointment_date'])
        df_app['month_year'] = df_app['appointment_date'].dt.to_period('M').astype(str)
        monthly_counts = df_app.groupby('month_year').size().reset_index(name='count')
        
        plt.figure()
        sns.lineplot(data=monthly_counts, x='month_year', y='count', marker='o', color='b')
        plt.title('Monthly Appointment Trend\n' + subtitle)
        plt.xlabel('Month-Year')
        plt.ylabel('Number of Appointments')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, 'monthly_appointments.png'))
        plt.close()
        
    # 2. gender_distribution.png - Gender pie chart
    if 'patients' in dfs:
        df_pat = dfs['patients']
        gender_counts = df_pat['gender'].value_counts()
        
        plt.figure()
        plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        plt.title('Gender Distribution\n' + subtitle)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, 'gender_distribution.png'))
        plt.close()

    # 3. treatment_costs.png - Average cost by treatment type
    if 'treatments' in dfs:
        df_treat = dfs['treatments']
        avg_cost = df_treat.groupby('treatment_type')['cost'].mean().sort_values(ascending=False).reset_index()
        
        plt.figure()
        sns.barplot(data=avg_cost, x='treatment_type', y='cost', palette='viridis')
        plt.title('Average Cost by Treatment Type\n' + subtitle)
        plt.xlabel('Treatment Type')
        plt.ylabel('Average Cost (₹)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, 'treatment_costs.png'))
        plt.close()

    # 4. payment_status.png - Payment status breakdown
    if 'billing' in dfs:
        df_bill = dfs['billing']
        status_counts = df_bill['payment_status'].value_counts()
        
        plt.figure()
        plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
        plt.title('Payment Status Breakdown\n' + subtitle)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, 'payment_status.png'))
        plt.close()

    # 5. top_doctors.png - Top 5 doctors by appointments
    if 'appointments' in dfs and 'doctors' in dfs:
        df_app = dfs['appointments']
        df_doc = dfs['doctors']
        
        merged = pd.merge(df_app, df_doc, on='doctor_id', how='left')
        merged['doctor_name'] = merged['first_name'] + ' ' + merged['last_name']
        doc_counts = merged['doctor_name'].value_counts().head(5).reset_index()
        doc_counts.columns = ['doctor_name', 'appointments']
        
        plt.figure()
        sns.barplot(data=doc_counts, x='appointments', y='doctor_name', palette='magma')
        plt.title('Top 5 Doctors by Appointments\n' + subtitle)
        plt.xlabel('Number of Appointments')
        plt.ylabel('Doctor Name')
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, 'top_doctors.png'))
        plt.close()

    # 6. age_distribution.png - Age group bar chart
    if 'patients' in dfs:
        df_pat = dfs['patients'].copy()
        
        # Create age groups
        bins = [0, 18, 35, 50, 150]
        labels = ['0-18', '19-35', '36-50', '51+']
        df_pat['age_group'] = pd.cut(df_pat['age'], bins=bins, labels=labels, right=True)
        age_group_counts = df_pat['age_group'].value_counts().reindex(labels).reset_index()
        age_group_counts.columns = ['age_group', 'count']
        
        plt.figure()
        sns.barplot(data=age_group_counts, x='age_group', y='count', palette='coolwarm')
        plt.title('Age Group Distribution\n' + subtitle)
        plt.xlabel('Age Group')
        plt.ylabel('Number of Patients')
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, 'age_distribution.png'))
        plt.close()

if __name__ == "__main__":
    print("Starting EDA Analysis...")
    data_frames = load_data()
    create_and_save_plots(data_frames)
    print("Plots saved in docs/ folder.")
