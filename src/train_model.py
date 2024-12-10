from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import data_loader

def train_model(X_train, y_train, X_test, y_test):
    """
    Εκπαιδεύει ένα μοντέλο Random Forest και αξιολογεί την απόδοσή του.

    Args:
        X_train, y_train: Δεδομένα εκπαίδευσης.
        X_test, y_test: Δεδομένα αξιολόγησης.

    Returns:
        model: Το εκπαιδευμένο μοντέλο.
    """
    # Δημιουργία και εκπαίδευση του μοντέλου
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Πρόβλεψη
    y_pred = model.predict(X_test)

    # Αξιολόγηση
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")

    return model


# Εκπαίδευση του μοντέλου
model = train_model(X_train, y_train, X_test, y_test)
