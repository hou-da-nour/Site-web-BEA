import pandas as pd

def clean_categories():
    # Lire le fichier CSV
    df = pd.read_csv('data/faqs_clean.csv')
    
    # Remplacer la catégorie erronée par "Sécurité"
    df.loc[df['Categorie'] == ' guidez le client vers le menu de réactivation."', 'Categorie'] = 'Sécurité'
    
    # Sauvegarder le fichier modifié
    df.to_csv('data/faqs_clean.csv', index=False)
    print('Modification effectuée avec succès')
    
    # Afficher les catégories uniques après modification
    print('\nCatégories uniques après modification:')
    print(sorted(df['Categorie'].unique().tolist()))

if __name__ == '__main__':
    clean_categories() 