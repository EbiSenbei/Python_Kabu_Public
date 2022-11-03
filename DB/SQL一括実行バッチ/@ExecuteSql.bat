ECHO test >>log.txt
type %5 >> ".\UpdateLog.txt"
sqlcmd -S %1 -d %2 -U %3 -P %4 -i %5 -o ".\UpdateResultWork.txt"
type UpdateResultWork.txt >> ".\UpdateLog.txt"