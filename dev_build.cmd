	if exist ".\Logs\*" (
        del /q ".\Logs\*"
    )
python Builder.py build

