import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# ضع توكن البوت الخاص بك هنا
TOKEN = 8950689089:AAEOF3ztIf30cXf8FNv7huXtgocpfxNoVEY
bot = telebot.TeleBot(TOKEN)

# ضع معرف تلغرام الخاص بك هنا (Admin ID)
ADMIN_ID = 7254799052  # استبدل الرقم بمعرفك الحقيقي

# قواعد البيانات المؤقتة
users_data = {}          # تخزين بيانات المستخدمين (رابط الإحالة، الأيدي، حالة الحساب)
pending_approvals = {}   # قائمة الانتظار للموافقة (user_id -> pocket_id)
active_users = set()     # قائمة المستخدمين المفعلين الذين تمت الموافقة عليهم

# قائمة أزواج الفوركس مع أعلام الدول
FOREX_PAIRS = {
    "EUR/USD": "🇪🇺/🇺🇸 EUR/USD", "GBP/USD": "🇬🇧/🇺🇸 GBP/USD", 
    "USD/JPY": "🇺🇸/🇯🇵 USD/JPY", "USD/CHF": "🇺🇸/🇨🇭 USD/CHF", 
    "AUD/USD": "🇦🇺/🇺🇸 AUD/USD", "USD/CAD": "🇺🇸/🇨🇦 USD/CAD", 
    "EUR/JPY": "🇪🇺/🇯🇵 EUR/JPY", "EUR/GBP": "🇪🇺/🇬🇧 EUR/GBP", 
    "CAD/JPY": "🇨🇦/🇯🇵 CAD/JPY", "CHF/JPY": "🇨🇭/🇯🇵 CHF/JPY", 
    "AUD/CAD": "🇦🇺/🇨🇦 AUD/CAD", "EUR/CAD": "🇪🇺/🇨🇦 EUR/CAD", 
    "GBP/JPY": "🇬🇧/🇯🇵 GBP/JPY", "EUR/AUD": "🇪🇺/🇦🇺 EUR/AUD", 
    "GBP/CHF": "🇬🇧/🇨🇭 GBP/CHF", "GBP/CAD": "🇬🇧/🇨🇦 GBP/CAD", 
    "GBP/AUD": "🇬🇧/🇦🇺 GBP/AUD", "AUD/JPY": "🇦🇺/🇯🇵 AUD/JPY", 
    "EUR/CHF": "🇪🇺/🇨🇭 EUR/CHF", "CAD/CHF": "🇨🇦/🇨🇭 CAD/CHF"
}

