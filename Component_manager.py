from Stack_manager import stack

class Component_manager:
    def __init__(self, c, type):
        self.Comercial_Resistors = [1, 1.2, 1.5, 1.8, 2.2,
                                    2.7, 3.3, 3.9, 4.7, 5.1,
                                    5.6, 6.8, 8.2, 10]
        self.Comercial_Capacitors = [1, 1.2, 2.2, 3.3,
                                     4.7, 5.6, 6.8, 8.2, 10]
        self.index = 0
        self.Component_stack = stack()
        self.Current_Component = c
        self.dot_amount = 0
        self.multiplier_amount = 0
        self.multiplier = 0
        self.Error_Component_vector = False
        self.Component_value = c
        self.Component = 0
        if isinstance(self.Component_value, str):
            self.to_decimal()
        if type != "R_no_comercial":
            if type.lower() == 'c' or type.lower() == 'r':
               if type.lower() == 'c':
                  self.normalization_value = self.normalization(self.Component_value)
                  self.Component_value = self.Component_value * pow(10, self.normalization_value)
            else:
                raise AssertionError('Tipo de componente no valido')
            self.tmp = self.Component_value
            self.Component_container = stack()
            if type.lower() == 'r':
                while self.tmp >= 1:
                        self.Component_values = self.heavier_values_Component(self.tmp)
                        self.Component_container.push(self.Comercial_comparation(self.Component_values, type)*pow(10,self.get_exp(self.tmp)))
                        self.tmp = self.tmp - self.Comercial_comparation(self.Component_values, type)*pow(10,self.get_exp(self.tmp))
            elif type.lower() == 'c':
                self.Component_values = self.heavier_values_Component(self.tmp)
                self.Component_container.push(self.Comercial_comparation(self.Component_values, type) * pow(10, self.get_exp(self.tmp)))
                self.Component_container.normalize(self.normalization_value)

    def to_decimal(self):
        while self.index < len(self.Current_Component) and self.dot_amount < 2 and self.multiplier_amount < 2:
            self.Component = self.Current_Component[self.index]
            if self.Component in "1234567890.":
                if self.Component == '.':
                    self.dot_amount += 1
                self.Component_stack.push(self.Component)
            elif self.Component.lower() in "kmun":
                self.multiplier = self.Component.lower()
                self.multiplier_amount += 1
            else:
                self.Error_Component_vector = True
            self.index += 1
        if self.dot_amount > 1 or self.multiplier_amount > 1 or self.Error_Component_vector == True:
            self.Component_stack.Empty()
            self.Error_Component_vector = True
            raise AssertionError('Cantidad de puntos o de multiplicadores incorrecta')
        else:
            if self.multiplier == 'k':
                self.Component_value = float(self.Component_stack.listToString()) * 1000
            elif self.multiplier == 'm':
                self.Component_value = float(self.Component_stack.listToString()) * 1000000
            elif self.multiplier == 'u':
                self.Component_value = float(self.Component_stack.listToString()) * 0.000001
            elif self.multiplier == 'n':
                self.Component_value = float(self.Component_stack.listToString()) * 0.000000001
            else:
                self.Component_value = float(self.Component_stack.listToString())

    def normalization(self,C):
        self.exp_normalization = 0
        while(C <= 100):
            C*=10
            self.exp_normalization+=1
        return self.exp_normalization

    def heavier_values_Component(self,C):
        self.Component_tmp = C
        while 10 <= self.Component_tmp:
            self.Component_tmp/=10
        return self.Component_tmp

    def Comercial_comparation(self, C, type):
        if type.lower() == 'r':
            self.vector_component = self.Comercial_Resistors
        elif type.lower() == 'c':
            self.vector_component = self.Comercial_Capacitors
        self.index = 0
        while(C >= self.vector_component[self.index]):
            self.index+=1
        if type.lower() == 'r':
            return self.vector_component[self.index - 1]
        elif type.lower() == 'c':
            return self.vector_component[self.index]
    def get_exp(self, number):
        self.number = number
        self.times = 0
        while (number>=1):
            number /= 10
            if number >= 1:
             self.times += 1
        return self.times

    def show_comercials(self):
        return self.Component_container.get_stack()

def To_comercial_parameters(Parameters):
    for index in Parameters:
        for index2 in Parameters[index]:
            if index2[0] == 'R':
                c = Component_manager(Parameters[index][index2], 'r')
                Parameters[index][index2] = c.show_comercials()
            elif index2[0] == 'C':
                c = Component_manager(Parameters[index][index2], 'c')
                Parameters[index][index2] = c.show_comercials()
