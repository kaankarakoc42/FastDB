from json import loads,dumps,load
from os import path,getcwd
from datetime import datetime
from base64 import b64decode,b64encode

class FastDB:

    def __init__(self,db_name):
        self.db=db_name
        self.createDB()

    def encode(self,text):
        return b64encode(text.encode("utf-8"))

  
    def decode(self,text):
        return b64decode(text.decode("utf-8")).decode("utf-8")
        
       
    def createDB(self):
        json={"db":self.db,"length":"-1","date":datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),"json":[]}
        if not path.exists(getcwd()+"/"+self.db+".fdb"):
           with open(self.db+".fdb","wb") as f:
                f.write(self.encode(str(json)))
    
    def getData(self):
        if not path.exists(getcwd()+"../"+self.db+".fdb"):
           with open(self.db+".fdb","rb") as f:
                st=self.decode(f.read()).replace("'",'"')
                db=loads(dumps(st))
           if db:
               return loads(db)
           else:
               return False
        else:
            return False      
           
    def writeData(self,jsonObject):
        db=self.getData()
        data=db["json"]
        data.append({str(int(db["length"])+1):jsonObject})
        json={"db":db["db"],"length":str(int(db["length"])+1),"date":db["date"],"json":data}
        with open(self.db+".fdb","wb") as f:
             f.write(self.encode(str(json)))

    def replace(self,list_,index,jsonObject):
        list_.pop(index)
        list_.insert(index,{str(index):jsonObject})

        

    def updateData(self,dict_,jsonObject):
        db=self.getData()
        liste=db["json"]
        if type(dict_)==dict:
           index=[ int(list(i.keys())[0]) for i in self.search(dict_)]
           [self.replace(liste,i,jsonObject) for i in index]
        elif type(dict_)==int:
           self.replace(liste,dict_,jsonObject)
        json={"db":db["db"],"length":db["length"],"date":db["date"],"json":liste}
        with open(self.db+".fdb","wb") as f:
             f.write(self.encode(dumps(json)))

    def getByIndex(self,index):
        return dumps(self.getData()["json"][index][str(index)],indent=4)

    def search(self,dict_):
        json=self.getData()["json"]
        return [json[i] for i in range(len(json)) if dict(set(list(json[i][str(i)].items())+list(dict_.items())))==json[i][str(i)]]

    def show(self):
        print(dumps(self.getData(),indent=4))



