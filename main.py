from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI(title="AwaisTraders")
templates = Jinja2Templates(directory="templates")

# Data Storage
CUSTOMERS = {}  
COMPLAINTS = [] 
ADMIN_MASTER_PASS = "admin123"
CAPTCHA_STORE = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    CAPTCHA_STORE['ans'] = num1 + num2
    return templates.TemplateResponse("login.html", {"request": request, "error": None, "captcha": f"{num1} + {num2} = ?"})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...), captcha: str = Form(...)):
    try:
        user_captcha = int(captcha)
    except ValueError:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Captcha mein sirf number likhein!", "captcha": "Error"})

    if user_captcha != CAPTCHA_STORE.get('ans'):
        num1, num2 = random.randint(1, 9), random.randint(1, 9)
        CAPTCHA_STORE['ans'] = num1 + num2
        return templates.TemplateResponse("login.html", {"request": request, "error": "Ghalat Captcha!", "captcha": f"{num1} + {num2} = ?"})

    if email == "admin" and password == ADMIN_MASTER_PASS:
        return templates.TemplateResponse("admin.html", {"request": request, "complaints": COMPLAINTS, "customers": CUSTOMERS})
    elif email in CUSTOMERS and CUSTOMERS[email]["password"] == password:
        return templates.TemplateResponse("complaint.html", {"request": request, "email": email, "cust_id": CUSTOMERS[email]["cust_id"], "phone": CUSTOMERS[email]["phone"], "address": CUSTOMERS[email]["address"], "success": None})
    else:
        num1, num2 = random.randint(1, 9), random.randint(1, 9)
        CAPTCHA_STORE['ans'] = num1 + num2
        return templates.TemplateResponse("login.html", {"request": request, "error": "Ghalat Email ya Password!", "captcha": f"{num1} + {num2} = ?"})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, email: str = Form(...), password: str = Form(...), cust_id: str = Form(...), phone: str = Form(...), address: str = Form(...), captcha: str = Form(...)):
    try:
        user_captcha = int(captcha)
    except ValueError:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Captcha error!", "captcha": "Refresh page"})

    if user_captcha != CAPTCHA_STORE.get('ans'):
        num1, num2 = random.randint(1, 9), random.randint(1, 9)
        CAPTCHA_STORE['ans'] = num1 + num2
        return templates.TemplateResponse("login.html", {"request": request, "error": "Ghalat Captcha!", "captcha": f"{num1} + {num2} = ?"})

    if email in CUSTOMERS:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Yeh email pehle se registered hai!", "captcha": "Refresh"})
    
    CUSTOMERS[email] = {"password": password, "cust_id": cust_id, "phone": phone, "address": address}
    return templates.TemplateResponse("login.html", {"request": request, "error": "Account ban gaya! Login karein.", "captcha": "Refresh"})

@app.post("/submit-complaint", response_class=HTMLResponse)
async def submit_complaint(request: Request, email: str = Form(...), cust_id: str = Form(...), phone: str = Form(...), address: str = Form(...), complaint_text: str = Form(...)):
    COMPLAINTS.append({"email": email, "cust_id": cust_id, "phone": phone, "address": address, "complaint": complaint_text, "status": "Pending"})
    return templates.TemplateResponse("complaint.html", {"request": request, "email": email, "cust_id": cust_id, "phone": phone, "address": address, "success": "Complaint darj ho gayi!"})