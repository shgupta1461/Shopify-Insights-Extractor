from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.repo import save_brand_insight, init_db
from app.services.extractor import extract_brand_context
from app.scraper.shopify import scrape_shopify_data

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
def on_startup():
    init_db()

class ExtractRequest(BaseModel):
    website_url: str

@app.post("/api/extract")
async def api_extract(req: ExtractRequest):
    try:
        data = scrape_shopify_data(req.website_url)
        if "error" in data:
            if data["error"].startswith("404"):
                raise HTTPException(status_code=401, detail="401 Website not found")
            raise HTTPException(status_code=500, detail="500 Internal Server Error")
        save_brand_insight(req.website_url, data)
        return JSONResponse(content=data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scrape")
async def scrape_endpoint():
    data = scrape_shopify_data()
    return {"scraped_data": data}
