from pydantic import BaseModel


class ProcOpdBase(BaseModel):
    hoscode: str
    start_date: str
    end_date: str


class ProcIpdBase(BaseModel):
    hoscode: str
    start_date: str
    end_date: str

