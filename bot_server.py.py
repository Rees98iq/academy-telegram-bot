import os
import logging
import random
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# إعدادات التطبيق
app = Flask(__name__)

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# التوكن من متغيرات البيئة
TOKEN = os.getenv('BOT_TOKEN', '8265161343:AAFgiWyxz-BSZN1MA1iu-qYdLYzlapgCJzo')

# بيانات الكورسات
COURSES_DATA = {
    "أكاديمية منارات": {
        "count": 26,
        "courses": [
            "كورس رقصة الحياة",
            "الكورس العملاق البوابات النجمية",
            "عقود الأرواح / دروسها / إكتشاف رسائل الروح",
            "كورس أنواع النفوس",
            "كورس تنظيف ذاكرة المشاعر و الأفكار",
            "حقيبـة المشاكل النفسـية (10 مشاكل نفسية)",
            "كورس مدخل الى عالم التجميل",
            "كورسات وسام هاتف (3 كورسات)",
            "كورس الضغوط النفسية",
            "كورس مهارات وتدريبات لتنمية ذكاء الأطفال",
            "الجرافيك ديزاين – مدخل الى عالم التصميم",
            "شحن الشاكرات بالطاقة الكونية",
            "التصوير الفوتوغرافي – المستوى الاول – رولا مفيد",
            "كورس التربية الأسرية",
            "المرحلة المتوسطة من العلاج البراني – ظافر الياسري",
            "فن استمرار العلاقات ” التواصل “",
            "اتيكيت وبروتكول دولي",
            "فيزياء الكم – محمد طه",
            "علوم ريكي",
            "تطوير ذات – دكتورة إيناس رعد",
            "السايكولوجي – منار عمران (علم الانغرام)",
            "السايكولوجي – منار عمران (القوانين الكونية)",
            "علوم باطنية (البرانا)",
            "روحانيات (الروحانيات وعلم الروح)",
            "روحانيات (عالم الماورائيات)"
        ]
    },
    "د. منار عمران": {
        "count": 35,
        "courses": [
            "الكورس العملاق البوابات النجمية",
            "انواع التعلق",
            "الطاقة الجنسية",
            "الفنغ شوي طاقة المنزل",
            "مواهب الروح",
            "باقة حكايات الاطفال 1",
            "باقة حكايات الاطفال 2",
            "طاقة الحسد",
            "عقلك هو انت",
            "انواع النفوس",
            "ما بعد 2023",
            "التاروت",
            "تنظيف ذاكرة المشاعر والأفكار",
            "فن التواصل",
            "كيف تكون مفسر حلمك",
            "الشاكرات",
            "مقامات الوعي",
            "عالم الماورائيات",
            "اتيكيت وبروتوكول دولي",
            "القوانين الكونية",
            "عقود الارواح",
            "علم الانيجرام",
            "مواعيد سرية - كيمياء الحب",
            "ميزان الانوثة والذكورة",
            "الضغوط النفسية",
            "الاكتئاب",
            "القلق",
            "الخوف",
            "الغضب",
            "التأنيب",
            "الرفض",
            "اقلال قيمة الذات",
            "عقدة الكمال",
            "التوحد",
            "مشاكل عاطفية وجنسية"
        ]
    }
}

# نظام الذكاء الاصطناعي المحلي
class LocalAI:
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        return {
            "تحية": [
                "🌅 أهلاً وسهلاً! يومك مُشرق بكل الخير والطاقة الإيجابية 🌟",
                "💫 مرحباً بك! الكون يُرسل لك ترددات من الحب والوفرة اليوم ✨",
                "🌺 أهلاً بعزيزي! أسعد الله صباحك بالطاقة والبركات 🌈",
                "🕊️ مرحباً! نورت المكان بطاقتك الجميلة 🌙"
            ],
            "شكر": [
                "💖 العفو! شكراً لطاقتك الجميلة وتفاعلك الرائع 🌸",
                "🌟 شكراً لك! وجودك يضيف نوراً خاصاً لهذا المكان ✨"
            ],
            "أسئلة": {
                "كيف أسجل": "📝 **طريقة التسجيل:**\n\n1. اختر الكورس المناسب\n2. تواصل عبر الواتساب: +966XXXXXXXXX\n3. ادفع الرسوم\n4. احصل على المواد فوراً\n\n🎁 خصم 10% للمشتركين الجدد!",
                "الأسعار": "💰 **أسعار الكورسات:**\n\n• الأساسية: 499 - 799 ر.س\n• المتقدمة: 899 - 1299 ر.س\n• الباقات الشاملة: 1499 - 1999 ر.س\n\n💎 جميع الأسعار تشمل شهادة وإشراف مباشر",
                "المدة": "⏰ **مدة الكورسات:**\n\n• كورسات قصيرة: 2-3 أسابيع\n• كورسات متوسطة: 4-6 أسابيع\n• برامج شاملة: 8-12 أسبوع\n\n✨ يمكنك الدراسة بالسرعة المناسبة لك"
            }
        }
    
    def process_message(self, user_id, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["مرحبا", "اهلا", "السلام", "اهلين"]):
            return random.choice(self.knowledge_base["تحية"])
        
        elif any(word in message_lower for word in ["شكر", "ممتاز", "رائع"]):
            return random.choice(self.knowledge_base["شكر"])
        
        elif any(word in message_lower for word in ["سجل", "اشترك", "تسجيل"]):
            return self.knowledge_base["أسئلة"]["كيف أسجل"]
        
        elif any(word in message_lower for word in ["سعر", "ثمن", "تكلفة"]):
            return self.knowledge_base["أسئلة"]["الأسعار"]
        
        elif any(word in message_lower for word in ["مدة", "كم مدة"]):
            return self.knowledge_base["أسئلة"]["المدة"]
        
        else:
            responses = [
                "🤔 سؤال جميل! للاستفسارات التفصيلية، تواصل معنا على الواتساب: +966XXXXXXXXX",
                "💭 أرى أن طاقتك جميلة اليوم! هل تريد معرفة شيء محدد عن كورساتنا؟",
                "✨ يمكنني مساعدتك في معلومات الكورسات والأسعار والتسجيل. ماذا تريد أن تعرف؟"
            ]
            return random.choice(responses)

ai_assistant = LocalAI()

# وظائف البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"""
🎓 **مرحباً {user.first_name} في أكاديمية منارات** 

🤖 **أنا مساعدك الذكي - أعمل 24/7 على السحابة!**

💫 **يمكنني مساعدتك في:**
• عرض الكورسات المتاحة 📚
• معلومات الأسعار 💰  
• طريقة التسجيل 📝
• إجابة استفساراتك 🤔

✨ **اختر من القائمة أو اكتب لي رسالة مباشرة!**
    """
    
    keyboard = [
        [InlineKeyboardButton("📖 عرض الكورسات", callback_data="academy_courses")],
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing_info")],
        [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact_info")],
        [InlineKeyboardButton("💬 محادثة ذكية", callback_data="ai_chat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    courses = COURSES_DATA["أكاديمية منارات"]["courses"]
    courses_text = "🎯 **كورسات أكاديمية منارات** \n\n"
    
    for i, course in enumerate(courses[:10], 1):  # عرض أول 10 كورسات فقط
        courses_text += f"{i}. {course}\n"
    
    courses_text += f"\n📊 **إجمالي عدد الكورسات: {len(courses)} كورس**"
    courses_text += "\n\n💬 **للعرض الكامل، تواصل معنا على الواتساب**"
    
    keyboard = [
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing_info")],
        [InlineKeyboardButton("📞 تواصل", callback_data="contact_info")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(courses_text, reply_markup=reply_markup, parse_mode='Markdown')

async def pricing_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    pricing_text = """
💰 **أسعار كورسات أكاديمية منارات**

🎯 **الكورسات الأساسية:**
• كورسات الطاقة: 499 - 799 ر.س
• دورات العلاقات: 599 - 899 ر.س
• برامج التطوير: 699 - 999 ر.س

