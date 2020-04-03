from Transistor_manager import TransistorManager


class Stage:
    def __init__(self, model):
        self.VCC_nominal = [3, 5, 9, 12, 18, 24, 30]
        self.VT = 0.026
        self.index = 0
        self.T = TransistorManager(model)
        self.Values_model_transistor = self.T.get_transitor_specs()
        self.parameters = {}
        self.pi = 3.141592

    def buld_stage_CC(self, RL, Ren, VCC, fc, hfe, darlinton):
        self.parameters['ICQ'] = self.Values_model_transistor['IC.Stable']
        self.parameters['Hib'] = self.VT/self.parameters['ICQ']
        self.parameters['VCC'] = VCC
        if darlinton:
            self.parameters['hfe'] = hfe
            self.parameters['VBE'] = 1.4
        else:
            self.parameters['hfe'] = self.Values_model_transistor['hfe.MAX']*0.7
            self.parameters['VBE'] = 0.7
        self.parameters['Hie'] = self.parameters['hfe']*self.parameters['Hib']
        if self.parameters['Hie'] + self.parameters['hfe']*0.5*RL >= Ren:
            self.parameters['RL'] = RL
            self.parameters['Re'] = VCC/(1.5*self.parameters['ICQ'])
            self.parameters['RB'] = Ren*(self.parameters['Hie']+self.parameters['hfe']*RL*0.5)/((self.parameters['Hie']+self.parameters['hfe']*RL*0.5)-Ren)
            self.parameters['VBB'] = self.parameters['ICQ']/self.parameters['hfe']*(self.parameters['RB']+(self.parameters['hfe']+1)*self.parameters['Re']) + self.parameters['VBE']
            if self.parameters['VBB'] > VCC:
                for self.index in range(len(self.VCC_nominal)):
                    self.parameters['VCC'] = self.VCC_nominal[self.index]
                if self.parameters['VBB'] > VCC:
                    raise AssertionError('Valor de Ren no apropiado, intente con un transistor con mayor hfe')
            self.parameters['R1'] = self.parameters['RB']*VCC/self.parameters['VBB']
            self.parameters['R2'] = self.parameters['RB']*VCC/(VCC - self.parameters['VBB'])
            self.parameters['C1'] = 10 / (2 * self.pi * fc * RL)
            self.parameters['C2'] = 10 / (2 * self.pi * fc * 2 * RL)
            return self.parameters
        else:
            raise AssertionError('No es posible hacer la maxima excursion')

    def build_stage_RS_EC(self, RL, RS, AV, fc, VCC):
        self.parameters['RS'] = RS
        return self.build_stage_EC(RL, AV, fc, VCC)

    def build_stage_EC(self, RL, AV, fc, VCC):
        self.parameters['AV'] = AV
        self.parameters['RL'] = RL
        self.parameters['hfe_MID'] = self.Values_model_transistor['hfe.MAX']*0.5
        if VCC == 0:
             self.parameters['ICQ'] = self.Values_model_transistor['IC.Stable']
        else:
             self.parameters['ICQ'] = VCC/(1.5*RL)*0.9
             self.parameters['VCC'] = VCC
        self.parameters['Hib'] = self.VT/self.parameters['ICQ']
        self.parameters['Re1'] = self.parameters['RL']*0.5/AV - self.parameters['Hib']
        if VCC == 0:
            self.parameters['VCC'] = self.vcc_selection_ec()
        self.parameters['Re2'] = self.parameters['VCC']/self.parameters['ICQ'] - self.parameters['RL']*1.5
        self.parameters['Re'] = self.parameters['Re2'] + self.parameters['Re1']
        self.parameters['RB'] = self.parameters['Re']*0.02*self.parameters['hfe_MID']
        self.parameters['IB'] = self.parameters['ICQ']/self.parameters['hfe_MID']
        self.parameters['VBB'] = self.parameters['IB']*(self.parameters['RB'] + (self.parameters['hfe_MID'] + 1)*self.parameters['Re']) + 0.7
        self.parameters['R1'] = self.parameters['VCC']*self.parameters['RB']/self.parameters['VBB']
        self.parameters['R2'] = self.parameters['VCC']*self.parameters['RB']/(self.parameters['VCC']-self.parameters['VBB'])
        self.parameters['Ren'] = self.parallel(self.parameters['RB'],self.parameters['hfe_MID']*(self.parameters['Hib']+self.parameters['Re']))
        self.parameters['Stable_status'] = self.parameters['Re1'] >= self.parameters['Hib']*8
        self.parameters['AI'] = AV*(self.parameters['Ren']/RL)
        self.parameters['C1'] = 10/(2*self.pi*fc*self.parameters['Ren'])
        self.parameters['C2'] = 10/(2*self.pi*fc*2*RL)
        self.parameters['C3'] = 10/(2*self.pi*fc*self.parallel(self.parameters['RB']+self.parameters['Hib'],self.parameters['Re']))
    def vcc_selection_ec(self):
        self.VCC_Minimun = self.parameters['ICQ'] * (1.5 * self.parameters['RL'] + self.parameters['Re1'])
        for self.index in range(len(self.VCC_nominal)):
            if self.VCC_Minimun < self.VCC_nominal[self.index]:
                return self.VCC_nominal[self.index + 1]

    def parallel(self, R1, R2):
        return R1*R2/(R1+R2)

    def get_parameters(self):
        return self.parameters