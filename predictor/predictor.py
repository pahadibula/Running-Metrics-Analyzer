from .models import RunningData
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

def get_data_from_db():
    data = RunningData.objects.all().values(
        'distance', 'minutes', 'seconds', 'pace', 'avg_bpm', 'stride', 'cadence'
    )
    if not data:
        raise ValueError("No data available in the database.")
    
    df = pd.DataFrame(list(data))
    return df

df = get_data_from_db()
# Features and target variables
X = df[['distance', 'minutes', 'seconds']]
y = df[['pace', 'avg_bpm', 'stride', 'cadence']]

# Normalize data
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Train the model
model = LinearRegression()
model.fit(X_scaled, y_scaled)

def predict_run(distance, minutes, seconds):
    input_data = scaler_X.transform(np.array([[distance, minutes, seconds]]))
    print("Transformed input data:", input_data)  # Debug
    predicted = model.predict(input_data)
    print("Predicted data:", predicted)  # Debug
    return scaler_y.inverse_transform(predicted)

def estimate_marathon_time(pace):
    marathon_distance = 42.195  # Full marathon in km
    time_minutes = marathon_distance * pace
    hours = int(time_minutes // 60)
    minutes = int(time_minutes % 60)
    result = f"{hours} hours and {minutes} minutes"
    
    print("Estimated Marathon Time:", result)  # Debug
    return result

def estimate_half_marathon_time(pace):
    # Convert pace from minutes per kilometer to total time for a full marathon
    full_marathon_time_minutes = 42.195 * pace
    
    # Apply Riegel Formula to estimate half marathon time
    half_marathon_time_minutes = full_marathon_time_minutes * (21.0975 / 42.195) ** 1.06
    
    hours1 = int(half_marathon_time_minutes // 60)
    minutes1 = int(half_marathon_time_minutes % 60)
    result1 = f"{hours1} hours and {minutes1} minutes"
    print("Estimated Half Marathon Time:", result1)  # Debug
    return result1
