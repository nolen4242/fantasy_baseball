import streamlit as st
import pandas as pd
import csv

def read_csv_to_dataframe(filename):
    data = []
    with open(filename, 'r', encoding='latin-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return pd.DataFrame(data)

def batter_data():
    batter_filename = 'batter-data.csv'
    batter_df = read_csv_to_dataframe(batter_filename)

    # Search feature
    search_name = st.text_input("Batter Name:")
    st.caption("Sorted by projected WAR")

    # Apply search to the original DataFrame
    search_result = search_by_name(batter_df, search_name)

    # Display the original DataFrame
    st.write("Batter DataFrame:")
    st.dataframe(search_result, width=1000)  # Adjust the width as needed

def pitcher_data():
    pitcher_filename = 'pitcher-data.csv'
    pitcher_df = read_csv_to_dataframe(pitcher_filename)

    # Search feature
    search_name = st.text_input("Pitcher name:")
    st.caption("Sorted by projected WAR")

    # Apply search to the original DataFrame
    search_result = search_by_name(pitcher_df, search_name)

    # Display the original DataFrame
    st.write("Pitcher DataFrame:")
    st.dataframe(search_result, width=1000)  # Adjust the width as needed

def search_by_name(df, name):
    if name:
        return df[df['Name'].str.contains(name, case=False, na=False)]
    return df

def stat_scout():
    st.write("StatScout will recommend players to draft.")

    # Initialize session state DataFrames if not already initialized
    if "batter_df" not in st.session_state:
        st.session_state.batter_df = read_csv_to_dataframe('batter-data.csv')
    if "pitcher_df" not in st.session_state:
        st.session_state.pitcher_df = read_csv_to_dataframe('pitcher-data.csv')

    # Ensure selected players are initialized
    if "selected_players" not in st.session_state:
        st.session_state.selected_players = []

    # Display the search results with checkboxes for selection
    all_players = st.session_state.batter_df['Name'].tolist() + st.session_state.pitcher_df['Name'].tolist()
    selected_players = st.multiselect("Select Players", all_players, default=st.session_state.selected_players)

    # Update the selected players in the session state
    st.session_state.selected_players = selected_players

    # Check if no players are selected
    if not st.session_state.selected_players:
        st.warning("Please select at least one player.")
        return

    # Create an empty DataFrame for totals
    totals_df = pd.DataFrame(columns=["Name", "Stolen Bases", "Runs", "RBIs", "Home Runs", "OBP"])

    # Calculate and add total stats to the totals DataFrame
    totals_df.loc[0, "Name"] = "Total Stats"
    totals_df.loc[0, "Stolen Bases"] = sum(
        st.session_state.batter_df.loc[st.session_state.batter_df['Name'] == player, 'SB'].astype(float).sum()
        for player in st.session_state.selected_players
    )
    totals_df.loc[0, "Runs"] = sum(
        st.session_state.batter_df.loc[st.session_state.batter_df['Name'] == player, 'R'].astype(float).sum()
        for player in st.session_state.selected_players
    )
    totals_df.loc[0, "RBIs"] = sum(
        st.session_state.batter_df.loc[st.session_state.batter_df['Name'] == player, 'RBI'].astype(float).sum()
        for player in st.session_state.selected_players
    )
    totals_df.loc[0, "Home Runs"] = sum(
        st.session_state.batter_df.loc[st.session_state.batter_df['Name'] == player, 'HR'].astype(float).sum()
        for player in st.session_state.selected_players
    )
    # Calculate average OBP and add it to the totals DataFrame
    average_obp = st.session_state.batter_df.loc[
        st.session_state.batter_df['Name'].isin(st.session_state.selected_players), 'OBP'].astype(float).mean()
    totals_df.loc[0, "OBP"] = f"{average_obp:.3f}"

    # Display the totals DataFrame
    st.write(totals_df.set_index('Name'))

def how_to():
    st.title("Docs")

def main():
    st.title("Fantasy Draft Calculator")
    st.caption("All projections are by Fangraphs/Steamer from Nov 23")

    # Add radio buttons for navigation
    page = st.sidebar.radio("Navigation", ["Steamer Projections", "StatScout", "How to"])

    # Search feature for both data sets
    if page == "Steamer Projections":
        batter_data()
        pitcher_data()
    elif page == "StatScout":
        stat_scout()
    elif page == "How to":
        how_to()

if __name__ == "__main__":
    main()
