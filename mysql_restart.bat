@echo off
echo Restarting MySQL Server...
net stop MySQL80
net start MySQL80
echo MySQL Server has been restarted.
