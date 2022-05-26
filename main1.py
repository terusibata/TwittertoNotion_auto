#Twitterダウンロード
import keep_alive
import json
from requests_oauthlib import OAuth1Session
import requests
import os
import time
from replit import db
#notionアップロード
from notion.client import NotionClient
from notion.block import TextBlock
from notion.block import DividerBlock
from notion.block import QuoteBlock
from notion.block import TodoBlock
from notion.block import PageBlock
from notion.block import ImageBlock
from datetime import datetime, timedelta, timezone

AK = os.environ['AK']
AS = os.environ['AS']
AT = os.environ['AT']
ATS = os.environ['ATS']
twitter = OAuth1Session(f"{AK}", f"{AS}", f"{AT}", f"{ATS}")

params = {
  'expansions'  : 'author_id,attachments.media_keys',
  'tweet.fields': 'created_at,public_metrics',
  'user.fields' : 'name',
  'media.fields' : 'duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width,alt_text',
  'max_results' : 50,
}


media_keys_datas=[]
media_keys_data_count=0
img_datas=[]
notion_upload_data=[]

json_open = open('./hololive.json', 'r')
channelnames = json.load(json_open)

jst = timezone(timedelta(hours=9), 'JST')
dt_now = datetime.now(jst)

def main():
  while True:
    for channelname in channelnames.keys():
      channelname_id = channelnames[f"{channelname}"]["id"]
      url = f"https://api.twitter.com/2/users/{channelname_id}/liked_tweets"
      res = twitter.get(url, params = params)
      tl = json.loads(res.text)
      global notion_upload_data,img_datas,dt_now

      if res.status_code == 200:
        tl = json.loads(res.text)

        # print(tl)
        # print(f"name : {tl['includes']['users'][0]['name']}")
        # print(f"user : {tl['includes']['users'][0]['username']}")
        # print('----------------------------')

        for l in tl['data']:
          try:
            media_keys_datas.clear() #配列をリセット
            notion_history_data=True
            other_data = False
            for media_data in l['attachments']['media_keys']: #media_keysを配列に代入
              if media_data in db[channelname]:
                notion_history_data=False
              media_keys_datas.append(media_data)
            
            if notion_history_data :
              print(media_keys_datas)
              print('----------------------------')
              print(l['text'])
              print(l['created_at'])
              media_keys_data_count=1 #表示のためのカウント
              for ls in tl['includes']['media']: #includesのmediaがあるだけループ
                for media_keys_data in media_keys_datas: #media_keysの数だけループ
                  if ls['media_key']==media_keys_data: #media_keysと一致するものを検索
                    if(ls['type']=='photo'): #typeが画像かを判断
                      print(str(media_keys_data_count)+"枚目の画像ダウンロード開始...")
                      print("URL : "+str(ls['url']))
                      file_name = str(media_keys_data)+".jpg"
                      response = requests.get(ls['url'].replace('.jpg','?format=jpg&name=orig'))
                      image = response.content
                      with open(file_name, "wb") as aaa:
                        aaa.write(image)
                      print(file_name+"で保存しました")
                      img_datas.append(file_name)
                      db[channelname].append(media_keys_data)
                      media_keys_data_count+=1
                    elif(ls['type']=='animated_gif'): #typeがgifかを判断
                      print(str(media_keys_data_count)+"枚目の画像ダウンロード開始...")
                      print("URL : "+str(ls['preview_image_url']))
                      file_name = str(media_keys_data)+".jpg"
                      response = requests.get(ls['preview_image_url'].replace('.jpg','?format=jpg&name=orig'))
                      image = response.content
                      with open(file_name, "wb") as aaa:
                        aaa.write(image)
                      print(file_name+"で保存しました")
                      img_datas.append(file_name)
                      db[channelname].append(media_keys_data)
                      media_keys_data_count+=1
                    else: #その他
                      print("その他画像ありツイート")
                      other_data = True
              #notionに追加 
              dt_now = datetime.now(jst)
              if other_data:
                print("notonには追加されません")
              else:
                title_data = str(l['text'][:40])+"…"
                channel_name = channelnames[f"{channelname}"]["name"]
                notion_upload_data=[channel_name,title_data,l['text'],l['created_at']]
                print("notionにアップロード開始...")
                notion_upload(channel_name)
              print('----------------------------')
              for img_data in img_datas:
                os.remove(f"./{img_data}")
              img_datas.clear()
            else:
              print("すでに追加済み")
          except KeyError: #attachments(media_keys)が存在しなかったら
            print(l['text'])
            print(l['created_at'])
            print("画像なし")
            print('----------------------------')

      else:
        print("Failed: %d" % res.status_code)

      print("チャンネル名 : "+channelnames[f"{channelname}"]["name"]+"を実行しました。")
      print("実行時間 : "+str(dt_now))
      for sleep_time_count in range(90):
        if (90-sleep_time_count)%10==0:
          print("カウント : "+str(90-sleep_time_count)+"秒")
        time.sleep(1)

  
  


