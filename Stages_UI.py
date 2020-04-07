from PyQt5.QtWidgets import QGridLayout, QTabWidget ,QListWidget, QLineEdit, QPlainTextEdit, QListWidgetItem, QMessageBox, QVBoxLayout
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QComboBox, QCheckBox, QSpinBox, QApplication, QLabel
from PyQt5.QtWidgets import  QWidget, QSizePolicy, QAction, QMainWindow, QPushButton, QGroupBox, QHBoxLayout, QRadioButton
import sys
import Component_manager
from Stage_constructor import Stage
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QIcon, QPalette, QMovie, QFont, QPixmap, QImage, QBrush
from PyQt5.QtCore import Qt, QByteArray, QSize, QFileInfo, QUrl
from Transistor_manager import TransistorManager
import Styles
from scipy import signal
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transistor Wizard")
        self.mainIcon = "Icons/Amplifier.png"
        self.clip = "Icons/MainBackground.gif"
        self.conftran = Conftran()
        self.confdata = ConfData()
        self.confsheet = ConfSheet()
        self.help_window = help()
        self.transistor_edit = transistor_editor()
        self.sounds = Sounds()
        self.parameters_conf = 0
        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QIcon(self.mainIcon))
        self.sounds.start()
        self.widget()
        self.CreateMenu()

    def CreateMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet(Styles.MenuBar)
        fileMenu = mainMenu.addMenu("Archivo")
        EditMenu = mainMenu.addMenu("Configuracion")
        HelpMenu = mainMenu.addMenu("Ayuda")

        ResetConfigAction = QAction(QIcon(self.mainIcon), "Nueva configuracion", self)
        ResetConfigAction.setShortcut("ctrl+r")
        fileMenu.addAction(ResetConfigAction)
        ResetConfigAction.setIcon(QIcon("Icons/new_file.png"))
        ResetConfigAction.triggered.connect(self.reset_conf)

        HelpAction = QAction(QIcon(self.mainIcon), "Acerca de", self)
        HelpAction.setIcon(QIcon("Icons/help.png"))
        HelpAction.setShortcut("ctrl+f")
        HelpMenu.addAction(HelpAction)
        HelpAction.triggered.connect(self.help)

        Transistores = QAction(QIcon(self.mainIcon), "Transistores db", self)
        Transistores.setIcon(QIcon("Icons/transistor.png"))
        EditMenu.addAction(Transistores)
        Transistores.setShortcut("ctrl+t")
        Transistores.triggered.connect(self.Transistor)

    def widget(self):
        self.grid = QGridLayout()
        self.gif(self.clip)
        self.create_button()
        self.open_tabs()
        self.Int_UI = QWidget()
        self.Int_UI.setStyleSheet(Styles.central_widget)
        self.Int_UI.setLayout(self.grid)
        self.setCentralWidget(self.Int_UI)

    def Transistor(self):
        self.sounds.button()
        self.transistor_edit.showMaximized()

    def help(self):
        self.help_window.show()

    def open_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.tabBar().setStyleSheet(Styles.tab);
        self.tabs.addTab(self.confdata, "Configuracion de transistor")
        self.tabs.addTab(self.confsheet, "Datos comerciales")

    def gif(self, clip):
        ##Configuracion del gif#########
        self.movie = QMovie(clip, QByteArray(), self)
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()
        self.grid.addWidget(self.movie_screen, 0, 0)

    def btn_start_config(self):
        self.conftran.show()
        self.sounds.button()
        self.close()

    def create_button(self):
        self.btn_start = QPushButton("Iniciar configuración")
        self.btn_start.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.btn_start.setIcon(QIcon("Icons/Transistor.png"))
        self.btn_start.clicked.connect(self.btn_start_config)
        self.btn_start.setIconSize(QSize(150, 150))
        self.btn_start.setStyleSheet(Styles.button)
        self.grid.addWidget(self.btn_start, 1, 0)

    def reset_conf(self):
        if mainwindow.conftran.parameters.reset_enable == True:
            self.close()
            self.movie_screen.close()
            self.tabs.close()
            self.open_tabs()
            self.grid.removeWidget(self.movie_screen)
            self.grid.removeWidget(self.tabs)
            self.clip = "Icons/MainBackground.gif"
            self.gif(self.clip)
            self.create_button()
            self.conftran.transistor_data.clear()
            ##clean parameters

            self.conftran.parameters.AV_textedit.clear()
            self.conftran.parameters.AI_textedit.clear()
            self.conftran.parameters.RL_textedit.clear()
            self.conftran.parameters.RS_textedit.clear()
            if self.conftran.config_selected == "EC":
                 self.conftran.parameters.VCC_textedit.clear()
            self.conftran.parameters.F1_textedit.clear()
            self.conftran.parameters.F2_textedit.clear()
            self.conftran.transistor_data.close()
            self.conftran.parameters.hbox_main.removeWidget(self.conftran.transistor_data)
            self.conftran.stage.T.transistor_avaliable = False
            mainwindow.conftran.parameters.reset_enable = False

            self.showMaximized()
        else:
            self.sounds.error1()

