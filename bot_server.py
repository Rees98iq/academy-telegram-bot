import os
import logging
import random
from flask import Flask, request
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, 
                         MessageHandler, Filters, CallbackContext)

# إعدادات التطبيق
app = Flask(__name__)

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# التوكن
TOKEN = os.getenv('BOT_TOKEN', '8265161343:AAFgiWyxz-BSZN1MA1iu-qYdLYzlapgCJzo')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '') + '/webhook'

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
                "الأسعار": "💰 **أسعار الكورسات:**\n\n• الأساسية: 499 - 799 ر.س\n• المتقدمة: 899 - 1299 ر.س\n• الباقات الشاملة: 1499 - 1999 ر.س",
                "المدة": "⏰ **مدة الكورسات:**\n\n• كورسات قصيرة: 2-3 أسابيع\n• كورسات متوسطة: 4-6 أسابيع\n• برامج شاملة: 8-12 أسبوع"
            }
        }
    
    def process_message(self, user_id, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["مرحبا", "اهلا", "السلام", "اهلين"]):
            return random.choice(self.knowledge_base["تحية"])
        
        elif any(word in message_lower for word in ["شكر", "ممتاز", "رائع", "جميل"]):
            return random.choice(self.knowledge_base["شكر"])
        
        elif any(word in message_lower for word in ["سجل", "اشترك", "تسجيل", "اشتراك"]):
            return self.knowledge_base["أسئلة"]["كيف أسجل"]
        
        elif any(word in message_lower for word in ["سعر", "ثمن", "تكلفة", "كم يكلف"]):
            return self.knowledge_base["أسئلة"]["الأسعار"]
        
        elif any(word in message_lower for word in ["مدة", "كم مدة", "كم وقت"]):
            return self.knowledge_base["أسئلة"]["المدة"]
        
        else:
            return "💬 للاستفسارات التفصيلية، تواصل معنا على الواتساب: +966XXXXXXXXX"

# إنشاء الذكاء الاصطناعي
ai_assistant = LocalAI()

# إنشاء البوت
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# وظائف البوت
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    welcome_message = f"""
🎓 **مرحباً {user.first_name} في أكاديمية منارات** 

🤖 **أنا مساعدك الذكي - أعمل 24/7!**

💫 **يمكنني مساعدتك في:**
• عرض الكورسات المتاحة 📚
• معلومات الأسعار 💰  
• طريقة التسجيل 📝
• إجابة استفساراتك 🤔

✨ **اختر من القائمة:**
    """
    
    keyboard = [
        [InlineKeyboardButton("📖 عرض الكورسات", callback_data="courses")],
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing")], 
        [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact")],
        [InlineKeyboardButton("💬 محادثة ذكية", callback_data="chat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

def show_courses(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    courses = COURSES_DATA["أكاديمية منارات"]["courses"]
    courses_text = "🎯 **كورسات أكاديمية منارات** \n\n"
    
    for i, course in enumerate(courses[:8], 1):
        courses_text += f"{i}. {course}\n"
    
    courses_text += f"\n📊 **الإجمالي: {len(courses)} كورس**"
    courses_text += "\n\n💬 **للعرض الكامل، تواصل معنا**"
    
    keyboard = [
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing")],
        [InlineKeyboardButton("📞 تواصل", callback_data="contact")],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(courses_text, reply_markup=reply_markup, parse_mode='Markdown')

def pricing_info(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    pricing_text = """
💰 **أسعار الكورسات:**

🎯 **الكورسات الأساسية:**
• الطاقة والعلاقات: 499 - 899 ر.س

💎 **الكورسات المتقدمة:**
• البوابات النجمية: 899 ر.س
• البرامج الشاملة: 1299 - 1999 ر.س

✨ **الباقات:**
• الباقة الذهبية: 2499 ر.س

🎁 **خصم 10% للمشتركين الجدد**
    """
    
    keyboard = [
        [InlineKeyboardButton("📞 سجل الآن", callback_data="contact")],
        [InlineKeyboardButton("📖 الكورسات", callback_data="courses")],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(pricing_text, reply_markup=reply_markup, parse_mode='Markdown')

def contact_info(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    contact_text = """
📞 **تواصل معنا:**

💬 **الواتساب:** +966XXXXXXXXX
📧 **البريد:** info@manarat-academy.com  
🌐 **الموقع:** www.manarat-academy.com

🕒 **أوقات الدعم:**
• الأحد - الخميس: 9 ص - 6 م
• الجمعة - السبت: 4 م - 10 م

🎯 **للتسجيل:**
1. اختر الكورس
2. تواصل على الواتساب  
3. احصل على خصم 10%
    """
    
    keyboard = [
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing")],
        [InlineKeyboardButton("📖 الكورسات", callback_data="courses")], 
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(contact_text, reply_markup=reply_markup, parse_mode='Markdown')

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = ai_assistant.process_message(update.effective_user.id, user_message)
    
    keyboard = [
        [InlineKeyboardButton("📖 الكورسات", callback_data="courses")],
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing")],
        [InlineKeyboardButton("📞 تواصل", callback_data="contact")],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(ai_response, reply_markup=reply_markup, parse_mode='Markdown')

def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user = query.from_user
    welcome_message = f"🎓 **مرحباً {user.first_name}**\n\n✨ **اختر من القائمة:**"
    
    keyboard = [
        [InlineKeyboardButton("📖 عرض الكورسات", callback_data="courses")],
        [InlineKeyboardButton("💰 الأسعار", callback_data="pricing")],
        [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact")], 
        [InlineKeyboardButton("💬 محادثة", callback_data="chat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

def chat_mode(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    chat_info = "💬 **المحادثة الذكية**\n\n🤖 **اسألني عن الكورسات، الأسعار، أو التسجيل**"
    
    query.edit_message_text(
        chat_info, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 الرئيسية", callback_data="main")]])
    )

# إضافة المعالجات
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# معالج الأزرار
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    handlers = {
        "courses": show_courses,
        "pricing": pricing_info, 
        "contact": contact_info,
        "chat": chat_mode,
        "main": main_menu
    }
    
    if data in handlers:
        handlers[data](update, context)

dispatcher.add_handler(CallbackQueryHandler(button_handler))

# routes للتطبيق
@app.route('/')
def home():
    return "🚀 بوت أكاديمية منارات يعمل بنجاح! 🌙"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
        return 'OK'
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'Error', 500

@app.route('/set_webhook')
def set_webhook():
    try:
        if WEBHOOK_URL and 'render.com' in WEBHOOK_URL:
            success = bot.set_webhook(WEBHOOK_URL)
            return f"✅ Webhook setup: {success}"
        return "❌ WEBHOOK_URL not set properly"
    except Exception as e:
        return f"❌ Error: {e}"

# التشغيل الرئيسي
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # إعداد webhook تلقائياً
    try:
        if WEBHOOK_URL and 'render.com' in WEBHOOK_URL:
            bot.set_webhook(WEBHOOK_URL)
            print(f"✅ Webhook set to: {WEBHOOK_URL}")
    except Exception as e:
        print(f"⚠️  Webhook error: {e}")
    
    print("🚀 Starting Flask app...")
    app.run(host='0.0.0.0', port=port, debug=False)
