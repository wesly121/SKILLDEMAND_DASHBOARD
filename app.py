from flask import Flask, render_template, abort
import pandas as pd

app = Flask(__name__)

def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()

@app.route('/')
def dashboard():
    courses_df = load_data('courses.csv')
    jobs_df = load_data('jobs.csv')
    
    # Updated chart names to avoid Python naming conflicts
    skills_context = {
        "chart_labels": ["Python", "SQL", "Cloud", "AI", "Project Management"],
        "chart_values": [95, 85, 80, 75, 65]
    }
    
    return render_template('index.html', 
                           courses=courses_df.head(6).to_dict(orient='records'), 
                           jobs=jobs_df.head(5).to_dict(orient='records'), 
                           skills=skills_context)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    df = load_data('courses.csv')
    course = df[df['id'] == course_id]
    if course.empty:
        abort(404)
    return render_template('course_details.html', course=course.iloc[0].to_dict())

@app.route('/catalog')
def catalog():
    courses = load_data('courses.csv').to_dict(orient='records')
    return render_template('course_catalog.html', courses=courses)

@app.route('/all-jobs')
def all_jobs():
    jobs = load_data('jobs.csv').to_dict(orient='records')
    return render_template('all_jobs.html', jobs=jobs)

import os

if __name__ == '__main__':
    # Use the port assigned by the cloud, or 5000 if running locally
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' makes the app accessible to the external internet
    app.run(host='0.0.0.0', port=port)