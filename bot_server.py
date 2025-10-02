import os
import logging
import random
from flask import Flask, request, jsonify
import requests

# إعدادات التطبيق
app = Flask(__name__)

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# التوكن الحقيقي للبوت
BOT_TOKEN = "8265161343:AAFgiWyxz-BSZN1MA1iu-qYdLYzlapgCJzo"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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
            # ... باقي الكورسات
        ]
    },
    "د. منار عمران": {
        "count": 35, 
        "courses": [
            "الكورس العملاق البوابات النجمية",
            "انواع التعلق",
            "الطاقة الجنسية",
            # ... باقي الكورسات
        ]
    }
}

# نظام الردود الذكية
class TelegramBot:
    def __init__(self):
        self.responses = {
            "greeting": [
                "🌅 أهلاً وسهلاً! يومك مُشرق بكل الخير 🌟",
                "💫 مرحباً بك! جئت في وقت رائع ✨", 
            ],
            "courses": "📚 *الكورسات المتاحة:*\n\n• أكاديمية منارات: 26 كورس\n• د. منار عمران: 35 كورس\n\n🔍 للمزيد: /courses",
            "pricing": "💰 *الأسعار:*\n\n• الأساسية: 499-799 ر.س\n• المتقدمة: 899-1299 ر.س\n🎁 خصم 10% للمشتركين الجدد!",
            "contact": "📞 *التواصل:*\n\n💬 الواتساب: +966XXXXXXXXX\n📧 البريد: info@manarat-academy.com",
        }
    
    def send_message(self, chat_id, text, parse_mode="Markdown", reply_markup=None):
        """إرسال رسالة عبر تليجرام"""
        url = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        if reply_markup:
            payload['reply_markup'] = reply_markup
            
        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def process_message(self, message_text, chat_id):
        """معالجة الرسالة وإرجاع الرد"""
        message_lower = message_text.lower()
        
        if any(word in message_lower for word in ["/start", "مرحبا", "اهلا", "السلام"]):
            welcome_text = """
🎓 *مرحباً في أكاديمية منارات!* 

🤖 *أنا مساعدك الذكي للاستفسار عن الكورسات*

💫 *يمكنني مساعدتك في:*
• عرض الكورسات المتاحة 📚
• معلومات الأسعار 💰  
• طريقة التسجيل 📝
• إجابة استفساراتك 🤔

✨ *اختر من الأوامر:*
/courses - عرض الكورسات
/pricing - الأسعار  
/contact - التواصل
            """
            keyboard = {
                'inline_keyboard': [[
                    {'text': '📚 الكورسات', 'callback_data': 'show_courses'},
                    {'text': '💰 الأسعار', 'callback_data': 'show_pricing'}
                ], [
                    {'text': '📞 التواصل', 'callback_data': 'show_contact'},
                    {'text': '💬 محادثة', 'callback_data': 'start_chat'}
                ]]
            }
            return self.send_message(chat_id, welcome_text, reply_markup=keyboard)
        
        elif any(word in message_lower for word in ["/courses", "كورس", "دورة", "كورسات"]):
            courses_text = "📚 *كورسات أكاديمية منارات:*\n\n"
            for i, course in enumerate(COURSES_DATA["أكاديمية منارات"]["courses"][:5], 1):
                courses_text += f"{i}. {course}\n"
            courses_text += f"\n*الإجمالي: 26 كورس*\n\n💬 للمزيد: +966XXXXXXXXX"
            return self.send_message(chat_id, courses_text)
        
        elif any(word in message_lower for word in ["/pricing", "سعر", "ثمن", "تكلفة"]):
            return self.send_message(chat_id, self.responses["pricing"])
        
        elif any(word in message_lower for word in ["/contact", "تواصل", "اتصل", "ارقام"]):
            return self.send_message(chat_id, self.responses["contact"])
        
        else:
            return self.send_message(chat_id, "🤔 للاستفسارات التفصيلية، تواصل معنا على الواتساب: +966XXXXXXXXX")

# إنشاء البوت
bot = TelegramBot()

# ويب هوك لتلجرام
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            # معالجة الرسالة
            bot.process_message(text, chat_id)
            
        elif 'callback_query' in data:
            # معالجة أزرار الإنلاين
            callback = data['callback_query']
            chat_id = callback['message']['chat']['id']
            data = callback['data']
            
            if data == 'show_courses':
                bot.process_message('/courses', chat_id)
            elif data == 'show_pricing':
                bot.process_message('/pricing', chat_id)
            elif data == 'show_contact':
                bot.process_message('/contact', chat_id)
            elif data == 'start_chat':
                bot.send_message(chat_id, "💬 *المحادثة الذكية*\n\nاكتب رسالتك وسأرد عليك...")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'status': 'error'}), 500

# إعداد ويب هوك
@app.route('/set_webhook')
def set_webhook():
    try:
        # الحصول على رابط التطبيق
        webhook_url = f"https://{request.host}/webhook"
        
        # تعيين ويب هوك في تليجرام
        url = f"{TELEGRAM_API_URL}/setWebhook"
        payload = {
            'url': webhook_url
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        return jsonify({
            'status': 'success' if result.get('ok') else 'error',
            'message': result.get('description', 'Unknown error'),
            'webhook_url': webhook_url
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# إزالة ويب هوك (للتجربة)
@app.route('/delete_webhook')
def delete_webhook():
    try:
        url = f"{TELEGRAM_API_URL}/deleteWebhook"
        response = requests.post(url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# الصفحة الرئيسية
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>بوت أكاديمية منارات</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #f0f8ff; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .btn { display: inline-block; background: #3498db; color: white; padding: 12px 24px; margin: 10px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 بوت أكاديمية منارات</h1>
            <p>البوت يعمل على تليجرام! اذهب إلى تليجرام وابحث عن البوت للبدء.</p>
            
            <div style="margin: 30px 0;">
                <a href="/set_webhook" class="btn">🔗 تفعيل البوت</a>
                <a href="https://t.me/ManaratAcademyBot" class="btn" target="_blank">💬 فتح تليجرام</a>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 خطوات التشغيل:</h3>
                <p>1. انقر على "تفعيل البوت"</p>
                <p>2. اذهب إلى تليجرام</p>
                <p>3. ابحث عن البوت: <strong>ManaratAcademyBot</strong></p>
                <p>4. ابدأ المحادثة بـ /start</p>
            </div>
        </div>
    </body>
    </html>
    """

# التشغيل الرئيسي
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 بدء تشغيل بوت تليجرام...")
    print("📞 جاهز لاستقبال الرسائل من تليجرام!")
    app.run(host='0.0.0.0', port=port, debug=False)
