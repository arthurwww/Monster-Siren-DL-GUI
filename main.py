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

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName(u"MainWindow")
                MainWindow.resize(792, 490)
                self.centralwidget = QWidget(MainWindow)
                self.centralwidget.setObjectName(u"centralwidget")
                self.label_directory = QLabel(self.centralwidget)
                self.label_directory.setObjectName(u"label_directory")
                self.label_directory.setGeometry(QRect(100, 40, 491, 21))
                self.label_directory.setFrameShape(QFrame.Box)
                self.label_directory.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
                self.label_directory.setWordWrap(True)
                self.label_directory.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.push_button_directory = QPushButton(self.centralwidget)
                self.push_button_directory.setObjectName(u"push_button_directory")
                self.push_button_directory.setGeometry(QRect(600, 38, 111, 24))
                self.push_button_directory.clicked.connect(self.select_directory)

                self.tab_widget = QTabWidget(self.centralwidget)
                self.tab_widget.setObjectName(u"tab_widget")
                self.tab_widget.setGeometry(QRect(70, 80, 651, 361))
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
                
        #        self.push_button_remove = QPushButton(self.tab_widget_tab_downloaded)
        #        self.push_button_remove.setObjectName(u"push_button_remove")
        #        self.push_button_remove.setGeometry(QRect(540, 40, 75, 24))

                self.create_tab_layout_base(self.tab_widget_tab_downloaded)

                self.tab_widget_tab_not_downloaded = QWidget()
                self.tab_widget_tab_not_downloaded.setObjectName(u"tab_widget_tab_not_downloaded")

                self.create_tab_layout_base(self.tab_widget_tab_not_downloaded)

        #        self.push_button_remove_2 = QPushButton(self.tab_widget_tab_not_downloaded)
        #        self.push_button_remove_2.setObjectName(u"push_button_remove_2")
        #        self.push_button_remove_2.setGeometry(QRect(540, 40, 75, 24))
        #        self.push_button_download = QPushButton(self.tab_widget_tab_not_downloaded)
        #        self.push_button_download.setObjectName(u"push_button_download")
        #        self.push_button_download.setGeometry(QRect(540, 270, 75, 24))
        #        self.check_box_instrumental = QCheckBox(self.tab_widget_tab_not_downloaded)
        #        self.check_box_instrumental.setObjectName(u"check_box_instrumental")
        #        self.check_box_instrumental.setGeometry(QRect(20, 320, 91, 20))
        #        self.check_box_lyrics = QCheckBox(self.tab_widget_tab_not_downloaded)
        #        self.check_box_lyrics.setObjectName(u"check_box_lyrics")
        #        self.check_box_lyrics.setGeometry(QRect(120, 320, 51, 20))
        #        self.check_box_cover = QCheckBox(self.tab_widget_tab_not_downloaded)
        #        self.check_box_cover.setObjectName(u"check_box_cover")
        #        self.check_box_cover.setGeometry(QRect(180, 320, 51, 20))

        #        self.progress_bar_album_1 = QProgressBar(self.scrollAreaWidgetContents_2)
        #        self.progress_bar_album_1.setObjectName(u"progress_bar_album_1")
        #        self.progress_bar_album_1.setGeometry(QRect(260, 20, 151, 20))
        #        self.progress_bar_album_1.setValue(24)
        #        self.label_estimated_time_1 = QLabel(self.scrollAreaWidgetContents_2)
        #        self.label_estimated_time_1.setObjectName(u"label_estimated_time_1")
        #        self.label_estimated_time_1.setGeometry(QRect(430, 20, 41, 16))

                self.label_progress_header = QLabel(self.tab_widget_tab_not_downloaded)
                self.label_progress_header.setObjectName(u"label_progress_header")
                self.label_progress_header.setGeometry(QRect(260, 10, 51, 16))
                self.label_estimated_time_header = QLabel(self.tab_widget_tab_not_downloaded)
                self.label_estimated_time_header.setObjectName(u"label_estimated_time_header")
                self.label_estimated_time_header.setGeometry(QRect(430, 10, 91, 16))

                self.tab_widget_tab_removed = QWidget()
                self.tab_widget_tab_removed.setObjectName(u"tab_widget_tab_removed")

                self.create_tab_layout_base(self.tab_widget_tab_removed)

        #        self.push_button_re_add = QPushButton(self.tab_widget_tab_removed)
        #        self.push_button_re_add.setObjectName(u"push_button_re_add")
        #        self.push_button_re_add.setGeometry(QRect(540, 40, 75, 24))

                MainWindow.setCentralWidget(self.centralwidget)

                self.retranslateUi()
                self.tab_widget.setCurrentIndex(0)

        def retranslateUi(self):
                self.label_directory.setText(u"")
                self.push_button_directory.setText(u"Select Directory")
        #        self.push_button_remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        #        self.check_box_album_1.setText("")

        #        self.label_album_1.setText(QCoreApplication.translate("MainWindow", u"Album Name", None))
        #        self.push_button_remove_2.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        #        self.push_button_download.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        #        self.check_box_instrumental.setText(QCoreApplication.translate("MainWindow", u"Instrumentals", None))
        #        self.check_box_lyrics.setText(QCoreApplication.translate("MainWindow", u"Lyrics", None))
        #        self.check_box_cover.setText(QCoreApplication.translate("MainWindow", u"Cover", None))
        #        self.check_box_album_2.setText("")
        #        self.label_album_name_1.setText(QCoreApplication.translate("MainWindow", u"Album Name", None))
        #        self.label_estimated_time_1.setText(QCoreApplication.translate("MainWindow", u"00:11:11", None))
                self.label_progress_header.setText(u"Progress")
                self.label_estimated_time_header.setText(u"Estimated Time")
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_downloaded), u"Downloaded")
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_not_downloaded), u"Not Downloaded")
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_widget_tab_removed), u"Removed")
        #        self.push_button_re_add.setText(QCoreApplication.translate("MainWindow", u"Re-add", None))
        #        self.check_box_album_3.setText("")
        #        self.label_album_name_2.setText(QCoreApplication.translate("MainWindow", u"Album Name", None))

        def select_directory(self):
                file_explorer = QFileDialog.getExistingDirectory(MainWindow, 'Open Folder', '')
                if os.path.isdir(file_explorer):
                        self.label_directory.setText(file_explorer)
                        os.chdir(file_explorer)

        def create_tab_layout_base(self, tab_widget_objects):
                self.scrollArea = QScrollArea(tab_widget_objects)
                self.scrollArea.setObjectName(u"scrollArea")
                self.scrollArea.setGeometry(QRect(0, 30, 531, 271))
                self.scrollArea.setWidgetResizable(True)
                self.scrollAreaWidgetContents = QWidget()
                self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
                self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 529, 269))
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)

                self.check_box_select_all = QCheckBox(tab_widget_objects)
                self.check_box_select_all.setObjectName(u"check_box_select_all")
                self.check_box_select_all.setGeometry(QRect(20, 10, 16, 20))
                self.check_box_select_all.setChecked(False)
                self.label_album_header = QLabel(tab_widget_objects)
                self.label_album_header.setObjectName(u"label_album_header")
                self.label_album_header.setGeometry(QRect(50, 10, 49, 16))

                self.check_box_select_all.setText("")
                self.label_album_header.setText(u"Album")
                
                self.tab_widget.addTab(tab_widget_objects, "")

#def create_tab_content(self):
#        for x in range():
#                test_dict = {}
#                self.check_box_album_x = QCheckBox(self.scrollAreaWidgetContents)
#                self.check_box_album_x.setObjectName(u"check_box_album_1")
#                self.check_box_album_x.setGeometry(QRect(20, 20, 16, 20))
#                self.label_album_x = QLabel(self.tab_widget_tab_downloaded)
#                self.label_album_x.setObjectName(u"label_album_1")
#                self.label_album_x.setGeometry(QRect(51, 51, 171, 16))
# create dictionary to store albums etc

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())