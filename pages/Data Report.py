import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

st.title(":memo: Data Report")

dfhq = pd.read_csv('fortune_500_hq.csv',index_col="NAME")
columns_to_drop = ["ADDRESS2","SOURCE","COUNTYFIPS","COMMENTS","PRC"]
dfhq.drop(columns=columns_to_drop, axis='columns',inplace=True)


st.subheader(":statue_of_liberty: Corporations by State")
st.write("Learn more about the Fortune 500 corporations by filtering the state in which their headquarters is located.")
#[ST2] - Streamlit widget select box
if "STATE" in dfhq.columns:
    states = sorted(dfhq["STATE"].unique())
    selected_state = st.selectbox("Select a state: ", states)
    filtered_df = dfhq[dfhq["STATE"] == selected_state]
    filtered_df.drop("LATITUDE", axis='columns', inplace=True)
    filtered_df.drop("LONGITUDE", axis='columns', inplace=True)
    filtered_df_sliced = filtered_df.iloc[:,4:]

    #[PY2] - Function that returns more than one value
    def state_stats(dataframe, state):
        state_df = dataframe[dataframe["STATE"] == state]
        num_companies = len(state_df)
        #[DA9] - Perform calculations on data frame
        total_employees = state_df["EMPLOYEES"].sum()
        return num_companies, total_employees

    num_companies, total_employees = state_stats(dfhq,selected_state)

    st.write("Number of corporation headquarters in ", selected_state,":", num_companies)
    st.write("Number of people in ", selected_state, " that work for a Fortune 500 corporation:", total_employees)
    st.dataframe(filtered_df_sliced)

    #[VIZ1] - Bar chart
    plt.figure(figsize=(15, 8))
    bars = plt.bar(filtered_df_sliced.index, filtered_df_sliced["REVENUES"], color='skyblue')

    #Labels and title of bar chart
    plt.xlabel("Corporation Name", fontsize=12)
    plt.ylabel("Revenue (in thousands)", fontsize=12)
    plt.title("Revenues of Corporations in State", fontsize=14)
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"${bar.get_height():,.0f}",
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.tight_layout()
    st.pyplot(plt)



st.subheader(":1234: By the numbers:")

#[PY1] - Function with two or more parameters, one of which has a default value
#Counts the number of unique cities there are in the CITY column of dataframe
def city_state_counter(dataframe, col_name="CITY"):
    if col_name in dfhq.columns:
        unique_city = dfhq[col_name].nunique()
        return unique_city

total_cities = city_state_counter(dfhq)
total_states = city_state_counter(dfhq,col_name="STATE")

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Number of cities that have a Fortune 500 corporation headquarter:",
        value=total_cities,
    )

    # [PY4] - List comprehension
    #Creates a data frame that shows the number of headquarters in each city of the CITY column
    if "CITY" in dfhq.columns:
        city_names = [city for city in dfhq["CITY"]]  # Uses list comprehension to extract city names
        city_counts = {city: city_names.count(city) for city in set(city_names)}
        city_counts_df = pd.DataFrame(city_counts.items(), columns=["City", "Number of Corporations"]).sort_values(
            by="Number of Corporations", ascending=False)

        st.dataframe(city_counts_df)

    #Reference article: https://fortune.com/2024/06/04/fortune-500-new-york-city-most-companies/
    st.info("New York City is home to the most Fortune 500 corporations, beating rivals like "
             "Houston, Atlanta, and Chicago. New York is home to some of the biggest names in banking, "
             "while Houston concentrates in industries such as energy and petroleum. ")

with col2:
    st.metric(
        label="Number of states that have a Fortune 500 corporation headquarter:",
        value=total_states,
    )
    #Creates a data frame that shows the number of headquarters in each state of the STATE column
    if "STATE" in dfhq.columns:
        #[PY3] - Error checking with try/except
        try:
            state_names = [state for state in dfhq["STATE"]]  # Uses list comprehension to extract city names
            state_counts = {state: state_names.count(state) for state in set(state_names)}
            state_counts_df = pd.DataFrame(state_counts.items(), columns=["State", "Number of Corporations"]).sort_values(
                by="Number of Corporations", ascending=False)

            st.dataframe(state_counts_df)
        except:
            st.error("An error occurred while creating the state counts data frame.")

    #Reference article: https://www.visualcapitalist.com/map-the-number-of-fortune-500-companies-in-each-u-s-state/#:~:text=California%2C%20New%20York%2C%20and%20Texas,industries%20and%20significant%20economic%20influence.
    st.info("California is home to many of America's biggest innovators and technology "
             "companies including, Apple, Nvidia, and Netflix. Texas has attracted many large "
             "corporations in recent years, with many of them relocating in the state. New York is "
             "primarily known for its financial institutions. ")




