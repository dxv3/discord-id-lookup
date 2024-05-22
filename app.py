from flask import Flask, request, render_template
import requests
from datetime import datetime
import json

app = Flask(__name__)
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

DISCORD_TOKEN = config['DISCORD_TOKEN']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    user_id = request.form['user_id']
    headers = {
        'Authorization': f'Bot {DISCORD_TOKEN}'
    }
    response = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        user_data['badges'] = get_user_badges(user_data.get('public_flags', 0))
        user_data['created_at'] = datetime.utcfromtimestamp(((int(user_data['id']) >> 22) + 1420070400000) / 1000).strftime('%Y-%m-%d %H:%M:%S' + " UTC")

        avatar_hash = user_data['avatar']
        if avatar_hash.startswith('a_'):
            user_data['avatar_url'] = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{avatar_hash}.gif?size=1024"
        else:
            user_data['avatar_url'] = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{avatar_hash}.png?size=1024"

        if 'banner' in user_data and user_data['banner']:
            banner_hash = user_data['banner']
            if banner_hash.startswith('a_'):
                user_data['banner_url'] = f"https://cdn.discordapp.com/banners/{user_data['id']}/{banner_hash}.gif?size=1024"
            else:
                user_data['banner_url'] = f"https://cdn.discordapp.com/banners/{user_data['id']}/{banner_hash}.png?size=1024"
        else:
            user_data['banner_url'] = None

        user_data['accent_color'] = user_data.get('accent_color', None)

        return render_template('result.html', user_data=user_data)
    else:
        return render_template('error.html', error="User not found or invalid ID.")

def get_user_badges(flags):
    badges = []
    badges.append('needs fixing, very bugged :(')
    return badges

if __name__ == '__main__':
    app.run(debug=True)
