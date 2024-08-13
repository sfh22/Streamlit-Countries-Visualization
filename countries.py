import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    df = pd.read_csv("countries.csv", encoding='latin-1')
    mena = pd.read_csv("mena.csv", encoding='latin-1')
    country_status = pd.read_csv("Country_status.csv", encoding='latin-1')
    passport_index = pd.read_csv("Passport_index.csv", encoding='latin-1')
    return df, mena, country_status, passport_index

df, mena, country_status, passport_index = load_data()

# Merge data
df1 = passport_index.merge(country_status, left_on='Country_name', right_on='TableName', how='inner')

# Convert columns to numeric
numeric_columns = ['Pop. Density (per sq. mi.)', 'Coastline (coast/area ratio)', 'Net migration',
                   'Infant mortality (per 1000 births)', 'Literacy (%)', 'Phones (per 1000)', 
                   'Arable (%)', 'Crops (%)', 'Other (%)', 'Climate', 'Birthrate', 'Deathrate', 
                   'Agriculture', 'Industry', 'Service']

df[numeric_columns] = df[numeric_columns].apply(lambda x: x.str.replace(',', '.').astype(float))

# Sidebar for navigation
st.sidebar.title("Navigation")
purpose = st.sidebar.radio("Choose an Option", 
                           ["Dataset Information", "Countries' Tables", "Visualize the Data", 
                            'Filter the Data', 'Plotly Visualizations'])

# Dataset Information
if purpose == "Dataset Information":
    st.title("Countries of the World")
    st.image("countries.jpeg", caption="Countries of the World")
    
    st.subheader("Context")
    st.write("This dataset contains demographic information about the world's countries, useful for thorough analysis when linked with other datasets.")

    st.subheader("Content")
    st.write("This dataset includes information such as population, area size, population density, region, GDP, infant mortality, literacy rates, and death rates.")

    st.subheader('Acknowledgements')
    st.write('Source: Data from the World Factbook is public domain and may be used freely by anyone at anytime without seeking permission. \
             [World Factbook FAQ](https://www.cia.gov/library/publications/the-world-factbook/docs/faqs.html)')

    st.subheader('Data Columns')
    st.write(df.columns.tolist())

# Countries' Tables
elif purpose == "Countries' Tables":
    st.title("Countries Data")
    
    table_choice = st.sidebar.selectbox("Select Table Type", 
                                        ["Demographics Table", "Geographical Table", "SocioEconomic Table"])

    if table_choice == 'Demographics Table':
        st.table(df[['Country', 'Population', 'Pop. Density (per sq. mi.)', 
                     'Net migration', 'Infant mortality (per 1000 births)', 
                     'Birthrate', 'Deathrate']].head())

    elif table_choice == 'Geographical Table':
        st.table(df[['Country', 'Region', 'Area (sq. mi.)', 
                     'Coastline (coast/area ratio)', 'Arable (%)', 
                     'Crops (%)', 'Other (%)']].head())

    elif table_choice == 'SocioEconomic Table':
        st.table(df[['Country', 'GDP ($ per capita)', 'Literacy (%)', 
                     'Phones (per 1000)', 'Agriculture', 'Industry', 'Service']].head())

# Visualize the Data
elif purpose == "Visualize the Data":
    st.title('Explore your Data')

    st.subheader("Number of Countries by Region")
    if st.checkbox('Show Histogram'):
        plt.figure(figsize=(10, 7))
        sns.barplot(x=df['Region'].value_counts().index, 
                    y=df['Region'].value_counts().values, palette='rocket')
        plt.xticks(rotation=45)
        st.pyplot()

    st.subheader('GDP by Region')
    if st.checkbox('Show Boxplot'):
        plt.figure(figsize=(10, 7))
        sns.boxenplot(data=df, x='Region', y='GDP ($ per capita)')
        plt.xticks(rotation=45)
        st.pyplot()

    st.subheader('Correlation between GDP and Variables')
    if st.checkbox('Show Pairplot'):
        sns.pairplot(df[["GDP ($ per capita)", "Infant mortality (per 1000 births)", 
                         "Birthrate", "Phones (per 1000)", "Literacy (%)"]])
        st.pyplot()

# Filter the Data
elif purpose == 'Filter the Data':
    st.title("Filter by GDP, Population, and Area")

    gdp_min, gdp_max = st.slider('Select GDP Range', 500.0, 60000.0, (500.0, 60000.0))
    pop_min, pop_max = st.slider('Select Population Range', 7000, 1400000000, (7000, 1400000000))
    area_min, area_max = st.slider('Select Area Range', 2, 18000000, (2, 18000000))

    filtered_df = df[(df['GDP ($ per capita)'] >= gdp_min) & (df['GDP ($ per capita)'] <= gdp_max) & 
                     (df['Population'] >= pop_min) & (df['Population'] <= pop_max) & 
                     (df['Area (sq. mi.)'] >= area_min) & (df['Area (sq. mi.)'] <= area_max)]
    
    st.subheader(f"Filtered Data - {len(filtered_df)} Countries")
    st.dataframe(filtered_df)

# Plotly Visualizations
elif purpose == 'Plotly Visualizations':
    st.title("Plotly Visualizations")

    st.subheader('Visa Free Score by MENA Country')
    if st.checkbox('Show Visa Free Score'):
        fig = px.bar(mena, x="country", y="visa_free_score", color="country", 
                     animation_frame="year", animation_group="country")
        fig.update_xaxes(tickangle=45, title_standoff=40)
        st.plotly_chart(fig)

    st.subheader('Scatter Plot of Visa Score vs Country Rank')
    if st.checkbox('Show Scatter Plot'):
        fig1 = px.scatter(mena, x="visa_free_score", y="rank", animation_frame="year", 
                          animation_group="country", color="income_group", 
                          hover_name="country", log_x=True, size_max=55)
        st.plotly_chart(fig1)

    st.subheader('Population and Life Expectancy shown per Region and Country')
    if st.checkbox('Show Sunburst Chart'):
        df1 = px.data.gapminder().query("year == 2007")
        fig2 = px.sunburst(df1, path=['continent', 'country'], values='pop', 
                           color='lifeExp', hover_data=['iso_alpha'], 
                           color_continuous_scale='RdBu', 
                           color_continuous_midpoint=np.average(df1['lifeExp'], weights=df1['pop']))
        st.plotly_chart(fig2)
