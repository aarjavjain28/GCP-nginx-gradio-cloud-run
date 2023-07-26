import importlib
from fastapi import FastAPI, Request, HTTPException, Cookie, Response
import httpx
from fastapi.templating import Jinja2Templates
import os
from fastapi import FastAPI
import gradio as gr

from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def format_string(s):
    return s.replace('-', ' ').replace('_', ' ').title()
templates = Jinja2Templates(directory="app/templates")
templates.env.globals['format_string'] = format_string  # add the function to the global template environment


def load_and_run_gradio_blocks(path, app ):
    files = [f[:-3] for f in os.listdir(path) if f.endswith('.py')]
    valid_pages = []

    for file in files:
        module_name = f"models.{file}"
        module = importlib.import_module(module_name)
        block = module.gradio_block()  # Execute the function immediately after it's imported
        app = gr.mount_gradio_app(app,block,path="/" + file)
        valid_pages.append(file)
    return app , valid_pages
app, valid_pages = load_and_run_gradio_blocks('app/models', app)


@app.get("/{path}-page", response_class=HTMLResponse)
async def text_flip_page(request: Request, path: str):
    if path not in valid_pages:
        return HTMLResponse(status_code=404, content="<h1>Page not found</h1>") # or any other way of handling invalid URLs
    return templates.TemplateResponse("model_page_template.html", {"request": request, "model_path": path})

@app.get("/")
def read_main(request: Request):
    return templates.TemplateResponse("main_template.html", {"request": request, "pages": valid_pages })

@app.get("/logout")
def logout(response: Response, vouch_cookie: str = Cookie(None)):
    if vouch_cookie is None:
        return {"message": "You're already logged out"}
    # Invalidate the VouchCookie
    response.delete_cookie(key="VouchCookie", domain="my-service-3blf5p4gxa-nw.a.run.app")
    return {"message": "Logged out successfully"}