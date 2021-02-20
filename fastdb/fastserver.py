from flask import Flask,request
from base64 import b64decode,b64encode
from fastdb import FastDB
from json import loads,dumps
from glob import glob

app=Flask(__name__,template_folder="html")

def parser(data,db):
    if data["action"]=="get":
       return str(db.get())
    if data["action"]=="write":
       db.write(data["json"])
       return "ok"     
    if data["action"]=="delete":
       db.delete(data["dict"])
       return "ok"          
    if data["action"]=="search":
       return str(db.search(data["dict"]))
    if data["action"]=="update":
       db.update(data["dict"],data["json"])
       return "ok"
    return encode("{'state':'invalid action'}")
        

@app.route("/connection/<db_name>",methods=["GET","POST"])
def connection(db_name):
    if request.method=="POST":
       if db_name in [i.split("\\")[1].split(".")[0] for i in glob(getPath())]:
          json=serverDecode(request.data)
          db=FastDB(db_name)
          if db.auth(json["password"]):
             return encode(parser(json,db))
          else:
             return encode("{'state':'invalid password'}")
       else:
          print(glob(getPath()))
          return encode("{'state':'not found'}")
    return encode("{'state':false}")


def run():
    app.run(port="1453")



#-------------Fastserver--------

def encode(text):
    return b64encode(text.encode("utf-8"))

def serverDecode(text):
    return loads(b64decode(text.decode("utf-8")).decode("utf-8").replace("'",'"'))

def getPath():
    liste=__file__.split("\\")
    liste.pop()
    liste="/".join(liste)
    return liste+f"/databases/*"


if __name__=="__main__":
   run()