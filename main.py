import os
import json
import tqdm
import requests
import multiprocessing
import pydub
import PIL
import pylrc

from PySide6.QtCore import (QRect, Qt)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel, QMainWindow, QProgressBar, QPushButton, QScrollArea, QTabWidget, QWidget, QFileDialog, QGridLayout)

json_path_list = ["downloaded_albums.json", "not_downloaded_albums.json", "downloading_albums.json", "removed_albums.json", "all_albums.json"]

widgets_scrollable_dictionary = {0:{},
                                1:{},
                                2:{},
                                3:{}}

def api_get_albums(): 
        global api_monster_siren_albums_data
        api_monster_siren_albums_data = []
        s = requests.session()
        api_monster_siren_albums_data_raw = s.get("https://monster-siren.hypergryph.com/api/albums", headers={'Content-Type': 'application/json'}).json()['data']

        for i in api_monster_siren_albums_data_raw:
                api_monster_siren_albums_data.append([i['cid'], i['name']])

def initialise_json():
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
        with open(json_path_list[4], "r", encoding="utf8") as all_albums_list:
                for i in data:
                        if i in all_albums_list.read():
                                return False
                        else:
                                return True
                
def update_albums_list():
        all_albums_list_missing = filter(check_new_albums, api_monster_siren_albums_data)
        with open(json_path_list[4], "a", encoding="utf-8") as f, open(json_path_list[1], "a", encoding="utf-8") as f2:
                for i in all_albums_list_missing:
                        json.dump(i, f, ensure_ascii=False)
                        json.dump(i, f2, ensure_ascii=False)

def button_remove(index):         # work on this next    /            /           /           /           /
        try:
                for i in range(widgets_scrollable_dictionary[index]):
                        if widgets_scrollable_dictionary[index][(i, 0)].isChecked():
                                return
        except: 
                return

def button_re_add(index):
        return

def button_add_download(index):
        return

def button_download(index):
        return

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
                                
def box_instrumental():
        return

def box_lyrics():
        return

def box_cover():
        return

push_button_dictionary = {
        0: button_remove,
        1: button_remove,
        2: button_remove,
        3: button_re_add,
        4: button_add_download,
        5: button_download
}

push_button_text_list = ["Remove", "Remove", "Remove", "Re-add", "Add to\nDownload", "Download"]

