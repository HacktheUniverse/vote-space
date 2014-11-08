import urllib2, simplejson, requests
from flask import Flask, render_template
from os.path import abspath, dirname

app = Flask(__name__)
app.root_path = abspath(dirname(__file__))

def update_settings(json=None):
	with open('settings.py', mode='r') as settingsfile:
	    settings = simplejson.loads(json)
	with open('settings.py', mode='w') as settingsfile:
	    settings['bills'] = bills
	    simplejson.dumps(settings, settingsfile)
	# data = urllib.urlencode(json)
	# h = httplib.HTTPConnection('myserver:8080')
	# app.data.driver.db['bills'].insert({ 'name': 'Joe' })
	# print app.data.driver.db['people']
	# app.test_client().post('/bills', data=simplejson.dumps({"bills":"Joe"}, content_type='application_json'))

bills = urllib2.urlopen("https://congress.api.sunlightfoundation.com/bills/search?query=NASA&apikey=a5871887a24348d1a40d969832721c91").read()
update_settings(bills)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
	app.debug = True
	app.run()
