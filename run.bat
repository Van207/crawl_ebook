@echo off
start "download_file_desc" cmd /c "mode con:cols=60 lines=10 & py z.py"
start "download_file" cmd /c "mode con:cols=60 lines=10 & py download_file.py"
