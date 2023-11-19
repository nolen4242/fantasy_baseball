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

def calculate_totals(totals_df, source_batter_df, source_pitcher_df, selected_players, selected_pitchers):
    totals_df.loc[0, "Name"] = "Total Stats"

    # Calculate and add batting stats
    totals_df.loc[0, "Stolen Bases"] = sum(
        source_batter_df.loc[source_batter_df['Name'] == player, 'SB'].astype(float).sum() for player in
        selected_players)
    totals_df.loc[0, "Runs"] = sum(
        source_batter_df.loc[source_batter_df['Name'] == player, 'R'].astype(float).sum() for player in
        selected_players)
    totals_df.loc[0, "RBIs"] = sum(
        source_batter_df.loc[source_batter_df['Name'] == player, 'RBI'].astype(float).sum() for player in
        selected_players)
    totals_df.loc[0, "Home Runs"] = sum(
        source_batter_df.loc[source_batter_df['Name'] == player, 'HR'].astype(float).sum() for player in
        selected_players)
    totals_df.loc[0, "OBP"] = source_batter_df.loc[source_batter_df['Name'].isin(selected_players), 'OBP'].astype(
        float).mean()

    # Calculate and add pitching stats
    totals_df.loc[0, "Wins"] = sum(
        source_pitcher_df.loc[source_pitcher_df['Name'] == player, 'W'].astype(float).sum() for player in
        selected_pitchers)
    totals_df.loc[0, "ERA"] = source_pitcher_df.loc[source_pitcher_df['Name'].isin(selected_pitchers), 'ERA'].astype(
        float).mean()
    totals_df.loc[0, "Saves"] = sum(
        source_pitcher_df.loc[source_pitcher_df['Name'] == player, 'SV'].astype(float).sum() for player in
        selected_pitchers)

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

    # Ensure selected players and pitchers are initialized for both teams
    if "selected_players_team1" not in st.session_state:
        st.session_state.selected_players_team1 = []
    if "selected_pitchers_team1" not in st.session_state:
        st.session_state.selected_pitchers_team1 = []

    if "selected_players_team2" not in st.session_state:
        st.session_state.selected_players_team2 = []
    if "selected_pitchers_team2" not in st.session_state:
        st.session_state.selected_pitchers_team2 = []

    # Display the search results with checkboxes for selection for Team 1 (Batters and Pitchers)
    available_players_team1 = st.session_state.batter_df['Name'].tolist() + st.session_state.pitcher_df['Name'].tolist()
    available_players_team1 = list(set(available_players_team1) - set(st.session_state.selected_players_team2) - set(
        st.session_state.selected_pitchers_team2))
    selected_players_team1 = st.multiselect("Team 1: Select Players", available_players_team1,
                                            default=list(st.session_state.selected_players_team1) + list(st.session_state.selected_pitchers_team1))
    selected_pitchers_team1 = st.multiselect("Team 1: Select Pitchers", available_players_team1,
                                             default=list(st.session_state.selected_pitchers_team1))

    # Update the selected players and pitchers for Team 1 in the session state
    st.session_state.selected_players_team1 = [player for player in selected_players_team1 if
                                               player not in st.session_state.selected_pitchers_team1]
    st.session_state.selected_pitchers_team1 = [player for player in selected_pitchers_team1 if
                                                player not in st.session_state.selected_players_team1]

    # Check if no players are selected for Team 1
    if not selected_players_team1 or not selected_pitchers_team1:
        st.warning("Team 1: Please select at least one player.")
    else:
        # Create an empty DataFrame for Team 1 totals
        totals_df_team1 = pd.DataFrame(
            columns=["Name", "Stolen Bases", "Runs", "RBIs", "Home Runs", "OBP", "Wins", "ERA", "Saves"])

        # Calculate and add total stats to the totals DataFrame for Team 1
        calculate_totals(totals_df_team1, st.session_state.batter_df, st.session_state.pitcher_df,
                         st.session_state.selected_players_team1, st.session_state.selected_pitchers_team1)

        # Display the totals DataFrame for Team 1
        st.write("Team 1 Selected Players and Pitchers:")
        st.write(totals_df_team1.set_index('Name'))

    # Display a divider between Team 1 and Team 2
    st.divider()

    # Display the search results with checkboxes for selection for Team 2 (Batters and Pitchers)
    available_players_team2 = st.session_state.batter_df['Name'].tolist() + st.session_state.pitcher_df['Name'].tolist()
    available_players_team2 = list(set(available_players_team2) - set(st.session_state.selected_players_team1) - set(
        st.session_state.selected_pitchers_team1))
    selected_players_team2 = st.multiselect("Team 2: Select Players", available_players_team2,
                                            default=list(st.session_state.selected_players_team2) + list(st.session_state.selected_pitchers_team2))
    selected_pitchers_team2 = st.multiselect("Team 2: Select Pitchers", available_players_team2,
                                             default=list(st.session_state.selected_pitchers_team2))

    # Update the selected players and pitchers for Team 2 in the session state
    st.session_state.selected_players_team2 = [player for player in selected_players_team2 if
                                               player not in st.session_state.selected_pitchers_team2]
    st.session_state.selected_pitchers_team2 = [player for player in selected_pitchers_team2 if
                                                player not in st.session_state.selected_players_team2]

    # Check if no players are selected for Team 2
    if not selected_players_team2 or not selected_pitchers_team2:
        st.warning("Team 2: Please select at least one player.")
    else:
        # Create an empty DataFrame for Team 2 totals
        totals_df_team2 = pd.DataFrame(
            columns=["Name", "Stolen Bases", "Runs", "RBIs", "Home Runs", "OBP", "Wins", "ERA", "Saves"])

        # Calculate and add total stats to the totals DataFrame for Team 2
        calculate_totals(totals_df_team2, st.session_state.batter_df, st.session_state.pitcher_df,
                         st.session_state.selected_players_team2, st.session_state.selected_pitchers_team2)

        # Display the totals DataFrame for Team 2
        st.write("Team 2 Selected Players and Pitchers:")
        st.write(totals_df_team2.set_index('Name'))


def main():
    st.title("Fantasy Draft Calculator")
    st.caption("All projections are by Fangraphs/Steamer from Nov 23")
    st.divider()

    # Add radio buttons for navigation
    page = st.sidebar.radio("Navigation", ["Steamer Projections", "StatScout", "How to"])

    # Search feature for both data sets
    if page == "Steamer Projections":
        batter_data()
        st.divider()
        pitcher_data()
    elif page == "StatScout":
        stat_scout()
    elif page == "How to":
        st.write("hello")


if __name__ == "__main__":
    main()


