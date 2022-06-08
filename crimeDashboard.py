from turtle import color
from pyparsing import alphas
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
# from streamlit_folium import st_folium
# %matplotlib inline

# import plost
# from PIL import Image

#Page setting
# st.set_page_config(layout = "wide")

# with open("style.css") as f:
#     st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html= True)


st.title('A.I Department Investigation')

st.header("Welcome To the FBI")
st.caption("Hello new guy!!! I am an A.I call it Rantoncito perez but you can call me master.First assgiment, before lunch Our boss wants a report from all the crimes from austin Texas between 2014 and 2015. HURRRYYY UP")
# with st.expander("See explanation"):
#      st.write("""
#          The chart above shows some numbers I picked for you.
#          I rolled actual dice for these, so they're *guaranteed* to
#          be random.
#      """)
#      st.image("https://static.streamlit.io/examples/dice.jpg")


# Data
xls = pd.ExcelFile('Annual_Crime_dataset_2014.xls')
df_guide = pd.read_excel(xls,'guide')
data = pd.read_excel(xls,'data')

#cleaning data
df_guide["description"] = df_guide["Unnamed: 1"]
df_guide.drop(columns="Unnamed: 1",inplace=True)
df_guide["description"] = df_guide["description"].fillna("")

#Gobal Variables
keep_investigate = False
showing_more = False
invetigate_crime = False

if st.button('Incidents'):
    st.header("Crime in Austin TX")
    st.dataframe(data)
    
    col1, col2= st.columns(2)

    # ==========Function Data Guide =================
    

    with col1:
        st.subheader("Status Clearence Guide")
        st.dataframe(df_guide.iloc[27:31])

    with col2:
        st.subheader("Number of reported cases")
        st.dataframe(data["GO Report Date"].value_counts())



    

else:
    st.write('Press your idiot, you need to start looking the data')


st.dataframe(data.describe())

with st.expander("See explanation"):
     st.write("""
         all statistic information
         that you will need from the columns,
         this data will be important for computation and be 
         more accord in or investigation.
     """)
     st.image("markus-winkler-cS2eQHB7wE4-unsplash.jpg")
#charge data frame


#=============FUNCTION NUMBER OF CRIMES========================

if st.button('Incidents Per Districts'):
    keep_investigate = True
    sns.set_theme(style="whitegrid")


    x = data["GO District"].value_counts()

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(4, 4))
    # Plot Incidents by Districts
    sns.set_color_codes("pastel")
    sns.barplot(x=x,
                y = data["GO District"].unique(),
                data=data,
                label="GO Highest Offense Desc",
                color="#E11358",
                )


    plt.title("Incident per Districst",fontsize = 18)
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 6000), ylabel="")
    ax.set_xlabel("Number of Incidents",fontsize = 6)
    sns.despine(left=True, bottom=True)

    st.write(f)

if keep_investigate:
    st.caption("All right it looks like we have and idea about how mouch crime is in eache District now, But for sure we can find more data, keep going.")

    st.dataframe(df_guide.iloc[32:])



    # #===============Incident Date Reports======================

    with st.expander("Check the icedent report "):
        st.write("""
         with this data lets create a histogram !!!
     """)
        f2,ax2 = plt.subplots(figsize=(12,8))
        sns.histplot(data = data,x = data["GO Report Date"],
                    bins = 12,color="#42BE71",cbar_ax = "#169acf")
        ax2.set_xlabel('Report Date')
        ax2.set_ylabel("")
        plt.title("Icidents Reports in 20014",fontweight=10,fontsize='20',
                    backgroundcolor='#FF0000',
                    color='white')

        st.write(f2)

st.info('I have notise something really strange, do you want me to check about it')

yes = st.checkbox('Yes, please')

if yes:
    showing_more = True
    
if showing_more:
    st.dataframe(data[["GO Highest Offense Desc","Highest NIBRS/UCR Offense Description"]])
    st.caption("There is nothing strange, just the key word from the crime and the other column is the description lets keep goin with:")


