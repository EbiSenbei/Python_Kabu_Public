@echo off
rem �X�N���v�g�̎��s�iSQLCMD�j���s���B�i�X�N���v�g��\Script�Ɋi�[���邱�Ɓj
rem SERVERNAME�ADBNAME�ADBUSER�ADBPASSWORD�͉��LSET�R�}���h�̓��e�����ɍ��킹�ď���������B
rem SERVERNAME�ADBNAME�͎��s���ɂ킽�������ŏ㏑���\�B

echo "�A�b�v�f�[�g���s��"
if exist ".\ExecuteSql.bat" goto okcd
echo �J�����g�f�B���N�g�����s���ł��B
echo �A�b�v�f�[�g���s����TENSUITEUpdate.bat�̂���t�H���_��
echo �J�����g�f�B���N�g���Ƃ��邩�A
echo ExecuteSql.bat���_�u���N���b�N���Œ��ڎ��s���ĉ������B
goto end
:okcd
set SERVERNAME="EBI-PC"
set DBNAME="TGP_KABU"
set DBUSER="sa"
set DBPASSWORD="password"

rem ��P�����������DB�T�[�o���Ƃ��Đݒ肷��B
if ""%1""=="""" goto doneSetServerName
set SERVERNAME=%1
:doneSetServerName
rem ��Q�����������DB���Ƃ��Đݒ肷��B
if ""%2""=="""" goto doneSetDBName
set DBNAME=%2
:doneSetDBName

if exist ".\UpdateLog.txt" del ".\UpdateLog.txt"
echo #�T�[�o��: %SERVERNAME% >> ".\UpdateLog.txt"
echo #�f�[�^�x�[�X��: %DBNAME% >> ".\UpdateLog.txt"

:executeScript
echo #�X�N���v�g�����s���܂��B >> ".\UpdateLog.txt"
FOR %%i IN (".\Script\*.sql") DO (
    type %%i >> ".\UpdateLog.txt"
    echo %%i
    sqlcmd -S %SERVERNAME% -d %DBNAME% -U %DBUSER% -P %DBPASSWORD% -i %%i -o ".\UpdateResultWork.txt"
    type UpdateResultWork.txt >> ".\UpdateLog.txt"
)
if errorlevel 1 echo �X�N���v�g���s���G���[(.sql)�iSQLCMD�R�}���h�����s�ł��Ȃ��\��������܂��B�j >> ".\UpdateLog.txt"


REM if exist ".\UpdateResultWork.txt" del ".\UpdateResultWork.txt"

:end
echo "�A�b�v�f�[�g�I��"
pause
