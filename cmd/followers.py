'''folowers.py - compare Instagram followers and followings'''
import os

from dotenv import load_dotenv
from InstagramAPI import InstagramAPI


def get_followings(api, user_id):
    """Returns list of followings"""
    followings = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''
        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followings.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followings


def get_followers(api, user_id):
    """Returns list of followers"""
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''
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


if __name__ == "__main__":
    # load environment
    load_dotenv()
    insta_id = os.environ["INSTA_CLIENT"]
    insta_pswd = os.environ["INSTA_SECRET"]
    api = InstagramAPI(insta_id, insta_pswd)
    api.login()

    user_id = api.username_id

    # List followers and followings
    followers = get_followers(api, user_id)
    followers_dict = list_to_pkdict(followers)
    followings = get_followings(api, user_id)
    followings_dict = list_to_pkdict(followings)

    print(f"Number of followers: {len(followers)}")
    print(f"Number of followings: {len(followings)}")
    
    print("\nFollowers who you don't follow:\n")
    for follower in followers:
        if follower['pk'] not in followings_dict:
            print(f"{follower['full_name']} ({follower['username']})")
    
    print("\nPeople you follow who don't follow you:\n")
    for following in followings:
        if following['pk'] not in followers_dict:
            print(f"{following['full_name']} ({following['username']})")
