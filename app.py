import flask
from flask import request, render_template, redirect, url_for
from flask_cors import CORS
import requests
# import json

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "seasdad(*2sffcra01^23sdet"

CORS(app)

# Get this URL from the Azure Overview page of your API web app
api_url = "https://hunter-ml-backend.azurewebsites.net/" # base url for API endpoints

# main index page route
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    print("in predict route")
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        print("in post method")
        #### capture data from the form
        form = request.form  # declare a form variable to capture the form data
        print("extracted form data")
        print(form)
        # extract user data from the form and save it in a python variable
        age = form["age"]
        print(age)
        gender = form["gender"]
        country = form["country"]
        highest_deg = form["highest_deg"]
        coding_exp = form["coding_exp"]
        title = form["title"]
        company_size = form["company_size"]

        print(age, gender, country, highest_deg, coding_exp, title, company_size)

        # Create dictionary of form data
        salary_predict_variables = {
            "age": age,
            "gender": gender,
            "country": country,
            "highest_deg": highest_deg,
            "coding_exp": coding_exp,
            "title": title,
            "company_size": company_size,
        }

        # Send data to API as JSON
        url = api_url + f"/predict"
        print(url)
        headers = {"Content-Type": "application/json"}
        print(headers)

        # get a response from the api
        try:
            # Send data to API as JSON and get a response
            response = requests.post(
                url, json=salary_predict_variables, headers=headers
            )
            
            # Check if the response was successful (status code 200)
            if response.status_code == 200:
                # Decode the JSON response
                prediction = response.json()

                print(prediction)  # Print the decoded JSON for debugging
                
                # Pass the decoded JSON response to the HTML page
                return render_template("index.html", prediction=prediction)

            else:
                # Handle responses with error status codes
                print(
                    f"Error: Received response with status code {response.status_code}"
                )
                error_message = f"Failed to get prediction, server responded with status code: {response.status_code}"
                return render_template("index.html", error=error_message)

        except requests.exceptions.RequestException as e:
            # Handle network-related errors (e.g., DNS failure, refused connection, etc)
            print(f"Request failed: {e}")
            return render_template(
                "index.html", error="Failed to make request to prediction API."
            )