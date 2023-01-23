from flask import Flask, jsonify
import json
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os

if __name__ == '__main__':
    app = Flask(__name__)


def get_scraped_data(username: str):
    query = f'(#100daysofcode) (from:{username}) until:2023-01-20 since:2018-12-01'
    tweets = []
    limit = 5000
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append({"date": tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
                           "username": tweet.user.username, "content": tweet.content})
    df = pd.DataFrame(tweets)
    return df.to_dict()


@app.route('/scraper/<username>')
def scraper(username):
    data = get_scraped_data(username)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
