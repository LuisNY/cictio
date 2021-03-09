from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import json
from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../'))

from urllib.parse import urlparse

from ORM.base import getSession
from ORM.schema import City, Person

hostName = "localhost"
serverPort = 8080

class CictioServer(BaseHTTPRequestHandler):
    
    URLErrorMsg : str = "Invalid URL"

    # refuse to receive non-json content
    def validateJson(self, ctype: str):
        return False if ctype != 'application/json' else True

    #####################################################################
    def do_GET(self):
        
        first = urlparse(self.path).path.split('/')[1]

        if first == 'city':
            self.handleGetCity()

        elif first == 'people':
            self.handleGetPeople()

        else :
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(self.URLErrorMsg), "utf-8"))

    #####################################################################
    def do_POST(self):
        
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if self.validateJson(ctype) == False:
            self.send_response(400)
            self.end_headers()
            return
    
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        payload_string = self.rfile.read(length).decode('utf-8')
        payload = json.loads(payload_string)
        
        if self.path == '/city/add':
            self.handleAddNewCity(payload)

        elif self.path == '/people/add':
            self.handleAddNewPerson(payload)

        else :
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(self.URLErrorMsg), "utf-8"))
        

    #########################################################################################################
    ##### Handle GET requests ###############################################################################
    #########################################################################################################
    
    #####################################################################
    def handleGetCity(self):

        second = urlparse(self.path).path.split('/')[2]

        if second == 'population' :
            self.getCityPopulation()
        elif second == 'name' :
            self.getCityName()
        else :
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(self.URLErrorMsg), "utf-8"))

    #####################################################################
    # get population of city 'city_name'
    def getCityPopulation(self): #/city/population/'city_name'
        
        try:

            city = urlparse(self.path).path.split('/')[3]

            session = getSession()
            results = session.query(Person.ssn).filter_by(city_code=city).all()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(len(results)), "utf-8"))

        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(error), "utf-8"))

        except IndexError as e:

            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(str(e)), "utf-8"))

    #####################################################################
    def getCityName(self) : 
        
        try:

            city = urlparse(self.path).path.split('/')[3]

            if city == 'all' :
                self.getAllCityNames()

            elif city == 'most_populated' :
                self.getMostPopulatedCity()  

            else :
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes(json.dumps(self.URLErrorMsg), "utf-8"))    

        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(error), "utf-8"))

        except IndexError as e:

            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(str(e)), "utf-8"))    


    #####################################################################
    # get name of most populated city
    def getMostPopulatedCity(self) : #/city/name/most_populated

        session = getSession()

        results = session.query(func.count(Person.city_code).label("occurrence"), Person.city_code).group_by(Person.city_code).order_by(desc("occurrence")).all()
        
        res_len = len(results)
        index = 0
        city_names = []

        if res_len > 0 :
            city_names.append({results[index][1] : results[index][0]})
            max_num = results[index][0]
            index += 1

            while  index < res_len :
                if max_num > results[index][0] :
                    break
                city_names.append({results[index][1] : results[index][0]})
                index += 1

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(city_names), "utf-8"))

    #####################################################################
    # get the names of all cities in DB
    def getAllCityNames(self) : #/city/name/all
        
        session = getSession()

        results = session.query(City.name).all()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(results), "utf-8"))
            
    #####################################################################
    def handleGetPeople(self) :
        
        try:
            second = urlparse(self.path).path.split('/')[2]
            
            if second == 'ssn': 
                self.handleGetSsnFromName()

            elif second == 'name':
                self.handleGetNameFromSSN()

            else :
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes(json.dumps(self.URLErrorMsg), "utf-8"))

        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(error), "utf-8"))

        except IndexError as e:

            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(str(e)), "utf-8"))

    #####################################################################
    # get all the SSNs of people named 'first_name'
    def handleGetSsnFromName(self): #/people/ssn/'first_name'

        name = urlparse(self.path).path.split('/')[3] 

        session = getSession()
    
        results = session.query(Person.ssn).filter_by(first_name=name).all()   
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(results), "utf-8"))
    

    #####################################################################
    # get first and last name of person with SSN = 'ssn'
    def handleGetNameFromSSN(self): #/people/name/'ssn'

        ssn = urlparse(self.path).path.split('/')[3] 
            
        session = getSession()

        results = session.query(Person.first_name, Person.last_name).filter_by(ssn=ssn).all()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(results), "utf-8"))


    #########################################################################################################
    ##### Handle POST requests ##############################################################################
    #########################################################################################################

    #####################################################################
    # add new city to DB
    def handleAddNewCity(self, payload):
        
        if self.validateNewCityObj(payload) == False:
            self.send_response(400)
            self.end_headers()
            return

        session = getSession()

        try:

            newCity = City(payload['name'], payload['code'], payload['country'])    
            session.add(newCity)
            session.commit()
            
        except SQLAlchemyError as e:
            
            error = str(e.__dict__['orig'])
            session.rollback()
            session.close()
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(error), "utf-8"))
        
        else:
            
            session.close()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(payload), "utf-8"))


    #####################################################################
    def validateNewCityObj(self, payload: dict) -> bool :

        if payload.get('name') == None:
            return False
        if payload.get('code') == None:
            return False
        if payload.get('country') == None:
            return False
        
        return True


    #####################################################################
    # add new person to DB
    def handleAddNewPerson(self, payload):

        if self.validateNewPersonObj(payload) == False:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps("Incorrect json payload"), "utf-8"))
            return

        session = getSession()

        try:
            dob = parser.parse(payload['dob'])
            newPerson = Person(payload['first_name'], payload['last_name'], dob, payload['ssn'], payload['city_code'])
            session.add(newPerson)
            session.commit()
            
        except SQLAlchemyError as e:
            
            error = str(e.__dict__['orig'])
            session.rollback()
            session.close()
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(error), "utf-8"))
        
        except ValueError as e:

            session.rollback()
            session.close()
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(str(e)), "utf-8"))

        else:
            
            session.close()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(str(payload['first_name'], " was added")), "utf-8"))


    #####################################################################
    def validateNewPersonObj(self, payload) -> bool :
        
        if payload.get('first_name') == None:
            return False
        if payload.get('last_name') == None:
            return False
        if payload.get('dob') == None:
            return False
        if payload.get('ssn') == None:
            return False
        if payload.get('city_code') == None:
            return False
        
        return True
         


def getServer():
    
    return HTTPServer(("localhost", 8080), CictioServer)
    
    