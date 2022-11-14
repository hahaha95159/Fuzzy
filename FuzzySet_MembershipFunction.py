# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 11:51:36 2022

@author: user
"""
import copy
import pandas as pd

SV = []
BV = []
SP = []
BP = []

TV = []

TV_half = []
TV_64 = []
TV_73 = []
TV_82 = []

class TraumatologyModule:
    
    def __init__(self):        
        self.normalPoint =  0
        self.bodyPoint = 0
        self.normalValue =  0.0
        self.bodyValue = 0.0
        self.totalPoint = 0.0
        self.Diseases = []

        self.AllDisease = [
        #set your diseases group
            ]
        self.AllDiseaseGroups = [
        #set each disease's group numbers
    ]

        self.stdunitSymptom = [
			#[set a disease's standard symptom]
            #[seconde disease's standard symptom]
            #[[if your disease has subgroup in unit group], [do like this]]
            #["a empty set"]
        ]

        self.stdBody = [
			#[set a disease's standard body exam symptom]
            #[seconde disease's standard body exam symptom]
            #[[if your disease has subgroup in unit group], [do like this]]
	]
    
    def create(self):
        #range dependent by your diseases set size
        for i in range(0, 23):
            self.Diseases.append(
                TraumatologyDisease(self.AllDisease[i], self.AllDiseaseGroups[i])
                )
    #differentiation start
    def diff(self, patient):
        self.create()
        #set standard symptoms
        for i in range(0, len(self.Diseases)):
            self.Diseases[i].set_Disease(self.stdunitSymptom[i])
            self.Diseases[i].set_DiseaseCheck(self.stdBody[i])
        #set the intersection & value in list
        for i in range(0, len(self.Diseases)):
            self.normalPoint = self.getSTDNumber(patient, self.Diseases[i])
            SP.append(self.normalPoint)
            self.bodyPoint = self.getBodyNumber(patient, self.Diseases[i])
            BP.append(self.bodyPoint)
            self.reBody(self.Diseases[i])
            self.normalValue = self.caculateSTD(self.normalPoint, self.Diseases[i])
            SV.append(self.normalValue)
            self.bodyValue = self.caculateBody(self.bodyPoint, self.Diseases[i])
            BV.append(self.bodyValue)
        #print("SV:",SV)
        #print("SP:",SP)
        #print("BV:",BV)
        #print("BP:",BP)
        
    
    def reBody(self, Disease):
        Disease.DiseaseCheck[0] = self.stdBody[self.AllDisease.index(Disease.toString())]
    
    #cacu intersection between STD symptom & patient
    def getSTDNumber(self, patient, TraumatologyDisease):
        patientSymptom = patient.split("。")
        stdPoint = 0
        for j in patientSymptom:
            if TraumatologyDisease.Disease[0].count(j):
                stdPoint = stdPoint + 1
        return stdPoint
    #cacu intersection between body exam symptom & patient
    def getBodyNumber(self, patient, Diseases):
        patientSymptom = patient.split("。")
        bodyPoint = 0
        if Diseases.toString() == 'ShoulderContusion':
            bodyPoint = 0 
        for j in patientSymptom:
            for k in range(0, Diseases.groups-1):
                if (Diseases.DiseaseCheck[0][k] != 1) and (Diseases.DiseaseCheck[0][k].count(j)):
                    Diseases.DiseaseCheck[0][k] = 1
        for i in Diseases.DiseaseCheck[0]:
            if i==1:
                bodyPoint = bodyPoint + 1
        return bodyPoint
    #cacu standard symptom's value
    def caculateSTD(self, normalPoint, TraumatologyDisease):
        if(normalPoint == len(TraumatologyDisease.Disease[0])):
            return 1
        elif (0 == normalPoint):
            return 0
        else:
            return 1.0/len(TraumatologyDisease.Disease[0]) + ((pow(2, normalPoint)-1.0)/pow(2, normalPoint)) * (len(TraumatologyDisease.Disease[0])-1.0)/len(TraumatologyDisease.Disease[0])
    #cacu body exam's value
    def caculateBody(self, bodyPoint, TraumatologyDisease):
        if TraumatologyDisease.toString() == 'ShoulderContusion':
            return None
        if(bodyPoint == TraumatologyDisease.groups-1):
            return 1
        elif (bodyPoint == 0):
            return 0
        else:
            return 1.0/(TraumatologyDisease.groups-1.0) + (TraumatologyDisease.groups-2.0)/(TraumatologyDisease.groups-1.0) * ((pow(2, bodyPoint)-1)/pow(2, bodyPoint))
          
    
    def reset(self):
        self.normalPoint =  0
        self.bodyPoint = 0
        self.totalPoint = 0.0
        self.Diseases = []
        
#unit disease class
class TraumatologyDisease:
    
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups
        
        #STD
        self.Disease = []
        #body exam
        self.DiseaseCheck = []
        
    #setter
    def set_Disease(self, symptom):
        self.Disease.append(symptom)
    #setter
    def set_DiseaseCheck(self, stdBody):
        self.DiseaseCheck.append(copy.deepcopy(stdBody))
        
    def toString(self):
        return self.name

#cacu membership function weighted by weight    
def weightTotal(TV_half, SV, BP, SVweight=0.5, BPweight=0.5):
    for i,j in zip(SV, BV):
        if j is None:
            TV_half.append(i)
        else :
            TV_half.append(i*SVweight + j*BPweight)
    

def clean():
    SV.clear()
    BV.clear()
    SP.clear()
    BP.clear()
    

if __name__ == '__main__':
    ps = [
    #put patient's symptom like "armache。handache"
        ]

    
    test = TraumatologyModule()
    
    for i in ps:
        test.diff(i)
        weightTotal(TV_half, SV, BV, SVweight=0.5, BPweight=0.5)
        clean()
        #gen csv file
        TV.append(["first row"])
        TV.append(copy.deepcopy(TV_half))
        TV_half.clear()
        test.reset()

        
    
    s = pd.DataFrame(TV)
    s.to_csv('name.csv', header=False, index=False)

