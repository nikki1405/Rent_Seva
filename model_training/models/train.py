import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
import json
from datetime import datetime

VIZAG_LOCATIONS = {
    'MVP Colony': {'min': 8000, 'max': 15000, 'tier': 3},  # Premium area
    'Beach Road': {'min': 10000, 'max': 18000, 'tier': 3},  # Most premium area
    'Madhurawada': {'min': 7000, 'max': 14000, 'tier': 2},  # Growing IT hub
    'Gajuwaka': {'min': 5000, 'max': 10000, 'tier': 1},    # Industrial area
    'Pendurthi': {'min': 4000, 'max': 8000, 'tier': 1},    # Budget area
    'Seethammadhara': {'min': 8000, 'max': 15000, 'tier': 3}, # Premium residential
    'Rushikonda': {'min': 7000, 'max': 14000, 'tier': 2}   # Beach/IT area
}

def generate_synthetic_data(location, min_rent, max_rent, tier):
    n_samples = 20
    synthetic_data = []
    for _ in range(n_samples):
        bhk = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
        sqft_ranges = {1: (400, 800), 2: (600, 1200), 3: (800, 1500)}
        sqft_min, sqft_max = sqft_ranges[bhk]
        
        rent = np.random.uniform(min_rent * (bhk/2), min(max_rent, max_rent * (bhk/2)))
        sqft = np.random.uniform(sqft_min, sqft_max)
        
        synthetic_data.append({
            'location': location,
            'built_area_sqft': sqft,
            'bhk': bhk,
            'bathrooms': min(bhk, 3),
            'rent': rent,
            'lift': np.random.choice([0, 1], p=[0.3, 0.7]) if tier > 1 else np.random.choice([0, 1], p=[0.7, 0.3]),
            'air_conditioner': np.random.choice([0, 1], p=[0.2, 0.8]) if tier > 1 else np.random.choice([0, 1], p=[0.6, 0.4]),
            'parking': np.random.choice([0, 1], p=[0.2, 0.8]) if tier > 1 else np.random.choice([0, 1], p=[0.5, 0.5]),
            'gym': np.random.choice([0, 1], p=[0.8, 0.2]),
            'security': np.random.choice([0, 1], p=[0.2, 0.8]) if tier > 1 else np.random.choice([0, 1], p=[0.5, 0.5]),
            'water_supply': np.random.choice([0, 1], p=[0.1, 0.9])
        })
    return pd.DataFrame(synthetic_data)

def train_model(data_path):
    print("Loading and preparing data...")
    df = pd.read_csv(data_path)
    
    # Generate synthetic data for Vizag locations
    synthetic_dfs = []
    for loc, params in VIZAG_LOCATIONS.items():
        if len(df[df['location'] == loc]) < 10:
            print(f"Generating synthetic data for {loc}...")
            synthetic_df = generate_synthetic_data(
                loc, 
                params['min'], 
                params['max'], 
                params['tier']
            )
            synthetic_dfs.append(synthetic_df)
    
    if synthetic_dfs:
        df = pd.concat([df] + synthetic_dfs, ignore_index=True)
    
    # Clean data
    df = df[(df['rent'] >= 4000) & (df['rent'] <= 30000)]
    df = df[(df['built_area_sqft'] >= 400) & (df['built_area_sqft'] <= 2000)]
    df = df[df['bhk'].between(1, 3)]
    
    # Add engineered features
    df['price_per_sqft'] = df['rent'] / df['built_area_sqft']
    df['area_per_room'] = df['built_area_sqft'] / (df['bhk'] + 0.5 * df['bathrooms'])
    df['location_tier'] = df['location'].map({loc: params['tier'] for loc, params in VIZAG_LOCATIONS.items()}).fillna(1)
    
    # Create amenities score
    amenities = {
        'lift': 0.15,
        'air_conditioner': 0.30,
        'parking': 0.20,
        'gym': 0.05,
        'security': 0.15,
        'water_supply': 0.15
    }
    df['amenities_score'] = sum(df[amenity] * weight for amenity, weight in amenities.items())
    
    # Prepare features
    feature_cols = [
        'location', 'built_area_sqft', 'bhk', 'bathrooms',
        'lift', 'air_conditioner', 'parking', 'gym', 'security', 'water_supply',
        'area_per_room', 'amenities_score', 'location_tier'
    ]
    
    X = df[feature_cols]
    y = df['rent']
    
    # Encode location
    le = LabelEncoder()
    X['location'] = le.fit_transform(X['location'])
    
    # Split and scale data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
        stratify=pd.qcut(y, q=5, duplicates='drop').astype(str)
    )
    
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training model...")
    model = RandomForestRegressor(
        n_estimators=400,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=4,
        max_features='log2',
        n_jobs=-1,
        random_state=42,
        bootstrap=True,
        oob_score=True
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_pred = np.clip(y_pred, 4000, 30000)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    # Save results
    print("Saving model and evaluation...")
    model_dir = '../../rentsevabackend/predictor/ml_models'
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(model_dir, 'rent_predictor.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.joblib'))
    joblib.dump(le, os.path.join(model_dir, 'label_encoder.joblib'))
    
    evaluation = {
        'model_performance': {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2_score': float(r2)
        },
        'feature_importance': dict(zip(feature_cols, model.feature_importances_)),
        'location_stats': {
            loc: {
                'count': int(len(df[df['location'] == loc])),
                'median_rent': float(df[df['location'] == loc]['rent'].median()),
                'avg_rent': float(df[df['location'] == loc]['rent'].mean())
            }
            for loc in VIZAG_LOCATIONS.keys()
        }
    }
    
    with open(os.path.join(model_dir, 'model_evaluation.json'), 'w') as f:
        json.dump(evaluation, f, indent=4)
    
    print("\nModel Training Results:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"Root Mean Squared Error: {rmse:.2f}")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R² Score: {r2:.4f}")
    print("\nLocation Statistics:")
    for loc in VIZAG_LOCATIONS.keys():
        loc_data = df[df['location'] == loc]
        if len(loc_data) > 0:
            print(f"\n{loc}:")
            print(f"  Count: {len(loc_data)}")
            print(f"  Median Rent: ₹{loc_data['rent'].median():,.2f}")
            print(f"  Average Rent: ₹{loc_data['rent'].mean():,.2f}")

if __name__ == "__main__":
    data_path = "../data/rent_data.csv"
    train_model(data_path)