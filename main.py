from flask import Flask, jsonify
import json
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os

app = Flask(__name__)


def get_scraped_data(username: str):
    query = f'(#100daysofcode) (from:{username})'
    tweets = []
    limit = 5000
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append({"date": tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
                           "username": tweet.user.username, "content": tweet.content, "name": tweet.user.displayname, "profile_image_url": tweet.user.profileImageUrl})
    df = pd.DataFrame(tweets)
    return df.to_dict()


@ app.route('/<username>')
def scraper(username):
    data = get_scraped_data(username)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
