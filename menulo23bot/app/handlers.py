from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ContentType
from aiogram.filters import CommandStart, Command
from . import keyboards
from .keyboards import Pagination
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
import os
from aiogram.types.input_file import InputFile

router = Router()
dp = Dispatcher()


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()
    id = State()
    email = State()


user_profiles = {}
ITEMS_PER_PAGE = 1

images = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgmqESjdK8NpEcAevXj--m1wO_82JDFVenrA&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPLYigOffiZzIexiNggIeNR8zLTcHHrygK9g&s"
]


async def back_to_main_menu(message: Message):
    await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.main)


async def paginated_images(message: Message, page: int):
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_images = images[start:end]

    if paginated_images:
        await message.answer_photo(photo=paginated_images[0], reply_markup=keyboards.paginator(page))


async def handle_pagination_query(query: CallbackQuery):
    data = Pagination.unpack(query.data)
    current_page = data['page']
    total_items = len(images)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    if data['action'] == 'prev':
        page = max(current_page - 1, 1)
    elif data['action'] == 'next':
        page = min(current_page + 1, total_pages)
    else:
        page = 1

    new_media = InputMediaPhoto(images[page - 1], caption=f"Page {page}/{total_pages}")
    await query.message.edit_media(media=new_media, reply_markup=keyboards.paginator(page))
    await query.answer()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await back_to_main_menu(message)
    await message.reply('Как дела?')


@router.message(Command('help'))
async def cmd_help(message: Message):
    info_text = "Вы можете использовать вот эти команды\n\n"
    info_text += "/help - Поможет вам увидеть все команды\n"
    info_text += "/info - Поможет вам увидеть информацию о нас\n"
    info_text += "/contacts - Поможет вам увидеть наши контакты\n"
    info_text += "/register - Поможет вам Зарегистрироваться\n"
    info_text += "/profile - Поможет вам увидеть ваш профиль\n"
    info_text += "/pagin - Показывает изображения с пагинацией\n"
    info_text += "/afir - Показывает наш последний эфир\n"

    await message.reply(info_text, parse_mode='Markdown')


@router.message(Command('file'))
async def cmd_file(message: Message):
    file_path = "C:\\Users\\perva\\ynamebot\\magicbot_lesson5.zip"
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
        file_input = InputFile.from_bytes(file_bytes, filename="magicbot_lesson5.zip")
        await message.answer_document(file_input)


async def back_to_main_menu(message: Message):
    await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.main)


@router.message(Command('afir'))
async def afect_command_handler(message: Message):
    info_text = "Предыдущий эфир:"
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbGqBPo4DCvz1FaB50KenW0mQb-9Xz3HPkMA&s"

    await message.reply(info_text, parse_mode='Markdown')

    await message.answer_photo(photo=image_url)


@router.message(Command('info'))
async def cmd_info(message: Message):
    info_text = "Информация о нас: Такой не имеется\n\n"
    await message.reply(info_text, parse_mode='Markdown')


@router.message(Command('contacts'))
async def cmd_contacts(message: Message):
    info_text = "Наши контакты:\n\n"
    info_text += "Бот 1: [@yakuzaname]\n"
    info_text += "Бот 2: [@man_wha]\n"
    info_text += "Бот 3: [@manwha1]\n"
    await message.reply(info_text, parse_mode='Markdown')


@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.email)
    await message.answer('Введите ваш email')


@router.message(Register.email)
async def register_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=keyboards.get_number)


@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await state.update_data(id=message.from_user.id)
    await state.set_state(Register.id)

    data = await state.get_data()
    user_id = message.from_user.id
    user_profiles[user_id] = data

    await message.reply(
        f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nНомер: {data["number"]} \nEmail: {data["email"]} \nАйди: {data["id"]} ')
    await state.clear()
    await back_to_main_menu(message)


@router.message(Command('profile'))
async def view_profile(message: Message):
    user_id = message.from_user.id
    user_profile = user_profiles.get(user_id)

    if user_profile:
        profile_info = (
            f'Имя: {user_profile["name"]}\n'
            f'Возраст: {user_profile["age"]}\n'
            f'Номер: {user_profile["number"]}\n'
            f'Email: {user_profile["email"]}\n'
            f'Айди: {user_id}'
        )
        await message.answer(profile_info)
    else:
        await message.answer('Профиль не найден. Пожалуйста, зарегистрируйтесь сначала.')


@router.message(Command('back'))
async def back_to_main(message: Message):
    await back_to_main_menu(message)


@router.message(Command('pagin'))
async def cmd_pagin(message: Message):
    await paginated_images(message, page=1)


def setup(dp: Dispatcher):
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_info, commands=['info'])
    dp.register_message_handler(cmd_contacts, commands=['contacts'])
    dp.register_message_handler(register, commands=['register'])
    dp.register_message_handler(register_name, state=Register.name)
    dp.register_message_handler(register_age, state=Register.age)
    dp.register_message_handler(register_email, state=Register.email)
    dp.register_message_handler(register_number, state=Register.number, content_types=ContentType.CONTACT)
    dp.register_message_handler(view_profile, commands=['profile'])
    dp.register_message_handler(back_to_main, commands=['back'])
    dp.register_message_handler(cmd_pagin, commands=['pagin'])
    dp.register_callback_query_handler(handle_pagination_query, F.data.startswith(Pagination.prefix))