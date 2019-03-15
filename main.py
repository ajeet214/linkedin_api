from flask import Flask, jsonify, request
from modules.linkedinSearch_db import linkedin_search
from modules.linkedin_db import Profile_existance
from modules.profile_db import Profile_fetch
from raven.contrib.flask import Sentry


app = Flask(__name__)
sentry = Sentry(app)
profile_info = Profile_fetch()


@app.route('/api/v1/search/profile')
def search():
    query = request.args.get('q')
    obj = linkedin_search()
    result1 = obj.db_check(query)
    return jsonify(result1)


@app.route('/api/v1/profile')
def profile():

    query = request.args.get('id')
    result2 = profile_info.db_check(query)
    return jsonify(result2)


@app.route('/api/v1/search/id')
def email_checker():
    query = request.args.get('q')
    # obj = EmailChecker()
    obj1 = Profile_existance()
    data = obj1.db_check(query)
    # return jsonify({'data': data})
    return jsonify({'data': {'availability': data['profileExists']}})


if __name__ == '__main__':
    app.run(port=5003)
