# Create a master file to do analyses
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage
import seaborn as sns
from config import config
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

config.set_mode("default")
F_NAME = config.F_NAME

# Load the datasets
allresults_combined_df = pd.read_excel(f'files/{F_NAME}_allresults_combined.xlsx')
model_rankings_df = pd.read_excel(f'files/{F_NAME}_model_rankings.xlsx')
analysis_df_path = f'files/{F_NAME}_analysis.xlsx'

# Preliminary cleaning to ensure consistency in model names and question texts
# allresults_combined_df['Model'] = allresults_combined_df['Model'].str.lower().str.replace(' ', '').str.replace('-', '').str.replace('.', '')

# Remove "Question: " part and other preprocessing in model_rankings_df
model_rankings_df['Question'] = model_rankings_df['Question'].str.replace('question: ', '', case=False).str.split('|').str[0].str.strip()

# Reshape model_rankings_df to long format
model_rankings_long_df = pd.melt(model_rankings_df, id_vars=['Question', 'Reasoning', 'Category'], var_name='Model', value_name='Ranking')

# Clean 'Model' column to ensure consistency
model_rankings_long_df['Model'] = model_rankings_long_df['Model'].str.lower().replace({'falcon40b': 'falcon-40b', 'gpt35turbo1106': 'gpt-3.5-turbo-1106', 'mistral7b': 'mistral-7b', 'mixtralinstruct': 'mixtral-instruct', 'noushermes2': 'noushermes2', 'yi34b': 'yi-34b'})

# Merge the datasets
combined_data = pd.merge(allresults_combined_df, model_rankings_long_df, on=['Question', 'Model'], how='inner')

combined_data.to_excel(analysis_df_path, index=False)

# Now, onwards to analysis and charts
data = pd.read_excel(analysis_df_path)

# Basic statistical analysis on latency and ranking by Model
latency_stats = data.groupby('Model')['Latency'].describe()
ranking_stats = data.groupby('Model')['Ranking'].describe()

# Analysis by Type
type_analysis = data.groupby(['Type', 'Model']).agg({'Latency': 'mean', 'Ranking': 'mean'}).reset_index()

# Plotting Mean Latency by Model and Type
plt.figure(figsize=(14, 7))
sns.barplot(x='Model', y='Latency', hue='Type', data=type_analysis)
plt.title('Mean Latency by Model and Type')
plt.xticks(rotation=45)
plt.ylabel('Mean Latency (Seconds)')
plt.xlabel('Model')
plt.legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'charts/{F_NAME}_mean_latency_by_model_and_type.png')  # Save plot
# plt.show()

# Plotting Mean Ranking by Model and Type
plt.figure(figsize=(14, 7))
sns.barplot(x='Model', y='Ranking', hue='Type', data=type_analysis)
plt.title('Mean Ranking by Model and Type')
plt.xticks(rotation=45)
plt.ylabel('Mean Ranking')
plt.xlabel('Model')
plt.legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'charts/{F_NAME}_mean_ranking_by_model_and_type.png')  # Save plot
# plt.show()

# Category Performance Analysis
category_performance = data.groupby(['Category_x']).agg({'Latency': 'mean', 'Ranking': 'mean'}).sort_values(by='Ranking', ascending=True)

# Plotting Category Performance
plt.figure(figsize=(14, 7))
category_performance['Ranking'].plot(kind='barh', color='skyblue')
plt.title('Average Ranking by Category')
plt.xlabel('Average Ranking')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig(f'charts/{F_NAME}_average_ranking_by_category.png')  # Save plot
# plt.show()

# Latency Distribution Across Models
plt.figure(figsize=(14, 7))
sns.boxplot(x='Model', y='Latency', data=data)
plt.title('Latency Distribution Across Models')
plt.xticks(rotation=45)
plt.ylabel('Latency (Seconds)')
plt.xlabel('Model')
plt.tight_layout()
plt.savefig(f'charts/{F_NAME}_latency_distribution_across_models.png')  # Save plot
# plt.show()

# Create a scatter plot
plt.figure(figsize=(14, 7))
scatter = sns.scatterplot(data=data, x='Latency', y='Ranking', hue='Model', style='Model', s=100)
plt.title('Latency vs. Ranking Across Models')
plt.xlabel('Latency (in seconds)')
plt.ylabel('Ranking')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig(f'charts/{F_NAME}_latency_vs_ranking_across_models.png')
# plt.show()

# Correlation analysis between latency and ranking
correlation_analysis = data[['Latency', 'Ranking']].corr()

# Textual analysis of Reasoning using TF-IDF and Cosine Similarity
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Reasoning'])
cosine_similarities = cosine_similarity(tfidf_matrix)

# Average Cosine Similarity across all responses
average_cosine_similarity = np.mean(cosine_similarities)

# Assuming correlation_analysis is a Pandas DataFrame with the correlation values
sns.heatmap(correlation_analysis, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap of Correlation between Latency and Ranking')
plt.savefig(f'charts/{F_NAME}_latency_ranking_corr_heatmap.png')
# plt.show()

# Assuming cosine_similarities is a square matrix
sns.heatmap(cosine_similarities, cmap='YlGnBu')
plt.title('Heatmap of Cosine Similarities among Responses')
plt.savefig(f'charts/{F_NAME}_cosine_similarities_heatmap.png')
# plt.show()

# Generate the linkage matrix
Z = linkage(cosine_similarities, 'ward')

# Plot the dendrogram
plt.figure(figsize=(10, 5))
dendrogram(Z)
plt.title('Dendrogram for Hierarchical Clustering of Responses')
plt.xlabel('Response Index')
plt.ylabel('Distance')
plt.savefig(f'charts/{F_NAME}_dendrogram_clustering.png')
# plt.show()
