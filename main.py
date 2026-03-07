from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from functools import lru_cache
from exa_py import Exa
import uuid
import os
import uvicorn

app = FastAPI()
exa = Exa("8da3779c-d967-449a-b5b3-1fb386e41604")

templates = Jinja2Templates(directory="templates")

@app.get("/background.jpeg")
def get_background():
    return FileResponse("background.jpeg", media_type="image/jpeg")

@app.get("/background_dark.jpeg")
def get_background_dark():
    return FileResponse("background_dark.jpeg", media_type="image/jpeg")

@app.get("/infoBG.jpeg")
def get_infoBG():
    return FileResponse("infoBG.jpeg", media_type="image/jpeg")

@app.get("/mic.png")
def get_mic():
    return FileResponse("mic.png", media_type="image/png")

@app.get("/mic_dark.png")
def get_mic_dark():
    return FileResponse("mic_dark.png", media_type="image/png")

@app.get("/speaking.png")
def get_speaking():
    return FileResponse("speaking.png", media_type="image/png")

@app.get("/speaking_dark.png")
def get_speaking_dark():
    return FileResponse("speaking_dark.png", media_type="image/png")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@lru_cache(maxsize=100)
def cacheSearch(query: str):
    return exa.search_and_contents(
        query,
        num_results = 5,
        type = "auto",
        summary = True,
    )

searchHistory = {}

@app.get("/results", response_class=HTMLResponse)
def result(q: str, request: Request):
    sessionID = request.query_params.get("sessionID", "")
    if not sessionID:
        sessionID = str(uuid.uuid4())

    if sessionID not in searchHistory:
        searchHistory[sessionID] = []

    format_results = []

    if q and q.strip():
        try:
            response = cacheSearch(q)

            for result in response.results: 
                published_date = result.published_date
                if published_date:
                    try:
                        dt = datetime.fromisoformat(published_date.replace("Z", "+00:00"))
                        formatted_date = f"{dt.month:02d}/{dt.day:02d}/{dt.year}"
                    except:
                        formatted_date = published_date[:10]
                else:
                    formatted_date = "N/A"

                title = "No title found"
                if result.title and len(result.title) < 50:
                    title = result.title
                elif result.title and len(result.title) >= 50:
                    title = result.title[:50]
                    if len(result.title) > 50:
                        title += "..."

                description = "No description found"
                if hasattr(result, "summary") and result.summary:
                    description = result.summary[:150]
                    if len(result.summary) > 150:
                        description += "..."
                elif hasattr(result, "text") and result.text:
                    description = result.text[:150]
                    if len(result.text) > 150:
                        description += "..."

                url = "N/A"
                if result.url and len(result.url) < 100:
                    url = result.url
                elif result.url and len(result.url) >= 100:
                    url = result.url[:100]
                    if len(result.url) > 100:
                        url += "..."

                format_results.append({
                    "title": title,
                    "published_date": formatted_date,
                    "description": description,
                    "url": url,
                })

            searchEntry = {
                "query": q,
                "results": format_results
            }
            if not searchHistory[sessionID] or searchHistory[sessionID][-1]["query"] != q:
                searchHistory[sessionID].append(searchEntry)
            if len(searchHistory[sessionID]) > 10:
                searchHistory[sessionID].pop(0)

        except Exception as e:
            errorEntry = {
                "query": q,
                "results": [{
                    "title": "N/A",
                    "published_date": "N/A",
                    "description": "N/A",
                    "url": "N/A"
                }],
                "error": True
            }
            searchHistory[sessionID].append(errorEntry)

    allSearches = searchHistory[sessionID]

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "q": q,
            "sessionID": sessionID,
            "allSearches": allSearches,
            "hasSearches": bool(allSearches)
        }
    )

@app.post("/clearSearch/{sessionID}")
def clearSession(sessionID: str):
    if sessionID in searchHistory:
        searchHistory[sessionID] = []
    return {"status": "cleared"}

@app.get("/api/cacheInfo")
def cacheInfo():
    cacheInfo = cacheSearch.cache_info()
    return {
        "cache_hits": cacheInfo.hits,
        "cache_misses": cacheInfo.misses,
        "cache_size": cacheInfo.currsize,
        "cache_maxsize": cacheInfo.maxsize,
        "total_sessions": len(searchHistory),
        "total_searches": sum(len(searches) for searches in searchHistory.values())
    }

@app.get("/api/search")
def search(query: str):
    response = exa.search_and_contents(
        query,
        num_results = 5,
        type = "auto",
    )

    format_results = []
    for result in response.results:
        format_results.append({
            "title": result.title or "No title",
            "published_date": result.published_date,
            "url": result.url,
        })

    return {
        "query": query,
        "results": format_results,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)