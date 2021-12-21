from flask import redirect, render_template, session
from flask_app import app
from flask_app.models import friend, game, users_game

@app.route('/view/game/<int:game_id>')
def view_game(game_id):
    if 'user_id' not in session:
        return redirect('/login')

    collection = {
        'user_id': session['user_id'],
        'game_id': game_id,
        'status': 'collection'
    }
    wishlist = collection
    wishlist['status'] = 'wishlist'

    return render_template('game.html', game = game.Game.get_by_id(game_id), \
        friends_collection = friend.Friend.get_friends_games(collection), \
        friends_wishlist = friend.Friend.get_friends_games(wishlist))

# --- Processes user's request to add game to collection or wishlist ---
@app.route('/add/<status>/game/<int:game_id>')
def add_to_game_category(status, game_id):
    data = {
        'user_id': session['user_id'],
        'game_id': game_id,
        'status': status
    }

    users_game.UsersGame.save(data)

    return redirect('/dashboard')