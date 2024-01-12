import requests
from fastapi import FastAPI, File, Response, Body, Request, Depends
from fastapi.responses import FileResponse
import uvicorn
import os
import re
import ast
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/alicloud")
async def alibaba(request: Request):
    date = list(request.query_params.values())
    input_date = ''.join(date[0])
    print(input_date)
    cleaned_date = input_date.strip("[]")
    result_date = ast.literal_eval(input_date)
    print(result_date)
    print(os.environ.get('ACCESS_KEY'))
    response = requests.post(
        "https://binaryowl-dev.materia-logic.com/api/alicloud/reseller-bill-chatbot",
        json={"billing_cycle_list": result_date, "access_key": os.environ.get('ACCESS_KEY')},
        # params=date,
    )
    print(response.json())
    data = response.json()['data']
    all_data = []
    for item in data:
        response_data = {}
        response_data['originalCost'] = item['originalCost']
        response_data['discount'] = item['discount']
        response_data['couponDeduct'] = item['couponDeduct']
        response_data['pretaxAmount'] = item['pretaxAmount']
        all_data.append(response_data)

    
    return all_data

@app.get("/breakdown")
async def alibaba_breakdown(request: Request):
    date = list(request.query_params.values())
    input_date = ''.join(date[0])
    result_date = ast.literal_eval(input_date)
    response = requests.post(
        "https://binaryowl-dev.materia-logic.com/api/alicloud/reseller-bill-chatbot",
        json={"billing_cycle_list": result_date, "access_key": os.environ.get('ACCESS_KEY') },
    )
    data = response.json()['data'][0]['item']
    all_data = []
    for item in data:
        all_data.append({'product name': item['productName'], 'cost': item['amount']})
    return all_data
@app.get("/.well-known/ai-plugin.json")
async def plugin():
    return FileResponse(os.path.join('.', 'ai-plugin.json'), media_type='application/json')

@app.get("/openapi.yaml")
async def serve_openapi_yaml():
    return FileResponse(os.path.join('.', 'openapi.yaml'), media_type='text/yaml')

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=5000)