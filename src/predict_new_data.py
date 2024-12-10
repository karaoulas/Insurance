from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import data_loader

def predict_new_data(model, new_data):
    """
    Κάνει πρόβλεψη για νέα δεδομένα.

    Args:
        model: Το εκπαιδευμένο μοντέλο.
        new_data (pd.DataFrame): Τα νέα δεδομένα για πρόβλεψη.

    Returns:
        predictions: Οι προβλέψεις του μοντέλου.
    """
    predictions = model.predict(new_data)
    return predictions

# Παράδειγμα πρόβλεψης
new_data = X_test.iloc[:5]  # Χρησιμοποιούμε 5 δείγματα από το test set
predictions = predict_new_data(model, new_data)
print("Predictions for new data:")
print(predictions)
