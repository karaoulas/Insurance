import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def parse_contracts(file_path):
    """
    Διαβάζει και αναλύει δεδομένα από το XML αρχείο.
    Συνδυάζει δεδομένα από τα συμβόλαια, εκπτώσεις και καλύψεις.

    Args:
        file_path (str): Διαδρομή στο XML αρχείο.

    Returns:
        pd.DataFrame: DataFrame με όλα τα δεδομένα.
    """
    # Φορτώνουμε το XML αρχείο
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Λίστα για αποθήκευση δεδομένων
    all_data = []

    # Διασχίζουμε κάθε συμβόλαιο
    for contract in root.findall('./SYMBOLAIO'):
        # Βασικές πληροφορίες συμβολαίου
        SYMBOLAIO = {
            'ARITHMOS_SYMBOLAIOY': contract.get('ARITHMOS_SYMBOLAIOY', 'N/A'),
            'TYPOS_DIARKEIAS': int(contract.get('TYPOS_DIARKEIAS', 0)),
            'DIARKEIA': float(contract.get('DIARKEIA', 0)),
            'IPPOI': int(contract.get('IPPOI', 0)),
            'KYBIKA': int(contract.get('KYBIKA', 0)),
            'THESEIS': contract.get('THESEIS', 'N/A'),
            'MARKA': contract.get('MARKA', 'N/A'),
            'KAYSIMA': int(contract.get('KAYSIMA', 0)),
            'KATHARA': float(contract.get('KATHARA', 0)),
            'OLIKA': contract.get('OLIKA', 'N/A'),
        }

        # Επεξεργασία Εκπτώσεων
        for discount in contract.findall('./EKPTOSEIS_EPIBARYNSEIS/EKPTOSH_EPIBARYNSH'):
            EKPTOSEIS_EPIBARYNSEIS = {
                'KODIKOS_EKP_EPI': discount.get('KODIKOS_EKP_EPI', 'N/A'),
                'TYPOS_EKP_EPI': discount.get('TYPOS_EKP_EPI', 'N/A'),
                'POSOSTO_EKP_EPI': float(discount.get('POSOSTO_EKP_EPI', 0))
            }
            combined_discount_info = {**SYMBOLAIO, **EKPTOSEIS_EPIBARYNSEIS}
            all_data.append(combined_discount_info)

        # Επεξεργασία Καλύψεων
        for coverage in contract.findall('./KALYPSEIS/KALYPSH'):
            coverage_info = {
                'KODIKOS_KALYPSHS': coverage.get('KODIKOS_KALYPSHS', 'N/A'),
                'KEFALAIO_KALYPSHS': int(coverage.get('KEFALAIO_KALYPSHS', 0)),
                'PROMHTHEIA_KALYPSHS': float(coverage.get('PROMHTHEIA_KALYPSHS', 0)),
                'EKPTOSH_KALYPSHS': float(coverage.get('EKPTOSH_KALYPSHS', 0)),
                'KATHARA_KALYPSHS': float(coverage.get('KATHARA_KALYPSHS', 0)),
                'POSOSTO_PROMHTHEIAS_KALYPSHS': float(coverage.get('POSOSTO_PROMHTHEIAS_KALYPSHS', 0))
            }
            combined_coverage_info = {**SYMBOLAIO, **coverage_info}
            all_data.append(combined_coverage_info)

    # Δημιουργία DataFrame από τη λίστα
    all_data_df = pd.DataFrame(all_data)
    return all_data_df


# Παράδειγμα χρήσης
file_path = 'PARG65890.xml'  # Διαδρομή στο XML αρχείο
data_df = parse_contracts(file_path)

# Προβολή των πρώτων γραμμών
print(data_df)

# Αποθήκευση σε αρχείο CSV για μελλοντική χρήση
data_df.to_csv('insurance_data.csv', index=False)

