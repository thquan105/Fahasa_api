import os
import sys
# add the directory containing the db module to the Python path
crawl_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(crawl_path)
from crawl.db_crawl import get_data
from db.db_actions import *
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
LOCALHOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')


# Docker
TEMPLATES = os.getenv('TEMPLATESDOCKER')

# TEMPLATES = os.getenv('TEMPLATES')

app = FastAPI()

app.mount("/static", StaticFiles(directory=f"{TEMPLATES}/static"), name="static")
templates = Jinja2Templates(directory=TEMPLATES)


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/title", response_class=HTMLResponse)
async def read_title(request: Request):
    return templates.TemplateResponse("title.html")

@app.post("/title", response_class=HTMLResponse)
async def do_search(request: Request, title: str = Form(...)):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        # create a cursor object
        cursor = conn.cursor()

        # define the search query
        query = f"SELECT * FROM product WHERE product_name LIKE '%{title}%'"

        # execute the query
        cursor.execute(query)

        # get the results
        results = cursor.fetchall()

        # extract the titles from the results
        titles = [result for result in results]

        # close the database connection
        cursor.close()
        conn.close()
        return templates.TemplateResponse("title.html", {'request': request, "results": titles})

    except Exception as e:
        print(e)
        return templates.TemplateResponse("title.html", {'request': request, "results": []})

@app.get("/suggest")
async def suggest(title: str):
    try:
        print(title)
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        # create a cursor object
        cursor = conn.cursor()

        # define the search query
        query = f"SELECT * FROM product WHERE product_name LIKE '%{title}%'"

        # execute the query
        cursor.execute(query)

        # get the results
        results = cursor.fetchall()

        # extract the titles from the results
        titles = [result[1] for result in results]

        cursor.close()
        conn.close()

        return {"suggestions": titles}
    except Exception as e:
        print(e)
        return {"suggestions": []}

@app.get('/search_product_name/')
def search_product(title):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        # create a cursor object
        cursor = conn.cursor()
        query = "SELECT * FROM product WHERE product_name LIKE '%" + title + "%'"
        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to dictionary
        rows = cursor.fetchall()

        dict_rows = []
        for row in rows:
            dict_row = {}
            for i, column in enumerate(columns):
                dict_row[column] = row[i]
            dict_rows.append(dict_row)
    except:
        return {'status': 400, 'message': 'Lỗi'}

    return dict_rows

@app.post('/add')
def add(product_id: int, product_name: str, product_price: str, product_finalprice: str, product_url: str, image_src: str, discount: int):
    data = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'product_finalprice': product_finalprice,
        'product_url': product_url,
        'image_src': image_src,
        'discount': discount
    }
    val = insert_data(data)
    if val:
        return {'status': 200, 'message': 'Thêm Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}

@app.put('/products/{product_id}')
def edit(product_id: int, product_name: str, product_price: str, product_finalprice: str, product_url: str, image_src: str, discount: int):
    data = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'product_finalprice': product_finalprice,
        'product_url': product_url,
        'image_src': image_src,
        'discount': discount
    }

    if edit_product(product_id, data):
        return {'status': 200, 'message': 'Sửa Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}

@app.delete('/products/{product_id}')
def remove(product_id: int):
    if remove_product(product_id):
        return {'status': 200, 'message': 'Xóa Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}


@app.get('/crawl')
def crawl():
    try:
        get_data()
    except: 
        return {"status": "Lỗi !!!"}
    return {"status": "Hoàn thành !!!"}


if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run(app, port=8000, reload=True)
    pass