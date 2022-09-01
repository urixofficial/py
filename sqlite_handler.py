import sqlite3

def sqlExec(dbPath, sqlString, rw=False):

	con = sqlite3.connect(dbPath)
	cur = con.cursor()
	cur.execute(sqlString)

	if rw: con.commit()
	else: sqlAnswer = cur.fetchall()

	con.close()

	return sqlAnswer

def sqlExecMany(dbPath, sqlString, values, rw=False):

	con = sqlite3.connect(dbPath)
	cur = con.cursor()
	cur.executemany(sqlString, values)

	if rw: con.commit()
	else: sqlAnswer = cur.fetchall()

	con.close()

	return sqlAnswer

def getTableInfo(dbPath, tableName):

	sqlString = f'SELECT * FROM pragma_table_info("{tableName}")'

	return sqlExec(dbPath, sqlString)
