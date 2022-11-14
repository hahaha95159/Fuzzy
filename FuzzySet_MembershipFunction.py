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
            "AdhesiveCapsulitis","ShoulderContusion", "SubacromialBursitis", "ShoulderSprain", "SupraspinatusTendonRupture", "BicepsTendinitis", "BicepsTendonRupture", 
            "ElbowInjury", "MedialEpicondylitis", "LateralEpicondylitis", "OlecranonBursitis", "SupinatorSyndrome", 
            "PerimyotenositisExtensorRadialAspect", "WristSprain", "InferiorRadioulnarJointSprain", "CarpalTunnelSyndrome", "TFCCSprain", "DeQuervainDisease","GanglionCyst", "CubitTubeSyndrome",
            "MetacarpophalangealSprain","TenovaginitisFlexorDigitorum","ExtensorTendonRupture"
            ]
        self.AllDiseaseGroups = [
            3,1,2,3,3,2,2,
            3,4,4,2,4,
            2,2,2,4,2,4,3,2,
            2,2,2
    ]

        self.stdunitSymptom = [
			["肩部酸","肩部壓痛","旋轉肌萎縮","肩部僵"],
		    ["肩部腫脹","肩部痛","肩部壓痛","肩部瘀血"],
		    ["肩外側腫脹","肩峰下壓痛","肩痛放射至頸部","肩痛放射至肘部","肩痛放射至肩胛","肩關節內收時疼痛減輕","肩關節內旋時疼痛減輕","三角肌腫塊"],
		    ["肩外側痛","肩痛傳導至手臂","肩痛傳導至手部","肩痛傳導至斜方肌","三角肌壓痛","遇寒肩痛加重","肩平舉時痛","肱骨大粗隆壓痛"],
		    ["肩外側劇痛","肩部無力","肱骨大粗隆壓痛"],
		    ["肩前外側腫脹","肩前外側痛","肩前外側壓痛","肘關節阻力屈曲時捻發音","三角肌痙攣"],
		    ["肩內前側劇痛","肱二頭肌瘀血","結節間溝壓痛","肱二頭肌腫塊","肘關節屈曲時捻發音"],
		    
		    ["肘部無力","肘前側壓痛","肱橈關節後側腫脹","肘痛屈曲加劇","肘痛旋前加劇","肘痛旋後加劇"],
		    ["肘部腫脹","刺激尺神經肘部無力","刺激尺神經小指麻","刺激尺神經無名指麻","內上髁壓痛"],
		    ["肘部無力","肘外側腫脹","外上髁壓痛","肘痛持物時加劇","持物時肘痛"],
		    ["肘皮溫高","肘部痛","肘部壓痛","肘部腫塊","肘部紅"],
		    ["肘外側壓痛"],
            
		    ["腕橈側痛","腕橈側壓痛","前臂皮溫高","腕橈側腫脹","握拳時捻發音","腕關節屈曲時捻發音","腕關節伸直時捻發音"],
		    ["腕橈側痛","腕尺骨莖突痛","腕部無力","腕部腫脹","握拳時腕部痛","腕掌尺側壓痛","腕皮溫高","腕部筋節"],	
		    ["尺骨小頭壓痛","握力減","肘關節屈曲時尺骨小頭凸出"],
		    ["手指僵","手指麻","手指痛","拇指無力","手指痛勞累後加劇","手指痛放射至肩部","手指痛放射至肘部","大魚際萎縮","手指痛晨起加劇","手麻活動後減輕","手痛活動後減輕"],
		    ["腕尺側腫脹","腕尺側痛","尺骨莖突遠側壓痛","腕關節間隙壓痛","握力減","甩手彈響聲"],
		    ["橈骨莖突腫脹","橈骨莖突痛","橈骨莖突壓痛","腕部熱"],
		    ["腕部無力","腕部痛","腕部酸","腱鞘囊腫塊","腫塊壓痛"],	
		    ["腕部痛","手部痛","腕部麻","手部麻","腕部無力","易醒","手部無力","腕部痛放射至腋窩","手部痛放射至肘部","腕部痛放射至肘部","手部痛放射至腋窩","無名指感覺遲鈍","小指感覺遲鈍"],    
		    
            ["手指劇痛","掌指關節手指腫脹","掌指關節壓痛","掌指關節瘀血","握力減"],
		    ["手部筋節","掌指關節掌側酸","掌指關節屈曲時彈響","掌指關節伸直時彈響","掌指關節掌側壓痛"],
		    ["手指劇痛","手指腫脹","錘狀指","手指壓痛"]
        ]

        self.stdBody = [
			[["肩關節阻力內旋受限"],["肩關節屈曲受限","肩關節伸直受限","肩關節內收受限","肩關節外展受限","肩關節內轉受限","肩關節外轉受限"]], 
			[""], 
			[["肩關節外展受限","肩關節外轉受限"]], 
			[["肩關節外展受限","肩關節外轉受限"],["肩關節阻力外展受限"]], 
			[["肩關節外展受限","肩關節屈曲受限"],["肩外展韻律紊亂陽性"]], 
			[["肘關節阻力屈曲受限"]], 
			[["肘關節屈曲受限"]], 
			
			[["肘關節屈曲受限","肘關節伸直受限"],["肘關節旋前受限","肘關節旋後受限"]], 
			[["腕關節阻力屈曲受限"],["腕關節被動伸直受限"],["肘關節阻力旋前受限"]], 
			[["肘關節旋前受限"],["肘關節伸直受限"],["腕關節阻力伸直受限"]],
			[["肘關節屈曲受限","肘關節伸直受限"]], 
			[["拇指伸直受限"],["掌指關節伸直受限"],["肘關節旋前受限","肘關節旋後受限"]], 
            
			[["腕關節屈曲受限","腕關節伸直受限","腕關節尺偏受限","腕關節橈偏受限"]], 
			[["腕關節屈曲受限","腕關節伸直受限","腕關節尺偏受限","腕關節橈偏受限"]], 
			[["腕關節尺偏受限","腕關節橈偏受限"]], 
			[["拇指對掌受限","拇指外展受限"],["Tinel陽性"],["Phalentest陽性"]], 
			[["腕關節尺偏受限","腕關節橈偏受限","腕關節伸直受限","腕關節屈曲受限"]], 
			[["腕關節尺偏受限"],["拇指外展受限","拇指伸直受限"],["Finkelstein測試陽性"]], 
			[["掌指關節外展受限","掌指關節內收受限"],["拇指屈曲受限","拇指伸直受限"]], 
			[["Phalentest陽性"]],
            
			[["掌指關節內收受限","掌指關節外展受限"]], 
			[["掌指關節屈曲受限","掌指關節伸直受限"]], 
			[["指間關節屈曲受限","指間關節伸直受限"]]
	]
        
    def create(self):
        for i in range(0, 23):
            self.Diseases.append(
                TraumatologyDisease(self.AllDisease[i], self.AllDiseaseGroups[i])
                )
    def diff(self, patient):
        print(len(self.Diseases))
        self.create()
        for i in range(0, len(self.Diseases)):
            self.Diseases[i].set_Disease(self.stdunitSymptom[i])
            self.Diseases[i].set_DiseaseCheck(self.stdBody[i])
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
        
    def getSTDNumber(self, patient, TraumatologyDisease):
        patientSymptom = patient.split("。")
        stdPoint = 0
        for j in patientSymptom:
            if TraumatologyDisease.Disease[0].count(j):
                stdPoint = stdPoint + 1
        return stdPoint
    
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
    
    def caculateSTD(self, normalPoint, TraumatologyDisease):
        if(normalPoint == len(TraumatologyDisease.Disease[0])):
            return 1
        elif (0 == normalPoint):
            return 0
        else:
            return 1.0/len(TraumatologyDisease.Disease[0]) + ((pow(2, normalPoint)-1.0)/pow(2, normalPoint)) * (len(TraumatologyDisease.Disease[0])-1.0)/len(TraumatologyDisease.Disease[0])
    
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
        

