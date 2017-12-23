# What is my purpose?
- tweet one file at a time out of a `unused` directory using a list of hashtags, reports with a success or failure, then moves the tweeted file to the `used` directory

# Forked Modifications
- add Twitter credentials to the `config.py` file
	- CONSUMER_KEY
	- CONSUMER_SECRET
	- ACCESS_TOKEN
	- ACCESS_TOKEN_SECRET
- uses `unused` directory to store the collection of unused images / videos
- uses `used` directory to store the used files that are moved after tweeting
- uses a `tags.txt` file that holds a CSV of hashtags to apply to each tweet
- handles `mp4, png, jpg, jpeg, gif, mpeg` image / gif / video file types 

# Instructions

#### Setup
- clone this repo using:
	- `git clone https://github.com/the-vampiire/auto-media-tweeting.git auto_tweet`
- install the dependancies using:
	-	`pip install -r requirements.txt`
- in the newly created `auto_tweet` directory create the `unused` directory and `used` directory using:
	- `mkdir unused used`
### Customize
- in the `unused` directory add all of the image / gif / video files you would like to upload
- leave the `used` directory empty
- in the `config.py` file add your Twitter credentials
	- you can find these on your app page at https://apps.twitter.com (if you dont have an app create one for free to obtain the credentials)
	- click on your app then go to `keys and token` tab and copy over the credentials
- in the `tags.txt` file add comma separated hashtags that will be added to the tweet
	- **DO NOT INCLUDE `#`** this is applied internally.
	- example content of `tags.txt`: `coding, python, autotweeting`
	- would be automatically converted and added to the upload as `#coding #python #autotweeting`

### Usage
- to start up the server and begin using the interface enter the following command (while in the `auto_tweet` directory)
	- `python main.py`
- click the url or navigate to `127.0.0.1:5000` in your browser
- use the dropdown menu to select the media to upload
- use the text field to input some text / hashtags
- hit the tweet button!

<hr>
<hr>

# Original Documentation Below

# Large Video Upload

This Python sample demonstrates the following process of uploading large video files asynchronously with the Twitter API.

1. **INIT** media upload.
2. **APPEND** chunked data.
3. **FINALIZE** media uploaded.
4. Check **STATUS** of video processing.
5. Tweet with attached video.

Large video files are longer than 30 seconds up to 140 seconds, and/or a file size larger than 15 megabytes up to 512 megabytes.

[Learn more](https://dev.twitter.com/rest/media) about the Twitter Media APIs. Pay attention to the other requirements such as encoding, frame size and video formats supported.

## Running the sample

1. Install requirements:

	```
	$ pip install -r requirements.txt
	```

2. Fill in your [consumer keys and access tokens](https://apps.twitter.com) in `async-upload.py`:

	```
	CONSUMER_KEY = 'your-consumer-key'
	CONSUMER_SECRET = 'your-consumer-secret'
	ACCESS_TOKEN = 'your-access-token'
	ACCESS_TOKEN_SECRET = 'your-access-secret'
	```

3. Edit path to your video file in `async-upload.py`:

 ```
 VIDEO_FILENAME = 'path/to/video/file'
 ```

4. Run script:

	```
	$ python async-upload.py
	```

Questions? Check our [developer discussion forums](https://https://twittercommunity.com/c/media-apis).
