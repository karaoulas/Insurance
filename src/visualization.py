import matplotlib.pyplot as plt
import seaborn as sns


def visualize_distribution(df):
    """
    Δημιουργεί γράφημα κατανομής των ποσών ασφάλισης.

    Args:
        df (pd.DataFrame): Τα δεδομένα σε DataFrame.
    """
    sns.histplot(df['Insurance_Amount'], bins=20, kde=True)  # Κατανομή με KDE
    plt.xlabel('Insurance Amount')
    plt.ylabel('Frequency')
    plt.title('Distribution of Insurance Amounts')
    plt.show()


# Οπτικοποίηση κατανομής
visualize_distribution(df)
