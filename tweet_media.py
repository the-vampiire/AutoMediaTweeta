import os, shutil
from requests_oauthlib import OAuth1

# import config credentials for oAuth
from local_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

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

# set names of dump and used directories and the hashtags CSV
dump_directory = 'dump'
used_directory = 'used'
hashtags = 'tags.txt'
dump_directory_path = os.path.abspath(dump_directory)
used_directory_path = os.path.abspath(used_directory)
hashtag_list = open(os.path.abspath(hashtags), 'r').read().split(', ')
hashtags = " ".join(['#'+hashtag for hashtag in hashtag_list]) if hashtag_list[0] else None

try:
  next_upload = os.listdir(dump_directory_path)[0]
except IndexError:
  print('dump directory is empty.\nadd more media files to the "dump" directory then rerun the script.')
  exit()
else:
  next_upload_path = "{}/{}".format(dump_directory_path, next_upload)
  used_upload_path = "{}/{}".format(used_directory_path, next_upload)
  file_type = next_upload[next_upload.find('.') + 1:]
  try:
    mime_type = mime_types[file_type]
  except KeyError:
    print('this file type [{}] of file [{}] is not accepted'.format(file_type, next_upload))

if __name__ == '__main__':
  OAUTH_TOKEN = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  mediaTweet = AnyMediaTweet(next_upload_path, mime_type, OAUTH_TOKEN, hashtags)
  mediaTweet.upload_init()
  mediaTweet.upload_append()
  mediaTweet.upload_finalize()
  mediaTweet.tweet()

  # move to used folder to prevent duplicate uploads
  shutil.move(next_upload_path, used_upload_path)
  print('File successfully uploaded and moved to "used" directory')
