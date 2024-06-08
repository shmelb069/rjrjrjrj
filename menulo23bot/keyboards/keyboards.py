@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("приветствую")

@dp.message_handler(commands=['register'])
async def register_user(message: types.Message):
    data = message.get_args().split()
    if len(data) != 5:
        await message.answer("неверные данные")
        return

    nickname, user_id, email, phone, name = data

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await message.answer("e-mail не найден")
        return

    if not phone.isdigit() or len(phone) != 11:
        await message.answer("неверный номер")
        return

    user_data = {
        "nickname": nickname,
        "user_id": user_id,
        "email": email,
        "phone": phone,
        "name": name
    }

    with open("users.json", "a") as file:
        json.dump(user_data, file)
        file.write('\n')

    await message.answer("вы зарегистрированы")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