class TraumatologyDisease:
    
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups
        
        self.Disease = []
        self.DiseaseCheck = []
        
        
    def set_Disease(self, symptom):
        self.Disease.append(symptom)
    
    def set_DiseaseCheck(self, stdBody):
        self.DiseaseCheck.append(copy.deepcopy(stdBody))
        
    def toString(self):
        return self.name
    
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
"肩部酸。肩部壓痛。旋轉肌萎縮。肩部僵。肩關節阻力內旋受限。肩關節屈曲受限。肩關節伸直受限。肩關節內收受限。肩關節外展受限。肩關節內轉受限。肩關節外轉受限"
,"肩部腫脹。肩部痛。肩部壓痛。肩部瘀血"
,"肩外側腫脹。肩峰下壓痛。肩痛放射至頸部。肩痛放射至肘部。肩痛放射至肩胛。肩關節內收時疼痛減輕。肩關節內旋時疼痛減輕。三角肌腫塊。肩關節外展受限。肩關節外轉受限"
,"肩外側痛。肩痛傳導至手臂。肩痛傳導至手部。肩痛傳導至斜方肌。三角肌壓痛。遇寒肩痛加重。肩平舉時痛。肱骨大粗隆壓痛。肩關節外展受限。肩關節外轉受限。肩關節阻力外展受限"
,"肩外側劇痛。肩部無力。肱骨大粗隆壓痛。肩關節外展受限。肩關節屈曲受限。肩外展韻律紊亂陽性"
,"肩前外側腫脹。肩前外側痛。肩前外側壓痛。肘關節阻力屈曲時捻發音。三角肌痙攣。肘關節阻力屈曲受限"
,"肩內前側劇痛。肱二頭肌瘀血。結節間溝壓痛。肱二頭肌腫塊。肘關節屈曲時捻發音。肘關節屈曲受限"
    
