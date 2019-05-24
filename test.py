import requests
import json
import sqlite3
import datetime
import cherrypy

api_token = "626e358b-29fb-405c-bc6c-78506601c3ee"
api_base  = "https://ego-vehicle-api.azurewebsites.net/api/" 

headers = {'Content-Type': 'application/json',
           'x-api-key': '{0}'.format(api_token)}    

class Dsia(object):
    
    @cherrypy.expose
    def index(self):
        database = sqlite3.connect("database.sql")
        return str(database.execute("select * from journey as j join timeframe as t on j.timeframe = t.id sort by j.timeframe;").fetchone())
    
    @cherrypy.expose
    def list_journeys(self):
        database = sqlite3.connect("database.sql")
        buffer = []
        for t in database.execute("select name, distance, t.start, t.end from journey as j join timeframe as t on j.timeframe=t.id order by t.start asc;").fetchall():
            buffer.append(list(t))
        return json.dumps(buffer)

    @cherrypy.expose
    def enter_new_journey(self,**data):
        try:
            with sqlite3.connect("database.sql") as database:
                database.execute("insert into timeframe (start, end) values ({},{})".format(int(data["timestemp"]), int(data["duration"])))
                (id_t, _, _) = database.execute("select * from timeframe where start={} and end={}".format(data["timestemp"], data["duration"])).fetchone()
                database.execute("insert into journey (distance, timeframe, name) values ({},{},'{}')".format(data["distance"], id_t, data["journey"]))
                return "ok"
        except:
            return "bitte überprüfe deine Eingaben"
            
    @cherrypy.expose
    def test(self):
        return open("proto1.htm")

if __name__ == "__main__":
    # response = requests.get("https://ego-vehicle-api.azurewebsites.net/api/v1", headers=headers)
    # Print the status code of the response.
    # print(response.json()["vehicle"]["team"])
    config = {
        '/css':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "css/",
            'tools.staticdir.root': "/Users/lukas/quellcode/general_projects/hackathon/"
         }
    }
    cherrypy.quickstart(Dsia(), config=config)
