import numpy as np
from sklearn.preprocessing import MinMaxScaler




class FPLModel:
    att_coeffs = {}
    mid_coeffs = {}
    def_coeffs = {}
    gk_coeffs = {}

    def __init__(self, csv_data):
        self.att_coeffs = create_model_by_pos(csv_data, 'ATT')
        self.mid_coeffs = create_model_by_pos(csv_data, 'MID')
        self.def_coeffs = create_model_by_pos(csv_data, 'DEF')
        self.gk_coeffs = create_model_by_pos(csv_data, 'GK')


def get_by_pos(df, pos):
    return df[df['element_type'] == pos]


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
    model_var_dict = {'ATT': ['expected_goal_involvements_per_90', 'expected_goals_per_90',
                              'expected_assists_per_90', 'bonus_per_90'],
                      'MID': ['expected_goal_involvements_per_90', 'expected_goals_per_90',
                              'expected_assists_per_90', 'bonus_per_90'],
                      'DEF': ['expected_goal_involvements_per_90', 'expected_goals_per_90',
                              'expected_assists_per_90', 'expected_goals_conceded_per_90', 'bonus_per_90'],
                      'GK': ['expected_goals_conceded_per_90', 'bonus_per_90']}

    return create_model_coeffs(data, pos, model_var_dict[pos])
