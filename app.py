from flask import Flask, render_template, request
import pandas as pd
import os

print("Current working directory:", os.getcwd())  # Print the current working directory


# Define a dictionary to store project data (alternative to file system)
projects = {}

# Define the filename of the Excel file to load
file_to_load = "Ain Shams Bridge.xlsx"

# Print out the filename to be loaded
print("Filename to load:", file_to_load)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", project_names=[])

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
    # Load the Excel file
    try:
        file_path = os.path.join(os.getcwd(), file_to_load)  # Use os.getcwd() to get the current working directory
        projects[file_to_load] = pd.read_excel(file_path)
        print(f"Successfully loaded Excel file: {file_to_load}")
    except FileNotFoundError:
        print(f"Warning: Excel file not found: {file_to_load}")
    except Exception as e:
        print(f"Error loading Excel file: {file_to_load}: {e}")

    # Print loaded project names
    print("Projects loaded:", projects.keys())

    # Function to open the browser
    def open_browser():
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://127.0.0.1:5000/')

    Timer(1, open_browser).start()
    app.run(debug=True)
