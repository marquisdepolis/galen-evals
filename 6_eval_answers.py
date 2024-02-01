from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from config import config
config.set_mode('dynamic')

def read_data(file_path):
    return pd.read_excel(file_path)

def collect_ratings(questions_df):
    ratings_data = []
    for index, row in questions_df.iterrows():
        print(f"\nQuestion: {row['Question']}")
        question_ratings = {}
        for i in range(1, 4):
            valid_rating = False
            while not valid_rating:
                try:
                    rating = int(input(f"Rate Answer {i} (1-5): {row[f'Answer{i}']} "))
                    if rating < 1 or rating > 5:
                        raise ValueError
                    valid_rating = True
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 5.")
            question_ratings[f'Answer{i}'] = rating
        ratings_data.append(question_ratings)
    return ratings_data

def save_ratings(ratings_data, file_path='ratings.xlsx'):
    ratings_df = pd.DataFrame(ratings_data)
    ratings_df.to_excel(file_path, index=False)
    print(f"Ratings saved to {file_path}")

def preprocess_data(df):
    # Handle text data
    vectorizer = TfidfVectorizer(max_features=100)  # Adjust max_features as needed
    tfidf_matrix = vectorizer.fit_transform(df['Final Analysis Response'])
    
    # Create a DataFrame with the TF-IDF features
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    
    # One-hot encode the "Category" column
    category_dummies = pd.get_dummies(df['Category'])
    
    # Merge with the original dataframe
    df_processed = pd.concat([df, tfidf_df, category_dummies], axis=1).drop(['Category', 'Final Analysis Response'], axis=1)
    
    return df_processed

def cluster_models(df, n_clusters=3):
    # Drop non-feature columns
    non_feature_cols = ['Model', 'Question', 'Response', 'Perturbed Question', 'Perturbed Response', 'Final Analysis Question']
    features = df.drop(non_feature_cols, axis=1, errors='ignore')  # errors='ignore' allows columns to be missing
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(features)
    df['Cluster'] = kmeans.labels_
    
    return df, kmeans

def integrate_ratings_with_data(df, ratings_data):
    # Assuming ratings_data is a DataFrame with the same order as df
    df_with_ratings = df.join(ratings_data)
    return df_with_ratings

def visualize_clusters(df):
    # This is a simplified visualization; adjust according to your dataset's specifics
    plt.scatter(df.index, df['Cluster'])
    plt.xlabel('Model Index')
    plt.ylabel('Cluster')
    plt.title('Model Clustering')
    plt.show()

def visualize_clusters_with_pca(df, features):
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df[features])
    
    plt.figure(figsize=(10, 8))
    plt.scatter(principal_components[:, 0], principal_components[:, 1], c=df['Cluster'])
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Model Clusters after PCA')
    plt.colorbar()
    plt.show()

def main():
    # Load and preprocess the data
    file_path = config.combined_file_path
    df = read_data(file_path)
    
    # Collect ratings directly related to the data loaded
    # Note: This will require manual input for each row in your dataframe
    ratings_data = collect_ratings(df)
    save_ratings(ratings_data, 'files/ratings.xlsx')

    # Preprocess the data after collecting ratings
    df_processed = preprocess_data(df)
    
    # Convert ratings_data to a DataFrame if it isn't already one
    ratings_df = pd.DataFrame(ratings_data)

    # Integrate ratings with your data
    # Ensure ratings_data is in a DataFrame with a structure that can be directly merged with df_processed
    df_with_ratings = integrate_ratings_with_data(df_processed, ratings_df)
    
    # Perform clustering on the integrated dataset
    df_clustered, kmeans = cluster_models(df_with_ratings)
    
    # Visualize the clusters
    visualize_clusters(df_clustered)
    
    # Visualize the clusters with PCA
    # Extract the features used for clustering (TF-IDF features)
    tfidf_feature_cols = [col for col in df_with_ratings.columns if col.startswith('feature_')]
    visualize_clusters_with_pca(df_clustered, tfidf_feature_cols)

if __name__ == "__main__":
    main()
