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
        user_data['badges'] = get_user_badges(user_data['public_flags'])
        user_data['created_at'] = datetime.utcfromtimestamp(((int(user_data['id']) >> 22) + 1420070400000) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        return render_template('result.html', user_data=user_data)
    else:
        return render_template('error.html', error="User not found or invalid ID.")

def get_user_badges(flags):
    badges = []
    if flags & 1 << 0: badges.append('Discord Employee')
    if flags & 1 << 1: badges.append('Partnered Server Owner')
    if flags & 1 << 2: badges.append('HypeSquad Events')
    if flags & 1 << 3: badges.append('Bug Hunter Level 1')
    if flags & 1 << 6: badges.append('House Bravery')
    if flags & 1 << 7: badges.append('House Brilliance')
    if flags & 1 << 8: badges.append('House Balance')
    if flags & 1 << 9: badges.append('Early Supporter')
    if flags & 1 << 14: badges.append('Bug Hunter Level 2')
    if flags & 1 << 16: badges.append('Verified Bot')
    if flags & 1 << 17: badges.append('Early Verified Bot Developer')
    if flags & 1 << 18: badges.append('Discord Certified Moderator')
    return badges

if __name__ == '__main__':
    app.run(debug=True)
