import streamlit as st
import pandas as pd
import csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def read_csv_to_dataframe(filename):
    data = []
    with open(filename, 'r', encoding='latin-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return pd.DataFrame(data)

def search_by_name(df, name):
    if name:
        return df[df['Name'].str.contains(name, case=False, na=False)]
    return df

def batter_data():
    batter_filename = 'batter-data.csv'
    batter_df = read_csv_to_dataframe(batter_filename)

    # Search feature
    search_name = st.text_input("Search by batter name:")
    st.write("Search Results:")

    # Apply search to the original DataFrame
    search_result = search_by_name(batter_df, search_name)

    # Display the original DataFrame
    st.write("Batter DataFrame:")
    st.dataframe(search_result, width=1000)  # Adjust the width as needed

def pitcher_data():
    pitcher_filename = 'pitcher-data.csv'
    pitcher_df = read_csv_to_dataframe(pitcher_filename)

    # Search feature
    search_name = st.text_input("Search by pitcher name:")
    st.write("Search Results:")

    # Apply search to the original DataFrame
    search_result = search_by_name(pitcher_df, search_name)

    # Display the original DataFrame
    st.write("Pitcher DataFrame:")
    st.dataframe(search_result, width=1000)  # Adjust the width as needed

def draft_help():
    st.write("Hello World! This is the Draft Help page.")

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

    # Display the selected players with all their stats
    st.write("Selected Players:")
    selected_df = pd.DataFrame()
    for player in st.session_state.selected_players:
        player_info = st.session_state.batter_df[st.session_state.batter_df['Name'] == player]
        if player_info.empty:
            player_info = st.session_state.pitcher_df[st.session_state.pitcher_df['Name'] == player]

        # Combine player info into a single DataFrame
        selected_df = pd.concat([selected_df, player_info], axis=0)

    # Display the combined DataFrame with player on the left and stats on the right
    st.write(selected_df.set_index('Name'))

    # Perform linear regression (example)
    st.write("Performing Linear Regression (Example):")
    X = selected_df[['PA', 'HR', 'R', 'RBI', 'SB']]
    y = selected_df['WAR']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    st.write(f"Mean Squared Error: {mse}")

def main():
    st.title("Baseball Player Stats")

    # Add radio buttons for navigation
    page = st.sidebar.radio("Navigation", ["Player Data", "Draft Help"])

    # Search feature for both data sets
    if page == "Player Data":
        batter_data()
        pitcher_data()
    elif page == "Draft Help":
        draft_help()

if __name__ == "__main__":
    main()

