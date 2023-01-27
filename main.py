import configparser
import time
import tweepy
import unidecode
import customtkinter
import tkinter
import pyttsx3
import threading

"""
You need to create a config.ini file in this format:
This makes sure that your keys are not hard coded into the program.

[twitter]

api_key = YOUR API_KEY
api_key_secret = YOUR API_KEY_SECRET

access_token = YOUR ACCESS_TOKEN
access_token_secret = YOUR ACCESS TOKEN SECRET
"""


# Read credentials from config file
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Authorization, setting access token
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Creates an instance of the tweepy API handler
api = tweepy.API(auth)

# Creating the LIMIT variable, this is the number of tweets you want from an acount
LIMIT = 1
# This is where the twitter accounts' names, you want to search are stored
searched_twitter_accounts = []
# This stores the already read tweets, so there are no duplicates read/shown
tweet_bank = set()
# This is a variable that determines if it is the first run of the program
is_start = True
# Sets the appearence of cutsomtkinter (ctk is a "skin" for Tkinter, which is responsible for the GUI)
customtkinter.set_appearance_mode("light") # Can be light/dark/ system(Not sure, but probably only works on MAC)
customtkinter.set_default_color_theme("green") # Can be green/blue/dark blue
#Creating an instance of the Ctk class (this is where the GUI elements will be displayed on)/ the app's window
root = customtkinter.CTk()
#sets the 'resolution' for the window
root.geometry("900x280")



def talk(tweet):
    """
    :param tweet: The tweet you want said
    :return: nothing
    """
    # Initializes the pyttsx3 class
    engine = pyttsx3.init()
    # Says the tweet
    engine.say(tweet)
    # Keeps running
    engine.runAndWait()
    # Deletes the tweet from the list displayed.
    tweet_listbox.delete(0,0)



def search_for_tweets():
    """
    searches for tweets, and calls talk function
    """
    # Loops through all added accounts
    tweets_to_read = []
    for user in searched_twitter_accounts:
        # searches for the current users timeline, returns (LIMIT) number of tweets
        tweets = api.user_timeline(screen_name=user, count=LIMIT, tweet_mode='extended')


        # Loops through the tweets
        for tweet in tweets:
            # Cleans the tweets text (gets rid of emojis, converts UNICODE characters into readable format)
            tweet = f"{user} Tweeted: {unidecode.unidecode(tweet.full_text)}"
            # Replaces the 'newline'/enter character at the end of sentences
            tweet = tweet.replace("\n", "")
            # Loops through the tweet bank
            if tweet not in tweet_bank:
                # Adds the tweet to the displayed list
                tweet_listbox.insert("end", tweet)
                # Adds the tweet to the tweet bank, this is where the already read tweets are.
                tweet_bank.add(tweet)
                # Adds the tweet into the tweets_to_read list. This is the list we loop thorugh to see what the program has to say
                tweets_to_read.append(tweet)
    # Loops thorugh the tweets that need to be said
    for tweet in tweets_to_read:
        # Calls the talk function - Line 58
        talk(tweet)
    #waits 10 seconds
    time.sleep(10)
    # Calls the same function, creating a thread
    thread = threading.Thread(target=search_for_tweets, daemon=True)
    # Starts the thread
    thread.start()


def start(is_start):
    # Checks if this is the first loop of the program
    if is_start:
        # if it is, it sets it to False
        is_start = False
        #starts a thread. You need multiple threads, so that the GUI doesn't freeze while the program says the tweets
        # target: this is the function you want running on the thread
        # Daemon: If your thread is a daemon thread, when you close the GUI, it stops the thread.
        a_thread = threading.Thread(target=search_for_tweets, daemon=True)
        #starts the thread
        a_thread.start()


def add_user_by_username(user):
    """
    Add the user to the list of users, and displays it
    :param user: the user that you want to add
    :return: nothing
    """
    # makes the user's name all lowercase, to eliminate duplicates made by different casing
    user = user.lower()
    # Checks if the user is in the list of users displayed
    if user not in current_users.get(0,"end"):
        # Checks if the user's name is empty
        if user == "" or user == " ":
            # breaks the function
            return
        # # This only runs if the previous if statement is false
        # Adds the user into a list containing the users you want to search
        searched_twitter_accounts.append(user)
        # Adds the user's name to the displayed listbox
        current_users.insert("end",user)
    # Clears the input field
    add_user.delete(0,"end")

def delete_selected():
    """
    Deletes the selected user from the usernames listbox
    :return: nothing
    """
    # Loops through the selected users
    for i in current_users.curselection():
        # deletes them from the list
        current_users.delete(i)
        # Removes the user from the searched user accounts
        searched_twitter_accounts.remove(i)


# Creates the lisbox where tweets are displayed
tweet_listbox = tkinter.Listbox(root, width=80, height=15, font=("Times", 14))
# Places lisbox on the grid at (0,0) Sticks to North(up), with an x padding of 5
tweet_listbox.grid(column=0, row= 0, sticky="N", padx=5)

# Creates the Input field for usernames
add_user = customtkinter.CTkEntry(root)
# Places entry field on the grid at (1,0) Sticks to North(up), with an x padding of 5
add_user.grid(column=1, row= 0,sticky="N", padx=5)

# Creates the ADD USER button, on click the button calls the add_user_by_username with the input field as attribute (- Line 125)
add_user_button = customtkinter.CTkButton(root, text="Add User", command=lambda: add_user_by_username(add_user.get()))
# Places button on the grid at (1,0) Sticks to North(up), with a y padding of 50
add_user_button.grid(column=1, row=0, sticky="N", pady= 50)

# Creates the current users listbox, where the searched users are displayed
current_users = tkinter.Listbox(root, width= 15, height=10, font=('Times', 14))
# Places listbox on the grid at (2,0) Sticks to North(up)
current_users.grid(column=2, row=0, sticky="N")

# Creates the "Delete selected account" button, on click it calls the delete selected function (- Line 147)
delete_selected_users = customtkinter.CTkButton(root, width=25, text="Delete selected account", command=delete_selected)
# Places listbox on the grid at (2,0) Sticks to North(up), with an y padding of 150
delete_selected_users.grid(column=2, row=0,sticky="N", pady= 150)

# Creates the main loop of the program, this keeps the GUI open
start(is_start)

root.mainloop()