from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import data_loader


def prepare_data(df):
    """
    Προετοιμάζει τα δεδομένα για μηχανικ
     μάθηση.

    Args:
        df (pd.DataFrame): Το DataFrame με τα δεδομένα.

    Returns:
        X, y: Χαρακτηριστικά και στόχοι για το μοντέλο.
    """
    # Επιλογή χαρακτηριστικών (features)
    features = ['KODIKOS_KALYPSHS', 'TYPOS_DIARKEIAS', 'KAYSIMA', 'KYBIKA', 'THESEIS']
    target = 'PROMHTHEIA_KALYPSHS'

    # Επεξεργασία κατηγορηματικών δεδομένων (Label Encoding)
    le = LabelEncoder()
    for col in ['KODIKOS_KALYPSHS', 'THESEIS']:
        df[col] = le.fit_transform(df[col])

    # Επιλογή χαρακτηριστικών και στόχου
    X = df[features]
    y = df[target]

    return X, y


# Προετοιμασία δεδομένων
X, y = prepare_data(data_df)

# Διαχωρισμός σε train και test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
