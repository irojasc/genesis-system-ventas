import mysql.connector
from objects import user, customer, ware_book, book, ware_, transferr, saleItem, saleDetailsItem, supplier, purchase
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

class wares_gestor:
	def __init__(self, condition = "main"):
		if condition == "main":
			self.wares = []
			self.load_wares()

	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
			self.cursor = self.mydb.cursor()
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def load_wares(self):
		self.connectDB()
		query = "use genesisDB;"
		query1 = "select * from wares;"
		try:
			self.cursor.execute(query)
			self.cursor.execute(query1)
			# param5: general enabled, param6: tooltip enabled
			for (param1, param2, param3, param4, param5, param6) in self.cursor:
				objWare = ware_(param2, param3, bool(param5), bool(param6))
				self.wares.append(objWare)
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

	def sort_ware(self):
		# funcion que mueve a primera posicion los datos de almacen actual
		self.wares.insert(0, self.wares.pop(next((i for i, item in enumerate(self.wares) if item.cod == self.abrev), -1)))

	def exist_ware(self):
		ware_name = ""
		try:
			file = open("registro.txt", "r")
			vect = file.readlines()
			self.abrev = vect[0].split(":")[1].strip('\n')
			ware_name = vect[1].split(":")[1].strip('\n')
			ware_inputLoc = bool(vect[1].split(":")[2].strip('\n'))
			for i in self.wares:
				if i.cod == self.abrev:
					file.close()
					self.sort_ware()
					return True, (i.cod, self.wares, (i.enabled, i.toolTip, ware_inputLoc)), ware_name
			file.close()
			return False, None, "UNKNOWN"
		except:
			file.close()
			return False, None, "UNKNOWN"

	def upload_location(self, almc = "", cod_book = "", ubic = ""):
		self.connectDB()
		#query = "use genesisDB;"
		query = ("update genesisDB.ware_books set genesisDB.ware_books.ubic_" + almc + " = '" + ubic + "' where genesisDB.ware_books.cod_book = '" + cod_book + "';")
		try:
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

	def upload_isokitem(self, cod_book = "", almc = ""):
		self.connectDB()
		query = ("update genesisDB.ware_books set genesisDB.ware_books.isok_" + almc + " = not genesisDB.ware_books.isok_" + almc + " where genesisDB.ware_books.cod_book = '" + cod_book + "';")
		try:
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

