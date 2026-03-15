from flask import Flask, render_template, abort
import pandas as pd
import os

app = Flask(__name__)

# This helps the server find your CSV files correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    try:
        # We skip bad lines to prevent crashes if a CSV row is messy
        return pd.read_csv(file_path, on_bad_lines='skip')
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return pd.DataFrame()

@app.route('/')
def dashboard():
    courses_df = load_data('courses.csv')
    jobs_df = load_data('jobs.csv')
    
    # Use .to_dict() safely only if the dataframe isn't empty
    courses = courses_df.head(6).to_dict(orient='records') if not courses_df.empty else []
    jobs = jobs_df.head(5).to_dict(orient='records') if not jobs_df.empty else []

    skills_context = {
        "chart_labels": ["Python", "SQL", "Cloud", "AI", "Project Management"],
        "chart_values": [95, 85, 80, 75, 65]
    }
    
    return render_template('index.html', courses=courses, jobs=jobs, skills=skills_context)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    df = load_data('courses.csv')
    if df.empty: abort(404)
    course = df[df['id'] == course_id]
    if course.empty: abort(404)
    return render_template('course_details.html', course=course.iloc[0].to_dict())

@app.route('/catalog')
def catalog():
    df = load_data('courses.csv')
    courses = df.to_dict(orient='records') if not df.empty else []
    return render_template('course_catalog.html', courses=courses)

@app.route('/all-jobs')
def all_jobs():
    df = load_data('jobs.csv')
    jobs = df.to_dict(orient='records') if not df.empty else []
    return render_template('all_jobs.html', jobs=jobs)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
