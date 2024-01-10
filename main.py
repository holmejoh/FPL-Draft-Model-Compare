import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests, json

columns_to_use = ['web_name', 'first_name', 'second_name', 'minutes', 'element_type',
                  'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
                  'expected_goals', 'expected_assists', 'expected_goals_conceded',
                  'expected_goal_involvements',
                  'threat', 'creativity', 'influence', 'ict_index',
                  'total_points', 'bps']

element_type_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'ATT'}


def read_data(file_name, minutes_cutoff):
    raw_data = pd.read_csv(file_name)
    df = pd.DataFrame(raw_data)
    # filter by columns of interest
    df = df[columns_to_use]
    # add per 90 columns
    df['goals_per_90'] = df['goals_scored'] / (df['minutes'] / 90)
    df['assists_per_90'] = df['assists'] / (df['minutes'] / 90)
    df['goal_involvements_per_90'] = (df['goals_scored'] + df['assists']) / (df['minutes'] / 90)
    df['points_per_90'] = df['total_points'] / (df['minutes'] / 90)
    df['expected_goals_per_90'] = df['expected_goals'] / (df['minutes'] / 90)
    df['expected_assists_per_90'] = df['expected_assists'] / (df['minutes'] / 90)
    df['expected_goal_involvements_per_90'] = df['expected_assists_per_90'] + df['expected_goals_per_90']
    df['expected_goals_conceded_per_90'] = df['expected_goals_conceded'] / (df['minutes'] / 90)
    df['bonus_per_90'] = df['bps'] / (df['minutes'] / 90)
    df['threat_per_90'] = df['threat'] / (df['minutes'] / 90)
    df['influence_per_90'] = df['influence'] / (df['minutes'] / 90)
    df['creativity_per_90'] = df['creativity'] / (df['minutes'] / 90)
    df['ict_per_90'] = df['ict_index'] / (df['minutes'] / 90)
    df['percent_minutes'] = df['minutes'] / (90 * 38)
    # filter by minutes played
    df = df[df['minutes'] > minutes_cutoff]
    df = df.replace({'element_type': element_type_map})
    return df


def format_players_df(df, minutes_cutoff):
    df = df[columns_to_use]
    df['expected_goals'] = df['expected_goals'].astype('float')
    df['expected_assists'] = df['expected_assists'].astype('float')
    df['expected_goals_conceded'] = df['expected_goals_conceded'].astype('float')
    df['threat'] = df['threat'].astype('float')
    df['creativity'] = df['creativity'].astype('float')
    df['influence'] = df['influence'].astype('float')
    df['ict_index'] = df['ict_index'].astype('float')

    # add per 90 columns
    df['goals_per_90'] = df['goals_scored'] / (df['minutes'] / 90)
    df['assists_per_90'] = df['assists'] / (df['minutes'] / 90)
    df['goal_involvements_per_90'] = (df['goals_scored'] + df['assists']) / (df['minutes'] / 90)
    df['points_per_90'] = df['total_points'] / (df['minutes'] / 90)
    df['expected_goals_per_90'] = df['expected_goals'] / (df['minutes'] / 90)
    df['expected_assists_per_90'] = df['expected_assists'] / (df['minutes'] / 90)
    df['expected_goals_conceded_per_90'] = df['expected_goals_conceded'] / (df['minutes'] / 90)
    df['expected_goal_involvements_per_90'] = df['expected_assists_per_90'] + df['expected_goals_per_90']
    df['bonus_per_90'] = df['bps'] / (df['minutes'] / 90)
    df['threat_per_90'] = df['threat'] / (df['minutes'] / 90)
    df['influence_per_90'] = df['influence'] / (df['minutes'] / 90)
    df['creativity_per_90'] = df['creativity'] / (df['minutes'] / 90)
    df['ict_per_90'] = df['ict_index'] / (df['minutes'] / 90)
    df['percent_minutes'] = df['minutes'] / (90 * 38)
    df['minutes'] = df['minutes'].astype('float')
    # filter by minutes played
    df = df[df['minutes'] > minutes_cutoff]
    df = df.replace({'element_type': element_type_map})
    return df


def get_by_pos(df, pos):
    return df[df['element_type'] == pos]


# used for initial exploration
def create_scatter_plot_by_pos(pos, data, column_x, column_y):
    position_data = get_by_pos(data, pos)
    plt.scatter(position_data[column_x], position_data[column_y])
    r = np.corrcoef(position_data[column_x], position_data[column_y])
    print(f'r: {r[0, 1]}')
    plt.xlabel(column_x)
    plt.ylabel(column_y)
    plt.title(f'{column_x} vs {column_y}')
    plt.show()
    plt.clf()


def create_model_coeffs(data, pos, columns):
    column_coeffs = {}
    column_weights = {}
    columns_sum = 0
    pos_data = get_by_pos(data, pos)
    for column in columns:
        r2 = np.corrcoef(pos_data[column], pos_data['points_per_90'])[0, 1] ** 2
        column_coeffs[column] = r2
        columns_sum += r2

    for key, value in column_coeffs.items():
        column_weights[key] = value
    return column_weights


def create_model_by_pos(data, pos):
    column_y = 'total_points'
    model_var_dict = {'ATT': ['bonus_per_90', 'expected_goal_involvements_per_90', 'expected_goals_per_90',
                              'expected_assists_per_90'],
                      'MID': ['bonus_per_90', 'expected_goal_involvements_per_90', 'expected_goals_per_90',
                              'expected_assists_per_90'],
                      'DEF': ['bonus_per_90', 'expected_goal_involvements_per_90', 'expected_goals_per_90',
                              'expected_assists_per_90', 'expected_goals_conceded_per_90'],
                      'GK': ['bonus_per_90', 'expected_goals_conceded_per_90']}

    return create_model_coeffs(data, pos, model_var_dict[pos])


def get_df_w_model(data, pos_models):
    data['model_score'] = 0
    for pos in ['ATT', 'MID', 'DEF', 'GK']:
        pos_model = pos_models[pos]
        for key, value in pos_model.items():
            data.loc[data['element_type'] == pos, ['model_score']] = data.loc[data['element_type'] == pos][
                                                                         'model_score'] + \
                                                                     data.loc[data['element_type'] == pos][key] * value
    data['model_score_per_minute'] = data['model_score'] * data['percent_minutes']
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ap23 = read_data('22_23_players_raw.csv', 1000)
    print(create_model_by_pos(ap23, 'ATT'))
    print(create_model_by_pos(ap23, 'MID'))
    print(create_model_by_pos(ap23, 'DEF'))
    print(create_model_by_pos(ap23, 'GK'))
    pos_models = {'ATT': create_model_by_pos(ap23, 'ATT'),
                  'MID': create_model_by_pos(ap23, 'MID'),
                  'DEF': create_model_by_pos(ap23, 'DEF'),
                  'GK': create_model_by_pos(ap23, 'GK')}
    ap_model = get_df_w_model(ap23, pos_models)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
