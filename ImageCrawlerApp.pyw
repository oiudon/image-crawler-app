import PySimpleGUI as sg
from icrawler.builtin import BingImageCrawler
import os

# テーマの選択
sg.theme("DarkBlue12")

# レイアウトの作成
layout = [[sg.T("保存先を選択し、検索ワードと最大保存枚数を入力してください。")],
          [sg.B(" 保存先 ", k="btn1"), sg.T(k="txt1", font=(None,8))],
          [sg.T("検索ワード"), sg.I(k="in1")],
          [sg.T("最大保存枚数"), sg.I(k="in2")],
          [sg.B(" 実行 ", k="btn2"), sg.T("", k="txt2")]]
win = sg.Window("検索画像収集アプリ", layout,
                font=(None,12), size=(500,160))

# 保存先フォルダ選択部分の作成
def loadFolder():
    global loadname
    global savepath
    # 保存先フォルダの読み込み
    loadname = sg.popup_get_folder("保存先フォルダを選択してください。")
    
    # 保存先フォルダが選択されなかったらreturnする
    if not loadname:
        return

    # 保存先フォルダの確定
    savepath = loadname
    win["txt1"].update(savepath)
    win["txt2"].update("")


# 実行部分の作成
def execute():
    # 保存先フォルダが選択されているか確認
    try:
        savepath
    except NameError:
        win["txt2"].update("*保存先フォルダを選択してください")
        return
    
    # 保存先フォルダが存在するか確認
    if not os.path.isdir(savepath):
        win["txt2"].update("*保存先フォルダが存在しません")
        return

    # 検索ワードの入力確認
    if v["in1"] == "":
        win["txt2"].update("*検索ワードを入力してください")
        return

    # 最大保存枚数の入力確認
    if v["in2"] == "":
        win["txt2"].update("*最大保存枚数を入力してください")
        return
    elif not v["in2"].isdigit():
        win["txt2"].update("*最大保存枚数には数字を入力してください")
        return

    # クローラーの作成
    bing_crawler = BingImageCrawler(downloader_threads=4,storage={'root_dir':savepath})
    # 画像収集の実行
    bing_crawler.crawl(keyword=v["in1"], filters=None, offset=0, max_num=int(v["in2"]))
    win["txt2"].update("保存完了")

while True:
    e, v = win.read()
    if e == "btn1":
        loadFolder()
    if e == "btn2":
        execute()
    if e == None:
        break
win.close()
