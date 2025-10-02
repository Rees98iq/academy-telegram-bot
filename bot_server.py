import os
import random
from flask import Flask, request, jsonify

# إعدادات التطبيق
app = Flask(__name__)

# التوكن (للاستخدام المستقبلي)
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

# نظام الردود الذكية
class SmartResponder:
    def __init__(self):
        self.responses = {
            "greeting": [
                "🌅 أهلاً وسهلاً! يومك مُشرق بكل الخير 🌟",
                "💫 مرحباً بك! جئت في وقت رائع ✨", 
                "🌺 أهلاً بعزيزي! نورت متجرنا 🌈",
                "🕊️ مرحباً! أسعد الله وقتك 🌙"
            ],
            "thanks": [
                "💖 العفو! شكراً لطاقتك الجميلة 🌸",
                "🌟 شكراً لك! وجودك يضيف نوراً ✨"
            ],
            "courses": "📚 **الكورسات المتاحة:**\n\nأكاديمية منارات: 26 كورس\nد. منار عمران: 35 كورس\n\n🔍 للمزيد: /courses",
            "pricing": "💰 **الأسعار:**\n\n• الأساسية: 499-799 ر.س\n• المتقدمة: 899-1299 ر.س\n• الباقات: 1499-1999 ر.س\n\n🎁 خصم 10% للمشتركين الجدد!",
            "contact": "📞 **التواصل:**\n\n💬 الواتساب: +966XXXXXXXXX\n📧 البريد: info@manarat-academy.com\n🌐 الموقع: www.manarat-academy.com",
            "unknown": "🤔 للاستفسارات التفصيلية، تواصل معنا مباشرة على الواتساب: +966XXXXXXXXX"
        }
    
    def get_response(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["مرحبا", "اهلا", "السلام", "اهلين", "hello", "hi"]):
            return random.choice(self.responses["greeting"])
        elif any(word in message_lower for word in ["شكر", "ممتاز", "رائع"]):
            return random.choice(self.responses["thanks"])
        elif any(word in message_lower for word in ["كورس", "دورة", "كورسات", "دورات"]):
            return self.responses["courses"]
        elif any(word in message_lower for word in ["سعر", "ثمن", "تكلفة", "كم يكلف"]):
            return self.responses["pricing"]
        elif any(word in message_lower for word in ["تواصل", "اتصل", "ارقام", "تلفون"]):
            return self.responses["contact"]
        else:
            return self.responses["unknown"]

# إنشاء المساعد
responder = SmartResponder()

