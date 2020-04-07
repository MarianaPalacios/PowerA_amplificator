from Transistor_manager import TransistorManager


class Stage:
    def __init__(self, model):
        self.VCC_nominal = [3, 5, 9, 12, 18, 24, 30, 35, 40, 50, 100, 200]
        self.VT = 0.026
        self.index = 0
        self.T = TransistorManager(model)
        self.Values_model_transistor = self.T.get_transitor_specs()
        self.parameters = {}
        self.pi = 3.141592

    def build_stage_CC(self, RS, RL, fc, fcs, AI):
        self.parameters['VCC'] = 5
        self.parameters['RS'] = RS
        self.parameters['RL'] = RL
        self.parameters['ICQ'] = self.Values_model_transistor['IC.Stable']*0.1
        self.parameters['Hib'] = self.VT/self.parameters['ICQ']
        self.parameters['hfe_MID'] = self.Values_model_transistor['hfe.MAX']*0.5
        if self.Values_model_transistor['Darlington'] == 1:
             self.parameters['VBE'] = 1.4
        else:
            self.parameters['VBE'] = 0.7
        self.parameters['Hie'] = self.parameters['hfe_MID']*self.parameters['Hib']
        self.parameters['RL'] = RL
        if 0 > self.parameters['VCC']/self.parameters['ICQ'] - RL:
            self.parameters['VCC'] = self.vcc_CC_fix()
        self.parameters['Re'] = self.parameters['VCC']/self.parameters['ICQ'] - RL
        self.parameters['RB'] = AI*RL
        self.parameters['Ren'] = self.parallel(self.parameters['RB'], self.parameters['Hie'] + 0.5*self.parameters['hfe_MID']*RL) + self.parameters['RS']
        if 0.1*self.parameters['hfe_MID']*self.parameters['Re'] < self.parameters['RB']:
            self.parameters['Stable_status'] = False
        else:
            self.parameters['Stable_status'] = True
        self.parameters['IB'] = self.parameters['ICQ']/self.parameters['hfe_MID']
        self.parameters['VBB'] = self.parameters['IB']*(self.parameters['RB']+(self.parameters['hfe_MID']+1)*self.parameters['Re']) + self.parameters['VBE']
        if self.parameters['VBB'] > self.parameters['VCC']:
            self.parameters['VCC'] = self.vcc_CC_fix2()
        self.parameters['R1'] = self.parameters['RB']*self.parameters['VCC']/self.parameters['VBB']
        self.parameters['R2'] = self.parameters['RB']*self.parameters['VCC']/(self.parameters['VCC'] - self.parameters['VBB'])
        self.parameters['C1'] = 10 / (2 * self.pi * fc* self.parameters['Ren'])
        self.parameters['C2'] = 10 / (2 * self.pi * fc* (self.parameters['Re'] + RL))
        self.parameters['C4'] = 1/(2*self.pi*fcs*0.5*self.parallel(self.parameters['Re'],self.parameters['RL']))
        return self.parameters

    def build_stage_EC(self, RS, RL, AV, fc, fcs, VCC):
        self.parameters['RS'] = RS
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
        self.parameters['RB'] = self.parameters['Re']*0.1*self.parameters['hfe_MID']
        self.parameters['IB'] = self.parameters['ICQ']/self.parameters['hfe_MID']
        self.parameters['VBB'] = self.parameters['IB']*(self.parameters['RB'] + (self.parameters['hfe_MID'] + 1)*self.parameters['Re']) + 0.7
        self.parameters['R1'] = self.parameters['VCC']*self.parameters['RB']/self.parameters['VBB']
        self.parameters['R2'] = self.parameters['VCC']*self.parameters['RB']/(self.parameters['VCC']-self.parameters['VBB'])
        self.parameters['Ren'] = self.parallel(self.parameters['RB'],self.parameters['hfe_MID']*(self.parameters['Hib']+self.parameters['Re']))
        self.parameters['Stable_status'] = self.parameters['Re1'] >= self.parameters['Hib']*8
        self.parameters['AI'] = AV*(self.parameters['Ren']/RL)
        self.parameters['C1'] = 10/(2*self.pi*fc*0.1*self.parameters['Ren'])
        self.parameters['C2'] = 10/(2*self.pi*fc*0.1*2*RL)
        self.parameters['C3'] = 10/(2*self.pi*fc*0.1*self.parallel(self.parameters['RB']+self.parameters['Hib'],self.parameters['Re']))
        self.parameters['C4'] = 1/(2*self.pi*fcs*self.parallel(self.parameters['RL'],self.parameters['Re']))
    def vcc_selection_ec(self):
        self.VCC_Minimun = self.parameters['ICQ'] * (1.5 * self.parameters['RL'] + self.parameters['Re1'])
        for self.index in range(len(self.VCC_nominal)):
            if self.VCC_Minimun < self.VCC_nominal[self.index]:
                return self.VCC_nominal[self.index + 1]

    def vcc_CC_fix(self):
        for self.index in range(len(self.VCC_nominal)):
            if self.VCC_nominal[self.index]/self.parameters['ICQ'] > self.parameters['RL']:
                return self.VCC_nominal[self.index + 1]

    def vcc_CC_fix2(self):
        for self.index in range(len(self.VCC_nominal)):
            if self.VCC_nominal[self.index] > self.parameters['VBB']:
                return self.VCC_nominal[self.index + 1]

    def parallel(self, R1, R2):
        return R1*R2/(R1+R2)

    def get_parameters(self):
        return self.parameters

