# SpyAlley FastAPI Application

This project is a FastAPI application that allows users to upload a Python class extending the `ComputerPlayer` class from the `Test_Batch/ComputerPlayer.py` file. The uploaded class is then matched against the `Z00_Bot` class defined in `Test_Batch/SpyAlley.py`. The results of the match are displayed on a web page.

## Project Structure

```
spyalley-fastapi-app
├── app
│   ├── main.py                # Entry point of the FastAPI application
│   ├── api
│   │   └── endpoints.py       # API endpoints for file uploads
│   ├── core
│   │   └── match.py           # Logic for matching uploaded classes
│   ├── templates
│   │   └── results.html       # HTML template for displaying results
│   └── Test_Batch
│       ├── ComputerPlayer.py   # Base class for computer players
│       └── SpyAlley.py        # Game logic and Z00_Bot class
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd spyalley-fastapi-app
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Use Uvicorn to run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000`. You can upload your Python class through the provided interface.

## Usage

- Upload a Python file that contains a class extending `ComputerPlayer`.
- The application will process the uploaded class and match it against the `Z00_Bot` class.
- The results will be displayed on a new page, indicating whether the uploaded class won or lost.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.