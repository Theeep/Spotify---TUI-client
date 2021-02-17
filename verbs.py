import requests


class Verbs():
    def __init__(self,token):
        #Headers needed for most requests
        self.headers =  {
        'Accept':'application/json',
        'Content-Type':'application/json',
        'Authorization':'Bearer '+token
        }
    def getRequest(self,pathURL,params = {}):
        response = requests.get(url = pathURL,headers=self.headers,params=params)
        return response.json()

    def putRequest(self,pathURL,params = {}):
        requests.put(url = pathURL,headers=self.headers,params=params)

    def postRequest(self,pathURL,params = {}):
        requests.post(url = pathURL,headers=self.headers,params=params)



# copying dicts if i need additional headers
#HEADERS = dict(self.headers)
#HEADERS.update(addHeaders)
