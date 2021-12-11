#!/usr/bin/python
# # -*- coding: utf-8 -*-

# Copyright (C) 2019 EASYSOFT-IN
# All rights exclusively reserved for EASYSOFT-IN,
# unless otherwise expressly agreed.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# This file contains class for easin generator with some checkers helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import requests
import json
import random
import unittest
import string

def rndString(legnth):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(legnth))


class RestEntity:
    def __init__(self, baseurl="http://localhost:8080/serverTest/0.0.1-SNAP/api/", entity="", secured=False):
        self.baseurl = baseurl
        self.entity = entity
        self.secured= secured
        self.token= ""
        self.nsHeaders = {'content-type': 'application/json',
                        'Accept-Charset': 'UTF-8'}
        self.__refreshHeader()

    def __refreshHeader(self):
        if self.secured and self.token != "" :
            self.headers = {'Authorization':'Bearer '+self.token,
                        'content-type': 'application/json',
                        'Accept-Charset': 'UTF-8'}
        else:
            self.headers = {'content-type': 'application/json',
                        'Accept-Charset': 'UTF-8'}

    def Create(self, jsonEntity):
        self.__refreshHeader()
        query = requests.post(self.baseurl + self.entity +'/new', data=jsonEntity, headers=self.headers)
        print (self.entity + '  Created .. \t', query)        
        return query

    def GetOne(self, id):
        self.__refreshHeader()
        print (self.entity + '  Getted .. \t' + id)
        return requests.get(self.baseurl + self.entity + '/' + id, headers=self.headers)

    def ExportOne(self, id):
        self.__refreshHeader()
        print (self.entity + '  Getted .. \t' + id)
        return requests.get(self.baseurl + self.entity + '/' + id + '/export', headers=self.headers)

    def GetAll(self):
        self.__refreshHeader()
        print (self.entity + ' Getted  All .. \t')
        return requests.get(self.baseurl + self.entity + '/all', headers=self.headers)

    def Update(self, id, jsonEntity):
        self.__refreshHeader()
        print (self.entity + ' Updated .. \t' + id)
        return requests.put(self.baseurl + self.entity + '/' + id, data=jsonEntity, headers=self.headers)

    def Delete(self, id):
        self.__refreshHeader()
        print (self.entity + ' Deleted .. \t' + id)
        return requests.delete(self.baseurl + self.entity + '/' + id)

    def Auth(self, email, passwd):        
        da = '{"password":"'+passwd+'","email":"'+email+'"}'
        print (">>   Auth query ", da)
        query = requests.post(self.baseurl + 'auth/token',
                              data=da, headers=self.nsHeaders)
        print (">>  Server  ", query.json())
        self.token = query.json()['token']
        self.__refreshHeader()   
        return self.token     

class TestCrudUser(unittest.TestCase):
      def test_ANewUSerCreate(self):
        self.tester = RestEntity("http://localhost:8080/serverTest/0.0.1-SNAP/api/","user",True)
        self.userEmail1 = rndString(16)+'@'+rndString(8)+'.com'
        self.userPassword1 = "MonPassword1"    
        myName=rndString(10)
        query = self.tester.Create(
            '{"version":1,"name":"'+myName+'","phone":"'+rndString(10)+'","mainRole":"ROLE_ADMIN","password":"'+self.userPassword1+'","firstName":"'+rndString(10)+'","lastName":"'+rndString(10)+'","email":"'+self.userEmail1+'","activated":true,"langKey":"EN","imageUrl":"L0evg9vxAQ","resetDate":null,"id":null}')
        self.user = query.json()
        self.us_id = self.user['id']
        self.assertNotEqual(self.user['id'], 'null')
        self.assertEqual(self.user['email'], self.userEmail1)
        self.assertEqual(self.user['name'], myName)
        self.assertEqual(query.status_code, 201)
        print ("Hashed password is ",self.user['password'])
        print ("Generated ID  is ",self.user['id'])
        # Auth user
        token = self.tester.Auth(self.userEmail1, self.userPassword1)
        self.assertNotEqual(token, 'null')        
        print ("New User token granted is ",token)        


if __name__ == '__main__':
    # Run only the tests in the specified classes
    unittest.main()
