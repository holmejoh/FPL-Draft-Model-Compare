from constants import Constants
import requests
import pandas as pd


class Data:
    _columns_to_use = ['web_name', 'first_name', 'second_name', 'minutes', 'element_type',
                       'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
                       'expected_goals', 'expected_assists', 'expected_goals_conceded',
                       'expected_goal_involvements',
                       'threat', 'creativity', 'influence', 'ict_index',
                       'total_points', 'bps']

    _element_type_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'ATT'}

    @staticmethod
    def get_df_w_model(data, pos_models):
        data['model_score'] = 0.0
        for pos in ['ATT', 'MID', 'DEF', 'GK']:
            pos_model = pos_models[pos]

            for key, value in pos_model.items():
                data.loc[data['element_type'] == pos, ['model_score']] = data.loc[data['element_type'] == pos][
                                                                             'model_score'] + \
                                                                         data.loc[data['element_type'] == pos][
                                                                             key] * value
        return data

    @staticmethod
    def get_current_players_data():
        return requests.get(Constants.PLAYERS_URL).json()

    def read_data(self, file_name, minutes_cutoff):
        raw_data = pd.read_csv(file_name)
        df = pd.DataFrame(raw_data)
        # filter by columns of interest
        df = df[self._columns_to_use]
        # add per 90 columns
        df['goals_per_90'] = df['goals_scored'] / (df['minutes'] / 90)
        df['assists_per_90'] = df['assists'] / (df['minutes'] / 90)
        df['goal_involvements_per_90'] = (df['goals_scored'] + df['assists']) / (df['minutes'] / 90)
        df['points_per_90'] = df['total_points'] / (df['minutes'] / 90)
        df['expected_goals_per_90'] = df['expected_goals'] / (df['minutes'] / 90)
        df['expected_assists_per_90'] = df['expected_assists'] / (df['minutes'] / 90)
        df['expected_goal_involvements_per_90'] = df['expected_assists_per_90'] + df['expected_goals_per_90']
        df['expected_goals_conceded_per_90'] = df['expected_goals_conceded'] / (df['minutes'] / 90)
        df['bps_per_90'] = df['bps'] / (df['minutes'] / 90)
        df['threat_per_90'] = df['threat'] / (df['minutes'] / 90)
        df['influence_per_90'] = df['influence'] / (df['minutes'] / 90)
        df['creativity_per_90'] = df['creativity'] / (df['minutes'] / 90)
        df['ict_per_90'] = df['ict_index'] / (df['minutes'] / 90)
        df['percent_minutes'] = df['minutes'] / (90 * 38)
        # filter by minutes played
        df = df[df['minutes'] > minutes_cutoff]
        df = df.replace({'element_type': self._element_type_map})
        return df

    def format_players_df(self, df, minutes_cutoff):
        df = pd.DataFrame(df)
        df = df[self._columns_to_use]
        df['expected_goals'] = df['expected_goals'].astype('float')
        df['expected_assists'] = df['expected_assists'].astype('float')
        df['expected_goals_conceded'] = df['expected_goals_conceded'].astype('float')
        df['threat'] = df['threat'].astype('float')
        df['creativity'] = df['creativity'].astype('float')
        df['influence'] = df['influence'].astype('float')
        df['ict_index'] = df['ict_index'].astype('float')
        df['bps'] = df['bps'].astype('float')

        # add per 90 columns
        df['goals_per_90'] = df['goals_scored'] / (df['minutes'] / 90)
        df['assists_per_90'] = df['assists'] / (df['minutes'] / 90)
        df['goal_involvements_per_90'] = (df['goals_scored'] + df['assists']) / (df['minutes'] / 90)
        df['points_per_90'] = df['total_points'] / (df['minutes'] / 90)
        df['expected_goals_per_90'] = df['expected_goals'] / (df['minutes'] / 90)
        df['expected_assists_per_90'] = df['expected_assists'] / (df['minutes'] / 90)
        df['expected_goals_conceded_per_90'] = df['expected_goals_conceded'] / (df['minutes'] / 90)
        df['expected_goal_involvements_per_90'] = df['expected_assists_per_90'] + df['expected_goals_per_90']
        df['bps_per_90'] = df['bps'] / (df['minutes'] / 90)
        df['threat_per_90'] = df['threat'] / (df['minutes'] / 90)
        df['influence_per_90'] = df['influence'] / (df['minutes'] / 90)
        df['creativity_per_90'] = df['creativity'] / (df['minutes'] / 90)
        df['ict_per_90'] = df['ict_index'] / (df['minutes'] / 90)
        df['percent_minutes'] = df['minutes'] / (90 * 38)
        df['minutes'] = df['minutes'].astype('float')
        # filter by minutes played
        df = df[df['minutes'] > minutes_cutoff]
        df = df.replace({'element_type': self._element_type_map})
        return df

    def get_historical_player_data(self):
        return self.read_data('data/22_23_players_raw.csv', 1000)
