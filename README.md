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
   The output should be as below:

<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Match Results</title>  
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/4.5.2/css/bootstrap.min.css">  
</head>  
<body>  
    <div class="container mt-5">  
        <h1 class="text-center">Match Results</h1>  
        <div class="card mt-4">  
            <div class="card-body">  
                <h5 class="card-title">Uploaded Class: Y00_Bot</h5>  
                <h5 class="card-title">Incumbent Class: Z00_Bot</h5>  
                <p class="card-text">Comparison result between Y00_Bot and Z00_Bot</p>  
                <h5 class="card-title">Outcome:</h5>  
                <p class="card-text">  
Z00_Bot #2 : 161 wins  
Y00_Bot #1 : 186 wins  
Y00_Bot #3 : 169 wins  
Z00_Bot #3 : 169 wins  
Y00_Bot #2 : 175 wins  
Z00_Bot #1 : 140 wins  
</p>  
            </div>  
        </div>  
    </div>  
</body>  
</html>  
