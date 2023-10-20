import os
import json
import requests
from PIL import Image
import multiprocessing
from pydub import AudioSegment
from mutagen.flac import FLAC, Picture

from PySide6.QtCore import (QRect, Qt)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QMainWindow, QPushButton, QScrollArea, QTabWidget, QWidget, QGridLayout)

file_explorer = os.getcwd() + "\Albums"
if os.path.exists(file_explorer) == False:
        os.mkdir(file_explorer)

json_path_list = ["downloaded_albums.json", "not_downloaded_albums.json", "downloading_albums.json", "removed_albums.json", "all_albums.json"]
push_button_text_list = ["Remove", "Remove", "Remove", "Re-add", "Add to\nDownload", "Download"]

widgets_scrollable_dictionary = {0:{},
                                1:{},
                                2:{},
                                3:{}}

api_monster_siren_albums_data = []

check_box_select_all_dictionary = {}
push_button_one_dictionary = {}
push_button_two_dictionary = {}
widgets_layout_dictionary = {}

s = requests.Session()
api_monster_siren_albums_data_raw = s.get("https://monster-siren.hypergryph.com/api/albums", headers={"Content-Type": "application/json"}).json()["data"]

for i in api_monster_siren_albums_data_raw:
        api_monster_siren_albums_data.append([i["cid"], i["name"]])

if os.path.exists(json_path_list[4]) == False:
        with open(json_path_list[4], "w", encoding="utf-8") as f:
                json.dump(api_monster_siren_albums_data, f, ensure_ascii=False)

if os.path.exists(json_path_list[1]) == False:
        with open(json_path_list[1], "w", encoding="utf-8") as f:
                json.dump(api_monster_siren_albums_data, f, ensure_ascii=False)

for json_path in json_path_list:
        if os.path.exists(json_path) == False:
                json_create = open(json_path, "x", encoding="utf8")

def check_new_albums(data):
        with open(json_path_list[4], "r", encoding="utf8") as f:
                for i in data:
                        if i in f.read():
                                return False
                        else:
                                return True
                
all_albums_list_missing = list(filter(check_new_albums, api_monster_siren_albums_data))

if len(all_albums_list_missing) > 0:
        with open(json_path_list[4], encoding="utf-8") as f, open(json_path_list[1], encoding="utf-8") as f2:
                y = json.load(f)
                y2 = json.load(f2)

                for i in all_albums_list_missing:
                        y.append(i)
                        y2.append(i)

        with open(json_path_list[4], "w", encoding="utf-8") as f, open(json_path_list[1], "w", encoding="utf-8") as f2:
                json.dump(y, f, ensure_ascii=False)
                json.dump(y2, f2, ensure_ascii=False)

def button_one(self, index, destination):
        try:
                delete_list = []
                with open (json_path_list[index], encoding="utf-8") as f:
                        y = json.load(f)

                        for i in range(len(y)):
                                if widgets_scrollable_dictionary[index][(i, 0)].isChecked():
                                        delete_list.append(y[i])
                        
                        if os.stat(json_path_list[destination]).st_size == 0:
                                y2 = []
                        else:
                                with open (json_path_list[destination], "r", encoding="utf-8") as f2:
                                        y2 = json.load(f2)
                        
                        for i in delete_list:
                                y.remove(i)
                                y2.append(i)

                with open (json_path_list[destination], "w", encoding="utf-8") as f2:
                        json.dump(y2, f2, ensure_ascii=False)

                with open (json_path_list[index], "w", encoding="utf-8") as f:
                        json.dump(y, f, ensure_ascii=False)

                for i in range(len(check_box_select_all_dictionary)):
                        check_box_select_all_dictionary[i].setChecked(False)

                self.refresh_tab_scrollable_content()
        except: 
                return

def validate_file_name(filename):
        new_name = filename.strip()
        new_name = new_name.replace(":", "：")
        new_name = new_name.replace("?", "？")
        new_name = new_name.replace("%", "％")
        new_name = new_name.replace("*", "＊")
        new_name = new_name.replace("|", "|")
        return new_name

