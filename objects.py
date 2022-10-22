class user:
	def __init__(self, user = "", passwd = "", name = "", doc = "", phone = "", enabled = False, flags = None):
		self.user = user #este es el codigo
		self.passwd = passwd
		self.name = name
		self.doc = doc
		self.phone = phone
		self.enabled = enabled
		self.flags = flags

class customer:
	def __init__(self, id = None, name = "", doc = "", tel = "", dir = "", gen = "", sex = 0):
		self.id = id
		self.name = name
		self.doc = doc
		self.tel = tel
		self.dir = dir
		self.gen = gen
		self.sex = sex

class supplier:
	def __init__(self, cod: str, main_doc: str, name: str, name_admin: str, doc_admin: str, phone: str, direction: str, mail: str, tipo: str):
		self.cod = cod
		self.main_doc = main_doc
		self.name = name
		self.name_admin = name_admin
		self.doc_admin = doc_admin
		self.phone = phone
		self.direction = direction
		self.mail = mail
		self.tipo = tipo

class gender:
	def __init__(self, id, name):
		self.id = id
		self.name = name

class movement_detail:
	def __init__(self, id, userID, books_IDs, depart_ID, depart_date, arrival_ID, arrival_date, cond = [False,False]):
		self.id = id
		self.userID = userID
		self.books_IDs = books_IDs
		self.depart_ID = depart_ID
		self.depart_date = depart_date
		self.arrival_ID = arrival_ID
		self.arrival_date = arrival_date
		self.cond = cond

class daily_sale:
	def __init__(self, id, date, books_IDs = [] , total_ = 0):
		self.id = id
		self.books_IDs = books_IDs
		self.date = date
		self.total_ = total_

class saleItem:
	def __init__(self, objBook = None, cantWare = 0):
		self.objBook = objBook
		self.cantWare = cantWare

class saleDetailsItem:
	def __init__(self, id_, id, codbook, isbn, title, customer, doc_, user, cant, credit = False, receipt = "", total = 0.0):
		self.id_ = id_ #int primary
		self.id = id #int day
		self.codbook = codbook
		self.isbn = isbn
		self.title = title  # string
		self.doc_ = doc_
		self.customer = customer
		self.user = user #string
		self.cant = cant #int
		self.credit = bool(credit) #bool
		if receipt == None:
			self.receipt = "" #string
			self.block = False
		else:
			self.receipt = receipt
			self.block = True
		self.total = total #float

class ware_book:
	#def __init__(self,wares = None, objBook = None, ware_quantity = [], ware_location = [], permissions = []):
	def __init__(self, objBook=None, wares = None, data = None):
		ware_1 = wares[1][0].cod
		ware_2 = wares[1][1].cod
		ware_3 = wares[1][2].cod
		ware_4 = wares[1][3].cod

		self.objBook = objBook
		self.almacen_data = {"cant_" + ware_1: int(data[7]),
							 "ubic_" + ware_1: str(data[8]),
							 "isok_" + ware_1: bool(data[9]),
							 "cant_" + ware_2: int(data[10]),
							 "ubic_" + ware_2: str(data[11]),
							 "isok_" + ware_2: bool(data[12]),
							 "cant_" + ware_3: int(data[13]),
							 "ubic_" + ware_3: str(data[14]),
							 "isok_" + ware_3: bool(data[15]),
			                 "cant_" + ware_4: int(data[16]),
							 "ubic_" + ware_4: str(data[17]),
							 "isok_" + ware_4: bool(data[18])}

class transferr:
	def __init__(self, cod = None, s_point = "", f_point = "", s_date = "", f_date = None, emiter = "", receiver = None, state = "", description = "", items= []):
		self.colors = {"amarillo": (225,229,0), "rojo": (211,31,33), "verde": (16,158,89)}
		self.cod = cod
		self.s_point = s_point
		self.f_point = f_point
		self.s_date = str(s_date)
		if f_date == None:
			self.f_date = ""
		elif f_date != None:
			self.f_date = str(f_date)
		self.emiter = emiter
		if receiver == None:
			self.receiver = ""
		elif receiver != None:
			self.receiver = receiver
		self.state = state
		self.description = description
		self.items = items

class book:
	#def __init__(self, cod, isbn, name, autor, editorial, supplierID, Pv = 0, genderID = "", Pc = 0, dsct = 0):
	def __init__(self, data, genderID="", Pc=0, dsct=0):
		self.cod = str(data[0]) # este
		self.isbn = str(data[1]) # este
		self.name = str(data[2]) # este
		self.autor = str(data[3]) # este
		self.editorial = str(data[4]) #este
		self.supplierID = str(data[5]) #este
		self.genderID = genderID
		self.Pc = Pc
		self.Pv = float(data[6]) #este
		self.dsct = dsct

class ware_:
	def __init__(self, cod = "", dir = "", enabled = False, toolTip = False):
		self.cod = cod
		self.dir = dir
		self.enabled = enabled
		self.toolTip = toolTip

class purchase:
	def __init__(self, id: int, user: str, inputDate: str, inputWare: str, tipo: str, serie: str, debt: float, payment: float):
		self.id = id
		self.user = user
		self.inputDate = inputDate
		self.inputWare = inputWare
		self.serie = serie
		self.type = tipo
		self.debt = debt
		self.payment = payment
