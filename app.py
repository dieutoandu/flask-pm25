from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
from pm25 import (
    get_pm25_data_from_mysql,
    update_db,
    get_pm25_data_by_site,
    get_all_counties,
    get_site_by_county,
)
import json

app = Flask(__name__)


@app.route("/pm25-county-site")
def pm25_county_site():
    county = request.args.get("county")
    site = get_site_by_county(county)

    result = json.dumps(site, ensure_ascii=False)

    return result


@app.route("/pm25-site")
def pm25_site():
    counties = get_all_counties()

    return render_template("pm25-site.html", counties=counties)


@app.route("/pm25-data-site")
def pm25_data_by_site():
    county = request.args.get("county")
    site = request.args.get("site")

    if not county or not site:
        result = {"erro": "county and site False"}
    else:
        datas, columns = get_pm25_data_by_site(county, site)
        df = pd.DataFrame(datas, columns=columns)
        date = df["datacreationdate"].apply(lambda x: x.strftime("%Y-%m-%d %H"))

        data = {
            "county": county,
            "site": site,
            "x_data": date.to_list(),
            "y_data": df["pm25"].to_list(),
            "pm25_max": df["pm25"].max(),
            "pm25_min": df["pm25"].min(),
        }

        result = json.dumps(data, ensure_ascii=False)
    return result


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

    df = pd.DataFrame(datas, columns=columns)

    counties = sorted(df["county"].unique().tolist())
    # print(counties)

    county = request.args.get("county", "ALL")

    if county == "ALL":
        df1 = df.groupby("county")["pm25"].mean().reset_index()
        x_data = df1["county"].tolist()

    else:
        df = df.groupby("county").get_group(county)
        x_data = df["site"].tolist()

    columns = df.columns.tolist()
    datas = df.values.tolist()
    y_data = df["pm25"].tolist()

    return render_template(
        "index.html",
        datas=datas,
        columns=columns,
        counties=counties,
        selected_county=county,
        x_data=x_data,
        y_data=y_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
