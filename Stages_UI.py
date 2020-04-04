from PyQt5.QtWidgets import QGridLayout, QTabWidget ,QListWidget, QLineEdit, QPlainTextEdit, QListWidgetItem, QMessageBox, QVBoxLayout, QApplication, QLabel, QWidget, QSizePolicy, QMenuBar, QAction, QMainWindow, QPushButton, QGroupBox, QHBoxLayout, QRadioButton
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QIcon, QPalette, QMovie, QFont, QPixmap
from PyQt5.QtCore import Qt, QByteArray, QSize, QFileInfo
from Transistor_manager import TransistorManager
import Component_manager
from Stage_constructor import Stage

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
        self.parameters_conf = 0
        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QIcon(self.mainIcon))
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        self.widget()
        self.CreateMenu()

    def CreateMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Archivo")
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

    def widget(self):
        self.grid = QGridLayout()
        self.gif(self.clip)
        self.create_button()
        self.open_tabs()
        self.Int_UI = QWidget()
        self.Int_UI.setLayout(self.grid)
        self.setCentralWidget(self.Int_UI)

    def help(self):
        self.help_window.show()

    def open_tabs(self):
        self.tabs = QTabWidget()
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
        self.close()

    def create_button(self):
        self.btn_start = QPushButton("Iniciar configuración")
        self.btn_start.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.btn_start.setFont(QFont("Times", 40))
        self.btn_start.setIcon(QIcon("Icons/Transistor.png"))
        self.btn_start.setIconSize(QSize(150, 150))
        self.btn_start.clicked.connect(self.btn_start_config)
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
            ##clean parameters

            self.conftran.parameters.AV_textedit.clear()
            self.conftran.parameters.AI_textedit.clear()
            self.conftran.parameters.RL_textedit.clear()
            self.conftran.parameters.RS_textedit.clear()
            self.conftran.parameters.VCC_textedit.clear()
            self.conftran.parameters.F_textedit.clear()

            mainwindow.conftran.parameters.reset_enable = False

            self.showMaximized()




class ConfSheet(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.conf_sheet = QPlainTextEdit(self)
        self.conf_sheet.setReadOnly(True)
        vbox.addWidget(self.conf_sheet)

        self.pdf_button = QPushButton("Guardar como pdf")
        self.pdf_button.setFont(QFont("Times", 12))
        self.pdf_button.setMinimumHeight(60)
        self.pdf_button.setIcon(QIcon("Icons/pdf.png"))
        self.pdf_button.clicked.connect(self.pdfExport)

        self.print_button = QPushButton("Imprimir")
        self.print_button.setIcon(QIcon("Icons/printer.png"))
        self.print_button.setMinimumHeight(60)
        self.print_button.setFont(QFont("Times", 12))
        self.print_button.clicked.connect(self.printDialog)

        hbox.addWidget(self.pdf_button)
        hbox.addWidget(self.print_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def pdfExport(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf)//All Files")

        if fn != '':
            if QFileInfo(fn).suffix() == "":fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.conf_sheet.print_(printer)

    def printDialog(self):
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

        self.re_label = QLabel("RE")
        self.re_label.setFont(QFont("Times", 14))
        self.re_image = QLabel(self)
        re_pixmap = QPixmap("Icons/RE.png")
        self.re_image.setPixmap(re_pixmap)
        self.grid.addWidget(self.re_label, 2, 0)
        self.grid.addWidget(self.re_image, 2, 1)
        self.hbox.addLayout(self.grid)

class Parameters(QWidget):
    def __init__(self, config):
        super().__init__()
        self.top = 250
        self.left = 500
        self.height = 200
        self.width = 200
        self.config = config
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.reset_enable = False
        self.setPalette(p)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("Transistor.png"))
        self.setWindowTitle("Seleccion de parametros")
        self.stage = 0
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
                        mainwindow.movie_screen.close()
                        mainwindow.grid.removeWidget(mainwindow.movie_screen)
                        mainwindow.btn_start.close()
                        mainwindow.grid.removeWidget(mainwindow.btn_start)
                        if self.config == 'EC':
                            if self.AV_textedit.text() != '' and self.test_syntax(self.AV_textedit.text()):
                                self.parameters['AV'] = self.to_float(self.AV_textedit.text())
                                self.stage = Stage(mainwindow.conftran.transistor_name)
                                self.stage.build_stage_EC(self.parameters['RS'], self.parameters['RL'], self.parameters['AV'], self.parameters['F'], self.parameters['VCC'])
                                parameters = self.stage.get_parameters()
                                ##gif
                                if self.stage.Values_model_transistor['Darlington'] == 1:
                                    mainwindow.clip = "Icons/EC_pnp_Darlington.gif"
                                else:
                                    if self.stage.Values_model_transistor['Type'] == "npn":
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
                                mainwindow.confdata.vcc_label.setText(self.VCC_textedit.text())
                                mainwindow.confdata.rl_label.setText(self.RL_textedit.text())

                                ##tabs
                                Component_manager.To_comercial_parameters(parameters)
                                mainwindow.grid.addWidget(mainwindow.tabs, 0, 1)
                                mainwindow.confsheet.conf_sheet.clear()
                                mainwindow.confsheet.conf_sheet.appendPlainText(f'Transistor = {mainwindow.conftran.transistor_name}')
                                for index in parameters:
                                    mainwindow.confsheet.conf_sheet.appendPlainText(f'{index} = {parameters[index]}')
                                mainwindow.confsheet.conf_sheet.setFont(QFont("Times", 15))
                                mainwindow.showMaximized()
                                self.reset_enable = True
                                self.close()
                            else:
                                QMessageBox.about(self, "Error AV", "Valor AV invalido o no ingresado")
                        elif self.config == 'CC':
                            if self.AI_textedit.text() != '' and self.test_syntax(self.AI_textedit.text()):
                                self.parameters['AI'] = self.to_float(self.AI_textedit.text())
                                self.stage = Stage(mainwindow.conftran.transistor_name)
                                self.stage.build_stage_CC(self.parameters['RS'], self.parameters['RL'],
                                                          self.parameters['F'], self.parameters['AI'],
                                                          self.parameters['VCC'])
                                parameters = self.stage.get_parameters()
                                ##gif
                                if self.stage.Values_model_transistor['Darlington'] == 1:
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
                                mainwindow.confdata.vcc_label.setText(self.VCC_textedit.text())
                                mainwindow.confdata.rl_label.setText(self.RL_textedit.text())
                                ##tabs
                                Component_manager.To_comercial_parameters(parameters)
                                mainwindow.grid.addWidget(mainwindow.tabs, 0, 1)
                                mainwindow.confsheet.conf_sheet.clear()
                                mainwindow.confsheet.conf_sheet.appendPlainText(
                                    f'Transistor = {mainwindow.conftran.transistor_name}')
                                for index in parameters:
                                    mainwindow.confsheet.conf_sheet.appendPlainText(f'{index} = {parameters[index]}')
                                mainwindow.confsheet.conf_sheet.setFont(QFont("Times", 15))
                                mainwindow.showMaximized()
                                self.reset_enable = True
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

class help(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.setWindowTitle("Ayuda")
        self.setWindowIcon(QIcon("Icons/help.png"))
        label = QLabel("Gracias profesor victor por las clases XD")
        label.setFont(QFont("Times", 14))
        image = QLabel(self)
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        pixmap = QPixmap("Icons/Amplifier.png")
        image.setPixmap(pixmap)
        vbox.addWidget(image)
        vbox.addWidget(label)
        self.setLayout(vbox)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.showMaximized()
    sys.exit(App.exec())