from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
from pm25 import get_pm25_data_from_mysql, update_db
import json

app = Flask(__name__)


@app.route("/update-db")
def update_pm25_db():
    row_count, message = update_db()
    nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = json.dumps(
        {"TIME": nowtime, "NEW DATE ": row_count, "MESSAGE ": message},
        ensure_ascii=False,
    )
    return result


@app.route("/")
def index():
    datas, columns = get_pm25_data_from_mysql()
    # print(datas)
    return render_template("index.html", datas=datas, columns=columns)


@app.route("/books")
def books_page():
    books = [
        {
            "name": "Python book",
            "price": 299,
            "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
        },
        {
            "name": "Java book",
            "price": 399,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
        },
        {
            "name": "C# book",
            "price": 499,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
        },
    ]

    # books = []
    if books:
        for key in books:
            print(key["name"])
            print(key["price"])
            print(key["image_url"])
    else:
        print("is no any books:")

    # return f"<h1>HELLO WORLD</h1><br>{datetime.now()}"
    username = "irving"
    nowtime = datetime.now().strftime("%Y-%m-%d")
    books = books
    print(username, nowtime)
    return render_template("books.html", name=username, now=nowtime, books=books)


@app.route("/bmi")
def get_bmi():
    # args => GET
    height = request.args.get("height")
    weight = request.args.get("weight")

    bmi = round(eval(weight) / (eval(height) / 100) ** 2, 2)

    return render_template("bmi.html", **locals())


@app.route("/pm25-data")
def get_pm25_data():
    api_url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=CSV"
    df = pd.read_csv(api_url)
    df["datacreationdate"] = pd.to_datetime(df["datacreationdate"])
    df1 = df.dropna()
    return df1.values.tolist()


if __name__ == "__main__":
    app.run(debug=True)
