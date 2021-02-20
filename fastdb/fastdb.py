from os import path,getcwd,remove,mkdir
from datetime import datetime
from base64 import b64decode,b64encode
from json import loads,dumps

class FastDB:

    def __init__(self,db_name,password=None,mode="web"):
        self.db=db_name
        self.path=getMode(db_name,mode)
        self.password=getPassword(password,self.get)
        createDatabasesFolder()
        createDatabaseIfNotExists(self.db,self.path,self.password)

        
    def auth(self,password):
        if password==self.get()["password"]:
           return True
        return False
    
    def get(self):
        if path.exists(self.path):
           with open(self.path,"rb") as f:
                st=decode(f.read()).replace("'",'"')
                db=loads(dumps(st))
           if db:
               return loads(db)
           else:
               return False
        else:
            return False      
           
    def write(self,jsonObject):
        db=self.get()
        data=db["json"]
        data.append({str(int(db["length"])+1):jsonObject})
        json={"db":db["db"],"password":self.password,"length":str(int(db["length"])+1),"date":db["date"],"json":data}
        commit(self.path,json)

    
    def update(self,dict_,jsonObject):
        db=self.get()
        liste=db["json"]
        if type(dict_)==int:
           listIndex=getIndex(liste,str(dict_))
           replace(liste,int(listIndex),jsonObject)
        if type(dict_)==dict:
           jsonIndex=[ int(list(i.keys())[0]) for i in self.search(dict_)]
           listIndex=dict([tuple([list(liste[i].items())[0][0],str(i)]) for i in range(len(liste))])
           [replaceAndUpdate(liste,int(listIndex[str(jsonIndex[i])]),jsonIndex[i],jsonObject) for i in range(len(jsonIndex))]
        json={"db":db["db"],"password":db["password"],"length":db["length"],"date":db["date"],"json":liste}
        commit(self.path,json)

    def search(self,dict_):
        json1=self.get()["json"]
        json,index=pretifyIndex(json1)
        if type(dict_)==dict: 
           return [{index.get(str(i)):list(json[i].items())[0][1]} for i in range(len(json)) if dict(set(json[i][str(i)].items()).difference(set(dict_.items())))!=json[i][str(i)]]
        if type(dict_)==int:  
           try: return json1[[int(i) for i in index.values()].index(dict_)] 
           except: return []

    def delete(self,dict_):
        db=self.get()
        liste=db["json"]
        json={"db":db["db"],"password":self.password,"length":db["length"],"date":db["date"]}
        if type(dict_)==dict:
           jsonIndex=[ int(list(i.keys())[0]) for i in self.search(dict_)]
           listIndex=dict([tuple([list(liste[i].items())[0][0],str(i)]) for i in range(len(liste))])
           [liste.pop(int(listIndex[str(jsonIndex[i])])-i) for i in range(len(jsonIndex))]
        if type(dict_)==int:
           liste.pop([i  for i in range(len(liste)) if int(list(liste[i].keys())[0]) == dict_][0])
        json.update({"json":liste})
        commit(self.path,json)


    def destroy(self):
        remove(self.path)
    
    def show(self):
        print(dumps(self.get(),indent=4))




#-----------FastDB---------------

def getPath(name):
    liste=__file__.split("\\")
    liste.pop()
    liste="/".join(liste)
    return liste+f"/databases/{name}.fdb"

def getMode(db_name,mode):
    path=getPath(db_name)
    if mode=="local":  
       path=f"{getcwd()}\\{db_name}.fdb"
    return path

def getPassword(password,func):
    if password==None: 
       try:
         password=func()["password"]
       except:
           print("[-] password error")
           exit()
    return password

def createDatabasesFolder():
    if not path.exists(getPath("").replace(".fdb","")):
       mkdir(getPath("").replace(".fdb",""))

def createDatabaseIfNotExists(db,db_path,password):
    if not path.exists(db_path):
       json={"db":db,"password":password,"length":"-1","date":datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),"json":[]}
       with open(db_path,"wb") as f:
            f.write(encode(str(json)))

def encode(text):
    return b64encode(text.encode("utf-8"))

  
def decode(text):
    return b64decode(text.decode("utf-8")).decode("utf-8")

def pretifyIndex(liste):
    return [{str(i):list(liste[i].items())[0][1]} for i in range(len(liste))],dict([tuple([str(i),list(liste[i].items())[0][0]]) for i in range(len(liste))])


def replace(list_,index,jsonObject):
    list_.pop(index)
    list_.insert(index,{str(index):jsonObject})

def replaceAndUpdate(list_,index,rindex,jsonObject):
    list_.pop(index)
    list_.insert(index,{str(rindex):jsonObject})

def getIndex(liste,index):
    return dict([tuple([list(liste[i].items())[0][0],str(i)]) for i in range(len(liste))])[index]

def commit(path,json):
    with open(path,"wb") as f:
         f.write(encode(dumps(json)))