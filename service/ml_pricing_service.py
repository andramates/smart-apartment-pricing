import numpy as np
import shap
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from service.geo_service import GeoService


class MLPricingService:

    def __init__(self):
        self.linear_model = LinearRegression()
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=6,
            random_state=42
        )

        self.best_model = None
        self.best_model_name = None
        self.scaler = None
        self.explainer = None
        self.metrics = {}

        self.feature_names = [
            "Distance",
            "Bedrooms",
            "Bathrooms",
            "Area",
            "Rating",
            "Amenities Count"
        ]

    def _extract_features(self, listing, target):
        distance = GeoService.haversine_distance(
            target.latitude,
            target.longitude,
            listing.latitude,
            listing.longitude
        )

        return [
            distance,
            listing.bedrooms,
            listing.bathrooms,
            listing.area_m2,
            listing.rating,
            len(listing.amenities)
        ]

    def train(self, ranked_listings, target, top_n=30):

        if len(ranked_listings) < 10:
            return False

        top_listings = ranked_listings[:top_n]

        X = []
        y = []

        for listing, score in top_listings:
            X.append(self._extract_features(listing, target))
            y.append(listing.price_per_night)

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        # ---- Scale for Linear Regression ----
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # ---- Linear Regression ----
        self.linear_model.fit(X_train_scaled, y_train)
        lr_pred = self.linear_model.predict(X_test_scaled)

        lr_r2 = r2_score(y_test, lr_pred)
        lr_mae = mean_absolute_error(y_test, lr_pred)

        # ---- Random Forest ----
        self.rf_model.fit(X_train, y_train)
        rf_pred = self.rf_model.predict(X_test)

        rf_r2 = r2_score(y_test, rf_pred)
        rf_mae = mean_absolute_error(y_test, rf_pred)

        # ---- Select best model ----
        if rf_r2 > lr_r2:
            self.best_model = self.rf_model
            self.best_model_name = "Random Forest"
            best_r2 = rf_r2
            best_mae = rf_mae

            # SHAP explainer pentru RF
            self.explainer = shap.TreeExplainer(self.rf_model)

        else:
            self.best_model = self.linear_model
            self.best_model_name = "Linear Regression"
            best_r2 = lr_r2
            best_mae = lr_mae

        self.metrics = {
            "linear_r2": lr_r2,
            "rf_r2": rf_r2,
            "best_model": self.best_model_name,
            "best_r2": best_r2,
            "best_mae": best_mae
        }

        return True

    def predict(self, target_listing, target):

        if self.best_model is None:
            return None

        features = np.array([self._extract_features(target_listing, target)])

        if self.best_model_name == "Linear Regression":
            features = self.scaler.transform(features)

        prediction = self.best_model.predict(features)[0]
        return prediction

    def explain(self, target_listing, target):

        if self.best_model_name != "Random Forest":
            return None

        features = np.array([self._extract_features(target_listing, target)])

        shap_values = self.explainer.shap_values(features)[0]

        explanation = dict(zip(self.feature_names, shap_values))

        return explanation

    def get_metrics(self):
        return self.metrics
