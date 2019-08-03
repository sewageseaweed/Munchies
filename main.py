import webapp2
import jinja2
import os
import json
from google.appengine.api import urlfetch
import urllib
import random

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        home_template = the_jinja_env.get_template('templates/index.html')
        self.response.write(home_template.render())


class ResultsPage(webapp2.RequestHandler):
    def post(self):
        results_template = the_jinja_env.get_template('templates/results.html')
        business_id = 'qA38uWTbtEXVEOcL-7pGCA'

        API_KEY = 'wJy5tvjtXsI62xNcl8RbOHkrrm4n71Lln-0Qc6EVP67jR8PvzUfN1_PKnbsITXeFkRevwXJ3bGeOTgcVDRK7kK6Pp4siyL_pW24eg9t0lB58JJna54MQGidJe0Q6XXYx'

        location_restaurant = self.request.get('cities')
        radius_search = self.request.get('search_radius')
        restaurant_type = self.request.get('restaurant_category')


        ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
        params = {'term': 'bar',
                    'limit': 50,
                    'radius': 10000,
                    'location': location_restaurant}
        encoded_param = urllib.urlencode(params)
        ENDPOINT = ENDPOINT + '?' + encoded_param


        try:
            HEADERS = {'Authorization': 'bearer %s' % API_KEY}
            result = urlfetch.fetch(
                url=ENDPOINT,
                method=urlfetch.GET,
                headers=HEADERS)
            yelp_response = result.content
            yelp_json = json.loads(yelp_response)
            yelp_results = yelp_json['businesses']

            print(location_restaurant)
            print("**************************")
            print(yelp_results[0]['name'])

            ls = []
            info = {
            'food': yelp_results[0]['name']
            }

            self.response.write(results_template.render(info))
        #     for i in yelp_results:
        #         ls.append(i['name'])
        #         print(i['location']['address1'])
        #     for i in ls:
        #         self.response.write(i + "||||")
        except urlfetch.Error:
            logging.exception(yelp_json)




        #
        # response = urlfetch.fetch(url=ENDPOINT, headers=HEADERS)
        # lol = response('San Francisco').content
        # self.response.write(lol)
        # print(response)
        # print(lol)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/results', ResultsPage)
], debug=True)

#http = urllib3.PoolManager()
#response = http.request('GET', url=ENDPOINT, params=PARAMETERS, headers=HEADERS)

#data = response.json()

#print(len(data['businesses']))

#for i in data['businesses']:
#    print(i['name'])
