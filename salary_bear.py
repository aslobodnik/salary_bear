from flask import render_template,request,redirect, url_for, Flask
from slugify import slugify
import language_check


app = Flask(__name__)

tool = language_check.LanguageTool('en-US')

person ={  'state':'FL'
            ,'organization': 'Department of Health'
            ,'title':'Janitor'
            ,'first_name': 'Bob'
            ,'last_name': 'Dole'
            ,'middle_name': 'D'
            ,'salary':25000
            ,'id':1}


person_1 ={  'state':'IL'
                        ,'organization': 'Department of Hell'
                        ,'title':'Fail'
                        ,'first_name': 'dude'
                        ,'last_name': 'mother'
                        ,'middle_name': 'D'
                        ,'salary':25001
                        ,'id':2}
            

person_1['url'] = '/' + person_1['state'] + '/' + slugify(person_1['organization']) + '/' + slugify(person_1['first_name'] + ' ' + person_1['middle_name'] + ' ' + person_1['last_name']) + '-' + str(person_1['id'])

person['url'] = '/' + person['state'] + '/' + slugify(person['organization']) + '/' + slugify(person['first_name'] + ' ' + person['middle_name'] + ' ' + person['last_name']) + '-' + str(person['id'])

people = [person,person_1]

@app.route('/')
def home():
    return render_template('home.html',search_nav='active')

@app.route('/<state>/<organization>/<name>-<int:person_id>')
def profile(state,organization,name,person_id):
    person = people[person_id - 1]
    profile_text = generate_profile_description(person)
    return render_template('profile.html',person=person,profile_text=profile_text)

@app.template_filter('format_currency')
def format_currency(value):
    return "${:,.0f}".format(value)


def generate_profile_description(person):
    base_text = "{0} works for the {1} as an {2} making {3} per year."
    profile_text = base_text.format(person['first_name'],person['organization'],person['title'],format_currency(person['salary']))
    matches = tool.check(profile_text)
    if len(matches) != 0:
        profile_text = language_check.correct(profile_text, matches)
    return profile_text
    


if __name__ == "__main__":
    app.run(debug=True)
