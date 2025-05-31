# PyAlleyWeb
Web interface for matching PyAlley bots against the sample bot

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```
   ```
   cd PyAlleyWeb
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`.

   ```bash
   python3 -m venv .venv
   ```
   ```
   source .venv/bin/activate
   ```

   ```bash
   pip install -r spyalley-fastapi-app/requirements.txt
   ```

4. **Run the application**:
   Use Uvicorn to run the FastAPI application:
   ```bash
   cd spyalley-fastapi-app
   ```
   ```
   uvicorn app.main:app --reload
   ```

5. **Access the application**:
   Submit bot for a local matchup:  
   ```bash
   curl -X POST -F "file=@/home/<DIR>/PyAlleyWeb/Sample/Y00_Bot.py" http://127.0.0.1:8000/upload/
   ```
