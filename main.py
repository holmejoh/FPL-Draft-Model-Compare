import pandas as pd
import joblib
from models.fpl_model import FPLModel, predict_total_points
from data import data
import argparse
import os


def handle_args():
    parser = argparse.ArgumentParser(description="FPL Draft Model comparison tool")
    parser.add_argument('--tool', type=str, required=True, help='Type of tool to use (comparison or prediction)')
    parser.add_argument('--position', type=str, required=True, help='Position type for prediction')
    parser.add_argument('--names', type=str, help='Player names for comparison')

    return parser.parse_args()


def create_players_dataframe():
    player_data = data.Data()
    ap23 = player_data.get_historical_player_data()
    ap23['year'] = '2023'
    ap24 = player_data.format_players_df(player_data.get_current_players_data()['elements'], 1000)
    ap24['year'] = '2024'
    return pd.concat([ap23, ap24])


def compare_players(model, scaler, df, position, names, year):
    players = df[(df['web_name'].isin(names)) & (df['year'] == year)]

    if len(players) > 2:
        raise Exception('Too many players to compare')

    player_1 = players.iloc[0]
    player_2 = players.iloc[1]

    # Predict total points for each player
    points_player1 = predict_total_points(model, scaler, player_1, position)
    points_player2 = predict_total_points(model, scaler, player_2, position)

    # Compare predictions
    if points_player1 > points_player2:
        print(f"Player 1 is expected to have a higher performance.")
    elif points_player1 < points_player2:
        print("Player 2 is expected to have a higher performance.")
    else:
        print("Both players are expected to have the same performance.")

    print(f"{players.iloc[0]['web_name']} predicted points: {points_player1}")
    print(f"{players.iloc[1]['web_name']} predicted points: {points_player2}")


def export_predictions_to_csv(model, scaler, players_data, output_file, position):
    # Create a DataFrame to store predictions
    predictions_df = pd.DataFrame(columns=['web_name', 'predicted_total_points'])

    # Iterate over player data and make predictions
    for idx, player_data in players_data.iterrows():
        # Predict total points for the player
        predicted_points = predict_total_points(model, scaler, player_data, position)

        # Append player name and predicted points to DataFrame
        predictions_df = pd.concat([predictions_df,
                                    pd.DataFrame([{'web_name': player_data['web_name'],
                                                   'predicted_total_points': predicted_points,
                                                   'total_points': player_data['total_points']}])], ignore_index=True)

    # Export DataFrame to CSV
    predictions_df.to_csv(output_file, index=False)


def main():
    args = handle_args()
    cum_df = create_players_dataframe()
    tool = args.tool
    position = args.position

    if tool is not None and position is not None:
        fpl_model = FPLModel(position=position)
        fpl_model.run(cum_df)
        saved_scaler = joblib.load('scaler.pkl')
        saved_model = joblib.load('model.pkl')

        if tool == 'comparison':
            names = args.names.split(' ')
            print(f"Comparing players: {names}")
            compare_players(saved_model, saved_scaler, cum_df, position, names, '2024')

        elif tool == 'prediction':
            position = args.position
            print(f"Predicting for position: {position}")
            export_predictions_to_csv(saved_model, saved_scaler,
                                      cum_df[(cum_df['year'] == '2024') & (cum_df['element_type'] == position)],
                                      f'/app/output/prediction_{position}.csv', position)
        else:
            raise Exception("Invalid tool type")


if __name__ == '__main__':
    main()
