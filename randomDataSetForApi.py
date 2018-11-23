import random
import datetime
import numpy as np
from matplotlib import pyplot as mp
import sys

import requests
import datetime
import time

class GraphQLClient():
    """
    Class designed to interact with atHome's GraphQL BoxApi
    Only used to send samples at this moment
    """

    class Error(Exception):
        pass

    def __init__(self, api_url):
        self.api_url = api_url

    def send_sample(self, module_id, json_payload, date):
        """
        Sends a sample from a module to the BoxApi
        :param module_id: represents the id of the module the sample came from
        :param json_payload: Json String representing the environmental sample
        :param date: DateTime of the sampling, formatted as such: strftime('%Y-%m-%d %H:%M:%S.%f')
        :return: Nothing
        :raises GraphQLClient.Error should an error happen
        """
        # TODO check formatting of the parameters before sending calling the API
        module_id = str(module_id)
        # Using %() instead of str.format() as JSON ruins it because of the {}'s:)
        json_post_data = ''' 
        mutation {
            newSample (sample: {
              date: "%s"
              payload: "%s"   
              moduleId: %s   
            }){
              date
              payload
              moduleId
            }
        }
        '''
        json_payload = json_payload.replace("\"", "\\\"")
        json_post_data %= (date, json_payload, module_id)
        response = requests.post(self.api_url, json={"query": json_post_data})
        # TODO handle other errors: no connection / 200 with error response from the API
        if int(response.status_code) != 200:
            raise self.Error("invalid return code from the API: {}".format(response.status_code))




NB_SAMPLES = 24


def trunc_gauss(mu, sigma, bottom, top):
    a = random.gauss(mu, sigma)
    while (bottom <= a <= top) == False:
        a = random.gauss(mu, sigma)
        return a


def generateListOfGaussianDeltas(nbItems):
    def gaussian(x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

    mu, sig = 0, 0.5

    nums = gaussian(np.linspace(-2, 2, nbItems /2), mu, sig)

    # for samples slowly going Over then under the maximum threshold
    halfOfList = [(num * 1) for num in nums]
    # for samples slowly going Below then over the minimum threshold
    # otherHalf = [(num * -1) for num in nums]
    result = halfOfList # + otherHalf

    # enable this snippet if you wanna see the curves
    # mp.plot(result)
    # mp.show()

    return result * 2

# Plain Old Data model for Samples
class Sample:
    def __init__(self, timeStamp=0, moduleId=0, payload=""):
        self.timeStamp  = ""
        self.moduleId   = moduleId
        self.payload    = payload

    # GraphQL mutation to send to the api
    def __str__(self):
        return '''
        newSample(sample:{{ moduleId:{} payload:"{}" date: "{}" }}) {{
          moduleId
        }}'''.format(self.moduleId, self.payload, self.timeStamp)
    __repr__ = __str__

    def toJson(self):
        return json.dumps(self.__dict__)

def addFakeTimeLapseToSamples(listOfSamples):
    now = datetime.datetime.now()
    for x in range(NB_SAMPLES):
        timeElapsed = x * 300  # sampleID * 5 min
        fakeTimeStamp = (now + datetime.timedelta(seconds=timeElapsed))
        listOfSamples[x].timeStamp = fakeTimeStamp.strftime('%Y-%m-%dT%H:%M:%S.%f')



def makeTemperatureList(listOfDeltas):
    # 20 degrees Celsius + variations
    return [int(((delta * 1000) + 0)) for delta in listOfDeltas]


if __name__ == "__main__":
    graphQLClient = GraphQLClient("http://woodbox.io:8080/graphql")
    listOfRandomDeltas   = generateListOfGaussianDeltas(NB_SAMPLES)
    listOfSamples        = [Sample() for _ in range(NB_SAMPLES)]

    addFakeTimeLapseToSamples(listOfSamples)
    temperatures = makeTemperatureList(listOfRandomDeltas)
    for sample, temperature in zip(listOfSamples, temperatures):
        # °
        sample.payload = '''{{ "unit_measure": "ppm", "measure":"{}", "name":"CO" }}'''.format(temperature)
    for sample in listOfSamples:
        sample.moduleId = 3

    print("[")
    for sample in listOfSamples:
        print("  {")
        print('    "moduleId":"{}",'.format(sample.moduleId))
        print('    "payload":"{}",'.format(sample.payload.replace('"', '\\"')))
        print('    "date":"{}"'.format(sample.timeStamp))
        print("  },")
    print("]")



    sys.exit(0)


    jsonPostData = (''' 
            mutation {
                newSample (sample: {
                  date: "%s"
                  payload: "%s"   
                  moduleId: %s   
                }){
                  date
                  payload
                  moduleId
                }
            }
        ''' % ("lol", "lol", "0")).replace("\n", " ")
        # import re
        # jsonPostData = re.sub(" +", " ", jsonPostData)

    sample = listOfSamples[random.randint(0, 999)]
    # for sample in listOfSamples:
    # graphQLClient.send_sample(42, "youpiyoup", "lolxD")

    sys.exit(0)
