from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader
import os
import github_kusa

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.method == 'HEAD':
        return Response()
    elif 'herokuapp' in urlparse(str(request.url)).netloc:
        domain = os.getenv('DOMAIN', 'example.com')
        url = urlparse(str(request.url))._replace(netloc=domain).geturl()
        response = RedirectResponse(url)
    else:
        response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__), encoding='utf8'))
    html = env.get_template('index.html').render()
    return HTMLResponse(content=html, status_code=200)


@app.get("/github-kusa")
async def read_github_kusa(user: str = ''):
    return HTMLResponse(content=github_kusa.main(user), status_code=200)
