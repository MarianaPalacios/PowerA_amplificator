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
                        if self.config == 'EC':
                            mainwindow.vbox.removeWidget(mainwindow.btn_start)
                            if self.AV_textedit.text() != '' and self.test_syntax(self.AV_textedit.text()):
                                self.parameters['AV'] = self.to_float(self.AV_textedit.text())
                                mainwindow.vbox.removeWidget(mainwindow.movie_screen)
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

