from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Кнопки клавиатуры
clientInfoButton = KeyboardButton('👤 Информация о клиенте')
orderCreateButton = KeyboardButton('🆕 Оформить новый заказ')
orderInfoButton = KeyboardButton('🎯 Информация о моих заказа')
addPhoneButton = KeyboardButton('Добавить номер телефона')
addLocationButton = KeyboardButton('Добавить локацию')
backButton = KeyboardButton('Назад')
cancelButton = KeyboardButton('❌Отмена')

# Клавиатуры и добавление кнопок
# главное меню
mainManuKb = ReplyKeyboardMarkup(resize_keyboard=True)
mainManuKb.row(orderCreateButton, orderInfoButton).row(clientInfoButton)

# добавление телефона и локации у клиента
addClinentInfoKb = ReplyKeyboardMarkup(resize_keyboard=True)
addClinentInfoKb.row(addPhoneButton, addLocationButton).row(backButton)

# Добавление телефона
addPhoneKb = ReplyKeyboardMarkup(resize_keyboard=True)
addPhoneKb.row(addPhoneButton).row(backButton)

# Добавление локации
addLocationKb = ReplyKeyboardMarkup(resize_keyboard=True)
addLocationKb.row(addLocationButton).row(backButton)

# Только кнопка отмена для отмены ввода информации
cancelKb = ReplyKeyboardMarkup(resize_keyboard=True)
cancelKb.row(cancelButton)