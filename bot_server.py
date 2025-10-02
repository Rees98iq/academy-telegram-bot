import os
import logging
import random
from flask import Flask, request

# إعدادات التطبيق
app = Flask(__name__)

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# محاكاة وظائف البوت بدون python-telegram-bot
class BotSimulator:
    def __init__(self):
        self.webhook_set = False
    
    def set_webhook(self, url):
        self.webhook_set = True
        return True
    
    def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
        print(f"📤 Simulated message to {chat_id}: {text[:50]}...")
        return True

# إنشاء محاكي البوت
bot = BotSimulator()

# routes للتطبيق
@app.route('/')
def home():
    return """
    🚀 بوت أكاديمية منارات يعمل بنجاح! 🌙
    
    📚 هذا البوت يعرض كورسات الأكاديمية ويجيب على استفساراتك.
    
    💫 المميزات:
    • عرض الكورسات المتاحة
    • معلومات الأسعار والتسجيل
    • محادثة ذكية مع المساعد
    
    📞 للتواصل: +966XXXXXXXXX
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        # محاكاة معالجة الرسالة
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text.startswith('/start'):
                response = "🎓 **مرحباً في أكاديمية منارات!**\n\nاختر من القائمة:\n• /courses - عرض الكورسات\n• /pricing - الأسعار\n• /contact - التواصل"
            elif text.startswith('/courses'):
                courses = COURSES_DATA["أكاديمية منارات"]["courses"][:5]
                response = "📚 **الكورسات المتاحة:**\n\n" + "\n".join([f"• {course}" for course in courses]) + "\n\n💬 للمزيد: +966XXXXXXXXX"
            elif text.startswith('/pricing'):
                response = "💰 **الأسعار:**\n\n• الأساسية: 499-799 ر.س\n• المتقدمة: 899-1299 ر.س\n\n🎁 خصم 10% للمشتركين الجدد!"
            elif text.startswith('/contact'):
                response = "📞 **التواصل:**\n\n💬 الواتساب: +966XXXXXXXXX\n📧 البريد: info@manarat-academy.com"
            else:
                response = ai_assistant.process_message(chat_id, text)
            
            # في تطبيق حقيقي، هنا نرسل الرسالة للبوت
            print(f"🤖 Response: {response}")
            
        return 'OK'
    except Exception as e:
        print(f"Webhook error: {e}")
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

@app.route('/courses')
def courses_page():
    courses = COURSES_DATA["أكاديمية منارات"]["courses"]
    courses_html = "<h1>🎯 كورسات أكاديمية منارات</h1><ul>"
    for course in courses:
        courses_html += f"<li>{course}</li>"
    courses_html += f"</ul><p><strong>الإجمالي: {len(courses)} كورس</strong></p>"
    courses_html += "<p>💬 للاستفسار: +966XXXXXXXXX</p>"
    return courses_html

@app.route('/pricing')
def pricing_page():
    return """
    <h1>💰 أسعار الكورسات</h1>
    <ul>
        <li>الكورسات الأساسية: 499 - 799 ر.س</li>
        <li>الكورسات المتقدمة: 899 - 1299 ر.س</li>
        <li>الباقات الشاملة: 1499 - 1999 ر.س</li>
    </ul>
    <p>🎁 خصم 10% للمشتركين الجدد</p>
    <p>📞 للاستفسار: +966XXXXXXXXX</p>
    """

@app.route('/contact')
def contact_page():
    return """
    <h1>📞 تواصل معنا</h1>
    <p>💬 الواتساب: +966XXXXXXXXX</p>
    <p>📧 البريد: info@manarat-academy.com</p>
    <p>🌐 الموقع: www.manarat-academy.com</p>
    <p>🕒 أوقات الدعم: 9 ص - 6 م</p>
    """

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