def calculate_custom_statistics(df):
    """
    Υπολογίζει στατιστικά που ζητήθηκαν:
    1. Κωδικός κάλυψης που εμφανίζεται πιο συχνά.
    2. Μέσος αριθμός καλύψεων ανά συμβόλαιο.
    3. Συνολικό ποσό `PROMHTHEIA_KALYPSHS` για τον πιο συχνό κωδικό κάλυψης.

    Args:
        df (pd.DataFrame): Το DataFrame με τα δεδομένα.

    Returns:
        dict: Τα υπολογισμένα στατιστικά.
    """
    # 1. Κωδικός κάλυψης που εμφανίζεται στα περισσότερα συμβόλαια
    most_frequent_coverage = df['KODIKOS_KALYPSHS'].value_counts().idxmax()

    # 2. Μέσος αριθμός καλύψεων ανά συμβόλαιο
    coverages_per_contract = df.groupby('ARITHMOS_SYMBOLAIOY')['KODIKOS_KALYPSHS'].count()
    avg_coverages_per_contract = coverages_per_contract.mean()

    # 3. Συνολικό ποσό προμήθειας για τον πιο συχνό κωδικό κάλυψης
    most_frequent_coverage_data = df[df['KODIKOS_KALYPSHS'] == most_frequent_coverage]
    total_commission_most_frequent = most_frequent_coverage_data['PROMHTHEIA_KALYPSHS'].sum()

    # Δημιουργία αποτελεσμάτων
    stats = {
        "Most Frequent Coverage Code": most_frequent_coverage,
        "Average Coverages Per Contract": avg_coverages_per_contract,
        "Total Commission for Most Frequent Coverage": total_commission_most_frequent,
    }

    return stats


# Παράδειγμα χρήσης
statistics = calculate_custom_statistics(data_df)
#print("Statistics:")
#for key, value in statistics.items():
    #print(f"{key}: {value}")


def plot_coverage_frequency(df):
    """
    Δημιουργεί ραβδόγραμμα για τη συχνότητα των κωδικών καλύψεων.

    Args:
        df (pd.DataFrame): Το DataFrame με τα δεδομένα.
    """
    coverage_counts = df['KODIKOS_KALYPSHS'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=coverage_counts.index, y=coverage_counts.values, palette="viridis")
    plt.title("Frequency of Coverage Codes")
    plt.xlabel("Coverage Code")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.show()

# Παράδειγμα χρήσης
#plot_coverage_frequency(data_df)


def plot_total_commission_per_coverage(df):
    """
    Δημιουργεί ραβδόγραμμα για το συνολικό ποσό προμήθειας ανά κωδικό κάλυψης.

    Args:
        df (pd.DataFrame): Το DataFrame με τα δεδομένα.
    """
    total_commission = df.groupby('KODIKOS_KALYPSHS')['PROMHTHEIA_KALYPSHS'].sum()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=total_commission.index, y=total_commission.values, palette="coolwarm")
    plt.title("Total Commission per Coverage Code")
    plt.xlabel("Coverage Code")
    plt.ylabel("Total Commission")
    plt.xticks(rotation=45)
    plt.show()

# Παράδειγμα χρήσης
#plot_total_commission_per_coverage(data_df)


def plot_coverages_per_contract(df):
    """
    Δημιουργεί ιστόγραμμα για τον αριθμό καλύψεων ανά συμβόλαιο.

    Args:
        df (pd.DataFrame): Το DataFrame με τα δεδομένα.
    """
    coverages_per_contract = df.groupby('ARITHMOS_SYMBOLAIOY')['KODIKOS_KALYPSHS'].count()
    plt.figure(figsize=(10, 6))
    sns.histplot(coverages_per_contract, bins=10, kde=False, color="skyblue")
    plt.title("Number of Coverages per Contract")
    plt.xlabel("Number of Coverages")
    plt.ylabel("Frequency")
    plt.show()

# Παράδειγμα χρήσης
#plot_coverages_per_contract(data_df)
