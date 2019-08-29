'''application.py - Flask code for Instagram follower app'''
import sys

from flask import Flask, render_template, request
from InstagramAPI import InstagramAPI

app = Flask(__name__)
global_init_flag = False  # set this to True when app has initialized


def get_followings(api, user_id):
    """Returns list of followings"""
    followings = []
    next_max_id = ''
    while next_max_id is not None:
        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followings.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followings


def get_followers(api, user_id):
    """Returns list of followers"""
    followers = []
    next_max_id = ''
    while next_max_id is not None:
        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


def list_to_pkdict(personlist):
    '''Gets a list of people and converts to a dictionary keyed on pk id'''
    return {
        f['pk']: f
        for f in personlist
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():

    insta_id = request.form['username']
    insta_pswd = request.form['pw']

    # initialize InstagramAPI and login
    api = InstagramAPI(insta_id, insta_pswd)
    api.login()
    
    user_id = api.username_id

    # List followers and followings
    followers = get_followers(api, user_id)
    followers_dict = list_to_pkdict(followers)
    followings = get_followings(api, user_id)
    followings_dict = list_to_pkdict(followings)

    # count followers and followings
    num_followers = str(len(followers))
    num_followings = str(len(followings))
    
    # people you follow who don't follow you
    nonfollowings = []
    for following in followings:
        if following['pk'] not in followers_dict:
            if following['is_private'] is False:
                public_status = "Public"
            else:
                public_status = "Private"
            nonfollowings.append([following['full_name'], following['username'], public_status])
            # print(f"{following['full_name']} ({following['username']})")

    # who follows you who you don't follow?
    nonfollowers = []
    for follower in followers:
        if follower['pk'] not in followings_dict:
            if follower['is_private'] is False:
                public_status = "Public"
            else:
                public_status = "Private"
            nonfollowers.append([follower['full_name'], follower['username'], public_status])
            print(follower)
            # print(f"{follower['full_name']} ({follower['username']})")

    return render_template('results.html',
                            username=insta_id,
                            numfollowers=num_followers, 
                            numfollowings=num_followings,
                            followers=nonfollowers,
                            followings=nonfollowings)


@app.errorhandler(400)
def not_found(error):
    """Handle 400 error"""
    print(f'400 error: {error}')
    return render_template('index.html')


@app.errorhandler(500)
def handle_500(error):
    """To do:Handle 500 error - e.g. when error starts with 500 handle logon error"""
    print(f'500 error: {error}')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
