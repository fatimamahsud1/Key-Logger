import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

class MLAnalysis:
    def __init__(self):
        self.isolation_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
        self.scaler = StandardScaler()
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)

    def analyze_keystrokes(self, logged_keystrokes):
        keystrokes = np.array([(timestamp.timestamp(), ord(keystroke)) for timestamp, keystroke in logged_keystrokes])

        # Scale the features
        keystrokes_scaled = self.scaler.fit_transform(keystrokes)

        # Apply Isolation Forest
        self.isolation_forest.fit(keystrokes_scaled)

        # Apply DBSCAN for clustering
        clusters = self.dbscan.fit_predict(keystrokes_scaled)

        # Check if any keystrokes are considered outliers by Isolation Forest or belong to an outlier cluster by DBSCAN
        if np.any(self.isolation_forest.predict(keystrokes_scaled) == -1) or np.any(clusters == -1):
            return True
        else:
            return False
