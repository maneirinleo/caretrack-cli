import requests

def get_daily_tip():
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=5)
        if response.status_code == 200:
            return response.json()['slip']['advice']
        return "Lembre-se de beber água e cuidar da sua saúde!"
    except:
        return "Mantenha o foco no seu autocuidado hoje."