check_box_select_all_dictionary = {}
push_button_one_dictionary = {}
push_button_two_dictionary = {}

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setFixedSize(792, 590)
                self.centralwidget = QWidget(MainWindow)
                self.label_directory = QLabel(self.centralwidget)
                self.label_directory.setGeometry(QRect(100, 40, 491, 21))
                self.label_directory.setFrameShape(QFrame.Box)
                self.label_directory.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
                self.label_directory.setWordWrap(True)
                self.label_directory.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.label_directory.setText(u"")

                self.push_button_directory = QPushButton(self.centralwidget)
                self.push_button_directory.setGeometry(QRect(600, 38, 111, 24))
                self.push_button_directory.clicked.connect(self.select_directory)
                self.push_button_directory.setText(u"Select Directory")

                self.tab_widget = QTabWidget(self.centralwidget)
                self.tab_widget.setGeometry(QRect(70, 80, 651, 461))
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
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloaded), u"Downloaded")

                self.tab_widget_tab_not_downloaded = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_not_downloaded, 1)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_not_downloaded), u"Not Downloaded")

                self.tab_widget_tab_downloading = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_downloading, 2)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloading), u"Downloading")

                self.tab_widget_tab_removed = QWidget()
                self.create_tab_layout_base(self.tab_widget_tab_removed, 3)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_removed), u"Removed")

                MainWindow.setCentralWidget(self.centralwidget)
                self.tab_widget.setCurrentIndex(1)

                api_get_albums()
                initialise_json()
                update_albums_list()

        def select_directory(self):
                file_explorer = QFileDialog.getExistingDirectory(MainWindow, "Open Folder", "")
                if os.path.isdir(file_explorer):
                        self.label_directory.setText(file_explorer)
                        #os.chdir(file_explorer)

        def create_tab_layout_base(self, tab_widget_objects, index):
                self.scrollArea = QScrollArea(tab_widget_objects)
                self.scrollArea.setWidgetResizable(True)
                self.scrollArea.setGeometry(QRect(0, 30, 531, 371))
                self.scrollAreaWidgetContents = QWidget()
                self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 529, 369))
                self.widgets_layout = QGridLayout()
                self.scrollAreaWidgetContents.setLayout(self.widgets_layout)
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)

                check_box_select_all_dictionary[index] = QCheckBox(tab_widget_objects)
                check_box_select_all_dictionary[index].setGeometry(QRect(20, 10, 16, 20))
                check_box_select_all_dictionary[index].setChecked(False)
                check_box_select_all_dictionary[index].setText("")
                check_box_select_all_dictionary[index].clicked.connect(lambda : box_select_all(index))

                self.label_album_header = QLabel(tab_widget_objects)
                self.label_album_header.setGeometry(QRect(60, 10, 49, 16))
                self.label_album_header.setText(u"Album")

                push_button_one_dictionary[index] = QPushButton(tab_widget_objects)
                push_button_one_dictionary[index].setGeometry(QRect(540, 40, 75, 48))
                push_button_one_dictionary[index].setText(push_button_text_list[index])

                if index == 0 or index == 1 or index == 2:
                        push_button_one_dictionary[index].clicked.connect(button_remove(index))
                else:
                        push_button_one_dictionary[index].clicked.connect(button_re_add(index))

                if index == 1 or index == 2:
                        push_button_two_dictionary[index] = QPushButton(tab_widget_objects)
                        push_button_two_dictionary[index].setGeometry(QRect(540, 120, 75, 48))
                        push_button_two_dictionary[index].setText(push_button_text_list[index + 3])

                        if index == 1:
                                push_button_two_dictionary[index].clicked.connect(button_add_download)
                        else:
                                push_button_two_dictionary[index].clicked.connect(button_download(index))

                        if index == 2:
                                self.label_progress_header = QLabel(tab_widget_objects)
                                self.label_progress_header.setGeometry(QRect(333, 10, 51, 16))
                                self.label_progress_header.setText(u"Progress")

                                self.check_box_instrumental = QCheckBox(tab_widget_objects)
                                self.check_box_instrumental.setGeometry(QRect(20, 420, 91, 20))
                                self.check_box_instrumental.setText(u"Instrumentals")
                                self.check_box_instrumental.clicked.connect(box_instrumental)

                                self.check_box_lyrics = QCheckBox(tab_widget_objects)
                                self.check_box_lyrics.setGeometry(QRect(140, 420, 51, 20))
                                self.check_box_lyrics.setText(u"Lyrics")
                                self.check_box_lyrics.clicked.connect(box_lyrics)

                                self.check_box_cover = QCheckBox(tab_widget_objects)
                                self.check_box_cover.setGeometry(QRect(220, 420, 51, 20))
                                self.check_box_cover.setText(u"Cover")
                                self.check_box_cover.clicked.connect(box_cover)

                self.tab_widget.addTab(tab_widget_objects, "")
                self.create_tab_scrollable_content(tab_widget_objects, index)
                if index == 2:
                        self.create_tab_scrollable_content_download(tab_widget_objects, index)

        def create_tab_scrollable_content(self, tab_widget_objects, index):
                if os.stat(json_path_list[index]).st_size == 0:
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

                                        self.widgets_layout.addWidget(widgets_scrollable_dictionary[index][(i, 0)], i, 0)
                                        self.widgets_layout.addWidget(widgets_scrollable_dictionary[index][(i, 1)], i, 1)
                except:
                        return

        def create_tab_scrollable_content_download(self, tab_widget_objects, index):
                if os.stat(json_path_list[index]).st_size == 0:
                        return
                
                with open (json_path_list[index], encoding="utf-8") as f:
                        y = json.load(f)
                        for i in range(len(y)):
                                widgets_scrollable_dictionary[index][(i, 2)].setFixedSize(255, 25)
                                widgets_scrollable_dictionary[index][(i, 2)] = QProgressBar(tab_widget_objects)
                                widgets_scrollable_dictionary[index][(i, 2)].setValue(50)
                                widgets_scrollable_dictionary[index][(i, 2)].setFixedSize(160, 25)

                                self.widgets_layout.addWidget(widgets_scrollable_dictionary[index][(i, 2)], i, 2)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())