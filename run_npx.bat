@echo off
set DEST=%LOCALAPPDATA%\Node
if not exist "%DEST%" mkdir "%DEST%"
if not exist "%DEST%\node-v20.15.0-win-x64\npx.cmd" (
    echo Downloading Node.js...
    curl -sL -o "%TEMP%\node.zip" "https://nodejs.org/dist/v20.15.0/node-v20.15.0-win-x64.zip"
    echo Extracting Node.js please wait...
    tar -xf "%TEMP%\node.zip" -C "%DEST%"
)
set PATH=%PATH%;%DEST%\node-v20.15.0-win-x64
echo Running npx antigravity-awesome-skills...
call npx antigravity-awesome-skills
