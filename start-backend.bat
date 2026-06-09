@echo off
cd /d "%~dp0backend"
echo Fish-Point backend baslatiliyor (0.0.0.0:8000)...
py -3 manage.py runserver 0.0.0.0:8000