def process_songs(albums):
                try:
                        album_path = file_explorer + "\\" + validate_file_name(albums[1]) + "\\"
                        if not os.path.exists(album_path):
                                os.mkdir(album_path)

                        r = s.get("https://monster-siren.hypergryph.com/api/album/{}/detail".format(albums[0]), headers={"Content-Type": "application/json"}).json()["data"]
                        
                        if ".png" in r["coverUrl"]:
                                with open(album_path + "\\cover.png", 'wb') as f2:
                                        f2.write(s.get(r["coverUrl"]).content)

                        elif ".jpg" in r["coverUrl"]:
                                with open(album_path + "\\cover.jpg", 'wb') as f2:
                                        f2.write(s.get(r["coverUrl"]).content)
                                        image_convert = Image.open(album_path + "\\cover.jpg")
                                        image_convert.save(album_path + "\\cover.png")

                        elif ".jpeg" in r["coverUrl"]:
                                with open(album_path + "\\cover.jpeg", 'wb') as f2:
                                        f2.write(s.get(r["coverUrl"]).content)
                                        image_convert = Image.open(album_path + "\\cover.jpeg")
                                        image_convert.save(album_path + "\\cover.png")

                        if ".jpg" in r["coverUrl"]:
                                os.remove(album_path + "\\cover.jpg")
                        elif ".jpeg" in r["coverUrl"]:
                                os.remove(album_path + "\\cover.jpeg")


                        for i in range(len(r["songs"])):
                                temp2 = validate_file_name(r["songs"][i]["name"])

                                if "Instrumental" in temp2:                                                                                               # prevents instrumentals from being downloaded
                                        break

                                r2 = s.get("https://monster-siren.hypergryph.com/api/song/{}".format(r["songs"][i]["cid"]), headers={"Content-Type": "application/json"}).json()["data"]

                                if ".flac" in r2["sourceUrl"]:
                                        with open(album_path + "\\" + temp2 + ".flac", 'wb') as f4:
                                                f4.write(s.get(r2["sourceUrl"]).content)
                                                audio_file = AudioSegment.from_file(album_path + "\\" + temp2 + ".flac", format="flac")
                                elif ".mp3" in r2["sourceUrl"]:
                                        with open(album_path + "\\" + temp2 + ".mp3", 'wb') as f4:
                                                f4.write(s.get(r2["sourceUrl"]).content)
                                                audio_file = AudioSegment.from_file(album_path + "\\" + temp2 + ".mp3", format="mp3")
                                elif ".wav" in r2["sourceUrl"]:
                                        with open(album_path + "\\" + temp2 + ".wav", 'wb') as f4:
                                                f4.write(s.get(r2["sourceUrl"]).content)
                                                audio_file = AudioSegment.from_file(album_path + "\\" + temp2 + ".wav", format="wav")
                                
                                audio_modify = audio_file.export(album_path + "\\" + temp2 + ".flac", format="flac")

                                if ".mp3" in r2["sourceUrl"]:
                                        os.remove(album_path + "\\" + temp2 + ".mp3")
                                elif ".wav" in r2["sourceUrl"]:
                                        os.remove(album_path + "\\" + temp2 + ".wav")

                                audio_flac = FLAC(album_path + "\\" + temp2 + ".flac")

                                image = Picture()
                                image.type = 3
                                image.mime = "image/png"

                                with open(album_path + "\\cover.png", 'rb') as f5:
                                        image.data = f5.read()

                                audio_flac.add_picture(image)
                                audio_flac["album"] = r["name"]
                                audio_flac["artist"] = r2["artists"]
                                audio_flac["title"] = r2["name"]

                                audio_flac.save()
                except requests.exceptions.Timeout:
                        process_songs(albums)
                except requests.exceptions.HTTPError:
                        process_songs(albums)
                except requests.exceptions.ConnectionError:
                        process_songs(albums)
                except requests.exceptions.RetryError:
                        process_songs(albums)
                except Exception as ex: 
                        print(ex)
                        process_songs(albums)

def pool_handler(albums):
        pool = multiprocessing.Pool() 
        pool.map(process_songs, albums)

def button_download(self, index):
        with open (json_path_list[2], encoding="utf-8") as f:
                y = json.load(f)

                download_list = []
                for i in range(len(y)):
                        if widgets_scrollable_dictionary[index][(i, 0)].isChecked():
                                download_list.append(y[i])
                
                pool_handler(download_list)

        button_one(self, index, 0)

def box_select_all(index):
        try:
                with open (json_path_list[index], encoding="utf-8") as f:
                        y = json.load(f)
                if check_box_select_all_dictionary[index].isChecked():
                        for i in range(len(y)):
                                widgets_scrollable_dictionary[index][(i, 0)].setCheckState(Qt.Checked)
                else:
                        for i in range(len(y)):
                                widgets_scrollable_dictionary[index][(i, 0)].setCheckState(Qt.Unchecked)
        except:
                return
                        