# #==========================CLEARANCE DATE ====================================

    f3,ax3 = plt.subplots(figsize=(14,4))
    sns.histplot(data = data,x = data['Clearance Date'],
                bins = 20,color="#6B9BAF",cbar_ax = "#169acf")

    csfont = {"fontname" : "Comic Sans MS"}
    ax3.set_xlabel('Dates')
    ax3.set_ylabel("")
    plt.title("Icidents Clearance in 20014 / 2015",fontsize = 27 , **csfont,
                        backgroundcolor='#FFDF59',
                color='olive'
                )
    st.write(f3)

    st.subheader("will be interesting if we check the difference on the status clearance, don´t you think??")

    # ======= HISTOPLOT STATUS =======================================================
    f4,ax4 = plt.subplots(figsize=(12,6))
    sns.color_palette("ch:start=.2,rot=-.3")
    sns.histplot(data = data,hue ="Clearance Status" ,x = data['Clearance Date'],element="step",
    common_norm=False,bins = 14
                )
    ax4.set_xlabel("CLERANCE STATUS",**csfont,color = "#4285F4",fontsize = 18 )
    ax4.set_ylabel("")
    plt.tight_layout()
    st.write(f4)

    #Create list of unique Name in
    temp_options = []

    for n in data["GO Highest Offense Desc"].unique():
        temp_options.append(n)
    
    select = st.select_slider("Chose a crime",options=temp_options)
    st.dataframe(data[data["GO Highest Offense Desc"]== select])

    if st.button('Incidents Per HIghest Ooffense'):
        invetigate_crime = True
        col1, col2= st.columns(2)

       
        # ======= HISTOPLOT STATUS =======================================================

        values = data["GO Highest Offense Desc"].value_counts()
        names = data["GO Highest Offense Desc"].unique()

        fig_plotly = px.pie(data, values=values, names=names,
                        title='Highest Offense Description in all Districts')
        fig_plotly.update_traces(textposition='inside', textinfo='percent+label')
        # fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        fig_plotly.update_layout(font_family="Courier New",
            font_color="blue",
            title_font_family="Times New Roman",
            title_font_color="red",
            legend_title_font_color="green",
            # fontsize = 13
            )
        fig_plotly.show()

        st.write(fig_plotly)

        with col1:

            # ======= HISTOPLOT STATUS =======================================================
            murder = data[(data["GO Highest Offense Desc"].str.contains("MURDER")) | (data["GO Highest Offense Desc"] == "MANSLAUGHTER")]["GO Highest Offense Desc"]

            murder_count = murder.value_counts()
            murder_unique = murder.unique() 

            fig_plotly_scatter = px.scatter(data,x = murder_count, y = murder_unique,size = murder_count,size_max = 60)

            st.write(fig_plotly_scatter)

            with col1:
                # ======= HISTOPLOT STATUS =======================================================
                theft = data[data["GO Highest Offense Desc"].str.contains("THEFT")]["GO Highest Offense Desc"]

                theft_count = theft.value_counts()
                theft_unique = theft.unique() 

                fig_plotly_scatter_2 = px.scatter(data,x = theft_unique, y =theft_count ,size = theft_count,
                                                size_max = 60,color = theft_unique,title="THEFT IN AUSTIN",labels={"theft_unique":""})

                fig_plotly_scatter_2.update_xaxes(title_font_family="Arial",tickangle=45)
                fig_plotly_scatter_2.update_yaxes("")

                st.write(fig_plotly_scatter_2)



        # ======= HISTOPLOT STATUS =======================================================

        values = data[data["GO District"] == "D"]["GO Highest Offense Desc"].value_counts()
        names = data[data["GO District"] == "D"]["GO Highest Offense Desc"].unique()
        colors = ["#027862","#70B23D","#E3D825","#32A5D8","#E6EAE9","#99044E","#763F93","#7FC1D5"]

        fig_most_violent = px.pie(data, values=values, names=names,
                    title='The most Violent District : D')
        fig_most_violent.update_traces(textposition='inside', textinfo='percent+label',
                        marker = dict(colors = colors)
                        )

        st.write(fig_most_violent)


        # m = folium.Map(location = [30.266666, -97.733330],zoom_start_ = 15)
        # st_folium = st_folium(m,width = 725) 

if invetigate_crime:
    st.subheader("Lest map all this cases :")


    # ======= HISTOPLOT STATUS =======================================================
    data_2 = pd.read_csv("austin_crime.csv")
    latitude = data_2["latitude"].dropna()
    longitud = data_2["longitude"].dropna()



    i = 0

    crimes = []
    for n in data["Highest NIBRS/UCR Offense Description"]:
        if i == len(latitude):
            break
            
        i += 1
        crimes.append(n)


    fig_map = px.scatter_mapbox(data,lat =latitude,lon= longitud,
                            zoom = 10,
                            color = crimes,
                            title = "Incidents Location Map",
                            width = 900,
                            height = 600,
                        )

    fig_map.update_layout(mapbox_style = "open-street-map")
    fig_map.update_layout(margin={"r" : 0,"t":50,"l":0,"b":10})
    # fig_map.show();
    # 
    st.write(fig_map)



    data = pd.DataFrame({
        'awesome cities' : ['Chicago', 'Minneapolis', 'Louisville', 'Topeka'],
        'lat' : [41.868171, 44.979840,  38.257972, 39.030575],
        'lon' : [-87.667458, -93.272474, -85.765187,  -95.702548]
    })

    # Adding code so we can have map default to the center of the data
    midpoint = (np.average(data['lat']), np.average(data['lon']))

