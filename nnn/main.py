import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# BOT TOKENINI SHU YERGA KIRIT
TOKEN = "8960089381:AAFGTvbTnplWKTmGi3utuPRFOFtnFjw28i4"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Asosiy menyu
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Hisobot hisoblash")],
    ],
    resize_keyboard=True
)


# Kiritiladigan ma'lumotlar holatlari
class Hisob(StatesGroup):
    marmelad = State()
    idish = State()
    nakleyka = State()
    ish_haqi = State()
    boshqa = State()
    soni = State()
    narx = State()


# Botni boshlash
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🍬 SMART CANDY ANALYTICS\n\n"
        "Marmelad biznesi xarajatlari va foydasini hisoblaymiz.",
        reply_markup=menu
    )


# Hisobot boshlash
@dp.message(F.text == "📊 Hisobot hisoblash")
async def boshlash(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("1️⃣ Marmelad xarajati qancha? (so'm)")
    await state.set_state(Hisob.marmelad)


# Raqam kiritishni tekshirish
async def raqam_olish(message: Message):
    try:
        qiymat = float(message.text.replace(" ", "").replace(",", "."))
        if qiymat < 0:
            raise ValueError
        return qiymat
    except (ValueError, AttributeError):
        await message.answer(
            "❌ Iltimos, 0 yoki undan katta son kiriting. Masalan: 300000"
        )
        return None


@dp.message(Hisob.marmelad)
async def marmelad_olish(message: Message, state: FSMContext):
    qiymat = await raqam_olish(message)
    if qiymat is None:
        return
    await state.update_data(marmelad=qiymat)
    await message.answer("2️⃣ Idishlar xarajati qancha? (so'm)")
    await state.set_state(Hisob.idish)


@dp.message(Hisob.idish)
async def idish_olish(message: Message, state: FSMContext):
    qiymat = await raqam_olish(message)
    if qiymat is None:
        return
    await state.update_data(idish=qiymat)
    await message.answer("3️⃣ Nakleykalar xarajati qancha? (so'm)")
    await state.set_state(Hisob.nakleyka)


@dp.message(Hisob.nakleyka)
async def nakleyka_olish(message: Message, state: FSMContext):
    qiymat = await raqam_olish(message)
    if qiymat is None:
        return
    await state.update_data(nakleyka=qiymat)
    await message.answer("4️⃣ Ish haqi qancha? (so'm)")
    await state.set_state(Hisob.ish_haqi)


@dp.message(Hisob.ish_haqi)
async def ish_haqi_olish(message: Message, state: FSMContext):
    qiymat = await raqam_olish(message)
    if qiymat is None:
        return
    await state.update_data(ish_haqi=qiymat)
    await message.answer("5️⃣ Boshqa xarajatlar qancha? (so'm)")
    await state.set_state(Hisob.boshqa)


@dp.message(Hisob.boshqa)
async def boshqa_olish(message: Message, state: FSMContext):
    qiymat = await raqam_olish(message)
    if qiymat is None:
        return
    await state.update_data(boshqa=qiymat)
    await message.answer("6️⃣ Nechta qadoq tayyorlandi?")
    await state.set_state(Hisob.soni)


@dp.message(Hisob.soni)
async def soni_olish(message: Message, state: FSMContext):
    qiymat = await raqam_olish(message)
    if qiymat is None:
        return

    if not qiymat.is_integer() or qiymat <= 0:
        await message.answer("Qadoqlar sonini musbat butun son bilan kiriting.")
        return

    await state.update_data(soni=int(qiymat))
    await message.answer("7️⃣ Bitta qadoqni do'konga necha so'mdan sotasiz?")
    await state.set_state(Hisob.narx)
@dp.message(Hisob.narx)
async def hisobot(message: Message, state: FSMContext):
    narx = await raqam_olish(message)

    if narx is None:
        return

    data = await state.get_data()

    jami_xarajat = (
        data["marmelad"]
        + data["idish"]
        + data["nakleyka"]
        + data["ish_haqi"]
        + data["boshqa"]
    )

    soni = data["soni"]
    jami_tushum = soni * narx
    tannarx = jami_xarajat / soni
    foyda = jami_tushum - jami_xarajat

    natija = (
        "🍬 SMART CANDY — HISOBOT\n\n"
        f"📦 Tayyorlangan qadoqlar: {soni} ta\n"
        f"💸 Jami xarajat: {jami_xarajat:,.0f} so'm\n"
        f"📦 Bitta qadoq tannarxi: {tannarx:,.2f} so'm\n"
        f"💰 Jami tushum: {jami_tushum:,.0f} so'm\n"
        f"📈 Foyda yoki zarar: {foyda:,.0f} so'm"
    )

    await message.answer(natija)
    await state.clear()


    
async def main():
    print("Bot ishga tushmoqda...")

    bot_info = await bot.get_me()
    print("topuvchi_rbot", bot_info.username)

    print("Telegram bilan aloqa o'rnatildi.")

    await dp.start_polling(bot)


if __name__== "__main__":
   asyncio.run(main())