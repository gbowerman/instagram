# Instagram tools
This repo is for tools which call the unnofficial [Instagram API](https://pypi.org/project/InstagramAPI/) to analyze followers and followings.

## Command Line tools

### cmd/followers.py

Prints a list of Instagram users who follow you but you don't follow.

Prints a list of Instagram users you follow but don't follow you.
 
To run this program create a .env file in the same folder containing these variables:  

INSTA_CLIENT=your instagram user name  
INSTA_SECRET=your instagram password  

Install the required libraries: 
```
pip install python-dotenv  
pip install InstagramApi  
```
Then run:
```  
python followers.py
```