class Sounds():
    def __init__(self):
        self.player = QMediaPlayer()
        self.sounds = {'Start': "Sounds/Start_Windows.wav",'button': "Sounds/Select.wav", "error1": "Sounds/Critical_Battery.wav",
                       "error2": "Sounds/Low_Battery.wav", "music": "Sounds/song.wav", "button2": "Sounds/Menu_Popup.wav"}

    def start(self):
        self.player.setMedia(QMediaContent(QUrl(self.sounds['Start'])))
        self.player.play()

    def button(self):
        self.player.setMedia(QMediaContent(QUrl(self.sounds['button'])))
        self.player.play()

    def button2(self):
        self.player.setMedia(QMediaContent(QUrl(self.sounds['button2'])))
        self.player.play()

    def error1(self):
        self.player.setMedia(QMediaContent(QUrl(self.sounds['error1'])))
        self.player.play()

    def error2(self):
        self.player.setMedia(QMediaContent(QUrl(self.sounds['error2'])))
        self.player.play()

class Addtransistor(QWidget):
    def __init__(self):
        super().__init__()
        self.initwindow()
        self.conf = ''
        self.darlington_status = '1'
        self.type_status = 'npn'
        self.setWindowIcon(QIcon("Icons/Transistor.png"))
        self.setStyleSheet(Styles.central_widget)

    def initwindow(self):
        self.vbox = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.group = QGroupBox("Datos transistor")
        self.group.setStyleSheet(Styles.group_box)
        self.vbox_main = QVBoxLayout()

        self.Model_label = QLabel("Modelo :")
        self.Model_text = QLineEdit()
        self.vbox.addWidget(self.Model_label)
        self.vbox.addWidget(self.Model_text)

        self.VCEMAX_label = QLabel("Vce_MAX :")
        self.VCEMAX_text = QSpinBox()
        self.VCEMAX_text.setMaximum(100000)
        self.vbox.addWidget(self.VCEMAX_label)
        self.vbox.addWidget(self.VCEMAX_text)

        self.hfe_min_label = QLabel("hfe_min :")
        self.hfe_min_text = QSpinBox()
        self.hfe_min_text.setMaximum(100000)
        self.vbox.addWidget(self.hfe_min_label)
        self.vbox.addWidget(self.hfe_min_text)

        self.hfe_max_label = QLabel("hfe_max :")
        self.hfe_max_text = QSpinBox()
        self.hfe_max_text.setMaximum(100000)
        self.vbox.addWidget(self.hfe_max_label)
        self.vbox.addWidget(self.hfe_max_text)

        self.Hfe_min_label = QLabel("Hfe_min :")
        self.Hfe_min_text = QSpinBox()
        self.Hfe_min_text.setMaximum(100000)
        self.vbox2.addWidget(self.Hfe_min_label)
        self.vbox2.addWidget(self.Hfe_min_text)

        self.Hfe_max_label = QLabel("Hfe_max :")
        self.Hfe_max_text = QSpinBox()
        self.Hfe_max_text.setMaximum(100000)
        self.vbox2.addWidget(self.Hfe_max_label)
        self.vbox2.addWidget(self.Hfe_max_text)

        self.IC_max_label = QLabel("IC_max :")
        self.IC_max_text = QLineEdit()
        self.vbox2.addWidget(self.IC_max_label)
        self.vbox2.addWidget(self.IC_max_text)

        self.IC_Stable_label = QLabel("IC Stable :")
        self.IC_Stable_text = QLineEdit()
        self.vbox2.addWidget(self.IC_Stable_label)
        self.vbox2.addWidget(self.IC_Stable_text)

        self.PD_label = QLabel("Potencia maxima :")
        self.PD_text = QLineEdit()
        self.vbox2.addWidget(self.PD_label)
        self.vbox2.addWidget(self.PD_text)

        self.darlington = QCheckBox()
        self.darlington.setStyleSheet(Styles.checkbox)
        self.darlington.setText("Darlington")
        self.darlington.toggled.connect(self.darlington_check)
        self.vbox.addWidget(self.darlington)
        self.darlington.setStyleSheet(Styles.checkbox)

        self.type = QComboBox()
        types = ['npn', 'pnp']
        self.type.addItems(types)
        self.type.currentTextChanged.connect(self.type_change)
        self.type_status = self.type.currentText()
        self.type.setStyleSheet(Styles.combobox)
        self.vbox2.addWidget(self.type)

        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.vbox2)

        self.group.setLayout(self.hbox)

        accept = QPushButton("Aceptar")
        accept.setFont(QFont("Times", 12))
        accept.setStyleSheet(Styles.button)
        accept.clicked.connect(self.accept)

        self.vbox_main.addWidget(self.group)
        self.vbox_main.addWidget(accept)
        self.setLayout(self.vbox_main)

    def type_change(self):
        mainwindow.sounds.button()
        self.type_status = self.type.currentText()

    def darlington_check(self):
        mainwindow.sounds.button()
        if self.darlington.isChecked():
            self.darlington_status = '1'
        else:
            self.darlington_status = '0'
        print(self.darlington_status)

    def accept(self):
        if self.PD_text.text() != '' and mainwindow.conftran.parameters.test_syntax(self.PD_text.text()):
            if self.IC_Stable_text.text() != '' and mainwindow.conftran.parameters.test_syntax(self.IC_Stable_text.text()):
                if self.IC_max_text.text() != '' and mainwindow.conftran.parameters.test_syntax(self.IC_max_text.text()):
                    mainwindow.sounds.button()
                    self.conf += "\n"
                    self.conf += self.Model_text.text()
                    self.conf += ','
                    self.conf += self.type_status
                    self.conf += ','
                    self.conf += self.VCEMAX_text.text()
                    self.conf += ','
                    self.conf += self.Hfe_min_text.text()
                    self.conf += ','
                    self.conf += self.Hfe_max_text.text()
                    self.conf += ','
                    self.conf += self.hfe_min_text.text()
                    self.conf += ','
                    self.conf += self.hfe_max_text.text()
                    self.conf += ','
                    self.conf += self.IC_max_text.text()
                    self.conf += ','
                    self.conf += self.PD_text.text()
                    self.conf += ','
                    self.conf += self.darlington_status
                    self.conf += ','
                    self.conf += self.IC_Stable_text.text()
                    with open('Transistors_db.txt', 'a') as doc:
                        doc.write(self.conf)
                    mainwindow.transistor_edit.transistor_db.get_db(True)
                    mainwindow.conftran.update_transistors()
                    self.conf = ''
                    self.close()
                else:
                     QMessageBox.about(self, "Error IC_max", "Valor IC_max invalido o no ingresado")
                     mainwindow.sounds.error2()
            else:
                QMessageBox.about(self, "Error IC_Stable", "Valor IC_Stable invalido o no ingresado")
                mainwindow.sounds.error2()
        else:
            QMessageBox.about(self, "Error PD_max", "Valor PD_max invalido o no ingresado")
            mainwindow.sounds.error2()

