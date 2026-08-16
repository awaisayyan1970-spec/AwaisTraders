from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email == "admin@awsaistraders.com" and password == "admin123":
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid login"})

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "complaints": []})

@app.get("/complaint", response_class=HTMLResponse)
async def complaint_page(request: Request):
    return templates.TemplateResponse("complaint.html", {"request": request})