,"肘部無力。肘前側壓痛。肱橈關節後側腫脹。肘痛屈曲加劇。肘痛旋前加劇。肘痛旋後加劇。肘關節屈曲受限。肘關節伸直受限。肘關節旋前受限。肘關節旋後受限"
,"肘部腫脹。刺激尺神經肘部無力。刺激尺神經小指麻。刺激尺神經無名指麻。內上髁壓痛。腕關節阻力屈曲受限。肘關節阻力旋前受限。腕關節被動伸直受限"
,"肘部無力。肘外側腫脹。外上髁壓痛。肘痛持物時加劇。持物時肘痛。肘關節旋前受限。肘關節伸直受限。腕關節阻力伸直受限"
,"肘皮溫高。肘部痛。肘部壓痛。肘部腫塊。肘部紅。肘關節屈曲受限。肘關節伸直受限"
,"肘外側壓痛。拇指伸直受限。掌指關節伸直受限。肘關節旋前受限。肘關節旋後受限"
    
,"腕橈側痛。腕橈側壓痛。前臂皮溫高。腕橈側腫脹。握拳時捻發音。腕關節屈曲時捻發音。腕關節伸直時捻發音。腕關節屈曲受限。腕關節伸直受限。腕關節尺偏受限。腕關節橈偏受限"
,"腕橈側痛。腕尺骨莖突痛。腕部無力。腕部腫脹。握拳時腕部痛。腕掌尺側壓痛。腕皮溫高。腕部筋節。腕關節屈曲受限。腕關節伸直受限。腕關節尺偏受限。腕關節橈偏受限"
,"尺骨小頭壓痛。握力減。肘關節屈曲時尺骨小頭凸出。腕關節尺偏受限。腕關節橈偏受限"
,"手指僵。手指麻。手指痛。拇指無力。手指痛勞累後加劇。手指痛放射至肩部。手指痛放射至肘部。大魚際萎縮。手指痛晨起加劇。手麻活動後減輕。手痛活動後減輕。拇指對掌受限。拇指外展受限。Tinel陽性。Phalentest陽性"
,"腕尺側腫脹。甩手彈響聲。腕尺側痛。尺骨莖突遠側壓痛。腕關節間隙壓痛。握力減。腕關節尺偏受限。腕關節橈偏受限。腕關節伸直受限。腕關節屈曲受限"
,"橈骨莖突腫脹。橈骨莖突痛。橈骨莖突壓痛。腕部熱。腕關節尺偏受限。拇指外展受限。拇指伸直受限。Finkelstein測試陽性"
,"腕部無力。腕部痛。腕部酸。腱鞘囊腫塊。腫塊壓痛。掌指關節外展受限。掌指關節內收受限。拇指屈曲受限。拇指伸直受限"
,"腕部痛。手部痛。腕部麻。手部麻。腕部無力。易醒。手部無力。腕部痛放射至腋窩。手部痛放射至肘部。腕部痛放射至肘部。手部痛放射至腋窩。無名指感覺遲鈍。小指感覺遲鈍。Phalentest陽性" 
    
,"手部筋節。掌指關節掌側酸。掌指關節屈曲時彈響。掌指關節伸直時彈響。掌指關節掌側壓痛。掌指關節屈曲受限。掌指關節伸直受限"
,"手指劇痛。掌指關節手指腫脹。掌指關節壓痛。掌指關節瘀血。握力減。掌指關節內收受限。掌指關節外展受限"
,"手指劇痛。手指腫脹。錘狀指。手指壓痛。指間關節屈曲受限。指間關節伸直受限"
        ]

    
    test = TraumatologyModule()
    
    for i in ps:
        test.diff(i)
        weightTotal(TV_half, SV, BV, SVweight=0.5, BPweight=0.5)
        clean()
        TV.append(["AdhesiveCapsulitis","ShoulderContusion", "SubacromialBursitis", "ShoulderSprain", "SupraspinatusTendonRupture", "BicepsTendinitis", "BicepsTendonRupture", 
            "ElbowInjury", "MedialEpicondylitis", "LateralEpicondylitis", "OlecranonBursitis", "SupinatorSyndrome", 
            "PerimyotenositisExtensorRadialAspect", "WristSprain", "InferiorRadioulnarJointSprain", "CarpalTunnelSyndrome", "TFCCSprain", "DeQuervainDisease","GanglionCyst", "CubitTubeSyndrome",
            "MetacarpophalangealSprain","TenovaginitisFlexorDigitorum","ExtensorTendonRupture"])
        TV.append(copy.deepcopy(TV_half))
        TV_half.clear()
        test.reset()

        
    
    s = pd.DataFrame(TV)
    s.to_csv('55.csv', header=False, index=False)

