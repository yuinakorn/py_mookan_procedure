import pymysql.cursors
from fastapi import HTTPException
from dotenv import dotenv_values

config_env = dotenv_values(".env")


def get_procedure_ipd(request, token):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized, Please input token")
    elif token != config_env["TOKEN"]:
        raise HTTPException(status_code=401, detail="Unauthorized, Token incorrect")
    else:
        pass
    hoscode = request.hoscode
    start_date = request.start_date
    end_date = request.end_date

    try:
        connection = pymysql.connect(host=config_env["DB_HOST"],
                                     user=config_env["DB_USER"],
                                     password=config_env["DB_PASSWORD"],
                                     db=config_env["DB_NAME"],
                                     charset=config_env["DB_CHARSET"],
                                     port=int(config_env["DB_PORT"]),
                                     cursorclass=pymysql.cursors.DictCursor
                                     )
        with connection.cursor() as cursor:
            sql = f"SELECT COUNT(*) FROM `mookan_procedure_ipd` WHERE `HOSPCODE` = %s AND left(DATETIME_ADMIT,10) BETWEEN %s AND %s"
            cursor.execute(sql, (hoscode, start_date, end_date))
            result = cursor.fetchone()
            count = result["COUNT(*)"]
            if count == 0:
                raise HTTPException(status_code=404, detail="Data not found")
            else:
                pass
    except Exception as e:
        print(e)
        raise e

    try:
        with connection.cursor() as cursor:
            sql = f"SELECT i.HOSPCODE,i.hn,i.AN,left(i.DATETIME_ADMIT,10) DATE_SERV,i.WARDSTAY,c.clinicdesc, " \
                  "i.PROCEDCODE,i.nhso_adp_code,i.SERVICEPRICE " \
                  "FROM mookan_procedure_ipd i " \
                  "LEFT JOIN cclinic c ON i.WARDSTAY = c.cliniccode " \
                  "WHERE i.HOSPCODE = %s AND left(i.DATETIME_ADMIT,10) BETWEEN %s AND %s"
            cursor.execute(sql, (hoscode, start_date, end_date))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)
        raise e
