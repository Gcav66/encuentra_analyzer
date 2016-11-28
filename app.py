from flask import Flask, request, redirect, render_template, session, url_for
from analyze_encuentra import read_and_clean, total
import os
from forms import RegistrationForm, OtherForm

def create_app():
    app=Flask(__name__)
    app.secret_key = 'myverylongsecetkey'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app

app = create_app()

"""
@app.route("/", methods=["GET", "POST"])
def bulk():
    if request.method == 'POST':
        if request.form['btn'] == 'value':
            car = request.form['carform']
            year = int(request.form['yearform'])
            cost_df = total(df, car, year)
            out_df = cost_df.to_html(classes="table table-hover")
            return render_template("result.html", mycar=car, myyear=year, valuation=out_df)
    cars = df['trimmed_name'].unique()
    cars.sort()
    #cars = [x for x in cars]
    form = RegistrationForm()
    form.car.choices = [(x, x) for x in cars]
    form.year.choices = [(y, y) for y in df[df.trimmed_name == form.car.data].clean_year.unique()] or []
    years = df['clean_year'].unique()
    yrs = [int(x) for x in years]
    yrs.sort(reverse=True)
    return render_template("index.html", cars=cars, years=yrs, form=form)
"""
@app.route("/", methods=["GET", "POST"])
def bulk():
    cars = df['trimmed_name'].unique()
    cars.sort()
    form = RegistrationForm()
    form.car.choices = [(x, x) for x in cars]
    if form.validate_on_submit():
    	#oform = OtherForm()
    	#oform.year.choices = [(y, y) for y in df[df.trimmed_name == form.car.data].clean_year.unique()] or []
    	#oform.car.choices = form.car.data
    	#session['year'] = oform.year.choices
    	session['car'] = form.car.data
    	return redirect(url_for("select"))
    return render_template("index.html", form=form)

@app.route("/select", methods=["GET", "POST"])
def select():
	#car = session['car'] or 'Peugot'
	car = str(session.get('car', None))
	print car
	print type(car)
	#year = session.get('year', None)
	oform = OtherForm()
	oform.year.choices = [(y, y) for y in df[df.trimmed_name == car].clean_year.unique()] or []
	oform.car.choices = [(car, car)]
	if oform.validate():
		print "valid"
	print oform.errors
	if request.method == "POST":
	#if oform.validate_on_submit():
		print oform.errors	
		year = oform.year.data
		year = int(float(year))
		cost_df = total(df, car, year)
		out_df = cost_df.to_html(classes="table table-hover")
		return render_template("result.html", mycar=car, myyear=year, valuation=out_df)
	return render_template("select.html", oform=oform)

if __name__ == "__main__":
	df = read_and_clean("../encuentro_data_2.xlsx")
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=int(port), debug=True)