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
    projects = {}

    print("Current working directory:", os.getcwd())  # Add this line to print the current working directory

    # Get the filename to load from user input or command line argument
    filename = "Ain Shams Bridge.xlsx"

    # Attempt to load the Excel file
    file_path = os.path.join(os.getcwd(), filename)  # Use os.getcwd() to get the current working directory
    try:
        projects[filename] = pd.read_excel(file_path)
        print(f"Successfully loaded Excel file: {filename}")
    except FileNotFoundError:
        print(f"Error: Excel file not found: {filename}")
    except Exception as e:
        print(f"Error loading Excel file: {e}")

    # Print the loaded project data (for debugging)
    print(f"Loaded project data: {projects.get(filename)}")

    # Function to open the browser
    def open_browser():
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://127.0.0.1:5000/')

    Timer(1, open_browser).start()
    app.run(debug=True)