class ware_gestor:
	def __init__(self):
		self.ware_list = []
		self.temp_list = []
	
	def connect_db(self):
		self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	def update_backtablequantity(self, list = None, currentWare = None , operation = None):
		try:
			for i in list:
				for j in self.ware_list:
					if j.objBook.cod == i["cod"]:
						if operation == "ingreso":
							j.almacen_data["cant_" + currentWare] += i["cantidad"]
						elif operation == "salida":
							j.almacen_data["cant_" + currentWare] -= i["cantidad"]
		except:
			ret = QMessageBox.question(self, 'Alerta', "Fallo en actualizacion. Contactar con asistencia", QMessageBox.Ok, QMessageBox.Ok)

	def update_quantity(self, list_ = None, tipo = "" ,Ware = ""):
		tmp_list = []
		dict = {"ingreso": "+",
			"salida": "-"
		}
		self.connect_db()
		try:
			query = ("use genesisDB;")
			for j in list_:
				tmp_list.append((str(j["cantidad"]), j["cod"]))
			query_ = ("update ware_books set cant_" + Ware + " = cant_" + Ware + " " + dict[tipo] + " %s where cod_book = %s")
			self.cursor.execute(query)
			self.cursor.executemany(query_, tmp_list)
			self.mydb.commit()
			self.disconnect_db()
			return True
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()
			return False

	def None_Type(self, val):
		myList = []
		for i in range(len(val)):
			if val[i] is None:
				myList.append("")
			else:
				myList.append(val[i])
		if len(val) > 1:
			tup = tuple(myList)
		else:
			tup = ()
		return tup

	def load_mainlist(self, wares = None):
		self.ware_list.clear()
		self.connect_db()
		try:
			initial_text = "select genesisDB.ware_books.cod_book, genesisDB.books.isbn, genesisDB.books.name, genesisDB.books.autor, " \
						   "genesisDB.books.editorial, genesisDB.books.supplierID, genesisDB.books.pv, "

			for i in wares[1]:
				initial_text = initial_text	 + "genesisDB.ware_books.cant_" + str(i.cod) + ", genesisDB.ware_books.ubic_" + str(i.cod) + ", genesisDB.ware_books.isok_" + str(i.cod) + ","
			initial_text = initial_text.rstrip(initial_text[-1]) + " from genesisDB.ware_books inner join genesisDB.books on genesisDB.ware_books.cod_book = genesisDB.books.cod;"
			query = (initial_text)
			# -----------  carga data de libros  -----------
			self.cursor.execute(query)
			for params in self.cursor:
				values = self.None_Type(tuple(params))
				#values = self.None_Type((params[0], params[1], params[2], params[3], params[4], params[5], params[6],
				#						 params[7], params[8], params[9], params[10], params[11], params[12],
				#						 params[13], params[14], params[15], params[16], params[17]))
				### 0 = cod_book, 1 = isbn, 2 = name, 3 = autor, 4 = editorial, 5 = supplierID, 6= pv, 7,8,9 - 10,11,12 - 13,14,15 - 16,17,18 = cant,ubc,isok
				#objLibro = book(str(values[0]),str(values[1]),str(values[2]),str(values[3]),str(values[4]),str(values[5]),str(values[6]))
				objLibro = book(values)
				#objwareBook = ware_book(wares, objLibro,[values[7],values[10],values[13],values[16]],[values[8],values[11],values[14],values[17]],[values[9],values[12],values[15],values[18]])
				objwareBook = ware_book(objLibro, wares, values)
				self.ware_list.append(objwareBook)

			# -----------  cerrar conexion db  -----------
			self.disconnect_db()
			# -----------  eliminar los codigos de almacen que no tienen objeto libro  -----------
			#for i in ware_list:
			#	if(type(i.book) != str):
			#		self.ware_list.append(i)

		except:
			print("no pudo cargar libros almacen de DB")
			self.disconnect_db()

	def load_items(self, currentWare = None):
		self.ware_list.clear()
		self.connect_db()
		try:
			query = ("select genesisDB.ware_books.cod_book, genesisDB.books.isbn, genesisDB.books.name, genesisDB.books.autor, " \
						   "genesisDB.books.editorial, genesisDB.books.pv, genesisDB.ware_books.cant_" + currentWare +" " \
						   "from genesisDB.ware_books inner join genesisDB.books on genesisDB.ware_books.cod_book = genesisDB.books.cod;")
			
			# -----------  carga data de libros  -----------
			self.cursor.execute(query)
			for params in self.cursor:
				values = self.None_Type(tuple(params))
				# values: [0]: codbook, [1]: isbn, [2]: name, [3]: autor, [4]: editorial, [5]: pv, [6]: cant_currentWare
				dataTup = (values[0], values[1], values[2], values[3], values[4], " ", values[5])
				objLibro = book(dataTup)
				item = saleItem(objLibro, values[6])
				self.ware_list.append(item)

		# -----------  cerrar conexion db  -----------
			self.disconnect_db()
		# -----------  eliminar los codigos de almacen que no tienen objeto libro  -----------
		# for i in ware_list:
		#	if(type(i.book) != str):
		#		self.ware_list.append(i)

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()

