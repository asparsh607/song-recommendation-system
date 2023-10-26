import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
curr_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = curr_dir / ".env"
load_dotenv(envars)


# Replace these with your own credentials in the .env file from the Spotify Developer Dashboard
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Spotify API endpoints
AUDIO_FEATURES_ENDPOINT = '/v1/audio-features/'

# Initialize Spotipy with client credentials
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)



def features_by_name(song_name: str) -> list:
    """
    Extract audio features from a Spotify song given its name.

    Parameters:
    song_name (str): The name of the song for which audio features will be extracted.

    Returns:
    list: A list containing selected audio features from the song.
    """

    # Search for the song by name using Spotify API (sp)
    audio_features_data = sp.search(q=f"{song_name}", type='track')

    # Extract the track ID of a specific result (in this case, the 4th result)
    track_id = audio_features_data['tracks']['items'][3]['id']

    # Request audio features for the specified track ID using Spotify API (sp)
    audio_features_data = sp.audio_features(track_id)

    if audio_features_data:
        # Get the first (and only) item from the audio_features_data list
        data = audio_features_data[0]

        # Convert the audio features data into a DataFrame using a function called response_to_df
        df = response_to_df(data)

        # Convert the DataFrame to a NumPy array
        arr_numpy = df.to_numpy()

        # Extract specific audio features from the NumPy array
        # You can modify this list based on the features you want to extract
        features_list = arr_numpy[0:1]

        # Return the selected audio features as a list
        return [
            features_list[0][0],  # Feature 1
            features_list[0][1],  # Feature 2
            features_list[0][5],  # Feature 6
            features_list[0][6],  # Feature 7
            features_list[0][7],  # Feature 8
            features_list[0][9],  # Feature 10
            features_list[0][10]  # Feature 11
        ]

    # Return an empty list if no audio features were found or if the search results were empty
    return []


def features_by_link(song_link: str) -> list:
    """
    Extract audio features from a Spotify song given its song link.

    Parameters:
    song_link (str): The Spotify song link from which audio features will be extracted.

    Returns:
    list: A list containing selected audio features from the song.
    """

    # Extract the track ID from the song link
    link = song_link
    id = link.split('/')[-1].split('?')[0]
    track_id = id

    # Request audio features for the specified track ID using Spotify API (sp)
    audio_features_data = sp.audio_features(track_id)

    if audio_features_data:
        # Get the first (and only) item from the audio_features_data list
        data = audio_features_data[0]

        # Convert the audio features data into a DataFrame using a function called response_to_df
        df = response_to_df(data)

        # Convert the DataFrame to a NumPy array
        arr_numpy = df.to_numpy()

        # Extract specific audio features from the NumPy array
        # You can modify this list based on the features you want to extract
        features_list = arr_numpy[0:1]

        # Return the selected audio features as a list
        return [
            features_list[0][0],  # Feature 1
            features_list[0][1],  # Feature 2
            features_list[0][5],  # Feature 6
            features_list[0][6],  # Feature 7
            features_list[0][7],  # Feature 8
            features_list[0][9],  # Feature 10
            features_list[0][10]  # Feature 11
        ]
    
    # Return an empty list if no audio features were found or if the search results were empty
    return []


def response_to_df(response_data: dict) -> pd.DataFrame:
    """
    Convert response data dictionary to a Pandas DataFrame.

    This function takes a dictionary of response data and extracts
    relevant information to create a structured DataFrame.

    Args:
        response_data (dict): A dictionary containing response data.

    Returns:
        pd.DataFrame: A DataFrame containing selected response data columns.
    """

    # Define the columns to select from the response data
    columns_to_select = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo', 'id', 'duration_ms', 
        'time_signature'
    ]

    # Prepare the data for the DataFrame
    for key in response_data:
        data = []
        data.append(response_data[key])
        response_data[key] = data
        
    # Create the DataFrame using the prepared data and columns
    df = pd.DataFrame(response_data)
    df = df[columns_to_select]
    return df



