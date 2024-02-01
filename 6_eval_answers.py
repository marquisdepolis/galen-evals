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
    # One-hot encode the "Category" column
    category_dummies = pd.get_dummies(df['Category'])
    # Merge with the original dataframe
    df_processed = pd.concat([df.drop('Category', axis=1), category_dummies], axis=1)
    return df_processed

def cluster_models(df, n_clusters=3):
    # Assuming 'Model' is the identifier and not a feature for clustering
    features = df.drop('Model', axis=1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(features)
    
    # Add cluster labels to the dataframe
    df['Cluster'] = kmeans.labels_
    
    return df, kmeans

def integrate_ratings_with_data(df, ratings_data):
    # This is a placeholder function. You'll need to customize it based on how ratings relate to your data.
    # Assume ratings_data is a DataFrame with a structure that can be directly merged with df.
    df_with_ratings = pd.merge(df, ratings_data, on="SomeCommonIdentifier", how="left")
    return df_with_ratings

def visualize_clusters(df):
    # This is a simplified visualization; adjust according to your dataset's specifics
    plt.scatter(df.index, df['Cluster'])
    plt.xlabel('Model Index')
    plt.ylabel('Cluster')
    plt.title('Model Clustering')
    plt.show()

def visualize_clusters_with_pca(df):
    pca = PCA(n_components=2)
    features = df[['Feature1', 'Feature2', 'Feature3']]  # Adjust accordingly
    principal_components = pca.fit_transform(features)
    plt.scatter(principal_components[:, 0], principal_components[:, 1], c=df['Cluster'])
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Model Clusters after PCA')
    plt.show()

def main():
    # Load and preprocess the data
    file_path = config.combined_file_path
    df = read_data(file_path)
    df_processed = preprocess_data(df)
    
    # Collect ratings directly related to the data loaded
    ratings_data = collect_ratings(df)
    save_ratings(ratings_data, 'files/ratings.xlsx')
    
    # Integrate ratings with your data
    # Ensure ratings_data is in a format that matches the df_processed for a successful merge
    df_with_ratings = integrate_ratings_with_data(df_processed, pd.DataFrame(ratings_data))
    
    # Perform clustering on the integrated dataset
    df_clustered, _ = cluster_models(df_with_ratings)
    
    # Visualize the clusters, potentially using PCA for a more insightful visualization
    visualize_clusters_with_pca(df_clustered)

if __name__ == "__main__":
    main()
