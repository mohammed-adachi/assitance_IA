from fastapi import FastAPI, HTTPException,Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# ollmam settings
ollama_url = "http://localhost:11434/api/generate"
ollama_model = "mistral"
@app.get("/")
def serverHome_page():
    return FileResponse("static/index.html")

@app.post("/ollama")
def ollama_generate(prompt: str = Query(..., description="The prompt to generate text from")):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.post(
            ollama_url,
            headers=headers,
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        return {"response": data.get("text", "")}
    except requests.exceptions.RequestException as e:
#        raise HTTPException(status_code=500, detail=str(e))
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON response from Ollama API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
