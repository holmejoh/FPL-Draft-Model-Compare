import os

import pandas as pd
import joblib
from models.fpl_model import FPLModel, predict_total_points
from data import data


def compare_players(model, scaler, df, names, year):
    players = df[(df['web_name'].isin(names)) & (df['year'] == year)]

    if len(players) > 2:
        raise Exception('Too many players to compare')

    player_1 = players.iloc[0]
    player_2 = players.iloc[1]

    # Predict total points for each player
    points_player1 = predict_total_points(model, scaler, player_1)
    points_player2 = predict_total_points(model, scaler, player_2)

    # Compare predictions
    if points_player1 > points_player2:
        print(f"Player 1 is expected to have a higher performance.")
    elif points_player1 < points_player2:
        print("Player 2 is expected to have a higher performance.")
    else:
        print("Both players are expected to have the same performance.")

    print(f"{players.iloc[0]['web_name']} predicted points: {points_player1}")
    print(f"{players.iloc[1]['web_name']} predicted points: {points_player2}")


def export_predictions_to_csv(model, scaler, players_data, output_file):
    # Create a DataFrame to store predictions
    predictions_df = pd.DataFrame(columns=['web_name', 'predicted_total_points'])

    # Iterate over player data and make predictions
    for idx, player_data in players_data.iterrows():
        # Predict total points for the player
        predicted_points = predict_total_points(model, scaler, player_data)

        # Append player name and predicted points to DataFrame
        predictions_df = pd.concat([predictions_df,
                                    pd.DataFrame([{'web_name': player_data['web_name'],
                                                   'predicted_total_points': predicted_points,
                                                   'total_points': player_data['total_points']}])], ignore_index=True)

    # Export DataFrame to CSV
    predictions_df.to_csv(output_file, index=False)


if __name__ == '__main__':
    web_names = os.environ['NAMES'].split(' ')

    data = data.Data()
    ap23 = data.get_historical_player_data()
    ap23['year'] = '2023'
    ap24 = data.format_players_df(data.get_current_players_data()['elements'], 1000)
    ap24['year'] = '2024'
    cum_df = pd.concat([ap23, ap24])

    fpl_model = FPLModel('MID')
    fpl_model.run(cum_df)
    saved_scaler = joblib.load('scaler.pkl')
    saved_model = joblib.load('model.pkl')
    compare_players(saved_model, saved_scaler, cum_df, web_names, '2024')

    export_predictions_to_csv(saved_model, saved_scaler,
                              cum_df[(cum_df['year'] == '2024') & (cum_df['element_type'] == 'MID')],
                              'prediction.csv')
