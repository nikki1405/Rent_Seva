import pandas as pd
import numpy as np

# Generate sample data
n_samples = 1000
data = {
    'built_area_sqft': np.random.uniform(500, 3000, n_samples),
    'bhk': np.random.randint(1, 5, n_samples),
    'bathrooms': np.random.randint(1, 4, n_samples),
    'lift': np.random.randint(0, 2, n_samples),
    'air_conditioner': np.random.randint(0, 2, n_samples),
    'parking': np.random.randint(0, 2, n_samples),
    'gym': np.random.randint(0, 2, n_samples),
    'security': np.random.randint(0, 2, n_samples),
    'water_supply': np.random.randint(0, 2, n_samples),
}

# Generate rent values (example formula)
rent = (data['built_area_sqft'] * 50 + 
        data['bhk'] * 5000 + 
        data['bathrooms'] * 2000 + 
        np.random.normal(0, 1000, n_samples))

data['rent'] = rent

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('rent_data.csv', index=False)