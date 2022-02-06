from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from roommates_bill import room

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):

    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)


class ResultsPage(MethodView):

    def post(self):
        billform = BillForm(request.form)
        amount = float(billform.amount.data)
        period = billform.period.data
        the_bill = room.Bill(amount, period)

        name1 = billform.name1.data
        days_in_house_1 = float(billform.days_in_house1.data)
        roommate1 = room.Roommate(name1, days_in_house_1)

        name2 = billform.name2.data
        days_in_house_2 = float(billform.days_in_house2.data)
        roommate2 = room.Roommate(name2, days_in_house_2)
        return render_template('results.html',
                               name1=roommate1.name, 
                               amount1=roommate1.pays(the_bill, roommate2),
                               name2=roommate2.name,
                               amount2=roommate2.pays(the_bill, roommate1))


class BillForm(Form):
    amount = StringField("Bill Amount: ", default="100")
    period = StringField("Bill Period: ", default="December 2021")

    name1 = StringField("Name: ", default="John")
    days_in_house1 = StringField("Days in the house: ", default=20)

    name2 = StringField("Name: ", default="Mary")
    days_in_house2 = StringField("Days in the house: ", default=12)

    button = SubmitField("Calculate")


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form', view_func=BillFormPage.as_view('bill_form_page'))
app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)
