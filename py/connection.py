from PyQt6 import QtSql

class connection():
	def __init__(self, server, db_name, name, password):
		self.server = server
		self.db_name = db_name
		self.name = name
		self.password = password

	def get_connect(self):
		db = QtSql.QSqlDatabase.addDatabase("QODBC")
		db.setDatabaseName(
			f"DRIVER = {{SQL SERVER}}"
			f"SERVER = {self.server}"
			f"DATABASE = {self.db_name}"
			f"UID = {self.name}"
			f"PWD = {self.password}"
		)

		return db