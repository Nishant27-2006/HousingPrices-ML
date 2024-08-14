import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

def preprocess_chunk(chunk_path):
    # Load the chunk
    housing_chunk = pd.read_excel(chunk_path)
    
    # Data Cleaning: Handle missing values only in numeric columns
    numeric_cols = housing_chunk.select_dtypes(include=['float64', 'int64']).columns
    housing_chunk_filled = housing_chunk.copy()
    housing_chunk_filled[numeric_cols] = housing_chunk[numeric_cols].fillna(housing_chunk[numeric_cols].median())
    
    # Data Normalization: Z-score normalization
    scaler_standard = StandardScaler()
    time_series_columns = housing_chunk_filled.columns[9:]  # Assuming time-series data starts from the 10th column
    housing_chunk_standardized = housing_chunk_filled.copy()
    housing_chunk_standardized[time_series_columns] = scaler_standard.fit_transform(housing_chunk_filled[time_series_columns])
    
    # Dimensionality Reduction: Apply PCA
    pca = PCA(n_components=5)  # Example: reducing to 5 principal components
    housing_chunk_pca = pca.fit_transform(housing_chunk_standardized[time_series_columns])
    
    # Convert PCA results back to DataFrame
    housing_chunk_pca_df = pd.DataFrame(housing_chunk_pca, columns=[f'PC{i+1}' for i in range(housing_chunk_pca.shape[1])])
    
    # Combine with original non-time-series data
    housing_chunk_final = pd.concat([housing_chunk_filled.iloc[:, :9], housing_chunk_pca_df], axis=1)
    
    return housing_chunk_final

# Example: Process a chunk
processed_chunk = preprocess_chunk('housing_data_chunk_10.xlsx')
processed_chunk.to_excel('processed_housing_data_chunk_10.xlsx', index=False)
