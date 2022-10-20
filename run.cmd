@ECHO OFF

START /D sd-webui webui.bat
START ngrok.exe http 7860
