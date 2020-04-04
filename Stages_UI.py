from PyQt5.QtWidgets import QGridLayout, QTabWidget, QListWidget, QLineEdit, QPlainTextEdit, QListWidgetItem, QMessageBox, QVBoxLayout, QApplication, QLabel, QWidget, QSizePolicy, QMenuBar, QAction, QMainWindow, QPushButton, QGroupBox, QHBoxLayout, QRadioButton
import sys
from PyQt5.QtGui import QIcon, QPalette, QMovie, QFont, QPixmap
from PyQt5.QtCore import Qt, QByteArray, QSize
from Transistor_manager import TransistorManager
from Stage_constructor import Stage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 200
        self.width = 300
        self.height = 250
        self.setWindowTitle("Transistor Wizard")
        self.mainIcon = "transistor.jpg"
        self.conftran = Conftran()
        self.parameters_conf = 0
        self.initWindow()

    def initWindow(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        self.widget()
        self.CreateMenu()

    def CreateMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Archivo")
        HelpMenu = mainMenu.addMenu("Ayuda")

        SaveAction = QAction(QIcon(self.mainIcon), "Guardar como pdf", self)
        SaveAction.setShortcut("ctrpl+g")
        fileMenu.addAction(SaveAction)

        ResetConfigAction = QAction(QIcon(self.mainIcon), "Nueva configuracion", self)
        ResetConfigAction.setShortcut("ctrpl+r")
        fileMenu.addAction(ResetConfigAction)

        HelpAction = QAction(QIcon(self.mainIcon), "Acerca de", self)
        HelpAction.setShortcut("ctrpl+f")
        HelpMenu.addAction(HelpAction)

    def widget(self):
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.gif()

        self.datasheet = QPlainTextEdit()
        self.datasheet.setReadOnly(True)
        self.datasheet.setFont(QFont("Times", 20))
        self.btn_start = QPushButton("Iniciar configuracion")
        self.btn_start.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.btn_start.setFont(QFont("Times", 15))
        self.btn_start.clicked.connect(self.btn_start_config)
        ##gif configuracion

        self.tabs
        ##Tabs para mostrar datos de la configuracion
        self.tabs = QTabWidget()
        self.tabWidget.addTab(ConfData(), "Configuracion de transistor")
        self.tabWidget.addTab(ConfSheet(), "Datos comerciales")

        self.hbox.addWidget(self.conf_sheet)
        self.hbox.addWidget(self.tabs)

        self.vbox.addWidget(self.btn_start)
        self.btn_start.setIcon(QIcon("Icons/Transistor.png"))
        self.btn_start.setIconSize(QSize(150,150))
        widget = QWidget()
        widget.setLayout(self.vbox)
        self.setCentralWidget(widget)

    def gif(self):
        ##Configuracion del gif#########
        self.movie = QMovie("Icons/gif.gif", QByteArray(), self)
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()
        self.vbox.addWidget(self.movie_screen)
    def btn_start_config(self):
        self.conftran.show()
        self.close()

class ConfSheet(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout
        self.conf_sheet = QPlainTextEdit()
        vbox.addWidget(self.conf_sheet)

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
        self.hbox = QHBoxLayout()
        self.gif()
        self.labels_icons()
        self.setLayout(self.hbox)

    def gif(self):
        ##Configuracion del gif#########
        self.movie = QMovie("Icons/CC_background.gif", QByteArray(), self)
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()
        self.hbox.addWidget(self.movie_screen)

    def labels_icons(self):
        grid = QGridLayout()

        c1_label = QLabel("C1")
        c1_image = QLabel(self)
        c1_pixmap = QPixmap("Icons/C1.png")
        c1_image.setPixmap(c1_pixmap)
        grid.addWidget(c1_label,0,0)
        grid.addWidget(c1_image,0,1)

        c2_label = QLabel("C2")
        c2_image = QLabel(self)
        c2_pixmap = QPixmap("Icons/C2.png")
        c2_image.setPixmap(c1_pixmap)
        grid.addWidget(c2_label, 1, 0)
        grid.addWidget(c2_image, 1, 1)

        c3_label = QLabel("C3")
        c3_image = QLabel(self)
        c3_pixmap = QPixmap("Icons/C3.png")
        c3_image.setPixmap(c3_pixmap)
        grid.addWidget(c3_label, 2, 0)
        grid.addWidget(c3_image, 2, 1)

        r1_label = QLabel("R1")
        r1_image = QLabel(self)
        r1_pixmap = QPixmap("Icons/R1.png")
        r1_image.setPixmap(r1_pixmap)
        grid.addWidget(r1_label, 3, 0)
        grid.addWidget(r1_image, 3, 1)

        r2_label = QLabel("R2")
        r2_image = QLabel(self)
        r2_pixmap = QPixmap("Icons/R2.png")
        r2_image.setPixmap(r2_pixmap)
        grid.addWidget(r2_label, 4, 0)
        grid.addWidget(r2_image, 4, 1)

        re1_label = QLabel("RE1")
        re1_image = QLabel(self)
        re1_pixmap = QPixmap("Icons/RE1.png")
        re1_image.setPixmap(re1_pixmap)
        grid.addWidget(re1_label, 0, 2)
        grid.addWidget(re1_image, 0, 3)

        re2_label = QLabel("RE2")
        re2_image = QLabel(self)
        re2_pixmap = QPixmap("Icons/RE2.png")
        re2_image.setPixmap(re2_pixmap)
        grid.addWidget(re2_label, 1, 2)
        grid.addWidget(re2_image, 1, 3)

        rc_label = QLabel("RC")
        rc_image = QLabel(self)
        rc_pixmap = QPixmap("Icons/RC.png")
        rc_image.setPixmap(rc_pixmap)
        grid.addWidget(rc_label, 2, 2)
        grid.addWidget(rc_image, 2, 3)

        rl_label = QLabel("RL")
        rl_image = QLabel(self)
        rl_pixmap = QPixmap("Icons/RL.png")
        rl_image.setPixmap(rl_pixmap)
        grid.addWidget(rl_label, 3, 2)
        grid.addWidget(rl_image, 3, 3)

        vcc_label = QLabel("VCC")
        vcc_image = QLabel(self)
        vcc_pixmap = QPixmap("Icons/VCC.png")
        vcc_image.setPixmap(vcc_pixmap)
        grid.addWidget(vcc_label, 4, 2)
        grid.addWidget(vcc_image, 4, 3)

        self.hbox.addLayout(grid)

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
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        vbox.addWidget(self.Transistor_List)
        vbox.addWidget(self.btn_accept)
        self.setLayout(vbox)

    def transistor_list(self):
        self.Transistor_List = QListWidget()

        transistor_models_avaliables = TransistorManager('show')
        transistor_models_avaliables = transistor_models_avaliables.show_transitors_avaliables()

        for index in range(len(transistor_models_avaliables)):
            l = QListWidgetItem(QIcon("Icons/Transistor.png"), transistor_models_avaliables[index])
            self.Transistor_List.insertItem(index, l)

    def radioButton(self):
        self.groupBox = QGroupBox("Elija Su configuracion")
        self.groupBox.setFont(QFont("Times", 13))
        hboxlayout = QHBoxLayout()

        self.EC_radio_button = QRadioButton()
        self.EC_radio_button.setChecked(True)
        self.EC_radio_button.setIcon(QIcon("Icons/EC.png"))
        self.EC_radio_button.setIconSize(QSize(150, 150))
        self.EC_radio_button.setFont(QFont("Sanserif", 13))
        self.EC_radio_button.toggled.connect(self.EC_button)
        hboxlayout.addWidget(self.EC_radio_button)

        self.CC_radio_button = QRadioButton()
        self.CC_radio_button.setIcon(QIcon("Icons/CC.png"))
        self.CC_radio_button.setIconSize(QSize(150, 150))
        self.CC_radio_button.setFont(QFont("Sanserif", 13))
        self.CC_radio_button.toggled.connect(self.CC_button)
        hboxlayout.addWidget(self.CC_radio_button)

        self.groupBox.setLayout(hboxlayout)

    def EC_button(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.config_selected = "EC"
            self.parameters = Parameters(self.config_selected)

    def CC_button(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.config_selected = "CC"
            self.parameters = Parameters(self.config_selected)

    def btn_accept_action(self):
        row = self.Transistor_List.currentRow()
        if row != -1:
            item = self.Transistor_List.item(row)
            self.transistor_name = item.text()
            self.parameters.show()
            self.close()
        else:
            QMessageBox.about(self, "Error", "Por favor seleccione un transistor")

class Parameters(QWidget):
    def __init__(self, config):
        super().__init__()
        self.top = 400
        self.left = 300
        self.height = 200
        self.width = 200
        self.config = config
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("Transistor.png"))
        self.setWindowTitle("Seleccion de parametros")
        self.stage = 0
        self.transistor_name = ""
        print(self.transistor_name)
        self.parameters = {}
        self.InitWindow()

    def InitWindow(self):
        RS_Panel = QGroupBox("Introduzca RS")
        RL_Panel = QGroupBox("Introduzca RL")
        self.AV_Panel = QGroupBox("Introduzca AV")
        self.AI_Panel = QGroupBox("Introduzca AI")
        F_Panel = QGroupBox("Introduzca F")
        VCC_Panel = QGroupBox("Introduzca VCC")

        hbox_RS = QHBoxLayout()
        hbox_RL = QHBoxLayout()
        hbox_VCC = QHBoxLayout()
        hbox_F = QHBoxLayout()
        hbox_AV = QHBoxLayout()
        hbox_AI = QHBoxLayout()

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

        self.F_label = QLabel("F")
        self.F_textedit = QLineEdit()
        hbox_F.addWidget(self.F_label)
        hbox_F.addWidget(self.F_textedit)
        F_Panel.setLayout(hbox_F)

        self.btn_Introducir_Datos = QPushButton("Aceptar")
        self.btn_Introducir_Datos.clicked.connect(self.btn_accept)

        self.MainParametersInput.addWidget(RS_Panel)
        self.MainParametersInput.addWidget(RL_Panel)
        self.MainParametersInput.addWidget(VCC_Panel)
        self.MainParametersInput.addWidget(F_Panel)
        if self.config == "EC":
            self.MainParametersInput.addWidget(self.AV_Panel)
        else:
            self.MainParametersInput.addWidget(self.AI_Panel)
        self.MainParametersInput.addWidget(self.btn_Introducir_Datos)
        self.setLayout(self.MainParametersInput)

    def btn_accept(self):
        if self.RS_textedit.text() != '' and self.test_syntax(self.RS_textedit.text()):
            if self.RL_textedit.text() != '' and self.test_syntax(self.RL_textedit.text()):
                if self.VCC_textedit.text() != '' and self.test_syntax(self.VCC_textedit.text()):
                    if self.F_textedit.text() != '' and self.test_syntax(self.F_textedit.text()):
                        self.parameters['RS'] = self.to_float(self.RS_textedit.text())
                        self.parameters['RL'] = self.to_float(self.RL_textedit.text())
                        self.parameters['VCC'] = self.to_float(self.VCC_textedit.text())
                        self.parameters['F'] = self.to_float(self.F_textedit.text())
                        mainwindow.vbox.removeWidget(mainwindow.btn_start)
                        if self.config == 'EC':
                            if self.AV_textedit.text() != '' and self.test_syntax(self.AV_textedit.text()):
                                self.parameters['AV'] = self.to_float(self.AV_textedit.text())
                                mainwindow.vbox.removeWidget(mainwindow.movie_screen)
                                mainwindow.movie.stop()
                                self.stage = Stage(mainwindow.conftran.transistor_name)
                                self.stage.build_stage_EC(self.parameters['RS'], self.parameters['RL'], self.parameters['AV'], self.parameters['F'], self.parameters['VCC'])
                                mainwindow.parameters_conf = self.stage.get_parameters()
                                mainwindow.datasheet.setPlainText(str(mainwindow.parameters_conf))
                                mainwindow.vbox.addWidget(mainwindow.datasheet)
                                mainwindow.setLayout(mainwindow.vbox)
                                mainwindow.show()
                                self.close()
                            else:
                                QMessageBox.about(self, "Error AV", "Valor AV invalido o no ingresado")
                        elif self.config == 'CC':
                            if self.AI_textedit.text() != '' and self.test_syntax(self.AI_textedit.text()):
                                self.parameters['AI'] = self.to_float(self.AI_textedit.text())
                                mainwindow.vbox.removeWidget(mainwindow.movie_screen)
                                self.stage = Stage(mainwindow.conftran.transistor_name)
                                self.stage.build_stage_CC(self.parameters['RS'], self.parameters['RL'],
                                                          self.parameters['F'], self.parameters['AI'],
                                                          self.parameters['VCC'])
                                mainwindow.parameters_conf = self.stage.get_parameters()
                                mainwindow.datasheet.setPlainText(str(mainwindow.parameters_conf))
                                mainwindow.vbox.addWidget(mainwindow.datasheet)
                                mainwindow.setLayout(mainwindow.vbox)
                                mainwindow.show()
                                self.close()
                            else:
                                QMessageBox.about(self, "Error AI", "Valor AI invalido o no ingresado")
                    else:
                        QMessageBox.about(self, "Error F ", "Valor F invalido o no ingresado")
                else:
                    QMessageBox.about(self, "Error VCC", "Valor VCC invalido o no ingresado")
            else:
                QMessageBox.about(self, "Error RL", "Valor RL invalido o no ingresado")
        else:
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
    mainwindow = ConfData()
    mainwindow.show()
    sys.exit(App.exec())