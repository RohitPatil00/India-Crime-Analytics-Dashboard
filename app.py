import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="India Crime Analytics Dashboard",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: rgba(30, 30, 50, 0.7) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
        border: 1px solid rgba(100, 100, 150, 0.3) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #3949ab, #5c6bc0);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
    }
    
    .kpi-card div:first-child {
        font-size: 14px !important;
        margin-bottom: 12px !important;
        color: #a0a0ff !important;
        font-weight: 600 !important;
        letter-spacing: 0.8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        text-transform: uppercase !important;
    }
    
    .kpi-card div:last-child {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 5px 0 0 0 !important;
        line-height: 1.3 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: #1a1a2e !important;  /* Dark blue-gray */
        color: #e6e6e6 !important;
        padding: 1.5rem 1rem !important;
        border-radius: 0 !important;
        box-shadow: 4px 0 15px rgba(0,0,0,0.3) !important;
        border-right: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    /* Sidebar headers */
    .sidebar .sidebar-content .sidebar-title {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-align: center !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        padding: 0.5rem;
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #2a2a3a !important;
        border-radius: 6px !important;
        padding: 12px 15px !important;
        border: 2px solid #6a6a8a !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #5d5d8d !important;
        background-color: #35354a !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Select box text */
    .stSelectbox > div > div > div {
        color: #4a90e2 !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Dropdown menu */
    .stSelectbox [data-baseweb="select"] {
        background-color: #2a2a3a !important;
        color: #ffffff !important;
    }
    
    /* Dropdown options */
    .stSelectbox [role="listbox"] {
        background-color: #2a2a3a !important;
        border: 2px solid #6a6a8a !important;
        border-radius: 6px !important;
        margin-top: 4px !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }
    
    .stSelectbox [role="option"] {
        color: #e0e0ff !important;
        padding: 12px 15px !important;
        font-size: 1.05em !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #3a3a8a !important;
        color: #ffffff !important;
    }
    
    /* Selected item in dropdown */
    .stSelectbox [aria-selected="true"] {
        background-color: #4a90e2 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar labels */
    .stSelectbox label, .stSlider label {
        color: #a0a0d0 !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        margin: 1.5rem 0 0.5rem 0 !important;
        display: block !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* KPI Subtext */
    .kpi-subtext {
        font-size: 14px !important;
        color: #a0a0ff !important;
        display: block !important;
        margin-top: 6px !important;
        font-weight: 500 !important;
        opacity: 0.9 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #1976d2, #1565c0) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        border: none !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
        margin-top: 1.5rem;
    }
    
    .stButton>button:hover {
        background: linear-gradient(145deg, #1e88e5, #1976d2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #bdc3c7;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #95a5a6;
    }
    
    /* Custom tooltip */
    .stTooltip {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Load NCRB crime data
    file_path = r"C:\Users\rohit\Desktop\New folder\ncrb_crime_data\NCRB_Table_1A.1.csv"
    df = pd.read_csv(file_path, thousands=',')
    
    # Clean and transform the data
    df = df.rename(columns={
        'State/UT': 'State',
        '2020': 'Cases_2020',
        '2021': 'Cases_2021',
        '2022': 'Cases_2022',
        'Rate of Cognizable Crimes (IPC) (2022)': 'Crime_Rate_2022',
        'Chargesheeting Rate (2022)': 'Chargesheet_Rate_2022'
    })
    
    # Remove any rows with missing values in key columns
    df = df.dropna(subset=['State', 'Cases_2020', 'Cases_2021', 'Cases_2022'])
    
    # Convert data to long format for easier visualization
    years = ['2020', '2021', '2022']
    cases = pd.melt(
        df, 
        id_vars=['State', 'Crime_Rate_2022', 'Chargesheet_Rate_2022'], 
        value_vars=[f'Cases_{year}' for year in years],
        var_name='Year',
        value_name='Number_of_Cases'
    )
    
    # Clean up year values
    cases['Year'] = cases['Year'].str.replace('Cases_', '').astype(int)
    
    # Add a crime type column (since the original data doesn't have it, we'll use 'All IPC Crimes')
    cases['Crime_Type'] = 'All IPC Crimes'
    
    return cases

df = load_data()

# Load India GeoJSON
@st.cache_data
def load_geojson():
    # This is a simplified GeoJSON for India states
    # In a real app, use a more accurate GeoJSON file
    india_geojson = requests.get(
        "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    ).json()
    return india_geojson

# Header with gradient
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); 
                padding: 2rem; 
                border-radius: 12px; 
                color: white;
                margin-bottom: 2rem;">
        <h1 style='color: white; margin: 0;'>🔍 India Crime Analytics Dashboard</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
            Analyzing crime patterns and trends across Indian states using NCRB data (2020-2022)
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Sidebar with improved styling
with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>🔍 Filters</h1>", unsafe_allow_html=True)
    
    # Year filter with better visibility
    selected_year = st.selectbox(
        "Select Year",
        options=sorted(df['Year'].unique(), reverse=True),
        help="Filter data by year"
    )
    
    # Add some spacing
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # State filter with better visibility
    state_list = ['All'] + sorted(df['State'].unique().tolist())
    selected_state = st.selectbox(
        "Select State",
        options=state_list,
        help="Filter by state or view all states"
    )
    
    # Add a divider and some info
    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px; margin-top: 2rem;'>
        <p style='color: #ffffff; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
            <span style='font-size: 1.2em; margin-right: 5px;'>ℹ️</span> 
            <strong>Tip:</strong> Use the filters above to explore crime data across different years and states in India.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Apply filters
filtered_df = df[df['Year'] == selected_year].copy()
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['State'] == selected_state]
    
# Sort by number of cases for better visualization
filtered_df = filtered_df.sort_values('Number_of_Cases', ascending=False)

# KPI Cards with Icons
st.markdown("### 📊 Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_crimes = filtered_df['Number_of_Cases'].sum()
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div>📌 Total IPC Crimes</div>
            <div>{int(total_crimes):,}<span class='kpi-subtext'>{'' if selected_state == 'All' else 'In ' + selected_state}</span></div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col2:
    if selected_state == 'All':
        highest_crime_state = filtered_df.groupby('State')['Number_of_Cases'].sum().idxmax()
        highest_crimes = int(filtered_df.groupby('State')['Number_of_Cases'].sum().max())
        st.markdown(
            f"""
            <div class='kpi-card'>
                <div>🏆 Highest Crime State</div>
                <div>{highest_crime_state}<span class='kpi-subtext'>{highest_crimes:,} cases</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        crime_rate = filtered_df['Crime_Rate_2022'].values[0] if 'Crime_Rate_2022' in filtered_df.columns else 'N/A'
        st.markdown(
            f"""
            <div class='kpi-card'>
                <div>📈 Crime Rate (per lakh)</div>
                <div>{crime_rate}<span class='kpi-subtext'>per 100,000 pop.</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )

with col3:
    if selected_state == 'All':
        avg_crimes = int(filtered_df['Number_of_Cases'].mean())
        st.markdown(
            f"""
            <div class='kpi-card'>
                <div>📊 Avg. Crimes per State</div>
                <div>{avg_crimes:,.0f}<span class='kpi-subtext'>across all states</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        chargesheet_rate = filtered_df['Chargesheet_Rate_2022'].values[0] if 'Chargesheet_Rate_2022' in filtered_df.columns else 'N/A'
        st.markdown(
            f"""
            <div class='kpi-card'>
                <div>📝 Chargesheet Rate</div>
                <div>{chargesheet_rate}%<span class='kpi-subtext'>cases with chargesheet</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )

# Main Charts Section
st.markdown("---")

# First Row: Two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Crime Trend Analysis")
    if selected_state == 'All':
        yearly_data = df.groupby('Year')['Number_of_Cases'].sum().reset_index()
    else:
        yearly_data = df[df['State'] == selected_state].groupby('Year')['Number_of_Cases'].sum().reset_index()
    
    fig_trend = px.area(
        yearly_data,
        x='Year',
        y='Number_of_Cases',
        title=f"Crime Trend Over Time{' - ' + selected_state if selected_state != 'All' else ''}",
        labels={'Number_of_Cases': 'Number of Cases', 'Year': 'Year'},
        color_discrete_sequence=['#3498db']
    )
    
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Arial'
        )
    )
    
    fig_trend.update_traces(
        line=dict(width=3),
        hovertemplate='<b>%{x}</b><br>%{y:,} cases<extra></extra>',
        fillcolor='rgba(52, 152, 219, 0.2)'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("### 📈 Top States Comparison")
    top_states = filtered_df.nlargest(5, 'Number_of_Cases')
    
    fig_pie = px.pie(
        top_states,
        names='State',
        values='Number_of_Cases',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value:,} cases (%{percent})<extra></extra>',
        marker=dict(line=dict(color='#ffffff', width=1))
    )
    
    fig_pie.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Second Row: Full width bar chart
st.markdown("### 🏆 State-wise Crime Distribution")
top_states = filtered_df.nlargest(15, 'Number_of_Cases').sort_values('Number_of_Cases', ascending=True)

fig_bar = px.bar(
    top_states,
    x='Number_of_Cases',
    y='State',
    orientation='h',
    color='Number_of_Cases',
    color_continuous_scale='Blues',
    labels={'Number_of_Cases': 'Number of Cases', 'State': 'State'},
    text_auto=True
)

fig_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
    yaxis=dict(showgrid=False),
    showlegend=False,
    height=500,
    margin=dict(l=0, r=0, t=40, b=0)
)

fig_bar.update_traces(
    texttemplate='%{x:,.0f}',
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>%{x:,} cases<extra></extra>',
    marker=dict(line=dict(color='#ffffff', width=1))
)

st.plotly_chart(fig_bar, use_container_width=True)

# Interactive Map Section
st.markdown("---")
st.markdown("### 📊 State-wise Crime Analysis")

if selected_state == 'All':
    state_wise_data = filtered_df.groupby('State')['Number_of_Cases'].sum().reset_index()

    india_geojson = load_geojson()
    # Auto-detect the correct state property key in GeoJSON
    state_prop_key = None
    if 'features' in india_geojson and len(india_geojson['features']) > 0:
        prop_keys = list(india_geojson['features'][0]['properties'].keys())
        # Try common keys
        for k in ['NAME_1', 'state_name', 'ST_NM', 'st_nm', 'NAME', 'name']:
            if k in prop_keys:
                state_prop_key = k
                break
        if not state_prop_key:
            # Fallback to first key
            state_prop_key = prop_keys[0]
    else:
        st.error("GeoJSON file is missing features or properties.")
        st.stop()

    geojson_states = set(f['properties'][state_prop_key].strip().lower() for f in india_geojson['features'])

    # Standardize state names in your data
    state_wise_data['State_std'] = state_wise_data['State'].str.strip().str.lower()

    # Find mismatches
    missing_in_geojson = set(state_wise_data['State_std']) - geojson_states
    if missing_in_geojson:
        st.warning(f"These states are missing from the GeoJSON and will not be shown: {missing_in_geojson}")

    # Only keep states that exist in the GeoJSON
    state_wise_data = state_wise_data[state_wise_data['State_std'].isin(geojson_states)]

    fig = px.choropleth(
        state_wise_data,
        geojson=india_geojson,
        locations='State_std',
        featureidkey=f'properties.{state_prop_key}',
        color='Number_of_Cases',
        color_continuous_scale='Viridis',
        labels={'Number_of_Cases': 'Cases'},
        hover_name='State',
        hover_data={'Number_of_Cases': ':,'},
        height=700,
        scope='asia'
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("ℹ️ Hover over states to view detailed crime statistics. Darker shades indicate higher crime rates.")
else:
    st.info("🔍 State-specific map view is not available when a single state is selected. Select 'All' from the state filter to view the interactive map.")

# Data table (collapsible)
with st.expander("📋 View Raw Data Table", expanded=False):
    st.dataframe(
        filtered_df.drop(columns=['Crime_Type']).sort_values('Number_of_Cases', ascending=False),
        use_container_width=True,
        height=400,
        column_config={
            'State': 'State/UT',
            'Year': st.column_config.NumberColumn('Year', format='%d'),
            'Number_of_Cases': st.column_config.NumberColumn('Number of Cases', format='%,d'),
            'Crime_Rate_2022': st.column_config.NumberColumn('Crime Rate (2022)', format='%.1f'),
            'Chargesheet_Rate_2022': st.column_config.NumberColumn('Chargesheet % (2022)', format='%.1f')
        }
    )

# Footer with improved styling
st.markdown(
    """
    <footer style='margin-top: 4rem; padding: 1.5rem; background-color: #f8f9fa; border-radius: 8px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <p style='margin: 0; font-size: 0.9rem; color: #7f8c8d;'>
                    <strong>Data Source:</strong> National Crime Records Bureau (NCRB) 2020-2022
                </p>
                <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #95a5a6;'>
                    For official use only. Data is for informational purposes.
                </p>
            </div>
            <div style='text-align: right;'>
                <p style='margin: 0; font-size: 0.9rem; color: #7f8c8d;'>
                    <strong>Dashboard:</strong> India Crime Analytics
                </p>
                <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #95a5a6;'>
                    Last updated: June 2025
                </p>
            </div>
        </div>
    </footer>
    """,
    unsafe_allow_html=True
)
