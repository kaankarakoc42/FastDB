from requests import get,post
from base64 import b64decode,b64encode
from json import loads

class FastClient:
      def __init__(self,db:"database name",password:"database password",url:"server url"="http://127.0.0.1:1453/connection/"):
          self.db=db
          self.password=password
          self.url=url+self.db

      def send(self,json):
          json.update({"password":self.password})
          return clientDecode(post(self.url,clientEncode(json)))

      def get(self):  
          return loads(self.send({"action":"get"}))
 
      def write(self,jsonObject):
          return self.send({"action":"write","json":jsonObject})

      def delete(self,dict_):
          return self.send({"action":"delete","dict":dict_})
        
      def search(self,dict_):
          return self.send({"action":"search","dict":dict_})

      def update(self,dict_,jsonObject):
          return self.send({"action":"update","dict":dict_,"json":jsonObject})
      



#-------------FastClient-----------------

def clientDecode(text):
    return b64decode(text.content.decode("utf-8")).decode("utf-8").replace("'",'"')
    
def clientEncode(text):
    return b64encode(str(text).encode("utf-8"))