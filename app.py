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
df = read_and_clean("encuentro_data_final.csv")

#New Comment
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
	oform.year.choices = [(y, y) for y in df[df.trimmed_name == car].clean_year.sort_values(ascending=False).unique()] or []
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

"""
@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/", methods=["GET", "POST"])
def test():
    cars = df['trimmed_name'].unique()
    cars.sort()
    form = RegistrationForm()
    form.car.choices = [(x, x) for x in cars]
    if form.validate_on_submit():
    	#car = form.car.data
    	session['car'] = form.car.data
    	comp_car = form.car.data.replace(" ", "_")
    	return redirect(url_for("show_car", comp_car=comp_car))
    return render_template("test.html", form=form)

@app.route("/<comp_car>", methods=["GET", "POST"])
def show_car(comp_car):
	car = str(session.get('car', None))
	oform = OtherForm()
	oform.year.choices = [(y, y) for y in df[df.trimmed_name == car].clean_year.sort_values(ascending=False).unique()] or []
	oform.car.choices = [(car, car)]
	if request.method == "POST":
	#if oform.validate_on_submit():
		print oform.errors	
		year = oform.year.data
		year = int(float(year))
		#cost_df = total(df, car, year)
		#out_df = cost_df.to_html(classes="table table-hover")
		return redirect(url_for("show_result", mycar=comp_car, myyear=year))
	return render_template("select.html", oform=oform)

@app.route("/<mycar>/<myyear>", methods=["GET", "POST"])
def show_result(mycar, myyear):
	car = str(session.get('car', None))
	cost_df = total(df, car, int(float(myyear)))
	out_df = cost_df.to_html(classes="table table-hover")
	return render_template("result.html", mycar=car, myyear=myyear, valuation=out_df)


if __name__ == "__main__":
	#df = read_and_clean("encuentro_data_final.csv")
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=int(port), debug=True)
