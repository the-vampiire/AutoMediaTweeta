import os, subprocess, shutil, time
from requests_oauthlib import OAuth1

# import config credentials for oAuth
from local_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, INSTAGRAM_USER, INSTAGRAM_PASSWORD

# import MediaTweet class
from any_media_tweet import AnyMediaTweet

# [source - https://www.freeformatter.com/mime-types-list.html]
twitter_mime_types = {
  'gif': 'image/gif',
  'png': 'image/png',
  'jpg': 'image/jpeg',
  'jpeg': 'image/jpeg',
  'mp4': 'video/mp4',
  'mpeg': 'video/mpeg'
}

instagram_mime_types = {
  'jpg': 'image/jpeg'
}

# set names of unused and used directories and the hashtags CSV
unused_directory_name = 'unused'
used_directory_name = 'used'
tags_file = 'tags.txt'

unused_directory_path = os.path.abspath(unused_directory_name)
used_directory_path = os.path.abspath(used_directory_name)


def refresh_directory():
  return os.listdir(unused_directory_path)

unused_directory = refresh_directory()

def get_file_type(media_file, mime_types):
  file_type = media_file[media_file.find('.') + 1:]
  try:
    mime_type = mime_types[file_type]
  except KeyError:
    print('this file type [{}] of file [{}] is not accepted'.format(file_type, media_file))
    exit()
  else:
    return mime_type

def move_file(origin, destination):
  shutil.move(origin, destination)
  print('File successfully uploaded and moved to "used" directory')

def get_hashtags():
  hashtag_list = open(os.path.abspath(tags_file), 'r').read().split(', ')
  hashtags = " ".join(['#'+hashtag if hashtag[0] != '#' else hashtag for hashtag in hashtag_list]) if hashtag_list[0] else None
  
  return hashtags

def post_media(media_file, text = get_hashtags(), option = 'twitter'):
  media_path = "{}/{}".format(unused_directory_path, media_file)
  used_upload_path = "{}/{}".format(used_directory_path, media_file)

  if 'both' in option:
    send_tweet(media_file, media_path, text)
    print('awaiting completion of tweet, 5 seconds.')
    time.sleep(5)
    print('tweet complete, posting to instagram now.')
    post_insta(media_file, media_path, text)
    print('awaiting completion of instagram post, 5 seconds')
  elif 'twitter' in option:
    send_tweet(media_file, media_path, text)
  elif 'instagram' in option:
    post_insta(media_file, media_path, text)
  else:
    raise Exception('Invalid media posting type [{}]'.format(option))
  
  # move to used folder after posting to prevent duplicate uploads
  time.sleep(5)
  move_file(media_path, used_upload_path)

def post_insta(media_file, media_path, text):
  file_type = get_file_type(media_file, instagram_mime_types)
  username = '-u {}'.format(INSTAGRAM_USER)
  password = '-p {}'.format(INSTAGRAM_PASSWORD)
  file = '-f{}'.format(media_path)
  text_input = '-t "{}"'.format(text)

  subprocess.Popen(['instapy', username, password, file, text_input])

def send_tweet(media_file, media_path, text):
  file_type = get_file_type(media_file, twitter_mime_types)

  OAUTH_TOKEN = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  mediaTweet = AnyMediaTweet(media_path, file_type, text, OAUTH_TOKEN)
  mediaTweet.upload_init()
  mediaTweet.upload_append()
  mediaTweet.upload_finalize()
  mediaTweet.tweet()

def main():
  try:
    next_upload = os.listdir(unused_directory_path)[0]
  except IndexError:
    print('unused directory is empty.\nadd more media files to the "unused" directory then rerun the script.')
    exit()
    
  hashtags = get_hashtags()
  send_tweet(next_upload, hashtags)
  
if __name__ == '__main__':
  main()

  