# الصفحة الرئيسية
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>أكاديمية منارات</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { 
                color: #fff; 
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .nav { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 15px; 
                margin: 30px 0; 
            }
            .nav a { 
                background: rgba(255,255,255,0.2); 
                color: white; 
                padding: 20px; 
                text-decoration: none; 
                border-radius: 10px; 
                transition: all 0.3s;
                font-size: 1.1em;
            }
            .nav a:hover { 
                background: rgba(255,255,255,0.3); 
                transform: translateY(-5px);
            }
            .course-list { 
                text-align: right; 
                margin: 20px 0; 
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
            }
            .course-item { 
                padding: 10px; 
                border-bottom: 1px solid rgba(255,255,255,0.2); 
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                gap: 15px; 
                margin: 30px 0; 
            }
            .stat-card { 
                background: rgba(255,255,255,0.2); 
                padding: 20px; 
                border-radius: 10px; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 أكاديمية منارات</h1>
            <p style="font-size: 1.2em; margin-bottom: 30px;">مرحباً بك في منصة الكورسات الروحانية والتطوير الذاتي</p>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📖 الأكاديمية</h3>
                    <p style="font-size: 2em; margin: 10px 0;">26</p>
                    <p>كورس متاح</p>
                </div>
                <div class="stat-card">
                    <h3>👩‍🏫 د. منار</h3>
                    <p style="font-size: 2em; margin: 10px 0;">35</p>
                    <p>كورس متاح</p>
                </div>
                <div class="stat-card">
                    <h3>⭐ الإجمالي</h3>
                    <p style="font-size: 2em; margin: 10px 0;">61</p>
                    <p>كورس</p>
                </div>
            </div>
            
            <div class="nav">
                <a href="/courses">📚 عرض الكورسات</a>
                <a href="/pricing">💰 الأسعار</a>
                <a href="/contact">📞 التواصل</a>
                <a href="/api/chat">💬 محادثة ذكية</a>
            </div>
            
            <div style="margin-top: 40px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                <h3>💫 لماذا تختار أكاديمية منارات؟</h3>
                <p>نقدم لك تجربة فريدة في مجال الطاقة الروحانية والتطوير الذاتي مع أفضل المدربين</p>
            </div>
        </div>
    </body>
    </html>
    """

# صفحة الكورسات
@app.route('/courses')
def courses():
    academy_courses = COURSES_DATA["أكاديمية منارات"]["courses"]
    dr_courses = COURSES_DATA["د. منار عمران"]["courses"]
    
    html = """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الكورسات - أكاديمية منارات</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1, h2 { 
                color: #fff; 
                text-align: center;
            }
            .course-section { 
                margin: 30px 0; 
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
            }
            .course-list { 
                text-align: right; 
            }
            .course-item { 
                padding: 12px; 
                border-bottom: 1px solid rgba(255,255,255,0.2); 
                margin: 5px 0;
            }
            .nav { 
                text-align: center; 
                margin: 20px 0; 
            }
            .nav a { 
                background: rgba(255,255,255,0.2); 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 كورسات أكاديمية منارات</h1>
            
            <div class="course-section">
                <h2>🎯 أكاديمية منارات (26 كورس)</h2>
                <div class="course-list">
    """
    
    for i, course in enumerate(academy_courses, 1):
        html += f'<div class="course-item">{i}. {course}</div>'
    
    html += """
                </div>
            </div>
            
            <div class="course-section">
                <h2>👩‍🏫 د. منار عمران (35 كورس)</h2>
                <div class="course-list">
    """
    
    for i, course in enumerate(dr_courses, 1):
        html += f'<div class="course-item">{i}. {course}</div>'
    
    html += """
                </div>
            </div>
            
            <div class="nav">
                <a href="/">🏠 الرئيسية</a>
                <a href="/pricing">💰 الأسعار</a>
                <a href="/contact">📞 التواصل</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

# صفحة الأسعار
@app.route('/pricing')
def pricing():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الأسعار - أكاديمية منارات</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { 
                color: #fff; 
                text-align: center;
            }
            .pricing-table { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 20px; 
                margin: 30px 0; 
            }
            .pricing-card { 
                background: rgba(255,255,255,0.2); 
                padding: 25px; 
                border-radius: 10px; 
                text-align: center;
            }
            .price { 
                font-size: 2em; 
                margin: 15px 0; 
                color: #ffd700;
            }
            .nav { 
                text-align: center; 
                margin: 20px 0; 
            }
            .nav a { 
                background: rgba(255,255,255,0.2); 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💰 أسعار الكورسات</h1>
            
            <div class="pricing-table">
                <div class="pricing-card">
                    <h3>🎯 الأساسية</h3>
                    <div class="price">499 - 799 ر.س</div>
                    <p>كورسات الطاقة والعلاقات</p>
                </div>
                
                <div class="pricing-card">
                    <h3>💎 المتقدمة</h3>
                    <div class="price">899 - 1299 ر.س</div>
                    <p>البوابات النجمية والبرامج المتقدمة</p>
                </div>
                
                <div class="pricing-card">
                    <h3>✨ الباقات</h3>
                    <div class="price">1499 - 1999 ر.س</div>
                    <p>باقات شاملة متعددة الكورسات</p>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; text-align: center;">
                <h3>🎁 عروض خاصة</h3>
                <p>• خصم 10% للمشتركين الجدد</p>
                <p>• خصم 15% للعائلات</p>
                <p>• خصم 20% للمجموعات</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 الرئيسية</a>
                <a href="/courses">📚 الكورسات</a>
                <a href="/contact">📞 التواصل</a>
            </div>
        </div>
    </body>
    </html>
    """

# صفحة التواصل
@app.route('/contact')
def contact():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>التواصل - أكاديمية منارات</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { 
                color: #fff; 
                text-align: center;
            }
            .contact-info { 
                background: rgba(255,255,255,0.2); 
                padding: 25px; 
                border-radius: 10px; 
                margin: 20px 0;
            }
            .contact-item { 
                margin: 15px 0; 
                padding: 15px; 
                background: rgba(255,255,255,0.1); 
                border-radius: 8px;
            }
            .nav { 
                text-align: center; 
                margin: 20px 0; 
            }
            .nav a { 
                background: rgba(255,255,255,0.2); 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📞 تواصل معنا</h1>
            
            <div class="contact-info">
                <div class="contact-item">
                    <h3>💬 الواتساب</h3>
                    <p style="font-size: 1.2em;">+966XXXXXXXXX</p>
                </div>
                
                <div class="contact-item">
                    <h3>📧 البريد الإلكتروني</h3>
                    <p style="font-size: 1.2em;">info@manarat-academy.com</p>
                </div>
                
                <div class="contact-item">
                    <h3>🌐 الموقع الإلكتروني</h3>
                    <p style="font-size: 1.2em;">www.manarat-academy.com</p>
                </div>
                
                <div class="contact-item">
                    <h3>🕒 أوقات الدعم</h3>
                    <p>الأحد - الخميس: 9:00 ص - 6:00 م</p>
                    <p>الجمعة - السبت: 4:00 م - 10:00 م</p>
                </div>
            </div>
            
            <div style="background: rgba(255,215,0,0.2); padding: 20px; border-radius: 10px; text-align: center;">
                <h3>🎯 طريقة التسجيل</h3>
                <p>1. اختر الكورس المناسب</p>
                <p>2. تواصل معنا على الواتساب</p>
                <p>3. احصل على خصم 10% كمشترك جديد</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 الرئيسية</a>
                <a href="/courses">📚 الكورسات</a>
                <a href="/pricing">💰 الأسعار</a>
            </div>
        </div>
    </body>
    </html>
    """

# API للمحادثة الذكية
@app.route('/api/chat', methods=['GET', 'POST'])
def chat_api():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message', '')
        response = responder.get_response(message)
        return jsonify({'response': response})
    
    # واجهة المحادثة
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المحادثة الذكية - أكاديمية منارات</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { 
                color: #fff; 
                text-align: center;
            }
            .chat-container { 
                height: 400px; 
                border: 1px solid rgba(255,255,255,0.3); 
                border-radius: 10px; 
                padding: 15px; 
                margin: 20px 0; 
                overflow-y: auto;
                background: rgba(255,255,255,0.05);
            }
            .message { 
                margin: 10px 0; 
                padding: 10px 15px; 
                border-radius: 10px; 
                max-width: 80%;
            }
            .user-message { 
                background: rgba(76, 175, 80, 0.3); 
                margin-left: auto; 
                text-align: left;
            }
            .bot-message { 
                background: rgba(33, 150, 243, 0.3); 
                margin-right: auto;
            }
            .input-group { 
                display: flex; 
                gap: 10px; 
            }
            input { 
                flex: 1; 
                padding: 12px; 
                border: none; 
                border-radius: 5px; 
                background: rgba(255,255,255,0.9);
            }
            button { 
                padding: 12px 25px; 
                background: #4CAF50; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
            }
            .nav { 
                text-align: center; 
                margin: 20px 0; 
            }
            .nav a { 
                background: rgba(255,255,255,0.2); 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💬 المحادثة الذكية</h1>
            
            <div class="chat-container" id="chat">
                <div class="message bot-message">
                    🌅 أهلاً وسهلاً! كيف يمكنني مساعدتك اليوم؟
                </div>
            </div>
            
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="اكتب رسالتك هنا..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">إرسال</button>
            </div>
            
            <div class="nav">
                <a href="/">🏠 الرئيسية</a>
                <a href="/courses">📚 الكورسات</a>
                <a href="/pricing">💰 الأسعار</a>
            </div>
        </div>

        <script>
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (message) {
                    // إضافة رسالة المستخدم
                    const chat = document.getElementById('chat');
                    const userMessage = document.createElement('div');
                    userMessage.className = 'message user-message';
                    userMessage.textContent = message;
                    chat.appendChild(userMessage);
                    
                    // مسح الحقل
                    input.value = '';
                    
                    // إرسال للخادم
                    fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({message: message})
                    })
                    .then(response => response.json())
                    .then(data => {
                        // إضافة رد البوت
                        const botMessage = document.createElement('div');
                        botMessage.className = 'message bot-message';
                        botMessage.textContent = data.response;
                        chat.appendChild(botMessage);
                        
                        // التمرير للأسفل
                        chat.scrollTop = chat.scrollHeight;
                    });
                }
            }
        </script>
    </body>
    </html>
    """

# API للويب هوك (للاستخدام المستقبلي)
@app.route('/webhook', methods=['POST'])
def webhook():
    return jsonify({'status': 'success', 'message': 'Webhook received'})

@app.route('/set_webhook')
def set_webhook():
    return jsonify({'status': 'success', 'message': 'Webhook is ready for future use'})

# التشغيل الرئيسي
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 بدء تشغيل موقع أكاديمية منارات...")
    print("📚 جاهز لعرض الكورسات والرد على الاستفسارات!")
    app.run(host='0.0.0.0', port=port, debug=False)
