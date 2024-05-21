from openai import OpenAI
from django.conf import settings
import requests
from .load import save_movies

def recommend_by_weather(weather_id):
    weather_message = ""
    recommend_conditions = ""
    if weather_id < 300:
        # Thunderstorm (2XX)
        weather_message = "천둥 번개가 몰려와요"
        recommend_conditions = """
            1. Genres: Action, SF, Thriller, Horror
            2. Fast paced story and loud music, dynamic scenes 
        """ 
    elif weather_id < 600:
        # Drizzle (3XX), Rain (5XX)
        weather_message = "촉촉한 비가 내려요"
        recommend_conditions = """
            1. Genres: Mistery, Classic, Romance, Indie
            2. Peaceful and tranquil, artistic
            3. Beatiful music and scenes
        """ 
    elif weather_id < 700:
        # Snow (6XX)
        weather_message = "하얀 눈이 내려요"
        recommend_conditions = """
            1. Genres: Romance, Family-Friendly
            2. Happy and exciting story
            3. Brings back childhood memories
            4. Great for christmast and snowy winter
        """ 
    elif weather_id == 800:
        # Clear (800)
        weather_message = "맑은 하늘이 아름다운 날이에요"
        recommend_conditions = """
            1. Genres: Feel-Good Comedies, Adventure, Drama
            2. Cheerful and dramatic story
        """ 
    else:
        # Atmosphere (8XX), Clouds (80X)
        weather_message = "우중충 하고 흐린 날이에요"
        recommend_conditions = """
            1. Genres: Mistery, Thriller, Detective, Noir
            2. Dark and hard-boiled story
        """ 
    
    client = OpenAI(
        api_key=settings.OPEN_API_KEY
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""
                Please recommend 10 movies that matches beyond conditions

                {recommend_conditions}

                Don't put additional words on your message.
                Just send me a list of movies in a format of a list.
                This unordered list should not contain any special character, 
                and movie titles should be seperated by '\n'.
                You can't make up the fake movie names.
                You only can recommend existing movies.
                """,
            },
        ],
    )

    response = completion.choices[0].message.content
    response = response.split('\n')

    recommended_movies = []
    recommended_movies_ids = []

    for movie_title in response:
        movie_title = movie_title[2:]
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&include_adult=true&language=ko-KR&page=1"
        response = requests.get(url, headers=headers).json().get('results')
        if response:
            result_movie = response[0]
            recommended_movies.append(result_movie)
            recommended_movies_ids.append(result_movie.get('id'))

    return weather_message, recommended_movies_ids


tmdb_access_token = settings.TMDB_ACCESS_TOKEN

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_access_token}"        
}