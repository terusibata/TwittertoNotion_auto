import glob
import os

def remove():
  remove_img_list = glob.glob("./*.jpg")
  print(str(len(remove_img_list))+"個の画像を削除します")
  
  for remove_img in remove_img_list:
    os.remove(remove_img)