import os
import json
import tqdm
import requests
import multiprocessing
import pydub
import PIL
import pylrc

from PySide6.QtCore import (QRect, Qt)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
        QMainWindow, QProgressBar, QPushButton, QScrollArea,
        QTabWidget, QWidget, QFileDialog)

def initialise_json():
        return

def button_remove():
        return

def button_re_add():
        return

def button_add_download():
        return

def button_download():
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

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName(u"MainWindow")
                MainWindow.setFixedSize(792, 590)
                self.centralwidget = QWidget(MainWindow)
                self.centralwidget.setObjectName(u"centralwidget")
                self.label_directory = QLabel(self.centralwidget)
                self.label_directory.setObjectName(u"label_directory")
                self.label_directory.setGeometry(QRect(100, 40, 491, 21))
                self.label_directory.setFrameShape(QFrame.Box)
                self.label_directory.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
                self.label_directory.setWordWrap(True)
                self.label_directory.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.label_directory.setText(u"")

                self.push_button_directory = QPushButton(self.centralwidget)
                self.push_button_directory.setObjectName(u"push_button_directory")
                self.push_button_directory.setGeometry(QRect(600, 38, 111, 24))
                self.push_button_directory.clicked.connect(self.select_directory)
                self.push_button_directory.setText(u"Select Directory")

                self.tab_widget = QTabWidget(self.centralwidget)
                self.tab_widget.setObjectName(u"tab_widget")
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
                self.tab_widget_tab_downloaded.setObjectName(u"tab_widget_tab_downloaded")
                self.create_tab_layout_base(self.tab_widget_tab_downloaded, 0)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloaded), u"Downloaded")

                self.tab_widget_tab_not_downloaded = QWidget()
                self.tab_widget_tab_not_downloaded.setObjectName(u"tab_widget_tab_not_downloaded")
                self.create_tab_layout_base(self.tab_widget_tab_not_downloaded, 1)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_not_downloaded), u"Not Downloaded")

                self.tab_widget_tab_downloading = QWidget()
                self.tab_widget_tab_downloading.setObjectName(u"tab_widget_tab_downloading")
                self.create_tab_layout_base(self.tab_widget_tab_downloading, 2)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloading), u"Downloading")

                self.tab_widget_tab_removed = QWidget()
                self.tab_widget_tab_removed.setObjectName(u"tab_widget_tab_removed")
                self.create_tab_layout_base(self.tab_widget_tab_removed, 3)
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_removed), u"Removed")

                MainWindow.setCentralWidget(self.centralwidget)

                self.tab_widget.setCurrentIndex(1)

        def select_directory(self):
                file_explorer = QFileDialog.getExistingDirectory(MainWindow, 'Open Folder', '')
                if os.path.isdir(file_explorer):
                        self.label_directory.setText(file_explorer)
                        os.chdir(file_explorer)

        def create_tab_layout_base(self, tab_widget_objects, index):
                self.scrollArea = QScrollArea(tab_widget_objects)
                self.scrollArea.setObjectName(u"scrollArea")
                self.scrollArea.setGeometry(QRect(0, 30, 531, 371))
                self.scrollArea.setWidgetResizable(True)
                self.scrollAreaWidgetContents = QWidget()
                self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
                self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 529, 369))
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)

                self.check_box_select_all = QCheckBox(tab_widget_objects)
                self.check_box_select_all.setObjectName(u"check_box_select_all")
                self.check_box_select_all.setGeometry(QRect(20, 10, 16, 20))
                self.check_box_select_all.setChecked(False)
                self.check_box_select_all.setText("")

                self.label_album_header = QLabel(tab_widget_objects)
                self.label_album_header.setObjectName(u"label_album_header")
                self.label_album_header.setGeometry(QRect(50, 10, 49, 16))
                self.label_album_header.setText(u"Album")

                self.push_button_first = QPushButton(tab_widget_objects)
                self.push_button_first.setObjectName(u"push_button_first")
                self.push_button_first.setGeometry(QRect(540, 40, 75, 48))
                self.push_button_first.clicked.connect(push_button_dictionary.get(index))
                self.push_button_first.setText(push_button_text_list[index])

                if index == 1 or index == 2:
                        self.push_button_second = QPushButton(tab_widget_objects)
                        self.push_button_second.setObjectName(u"push_button_second")
                        self.push_button_second.setGeometry(QRect(540, 120, 75, 48))
                        self.push_button_second.setText(push_button_text_list[index + 3])
                        self.push_button_second.clicked.connect(push_button_dictionary.get(index + 3))

                        if index == 2:
                                self.label_progress_header = QLabel(tab_widget_objects)
                                self.label_progress_header.setObjectName(u"label_progress_header")
                                self.label_progress_header.setGeometry(QRect(260, 10, 51, 16))
                                self.label_progress_header.setText(u"Progress")

                                self.label_estimated_time_header = QLabel(tab_widget_objects)
                                self.label_estimated_time_header.setObjectName(u"label_estimated_time_header")
                                self.label_estimated_time_header.setGeometry(QRect(430, 10, 91, 16))
                                self.label_estimated_time_header.setText(u"Estimated Time")

                                self.check_box_instrumental = QCheckBox(tab_widget_objects)
                                self.check_box_instrumental.setObjectName(u"check_box_instrumental")
                                self.check_box_instrumental.setGeometry(QRect(20, 420, 91, 20))
                                self.check_box_instrumental.setText(u"Instrumentals")

                                self.check_box_lyrics = QCheckBox(tab_widget_objects)
                                self.check_box_lyrics.setObjectName(u"check_box_lyrics")
                                self.check_box_lyrics.setGeometry(QRect(140, 420, 51, 20))
                                self.check_box_lyrics.setText(u"Lyrics")

                                self.check_box_cover = QCheckBox(tab_widget_objects)
                                self.check_box_cover.setObjectName(u"check_box_cover")
                                self.check_box_cover.setGeometry(QRect(220, 420, 51, 20))
                                self.check_box_cover.setText(u"Cover")

                self.tab_widget.addTab(tab_widget_objects, "")

        def create_tab_scrollable_content():
                return
               #widgets_scrollable_dictionary = {}
        #        for i in range(len(temp_var)):
        #                widgets_scrollable_dictionary[(i, 0)] = QCheckBox(tab_widget_objects)
        #                widgets_scrollable_dictionary[(i, 0)].setGeometry(QRect(20, 10, 16, 20))
        #                widgets_scrollable_dictionary[(i, 0)].setText("")

        #                widgets_scrollable_dictionary[(i, 1)] = QLabel(tab_widget_objects)
        #                widgets_scrollable_dictionary[(i, 1)].setText(temp_var_album_names)
        #                widgets_scrollable_dictionary[(i, 1)].setGeometry(QRect(51, 51, 171, 16))

        def create_tab_scrollable_content_download():
                return
        #        widgets_scrollable_dictionary[(i, 2)] = QProgressBar(tab_widget_objects)
        #        widgets_scrollable_dictionary[(i, 2)].setGeometry(QRect(260, 20, 151, 20))
        #        widgets_scrollable_dictionary[(i, 2)].setValue(1)

        #        widgets_scrollable_dictionary[(i, 3)] = QLabel(tab_widget_objects)
        #        widgets_scrollable_dictionary[(i, 3)].setGeometry(QRect(430, 20, 41, 16))
        #        widgets_scrollable_dictionary[(i, 3)].setText(u"00:11:11")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())