from recommendation import get_recommendation_by_link, get_recommendation_by_name

def by_name(song_name :str):
    df = get_recommendation_by_name(song_name)
    random_rows = df.sample(10)
    song_title = random_rows['track_name'].values.tolist()
    song_id = random_rows['track_id'].values.tolist()
    return(song_id, song_title)


def by_link(song_link :str):
    df = get_recommendation_by_link(song_link)
    random_rows = df.sample(10)
    song_title = random_rows['track_name'].values.tolist()
    song_id = random_rows['track_id'].values.tolist()
    return(song_id, song_title)
#https://open.spotify.com/track/0DW5anNzTO7h0OlKqFsVQ6