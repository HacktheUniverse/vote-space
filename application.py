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
    representative_ids = "|".join(representative_ids_list)
    # S000148|N000002|M000087|G000555

    bill_ids_url = "https://congress.api.sunlightfoundation.com/bills?query=NASA&fields=bill_id&last_vote_at__exists=true&apikey=a5871887a24348d1a40d969832721c91"
    bill_ids = "|".join(pluck("bill_id", requests.get(bill_ids_url).json()['results']))
    # hr4660-113|hr4412-113|hr3547-113|hr3304-113|hr2413-113|hr1960-113|hr1232-113|hconres25-113|sconres8-113|hr967-113|hr933-113|hr667-113|hr152-113|hres1714-111|hres1421-111|hres1231-111|hres67-111|s3729-111|s3454-111|s1391-111

    voter_ids_url = "https://congress.api.sunlightfoundation.com/votes?bill_id__in=" + bill_ids + "&fields=voter_ids&vote_type=passage&voter_ids__in=" + representative_ids + "&apikey=a5871887a24348d1a40d969832721c91"
    voter_ids = "|".join(pluck("bill_id", requests.get(bill_ids_url).json()['results']))

    # https://congress.api.sunlightfoundation.com/votes?bill_id__in=hr4660-113|hr4412-113|hr3547-113|hr3304-113|hr2413-113|hr1960-113|hr1232-113|hconres25-113|sconres8-113|hr967-113|hr933-113|hr667-113|hr152-113|hres1714-111|hres1421-111|hres1231-111|hres67-111|s3729-111|s3454-111|s1391-111&fields=voter_ids&vote_type=passage&voter_ids__in=S000148|N000002|M000087|G000555&apikey=a5871887a24348d1a40d969832721c91

    all_votes_url = "https://congress.api.sunlightfoundation.com/votes?bill_id__in=" + bill_ids + "&fields=voters&vote_type=passage&apikey=a5871887a24348d1a40d969832721c91"
    all_votes = pluck("voters", requests.get(all_votes_url).json()['results'])

    scores = {}
    for vote in all_votes:
        for voter, value in vote.iteritems():
            if value['voter']['bioguide_id'] in representative_ids_list:
                name = value['voter']['first_name'] + ' ' + value['voter']['last_name']
                if not name in scores.keys():
                    scores[name] = 0
                if value['vote'] == "Nay":
                    scores[name] -= 1
                elif value['vote'] == "Yea":
                    scores[name] += 1

    return json.dumps(scores)

if __name__ == '__main__':
	app.run(debug=True)
