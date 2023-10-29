# import FastAPI
from typing import Optional

from fastapi import FastAPI, Header
# import uvicorn
import uvicorn
import pydantic
from controllers.proc_opd_controller import get_procedure_opd
from controllers.proc_ipd_controller import get_procedure_ipd
import pymysql.cursors
from dotenv import dotenv_values
from models.procedure_model import ProcOpdBase, ProcIpdBase

config_env = dotenv_values(".env")

# Create FastAPI instance
app = FastAPI(docs_url="/apidocs")

connection = pymysql.connect(host=config_env["DB_HOST"],
                             user=config_env["DB_USER"],
                             password=config_env["DB_PASSWORD"],
                             db=config_env["DB_NAME"],
                             charset=config_env["DB_CHARSET"],
                             port=int(config_env["DB_PORT"]),
                             cursorclass=pymysql.cursors.DictCursor
                             )


@app.get("/")
def read_root():
    return {"message": "API ของ อ.กรรณ"}


@app.post("/procedure_opd")
def read_procedure_opd(request: ProcOpdBase, token: str = Header(None, convert_underscores=True)):
    return get_procedure_opd(request, connection, token)


@app.post("/procedure_ipd")
def read_procedure_ipd(request: ProcIpdBase, token: str = Header(None, convert_underscores=True)):
    return get_procedure_ipd(request, connection, token)

