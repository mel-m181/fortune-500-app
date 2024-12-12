'''

Description: This program provides users with data insights on the Fortune 500 list of corporations.
Data visualizations, including tables, charts, and graphs highlight trends between corporation revenues,
profits, and employees. The program offers interactive features that allow users to gain specific insights
about different corporations on the Fortune 500 list.
'''


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

st.set_page_config(page_title="Fortune 500 Corporate Headquarters", layout="wide")

st.page_link("finalProject.py", label="About Fortune 500 Corporations", icon="🏢")
st.page_link("pages/Data Report.py", label="Data Report", icon="📝")
st.page_link("pages/Trends and Analytics.py", label="Trends and Analytics", icon="📈")

#[ST4] - Page design features
st.title(":office: :blue[Fortune 500] Corporate Headquarters")

st.write("Fortune 500 is an annual list of the 500 largest corporations that operate in the "
            "United States, published by Fortune magazine. The corporations are ranked "
            "based on revenues, profits, and market value. This data is for the fiscal year "
            "ended on or before Jan. 31, 2017.")

st.subheader(":scroll: History of the Fortune 500")
#Reference article: https://www.investopedia.com/terms/f/fortune500.asp#:~:text=The%20Fortune%20500%20is%20an%20annual%20list%20of%20500%20of,to%20be%20of%20high%20quality.
st.write("The Fortune 500 has put out a list of the top 500 corporations in the United States "
         "since 1955. The list of companies has changed dramatically since the first Fortune 500. "
         "The original Fortune 500 lists only included companies that were in manufacturing, "
         "mining, and energy sectors. In 1995, the Fortune 500 combined all sectors on the list. Being on the Fortune 500 is considered to be very prestigious. "
         "To make it to the list, the company must be a for-profit U.S.-based entity that files financial statements "
         "with a U.S. government agency. The company must also be among the 500 companies with the highest revenues "
         "within the last fiscal year.")
st.write("Over 2,200 American companies have been featured on the list over the course of its history. "
         "There have been 49 companies that have remained on the Fortune 500 list since the magazine was compiled "
         "in 1955. Walmart has remained at the top spot on the list for 12 consecutive years. ")


st.subheader(":arrow_up_small: Ranked Fortune 500")
st.write("The top industries in the Fortune 500 are the technology, healthcare, finance and "
         "insurance, wholesale trade, retail trade, and energy sectors. ")

dfhq = pd.read_csv('fortune_500_hq.csv',index_col="NAME")

#[DA7] - Drop column
columns_to_drop = ["ADDRESS2","SOURCE","COUNTYFIPS","COMMENTS","PRC"]
dfhq.drop(columns=columns_to_drop, axis='columns',inplace=True)


#[DA2] - Sort data in ascending order
dsort = dfhq.sort_values("RANK",ascending=True)
d_rank_sliced = dsort.iloc[:, 4:]
d_rank_sliced.drop("LONGITUDE", axis='columns', inplace=True)
d_rank_sliced.drop("LATITUDE", axis='columns', inplace=True)

#[VIZ1] - Table
column_options = list(d_rank_sliced.columns)

#Creates multiselect options
#[ST1] - Streamlit widget multiselect
selected_columns = st.multiselect(
    "Choose the columns to include in the dataset:",
    options=column_options,
    default=column_options
)

#Displays filtered data frame
if selected_columns:
    filtered_df = d_rank_sliced[selected_columns]
    st.dataframe(filtered_df)

#st.dataframe(d_rank_sliced)



#[MAP]
st.subheader(":earth_americas: Map of Fortune 500 Corporation Headquarters Across the US")
st.write("A majority of Fortune 500 corporations are located in New York, California, and Texas.")
if "LATITUDE" in dfhq.columns and "LONGITUDE" in dfhq.columns:
    dfhq = pd.read_csv('fortune_500_hq.csv')
    #map_data = dfhq[["LATITUDE","LONGITUDE"]]
    #st.map(map_data, color='#0bbde0')
    map_data = dfhq[["LATITUDE", "LONGITUDE","NAME","ADDRESS","REVENUES","CITY","STATE"]]

    #Pydeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position=["LONGITUDE", "LATITUDE"],
        get_radius=10000,
        get_fill_color=[0, 0, 255, 160],  #Blue markers with transparency
        pickable=True,
    )

    #Shows the view of map data
    view_state = pdk.ViewState(
        latitude=map_data["LATITUDE"].mean(),
        longitude=map_data["LONGITUDE"].mean(),
        zoom=4,
        pitch=40,
    )

    #Uses tooltip to create hover features
    tooltip = {
        "html": "<b>Company:</b> {NAME}<br><b>Location:</b> {CITY}, {STATE}<br><b>Address:</b> {ADDRESS}<br><b>Revenues:</b> {REVENUES}",
        "style": {"color": "white", "backgroundColor": "black"},
    }

    #Creates deck
    map_deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
        tooltip=tooltip,
    )

    #Displays map
    st.pydeck_chart(map_deck)


#Reference image:  https://mageenews.com/fortune-global-500-list/
#st.image("fortune500logos.jpg",caption="Company logos of Fortune 500 corporations")





