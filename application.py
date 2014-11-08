import simplejson as json, requests, operator, pprint
from flask import Flask, render_template
from os.path import abspath, dirname
from funcy import pluck

app = Flask(__name__)
app.root_path = abspath(dirname(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_reps/<zip_code>')
def get_reps(zip_code):
    representatives_ids_url = "https://congress.api.sunlightfoundation.com/legislators/locate?zip=" + zip_code + "&fields=bioguide_id&apikey=a5871887a24348d1a40d969832721c91"
    representative_ids_list = pluck("bioguide_id", requests.get(representatives_ids_url).json()['results'])

    bill_ids_url = "https://congress.api.sunlightfoundation.com/bills?query=NASA&fields=bill_id&last_vote_at__exists=true&apikey=a5871887a24348d1a40d969832721c91"
    bill_ids = "|".join(pluck("bill_id", requests.get(bill_ids_url).json()['results']))

    all_votes_url = "https://congress.api.sunlightfoundation.com/votes?bill_id__in=" + bill_ids + "&fields=voters&vote_type=passage&apikey=a5871887a24348d1a40d969832721c91"
    all_votes = pluck("voters", requests.get(all_votes_url).json()['results'])

    scores = {}
    for vote in all_votes:
        for voter, value in vote.iteritems():
            if voter in representative_ids_list:
                if not voter in scores.keys():
                    scores[voter] = value['voter'];
                    scores[voter]['score'] = 0
                if value['vote'] == "Nay":
                    scores[voter]['score'] -= 1
                elif value['vote'] == "Yea":
                    scores[voter]['score'] += 1

    pprint.pprint(json.dumps(scores), width=1)
    return json.dumps(scores)

if __name__ == '__main__':
	app.run(debug=True)
