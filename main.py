import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Lapor Scam/Ripper")],
        [KeyboardButton(text="⚠️ Lapor Masalah")],
        [KeyboardButton(text="📩 Hubungi Admin")],
        [KeyboardButton(text="📖 Cara Melapor")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Selamat Datang\n\n"
        "Pilih menu di bawah:",
        reply_markup=menu
    )


@dp.message(Text("📖 Cara Melapor"))
async def cara(message: types.Message):
    await message.answer(
        "📖 Cara Melapor:\n\n"
        "1. Masukkan username terlapor\n"
        "2. Kirim bukti chat\n"
        "3. Kirim bukti transaksi\n"
        "4. Jelaskan kronologi"
    )


@dp.message(Text("📩 Hubungi Admin"))
async def admin(message: types.Message):
    await message.answer(
        "Hubungi admin melalui Telegram."
    )


@dp.message(Text("⚠️ Lapor Masalah"))
async def masalah(message: types.Message):
    await message.answer(
        "Silakan jelaskan masalah kamu."
    )


@dp.message(Text("📢 Lapor Scam/Ripper"))
async def laporan(message: types.Message):
    user_data[message.from_user.id] = {
        "step": "username"
    }

    await message.answer(
        "Masukkan username Telegram terlapor:"
    )


@dp.message()
async def proses(message: types.Message):

    uid = message.from_user.id

    if uid not in user_data:
        return

    step = user_data[uid]["step"]

    if step == "username":
        user_data[uid]["username"] = message.text
        user_data[uid]["step"] = "alasan"

        await message.answer(
            "Masukkan alasan laporan:"
        )

    elif step == "alasan":
        user_data[uid]["alasan"] = message.text

        laporan = (
            "🚨 LAPORAN BARU\n\n"
            f"Pelapor: @{message.from_user.username}\n"
            f"Username terlapor: {user_data[uid]['username']}\n"
            f"Alasan: {user_data[uid]['alasan']}"
        )

        await bot.send_message(
            ADMIN_ID,
            laporan
        )

        await message.answer(
            "✅ Laporan sudah dikirim ke admin."
        )

        del user_data[uid]


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
