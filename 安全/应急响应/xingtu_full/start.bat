@echo off
cd %~dp0
echo ****************************************************
echo. 
echo 360��ͼ-Web��־��������
echo Copyright@2014 360��վ��ʿ [http://wangzhan.360.cn]
echo ����QQȺ��12803537
echo.
echo ****************************************************
start "" "%cd%/bin/xingtu.exe"
ping 1.1.1.1 -n 1 -w 1000 > nul
tail -f logs/output.log
pause