class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setFixedSize(750, 530)
                MainWindow.setWindowTitle("塞壬唱片-MSR Downloader")
                self.centralwidget = QWidget(MainWindow)
                self.tab_widget = QTabWidget(self.centralwidget)
                self.tab_widget.setGeometry(QRect(49, 30, 651, 461))
                self.tab_widget.setContextMenuPolicy(Qt.NoContextMenu)
                self.tab_widget.setLayoutDirection(Qt.LeftToRight)
                self.tab_widget.setAutoFillBackground(False)
                self.tab_widget.setTabPosition(QTabWidget.West)
                self.tab_widget.setTabShape(QTabWidget.Rounded)
                self.tab_widget.setElideMode(Qt.ElideLeft)
                self.tab_widget.setUsesScrollButtons(False)
                self.tab_widget.setMovable(False)
                self.tab_widget.setTabBarAutoHide(False)
                
                self.tab_widget_tab_downloaded = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_downloaded, 0)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloaded), "Downloaded")

                self.tab_widget_tab_not_downloaded = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_not_downloaded, 1)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_not_downloaded), "Not Downloaded")

                self.tab_widget_tab_downloading = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_downloading, 2)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloading), "Downloading")

                self.tab_widget_tab_removed = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_removed, 3)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_removed), "Removed")

                MainWindow.setCentralWidget(self.centralwidget)
                self.tab_widget.setCurrentIndex(1)

        def create_tab_layout_base(self, tab_widget_objects, index):
                self.scrollArea = QScrollArea(tab_widget_objects)
                self.scrollArea.setWidgetResizable(True)
                self.scrollArea.setGeometry(QRect(0, 30, 531, 371))
                self.scrollAreaWidgetContents = QWidget()
                self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 529, 369))
                widgets_layout_dictionary[index] = QGridLayout()
                self.scrollAreaWidgetContents.setLayout(widgets_layout_dictionary[index])
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)

                check_box_select_all_dictionary[index] = QCheckBox(tab_widget_objects)
                check_box_select_all_dictionary[index].setGeometry(QRect(20, 10, 16, 20))
                check_box_select_all_dictionary[index].setChecked(False)
                check_box_select_all_dictionary[index].setText("")
                check_box_select_all_dictionary[index].clicked.connect(lambda : box_select_all(index))

                self.label_album_header = QLabel(tab_widget_objects)
                self.label_album_header.setGeometry(QRect(60, 10, 49, 16))
                self.label_album_header.setText("Album")

                push_button_one_dictionary[index] = QPushButton(tab_widget_objects)
                push_button_one_dictionary[index].setGeometry(QRect(540, 40, 75, 48))
                push_button_one_dictionary[index].setText(push_button_text_list[index])

                if index == 0 or index == 1 or index == 2:
                        push_button_one_dictionary[index].clicked.connect(lambda : button_one(self, index, 3))
                else:
                        push_button_one_dictionary[index].clicked.connect(lambda : button_one(self, index, 1))

                if index == 1 or index == 2:
                        push_button_two_dictionary[index] = QPushButton(tab_widget_objects)
                        push_button_two_dictionary[index].setGeometry(QRect(540, 120, 75, 48))
                        push_button_two_dictionary[index].setText(push_button_text_list[index + 3])

                        if index == 1:
                                push_button_two_dictionary[index].clicked.connect(lambda: button_one(self, index, 2))
                        else:
                                push_button_two_dictionary[index].clicked.connect(lambda: button_download(self, index))
                                
                self.tab_widget.addTab(tab_widget_objects, "")
                self.create_tab_scrollable_content(tab_widget_objects, index)

        def create_tab_scrollable_content(self, tab_widget_objects, index): 
                try:
                        if os.stat(json_path_list[index]).st_size == 0:
                                return
                except:
                        return

                try:
                        with open (json_path_list[index], encoding="utf-8") as f:
                                y = json.load(f)
                                for i in range(len(y)):
                                        widgets_scrollable_dictionary[index][(i, 0)] = QCheckBox(tab_widget_objects)
                                        widgets_scrollable_dictionary[index][(i, 0)].setText("")
                                        widgets_scrollable_dictionary[index][(i, 0)].setFixedSize(25, 25)

                                        widgets_scrollable_dictionary[index][(i, 1)] = QLabel(tab_widget_objects)
                                        widgets_scrollable_dictionary[index][(i, 1)].setText(str(y[i][1]))
                                        widgets_scrollable_dictionary[index][(i, 1)].setFixedSize(432, 25)

                                        widgets_layout_dictionary[index].addWidget(widgets_scrollable_dictionary[index][(i, 0)], i, 0)
                                        widgets_layout_dictionary[index].addWidget(widgets_scrollable_dictionary[index][(i, 1)], i, 1)
                except:
                        return

        def delete_tab_scrollable_content(self, index):
                for i in reversed(range(widgets_layout_dictionary[index].count())): 
                        widgets_layout_dictionary[index].itemAt(i).widget().deleteLater()

        def refresh_tab_scrollable_content(self): 
                self.delete_tab_scrollable_content(0)
                self.delete_tab_scrollable_content(1)
                self.delete_tab_scrollable_content(2)
                self.delete_tab_scrollable_content(3)

                self.create_tab_scrollable_content(self.tab_widget_tab_downloaded, 0)
                self.create_tab_scrollable_content(self.tab_widget_tab_not_downloaded, 1)
                self.create_tab_scrollable_content(self.tab_widget_tab_downloading, 2)
                self.create_tab_scrollable_content(self.tab_widget_tab_removed, 3)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())