# قائمة أزواج OTC مع أعلام الدول
OTC_PAIRS = {
    "EUR/USD OTC": "🇪🇺/🇺🇸 EUR/USD OTC", "GBP/USD OTC": "🇬🇧/🇺🇸 GBP/USD OTC", 
    "AUD/CAD OTC": "🇦🇺/🇨🇦 AUD/CAD OTC", "BHD/CNY OTC": "🇧🇭/🇨🇳 BHD/CNY OTC",
    "USD/EGP OTC": "🇺🇸/🇪🇬 USD/EGP OTC", "USD/DZD OTC": "🇺🇸/🇩🇿 USD/DZD OTC", 
    "USD/ARS OTC": "🇺🇸/🇦🇷 USD/ARS OTC", "SAR/CNY OTC": "🇸🇦/🇨🇳 SAR/CNY OTC",
    "MAD/USD OTC": "🇲🇦/🇺🇸 MAD/USD OTC", "UAH/USD OTC": "🇺🇦/🇺🇸 UAH/USD OTC", 
    "EUR/TRY OTC": "🇪🇺/🇹🇷 EUR/TRY OTC", "CAD/JPY OTC": "🇨🇦/🇯🇵 CAD/JPY OTC", 
    "EUR/CHF OTC": "🇪🇺/🇨🇭 EUR/CHF OTC", "EUR/NZD OTC": "🇪🇺/🇳🇿 EUR/NZD OTC", 
    "QAR/CNY OTC": "🇶🇦/🇨🇳 QAR/CNY OTC", "LBP/USD OTC": "🇱🇧/🇺🇸 LBP/USD OTC", 
    "USD/CLP OTC": "🇺🇸/🇨🇱 USD/CLP OTC", "NGN/USD OTC": "🇳🇬/🇺🇸 NGN/USD OTC", 
    "USD/MXN OTC": "🇺🇸/🇲🇽 USD/MXN OTC", "USD/MYR OTC": "🇺🇸/🇲🇾 USD/MYR OTC", 
    "USD/PHP OTC": "🇺🇸/🇵🇭 USD/PHP OTC", "USD/RUB OTC": "🇺🇸/🇷🇺 USD/RUB OTC", 
    "USD/SGD OTC": "🇺🇸/🇸🇬 USD/SGD OTC", "YER/USD OTC": "🇾🇪/🇺🇸 YER/USD OTC", 
    "EUR/HUF OTC": "🇪🇺/🇭🇺 EUR/HUF OTC", "KES/USD OTC": "🇰🇪/🇺🇸 KES/USD OTC", 
    "USD/BDT OTC": "🇺🇸/🇧🇩 USD/BDT OTC", "USD/COP OTC": "🇺🇸/🇨🇴 USD/COP OTC", 
    "USD/IDR OTC": "🇺🇸/🇮🇩 USD/IDR OTC", "TND/USD OTC": "🇹🇳/🇺🇸 TND/USD OTC", 
    "NZD/JPY OTC": "🇳🇿/🇯🇵 NZD/JPY OTC", "CHF/NOK OTC": "🇨🇭/🇳🇴 CHF/NOK OTC", 
    "OMR/CNY OTC": "🇴🇲/🇨🇳 OMR/CNY OTC", "AUD/NZD OTC": "🇦🇺/🇳🇿 AUD/NZD OTC", 
    "AED/CNY OTC": "🇦🇪/🇨🇳 AED/CNY OTC", "USD/CNH OTC": "🇺🇸/🇨🇳 USD/CNH OTC", 
    "USD/BRL OTC": "🇺🇸/🇧🇷 USD/BRL OTC", "JOD/CNY OTC": "🇯🇴/🇨🇳 JOD/CNY OTC", 
    "USD/PKR OTC": "🇺🇸/🇵🇰 USD/PKR OTC", "USD/INR OTC": "🇺🇸/🇮🇳 USD/INR OTC", 
    "USD/VND OTC": "🇺🇸/🇻🇳 USD/VND OTC", "ZAR/USD OTC": "🇿🇦/🇺🇸 ZAR/USD OTC", 
    "USD/THB OTC": "🇺🇸/🇹🇭 USD/THB OTC"
}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    
    # إذا كان المستخدم هو المدير
    if user_id == ADMIN_ID:
        send_main_menu(message.chat.id, is_admin=True)
        return

    # إذا كان المستخدم تمت الموافقة عليه مسبقاً
    if user_id in active_users:
        send_main_menu(message.chat.id, is_admin=False)
        return

    # إذا كان بانتظار الموافقة
    if user_id in pending_approvals:
        bot.send_message(message.chat.id, "⏳ حسابك قيد المراجعة والانتظار ريثما يوافق عليه المدير من لوحة التحكم.")
        return

    # رسالة الترحيب الأولى للتسجيل عبر الرابط وإدخال الأيدي
    markup = InlineKeyboardMarkup()
    btn_register = InlineKeyboardButton("🌐 تسجيل حساب جديد", url="https://pocket-friends.co/r/xhjemrkowr")
    markup.add(btn_register)
    btn_submit_id = InlineKeyboardButton("✍️ إدخال الأيدي (ID) للتحقق", callback_data="enter_pocket_id")
    markup.add(btn_submit_id)

    welcome_text = (
        "<b>مرحباً بك في بوت التوصيات الاحترافي!</b>\n\n"
        "للتمكن من استخدام البوت والحصول على الإشارات، يجب عليك أولاً:\n"
        "1. إنشاء حساب جديد عبر رابط الإحالة الخاص بنا.\n"
        "2. إدخال رقم الأيدي (Pocket ID) الخاص بك للتحقق.\n\n"
        "اضغط على الأزرار أدناه للبدء:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'enter_pocket_id')
def request_pocket_id(call):
    msg = bot.send_message(call.message.chat.id, "✍️ أرسل الآن رقم الأيدي (Pocket ID) الخاص بك في رسالة:")
    bot.register_next_step_handler(msg, process_pocket_id)

def process_pocket_id(message):
    user_id = message.from_user.id
    pocket_id = message.text.strip()
    username = message.from_user.username or message.from_user.first_name

    # حفظ الأيدي مؤقتاً
    users_data[user_id] = pocket_id
    pending_approvals[user_id] = pocket_id

    bot.send_message(message.chat.id, "✅ تم إرسال الأيدي بنجاح!\n⏳ يرجى الانتظار ريثما يقوم المدير بمراجعة طلبك والموافقة عليه.")

    # إشعار المدير بوجود طلب تفعيل جديد
    admin_markup = InlineKeyboardMarkup(row_width=2)
    btn_accept = InlineKeyboardButton("✅ موافقة", callback_data=f"approve_{user_id}")
    btn_reject = InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user_id}")
    admin_markup.add(btn_accept, btn_reject)

    admin_text = (
        "🔔 <b>طلب تفعيل حساب جديد قيد الانتظار:</b>\n\n"
        f"👤 اسم المستخدم: @{username}\n"
        f"🆔 معرف التيليجرام: <code>{user_id}</code>\n"
        f"💳 الأيدي المُدخل: <b>{pocket_id}</b>"
    )
    try:
        bot.send_message(ADMIN_ID, admin_text, reply_markup=admin_markup, parse_mode='HTML')
    except Exception:
        pass