class transfer:
	def __init__(self):
		pass

	def connect_db(self):
		self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	def createTransfer(self, list_ = "", wares_i_f = None, user = ""):

		tmp_list = []
		self.connect_db()
		try:
			query_ = ("use genesisDB;")
			query = ("insert into transfer (s_point, f_point, s_date, emiter) values ('" + wares_i_f[0] + "','" +
					 wares_i_f[1] + "','" + datetime.now().strftime("%Y-%m-%d") + "','" + user + "');")
			self.cursor.execute(query_)
			self.cursor.execute(query)
			self.mydb.commit()
			query__ = ("select transfer.id from genesisDB.transfer order by id desc limit 1;")
			query___ = ("insert into transferDetails (cod_operation, book, cant) values (%s, %s, %s)")
			self.cursor.execute(query__)
			for param1 in self.cursor:
				for j in list_:
					tmp_list.append((str(param1[0]), j["cod"], str(j["cantidad"])))
			self.cursor.executemany(query___, tmp_list)
			self.mydb.commit()
			tmp_list.clear()
			for j in list_:
				tmp_list.append((str(j["cantidad"]), j["cod"]))
			query_ = ("update ware_books set cant_" + wares_i_f[0] + " = cant_" + wares_i_f[0] + " - %s where cod_book = %s")
			self.cursor.executemany(query_, tmp_list)
			self.mydb.commit()
			self.disconnect_db()
			return True
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()
			return False

