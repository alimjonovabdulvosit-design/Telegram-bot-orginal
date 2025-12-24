@echo off
title Telegram Bot Runner
:start
echo Bot ishga tushmoqda...
python main.py
echo.
echo Bot jarayoni to'xtadi. 5 soniyadan keyin qayta ishga tushadi...
timeout /t 5
goto start
