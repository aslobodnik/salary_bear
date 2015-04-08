from flask import render_template,request,redirect, url_for, Flask

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',search_nav='active')

if __name__ == "__main__":
    app.run(debug=True)
