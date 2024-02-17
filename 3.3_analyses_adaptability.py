# Update adaptability excel and run analyses
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage
import seaborn as sns
from config import config

config.set_mode("default")
F_NAME = config.F_NAME

# Load the Excel files
galen_analysis_path = f'files/{F_NAME}_analysis.xlsx'
galen_analysis_adaptability_path = f'files/{F_NAME}_analysis_adaptability.xlsx'

# Read the Excel files into DataFrame
galen_analysis_df = pd.read_excel(galen_analysis_path)
galen_analysis_adaptability_df = pd.read_excel(galen_analysis_adaptability_path)

galen_analysis_df['Normalized_Question'] = galen_analysis_df['Question'].str.lower().str.strip()
galen_analysis_adaptability_df['Normalized_Question'] = galen_analysis_adaptability_df['Question'].str.lower().str.strip()

# Perform the merge again, this time including the normalized question for matching
refined_merge_df = pd.merge(
    galen_analysis_adaptability_df,
    galen_analysis_df[['Normalized_Question', 'Model', 'Type', 'Ranking']],
    on=['Normalized_Question', 'Model', 'Type'],
    how='left'
)

# Show the result of the refined merge to check the outcome
analysis_df_path = f'files/{F_NAME}_analysis_adaptability_combined.xlsx'
refined_merge_df.to_excel(analysis_df_path, index=False)

# Normalizing data for better comparison in the heatmap
# Min-Max scaling to get values between 0 and 1
heatmap_data = refined_merge_df[['Model', 'Rating_Single', 'Ranking']].set_index('Model')
heatmap_data_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())

# Plotting the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data_normalized, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Normalized Average Ranking and Rating Heatmap', fontsize=16)
plt.ylabel('Model')
plt.savefig(f'charts/{F_NAME}_rankvsrate_heatmap.png')

# Generating a CDF plot for model ratings to assess adaptability
plt.figure(figsize=(12, 8))
unique_models = refined_merge_df['Model'].unique()
for model in unique_models:
    # Selecting ratings for the current model
    model_ratings = refined_merge_df[refined_merge_df['Model'] == model]['Rating_Single']
    # Generating CDF values
    values, base = np.histogram(model_ratings, bins=40, density=True)
    cumulative = np.cumsum(values)
    # Plotting
    plt.plot(base[:-1], cumulative, label=model)

plt.title('CDF of Model Ratings for Adaptability', fontsize=16)
plt.xlabel('Rating', fontsize=14)
plt.ylabel('CDF', fontsize=14)
plt.legend(title='Model')
plt.grid(True)
# Adjusting the layout and subtitle position
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.figtext(0.5, 0.01, 'Models that reach higher CDF values at lower ratings are generally more adaptable, as a larger proportion of their responses are rated highly.', fontsize=10, ha='center')
plt.savefig(f'charts/{F_NAME}_rankvsrate_CDF.png')

# Assuming df is your DataFrame and it contains 'Rating_Single' and 'Ranking' columns
sns.jointplot(x='Rating_Single', y='Ranking', data=refined_merge_df, kind='reg', height=10)
plt.suptitle('Jointplot of Adaptability Rating vs. Ranking', fontsize=14, y=1.0)
plt.xlabel('Adaptability Rating', fontsize=11)
plt.ylabel('Ranking', fontsize=11)
correlation = refined_merge_df['Rating_Single'].corr(refined_merge_df['Ranking'])
subtitle = (f"Correlation coefficient between Adaptability Rating and Ranking: {correlation:.2f}")
plt.figtext(0.5, 0.01, subtitle, fontsize=9, ha='center')
plt.savefig(f'charts/{F_NAME}_ratevsrank_jointplot.png')

