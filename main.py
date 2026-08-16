import random
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Templates folder link karna
templates = Jinja2Templates(directory="templates")

# Temporary in-memory database for demo
WORKERS_DB = ["Worker 1", "Worker 2", "Worker 3"]
COMPLAINTS_DB = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    # Naya aur theek syntax TemplateResponse ke liye
    return templates.TemplateResponse(
        request, 
        "login.html", 
        {"error": None, "captcha": f"{num1} + {num2}"}
    )

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Basic login check for admin/worker
    if email == "admin@awsaistraders.com" and password == "admin123":
        return RedirectResponse(url="/admin", status_code=303)
    
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return templates.TemplateResponse(
        request, 
        "login.html", 
        {"error": "Ghalat Email ya Password!", "captcha": f"{num1} + {num2}"}
    )

@app.get("/complaint", response_class=HTMLResponse)
def complaint_page(request: Request):
    return templates.TemplateResponse(request, "complaint.html", {"success": False})

@app.post("/complaint", response_class=HTMLResponse)
def submit_complaint(
    request: Request, 
    name: str = Form(...), 
    phone: str = Form(...), 
    address: str = Form(...), 
    issue: str = Form(...)
):
    complaint_data = {
        "name": name,
        "phone": phone,
        "address": address,
        "issue": issue,
        "status": "Pending",
        "assigned_to": "Not Assigned"
    }
    COMPLAINTS_DB.append(complaint_data)
    return templates.TemplateResponse(request, "complaint.html", {"success": True})

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        request, 
        "admin.html", 
        {"complaints": COMPLAINTS_DB, "workers": WORKERS_DB}
    )
    