class transistor_editor(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.setWindowIcon(QIcon("Icons/Transistor.png"))
        self.setWindowTitle("Configuracion de transistores")
        self.addtransistor = Addtransistor()
        self.setStyleSheet(Styles.central_widget)
        self.transistor_db = TransistorDb()
        self.transistor_db.get_db(True)

        vbox.addWidget(self.transistor_db)

        add_transistor = QPushButton("Añadir transistor")
        add_transistor.setFont(QFont("Times", 15))
        add_transistor.clicked.connect(self.Add_transistor_action)
        add_transistor.setStyleSheet(Styles.button)
        hbox.addWidget(add_transistor)

        reset_db = QPushButton("Reset")
        reset_db.setFont(QFont("Times", 15))
        reset_db.clicked.connect(self.reset_transistor_action)
        reset_db.setStyleSheet(Styles.button)
        hbox.addWidget(reset_db)

        Aceptar = QPushButton("Aceptar")
        Aceptar.setFont(QFont("Times", 15))
        Aceptar.clicked.connect(self.Exit)
        Aceptar.setStyleSheet(Styles.button)
        hbox.addWidget(Aceptar)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def Exit(self):
        mainwindow.sounds.button()
        self.close()

    def Add_transistor_action(self):
        mainwindow.sounds.button()
        self.addtransistor.show()

    def reset_transistor_action(self):
        mainwindow.sounds.button()
        with open('Transistors_db-backup.txt', 'r') as doc:
            with open('Transistors_db.txt', 'w') as doc2:
                data = doc.readlines()
                for index in range(len(data)):
                    doc2.write(data[index])
        self.transistor_db.get_db(True)

class TransistorDb(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.transistors = QTableWidget()

    def get_db(self, update):
        if update:
            self.transistors.close()
            self.vbox.removeWidget(self.transistors)
            self.transistors = QTableWidget()
        column = 0
        with open('Transistors_db.txt', 'r') as self.transistors_db:
            transistors_content = self.transistors_db.readlines()
            row = len(transistors_content)
            tmp = ''
            index3 = 0
            for index in range(len(transistors_content[0])):
                if transistors_content[0][index] == ',':
                    column+=1
            column+=1
            self.transistors.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.transistors.setRowCount(row)
            self.transistors.setColumnCount(column)
            ##hacer celdas de los transistores
            for index in range(row):
                for index2 in range(len(transistors_content[index])):
                    if transistors_content[index][index2] == ',':
                        self.transistors.setItem(index, index3, QTableWidgetItem(tmp))
                        tmp = ''
                        if index3 < column:
                            index3 +=1
                    elif transistors_content[index][index2] == '\n':
                        self.transistors.setItem(index, index3, QTableWidgetItem(tmp))
                        tmp = ''
                        index3 = 0
                    else:
                        tmp += transistors_content[index][index2]
            self.transistors.setItem(index, index3, QTableWidgetItem(tmp))
        ############################################################################
        self.vbox.addWidget(self.transistors)
        self.setLayout(self.vbox)

class ConfSheet(QWidget):
    def __init__(self):
        super().__init__()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.conf_sheet = QPlainTextEdit(self)
        self.conf_sheet.setReadOnly(True)
        vbox1.addWidget(self.conf_sheet)

        self.pdf_button = QPushButton("Guardar como pdf")
        self.pdf_button.setFont(QFont("Times", 12))
        self.pdf_button.setMinimumHeight(60)
        self.pdf_button.setIcon(QIcon("Icons/pdf.png"))
        self.pdf_button.clicked.connect(self.pdfExport)
        self.pdf_button.setStyleSheet(Styles.button)

        self.print_button = QPushButton("Imprimir")
        self.print_button.setIcon(QIcon("Icons/printer.png"))
        self.print_button.setMinimumHeight(60)
        self.print_button.setFont(QFont("Times", 12))
        self.print_button.clicked.connect(self.printDialog)
        self.print_button.setStyleSheet(Styles.button)

        self.bode1_button = QPushButton("Visualizar bode corte inferior")
        self.bode1_button.setIcon(QIcon("Icons/graph.png"))
        self.bode1_button.setMinimumHeight(60)
        self.bode1_button.setFont(QFont("Times", 12))
        self.bode1_button.clicked.connect(self.bode1)
        self.bode1_button.setStyleSheet(Styles.button)

        self.bode2_button = QPushButton("Visualizar bode corte superior")
        self.bode2_button.setIcon(QIcon("Icons/graph.png"))
        self.bode2_button.setMinimumHeight(60)
        self.bode2_button.setFont(QFont("Times", 12))
        self.bode2_button.clicked.connect(self.bode2)
        self.bode2_button.setStyleSheet(Styles.button)

        hbox1.addWidget(self.pdf_button)
        hbox1.addWidget(self.print_button)

        hbox2.addWidget(self.bode1_button)
        hbox2.addWidget(self.bode2_button)

        vbox2.addLayout(hbox1)
        vbox2.addLayout(hbox2)

        vbox1.addLayout(vbox2)
        self.setLayout(vbox1)

    def bode1(self):
        mainwindow.conftran.parameters.bode.FI_show()

    def bode2(self):
        mainwindow.conftran.parameters.bode.FS_show()

    def pdfExport(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf)//All Files")
        mainwindow.sounds.button()
        if fn != '':
            if QFileInfo(fn).suffix() == "":fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.conf_sheet.print_(printer)

    def printDialog(self):
        mainwindow.sounds.button()
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QPrintDialog.Accepted:
            self.conf_sheet.print_(printer)

class Conftran(QWidget):
    def __init__(self):
        super().__init__()
        self.height = 400
        self.width = 300
        self.top = 500
        self.left = 500
        self.setWindowTitle("Transistor Wizard")
        self.mainIcon = "Icons/transistor.jpg"
        self.config_selected = "EC"
        self.parameters = Parameters(self.config_selected)
        self.setStyleSheet(Styles.central_widget)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QIcon("Icons/Amplifier.png"))
        self.setWindowTitle("Eleccion de transistor y configuracion")
        self.setGeometry(self.top, self.width, self.height, self.width)
        self.radioButton()
        self.transistor_list()
        self.btn_accept = QPushButton("Aceptar")
        self.btn_accept.setFont(QFont("Times", 12))
        self.btn_accept.clicked.connect(self.btn_accept_action)
        self.btn_accept.setStyleSheet(Styles.button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        vbox.addWidget(self.Transistor_List)
        vbox.addWidget(self.btn_accept)
        self.setLayout(vbox)

    def transistor_list(self):
        self.Transistor_List = QListWidget()
        self.update_transistors()

    def update_transistors(self):
        self.transistor_models_avaliables = TransistorManager('show')
        self.transistor_models_avaliables = self.transistor_models_avaliables.show_transitors_avaliables()
        #self.Transistor_List.clear()
        for index in range(len(self.transistor_models_avaliables)):
            l = QListWidgetItem(QIcon("Icons/Transistor.png"), self.transistor_models_avaliables[index])
            self.Transistor_List.insertItem(index, l)

    def radioButton(self):
        self.groupBox = QGroupBox("Elija Su configuracion")
        self.groupBox.setFont(QFont("Times", 12))
        self.groupBox.setStyleSheet(Styles.group_box)
        hboxlayout = QHBoxLayout()
        self.EC_radio_button = QRadioButton()
        self.EC_radio_button.setChecked(True)
        self.EC_radio_button.setIcon(QIcon("Icons/EC.png"))
        self.EC_radio_button.setIconSize(QSize(150, 150))
        self.EC_radio_button.toggled.connect(self.EC_button)
        hboxlayout.addWidget(self.EC_radio_button)

        self.CC_radio_button = QRadioButton()
        self.CC_radio_button.setIcon(QIcon("Icons/CC.png"))
        self.CC_radio_button.setIconSize(QSize(150, 150))
        self.CC_radio_button.toggled.connect(self.CC_button)
        hboxlayout.addWidget(self.CC_radio_button)

        self.groupBox.setLayout(hboxlayout)

    def EC_button(self):
        mainwindow.sounds.button2()
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.config_selected = "EC"
            self.parameters = Parameters(self.config_selected)

    def CC_button(self):
        mainwindow.sounds.button2()
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.config_selected = "CC"
            self.parameters = Parameters(self.config_selected)

    def btn_accept_action(self):
        mainwindow.sounds.button()
        row = self.Transistor_List.currentRow()
        if row != -1:
            item = self.Transistor_List.item(row)
            self.transistor_name = item.text()
            self.parameters.show()
            self.stage = Stage(self.transistor_name)
            self.transistor_data = QPlainTextEdit()
            self.transistor_data.setStyleSheet(Styles.plaintext)
            self.transistor_data.setReadOnly(True)
            for index in self.stage.Values_model_transistor:
                self.transistor_data.appendPlainText(f'{index} = '
                                                f'{self.stage.Values_model_transistor[index]}\n')
            self.parameters.hbox_main.addWidget(self.transistor_data)
            self.close()
        else:
            QMessageBox.about(self, "Error", "Por favor seleccione un transistor")

class ConfData(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 200
        self.width = 300
        self.height = 250
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        self.setWindowTitle("Transistor Wizard")
        self.mainIcon = "transistor.jpg"
        self.re_label = None
        self.re2_label = None
        self.re1_label = None
        self.c3_label = None
        self.rc_label = None
        self.hbox = QHBoxLayout()
        self.labels_icons()
        self.setLayout(self.hbox)

    def labels_icons(self):
        self.grid = QGridLayout()

        self.c1_label = QLabel("C1")
        self.c1_label.setFont(QFont("Times", 14))
        c1_image = QLabel(self)
        c1_pixmap = QPixmap("Icons/C1.png")
        c1_image.setPixmap(c1_pixmap)
        self.grid.addWidget(self.c1_label,0,0)
        self.grid.addWidget(c1_image,0,1)

        self.c2_label = QLabel("C2")
        self.c2_label.setFont(QFont("Times", 14))
        c2_image = QLabel(self)
        c2_pixmap = QPixmap("Icons/C2.png")
        c2_image.setPixmap(c2_pixmap)
        self.grid.addWidget(self.c2_label, 1, 0)
        self.grid.addWidget(c2_image, 1, 1)

        self.r1_label = QLabel("R1")
        self.r1_label.setFont(QFont("Times", 14))
        r1_image = QLabel(self)
        r1_pixmap = QPixmap("Icons/R1.png")
        r1_image.setPixmap(r1_pixmap)
        self.grid.addWidget(self.r1_label, 3, 0)
        self.grid.addWidget(r1_image, 3, 1)

        self.r2_label = QLabel("R2")
        self.r2_label.setFont(QFont("Times", 14))
        r2_image = QLabel(self)
        r2_pixmap = QPixmap("Icons/R2.png")
        r2_image.setPixmap(r2_pixmap)
        self.grid.addWidget(self.r2_label, 4, 0)
        self.grid.addWidget(r2_image, 4, 1)

        self.rl_label = QLabel("RL")
        self.rl_label.setFont(QFont("Times", 14))
        rl_image = QLabel(self)
        rl_pixmap = QPixmap("Icons/RL.png")
        rl_image.setPixmap(rl_pixmap)
        self.grid.addWidget(self.rl_label, 3, 2)
        self.grid.addWidget(rl_image, 3, 3)

        self.vcc_label = QLabel("VCC")
        self.vcc_label.setFont(QFont("Times", 14))
        vcc_image = QLabel(self)
        vcc_pixmap = QPixmap("Icons/VCC.png")
        vcc_image.setPixmap(vcc_pixmap)
        self.grid.addWidget(self.vcc_label, 4, 2)
        self.grid.addWidget(vcc_image, 4, 3)

    def EC_CC_choice(self):
        if mainwindow.conftran.config_selected == "EC":
            self.EC_mode()
        elif mainwindow.conftran.config_selected == "CC":
            self.CC_mode()

    def EC_mode(self):
        if self.re_label != None:
            self.re_image.close()
            self.grid.removeWidget(self.re_image)
            self.re_label.close()
            self.grid.removeWidget(self.re_label)

        if self.re2_label != None:
            self.re2_label.close()
            self.grid.removeWidget(self.re2_label)
            self.re2_image.close()
            self.grid.removeWidget(self.re2_image)
            self.re1_label.close()
            self.grid.removeWidget(self.re1_label)
            self.re1_image.close()
            self.grid.removeWidget(self.re1_image)
            self.c3_label.close()
            self.grid.removeWidget(self.c3_label)
            self.c3_image.close()
            self.grid.removeWidget(self.c3_image)
            self.rc_label.close()
            self.grid.removeWidget(self.rc_label)
            self.rc_image.close()
            self.grid.removeWidget(self.rc_image)

        self.c3_label = QLabel("C3")
        self.c3_label.setFont(QFont("Times", 14))
        self.c3_image = QLabel(self)
        c3_pixmap = QPixmap("Icons/C3.png")
        self.c3_image.setPixmap(c3_pixmap)
        self.grid.addWidget(self.c3_label, 2, 0)
        self.grid.addWidget(self.c3_image, 2, 1)

        self.rc_label = QLabel("RC")
        self.rc_label.setFont(QFont("Times", 14))
        self.rc_image = QLabel(self)
        rc_pixmap = QPixmap("Icons/RC.png")
        self.rc_image.setPixmap(rc_pixmap)
        self.grid.addWidget(self.rc_label, 2, 2)
        self.grid.addWidget(self.rc_image, 2, 3)


        self.re1_label = QLabel("RE1")
        self.re1_label.setFont(QFont("Times", 14))
        self.re1_image = QLabel(self)
        re1_pixmap = QPixmap("Icons/RE1.png")
        self.re1_image.setPixmap(re1_pixmap)
        self.grid.addWidget(self.re1_label, 0, 2)
        self.grid.addWidget(self.re1_image, 0, 3)

        self.re2_label = QLabel("RE2")
        self.re2_label.setFont(QFont("Times", 14))
        self.re2_image = QLabel(self)
        re2_pixmap = QPixmap("Icons/RE2.png")
        self.re2_image.setPixmap(re2_pixmap)
        self.grid.addWidget(self.re2_label, 1, 2)
        self.grid.addWidget(self.re2_image, 1, 3)
        self.hbox.addLayout(self.grid)


    def CC_mode(self):
        if self.re2_label != None:
            self.re2_label.close()
            self.grid.removeWidget(self.re2_label)
            self.re2_image.close()
            self.grid.removeWidget(self.re2_image)
            self.re1_label.close()
            self.grid.removeWidget(self.re1_label)
            self.re1_image.close()
            self.grid.removeWidget(self.re1_image)
            self.c3_label.close()
            self.grid.removeWidget(self.c3_label)
            self.c3_image.close()
            self.grid.removeWidget(self.c3_image)
            self.rc_label.close()
            self.grid.removeWidget(self.rc_label)
            self.rc_image.close()
            self.grid.removeWidget(self.rc_image)
        if self.re_label != None:
            self.re_image.close()
            self.grid.removeWidget(self.re_image)
            self.re_label.close()
            self.grid.removeWidget(self.re_label)
        self.re_label = QLabel("RE")
        self.re_label.setFont(QFont("Times", 14))
        self.re_image = QLabel(self)
        re_pixmap = QPixmap("Icons/RE.png")
        self.re_image.setPixmap(re_pixmap)
        self.grid.addWidget(self.re_label, 2, 0)
        self.grid.addWidget(self.re_image, 2, 1)
        self.hbox.addLayout(self.grid)



class help(QWidget):
    def __init__(self):
        super().__init__()
        self.help_music = Sounds()
        self.help_music.player.setMedia(QMediaContent(QUrl("Sounds/song.wav")))
        self.setStyleSheet(Styles.central_widget)
        vbox = QVBoxLayout()
        self.setWindowTitle("Ayuda")
        self.setWindowIcon(QIcon("Icons/help.png"))
        image = QLabel(self)
        pixmap = QPixmap("Icons/Quedate.jpg")
        image.setPixmap(pixmap)
        vbox.addWidget(image)

        self.button_play_stop = QPushButton("play")
        self.button_play_stop.clicked.connect(self.button_play)
        self.button_play_stop.setStyleSheet(Styles.button)
        vbox.addWidget(self.button_play_stop)

        self.setLayout(vbox)

    def button_play(self):
        print( self.help_music.player.state() == QMediaPlayer.PlayingState)
        if self.help_music.player.state() == QMediaPlayer.PlayingState:
            self.help_music.player.pause()
            self.button_play_stop.setText("play")
        else:
            self.button_play_stop.setText("pause")
            self.help_music.player.play()

class Bode:
    def __init__(self, tao_C2, tao_C4):
        #
        self.s1 = signal.lti([tao_C2,0],[tao_C2,1])
        self.s2 = signal.lti([1], [tao_C4, 1])

    def FS_show(self):
        w2, mag2, phase2 = signal.bode(self.s2)
        plt.figure()
        plt.semilogx(w2, mag2)
        plt.title("Diagrama de bode de corte superior")
        plt.xlabel("Rads")
        plt.ylabel("AV")
        plt.show()

    def FI_show(self):
        w1, mag1, phase1 = signal.bode(self.s1)
        plt.figure()
        plt.semilogx(w1, mag1)
        plt.title("Diagrama de bode de corte inferior")
        plt.xlabel("Rads")
        plt.ylabel("AV")
        plt.show()


class Parameters(QWidget):
    def __init__(self, config):
        super().__init__()
        self.top = 250
        self.left = 500
        self.height = 200
        self.width = 300
        self.config = config
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.reset_enable = False
        self.setPalette(p)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("Icons/Transistor.png"))
        self.setWindowTitle("Seleccion de parametros")
        self.stage = 0
        self.bode = 0
        self.parameters = {}
        self.setStyleSheet(Styles.central_widget)
        self.InitWindow()

    def InitWindow(self):
        RS_Panel = QGroupBox("Introduzca RS")
        RS_Panel.setStyleSheet(Styles.group_box)
        RL_Panel = QGroupBox("Introduzca RL")
        RL_Panel.setStyleSheet(Styles.group_box)
        self.AV_Panel = QGroupBox("Introduzca AV")
        self.AV_Panel.setStyleSheet(Styles.group_box)
        self.AI_Panel = QGroupBox("Introduzca AI")
        self.AI_Panel.setStyleSheet(Styles.group_box)
        F_Panel = QGroupBox("Introduzca F")
        F_Panel.setStyleSheet(Styles.group_box)
        VCC_Panel = QGroupBox("Introduzca VCC")
        VCC_Panel.setStyleSheet(Styles.group_box)


        hbox_RS = QHBoxLayout()
        hbox_RL = QHBoxLayout()
        hbox_VCC = QHBoxLayout()
        vbox_F = QVBoxLayout()
        hbox_F1 = QHBoxLayout()
        hbox_F2 = QHBoxLayout()
        hbox_AV = QHBoxLayout()
        hbox_AI = QHBoxLayout()

        self.hbox_main = QHBoxLayout()

        self.MainParametersInput = QVBoxLayout()

        self.RS_label = QLabel("RS")
        self.RS_textedit = QLineEdit()
        hbox_RS.addWidget(self.RS_label)
        hbox_RS.addWidget(self.RS_textedit)
        RS_Panel.setLayout(hbox_RS)

        self.AV_label = QLabel("AV")
        self.AV_textedit = QLineEdit()
        hbox_AV.addWidget(self.AV_label)
        hbox_AV.addWidget(self.AV_textedit)
        self.AV_Panel.setLayout(hbox_AV)

        self.AI_label = QLabel("AI")
        self.AI_textedit = QLineEdit()
        hbox_AI.addWidget(self.AI_label)
        hbox_AI.addWidget(self.AI_textedit)
        self.AI_Panel.setLayout(hbox_AI)

        self.RL_label = QLabel("RL")
        self.RL_textedit = QLineEdit()
        hbox_RL.addWidget(self.RL_label)
        hbox_RL.addWidget(self.RL_textedit)
        RL_Panel.setLayout(hbox_RL)

        self.VCC = QLabel("VCC")
        self.VCC_textedit = QLineEdit()
        hbox_VCC.addWidget(self.VCC)
        hbox_VCC.addWidget(self.VCC_textedit)
        VCC_Panel.setLayout(hbox_VCC)

        self.F1_label = QLabel("F1")
        self.F1_textedit = QLineEdit()
        hbox_F1.addWidget(self.F1_label)
        hbox_F1.addWidget(self.F1_textedit)
        vbox_F.addLayout(hbox_F1)

        self.F2_label = QLabel("F2")
        self.F2_textedit = QLineEdit()
        hbox_F2.addWidget(self.F2_label)
        hbox_F2.addWidget(self.F2_textedit)
        vbox_F.addLayout(hbox_F2)

        F_Panel.setLayout(vbox_F)

        self.btn_Introducir_Datos = QPushButton("Aceptar")
        self.btn_Introducir_Datos.setStyleSheet(Styles.button)
        self.btn_Introducir_Datos.clicked.connect(self.btn_accept)

        self.MainParametersInput.addWidget(RS_Panel)
        self.MainParametersInput.addWidget(F_Panel)
        self.MainParametersInput.addWidget(RL_Panel)
        if self.config == "EC":
            self.MainParametersInput.addWidget(VCC_Panel)
            self.MainParametersInput.addWidget(self.AV_Panel)
        else:
            self.MainParametersInput.addWidget(self.AI_Panel)
        self.MainParametersInput.addWidget(self.btn_Introducir_Datos)
        self.hbox_main.addLayout(self.MainParametersInput)
        self.setLayout(self.hbox_main)

    def btn_accept(self):
        if self.RS_textedit.text() != '' and self.test_syntax(self.RS_textedit.text()):
            if self.F1_textedit.text() != '' and (self.test_syntax(self.F1_textedit.text()) and self.to_float(self.F1_textedit.text()) < 1000000000):
                if self.F2_textedit.text() != '' and (self.test_syntax(self.F2_textedit.text())
                                                      and self.to_float(self.F2_textedit.text()) < 1000000000 and  self.to_float(self.F2_textedit.text()) > self.to_float(self.F1_textedit.text())):
                    self.parameters['RS'] = self.to_float(self.RS_textedit.text())
                    self.parameters['F1'] = self.to_float(self.F1_textedit.text())
                    self.parameters['F2'] = self.to_float(self.F2_textedit.text())
                    mainwindow.movie_screen.close()
                    mainwindow.grid.removeWidget(mainwindow.movie_screen)
                    mainwindow.btn_start.close()
                    mainwindow.grid.removeWidget(mainwindow.btn_start)
                    if self.config == 'EC':
                        if self.RL_textedit.text() != '' and (self.test_syntax(self.RL_textedit.text()) and self.to_float(self.RL_textedit.text()) < 100000):
                            if self.VCC_textedit.text() != '' and (self.test_syntax(self.VCC_textedit.text()) and self.to_float(self.VCC_textedit.text()) < 200):
                                if self.AV_textedit.text() != '' and (self.test_syntax(self.AV_textedit.text()) and self.to_float(self.AV_textedit.text()) < 400):
                                    mainwindow.sounds.button()
                                    self.parameters['RL'] = self.to_float(self.RL_textedit.text())
                                    self.parameters['VCC'] = self.to_float(self.VCC_textedit.text())
                                    self.parameters['AV'] = self.to_float(self.AV_textedit.text())
                                    mainwindow.conftran.stage.build_stage_EC(self.parameters['RS'], self.parameters['RL'], self.parameters['AV'],
                                                                             self.parameters['F1'], self.parameters['F2'], self.parameters['VCC'])
                                    parameters = mainwindow.conftran.stage.get_parameters()
                                    ##gif
                                    if mainwindow.conftran.stage.Values_model_transistor['Darlington'] == 1:
                                        mainwindow.clip = "Icons/EC_pnp_Darlington.gif"
                                    else:
                                        if mainwindow.conftran.stage.Values_model_transistor['Type'] == "npn":
                                            mainwindow.clip = "Icons/EC_npn_background.gif"
                                        else:
                                           mainwindow.clip = "Icons/EC_pnp_background.gif"
                                    mainwindow.gif(mainwindow.clip)
                                    ##set parameters
                                    mainwindow.confdata.EC_CC_choice()
                                    mainwindow.confdata.c1_label.setText(str(parameters['C1']))
                                    mainwindow.confdata.c2_label.setText(str(parameters['C2']))
                                    mainwindow.confdata.c3_label.setText(str(parameters['C3']))
                                    mainwindow.confdata.r1_label.setText(str(parameters['R1']))
                                    mainwindow.confdata.r2_label.setText(str(parameters['R2']))
                                    mainwindow.confdata.re1_label.setText(str(parameters['Re1']))
                                    mainwindow.confdata.re2_label.setText(str(parameters['Re2']))
                                    mainwindow.confdata.rc_label.setText(self.RL_textedit.text())
                                    mainwindow.confdata.vcc_label.setText(str(parameters['VCC']))
                                    mainwindow.confdata.rl_label.setText(self.RL_textedit.text())

                                    self.bode = Bode(parameters['C1']*parameters['RB'],parameters['C4']*parameters['RL']*0.5)

                                    ##tabs
                                    Component_manager.To_comercial_parameters(parameters)
                                    mainwindow.grid.addWidget(mainwindow.tabs, 0, 1)
                                    mainwindow.confsheet.conf_sheet.clear()
                                    mainwindow.confsheet.conf_sheet.appendPlainText(f'Transistor = {mainwindow.conftran.transistor_name}')
                                    mainwindow.confsheet.conf_sheet.appendPlainText("Tipo " +  str(mainwindow.conftran.stage.Values_model_transistor['Type']))
                                    for index in parameters:
                                        mainwindow.confsheet.conf_sheet.appendPlainText(f'{index} = {parameters[index]}')
                                    mainwindow.confsheet.conf_sheet.setFont(QFont("Times", 15))
                                    mainwindow.showMaximized()
                                    self.reset_enable = True
                                    self.close()
                                else:
                                    QMessageBox.about(self, "Error AV", "Valor AV invalido o no ingresado")
                                    mainwindow.sounds.error1()
                            else:
                                QMessageBox.about(self, "Error VCC", "Valor VCC invalido o no ingresado")
                                mainwindow.sounds.error1()
                        else:
                            QMessageBox.about(self, "Error RL", "Valor RL invalido o no ingresado")
                            mainwindow.sounds.error1()
                    elif self.config == 'CC':
                        if self.RL_textedit.text() != '' and self.test_syntax(self.RL_textedit.text()) and self.to_float(self.RL_textedit.text()) < 200:
                            if self.AI_textedit.text() != '' and self.test_syntax(self.AI_textedit.text()):
                                mainwindow.sounds.button()
                                self.parameters['RL'] = self.to_float(self.RL_textedit.text())
                                self.parameters['AI'] = self.to_float(self.AI_textedit.text())
                                mainwindow.conftran.stage.build_stage_CC(self.parameters['RS'], self.parameters['RL'],
                                                          self.parameters['F1'],self.parameters['F2'], self.parameters['AI'])
                                parameters = mainwindow.conftran.stage.get_parameters()
                                ##gif
                                if mainwindow.conftran.stage.Values_model_transistor['Darlington'] == 1:
                                    mainwindow.clip = "Icons/CC_Background_Darlington.gif"
                                else:
                                    mainwindow.clip = "Icons/CC_Background.gif"
                                mainwindow.gif(mainwindow.clip)
                                ##set parameters
                                mainwindow.confdata.EC_CC_choice()
                                mainwindow.confdata.c1_label.setText(str(parameters['C1']))
                                mainwindow.confdata.c2_label.setText(str(parameters['C2']))
                                mainwindow.confdata.r1_label.setText(str(parameters['R1']))
                                mainwindow.confdata.r2_label.setText(str(parameters['R2']))
                                mainwindow.confdata.re_label.setText(str(parameters['Re']))
                                mainwindow.confdata.vcc_label.setText(str(parameters['VCC']))
                                mainwindow.confdata.rl_label.setText(self.RL_textedit.text())

                                self.bode = Bode(parameters['C1'] * parameters['RB'],
                                                 parameters['C4'] * mainwindow.conftran.stage.parallel(parameters['Re'],parameters['RL']))

                                ##tabs
                                Component_manager.To_comercial_parameters(parameters)
                                mainwindow.grid.addWidget(mainwindow.tabs, 0, 1)
                                mainwindow.confsheet.conf_sheet.clear()
                                mainwindow.confsheet.conf_sheet.appendPlainText(
                                    f'Transistor = {mainwindow.conftran.transistor_name}')
                                mainwindow.confsheet.conf_sheet.appendPlainText(
                                    "Tipo " + str(mainwindow.conftran.stage.Values_model_transistor['Type']))
                                for index in parameters:
                                    mainwindow.confsheet.conf_sheet.appendPlainText(f'{index} = {parameters[index]}')
                                mainwindow.confsheet.conf_sheet.setFont(QFont("Times", 15))
                                mainwindow.showMaximized()
                                self.reset_enable = True
                                self.close()
                            else:
                                QMessageBox.about(self, "Error AI", "Valor AI invalido o no ingresado")
                                mainwindow.sounds.error1()
                        else:
                            QMessageBox.about(self, "Error RL", "Valor RL invalido o no ingresado")
                            mainwindow.sounds.error1()
                else:
                    QMessageBox.about(self, "Error F2 ", "Valor F2 invalido o no ingresado")
                    mainwindow.sounds.error1()
            else:
                QMessageBox.about(self, "Error F1 ", "Valor F2 invalido o no ingresado")
                mainwindow.sounds.error1()
        else:
            mainwindow.sounds.error1()
            QMessageBox.about(self, "Error RS", "Valor RS invalido o no ingresado")

    def test_syntax(self, value):
        dot = 0
        mul = 0
        for index in range(len(value)):
            if value[index].lower() in "0123456789.km":
                if value[index] == '.':
                    dot += 1
                elif value[index].lower() in 'km':
                    mul += 1
                if mul > 1 or dot > 1:
                    return False
            else:
                return False
        return True

    def to_float(self, value):
        tmp = ''
        mul = 0
        for index in range(len(value)):
            if value[index] in "0987654321.":
                tmp += value[index]
            else:
                mul = value[index]
        tmp = float(tmp)
        if mul != 0:
            if mul.lower() == 'k':
                 tmp *= 1000
            elif mul.lower() == 'm':
                 tmp *= 1000000
        return tmp

    def clear(self):
        self.RL_textedit.setText('')
        self.RS_textedit.setText('')
        self.AV_textedit.setText('')
        self.F_textedit.setText('')

if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.showMaximized()
    sys.exit(App.exec())