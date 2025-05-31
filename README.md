# PyAlleyWeb
Web interface for matching PyAlley bots against the sample bot

Run locally:  

pip install -r requirements.txt
uvicorn app.main:app --reload

Submit bot for a local matchup:

curl -X POST -F "file=@/home/<PATH>/Y00_Bot.py" http://127.0.0.1:8000/upload/
