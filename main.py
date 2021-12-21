from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pickle
import sklearn

app = Flask(__name__)

@app.route('/')
def home():
    connection = sqlite3.connect('db/Advertising.db')
    cursor = connection.cursor()
    query = '''SELECT price FROM price'''
    cursor.execute(query)
    price = cursor.fetchall()
    query_delete = '''DELETE FROM price'''
    cursor.execute(query_delete)
    connection.commit()
    connection.close()
    return render_template("index.html", price_list=price)


@app.route("/v1/predict_price", methods=['POST'])
def predict_price():
    connection = sqlite3.connect('db/Advertising.db')
    cursor = connection.cursor()

    TV, radio, newspaper = None, None, None

    try :
        TV = request.form['TV']
        radio = request.form['radio']
        newspaper = request.form['newspaper']

        model = pickle.load(open('model/advertising.model', 'rb'))
        prediction = model.predict([[float(TV), float(radio), float(newspaper)]])
        pred = [str(round(prediction[0], 2))+" €"]

    except:
        pred =  ["Missing values, the sales won't be predicted"]

    query = '''INSERT INTO price (price) VALUES (?);'''
    cursor.execute(query, pred)

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()