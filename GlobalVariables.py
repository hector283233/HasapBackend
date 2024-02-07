# Глобальные переменные для разрешений
MANAGER = 'Manager' # Глобальная переменная для пользователей с разрешением MANAGER
STOCK = 'Stock' # Глобальная переменная для пользователей с разрешением STOCK
EMPLOYEE = 'Employee'

INCOME = 'Поступление'
OUTGO = 'Отправление'

HASAP_NO = "Hasap №"
FROM_WHOM = "Kimden"
FROM_WHOM_DEP = "Kimden Bölümi"
TO_WHOM = "Kime"
TO_WHOM_DEP = "Kime Bölümi"
CAR_MODEL = "Marka maşyn"
CAR_NUMBER = "Döwlet Belgisi"
CAR_DRIVER = "Sürüjiniň ady, familiýasy"
DIRECTOR = "Başlyk"
ACCOUNTANT = "Baş buhgalter"
SENT_BY = "Goýberdi"
RECIVED_BY = "Kabul etdi"

# Коды ошибок
ERR_PERMISSION_DECLINED = "PER01"
ERR_PERMISSION_WRONG_PASS = "PER02"
ERR_PARAMETERS_INSUFFICIENT = "PAR01"
ERR_PRODUCT_NOT_FOUND = "NF01"
ERR_UNKNOW_ERROR = "UN01"
ERR_USER_NOT_FOUND = "NF02"
ERR_CELL_NOT_FOUND = "NF03"
ERR_CELL_FULL = "CF01"
ERR_CELL_EMPTY = "CE01"
ERR_PALLET_NOT_FOUND = "NF04"
ERR_TRANSFER_NOT_FOUND = "NF05"
ERR_WRONG_TRANSFER = "TR01"
ERR_PALLET_PLACED = "PAL01"
ERR_PALLET_NOT_PLACED = "PAL02"
ERR_CELL_OUT_DOESNT_MATCH = "COD01"
ERR_FILE_NOT_CREATED = "FIL01"


# Глобальные сообшения
MSG_PERMISSION_DECLINED = "У вас нету доступа этим данным."
MSG_PARAMETERS_INSUFFICIENT = "Предоставтье все необходимые и правильные данные."
MSG_PRODUCT_NOT_FOUND = "Данный обект не найден, проверте правильность pk продукта."
MSG_UNKNOWN_ERROR = "неизвестная ошибка, попробуйте заново."
MSG_PERMISSION_WRONG_PASSWORD = "Проверте правильность старого пароля."
MSG_OBJECT_DELETED = "Обект успешно удален."
MSG_USER_NOT_FOUND = "Пользаватель не найден."
MSG_CELL_NOT_FOUND = "Ячейка с таким идентифкатором не существует."
MSG_CELL_NOT_EMPTY = "Данная Ячейка не пуста, попробуйте другую ячейку."
MSG_CELL_EMPYT = "Данная Ячейка пуста, попробуйте другую ячейку."
MSG_PALLET_NOT_FOUND= "Данный Паллет не существует, попробуйте другой паллет."
MSG_TRANSFER_NOT_FOUND = "Данная транзакция не существует, попробуйте другую транзакцию."
MSG_WRONG_TRANSFER = "Идентификаторы транзакции не совпадают."
MSG_PALLET_PLACED = "Данный Пллет уже распределен в ячейку."
MSG_PALLET_NOT_PLACED = "Данный Пллет еще не распределен в ячейку."
MSG_CELL_OUT_DOESNT_MATCH = "Ячейка отправления не совпадают."
MSG_FILE_NOT_CREATED = "Файл не создан, сообшите об ошибке Админу."



TEMP_STOCK_RESPONSIBLE = "Öwezow Merdan"