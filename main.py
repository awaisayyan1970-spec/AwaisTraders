from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Templates folder setup
templates = Jinja2Templates(directory="templates")

# Temporary in-memory databases for demo
WORKERS_DB = ["Worker 1", "Worker 2", "Worker 3"]
COMPLAINTS_DB = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"error": None}
    )

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Basic admin check
    if email == "admin@awsaistraders.com" and password == "admin123":
        return RedirectResponse(url="/admin", status_code=303)
    
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"error": "Ghalat Email ya Password!"}
    )

@app.get("/complaint", response_class=HTMLResponse)
def complaint_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="complaint.html", 
        context={"success": False}
    )

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
    return templates.TemplateResponse(
        request=request, 
        name="complaint.html", 
        context={"success": True}
    )

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="admin.html", 
        context={"complaints": COMPLAINTS_DB, "workers": WORKERS_DB}
    )

