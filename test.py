from replit import db
# import json
if not "hakosbaelz" in db.keys():
  print("なし")

# json_open = open('./hololive.json', 'r')
# channelnames = json.load(json_open)

# for channelname in channelnames.keys():
#   db[channelname] = []


# import datetime
# import pytz

# now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
# print(now)

# import time

# for sleep_time_count in range(90):
#   if (90-sleep_time_count)%10==0:
#     print("カウント : "+str(90-sleep_time_count)+"秒")
#   time.sleep(1)

# from datetime import datetime, timedelta, timezone

# # JSTタイムゾーンを作成
# jst = timezone(timedelta(hours=9), 'JST')

# # JSTで、日付を作成
# now = datetime.now(jst)
# print(now)
# # 出力例：2018-12-06 01:18:21.852966+09:00

#Twitterダウンロード
# import keep_alive
# import json
# from requests_oauthlib import OAuth1Session
# import requests
# import os
# import time
# from replit import db

# AK = os.environ['AK']
# AS = os.environ['AS']
# AT = os.environ['AT']
# ATS = os.environ['ATS']
# twitter = OAuth1Session(f"{AK}", f"{AS}", f"{AT}", f"{ATS}")

# params = {
#   'expansions'  : 'author_id,attachments.media_keys',
#   'tweet.fields': 'created_at,public_metrics',
#   'user.fields' : 'name',
#   'media.fields' : 'duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width,alt_text',
#   'max_results' : 5,
#   'pagination_token':''
# }

# url = f"https://api.twitter.com/2/users/880317891249188864/liked_tweets"
# res = twitter.get(url, params = params)
# tl = json.loads(res.text)

# print(tl)