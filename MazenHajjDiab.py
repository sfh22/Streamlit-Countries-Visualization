import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import plotly 
from plotly import __version__ 
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib

#to read  files
@st.cache
#function that defines the type of the file (csv, xlsx...)
def define_file(file):
    result = file.split(".")
    return result[1]


@st.cache
#function that reads the file depending on its type
def read_file(file):
    #reading the file depending on its type 
    if (define_file(file) == "csv"):                
        data = pd.read_csv(file)
    elif (define_file(file) == "xlsx" or define_file(file) == "xls"):
        data = pd.read_excel(file,engine='openpyxl')
    else:
            data = []
    return data


file  = st.sidebar.text_input("Enter Your file (file must be in the directory)",r"C:\Users\samer\OneDrive\Desktop\msba325.csv")


if len(file) == 0:
    st.warning("Add a file")
else:
    data = read_file(file)
    all_columns = data.columns.tolist()

    purpose = st.sidebar.selectbox("Purpose",["What is the data about","Visualize data", "Explore data"])

    if purpose == "What is the data about":
        st.title("Data")
        st.subheader("Context")
        st.write("Air Pollution continues to be the reason for the killing of Innocent lives in the world. This data will open your eyes and give you a great insight.")
        
        st.subheader("Content")
        st.write("The data contains the number of deaths per 100,000 due to air pollution in around 180 countries from years 1990 until 2017. In addition to that, the data dives deeper into dividing air pollution deaths into three categories: indoor air pollution, outdoor particulate matter and outdoor ozone pollution. ")
        st.write("Air pollution (total) (deaths per 100,000) : Contain total death.")
        st.write("Indoor air pollution (deaths per 100,000) : Contains death due to indoor air pollution.")
        st.write("Outdoor particulate matter (deaths per 100,000) : Contains death due to outdoor pollution.")
        st.write("Outdoor ozone pollution (deaths per 100,000) : Death due to ozone pollution.")

        
    elif purpose=='Visualize data':
        st.title("Visualize your data")
        plot = st.sidebar.selectbox("What do you want to plot",["Nth worst countries",
                                                                "Nth best countries", "Heatmap","Lineplot",
                                                                "Barchart","Animated Barchart"])
        if plot == "Nth worst countries":
            #user chooses between the minimum year (1990 in this case) and maximum year(2017 in this case) present in data 
            top_year = st.sidebar.slider('What year do you want to check the worst', int(data.year.unique()[0]), int(data.year.unique()[len(data.year.unique())-1]))
            #filtering rows corresponding to that specific year
            year_data = data[data['year']==top_year]
            #user chooses the number of countries they want to display
            top_num = st.sidebar.slider("n:",1,30)
            st.header(str(top_num)+ " most air polluted countries map in "+str(top_year))
            #picking the nth countries with highest deaths due to air pollution and plot it on a map
            top = year_data.nlargest(top_num,'air_pollution')
            map_data = top[["latitude","longitude"]]
            st.map(map_data)
            st.write(top[['country','air_pollution']])
        
        elif plot == "Nth best countries":
            #this is similar to the previous code but picking the countries with least number of deaths
            top_year = st.sidebar.slider('What year do you want to check the best', int(data.year.unique()[0]), int(data.year.unique()[len(data.year.unique())-1]))
            year_data = data[data['year']==top_year]
            top_num = st.sidebar.slider("n:",1,30)
            st.header(str(top_num)+ " best countries dealing with air pollution in "+str(top_year))
            top = year_data.nsmallest(top_num,'air_pollution')
            map_data = top[["latitude","longitude"]]
            st.map(map_data)
            st.write(top[['country','air_pollution']])
        
        elif plot == "Heatmap":
            st.header("Heatmap")
            #user picks which variables they want to plot a heatmap for and plot the heatmap
            num_vars_plot = st.sidebar.multiselect("Pick the variables (an error will occur until you pick at least one variable)",["air_pollution","indoor_air_pollution","outdoor_particulate_matter","outdoor_ozone_pollution"])
            st.write(sns.heatmap(data[num_vars_plot].corr(), annot = True))
            plt.title("Heatmap " , fontsize=15)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
                            
                
        elif plot == "Lineplot":
            #users selects the country that they want to plot for
            country_filter = st.sidebar.selectbox('Country', data.country.unique())
            st.header("Lineplot for air pollution in "+str(country_filter))
            #filter rows according to that country
            data1 = data[data["country"]==country_filter]
            #users selects the variables they want to show on the lineplot 
            line_vars = st.sidebar.multiselect("Pick the variables (an error wil occur until you pick at least one variable)",["air_pollution","indoor_air_pollution","outdoor_particulate_matter","outdoor_ozone_pollution"])
            #plotting and specifying the x axis and y axis range
            fig = px.line(data1, x="year", y=line_vars)
            #x axis range depends on the maximum value of air pollution deaths since it varies for each country
            fig.update_yaxes(range=[0, max(data1["air_pollution"])+20])
            fig.update_xaxes(range=[1990, 2018])
            st.plotly_chart(fig)

        elif plot == "Barchart":
            st.header("Bar Chart")
            #user picks countries and year needed and filter the rows accordingly 
            country_filter = st.sidebar.multiselect('Countries', data.country.unique())
            year = st.sidebar.slider('What year do you want to check the best', int(data.year.unique()[0]), int(data.year.unique()[len(data.year.unique())-1]))
            data1 = data[data['year']==year]
            data1 = data1[data1.country.isin(country_filter)]
            #plot a bar chart
            fig = go.Figure(data=[
            go.Bar(name='Air Pollution', x=data1['country'], y=data1['air_pollution']),
            go.Bar(name='Indoor Air Pollution', x=data1['country'], y=data1['outdoor_particulate_matter']),
            go.Bar(name='Outdoor Particulate Matter', x=data1['country'], y=data1['outdoor_ozone_pollution']),
            go.Bar(name='Outdoor Ozone Pollution', x=data1['country'], y=data1['indoor_air_pollution'])])
            st.plotly_chart(fig)
            
            
            
        elif plot == "Animated Barchart":
            st.header("Animated Bar Chart")
            #user selects the countries to filter the rows accordingle 
            country_filter = st.sidebar.multiselect('Countries (an error will occur until you pick at least one country)', data.country.unique())
            #user picks variable that they want to plot
            var = st.sidebar.selectbox("Variable that you want to check",["air_pollution","indoor_air_pollution",
                                                                  "outdoor_particulate_matter","outdoor_ozone_pollution"])
            data1 = data[data.country.isin(country_filter)]
            #plotting a barchart and animating it with respect to the years
            fig = px.bar(data1, x=data1["country"], y=data1[var], color=data1["country"],
                         animation_frame="year", animation_group="country", range_y=[0,max(data1[var])+20])
            st.plotly_chart(fig)
            
    elif purpose == 'Explore data':
        st.title("Explore your data")
        if st.checkbox('Show dataset'):
            number = st.number_input('Number of rows',1,len(data))
            st.dataframe(data.head(number))

        if st.checkbox('Column Names'):
            st.write(data.columns)
        if st.checkbox('Shape of Dataset'):
            data_dim = st.radio('Show Dimension by',('Dimension','Rows','Columns'))
            if data_dim == 'Rows':
                st.text('Number of rows')
                st.write(data.shape[0])
            elif data_dim == 'Columns':
                st.text('Number of columns')
                st.write(data.shape[1])
            else :
                st.text('Data dimension')
                st.write(data.shape)
        if st.checkbox('Data types'):                                       
            st.write(data.dtypes)
        if st.checkbox('Summary'):
            st.write(data.describe().T)
        if st.checkbox('Value Counts'):
            st.text('Value counts by Target/Class')
            selected_column = st.selectbox("Column name",all_columns)
            st.write(data[selected_column].value_counts())

