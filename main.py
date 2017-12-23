from flask import Flask, request, redirect, render_template
from tweet_media import post_media, refresh_directory
import cgi, os

app = Flask(__name__)
app.config['DEBUG'] = True

post_options = [
    {
        'name': 'twitter and instagram',
        'value': 'both'
    },
    {
        'name': 'twitter',
        'value': 'twitter'
    },
    {
        'name': 'instagram',
        'value': 'instagram'
    }]

@app.route("/tweet", methods=['POST'])
def tweet_media():
    media = request.form['media']
    tweet_text = request.form['text']
    option = request.form['post_options']

    post_media(media, tweet_text, option)
    return render_template('edit.html', unused_directory = refresh_directory(), post_options = post_options)

@app.route("/")
def index():
    javascript = os.path.relpath('./static/main.js')
    return render_template('edit.html', javascript = javascript, unused_directory = refresh_directory(), post_options = post_options)

app.run()
