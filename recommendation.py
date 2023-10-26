import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from user_search import features_by_name, features_by_link

# Constants
SIMILARITY_THRESHOLD = 0.3
NUM_RECOMMENDATIONS = 50

def compute_cosine_similarity(A, data_as_np_array):
    """
    Compute the cosine similarity between vector A and an array of vectors.

    Args:
        A (numpy.ndarray): The input vector A.
        data_as_np_array (numpy.ndarray): An array of vectors to compare with A.

    Returns:
        list: A list of cosine similarity values.
    """
    norm_A = np.linalg.norm(A)
    cos_similarity = []

    for B in data_as_np_array:
        cosine = np.dot(A, B) / (norm_A * np.linalg.norm(B))
        cos_similarity.append(cosine)

    return cos_similarity

def get_recommendations(df, ans):
    """
    Get song recommendations based on input features and cosine similarity.

    Args:
        df (pandas.DataFrame): The DataFrame containing song data.
        ans (list): A list of audio features representing the input song.

    Returns:
        pandas.DataFrame: A DataFrame containing recommended songs sorted by similarity.
    """
    result = df.loc[
        (df['danceability'] > round(ans[0] - SIMILARITY_THRESHOLD, 1)) &
        (df['danceability'] < round(ans[0] + SIMILARITY_THRESHOLD, 1)) &
        (df['energy'] > round(ans[1] - SIMILARITY_THRESHOLD, 1)) &
        (df['energy'] < round(ans[1] + SIMILARITY_THRESHOLD, 1)) &
        (df['speechiness'] > round(ans[2] - SIMILARITY_THRESHOLD, 1)) &
        (df['speechiness'] < round(ans[2] + SIMILARITY_THRESHOLD, 1)) &
        (df['acousticness'] > round(ans[3] - SIMILARITY_THRESHOLD, 1)) &
        (df['acousticness'] < round(ans[3] + SIMILARITY_THRESHOLD, 1)) &
        (df['instrumentalness'] > round(ans[4] - SIMILARITY_THRESHOLD, 1)) &
        (df['instrumentalness'] < round(ans[4] + SIMILARITY_THRESHOLD, 1)) &
        (df['valence'] > round(ans[5] - SIMILARITY_THRESHOLD, 1)) &
        (df['valence'] < round(ans[5] + SIMILARITY_THRESHOLD, 1)) &
        (df['tempo'] > round(ans[6] - SIMILARITY_THRESHOLD, 1)) &
        (df['tempo'] < round(ans[6] + SIMILARITY_THRESHOLD, 1))
    ]

    data_as_np_array = result[['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']].to_numpy()
    A = np.array(ans)
    cos_similarity = compute_cosine_similarity(A, data_as_np_array)

    result['Cosine_Similarity'] = cos_similarity
    sorted_df = result.sort_values(by='Cosine_Similarity', ascending=False)
    sorted_df = sorted_df[['track_name', 'track_id', 'Cosine_Similarity']]
    sorted_df = sorted_df.head(NUM_RECOMMENDATIONS)

    return sorted_df

def get_recommendation_by_link(link: str)-> pd.DataFrame:
    """
    Get song recommendations by a Spotify track link.

    Args:
        link (str): The Spotify track link.

    Returns:
        pandas.DataFrame: A DataFrame containing recommended songs sorted by similarity.
    """
    df = pd.read_csv(r'process_data\filtered_data.csv')
    ans = features_by_link(link)
    return get_recommendations(df, ans)

def get_recommendation_by_name(name: str)-> pd.DataFrame:
    """
    Get song recommendations by a song name.

    Args:
        name (str): The name of the song.

    Returns:
        pandas.DataFrame: A DataFrame containing recommended songs sorted by similarity.
    """
    df = pd.read_csv(r'process_data\filtered_data.csv')
    ans = features_by_name(name)
    return get_recommendations(df, ans)
