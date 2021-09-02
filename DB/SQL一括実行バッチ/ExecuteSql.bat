@echo off
rem スクリプトの実行（SQLCMD）を行う。（スクリプトは\Scriptに格納すること）
rem SERVERNAME、DBNAME、DBUSER、DBPASSWORDは下記SETコマンドの内容を環境に合わせて書きかえる。
rem SERVERNAME、DBNAMEは実行時にわたす引数で上書き可能。

echo "アップデート実行中"
if exist ".\ExecuteSql.bat" goto okcd
echo カレントディレクトリが不正です。
echo アップデート実行時はTENSUITEUpdate.batのあるフォルダを
echo カレントディレクトリとするか、
echo ExecuteSql.batをダブルクリック等で直接実行して下さい。
goto end
:okcd
set SERVERNAME="EBI-PC"
set DBNAME="TGP_KABU"
set DBUSER="sa"
set DBPASSWORD="password"

rem 第１引数があればDBサーバ名として設定する。
if ""%1""=="""" goto doneSetServerName
set SERVERNAME=%1
:doneSetServerName
rem 第２引数があればDB名として設定する。
if ""%2""=="""" goto doneSetDBName
set DBNAME=%2
:doneSetDBName

if exist ".\UpdateLog.txt" del ".\UpdateLog.txt"
echo #サーバ名: %SERVERNAME% >> ".\UpdateLog.txt"
echo #データベース名: %DBNAME% >> ".\UpdateLog.txt"

:executeScript
echo #スクリプトを実行します。 >> ".\UpdateLog.txt"
FOR %%i IN (".\Script\*.sql") DO (
    type %%i >> ".\UpdateLog.txt"
    echo %%i
    sqlcmd -S %SERVERNAME% -d %DBNAME% -U %DBUSER% -P %DBPASSWORD% -i %%i -o ".\UpdateResultWork.txt"
    type UpdateResultWork.txt >> ".\UpdateLog.txt"
)
if errorlevel 1 echo スクリプト実行時エラー(.sql)（SQLCMDコマンドが実行できない可能性があります。） >> ".\UpdateLog.txt"


REM if exist ".\UpdateResultWork.txt" del ".\UpdateResultWork.txt"

:end
echo "アップデート終了"
pause
