@echo off
echo Installing Python dependencies...
echo.
echo Attempting to install with requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Standard installation failed. Trying minimal requirements...
    pip install -r requirements-minimal.txt
    if errorlevel 1 (
        echo.
        echo Installation failed. Trying individual packages...
        pip install fastapi uvicorn[standard] python-multipart pydantic numpy librosa scikit-learn scipy python-jose[cryptography] passlib[bcrypt] python-dotenv aiofiles pydub
    )
)
echo.
echo Setup complete!
echo.
echo To start the backend server, run: start_backend.bat
echo To open the frontend, open frontend/index.html in your browser

