import httplib2
import os
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secret.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))

args = argparser.parse_args()
service = get_authenticated_service(args)

def liked_videos_list_by_username(service, **kwargs):
  results = service.channels().list(
    **kwargs
  ).execute()
  return results['items'][0]['id']['liked'](category = 'comedy').join(results['items'][0]['id']['liked'](category = 'music'))

def youtube_search(options):
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"],
                                 search_result["snippet"]["description"],
                                 search_result["snippet"]["tags"]))
      return videos

def train(channel_data, ran_video_data):
    ds_channel = pd.read_json(channel_data)
    ds_videos = pd.read_json(ran_video_data)
    self._train(ds_channel,ds_videos)

def _train(self, ds_channel, ds_videos):

  tf = TfidfVectorizer(analyzer='word',
                       ngram_range=(1, 3),
                       min_df=0,
                       stop_words='english')
  channel_matrix = tf.fit_transform(ds_channel['title'],ds_channel['description'],ds_channel['tags'])
  video_matrix = tf.fit_transform(ds_videos['title'],ds_videos['description'],ds_videos['tags'])

  cosine_similarities = linear_kernel(channel_matrix, video_matrix)

  for idx, row in ds_videos.iterrows():
      similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
      similar_items = [(cosine_similarities[idx][i], ds_videos['title'][i],ds_videos['description'][i],ds_videos['tags'][i])
                       for i in similar_indices]
      flattened = sum(similar_items[1:], ())

def predict(self, title, description, tags, num):

  return self.zrange(self.SIMKEY % title, description, tags,
                        0,
                        num-1,
                        withscores=True,
                        desc=True)

if __name__ == '__main__':
  search_term = "funny songs" #could use a better term here
  argparser.add_argument("--q", help="Search term", default=search_term)
  argparser.add_argument("--max-results", help="Max results", default=5000)
  args = argparser.parse_args()
  
  liked_videos = liked_videos_list_by_username(service, part='snippet,contentDetails,statistics', mine=true)

  train(liked_videos, youtube_search(args))

  first_ten_similar = []

    #poping only top 10 of similar index for variety in the types of songs/videos we'll have
  for idx, row in ds_videos.iterrows():
      first_ten_similar.push(row.predict(10)) #will return the 10 most similar

  print(first_ten_similar.sort(similar_items)[:10]) #sort by similarity score and print



