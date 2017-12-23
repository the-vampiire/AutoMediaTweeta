import os, shutil
from requests_oauthlib import OAuth1

# import config credentials for oAuth
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# import MediaTweet class
from any_media_tweet import AnyMediaTweet

# [source - https://www.freeformatter.com/mime-types-list.html]
mime_types = {
  'gif': 'image/gif',
  'png': 'image/png',
  'jpg': 'image/jpeg',
  'jpeg': 'image/jpeg',
  'mp4': 'video/mp4',
  'mpeg': 'video/mpeg'
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

def move_file(origin, destination):
  shutil.move(origin, destination)
  print('File successfully uploaded and moved to "used" directory')

def get_hashtags():
  hashtag_list = open(os.path.abspath(tags_file), 'r').read().split(', ')
  hashtags = " ".join(['#'+hashtag if hashtag[0] != '#' else hashtag for hashtag in hashtag_list]) if hashtag_list[0] else None
  
  return hashtags

def send_tweet(media_file, text = get_hashtags()):
  media_path = "{}/{}".format(unused_directory_path, media_file)
  used_upload_path = "{}/{}".format(used_directory_path, media_file)
  file_type = media_file[media_file.find('.') + 1:]

  try:
    mime_type = mime_types[file_type]
  except KeyError:
    print('this file type [{}] of file [{}] is not accepted'.format(file_type, media_file))
    exit()

  OAUTH_TOKEN = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  mediaTweet = AnyMediaTweet(media_path, mime_type, text, OAUTH_TOKEN)
  mediaTweet.upload_init()
  mediaTweet.upload_append()
  mediaTweet.upload_finalize()
  mediaTweet.tweet()
  
  # move to used folder to prevent duplicate uploads
  move_file(media_path, used_upload_path)

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

  
