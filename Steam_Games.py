import requests
import csv
import os
from datetime import datetime

USERS = [
    {
        'api_key': 'SUA_API_KEY_1',
        'steam_id': 'SUA_ID_STEAM_1'
    },
    {
        'api_key': 'SUA_API_KEY_2', 
        'steam_id': 'SUA_ID_STEAM_2'
    },
    {
        'api_key': 'SUA_API_KEY_3', 
        'steam_id': 'SUA_ID_STEAM_3'
    },
    {
        'api_key': 'SUA_API_KEY_4', 
        'steam_id': 'SUA_ID_STEAM_4'
    },
     {
        'api_key': 'SUA_API_KEY_5', 
        'steam_id': 'SUA_ID_STEAM_5'
    },
     {
        'api_key': 'SUA_API_KEY_6', 
        'steam_id': 'SUA_ID_STEAM_6'
    }
    
]

USER_NAMES = {
    'SUA_ID_STEAM_1': 'Utilizador 1',
    'SUA_ID_STEAM_2': 'Utilizador 2',
    'SUA_ID_STEAM_3': 'Utilizador 3',
    'SUA_ID_STEAM_4': 'Utilizador 4',
    'SUA_ID_STEAM_5': 'Utilizador 5',
    'SUA_ID_STEAM_6': 'Utilizador 6'
}


OUTPUT_FILE = 'steam_games_aggregated.csv'


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_user_games(api_key, steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': True,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        games = response.json().get('response', {}).get('games', [])
        log(f"Conta {steam_id} possui {len(games)} jogos.")
        return games
    except Exception as e:
        return []

def load_existing_data():
    data = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                owners = row['Owner'].split(', ') if row['Owner'] else []
                data[row['AppID']] = {
                    'AppID': row['AppID'],
                    'Game Name': row['Game Name'],
                    'Number of Copies': int(row['Number of Copies']),
                    'Owner': owners
                }
        log(f"Dados existentes carregados: {len(data)} jogos no arquivo.")
    else:
        log("Nenhum arquivo existente encontrado. Criando novo arquivo.")
    return data

def save_data(data):
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['AppID', 'Game Name', 'Number of Copies', 'Owner']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for appid in data:
            game = data[appid]
            owner_names = [USER_NAMES.get(owner, owner) for owner in game['Owner']]
            writer.writerow({
                'AppID': appid,
                'Game Name': game['Game Name'],
                'Number of Copies': game['Number of Copies'],
                'Owner': ', '.join(owner_names)
            })
    log(f"Arquivo salvo com {len(data)} jogos.")

def process_users():
    data = load_existing_data()
    
    for user in USERS:
        log(f"Processando conta {USER_NAMES.get(user['steam_id'], user['steam_id'])}...")
        games = get_user_games(user['api_key'], user['steam_id'])
        if not games:
            log(f"Nenhum jogo encontrado para a conta {USER_NAMES.get(user['steam_id'], user['steam_id'])}.")
            continue
            
        new_games = 0
        updated_games = 0
        
        for game in games:
            appid = str(game.get('appid'))
            name = game.get('name', 'Unknown')
            
            if appid in data:
                if user['steam_id'] not in data[appid]['Owner']:
                    data[appid]['Number of Copies'] += 1
                    data[appid]['Owner'].append(user['steam_id'])
                    updated_games += 1
            else:
                data[appid] = {
                    'AppID': appid,
                    'Game Name': name,
                    'Number of Copies': 1,
                    'Owner': [user['steam_id']]
                }
                new_games += 1
        
        log(f"Conta {USER_NAMES.get(user['steam_id'], user['steam_id'])} adicionou {new_games} novos jogos e atualizou {updated_games} existentes.")
    
    save_data(data)

if __name__ == "__main__":
    process_users()