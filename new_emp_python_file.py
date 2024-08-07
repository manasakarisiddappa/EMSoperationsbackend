import subprocess
import os

def create_virtualenv():
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.run(["python", "-m", "venv", "venv"], check=True)

def install_dependencies():
    print("Installing dependencies...")
    subprocess.run(["venv\\Scripts\\python.exe", "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def set_environment_variables():
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'

def create_database():
    print("Creating database...")
    subprocess.run(["venv\\Scripts\\python.exe", "db_create.py"], check=True)

def insert_initial_data():
    print("Inserting initial data...")
    subprocess.run(["venv\\Scripts\\python.exe", "insert_initial_data.py"], check=True)

def run_flask_app():
    print("Starting Flask application...")
    subprocess.run(["venv\\Scripts\\python.exe", "-m", "flask", "run"], check=True)

if __name__ == '__main__':
    create_virtualenv()
    install_dependencies()
    set_environment_variables()
    create_database()
    insert_initial_data()
    run_flask_app()
