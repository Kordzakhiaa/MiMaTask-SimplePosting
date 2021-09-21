import os
import json
from datetime import datetime
from passlib.hash import sha256_crypt

from flask import Flask, request
from validate_data import check_email, is_valid_email, check_password, is_valid_password

app = Flask(__name__)


# @TODO: WRITE APPROPRIATE STATUS CODEs!!!!

@app.route('/')
def index() -> str:
    routes = [f'{rule}' for rule in app.url_map.iter_rules()]

    return f'Routes: {routes}'


@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    if request.method == 'POST':
        user_data: dict = request.json
        email: str = user_data['email']
        password1: str = user_data['password1']
        password2: str = user_data['password2']

        if is_valid_email(email):
            if not is_valid_password(password1):
                return '403 Forbidden\npassword: length>=8, capitalize, symbols'
            elif password1 == password2:
                user_data['password1'] = sha256_crypt.hash(password1)
                user_data['password2'] = sha256_crypt.hash(password2)
                filesize = os.path.getsize('user_data.json')

                if filesize == 0:
                    data = [user_data]
                    with open('user_data.json', mode='w') as f:
                        f.write(json.dumps(data, indent=2))
                else:
                    if check_email(email):
                        return '400 bad request\nMail is used'
                    with open('user_data.json') as feedsjson:
                        feeds = json.load(feedsjson)
                    feeds.append(user_data)
                    with open('user_data.json', mode='w') as f:
                        f.write(json.dumps(feeds, indent=2))
            else:
                return '400 Bad request\nPassword1 != Password2'
            return '201 Created\nSuccessfully registered!'
        return '400 Bad request\ninvalid mail'

    return 'register page'


@app.route('/login', methods=['POST', 'GET'])
def login() -> str:
    if request.method == 'POST':
        user_data: dict = request.json
        email: str = user_data['email']
        password: str = user_data['password']

        if check_email(email):
            if check_password(password):
                return '200 Ok'
            return '403 Forbidden\npassword or email is incorrect'

        return '400 Bad request \nregister please'
    return 'login page'


@app.route('/create_post', methods=['GET', 'POST'])
def create_post() -> str:
    # @TODO: is_authenticated...
    if request.method == 'POST':
        user_data: dict = request.json
        email: str = user_data['email']
        user_data['date_created'] = str(datetime.utcnow())
        user_data['likes'] = []
        user_data['total_likes'] = 0
        user_data['comments'] = []
        user_data['total_comments'] = 0

        filesize = os.path.getsize('posts.json')

        if check_email(email):
            if filesize == 0:
                user_data['id'] = 1
                data = [user_data]
                with open('posts.json', mode='w') as f:
                    f.write(json.dumps(data, indent=2))
            else:
                with open('posts.json') as feedsjson:
                    feeds = json.load(feedsjson)
                user_data['id'] = feeds[-1]['id'] + 1
                feeds.append(user_data)

                with open('posts.json', mode='w') as f:
                    f.write(json.dumps(feeds, indent=2))

            return '201 Created\nPost successfully created'
        return '403 Forbidden\nregister first!'
    return 'create post page'


@app.route('/posts')
def all_posts() -> str:
    with open('posts.json') as postsjson:
        posts = json.load(postsjson)
    return json.dumps(posts, indent=2)


@app.route('/post/<int:id>')
def get_post(id: int):
    # @ TODO: if not id in posts return bad request
    with open('posts.json') as postsjson:
        posts = json.load(postsjson)

    for post in posts:
        if id == post['id']:
            return post
        else:
            pass
    return f'400 bad request\nthere is no post with id-{id}'


@app.route('/like_post/<int:id>', methods=['GET', 'POST'])
def like_post(id: int) -> str:
    if request.method == 'POST':
        who_like_data: dict = request.json
        user_email: str = who_like_data['email']

        if check_email(user_email):
            with open('posts.json') as postsjson:
                posts = json.load(postsjson)

            for post in posts:
                if id == post['id']:
                    post['likes'].append({user_email: 1})
                post['total_likes'] = len(post['likes'][:])
            with open('posts.json', mode='w') as f:
                f.write(json.dumps(posts, indent=2))
            return '201 Created\nLIKE'
        return '403 Forbidden\nregister first!'


@app.route('/comment/<int:id>', methods=['GET', 'POST'])
def comment_post(id: int) -> str:
    if request.method == 'POST':
        who_comments_data = request.json
        user_email: str = who_comments_data['email']
        comment: str = who_comments_data['comment']

        with open('posts.json') as postsjson:
            posts = json.load(postsjson)

        if check_email(user_email):
            for post in posts:
                if id == post['id']:
                    post['comments'].append({user_email: comment})
                post['total_comments'] = len(post['comments'][:])
            with open('posts.json', mode='w') as f:
                f.write(json.dumps(posts, indent=2))
            return '201 Created\nCOMMENT'
        return '403 Forbidden\nregister first!'


if __name__ == '__main__':
    app.run(debug=True)
