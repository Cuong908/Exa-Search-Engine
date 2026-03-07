from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from functools import lru_cache
from exa_py import Exa
import uuid
from dotenv import load_dotenv
import os
import uvicorn

app = FastAPI()

load_dotenv()
api_key = os.environ.get("EXA_API_KEY")
exa = Exa(api_key=api_key)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# LRU cache to avoid redundant Exa API calls for repeated queries
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
                # Format the returned ISO 8601 dates into MM/DD/YYYY for readability
                published_date = result.published_date
                if published_date:
                    try:
                        dt = datetime.fromisoformat(published_date.replace("Z", "+00:00"))
                        formatted_date = f"{dt.month:02d}/{dt.day:02d}/{dt.year}"
                    except (ValueError, AttributeError):
                        formatted_date = published_date[:10]
                else:
                    formatted_date = "N/A"

                # Shorten title, description, and url if too long to prevent overflow
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
            # Cap history at 10 entries per session to limit memory usage
            if len(searchHistory[sessionID]) > 10:
                searchHistory[sessionID].pop(0)

        except Exception as e:
            print(f"Search error for query '{q}': {e}")
            errorEntry = {
                "query": q,
                "results": [{
                    "title": "Search Failed",
                    "published_date": "N/A",
                    "description": "An error has occured. Please try again!",
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
    try:
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
    except Exception as e:
        return {"error": "Search failed", "Details": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)