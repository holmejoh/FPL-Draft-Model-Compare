import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from utils.contstants import FEATURES


def preprocess_player_data(player_data, scaler):
    # Ensure features are in the correct order and format
    x = player_data[FEATURES].values.reshape(1, -1)  # Reshape to 2D array

    # Apply the same scaling as used in training
    x_scaled = scaler.transform(x)

    return x_scaled


def predict_total_points(model, scaler, player_data):
    # Preprocess the data point
    x_scaled = preprocess_player_data(player_data, scaler)

    # Predict using the trained model
    predicted_points = model.predict(x_scaled)

    return predicted_points[0]


class FPLModel:
    def __init__(self, position):
        self.position = position
        self.model = LinearRegression()
        self.scaler = MinMaxScaler()
        self.model_trained = False

    def _preprocess_data(self, data):
        # Filter data by position
        position_data = data[data['element_type'] == self.position]

        # Separate features and target
        x = position_data[FEATURES]
        y = position_data['total_points']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Feature scaling with Min-Max Normalization
        x_train_scaled = self.scaler.fit_transform(x_train)
        x_test_scaled = self.scaler.transform(x_test)

        # Saving Scaler
        joblib.dump(self.scaler, 'scaler.pkl')

        return x_train_scaled, x_test_scaled, y_train, y_test

    def _train_model(self, x_train, y_train):
        self.model_trained = True
        self.model.fit(x_train, y_train)

        # Saving Model
        joblib.dump(self.model, 'model.pkl')

    def _evaluate_model(self, x_test, y_test):
        y_pred = self.model.predict(x_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return mae, mse, r2

    def run(self, data):
        x_train, x_test, y_train, y_test = self._preprocess_data(data)
        self._train_model(x_train, y_train)
        return self._evaluate_model(x_test, y_test)

    def load_trained_model(self):
        if self.model_trained:
            return self.model
        else:
            raise Exception('Model not trained')