class notifications:
	def __init__(self):
		self.trasfer_list = []

	def connect_db(self):
		self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	def getTransfers(self, currentWare):
		self.trasfer_list.clear()
		init_val = 0
		self.connect_db()
		try:
			query = ("select transfer.id, transfer.s_point, transfer.f_point, transfer.s_date, transfer.f_date, " \
				   "transfer.emiter, transfer.receiver, transfer.state, books.cod, books.isbn, books.name, " \
				   "transferDetails.cant from genesisDB.transferDetails inner join genesisDB.transfer on transferDetails.cod_operation " \
				   "= transfer.id inner join genesisDB.books on transferDetails.book = books.cod where " \
				   "(transfer.f_date = '" + datetime.now().strftime("%Y-%m-%d") + "' or transfer.state != 'CERRADO') "
					"and (transfer.f_point = '" + currentWare + "' or transfer.s_point = '" + currentWare + "');")
			self.cursor.execute(query)
			tmp_list = []
			data = self.cursor.fetchall()
			longitud = len(data)
			k = 0
			for params in data:
				if params[0] == init_val:
					# objTransfer.items.append({"cod": str(params[8]), "isbn": str(params[9]), "name": str(params[10]), "cantidad": int(params[11])})
					tmp_list.append({"cod": str(params[8]), "isbn": str(params[9]), "name": params[10][:30], "cantidad": int(params[11])})
					k += 1
				elif params[0] != init_val:
					if len(self.trasfer_list) > 0:
						objTransfer.items = tmp_list.copy()
						tmp_list.clear()
				# 	# cod[4], s_point[5], f_point[6], s_date[7], f_date[8], emiter[9], receiver[10], state[11], description, items = []
					objTransfer = transferr(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
					#objTransfer.items.append({"cod": str(params[8]), "isbn": str(params[9]), "name": str(params[10]), "cantidad": int(params[11])})
					tmp_list.append({"cod": str(params[8]), "isbn": str(params[9]), "name": params[10][:30], "cantidad": int(params[11])})
					k += 1
					init_val = objTransfer.cod
					self.trasfer_list.append(objTransfer)
			if k == longitud and longitud > 0:
				objTransfer.items = tmp_list.copy()
			self.disconnect_db()
			return True, self.trasfer_list
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()
			return False, None

	def validarReceiver(self, cod, user):
		self.connect_db()
		try:
			que = ("use genesisDB;")
			query = ("select genesisDB.transfer.receiver from transfer where id = " + str(cod) +";")
			self.cursor.execute(que)
			self.cursor.execute(query)
			for params in self.cursor:
				if params[0] != None:
					self.disconnect_db()
					return False, params[0]
			query = ("update genesisDB.transfer set receiver = '" + user + "' where id = " + str(cod) + ";")
			quer = ("update genesisDB.transfer set state = 'ATENDIDO' where id = " + str(cod) + ";")
			self.cursor.execute(query)
			self.cursor.execute(quer)
			self.mydb.commit()
			self.disconnect_db()
			return True, user
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()
			return False, None

	def validarObservar(self, cod, date):
		self.connect_db()
		try:
			query = ("select genesisDB.transfer.state, genesisDB.transfer.f_date from genesisDB.transfer where id = " + str(cod) + ";")
			self.cursor.execute(query)
			for params in self.cursor:
				if params[0] == "OBSERVADO":
					self.disconnect_db()
					return False, params[1]
			quer = ("update genesisDB.transfer set genesisDB.transfer.state = 'OBSERVADO' where id = " + str(cod) + ";")
			quer_ = ("update genesisDB.transfer set genesisDB.transfer.f_date = '" + date + "' where id = " + str(cod) + ";")
			self.cursor.execute(quer)
			self.cursor.execute(quer_)
			self.mydb.commit()
			self.disconnect_db()
			return True, date
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()
			return False, None

	def getText(self, items):
		line = ""
		for i in items:
			line = line + "|CODIGO: " + str(i["cod"]) + " ,ISBN: " + i["isbn"] + " ,NOMBRE: " + i["name"] + ",CANT: " + str(i["cantidad"]) + " \n"
		return line.rstrip()

	def ingresarItems(self, Ware, items, date, cod):
		tmp_list = []
		self.connect_db()
		try:
			query = ("select genesisDB.transfer.state, genesisDB.transfer.f_date from genesisDB.transfer where id = " + str(cod) + ";")
			self.cursor.execute(query)
			for params in self.cursor:
				if params[0] == "CERRADO":
					self.disconnect_db()
					return False, params[1]
			quer = ("update genesisDB.transfer set genesisDB.transfer.state = 'CERRADO' where id = " + str(cod) + ";")
			quer_ = ("update genesisDB.transfer set genesisDB.transfer.f_date = '" + date + "' where id = " + str(cod) + ";")
			self.cursor.execute(quer)
			self.cursor.execute(quer_)

			for j in items:
				tmp_list.append((str(j["cantidad"]), j["cod"]))
			query_ = ("update genesisDB.ware_books set cant_" + Ware + " = cant_" + Ware + " + %s where cod_book = %s")
			self.cursor.executemany(query_, tmp_list)
			self.mydb.commit()
			self.disconnect_db()
			return True, date
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()
			return False, None

class users_gestor:
	def __init__(self):
		self.users = []
		self.fill_users()
		#try:
		#	self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
		#	self.cursor = self.mydb.cursor()
		#except:
		#	self.cursor.close()
		#	self.mydb.close()

	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
			self.cursor = self.mydb.cursor()
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def fill_users(self):
		self.connectDB()
		query = ("CREATE TEMPORARY TABLE genesisDB.tmp "
				 "AS select * from genesisDB.users "
				 "inner join genesisDB.user_flags "
				 "on genesisDB.users.level = genesisDB.user_flags.lvl;")
		query_1 = ("ALTER TABLE genesisDB.tmp DROP COLUMN id, DROP COLUMN level, DROP COLUMN lvl;")
		query_2 = ("SELECT * FROM genesisDB.tmp;")
		try:
			self.cursor.execute(query)
			self.cursor.execute(query_1)
			self.cursor.execute(query_2)
			#param1, param2, param3, param4, param5, param6 -> datos propios (usr, pwd, name, doc, phone, enabled)
			#param7, param8, param9, param10, param11, param12 -> permisos (vender, comprar, registrar compra,
			# verProve, comparar, transferir)
			for (par1, par2, par3, par4, par5, par6, par7, par8, par9, par10, par11, par12) in self.cursor:
				objUser = user(par1, par2, par3, par4, par5, bool(par6), (bool(par7), bool(par8), bool(par9), bool(par10),
																		  bool(par11), bool(par12)))
				self.users.append(objUser)
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

	def check_login(self, name, passwd):
		for i in self.users:
			if i.user == name and i.passwd == passwd:
				return True, (i.user, self.users, i.enabled, i.flags)
		return False, (i.user, self.users, False, None)

class customer_gestor:
	def __init__(self, flag = False):
		if not flag:
			self.Customers = []

	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
			self.cursor = self.mydb.cursor()
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def fill_customers(self):
		self.Customers.clear()
		self.connectDB()
		query = ("select * from genesisDB.customers;")
		try:
			self.cursor.execute(query)
			#param1: id, param2: name, param3: doc_, param4: tel_, param5: dir, param6: gen, param7: sex
			for (param1, param2, param3, param4, param5, param6, param7) in self.cursor:
				objCustomer = customer(param1, param2, str(param3), str(param4), str(param5), str(param6), param7)
				self.Customers.append(objCustomer)
			self.disconnectDB()

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnectDB()

	def addCustomer(self, name: str, doc: str, phone: str):
		try:
			self.connectDB()
			query = ("insert into genesisDB.customers (name_, doc_, tel_) values ('" + name + "', '" + doc + "' "
						", '" + phone + "');")
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
			return True
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnectDB()
			return False

class sales_gestor:
	def __init__(self, condition = False):
		if condition:
			self.sales = []
		else:
			pass
	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
			self.cursor = self.mydb.cursor()
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()
	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def loadSalesDetails(self, currentWare = "", date = ""):
		self.sales.clear()
		self.connectDB()
		query = ("select id_,genesisDB.salesDetails.id,cod,isbn,name,name_,doc_,usr_,cant,genesisDB.salesDetails.credit_,receipt_,total "
				 "from genesisDB.salesDetails "
				 "inner join genesisDB.books on genesisDB.salesDetails.codBook = genesisDB.books.cod "
				 "inner join genesisDB.customers on genesisDB.salesDetails.cust_ = genesisDB.customers.id "
				 "inner join genesisDB.sales on genesisDB.salesDetails.id_sales = genesisDB.sales.id "
				 "where date_ = '" + date + "' and ware_ = '" + currentWare + "' order by id asc;")
		try:
			self.cursor.execute(query)
			##param6: nombre de usuario, param7: doc
			for (param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11, param12) in self.cursor:
				objDetailItems = saleDetailsItem(param1, param2, param3, str(param4), param5, param6, str(param7), param8, param9, param10, param11, float(param12))
				self.sales.append(objDetailItems)
			self.disconnectDB()
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnectDB()

	def addSale(self, currentDate = None, List = None, currentWare = None, idCustomer = None, User = None, val = False):
		self.connectDB()
		query = ("select max(genesisDB.salesDetails.id) from genesisDB.salesDetails left join genesisDB.sales on "
				"genesisDB.salesDetails.id_sales = genesisDB.sales.id where date_ = '" + currentDate + "' "
				"and ware_ = '" + currentWare + "' union select id from genesisDB.sales "
				"where date_ = '" + currentDate + "';")
		try:
			self.cursor.execute(query)
			idValues, b = self.cursor.fetchall()
			idValues = list(idValues)
			if idValues[0] == None and val:
				idValues[0] = 1
			elif idValues[0] != None and val:
				idValues[0] = idValues[0] + 1
			elif not val:
				idValues[0] = 0

			data_update = []
			data = []
			for i in List:
				data_update.append((str(i["cantidad"]), i["cod"]))
				data.append((str(i["id"]), str(b[0]), str(idValues[0]), currentWare, str(idCustomer), User, i["cod"],
						 str(i["cantidad"]), str(int(i["tarjeta"])), str(i["v.final"])))

			stmt_update = "update genesisDB.ware_books set cant_" + currentWare + " = cant_" + currentWare + " - %s " \
							"where cod_book = %s"

			stmt = "insert into genesisDB.salesDetails (id_, id_sales, id, ware_, cust_, usr_, codBook, cant, credit_, total) " \
				   "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) as t " \
				   "on duplicate key update genesisDB.salesDetails.total = genesisDB.salesDetails.total + t.total, " \
				   "genesisDB.salesDetails.cant = genesisDB.salesDetails.cant + t.cant"

			self.cursor.executemany(stmt, data)
			self.mydb.commit()

			self.cursor.executemany(stmt_update, data_update)
			self.mydb.commit()
			self.disconnectDB()

			return True
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnectDB()
			return False

	def changeReceipt(self, currentWare, id_, receipt = "", type = False, date = None, id = None):
		self.connectDB()
		if not type:
			query = ("update genesisDB.salesDetails set receipt_ = '" + receipt + "' "
					"where id_ = " + str(id_) + " and ware_ = '"+ currentWare +"';")
		elif type:
			query = ("update genesisDB.salesDetails as a "
					 "inner join genesisDB.sales b on a.id_sales = b.id set a.receipt_ = '"+ receipt +"' "
			"where b.date_ in ('"+ date +"') and a.id in ("+ str(id) +") and a.ware_ in ('" + currentWare + "');")
		try:
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
			return True
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnectDB()
			return False

class supplier_gestor:
	def __init__(self):
		self.suppliers = []
	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
			self.cursor = self.mydb.cursor(buffered=True)
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()
	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def fill_suppliers(self):
		self.suppliers.clear()
		self.connectDB()
		query = ("select * from genesisDB.suppliers;")
		try:
			self.cursor.execute(query)
			# # param2: usr, param3: pssswd, param4: name, param5: doc, param6: phone, param7: enabled
			for (param1, param2, param3, param4, param5, param6, param7, param8, param9) in self.cursor:
				objSupplier = supplier(param1, param2, param3, param4, param5, param6, param7, param8, param9)
				self.suppliers.append(objSupplier)
			self.disconnectDB()
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

class documents:
	def __init__(self):
		pass
	def get_PDFReport(self):
		passs

class purchase_gestor:
	def __init__(self):
		self.list_purchases = []
	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host="mysql-28407-0.cloudclusters.net", user="admin01",
												passwd="alayza2213", port="28416")
			self.cursor = self.mydb.cursor(buffered=True)
		except:
			print("No se puede conectar a DB")
			self.cursor.close()
			self.mydb.close()
	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def getPurchasesxSupplier(self, supplierCode: str):
		self.list_purchases.clear()
		self.connectDB()
		query = ("select pr.id, pr.user, pr.ware, pr.input_date, pr.serie, pr.type, "
				 "(select IFNULL(truncate(sum(pd.cant*pd.pc), 2), NULL) "
				 "from genesisDB.purchaseDetails pd "
				 "where pd.purchase=pr.id) as sumadeuda, "
				 "(select sum(py.amount) "
				 "from genesisDB.purchase_payments as py "
				 "where py.pur_id=pr.id) as sumapagos "
				 "from genesisDB.purchases as pr where pr.supplier = '" + supplierCode + "';")
		try:
			self.cursor.execute(query)
			# par1: id, par2: user, par3: ware, par4: in_date, par5: serie, par6: type, par7: debt, par8: payment
			filter = lambda x: False if (x == None) else x
			for (par1, par2, par3, par4, par5, par6, par7, par8) in self.cursor:
				objPurchase = purchase(par1, par2, par3, str(par4), par5, par6,
									   float(filter(par7)), float(filter(par8)))
				self.list_purchases.append(objPurchase)
			self.disconnectDB()
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			print("No se puede conectar a DB")
			self.disconnectDB()








