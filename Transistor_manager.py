from Stack_manager import stack


class TransistorManager:
    def __init__(self, model):
        with open('Transistors_db.txt', 'r') as self.transistors_db:
            self.transistors_content = self.transistors_db.readlines()
            self.specs = stack()
            self.models_db = stack()
            self.model_specs = stack()
            self.tmp = ''
            self.tmp_index = 0
            self.model_location = 0
            self.shape = [0, range(len(self.transistors_content))]
            self.transistor_specs = {}
            if model != 'show':
                self.show_transitors_avaliables()
                # aqui se busca si hay coincidencia con el transistor ingresado
                for self.tmp_index in range(len(self.models_db)):
                    if self.models_db[self.tmp_index] == model:
                        self.model_location = self.tmp_index
                if self.model_location != 0:
                    # Aqui se crea un array con los specs
                    for self.index in range(len(self.transistors_content[0]) - 1):
                        if self.transistors_content[0][self.index] != ',':
                            self.tmp += self.transistors_content[0][self.index]
                            self.shape[0] += 1
                        else:
                            if self.tmp != '':
                                self.specs.push(self.tmp)
                                self.tmp = ''
                            self.shape[0] += 1
                    self.specs.push(self.tmp)
                    self.specs = self.specs.get_stack()
                    self.tmp = ''
                    # aqui se toman todos los datos de nuestro transistor
                    for self.index in range(len(self.transistors_content[self.model_location+1]) - 1):
                        if self.transistors_content[self.model_location+1][self.index] != ',':
                            self.tmp += self.transistors_content[self.model_location+1][self.index]
                        else:
                            if self.tmp != '':
                                self.model_specs.push(self.tmp)
                                self.tmp = ''
                    self.model_specs.push(self.tmp)
                    self.model_specs = self.model_specs.get_stack()
                    self.tmp = ''
                else:
                    raise AssertionError('Transistor no esta en base de datos')

    def get_transitor_specs(self):
        if self.model_location != 0:
            for self.tmp_index in range(len(self.model_specs)):
                if self.tmp_index > 1:
                     self.transistor_specs[self.specs[self.tmp_index]] = float(self.model_specs[self.tmp_index])
                else:
                    self.transistor_specs[self.specs[self.tmp_index]] = self.model_specs[self.tmp_index]
            return self.transistor_specs
        else:
            raise AssertionError('No se encontro el transistor')
    def show_transitors_avaliables(self):
        for self.index in self.shape[1]:
            while self.transistors_content[self.index][self.tmp_index] != ',':
                self.tmp += self.transistors_content[self.index][self.tmp_index]
                self.tmp_index += 1
            if self.tmp != 'Modelo':
                 self.models_db.push(self.tmp)
            self.tmp = ''
            self.tmp_index = 0
        self.models_db = self.models_db.get_stack()
        return self.models_db