💎 **الكورسات المتقدمة:**
• البوابات النجمية: 899 ر.س
• الشفاء الشامل: 1299 ر.س
• البرنامج الذهبي: 1999 ر.س

✨ **الباقات الشاملة:**
• باقة البداية: 1499 ر.س
• باقة التميز: 2499 ر.س
• الباقة الذهبية: 3499 ر.س

🎁 **خصومات خاصة:**
• 10% للطلاب الجدد
• 15% للعائلات
• 20% للمجموعات

💳 **طرق الدفع:** بنكي، تحويل، STC Pay
    """
    
    keyboard = [
        [InlineKeyboardButton("📞 سجل الآن", callback_data="contact_info")],
        [InlineKeyboardButton("📖 الكورسات", callback_data="academy_courses")],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(pricing_text, reply_markup=reply_markup, parse_mode='Markdown')

async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    contact_text = """
📞 **تواصل مع أكاديمية منارات**

💬 **الواتساب:** +966XXXXXXXXX
📧 **البريد الإلكتروني:** info@manarat-academy.com
🌐 **الموقع:** www.manarat-academy.com

🕒 **أوقات الدعم:**
• الأحد - الخميس: 9:00 ص - 6:00 م
• الجمعة - السبت: 4:00 م - 10:00 م

🎯 **للتسجيل في الكورسات:**
1. اختر الكورس المناسب
2. تواصل معنا على الواتساب
3. احصل على خصم 10% كمشترك جديد

✨ **نحن هنا لمساعدتك في رحلتك الروحية**
    """
    
    keyboard = [
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing_info")],
        [InlineKeyboardButton("📖 الكورسات", callback_data="academy_courses")],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(contact_text, reply_markup=reply_markup, parse_mode='Markdown')

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chat_info = """
💬 **المحادثة الذكية**

🤖 **يمكنك سؤالي عن:**

• معلومات عن كورس معين
• أسعار الكورسات 💰
• طريقة التسجيل 📝
• مدة الكورسات ⏰
• أو أي استفسار آخر

💫 **اكتب رسالتك وسأرد عليك فوراً!**
    """
    
    await query.edit_message_text(
        chat_info,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]])
    )

async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_response = ai_assistant.process_message(update.effective_user.id, user_message)
    
    keyboard = [
        [InlineKeyboardButton("📖 الكورسات", callback_data="academy_courses")],
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing_info")],
        [InlineKeyboardButton("📞 تواصل", callback_data="contact_info")],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(ai_response, parse_mode='Markdown', reply_markup=reply_markup)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    welcome_message = f"""
🎓 **مرحباً {user.first_name}** 

✨ **اختر من القائمة:**
    """
    
    keyboard = [
        [InlineKeyboardButton("📖 عرض الكورسات", callback_data="academy_courses")],
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing_info")],
        [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact_info")],
        [InlineKeyboardButton("💬 محادثة ذكية", callback_data="ai_chat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    handlers = {
        "academy_courses": show_courses,
        "pricing_info": pricing_info,
        "contact_info": contact_info,
        "ai_chat": ai_chat,
        "main_menu": main_menu
    }
    
    if data in handlers:
        await handlers[data](update, context)

# إعداد التطبيق
def create_application():
    application = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    return application

# إنشاء التطبيق
application = create_application()

# routes للتطبيق
@app.route('/')
def home():
    return "🚀 بوت أكاديمية منارات يعمل على السيرفر بنجاح! 🌙"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(), application.bot)
        application.process_update(update)
        return 'OK'
    except Exception as e:
        print(f"Error: {e}")
        return 'Error', 500

@app.route('/set_webhook')
def set_webhook():
    webhook_url = os.getenv('WEBHOOK_URL', '') + '/webhook'
    if webhook_url:
        success = application.bot.set_webhook(webhook_url)
        return f"✅ Webhook setup: {success}"
    return "❌ WEBHOOK_URL not set"

# التشغيل
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)