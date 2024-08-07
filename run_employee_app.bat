@echo off

REM Navigate to the project directory
cd /d %~dp0

REM Set up the virtual environment if it does not exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required packages
echo Installing dependencies...
pip install -r requirements.txt

REM Set environment variables
echo Setting environment variables...
set FLASK_APP=app.py
set FLASK_ENV=development

REM Create the database within application context
echo Creating database...
python db_create.py

REM Insert initial data within application context
echo Inserting initial data...
python insert_initial_data.py

REM Run the Flask application
echo Starting Flask application...
python -m flask run

REM Pause the script
pause
