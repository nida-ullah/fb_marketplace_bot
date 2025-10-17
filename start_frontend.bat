@echo off
echo ================================================
echo   Facebook Marketplace Bot - Frontend Setup
echo ================================================
echo.

cd frontend

echo [1/2] Installing dependencies (if needed)...
if not exist "node_modules" (
    npm install
)

echo.
echo [2/2] Starting Next.js development server...
echo.
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev
