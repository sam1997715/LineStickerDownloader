import requests
from bs4 import BeautifulSoup
import tkinter as tk
import re
from tkinter import filedialog
from tkinter import messagebox
import os
import webbrowser
from urllib.request import urlretrieve
from PIL import Image

URL = "" #使用者輸入網址
DownloadLocation = "" #存圖本地路徑
Title = "" #貼圖名字
mainPic = "" #用於貼圖集的縮圖
StickerURL = []#用於貼圖集的來源網址

def getTextInput():
    global URL ,DownloadLocation ,Title ,mainPic ,StickerURL

    URL = URLbox.get("1.0","end-1c")
    
    DownloadLocation = filedialog.askdirectory()
    while(DownloadLocation == ""):
        tk.messagebox.showerror(title="請選擇路徑", message="存檔路徑為空白，請重新選擇路徑")
        DownloadLocation = filedialog.askdirectory()
    
    readURL = requests.get(URL)
    soup = BeautifulSoup(readURL.text, 'html.parser')
    Title = soup.find("ul" ,"mdCMN38Item01").find("div" ,"mdCMN38Item0lHead").find("p" ,"mdCMN38Item01Ttl").string #取得貼圖名字
    Title = re.sub(r"\?","？",Title)
    Title = re.sub(r" +","_",Title)
    mainPic = soup.find("div" ,"mdCMN38Img").find("img" ,"FnImage")['src'].replace(";compress=true", "") #取得原始圖片網站，去掉壓縮php
    firstStickerHTML = soup.find("ul" ,"mdCMN09Ul FnStickerList").find("li","mdCMN09Li FnStickerPreviewItem").find("div","mdCMN09LiInner FnImage")#擷取網頁碼直到最後一層
    firstStickerGetIndex = re.findall(r"\d{7,9}",str(firstStickerHTML))#取得8位數的貼圖編號
    firstStickerIndex = int("".join(firstStickerGetIndex))#轉換資料型態

    StickerNum = len(soup.find("ul" ,"mdCMN09Ul FnStickerList").find_all("li","mdCMN09Li FnStickerPreviewItem"))#計算個數
    for i in range(0,StickerNum):
        StickerURL.append("https://stickershop.line-scdn.net/stickershop/v1/sticker/" + str(firstStickerIndex) + "/android/sticker.png")
        firstStickerIndex += 1
        #以list型態儲存圖片來源網址
    zeroPic = requests.get(mainPic).content
    if not os.path.isdir(DownloadLocation + "/" + Title):
        os.mkdir(DownloadLocation + "/" + Title)
    urlretrieve(mainPic ,DownloadLocation + "/" + Title + "/Title.png")

    count = 1
    for pngURL in StickerURL:
        urlretrieve(pngURL ,DownloadLocation + "/" + Title + "/" + str(count) + ".png")
        count +=1

    picPath = DownloadLocation + "/" + Title
    pngList = os.listdir(picPath)
    #列出資料夾的檔案

    if not os.path.exists(picPath + "/new"):
        os.mkdir(picPath + "/new")
    #若new資料夾不存在就建立一個，用以儲存調整過後的圖片

    for pname in pngList:
            
            file = picPath + "/" + pname
            if not os.path.isfile(file):
                continue
            #如果資料夾下的物件不是檔案，就跳過(ex.資料夾)
            
            img = Image.open(file)
            #開啟圖案檔

            (w, h) = img.size
            #取得圖片大小
            if pname in ["main.png", "Title.png"]:
                rate = 100/h
            #如果檔案是封面圖片(main.png)，亦調整符合tg貼圖封面圖片的要求
                
            else:
                if (w >= h):
                    if (w < 512):
                        rate = 512/w
                else:
                    if (h < 512):
                        rate = 512/h
            #計算縮放比例

            newW = int(w * rate)
            newH = int(h * rate)
            #計算新尺寸的大小
            
            newimg = img.resize((newW, newH))
            newimg.save(picPath + "/new/" + pname)
    
    tk.messagebox.showinfo(title="完成", message="下載完成")
    StickerURL = []

def callback(lineurl):
    webbrowser.open_new(lineurl) 

def closeWindow():
    window.destroy()



window = tk.Tk()
window.title("LINE貼圖下載器")
window.minsize(280,200)

hyperlink = tk.Label(window ,text = "點我進入貼圖小舖" ,justify = "left" ,font="msjh 12 underline ", fg = "blue")
hyperlink.place(x=48, y=20)
hyperlink.bind("<Button-1>", lambda e: callback("https://store.line.me"))

explain = tk.Label(window ,text = "請輸入LINE貼圖網址" ,font="msjh 12 " ,justify = "left")
explain.place(x=48, y=43)

URLbox = tk.Text(window ,height = 1 ,width = 22 ,font="msjh 12 ")
URLbox.place(x=50, y=70)

URLButton = tk.Button(window ,height = 1 ,width = 10 ,text = "確定" ,command = getTextInput)
URLButton.place(x=50, y=120)

CloseButton = tk.Button(window ,height = 1 ,width = 10 ,text = "關閉程式" ,command = closeWindow)
CloseButton.place(x=150, y=120)
        
frame = tk.Frame(window)
window.mainloop()




