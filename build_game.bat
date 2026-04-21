@echo off
echo Установка необходимых библиотек...
pip install pygame pyinstaller

echo.
echo Запуск сборки исполняемого файла (EXE)...
pyinstaller --onefile --windowed --name "ETVP_Field_Simulator" game_core.py

echo.
echo Сборка завершена!
echo Исполняемый файл находится в папке "dist".
pause@echo off
echo Установка необходимых библиотек...
pip install pygame pyinstaller

echo.
echo Запуск сборки исполняемого файла (EXE)...
pyinstaller --onefile --windowed --name "ETVP_Field_Simulator" game_core.py

echo.
echo Сборка завершена!
echo Исполняемый файл находится в папке "dist".
pause
