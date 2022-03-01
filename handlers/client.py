from aiogram import types, Dispatcher
from aiogram.types.message import ContentType
from config import bot
from keyboards import mainManuKb, addClinentInfoKb, addPhoneKb, addLocationKb, cancelKb
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.mongodb import getClientInfo, addClient, addClientInfo

# ! Объявляем состояния
class QuestionsClientInfo(StatesGroup):
    info_menu = State()
    phone = State()
    location = State()

# ! проверяем наличие дынных, для фильтра клавиатур в состоянии info_menu
# ! генерируем сообщение для отправки информации


def checkClientInfo(clientId):
    client_status = None
    data = getClientInfo(clientId)
    if data[3] is None and data[4] is None:
        client_status = 'zero'
    elif data[3] is None and data[4] is not None:
        client_status = 'location'
    elif data[3] is not None and data[4] is None:
        client_status = 'phone'
    else:
        client_status = 'done'
    mess = f'''Информация о клиенте:
TG Nickname: {data[0]}
ФИО: {data[2]} {data[1]}
Локация: {data[3]}
Телефон: {data[4]}

Обращаю внимание, что если поля 'Локация' и 'Телефон' имеют
значение 'None',
значит Вы просто не передавали их мне ранее.'''
    return mess, client_status

# ! Реагируем на команду /start
async def commandStart(message: types.Message):
    client_id = message.from_user.id
    user = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    try:
        await bot.send_message(message.from_user.id, 'ДОБРО ПОЖАЛОВАТЬ!\
            \nЯ бот по заказу Красной икры и работе с клиентами.\nВыберите в МЕНЮ ниже, что Вас интересует?',
                               reply_markup=mainManuKb)
        await message.delete()
        addClient(client_id, user, first_name, last_name)
    except:
        await message.reply('Общение с ботом только в ЛС. Напишите боту: \nhttps://t.me/RedCaviarBot')


# ! Идем в меню инфо клиента, фильтруем клавиатуры.
async def clientInfo(event: types.Message, state: FSMContext):
    await QuestionsClientInfo.info_menu.set()
    data = checkClientInfo(event.from_user.id)
    if data[1] == 'zero':
        await event.answer(data[0], reply_markup=addClinentInfoKb)
    elif data[1] == 'phone':
        await event.answer(data[0], reply_markup=addPhoneKb)
    elif data[1] == 'location':
        await event.answer(data[0], reply_markup=addLocationKb)
    else:
        await state.finish()
        await event.answer(data[0], reply_markup=mainManuKb)

# ! обрабатываем кнопку НАЗАД в меню инфо о клиенте
async def backMainMenu(event: types.Message, state: FSMContext):
        await bot.send_message(chat_id=event.from_user.id, text='ГЛАВНОЕ МЕНЮ\nВыберите один из пунктов:', reply_markup=mainManuKb)
        await state.finish()

# ! добавляем номер телефона - обрабатываем кнопку
async def addClientPhone(message: types.Message, state: FSMContext):
    await message.answer('Введите номер телефона в формате - 79991234567', reply_markup=cancelKb)
    await QuestionsClientInfo.phone.set()


# ! Добавляем локацию - обрабатываем кнопку
async def addClientLocation(message: types.Message, state: FSMContext):
    await message.answer('Введите название города в котором вы находитесь:', reply_markup=cancelKb)
    await QuestionsClientInfo.location.set()



# ! обработчик состояний телефона
async def setDataPhone(event: types.Message, state: FSMContext):
    if event.text == '❌Отмена':
        await QuestionsClientInfo.info_menu.set()
        data = checkClientInfo(event.from_user.id)
        if data[1] == 'zero':
            await event.answer(data[0], reply_markup=addClinentInfoKb)
        elif data[1] == 'location':
            await event.answer(data[0], reply_markup=addLocationKb)
        elif data[1] == 'phone':
            await event.answer(data[0], reply_markup=addPhoneKb)
        else:
            await state.finish()
            await event.answer(data[0], reply_markup=mainManuKb)
    else:
        async with state.proxy() as data:
            data['phone'] = event.text
        addClientInfo(data['phone'], event.from_user.id, 'phone')
        inf = checkClientInfo(event.from_user.id)
        if inf[1] == 'location':
            await QuestionsClientInfo.info_menu.set()
            await event.answer(inf[0], reply_markup=addLocationKb)
            await event.answer(f"Отлично! Ваш контактный номер телефона - {data['phone']} - успешно добавлен. Обновленные данные в сообщении выше.")
        else:
            await state.finish()
            await event.answer(inf[0], reply_markup=mainManuKb)
            await event.answer(f"Отлично! Ваш контактный номер телефона - {data['phone']} - успешно добавлен. Обновленные данные в сообщении выше.")


# ! обработчик состояний локации
async def setDataLocation(event: types.Message, state: FSMContext):
    if event.text == '❌Отмена':
        await QuestionsClientInfo.info_menu.set()
        data = checkClientInfo(event.from_user.id)
        if data[1] == 'zero':
            await event.answer(data[0], reply_markup=addClinentInfoKb)
        elif data[1] == 'location':
            await event.answer(data[0], reply_markup=addLocationKb)
        elif data[1] == 'phone':
            await event.answer(data[0], reply_markup=addPhoneKb)
        else:
            await state.finish()
            await event.answer(data[0], reply_markup=mainManuKb)
    else:
        async with state.proxy() as data:
            data['location'] = event.text
        addClientInfo(data['location'], event.from_user.id, 'location')
        inf = checkClientInfo(event.from_user.id)
        if inf[1] == 'phone':
            await QuestionsClientInfo.info_menu.set()
            await event.answer(inf[0], reply_markup=addPhoneKb)
            await event.answer(f"Отлично! Ваша Локация {data['location']} успешно добавлена. Обновленные данные в сообщении выше.")
        else:
            await state.finish()
            await event.answer(inf[0], reply_markup=mainManuKb)
            await event.answer(f"Отлично! Ваша Локация {data['location']} успешно добавлена. Обновленные данные в сообщении выше.")

# ! регистрируем хэндлеры для запуска
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commandStart, commands=['start', 'help'])
    dp.register_message_handler(
        clientInfo, Text(equals='👤 Информация о клиенте'), state='*')
    dp.register_message_handler(backMainMenu, Text(equals='Назад'), state = QuestionsClientInfo.info_menu)
    dp.register_message_handler(
        addClientPhone, Text(equals = 'Добавить номер телефона'), state = QuestionsClientInfo.info_menu)
    dp.register_message_handler(
        addClientLocation, Text(equals = 'Добавить локацию'), state = QuestionsClientInfo.info_menu)
    dp.register_message_handler(
        setDataPhone, content_types=ContentType.TEXT, state=QuestionsClientInfo.phone)
    dp.register_message_handler(
        setDataLocation, content_types=ContentType.TEXT, state=QuestionsClientInfo.location)
