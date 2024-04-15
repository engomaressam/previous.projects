from flask import Flask, render_template, request
import pandas as pd
import os
import webbrowser
from threading import Timer

# Define a dictionary to store project data (alternative to file system)
projects = {}

# Get the list of files in the root directory
root_files = os.listdir()

# Print out the filenames in the root directory for debugging purposes
print("Filenames in root directory:")
print(root_files)

# Extract project names from Excel files in the root directory
project_names = [os.path.splitext(filename)[0] for filename in root_files if filename.endswith(".xlsx")]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", project_names=project_names)

@app.route("/project", methods=["POST"])
def show_project():
    if 'project' in request.form:
        selected_project = request.form["project"]
        print(f"Selected project: {selected_project}")  # Debug: Print selected project name

        # Debug: Print the keys of the projects dictionary
        print(f"Available projects: {list(projects.keys())}")

        if selected_project in projects:
            project_table = projects[selected_project]  # Get project data
            print(f"Project data: {project_table}")  # Debug: Print project data
            return render_template("forms.html", project_table=project_table.to_html())
        else:
            print(f"Available projects: {list(projects.keys())}")  # Debug: Print available project names
            return render_template("forms.html", message="Project not found!")
    else:
        return render_template("forms.html", message="Please select a project.")


if __name__ == "__main__":
    # Read Excel files and store data in the projects dictionary
    projects = {}
    for filename in root_files:
        if filename.endswith(".xlsx"):  # Check for Excel files
            project_name = os.path.splitext(filename)[0]
            file_path = os.path.join(os.getcwd(), filename)  # Construct full path
            try:
                projects[project_name] = pd.read_excel(file_path)
                print(f"Successfully loaded Excel file for project: {project_name}")  # Debug: Print successful loading
            except FileNotFoundError:
                print(f"Warning: Excel file not found for project: {project_name}")
            except Exception as e:
                print(f"Error loading Excel file for project {project_name}: {e}")

    # Function to open the browser
    def open_browser():
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://127.0.0.1:5000/')

    Timer(1, open_browser).start()
    app.run(debug=True)
