import sqlite3


def sqlExec(dbPath: str, sqlRequest: str, rw: bool = False) -> list:
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute(sqlRequest)

    if rw:
        con.commit()
        sqlAnswer = None
    else:
        sqlAnswer = cur.fetchall()

    con.close()

    return sqlAnswer


def sqlExecMany(dbPath: str, sqlString: str, values, rw: bool =False) -> list:
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.executemany(sqlString, values)

    if rw:
        con.commit()
        sqlAnswer = None
    else:
        sqlAnswer = cur.fetchall()

    con.close()

    return sqlAnswer


def getTableInfo(dbPath: str, tableName: str) -> list:
    sqlString = f'SELECT * FROM pragma_table_info("{tableName}")'

    return sqlExec(dbPath, sqlString)