# --- لوحة تحكم المدير لإدارة الموافقات ---
@bot.callback_query_handler(func=lambda call: call.data == 'admin_panel')
def admin_panel(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "عذراً، هذه اللوحة للمدير فقط!", show_alert=True)
        return

    markup = InlineKeyboardMarkup(row_width=1)
    btn_stats = InlineKeyboardButton(f"👥 الطلبات المعلقة ({len(pending_approvals)})", callback_data="admin_pending_list")
    btn_broadcast = InlineKeyboardButton("📢 إرسال رسالة للجميع (بث)", callback_data="admin_broadcast")
    btn_back = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")
    markup.add(btn_stats, btn_broadcast, btn_back)

    text = (
        "🛠 <b>لوحة تحكم المدير (Admin Panel)</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"لديك {len(pending_approvals)} طلبات تفعيل بانتظار الموافقة."
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_pending_list')
def admin_pending_list(call):
    if call.from_user.id != ADMIN_ID:
        return

    if not pending_approvals:
        bot.answer_callback_query(call.id, "لا توجد طلبات معلقة حالياً!", show_alert=True)
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for u_id, p_id in list(pending_approvals.items())[:10]:
        markup.add(InlineKeyboardButton(f"ID: {p_id} (User: {u_id})", callback_data=f"review_{u_id}"))
    markup.add(InlineKeyboardButton("🔙 رجوع لوحة التحكم", callback_data="admin_panel"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="📋 <b>قائمة الطلبات المعلقة:</b>\nاختر طلباً لمراجعته:", reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data.startswith('review_'))
def review_specific_user(call):
    if call.from_user.id != ADMIN_ID:
        return
    u_id = int(call.data.split('_')[1])
    p_id = pending_approvals.get(u_id, "غير معروف")

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("✅ موافقة", callback_data=f"approve_{u_id}"),
               InlineKeyboardButton("❌ رفض", callback_data=f"reject_{u_id}"))
    markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_pending_list"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"👤 تفاصيل المستخدم:\n- Telegram ID: {u_id}\n- Pocket ID: {p_id}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_') or call.data.startswith('reject_'))
def handle_approval_action(call):
    if call.from_user.id != ADMIN_ID:
        return

    action, u_id_str = call.data.split('_')
    u_id = int(u_id_str)

    if action == 'approve':
        if u_id in pending_approvals:
            del pending_approvals[u_id]
        active_users.add(u_id)
        try:
            bot.send_message(u_id, "🎉 <b>تمت الموافقة على حسابك بنجاح!</b>\nيمكنك الآن استخدام البوت والحصول على التوصيات.", parse_mode='HTML')
        except Exception:
            pass
        bot.answer_callback_query(call.id, "تمت الموافقة بنجاح وإشعار المستخدم.")
    else:
        if u_id in pending_approvals:
            del pending_approvals[u_id]
        if u_id in users_data:
            del users_data[u_id]
        try:
            bot.send_message(u_id, "❌ عذراً، تم رفض طلب تفعيل حسابك. تأكد من التسجيل عبر الرابط الصحيح وإدخال الأيدي بدقة.")
        except Exception:
            pass
        bot.answer_callback_query(call.id, "تم رفض الطلب وإشعار المستخدم.")

    # تحديث لوحة التحكم للمدير
    try:
        admin_panel(call)
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'admin_broadcast')
def admin_broadcast_prompt(call):
    if call.from_user.id != ADMIN_ID:
        return
    msg = bot.send_message(call.message.chat.id, "📢 أرسل الآن نص الإعلان أو الرسالة لبثها لجميع المستخدمين المفعلين:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    broadcast_text = message.text
    success, fail = 0, 0
    for u_id in active_users:
        try:
            bot.send_message(u_id, f"📢 <b>إعلان من الإدارة:</b>\n\n{broadcast_text}", parse_mode='HTML')
            success += 1
        except Exception:
            fail += 1
    bot.send_message(message.chat.id, f"✅ تم الإرسال بنجاح إلى: {success}\n❌ فشل الإرسال إلى: {fail}")

# --- الوظائف الرئيسية للمשתمين المفعلين ---
def send_main_menu(chat_id, is_admin):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_forex = InlineKeyboardButton("📈 FOREX", callback_data="category_forex")
    btn_otc = InlineKeyboardButton("🔄 OTC", callback_data="category_otc")
    markup.add(btn_forex, btn_otc)

    if is_admin:
        markup.add(InlineKeyboardButton("🛠 لوحة إدارة المدير", callback_data="admin_panel"))

    welcome_text = (
        "<b>Signals hub</b>\n\n"
        "أهلاً بك في مركز التوصيات. اختر السوق المفضل أدناه:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def category_selection(call):
    user_id = call.from_user.id
    if user_id != ADMIN_ID and user_id not in active_users:
        bot.answer_callback_query(call.id, "حسابك غير مفعل بعد، انتظر موافقة المدير!", show_alert=True)
        return

    category = call.data.split('_')[1]
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []

    if category == 'forex':
        for key, label in FOREX_PAIRS.items():
            buttons.append(InlineKeyboardButton(label, callback_data=f"signal_{key}"))
        text = "<b>قسم الفوركس (Classic):</b>\nاختر زوج العملات للحصول على التوصيات:"
    elif category == 'otc':
        for key, label in OTC_PAIRS.items():
            buttons.append(InlineKeyboardButton(label, callback_data=f"signal_{key}"))
        text = "<b>قسم التداول الرقمي (OTC):</b>\nاختر زوج العملات للحصول على التوصيات:"

    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data.startswith('signal_'))
def send_signal(call):
    user_id = call.from_user.id
    if user_id != ADMIN_ID and user_id not in active_users:
        bot.answer_callback_query(call.id, "حسابك غير مفعل بعد!", show_alert=True)
        return

    pair_key = call.data.replace('signal_', '', 1)
    directions = ["🟢 شراء (CALL)", "🔴 بيع (PUT)"]
    
    sig_1m = random.choice(directions)
    sig_3m = random.choice(directions)
    sig_5m = random.choice(directions)
    sig_15m = random.choice(directions)
    sig_1h = random.choice(directions)
    sig_4h = random.choice(directions)

    signal_text = (
        f"📊 <b>مركز التوصيات والإشارات الشاملة</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 الزوج: <b>{pair_key}</b>\n\n"
        f"⏱ <b>الفريمات الزمنية:</b>\n"
        f"├ 1 دقيقة ⟵ {sig_1m}\n"
        f"├ 3 دقائق ⟵ {sig_3m}\n"
        f"├ 5 دقائق ⟵ {sig_5m}\n"
        f"├ 15 دقيقة ⟵ {sig_15m}\n"
        f"├ 1 ساعة (1H) ⟵ {sig_1h}\n"
        f"└ 4 ساعات (4H) ⟵ {sig_4h}\n\n"
        f"⚠️ <i>ملاحظة: التزم بإدارة رأس المال ودخول الصفقة في الوقت المناسب.</i>"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 تحديث الإشارات", callback_data=f"signal_{pair_key}"))
    markup.add(InlineKeyboardButton("🔙 رجوع للأزواج", callback_data="back_main"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=signal_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'back_main')
def back_to_main(call):
    user_id = call.from_user.id
    is_admin = (user_id == ADMIN_ID)
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn_forex = InlineKeyboardButton("📈 FOREX", callback_data="category_forex")
    btn_otc = InlineKeyboardButton("🔄 OTC", callback_data="category_otc")
    markup.add(btn_forex, btn_otc)

    if is_admin:
        markup.add(InlineKeyboardButton("🛠 لوحة إدارة المدير", callback_data="admin_panel"))

    welcome_text = (
        "<b>Signals hub</b>\n\n"
        "أهلاً بك في مركز التوصيات. اختر السوق المفضل أدناه:"
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=welcome_text, reply_markup=markup, parse_mode='HTML')

# تشغيل البوت
bot.polling(none_stop=True)
 
