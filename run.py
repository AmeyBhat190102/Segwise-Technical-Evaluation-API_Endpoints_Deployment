from app import app
import io
import pandas as pd
import requests
from flask import request, jsonify, render_template
from app import app, db, auth
from models import Game


@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)


@app.route('/upload', methods=['POST'])
def upload_csv():
    data = request.json
    url = data.get('csv_url')
    if not url:
        return jsonify({'error': 'CSV URL is required'}), 400

    try:
        if 'docs.google.com/spreadsheets' in url:
            csv_url = convert_google_sheets_url(url)
            response = requests.get(csv_url)
            response.raise_for_status()  # Check if the request was successful
            csv_data = io.StringIO(response.text)
        else:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            csv_data = io.StringIO(response.text)

        # Read CSV data into a pandas DataFrame
        df = pd.read_csv(csv_data)  # Skip bad lines
        # Select specific columns
        selected_columns = ['AppID', 'Name', 'Release date', 'Required age', 'Price', 'DLC count',
                            'About the game', 'Supported languages', 'Windows', 'Mac', 'Linux',
                            'Positive', 'Negative', 'Score rank', 'Developers', 'Publishers',
                            'Categories', 'Genres', 'Tags']

        # Filter DataFrame to selected columns
        df = df[selected_columns]
        df.rename(columns={
            'AppID': 'appid',
            'Name': 'name',
            'Release date': 'release_date',
            'Required age': 'required_age',
            'Price': 'price',
            'DLC count': 'dlc_count',
            'About the game': 'about_the_game',
            'Supported languages': 'supported_languages',
            'Windows': 'windows',
            'Mac': 'mac',
            'Linux': 'linux',
            'Positive': 'positive',
            'Negative': 'negative',
            'Score rank': 'score_rank',
            'Developers': 'developers',
            'Publishers': 'publishers',
            'Categories': 'categories',
            'Genres': 'genres',
            'Tags': 'tags'
        }, inplace=True)

        # Convert DataFrame to list of dictionaries
        games_data = df.to_dict(orient='records')

        # Add data to database
        for game_data in games_data:
            game = Game(**game_data)
            db.session.add(game)

        db.session.commit()

        return jsonify({'message': 'Data uploaded successfully'}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {e}'}), 400
    except pd.errors.ParserError as e:
        return jsonify({'error': f'Error parsing CSV: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 400


def convert_google_sheets_url(url):
    csv_export_url = url.replace('/edit?gid=', '/gviz/tq?tqx=out:csv&gid=')
    return csv_export_url


@app.route('/query', methods=['GET'])
def query_data():
    args = request.args
    query = db.session.query(Game)

    if 'name' in args:
        query = query.filter(Game.name.contains(args['name']))
    if 'appid' in args:
        query = query.filter(Game.appid == int(args['appid']))
    if 'release_date' in args:
        query = query.filter(Game.release_date == args['release_date'])
    if 'release_date_gt' in args:
        query = query.filter(Game.release_date > args['release_date_gt'])
    if 'release_date_lt' in args:
        query = query.filter(Game.release_date < args['release_date_lt'])
    if 'required_age' in args:
        query = query.filter(Game.required_age == int(args['required_age']))
    if 'price' in args:
        query = query.filter(Game.price == float(args['price']))
    if 'dlc_count' in args:
        query = query.filter(Game.dlc_count == int(args['dlc_count']))
    if 'supported_languages' in args:
        query = query.filter(Game.supported_languages.contains(args['supported_languages']))
    if 'windows' in args:
        query = query.filter(Game.windows == (args['windows'].lower() == 'true'))
    if 'mac' in args:
        query = query.filter(Game.mac == (args['mac'].lower() == 'true'))
    if 'linux' in args:
        query = query.filter(Game.linux == (args['linux'].lower() == 'true'))
    if 'positive' in args:
        query = query.filter(Game.positive == int(args['positive']))
    if 'negative' in args:
        query = query.filter(Game.negative == int(args['negative']))
    if 'score_rank' in args:
        query = query.filter(Game.score_rank == int(args['score_rank']))
    if 'developers' in args:
        query = query.filter(Game.developers.contains(args['developers']))
    if 'publishers' in args:
        query = query.filter(Game.publishers.contains(args['publishers']))
    if 'categories' in args:
        query = query.filter(Game.categories.contains(args['categories']))
    if 'genres' in args:
        query = query.filter(Game.genres.contains(args['genres']))
    if 'tags' in args:
        query = query.filter(Game.tags.contains(args['tags']))
    if 'price_gt' in args:
        query = query.filter(Game.price > float(args['price_gt']))
    if 'price_lt' in args:
        query = query.filter(Game.price < float(args['price_lt']))

    if 'aggregate' in args:
        if args['aggregate'] == 'max_price':
            result = query.order_by(Game.price.desc()).first()
            return jsonify({'max_price': result.price if result else None}), 200
        if args['aggregate'] == 'min_price':
            result = query.order_by(Game.price.asc()).first()
            return jsonify({'min_price': result.price if result else None}), 200
        if args['aggregate'] == 'avg_price':
            result = query.with_entities(db.func.avg(Game.price)).scalar()
            return jsonify({'avg_price': result}), 200

    results = query.all()
    result_list = []
    for result in results:
        result_list.append({
            'appid': result.appid,
            'name': result.name,
            'release_date': result.release_date,
            'required_age': result.required_age,
            'price': result.price,
            'dlc_count': result.dlc_count,
            'about_the_game': result.about_the_game,
            'supported_languages': result.supported_languages,
            'windows': result.windows,
            'mac': result.mac,
            'linux': result.linux,
            'positive': result.positive,
            'negative': result.negative,
            'score_rank': result.score_rank,
            'developers': result.developers,
            'publishers': result.publishers,
            'categories': result.categories,
            'genres': result.genres,
            'tags': result.tags
        })

    return jsonify(result_list), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
