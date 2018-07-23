import os
import fnmatch
from flask import render_template,request
from .markov_model import basic_markov_model, format_output
from app import app

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.realpath(os.path.dirname(__file__))
DEFAULTS = {"file": os.path.join(APP_ROOT, "wkl_taunts.txt"), 
			"wordnum": 200,
			"seed":None}

@app.route("/")
@app.route("/index")
def index():
    output = ""
    return render_template("index.html", taunt_output=output)

@app.route("/maketaunt", methods=['GET', 'POST'])
def run_markov_model():
	if request.method == 'POST': #this block is only entered when the form is submitted
		filename = request.form.get('file-upload')
		wordnum = request.form['wordnum']
		seed = request.form['seed']

		if not filename:
			filename = DEFAULTS["file"]

		if not wordnum:
			wordnum = DEFAULTS["wordnum"]
		else:
			wordnum = int(wordnum)

		if not seed:
			seed = DEFAULTS["seed"]
		else:
			seed = int(seed)
		
		if fnmatch.fnmatch(filename, '*.txt'):
			output_raw, startseed = basic_markov_model(filename, wordnum, seed_var=seed)
			output = format_output(output_raw, startseed)
		else:
			output = "Wrong! I said upload a .txt file, asshole!"
		return render_template("maketaunt.html", taunt_output=output);
