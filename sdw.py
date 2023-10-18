import pandas as pd
import requests
import json
import openai


sdw_api_url = "https://sdw-2023-prd.up.railway.app"

df = pd.read_csv("SDW.csv")
user_ids = df["UserID"].tolist()
print(user_ids)


def get_user(id):
    response = requests.get(f"{sdw_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

openai_api_key = "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"


openai.api_key = openai_api_key


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você agora é um especialista em marketing bancário.",
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)",
            },
        ],
    )
    return completion.choices[0].message.content.strip('"')


for user in users:
    news = generate_ai_news(user)
    print(news)
    user["news"].append(
        {
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news,
        }
    )

    from requests.api import request


def update_user(user):
    reponse = requests.put(f"{sdw_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")
