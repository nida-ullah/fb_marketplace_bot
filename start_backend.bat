@echo off
echo ================================================
echo   Facebook Marketplace Bot - Backend Setup
echo ================================================
echo.

echo [1/3] Installing required packages...
pip install djangorestframework djangorestframework-simplejwt django-cors-headers

echo.
echo [2/3] Running migrations...
python manage.py migrate

echo.
echo [3/3] Starting Django server...
echo.
echo Backend will run on: http://localhost:8000
echo API endpoints available at: http://localhost:8000/api/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
