from fastdb import FastDB

db=FastDB("test")

for i in range(100):
    db.writeData({"val":i})

db.show()
