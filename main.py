from flask import Flask, request, redirect, render_template
from tweet_media import send_tweet, refresh_directory
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/tweet", methods=['POST'])
def tweet_media():
    dump_directory = refresh_directory()
    media = request.form['media']
    tweet_text = request.form['text']
    if media not in dump_directory:
        error = "'{0}' is not in your dump directory".format(media)
        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    send_tweet(media, tweet_text)
    return render_template('edit.html', dump_directory = refresh_directory())

@app.route("/")
def index(): 
    encoded_error = request.args.get("error")
    return render_template('edit.html', dump_directory = refresh_directory(), quote=True)

app.run()
