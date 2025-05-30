from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import importlib.util
import sys

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.post("/upload/")
async def upload_class(file: UploadFile = File(...)):
    file_location = f"app/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Dynamically load the uploaded class
    spec = importlib.util.spec_from_file_location("UploadedClass", file_location)
    uploaded_class_module = importlib.util.module_from_spec(spec)
    sys.modules["UploadedClass"] = uploaded_class_module
    spec.loader.exec_module(uploaded_class_module)
 
    # Assuming the uploaded class extends ComputerPlayer
    uploaded_class_name = file.filename.split(".")[0]
    uploaded_class = getattr(uploaded_class_module, uploaded_class_name, None)
    if uploaded_class is None:
        return {"error": "Uploaded class does not contain '" + uploaded_class_name + "'."}

    from app.Test_Batch.Z00_Bot import Z00_Bot
    from app.Test_Batch.SpyAlley import SpyAlleyGame

    # Here you would implement the logic to compare the uploaded class with Z00_Bot
    # For demonstration, let's assume we have a simple comparison function
    result = compare_classes(uploaded_class, uploaded_class_name, "Z00_Bot")

    batch=1
    g=SpyAlleyGame(batch)

    outcome = g.botMatchup(uploaded_class, uploaded_class_name)

    return templates.TemplateResponse("results.html", {"request": {}, "uploaded_class_name": uploaded_class_name, "result_message": result, "outcome": outcome})

def compare_classes(uploaded_class, uploaded_class_name, incumbent_class_name):
    # Placeholder for actual comparison logic
    # This should contain the logic to determine the outcome of the match
    return "Comparison result between " + uploaded_class(uploaded_class_name, "French").getName() + " and " + incumbent_class_name  # Replace with actual logic

@app.get("/")
async def main():
    return {"message": "Welcome to the Spy Alley FastAPI application!"}