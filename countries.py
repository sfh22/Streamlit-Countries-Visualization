
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_observable import observable
import plotly.express as px


@st.cache(allow_output_mutation=True)
def define_file(file):
    result = file.split(".")
    return result[1]

@st.cache(allow_output_mutation=True)
def read_file(file):             
    df = pd.read_csv(file, encoding='latin-1')
   

file  = ("countries.csv")
file2 = ("mena.csv")
file3 = ("Country_status.csv")
file4 = ("Passport_index.csv")

if len(file) == 0:
    st.warning("Add a file")
else:
    df = read_file(file)
    mena = read_file(file2)
    country_status = read_file(file3)
    passport_index = read_file(file4)

    df1 = passport_index.merge(country_status, left_on='Country_name', right_on='TableName', how='inner')

    all_columns = df.columns.tolist()

    df.fillna(df.mean(), inplace=True)

    def value_converter(cols):
        for c in cols:
            df[c] = df[c].astype(str)
            new_data = []
            for val in df[c]:
                val = val.replace(',','.')
                val = float(val)
                new_data.append(val)

            df[c] = new_data

    cols = df[['Pop. Density (per sq. mi.)', 'Coastline (coast/area ratio)', 'Net migration', 'Infant mortality (per 1000 births)', 'Literacy (%)', 'Phones (per 1000)', 'Arable (%)', 'Crops (%)', 'Other (%)', 'Climate', 'Birthrate', 'Deathrate', 'Agriculture', 'Industry', 'Service']]

    value_converter(cols)

    purpose = st.sidebar.selectbox("Choose an Option",["Information about the Dataset", "Countries' Tables", "Visualize the Data",  'Filter the Data', 'Plotly Visualizations'])


    if purpose == "Information about the Dataset":
        st.title("Countries of the World")
        st.text('')

        from PIL import Image
        image = Image.open("countries.jpeg")
        st.image(image)
        st.text('')
        
        st.subheader("Context")
        st.write("World fact sheet, it's fun to link it with other datasets to have more thorough analysis.")
        
        st.subheader("Content")
        st.write("This Dataset contains demoghraphic information about the world's countries. Some of the dataset's content include population, area size, population density, region, GDP, infant mortality, literacy rates, death rates, ")
        
        st.subheader('Acknowledgements')
        st.write('**Source**: All these data sets are made up of data from the US government.\
                    Generally they are free to use if you use the data in the US.\
                    If you are outside of the US, you may need to contact the US Govt to ask.\
                    Data from the World Factbook is public domain. The website says "The World\
                    Factbook is in the public domain and may be used freely by anyone at anytime without seeking permission."\
                    https://www.cia.gov/library/publications/the-world-factbook/docs/faqs.html'
                    )
        
        st.subheader('Data Columns')
        st.write('**Country:** Contains the name of 127 countries in the world')
        st.write('**Region:** Shows the region in which the countries belongs to. For example, Latin America, Western Europe, Northern Africa, etc.')
        st.write('**Population:** Shows the population of each of the countries')
        st.write('**Area:** Contains the Area in squared miles of each of the countries')
        st.write('**Pop. Density:** Shows the population density in miles square for each of the countries')
        st.write('**Coastline:** Displays the ratio of coastline/area')
        st.write('**Net Migration:** Contains the net migtation of each country (Migrated from - Migrated to')
        st.write('**Infant Mortality:** Number of dead new borns per 1000 births')
        st.write('**GDP:** Growth Domestic Product in American Dollars per Capita ')
        st.write('**Literacy:** Percentage of the population whom are literate')
        st.write('**Phones:** The number of citezens who own mobile phones per 1000 people')
        st.write('**Arable:** Percentage of the land that is arable')
        st.write('**Crops:** Percentage of the land which can grow crops')
        st.write('**Other:** Percentage of the land used for other than arable and crops')
        st.write('**Birth Rate:** Number of people born per 1000 people')
        st.write("**Death Rete:** Number of deaths per 1000 people")
        st.write("**Agriculture:** The percentage of agriculture from the countries total GDP")
        st.write("**Industry:** The percentage of industry from the countries total GDP")
        st.write("**Service:** The percentage of service from the countries total GDP")


    elif purpose == "Countries' Tables":
        
        st.title("Countries Data")
        
        geo = df[['Country', 'Region', 'Area (sq. mi.)', 'Coastline (coast/area ratio)', 'Arable (%)', 'Crops (%)', 'Other (%)']]
        demo = df[['Country', 'Population', 'Pop. Density (per sq. mi.)', 'Net migration', 'Infant mortality (per 1000 births)', 'Birthrate', 'Deathrate']]
        socioeco = df[['Country', 'GDP ($ per capita)', 'Literacy (%)', 'Phones (per 1000)', 'Agriculture', 'Industry', 'Service']]
        
        st.text('')

        radio_list = ['Demographics Table', "Geograpical Table", 'SocioEconomical Table']
        query_params = st.experimental_get_query_params()

        
        default = int(query_params["activity"][0]) if "activity" in query_params else 0

        activity = st.sidebar.radio("Which table would you like to see?", radio_list)

        if activity == 'Demographics Table':
           st.experimental_set_query_params(activity=radio_list.index(activity))
           number = st.slider('Number of rows',1,len(demo))
           st.table(demo.head(number))
           

        if activity == 'Geograpical Table':
           st.experimental_set_query_params(activity=radio_list.index(activity))
           number = st.slider('Number of rows',1,len(geo))
           st.table(geo.head(number))

        if activity == 'SocioEconomical Table':
           st.experimental_set_query_params(activity=radio_list.index(activity))
           number = st.slider('Number of rows',1,len(socioeco))
           st.table(socioeco.head(number))


    elif purpose == "Visualize the Data":

        st.title('Explore your Data')

        ########################################################################
        st.set_option('deprecation.showPyplotGlobalUse', False)
            
        st.subheader("Number of Countries by Region")

        region = df['Region'].value_counts()
        plt.figure(figsize=(10,7))
        sns.barplot(x=region.index, y=region.values, palette='rocket')
        plt.ylabel('Counts')
        plt.xticks(rotation = 45)

        if st.checkbox('Show Number of Countries by Region Histogram'):
            st.pyplot()

            st.text('')
            st.text('')

        ############################################################################
        st.subheader('GDP by Region')
        plt.figure(figsize=(10,7))
        sns.boxenplot(data=df, x='Region', y='GDP ($ per capita)')
        plt.xticks(rotation=45)

        if st.checkbox('Show GDP by Region Boxplot'):
            st.pyplot()

            st.text('')
            st.text('')

        ########################################################################
        st.subheader('Correlation between GDP and Variables')

        x = df.loc[:,["Region","GDP ($ per capita)","Infant mortality (per 1000 births)","Birthrate","Phones (per 1000)","Literacy (%)"]]
        sns.pairplot(x, palette='Paired', diag_kind='hist')

        if st.checkbox('Show Correlation between GDP and Variables'):
            st.pyplot()

            st.text('')
            st.text('')

        ####################################################################
        st.subheader('Distribution of Sectors across Regions')

        fig = plt.figure(figsize=(15,15))
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)

        sns.barplot(data=df, x='Agriculture', y='Region', ax=ax1)
        sns.barplot(data=df, x='Service', y='Region', ax=ax2)
        sns.barplot(data=df, x='Industry', y='Region', ax=ax3)

        ax1.set_xlabel('Agriculture', fontsize=15)
        ax2.set_xlabel('Service', fontsize=15)
        ax3.set_xlabel('Industry', fontsize=15)


        plt.subplots_adjust(hspace = 0.5)

        if st.checkbox('Show Distribution of Sectors across Regions'):
            st.pyplot()

            st.text('')
            st.text('')

        #########################################################
        st.subheader('Countries with Highest Service')

        plt.figure(figsize=(12,8))
        sns.barplot(data = df.nlargest(15, 'Service'), y = 'Country', x = 'Service', palette='mako')
        plt.title("TOP15 Countries with the highest Service %", size=16)
        plt.xlabel(xlabel='Service', fontsize=14)

        if st.checkbox('Show Top 15 Countries with Highest Service'):
            st.pyplot()

            st.text('')
            st.text('')

        ########################################################
        st.subheader('Countries with Highest Agriculture')

        plt.figure(figsize=(12,8))
        sns.barplot(data = df.nlargest(15, 'Agriculture'), y = 'Country', x = 'Agriculture', palette='magma')
        plt.title("TOP15 Countries with the highest Agriculture %", size=16)
        plt.xlabel(xlabel='Agriculture', fontsize=14)

        if st.checkbox('Show Top 15 Countries with Highest Agriculture'):
            st.pyplot()

            st.text('')
            st.text('')

        ########################################################
        st.subheader('Countries with Highest Industry')

        plt.figure(figsize=(12,8))
        sns.barplot(data = df.nlargest(15, 'Industry'), y = 'Country', x = 'Industry', palette='viridis')
        plt.title("TOP15 Countries with the highest Industry %", size=16)
        plt.xlabel(xlabel='Industry', fontsize=14)

        if st.checkbox('Show Top 15 Countries with Highest Industry'):
            st.pyplot()

            st.text('')
            st.text('')
    
        ########################################################

    elif purpose == 'Filter the Data':
        df.head()

        st.title("Filter by GDP, Population, and Area")

        st.text('')
 
        sliders = {'GDP': st.sidebar.slider('Filter by GDP (Min)', 500.0, 60000.0, 500.0, 500.0),
                   'GDP1': st.sidebar.slider('Filter by GDP (Max)', 500.0, 60000.0, 60000.0, 500.0),
                   'Population': st.sidebar.slider('Filter by Population (Min)', 7000, 1400000000, 7000, 10000),
                   'Population1': st.sidebar.slider('Filter by Population (Max)', 7000, 1400000000, 1400000000, 10000),
                   'Area': st.sidebar.slider('Filter by Area (Min)', 2, 18000000, 2, 100000),
                   'Area1': st.sidebar.slider('Filter by Area (Max)', 2, 18000000, 18000000, 100000)
                   }

        filter = np.full(227, True)  # Initialize filter as only True

        for feature_name, slider in sliders.items():
            # Here we update the filter to take into account the value of each slider
            filter = (
            filter & (df['GDP ($ per capita)'] >= sliders.get("GDP")) & (df['GDP ($ per capita)'] <= sliders.get("GDP1"))
            & (df['Population'] >= sliders.get('Population')) & (df['Population'] <= sliders.get('Population1'))
            & (df['Area (sq. mi.)'] >= sliders.get('Area')) & (df['Area (sq. mi.)'] <= sliders.get('Area1'))
            )


        st.subheader('Number of Countries in Filtered Table')
        st.write(len(df[filter]))


        st.subheader('Filtered Table')
        st.write(df[filter])




    elif purpose == 'Plotly Visualizations':

        st.title("Plotly Visualizations")
        st.text('')
        st.text('')

        st.subheader('Visa Free Score by MENA Country')

        fig = px.bar(mena, x="country", y="visa_free_score", color="country", animation_frame="year", animation_group="country")
        fig.update_xaxes(tickangle=45)
        fig.update_xaxes(title_standoff = 40)
        
        if st.checkbox('Show Visa Free Score'):
            st.plotly_chart(fig)
            st.text('')
            st.text('')

        st.subheader('Scatter Plot of Visa Score vs Country Rank')
        fig1 = px.scatter(mena, x="visa_free_score", y="rank", animation_frame="year", animation_group="country",
           color="income_group", hover_name="country",
           log_x=True, size_max=55)

        if st.checkbox('Show Scatter Plot'):
            st.plotly_chart(fig1)
            st.text('')
            st.text('')
        
        st.subheader('Population and Life Expectancy shown per Region and Country')
        df1 = px.data.gapminder().query("year == 2007")
        fig2 = px.sunburst(df1, path=['continent', 'country'], values='pop',
                color='lifeExp', hover_data=['iso_alpha'],
                color_continuous_scale='RdBu',
                color_continuous_midpoint=np.average(df1['lifeExp'], weights=df1['pop']))

        if st.checkbox('Show Pie Chart'):
            st.plotly_chart(fig2)
            st.text('')
            st.text('')
