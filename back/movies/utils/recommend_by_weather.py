from openai import OpenAI


def recommend_by_weather(weather_id):
    weather_message = ""
    if weather_id < 300:
        # Thunderstorm (2XX)
        weather_message = "천둥 번개가 몰려와요"
    elif weather_id < 600:
        # Drizzle (3XX), Rain (5XX)
        weather_message = "촉촉한 비가 내려요"
    elif weather_id < 700:
        # Snow (6XX)
        weather_message = "하얀 눈이 송이송이 내려요"
    elif weather_id == 800:
        # Clear (800)
        weather_message = "맑은 하늘이 아름다운 날이에요"
    else:
        # Atmosphere (8XX), Clouds (80X)
        weather_message = "우중충 하고 흐린 날이에요"
    
    # client = OpenAI(
    #     api_key:
    # )