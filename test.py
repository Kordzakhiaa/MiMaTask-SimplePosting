import json
import pprint
from validate_data import check_email

users_data = [
    {
        "name": "giorgi",
        "email": "giorgi@gmail.com",
        "password1": "$5$rounds=535000$JlSnm01ConU/peyl$eHaY7FTOJI2Rc9I4oJ/uTk1WjK7xHuegRhicyWtMe39",
        "password2": "$5$rounds=535000$Aw62vhAU8H6DIvr3$uTsQ4XgKu5l.ZaZkLmm263U0tSeKEO0S0JVEnNRj6T/"
    }
]

posts = [
    {
        "name": "miriani",
        "email": "miriani@gmail.com",
        "title": "What is history?",
        "content": "History is the study of people, actions, decisions, interactions and behaviours.......",
        "date_created": "2021-09-21 19:05:55.322369",
        "likes": [
            {
                "giorgi@gmail.com": 1,
                "luka@gmail.com": 1
            }
        ],
        "total_likes": 0,
        "comments": [],
        "id": 1
    }
]

user_email: str = 'giorgi@gmail.com'
post_id = 1
comment = 'magaria sagol:)'

if check_email(user_email):
    for post in posts:
        if post_id == post['id']:
            post['comments'].append({user_email: comment})
        post['total_likes'] = len(post['likes'][:])

pprint.pprint(posts)
