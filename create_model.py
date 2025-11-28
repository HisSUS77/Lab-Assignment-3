"""
Create a sample trained model for CYBER-DEF25 Challenge
This creates a simple Random Forest classifier as a placeholder
"""

import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Create a sample Random Forest model
# In production, this would be your actual trained model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

# Fit with dummy data (10 features)
# In production, this would be trained on real malware detection data
X_dummy = np.random.rand(100, 10)
y_dummy = np.random.randint(0, 2, 100)
model.fit(X_dummy, y_dummy)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Sample model created and saved as model.pkl")
print(f"Model type: {type(model)}")
print(f"Number of features: 10")
print(f"Classes: {model.classes_}")
