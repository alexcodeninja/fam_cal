import re

from PyQt6 import QtWidgets, QtCore, QtGui
import choice
import log_in
import registration
import connection
import sys
from PyQt6.QtSql import QSqlQuery

class start_window(QtWidgets.QWidget, choice.Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.pb_enter.clicked.connect(self.show_log_in)
		self.pb_registration.clicked.connect(self.show_reg)

	def show_reg(self):
		self.reg_win = registration_window()
		self.reg_win.show()
		self.close()

	def show_log_in(self):
		self.log_in_win = log_in_window()
		self.log_in_win.show()
		self.close()


class registration_window(QtWidgets.QWidget, registration.Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.pb_confirm.clicked.connect(self.confirmation)

	def confirmation(self):
		#Проверка пароля на спец символы, цифры, uppercase, lowercase, длину
		pas_txt = self.le_password.text()
		is_spec = any([True if (i in r",<.>/?:;\|'{[}]+=_-)(*&^%$#@!'") else False for i in pas_txt])
		is_num = any([True if i.isnumeric() else False for i in pas_txt])
		is_up = any([True if i.isupper() else False for i in pas_txt])
		is_low = any([True if i.islower() else False for i in pas_txt])
		at_all = all([is_up, is_num, is_spec, is_low])

		login_txt = self.le_login.text()
		email_txt = self.le_login.text()

		con = connect_to_sql()
		con.open()
		query = QSqlQuery(con)
		query.prepare(f"SELECT * FROM Users WHERE login='{login_txt}'")
		query.exec()

		#Проверка на существование логина и/или пароля
		if query.numRowsAffected() != -1 :
			msg = QtWidgets.QMessageBox()
			msg.setText("Аккаунт с таким логином уже существует, пожалуйста придумайте другой")
			msg.exec()
			return

		query.prepare("SELECT * WHERE email")

		#Вывод сообщений об ошибке в пароле или почте
		if pas_txt != self.le_repeated_password.text():
			msg = QtWidgets.QMessageBox()
			msg.setText("Пароли не совпадают, проверьте правильность введённых паролей.")
			msg.setWindowTitle("Ошибка регистрации")
			msg.exec()

		elif len(pas_txt) < 8:
			msg = QtWidgets.QMessageBox()
			msg.setText("Длина пароля слишком мала, введите хотябы 8 символов")
			msg.setWindowTitle("Ошибка регистрации")
			msg.exec()

		elif at_all == False:
			msg = QtWidgets.QMessageBox()
			msg.setText("Пароль не надежен:\nдолжен быть хоятбы один спец символ,\nодна буква в малом и большом регистре, и одна цифра")
			msg.setWindowTitle("Ошибка регистрации")
			msg.exec()

		elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' ,self.le_email.text()):
			msg = QtWidgets.QMessageBox()
			msg.setText("Почта была введена не корректно, пожалуйста проверьте валидность почты")
			msg.exec()

		#При правильно введенном пароле
		else:
			msg = QtWidgets.QMessageBox()
			msg.setText("Ваш аккаунт успешно создан!\nПожалуйста запомните ваш логин и пароль\nв дальнейшем их невозможно будет восстановить")
			msg.exec()



class log_in_window(QtWidgets.QWidget, log_in.Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)


def connect_to_sql():
	return connection.connection("DESKTOP-1LBPB4U\SQLEXPRESS", "family_calendar", "admin", "admin").get_connect()

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	app.setStyle("")
	win = start_window()
	win.show()
	sys.exit(app.exec())