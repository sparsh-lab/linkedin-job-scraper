import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def clean_and_analyze_jobs():
    """Clean duplicate jobs and visualize company hiring frequency"""
    
    # 1. Load all CSV files (in case you scraped multiple times)
    print("📁 Loading CSV files...")
    csv_files = glob.glob("linkedin_jobs*.csv")
    
    if not csv_files:
        print("❌ No LinkedIn job CSV files found!")
        return
    
    print(f"✅ Found {len(csv_files)} CSV files: {csv_files}")
    
    # 2. Combine all CSV files
    all_jobs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            all_jobs.append(df)
            print(f"📊 Loaded {len(df)} jobs from {file}")
        except Exception as e:
            print(f"⚠️ Error loading {file}: {e}")
    
    if not all_jobs:
        print("❌ No data loaded!")
        return
    
    # 3. Combine all dataframes
    combined_df = pd.concat(all_jobs, ignore_index=True)
    print(f"📋 Total jobs before cleaning: {len(combined_df)}")
    
    # 4. Clean duplicates based on Job Title + Company + Location
    print("🧹 Removing duplicates...")
    
    # Remove rows where essential fields are NULL
    before_null_removal = len(combined_df)
    combined_df = combined_df[
        (combined_df['Job Title'] != 'NULL') & 
        (combined_df['Company'] != 'NULL')
    ]
    print(f"🗑️ Removed {before_null_removal - len(combined_df)} jobs with NULL titles/companies")
    
    # Remove duplicates
    before_dedup = len(combined_df)
    combined_df = combined_df.drop_duplicates(
        subset=['Job Title', 'Company', 'Location'], 
        keep='first'
    )
    duplicates_removed = before_dedup - len(combined_df)
    print(f"🔄 Removed {duplicates_removed} duplicate jobs")
    print(f"✅ Final clean dataset: {len(combined_df)} unique jobs")
    
    # 5. Save cleaned dataset
    cleaned_filename = 'linkedin_jobs_cleaned.csv'
    combined_df.to_csv(cleaned_filename, index=False)
    print(f"💾 Saved clean data to: {cleaned_filename}")
    
    # 6. Visualize job frequency by company
    create_company_chart(combined_df)
    
    return combined_df

def create_company_chart(df):
    """Create bar chart of job frequency by company"""
    print("📊 Creating company hiring frequency chart...")
    
    # Count jobs per company
    company_counts = df['Company'].value_counts().head(15)  # Top 15 companies
    
    if len(company_counts) == 0:
        print("❌ No company data to visualize!")
        return
    
    # Create the chart
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(company_counts)), company_counts.values, color='steelblue')
    
    # Customize the chart
    plt.title('Top Companies by Number of Job Listings', fontsize=16, fontweight='bold')
    plt.xlabel('Company Names', fontsize=12)
    plt.ylabel('Number of Job Listings', fontsize=12)
    plt.xticks(range(len(company_counts)), company_counts.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom')
    
    # Improve layout
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    
    # Save the chart
    chart_filename = 'company_hiring_frequency.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    print(f"📈 Chart saved as: {chart_filename}")
    
    # Show the chart
    plt.show()
    
    # Print top companies in table format
    print("\n🏆 TOP COMPANIES HIRING:")
    print("-" * 40)
    top_companies_df = pd.DataFrame({
        'Rank': range(1, min(11, len(company_counts) + 1)),
        'Company': company_counts.head(10).index,
        'Jobs': company_counts.head(10).values
    })
    print(top_companies_df.to_string(index=False))

def display_data_tables(df):
    """Display data in proper table format"""
    print("\n" + "="*80)
    print("📊 DATASET OVERVIEW")
    print("="*80)
    
    # Basic stats
    print(f"Total unique jobs: {len(df)}")
    print(f"Total companies: {df['Company'].nunique()}")
    print(f"Total locations: {df['Location'].nunique()}")
    
    # Display first 10 jobs in table format
    print("\n📋 FIRST 10 JOBS:")
    print("-" * 100)
    display_df = df[['Job Title', 'Company', 'Location']].head(10)
    print(display_df.to_string(index=True, max_colwidth=30))
    
    # Top companies table
    print("\n\n🏆 TOP COMPANIES (Job Count):")
    print("-" * 50)
    company_counts = df['Company'].value_counts().head(10)
    company_table = pd.DataFrame({
        'Company': company_counts.index,
        'Job Count': company_counts.values
    })
    print(company_table.to_string(index=False))
    
    # Top locations table
    print("\n\n🌍 TOP LOCATIONS (Job Count):")
    print("-" * 50)
    location_counts = df['Location'].value_counts().head(10)
    location_table = pd.DataFrame({
        'Location': location_counts.index,
        'Job Count': location_counts.values
    })
    print(location_table.to_string(index=False))
    
    # Sample of complete data
    print("\n\n📄 SAMPLE OF COMPLETE DATA:")
    print("-" * 120)
    sample_df = df.head(5)[['Job Title', 'Company', 'Location', 'Posted Date', 'Job Type']]
    print(sample_df.to_string(index=True, max_colwidth=25))

if __name__ == "__main__":
    # Run the analysis
    print("🚀 Starting LinkedIn Jobs Analysis...")
    clean_df = clean_and_analyze_jobs()
    
    if clean_df is not None:
        display_data_tables(clean_df)
        print("\n✅ Analysis complete!")