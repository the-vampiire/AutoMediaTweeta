import os, sys, time, json, requests

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

class AnyMediaTweet(object):

  def __init__(self, media_path, mime_type, text, o_auth_token):
   
    self.media_path = media_path
    self.mime_type = mime_type
    self.tags = tags or "Automated using the AutoMediaTweeta script by #vampiire"
    self.token = o_auth_token
    self.total_bytes = os.path.getsize(self.media_path)
    self.media_id = None
    self.processing_info = None
    self.response = None

  def upload_init(self):
    request_data = {
      'command': 'INIT',
      'media_type': self.mime_type,
      'total_bytes': self.total_bytes,
    }

    req = requests.post(url = MEDIA_ENDPOINT_URL, data = request_data, auth = self.token)
    try:
      self.media_id = req.json()['media_id']
    except KeyError:
        print('Invalid credentials')
        exit()

  def upload_append(self):
    '''
    Uploads media in chunks and appends to chunks uploaded
    '''
    segment_id = 0
    bytes_sent = 0
    file = open(self.media_path, 'rb')

    while bytes_sent < self.total_bytes:
      chunk = file.read(4*1024*1024)
      
      print('APPEND')

      request_data = {
        'command': 'APPEND',
        'media_id': self.media_id,
        'segment_index': segment_id
      }

      files = {
        'media':chunk
      }

      req = requests.post(url = MEDIA_ENDPOINT_URL, data = request_data, files = files, auth = self.token)
      

      if req.status_code < 200 or req.status_code > 299:
        print(req.status_code)
        print(req.text)
        sys.exit(0)

      segment_id = segment_id + 1
      bytes_sent = file.tell()

      print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

    print('Upload chunks complete.')


  def upload_finalize(self):
    print('FINALIZE')

    request_data = {
      'command': 'FINALIZE',
      'media_id': self.media_id
    }

    req = requests.post(url = MEDIA_ENDPOINT_URL, data = request_data, auth = self.token)

    self.processing_info = req.json().get('processing_info', None)
    self.check_status()

  def check_status(self):
    if self.processing_info is None:
      return

    state = self.processing_info['state']

    print('Media processing status is %s ' % state)

    if state == u'succeeded':
      return

    if state == u'failed':
      sys.exit(0)

    check_after_secs = self.processing_info['check_after_secs']
    
    print('Checking after %s seconds' % str(check_after_secs))
    time.sleep(check_after_secs)

    print('STATUS')

    request_params = {
      'command': 'STATUS',
      'media_id': self.media_id
    }

    req = requests.get(url = MEDIA_ENDPOINT_URL, params = request_params, auth = self.token)
    
    self.processing_info = req.json().get('processing_info', None)
    self.check_status()


  def tweet(self):
    request_data = {
      'status': self.text,
      'media_ids': self.media_id
    }

    req = requests.post(url = POST_TWEET_URL, data = request_data, auth = self.token)
    response = req.json()
    tweet_link = response['entities']['media'][0]['expanded_url']
    print("\nTweet link: {}".format(tweet_link))

    # uncomment for full response during debugging
    # print(json.dumps(response, sort_keys=True, indent=2))