#-------------------------------------------

client = NotionClient(token_v2=os.environ['token_v2'])

def notion_upload(channelname):
  page = client.get_block("https://www.notion.so/terusibata/75f9a276259242f183f3cd93ff947451")
  print("追加TOPページ : ", page.title)
  channelnamedata = False
  for child in page.children :
      if child.title==channelname:
          channelnamedata=True
          channelnamedata_id=child.id

  if channelnamedata:
      subpage_year(channelnamedata_id)
  else:
      child_newpage = page.children.add_new(PageBlock, title=channelname)
      subpage_year(child_newpage.id)

def subpage_year(page_id):
  page = client.get_block(f"https://www.notion.so/terusibata/{page_id.replace('-','')}")
  print("チャンネル名 : ", page.title)
  # page.children.add_new(TextBlock, title='追加完了')
  channelname_year_data = False
  for child in page.children :
      if child.title==str(dt_now.year)+"年":
          channelname_year_data=True
          channelnamedata_id=child.id

  if channelname_year_data:
      subpage_month(channelnamedata_id)
  else:
      child_newpage = page.children.add_new(PageBlock, title=str(dt_now.year)+"年")
      subpage_month(child_newpage.id)

def subpage_month(page_id):
  page = client.get_block(f"https://www.notion.so/terusibata/{page_id.replace('-','')}")
  print("追加年 : ", page.title)
  # page.children.add_new(TextBlock, title='追加')
  channelname_month_data = False
  for child in page.children :
      if child.title==str(dt_now.month)+"月":
          channelname_month_data=True
          channelnamedata_id=child.id

  if channelname_month_data:
      subpage_day(channelnamedata_id)
  else:
      child_newpage = page.children.add_new(PageBlock, title=str(dt_now.month)+"月")
      subpage_day(child_newpage.id)

def subpage_day(page_id):
  page = client.get_block(f"https://www.notion.so/terusibata/{page_id.replace('-','')}")
  print("追加月 : ", page.title)
  channelname_month_data = False
  for child in page.children :
      if child.title==str(dt_now.day)+"日":
          channelname_month_data=True
          channelnamedata_id=child.id

  if channelname_month_data:
      subpage_data(channelnamedata_id)
  else:
      child_newpage = page.children.add_new(PageBlock, title=str(dt_now.day)+"日")
      subpage_data(child_newpage.id)

def subpage_data(page_id):
  page = client.get_block(f"https://www.notion.so/terusibata/{page_id.replace('-','')}")
  print("追加日 : ", page.title)
  global notion_upload_data
  child_newpage = page.children.add_new(PageBlock, title=notion_upload_data[1])
  Twitter_data_upload(child_newpage.id)
  
def Twitter_data_upload(page_id):
  page = client.get_block(f"https://www.notion.so/terusibata/{page_id.replace('-','')}")
  global notion_upload_data,img_datas
  page.children.add_new(TextBlock, title=notion_upload_data[2])
  page.children.add_new(TextBlock, title='')
  page.children.add_new(DividerBlock)
  page.children.add_new(TextBlock, title='')
  for img_data in img_datas:
    image = page.children.add_new(ImageBlock).upload_file(f"./{img_data}")
  print("notionに画像アップロード完了")

keep_alive.keep_alive()

main()
