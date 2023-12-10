"""
Project Afetadres by Murat Baran Polat/ ChatGPT

"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import json
import os
from scraper import fetch_tweets


class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # Add any additional fields if needed

def process_fetched_tweets():
    # Ensure the 'tweets.json' file exists
    if not os.path.exists('tweets.json'):
        print("No tweets to process.")
        return

    with open('tweets.json', 'r') as file:
        tweets = json.load(file)
        for tweet_data in tweets:
            # Extract relevant data from each tweet
            # Assume tweet_data contains 'message', 'phone', 'address', 'latitude', and 'longitude'
            # Adjust the following line according to the actual structure of your tweet data
            message, phone, address, latitude, longitude = extract_tweet_data(tweet_data)
            
            # Create and save a new report
            new_report = Report(message=message, phone=phone, address=address, 
                                latitude=latitude, longitude=longitude)
            db.session.add(new_report)
        db.session.commit()

def extract_tweet_data(tweet_data):
    # Extract and return relevant data from tweet_data
    # This is a placeholder function - implement according to your tweet data structure
    return tweet_data['message'], tweet_data['phone'], tweet_data['address'], tweet_data['latitude'], tweet_data['longitude']

@scheduler.task('interval', id='fetch_tweets_task', hours=12)
def scheduled_tweet_fetching():
    fetch_tweets("#afetadres", limit=50)  # Fetch tweets with Twint
    process_fetched_tweets()  # Process and store tweets
    print("Tweets fetched and processed.")

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/report', methods=['POST'])
def add_report():
    report_data = request.json
    new_report = Report(message=report_data['message'], phone=report_data['phone'], 
                        address=report_data['address'], latitude=report_data['latitude'], 
                        longitude=report_data['longitude'])
    db.session.add(new_report)
    db.session.commit()
    return jsonify({"status": "success"}), 201

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    return jsonify([{'message': report.message, 'phone': report.phone, 
                     'address': report.address, 'latitude': report.latitude, 
                     'longitude': report.longitude} for report in reports]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    scheduler.start()
    app.run(debug=True)
