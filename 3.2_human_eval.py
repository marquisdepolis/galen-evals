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
        print(f"\nModel: {row['Model']} | Question: {row['Question']}")
        question_ratings = {'Model': row['Model'], 'Question': row['Question']}
        for i in range(1, 4):
            while True:
                try:
                    rating = int(input(f"Rate Answer {i} (1-5): {row[f'Response{i}']} "))
                    if 1 <= rating <= 5:
                        question_ratings[f'Response{i}_Rating'] = rating
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")
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
    
    # Merge with the original dataframe, excluding 'Final Analysis Response' and 'Category' from vectorization
    df_processed = pd.concat([df.drop(['Final Analysis Response', 'Category'], axis=1), tfidf_df, category_dummies], axis=1)
    
    return df_processed

def cluster_models(df, n_clusters=3):
    # Drop non-feature columns, including identifiers 'Model' and 'Question'
    non_feature_cols = ['Model', 'Question', 'Response1', 'Response2', 'Response3', 'Perturbed Question', 'Perturbed Response', 'Final Analysis Question']
    features = df.drop(non_feature_cols, axis=1, errors='ignore')
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(features)
    df['Cluster'] = kmeans.labels_
    
    return df, kmeans

def integrate_ratings_with_data(df, ratings_df):
    # Merge ratings with your data on 'Model' and 'Question'
    df_with_ratings = pd.merge(df, ratings_df, on=['Model', 'Question'], how='left')
    return df_with_ratings

def visualize_clusters(df):
    plt.scatter(df.index, df['Cluster'])
    plt.xlabel('Index')
    plt.ylabel('Cluster')
    plt.title('Model Clustering')
    plt.show()

def visualize_clusters_with_pca(df, feature_cols):
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df[feature_cols])
    
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
    ratings_data = collect_ratings(df)
    
    # Save the ratings DataFrame to an Excel file
    save_ratings(pd.DataFrame(ratings_data), 'files/ratings.xlsx')

    # Preprocess the data to include TF-IDF features and one-hot encoded categories
    df_processed = preprocess_data(df)
    
    # Integrate ratings with the preprocessed data using 'Model' and 'Question' as keys
    df_with_ratings = pd.merge(df_processed, pd.DataFrame(ratings_data), on=['Model', 'Question'], how='left')
    
    # Extract numeric columns for clustering (from TF-IDF and one-hot encoding)
    numeric_feature_cols = df_with_ratings.select_dtypes(include=['float64', 'int']).columns.tolist()
    
    # Perform clustering on the integrated dataset
    df_clustered, kmeans = cluster_models(df_with_ratings[numeric_feature_cols])
    
    # Visualize the clusters
    visualize_clusters(df_clustered)
    
    # Visualize the clusters with PCA
    visualize_clusters_with_pca(df_clustered, numeric_feature_cols)

if __name__ == "__main__":
    main()
