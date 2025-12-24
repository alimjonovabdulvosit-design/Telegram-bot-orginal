from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, PhotoSize
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID, CHANNEL_ID, REQUIRED_CHANNEL_ID
import database as db

router = Router()

# Subscription check helper
async def is_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID, user_id=user_id)
        # Log for debugging
        print(f"DEBUG: User {user_id} status in {REQUIRED_CHANNEL_ID} is {member.status}")
        return member.status in ["member", "administrator", "creator", "restricted"]
    except Exception as e:
        print(f"CRITICAL: Subscription check failed for {user_id}: {e}")
        return False

# Keyboards
def get_check_sub_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url="https://t.me/si_ustoz"))
    builder.row(InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription"))
    return builder.as_markup()

def get_subscribe_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Kursga obuna bo'lish", callback_data="subscribe"))
    return builder.as_markup()

def get_payment_done_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="To'lov qildim (skrinshot yuborish)", callback_data="payment_done"))
    return builder.as_markup()

# Admin Keyboards
def get_admin_approval_kb(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{user_id}"),
        InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{user_id}")
    )
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    
    # Check if this is the channel's bot message
    await message.answer("Ushbu bot SI ustoz kanalinining rasmiy boti hisoblanadi.")
    
    if not await is_subscribed(bot, user_id):
        await message.answer(
            "Botdan foydalanish uchun avval kanalimizga a'zo bo'ling:",
            reply_markup=get_check_sub_kb()
        )
        return

    await db.add_user(user_id, message.from_user.username)
    await message.answer(
        f"Xush kelibsiz, {message.from_user.full_name}!\n\n"
        "Kursga yozilish uchun quyidagi tugmani bosing:",
        reply_markup=get_subscribe_kb()
    )

@router.callback_query(F.data == "check_subscription")
async def process_check_sub(callback: CallbackQuery, bot: Bot):
    if await is_subscribed(bot, callback.from_user.id):
        await callback.message.delete()
        await db.add_user(callback.from_user.id, callback.from_user.username)
        await callback.message.answer(
            f"Rahmat! Obuna tasdiqlandi.\n\nXush kelibsiz, {callback.from_user.full_name}!\n\n"
            "Kursga yozilish uchun quyidagi tugmani bosing:",
            reply_markup=get_subscribe_kb()
        )
    else:
        await callback.answer("❌ Siz hali kanalga a'zo emassiz!", show_alert=True)

@router.callback_query(F.data == "subscribe")
async def process_subscribe(callback: CallbackQuery):
    await callback.message.edit_text(
        "To'lov malumotlari:\n\n"
        "💳 Karta: 9860 3501 4404 1398\n"
        "💰 Summa: 50 000 so'm\n\n"
        "To'lovni amalga oshirgach, chekni (skrinshot) yuboring.",
        reply_markup=get_payment_done_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "payment_done")
async def process_payment_done(callback: CallbackQuery):
    await callback.message.answer("Iltimos, to'lov chekini (rasm ko'rinishida) yuboring.")
    await callback.answer()

@router.message(F.photo)
async def handle_screenshot(message: Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or "Noma'lum"
    
    # Send confirmation to user
    await message.answer("Sizning so'rovingiz adminga yuborildi, kuting...")
    
    # Forward to admin
    photo = message.photo[-1]
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=f"Yangi to'lov so'rovi!\n\nFoydalanuvchi: {message.from_user.full_name} (@{username})\nID: {user_id}",
        reply_markup=get_admin_approval_kb(user_id)
    )

@router.callback_query(F.data.startswith("approve_"))
async def process_approval(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[1])
    
    try:
        # Create invite link with join request
        invite_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            creates_join_request=True,
            name=f"Invite for {user_id}"
        )
        
        await db.update_user_status(user_id, "premium")
        
        await bot.send_message(
            chat_id=user_id,
            text=f"✅ To'lovingiz tasdiqlandi!\n\nKanalga qo'shilish uchun havola: {invite_link.invite_link}\n\n"
                 "Eslatma: Havolani bosganingizdan so'ng, qo'shilish so'rovini yuborishingiz kerak."
        )
        
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n✅ Tasdiqlandi!",
            reply_markup=None
        )
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {e}")
    
    await callback.answer()

@router.callback_query(F.data.startswith("reject_"))
async def process_rejection(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[1])
    
    await bot.send_message(
        chat_id=user_id,
        text="❌ To'lov tasdiqlanmadi. Iltimos, qaytadan urinib ko'ring yoki admin bilan bog'laning: t.me/al_ba_sit"
    )
    
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n❌ Rad etildi!",
        reply_markup=None
    )
    await callback.answer()
