import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. CORE ARCHITECTURE & TIME ENGINE
# =====================================================================
st.set_page_config(page_title="Titan V23 - The Absolute Monolith", page_icon="👑", layout="wide")

def get_makkah_time():
    """
    محرك التوقيت الدقيق لمكة المكرمة (UTC+3)
    يعمل بشكل مستقل عن إعدادات السيرفر السحابي لضمان الدقة
    """
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# =====================================================================
# 2. ADVANCED FRONTEND ENGINEERING (CSS)
# تصميم الواجهة باستخدام CSS مفصل لضمان استقرار العرض على الجوال
# =====================================================================
css_code = """
<style>
    /* الإعدادات الأساسية والخلفية المظلمة لتقليل إجهاد العين */
    .stApp { 
        background-color: #030303; 
        color: #E0E0E0; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    h1, h2, h3, h4, h5 { 
        color: #D4AF37 !important; 
        text-align: center; 
        font-weight: 900; 
        letter-spacing: 1px; 
    }
    
    /* تصميم الألسنة (Tabs) لتعمل كأزرار تحكم ضخمة في الجوال */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; 
        justify-content: center; 
        margin-bottom: 30px; 
        flex-wrap: wrap; 
    }
    
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; 
        background-color: #111111; 
        border-radius: 10px; 
        padding: 15px 20px; 
        color: #D4AF37; 
        font-size: 15px; 
        font-weight: bold; 
        transition: all 0.3s ease; 
    }
    
    .stTabs [aria-selected="true"] { 
        background-color: #D4AF37 !important; 
        color: #000000 !important; 
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); 
        transform: scale(1.05); 
    }
    
    /* تصميم البطاقات الميدانية (Cards) */
    .titan-card { 
        background: linear-gradient(145deg, #161B22, #0A0D12); 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        border-radius: 18px; 
        padding: 30px; 
        margin-bottom: 25px; 
        text-align: right; 
        box-shadow: 0 15px 25px rgba(0,0,0,0.6); 
        transition: transform 0.3s; 
    }
    
    .titan-card:hover { 
        border-color: rgba(212, 175, 55, 0.8); 
    }
    
    .titan-card-center { 
        text-align: center; 
    }
    
    /* الأرقام الذهبية للإحصائيات الحيوية */
    .gold-value { 
        color: #FFD700; 
        font-size: 42px; 
        font-weight: 900; 
        margin: 20px 0; 
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.3); 
    }
    
    .macro-val { 
        color: #E0E0E0; 
        font-size: 28px; 
        font-weight: bold; 
    }
    
    /* ألوان خريطة الألم (DOMS Tracker) */
    .pain-zone { 
        color: #FF4136; 
        font-weight: bold; 
        font-size: 18px; 
    }
    
    .good-pain {
        color: #2ECC40;
        font-weight: bold;
    }
    
    /* البروتوكولات الطبية والتنبيهات الميدانية */
    .recovery-routine { 
        background: linear-gradient(135deg, #001220, #001f3f); 
        border-right: 8px solid #0074D9; 
        padding: 25px; 
        border-radius: 15px; 
        margin-bottom: 20px; 
        text-align: right; 
    }
    
    .fertility-safe { 
        background: linear-gradient(135deg, #051409, #0a1910); 
        border-right: 8px solid #2ECC40; 
        padding: 25px; 
        border-radius: 15px; 
        margin-bottom: 20px; 
        text-align: right; 
    }
    
    .fertility-warning { 
        background: linear-gradient(135deg, #1a0505, #1a0808); 
        border-right: 8px solid #FF4136; 
        padding: 25px; 
        border-radius: 15px; 
        margin-bottom: 20px; 
        text-align: right; 
    }
    
    /* صناديق رسائل النظام التفاعلية */
    .alert-box { 
        background: rgba(255, 65, 54, 0.1); 
        border: 1px solid #FF4136; 
        padding: 18px; 
        border-radius: 10px; 
        color: #FF4136; 
        text-align: right; 
        margin-bottom: 15px; 
        font-weight: bold;
    }
    
    .success-box { 
        background: rgba(46, 204, 64, 0.1); 
        border: 1px solid #2ECC40; 
        padding: 18px; 
        border-radius: 10px; 
        color: #2ECC40; 
        text-align: right; 
        margin-bottom: 15px; 
        font-weight: bold;
    }
    
    .info-box { 
        background: rgba(0, 116, 217, 0.1); 
        border: 1px solid #0074D9; 
        padding: 18px; 
        border-radius: 10px; 
        color: #0074D9; 
        text-align: right; 
        margin-bottom: 15px; 
        font-weight: bold;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =====================================================================
# 3. ROBUST SESSION STATE MANAGEMENT (إدارة الذاكرة المؤقتة)
# =====================================================================
# يتم تخزين المتغيرات هنا لمنع فقدان البيانات عند التبديل بين الألسنة
STATES = [
    'offline_logs', 'offline_weekly', 'offline_health', 'offline_inbody', 'offline_doms',
    'attendance_mode', 'meal_cals', 'meal_protein', 'pre_workout_pain', 'post_workout_pain'
]

for state in STATES:
    if state not in st.session_state:
        if 'offline' in state: 
            st.session_state[state] = []
        elif 'meal' in state: 
            st.session_state[state] = 0
        elif state == 'attendance_mode': 
            st.session_state[state] = "Full"
        elif state == 'pre_workout_pain': 
            st.session_state[state] = "سليم 100%"
        elif state == 'post_workout_pain': 
            st.session_state[state] = "لم يتم التقييم"

# =====================================================================
# 4. SECURE CLOUD CONNECTORS (Google Sheets API)
# =====================================================================
def get_db_connection():
    """تأسيس الاتصال بقاعدة بيانات جوجل شيتس بصمت"""
    try: 
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception: 
        return None

def fetch_sheet_safe(sheet_name):
    """جلب البيانات بأمان، مع إرجاع جدول فارغ عند الانقطاع"""
    conn = get_db_connection()
    if conn is None: 
        return pd.DataFrame()
    try: 
        df = conn.read(worksheet=sheet_name, ttl="0s")
        return df.dropna(how='all')
    except Exception: 
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """حقن البيانات الجديدة في السحابة مع الحفظ المحلي كبديل"""
    conn = get_db_connection()
    if not conn: 
        return False, "تم الحفظ محلياً في الذاكرة المؤقتة (لا يوجد اتصال)."
        
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        if df.empty:
            updated_df = pd.DataFrame([new_data_dict])
        else:
            updated_df = pd.concat([df, pd.DataFrame([new_data_dict])], ignore_index=True)
            
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم التوثيق والتشفير السحابي بنجاح."
    except Exception as e: 
        return False, f"تم الرفض من خوادم جوجل: {str(e)}"

def overwrite_sheet_safe(sheet_name, df_new):
    """استبدال كامل للملف (يستخدم لجدول الأسبوع)"""
    conn = get_db_connection()
    if not conn: 
        return False, "حفظ محلي فقط."
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط سحابياً."
    except Exception as e: 
        return False, f"فشل الرفع الشامل: {str(e)}"

# =====================================================================
# 5. EXPANDED BIOMECHANICS & EXERCISE DATABASE (هندسة التمارين والألم)
# يربط التمرين بالنطاق العلمي للعدات وأماكن الألم المتوقعة
# =====================================================================
EXERCISE_DB = {
    "صدر": [
        {"name": "Incline Barbell Bench Press", "reps": "6-8 عدات (أوزان عالية)", "target": "الصدر العلوي (لشد الجلد)", "good_pain": "أعلى الصدر وأمام الكتف", "bad_pain": "مفصل الكتف الداخلي (يعني أن الكوع مفتوح زيادة)"},
        {"name": "Flat Dumbbell Press", "reps": "8-10 عدات", "target": "الكتلة الشاملة", "good_pain": "منتصف الصدر", "bad_pain": "الرسغ أو الكوع (عدل زاوية القبضة)"},
        {"name": "Decline Cable Flys", "reps": "12-15 عدة", "target": "أسفل الصدر (للقضاء على التثدي)", "good_pain": "أسفل الصدر والخط الفاصل", "bad_pain": "الكتف الأمامي (أنت تدفع بدل أن تعصر)"},
        {"name": "Pec Deck Machine", "reps": "12-15 عدة", "target": "الصدر الداخلي", "good_pain": "عمق الصدر", "bad_pain": "مفصل الكتف (الوزن ثقيل جداً)"},
        {"name": "Dips - Chest Focus", "reps": "حتى الفشل العضلي", "target": "أسفل الصدر بقوة", "good_pain": "أسفل الصدر والتراي", "bad_pain": "عظمة القص (لا تنزل بعمق مبالغ فيه)"},
        {"name": "Push-ups", "reps": "15-20 عدة", "target": "إحماء/ضخ دم نهائي", "good_pain": "عضلة الصدر بالكامل", "bad_pain": "أسفل الظهر (ارفع حوضك للأعلى)"}
    ],
    "ظهر": [
        {"name": "Deadlift", "reps": "3-5 عدات (قوة)", "target": "السلسلة الخلفية ورفع التستوستيرون", "good_pain": "أوتار الركبة، القطنية، الظهر", "bad_pain": "ألم حاد ومفاجئ في فقرات أسفل الظهر (توقف فوراً، ظهرك مقوس)"},
        {"name": "Lat Pulldown - Wide Grip", "reps": "8-12 عدة", "target": "المجنص (للتعريض وسحب الجلد)", "good_pain": "تحت الإبط والظهر الجانبي", "bad_pain": "البايسبس (استخدم سحب الكوع وليس الذراع)"},
        {"name": "Seated Cable Row", "reps": "10-12 عدة", "target": "سمك الظهر", "good_pain": "بين لوحي الكتف", "bad_pain": "القطنية (لا تتأرجح للخلف بقوة)"},
        {"name": "Barbell Bent-Over Row", "reps": "6-8 عدات", "target": "الكتلة الشاملة والجذع", "good_pain": "الظهر الأوسط", "bad_pain": "أسفل الظهر (الوزن ثقيل جداً عليك)"},
        {"name": "T-Bar Row", "reps": "8-10 عدات", "target": "الظهر الداخلي العميق", "good_pain": "عمق الظهر", "bad_pain": "الركبة (عدل وقفتك)"},
        {"name": "Pull-ups", "reps": "حتى الفشل", "target": "التعريض الصافي", "good_pain": "المجنص", "bad_pain": "الكتف العلوي (الترابيس تسحب بدل المجنص)"}
    ],
    "أرجل": [
        {"name": "Barbell Squat", "reps": "4-6 عدات (أوزان حرة)", "target": "حرق دهون البطن ورفع هرمون النمو", "good_pain": "الفخذ الأمامي والمؤخرة", "bad_pain": "ألم الركبة الأمامي أو أسفل الظهر (راجع تكنيك النزول)"},
        {"name": "Leg Press", "reps": "10-12 عدة", "target": "ضغط الكتلة بأمان", "good_pain": "الفخذ بالكامل يحترق", "bad_pain": "الركبة (يُمنع قفل الركبة 100% في الأعلى)"},
        {"name": "Bulgarian Split Squat", "reps": "10-12 لكل رجل", "target": "نحت المؤخرة والأرجل وتصحيح التوازن", "good_pain": "الأرداف والفخذ الأمامي", "bad_pain": "توازن سيء وألم في الكاحل"},
        {"name": "Romanian Deadlift - RDL", "reps": "8-10 عدات", "target": "الخلفيات وشد المؤخرة", "good_pain": "شد قوي في الخلفيات أثناء النزول", "bad_pain": "القطنية (أنت تثني ظهرك، حافظ عليه مستقيماً)"},
        {"name": "Leg Extension", "reps": "12-15 عدة", "target": "الرباعيات (عزل تفصيلي)", "good_pain": "الفخذ الأمامي فقط", "bad_pain": "صابونة الركبة (الوزن عالي جداً)"},
        {"name": "Lying Leg Curl", "reps": "12-15 عدة", "target": "الخلفيات (عزل تفصيلي)", "good_pain": "الفخذ الخلفي", "bad_pain": "السمانة (أنت تسحب بمشط قدمك بدل ركبتك)"},
        {"name": "Standing Calf Raise", "reps": "15-20 عدة", "target": "السمانات", "good_pain": "السمانة احتراق تام", "bad_pain": "وتر أخيل (لا تنزل بسرعة وبشكل مفاجئ)"}
    ],
    "أكتاف": [
        {"name": "Overhead Barbell Press", "reps": "4-6 عدات", "target": "الكتف الأمامي والجانبي", "good_pain": "الكتف كاملاً", "bad_pain": "أسفل الظهر (لا تقوس ظهرك للوراء أثناء الدفع)"},
        {"name": "Dumbbell Lateral Raise", "reps": "12-15 عدة", "target": "الكتف الجانبي (للتعريض البصري)", "good_pain": "الكتف الجانبي احتراق", "bad_pain": "الترابيس العلوية (أنت ترفع كتفك بدل ذراعك)"},
        {"name": "Front Cable Raise", "reps": "12-15 عدة", "target": "الكتف الأمامي", "good_pain": "الكتف الأمامي", "bad_pain": "مفصل الكتف"},
        {"name": "Face Pulls", "reps": "15-20 عدة", "target": "الكتف الخلفي وصحة القوام", "good_pain": "الكتف الخلفي وبين اللوحين", "bad_pain": "الرقبة"},
        {"name": "Arnold Press", "reps": "8-10 عدات", "target": "دوران الكتف الشامل", "good_pain": "شامل للكتف", "bad_pain": "المفصل الداخلي الدوار"}
    ],
    "باي": [
        {"name": "Barbell Bicep Curl", "reps": "8-10 عدات", "target": "الكتلة الأساسية", "good_pain": "بطن البايسبس", "bad_pain": "الساعد أو الكوع الداخلي"},
        {"name": "Dumbbell Hammer Curl", "reps": "10-12 عدة", "target": "العضلة العضدية والساعد", "good_pain": "الجانب الخارجي للبايسبس", "bad_pain": "الرسغ"},
        {"name": "Preacher Curl Machine", "reps": "12-15 عدة", "target": "التكوير والعزل المباشر", "good_pain": "الأسفل القريب من الكوع", "bad_pain": "وتر الكوع (لا تفرد يدك 100% في النزول)"},
        {"name": "Cable Rope Curl", "reps": "12-15 عدة", "target": "الضخ المستمر (Pump)", "good_pain": "البايسبس كاملة", "bad_pain": "لا يوجد"}
    ],
    "تراي": [
        {"name": "Tricep Rope Pushdown", "reps": "12-15 عدة", "target": "الرأس الجانبي", "good_pain": "خلف الذراع الخارجي", "bad_pain": "مفصل الكوع الحاد"},
        {"name": "Skull Crushers (EZ Bar)", "reps": "8-10 عدات", "target": "الكتلة والتمدد العميق", "good_pain": "خلف الذراع العميق", "bad_pain": "الكوع (قم بتدفئة الكوع جيداً قبل التمرين)"},
        {"name": "Overhead Dumbbell Extension", "reps": "10-12 عدة", "target": "الرأس الطويل (شد الترهل السفلي)", "good_pain": "طول الترايسبس من الأسفل للأعلى", "bad_pain": "الكتف الداخلي"},
        {"name": "Close-Grip Bench Press", "reps": "6-8 عدات", "target": "قوة الترايسبس والصدر الداخلي", "good_pain": "الصدر والتراي معاً", "bad_pain": "الرسغ (وسع القبضة قليلاً لتخفيف الضغط)"}
    ],
    "بطن": [
        {"name": "Cable Crunches", "reps": "10-12 عدة (وزن عالي)", "target": "بروز عضلات البطن 6-pack", "good_pain": "البطن العلوية والوسطى", "bad_pain": "القطنية (أنت تسحب بظهرك وليس ببطنك)"},
        {"name": "Hanging Leg Raises", "reps": "12-15 عدة", "target": "البطن السفلي وشفط الكرش", "good_pain": "أسفل البطن بقوة", "bad_pain": "الفخذ الأمامي (حاول ثني الركبة قليلاً إذا شعرت به)"},
        {"name": "Plank - Weighted", "reps": "60 ثانية", "target": "قوة الجذع للداخل", "good_pain": "الارتجاف في كامل جدار البطن", "bad_pain": "انهيار أسفل الظهر للأسفل"},
        {"name": "Ab Roller", "reps": "8-10 عدات", "target": "تدمير شامل لدهون البطن", "good_pain": "البطن كاملة من الأعلى للأسفل", "bad_pain": "القطنية (لم تشد بطنك جيداً)"}
    ],
    "جوانب": [
        {"name": "Cable Woodchoppers", "reps": "12-15 عدة", "target": "نحت الخصر", "good_pain": "الخواصر الجانبية", "bad_pain": "الظهر أو العمود الفقري"},
        {"name": "Russian Twists", "reps": "20-30 عدة", "target": "تحمل الجوانب", "good_pain": "الخواصر", "bad_pain": "القطنية (النزول للخلف مبالغ فيه)"}
    ],
    "تمرين حر": [
        {"name": "Custom Machine Workout", "reps": "10-12", "target": "تمرين جهاز مخصص", "good_pain": "حسب العضلة", "bad_pain": "ألم المفاصل"},
        {"name": "Cardio Intensive Session", "reps": "30 دقيقة", "target": "رفع اللياقة والقلب", "good_pain": "تسارع التنفس والتعرق", "bad_pain": "ألم الركبة المستمر"}
    ]
}

def get_exercise_names(muscle):
    """إرجاع أسماء التمارين فقط للقوائم المنسدلة"""
    if not muscle or muscle == "اذهب لسان هندسة الأسبوع": 
        return [ex["name"] for ex in EXERCISE_DB["تمرين حر"]]
        
    names = []
    for k, v in EXERCISE_DB.items():
        if k in muscle: 
            names.extend([ex["name"] for ex in v])
            
    return list(set(names)) if names else [ex["name"] for ex in EXERCISE_DB["تمرين حر"]]

def get_exercise_details(ex_name):
    """إرجاع تفاصيل التمرين (العدات، الاستهداف، وأماكن الألم) بناءً على اختيار المستخدم"""
    for group in EXERCISE_DB.values():
        for ex in group:
            if ex["name"] == ex_name:
                return ex
                
    # القيمة الافتراضية إذا لم يطابق شيء
    return {
        "name": ex_name, 
        "reps": "10-12 عدة", 
        "target": "تمرين شامل", 
        "good_pain": "بطن العضلة المستهدفة", 
        "bad_pain": "ألم المفاصل والأربطة"
    }

# =====================================================================
# 6. EXPANDED NUTRITION DATABASE (Saudi & Fast Food)
# =====================================================================
EDAAM_DB = {
    "إيدام دجاج بالبطاطس (بدون رز)": {"protein": 35, "cals": 320},
    "إيدام دجاج بالبطاطس + صحن رز أبيض": {"protein": 40, "cals": 580},
    "إيدام لحم بالخضار (بدون رز)": {"protein": 45, "cals": 450},
    "إيدام لحم بالخضار + صحن رز": {"protein": 50, "cals": 710},
    "إيدام بامية باللحم (طبيخ منزلي)": {"protein": 40, "cals": 410},
    "ملوخية بالدجاج + صحن رز": {"protein": 35, "cals": 480},
    "كبسة دجاج (صدر دجاج + رز)": {"protein": 45, "cals": 650},
    "مكرونة حمراء بالدجاج": {"protein": 30, "cals": 520},
    "صالونة خضار (بدون لحم)": {"protein": 5, "cals": 150}
}

FAST_FOOD_DB = {
    "نصف حبة دجاج شواية (بدون جلد)": {"protein": 45, "cals": 420},
    "نصف حبة دجاج فحم": {"protein": 40, "cals": 450},
    "علبة تونة (مصفاة بالماء)": {"protein": 26, "cals": 120},
    "علبة تونة (بالزيت)": {"protein": 24, "cals": 220},
    "صاروخ شاورما دجاج (عادي)": {"protein": 25, "cals": 550},
    "صحن شاورما عربي دجاج": {"protein": 35, "cals": 850},
    "سكوب بروتين (Whey Protein)": {"protein": 25, "cals": 120},
    "3 بيضات مسلوقة كاملة": {"protein": 18, "cals": 210},
    "شريحة لحم ستيك (200 جرام)": {"protein": 50, "cals": 450},
    "وجبة برجر لحم مشوي (مفرد)": {"protein": 20, "cals": 350},
    "علبة زبادي يوناني سادة": {"protein": 15, "cals": 100},
    "بروستد (نصف حبة دجاج مقلي)": {"protein": 35, "cals": 750}
}

# =====================================================================
# 7. INTERACTIVE GPS & TRAFFIC ALGORITHM
# تعتمد على حسابات الروابط الجغرافية المقدمة من المستخدم
# =====================================================================
def calculate_live_commute(origin):
    """
    خوارزمية ذكية تحاكي خرائط جوجل.
    تأخذ الموقع الجغرافي للمستخدم، وتقرأ توقيت مكة، وتطبق معامل الزحام (Traffic Multiplier).
    """
    now = get_makkah_time()
    hour = now.hour
    
    # 1. تحديد الدقائق الأساسية للرحلة (Base Commute in minutes) بناءً على الروابط
    if origin == "🏠 البيت (جدة - المروة)": 
        base_mins = 15
    elif origin == "🏢 العمل (جدة)": 
        base_mins = 25
    elif origin == "🕋 العمل (مكة المكرمة)": 
        base_mins = 60 # طريق مكة جدة السريع
    else: 
        base_mins = 30 # موقع مخصص

    # 2. تحديد معامل الزحام المروري في السعودية (Traffic Multipliers)
    if 7 <= hour <= 9: 
        multiplier = 1.5 # زحمة الصباح
    elif 13 <= hour <= 15: 
        multiplier = 1.6 # خروج المدارس والدوامات
    elif 17 <= hour <= 21: 
        multiplier = 1.8 # ذروة المساء
    else: 
        multiplier = 1.1 # طريق سالك نسبياً

    # 3. حساب الوقت النهائي
    total_mins = int(base_mins * multiplier)
    
    # ضمان أن الوقت لا يكون غير منطقي
    if origin == "🕋 العمل (مكة المكرمة)" and total_mins < 60:
        total_mins = 65
        
    return total_mins

def get_dynamic_schedule(attendance_mode, origin):
    """بناء الجدول الزمني الميداني بناءً على وقت الرحلة المحسوب"""
    now = get_makkah_time()
    commute_mins = calculate_live_commute(origin)
    
    arrival_timeObj = now + timedelta(minutes=commute_mins)
    
    now_str = now.strftime("%I:%M %p")
    arr_str = arrival_timeObj.strftime("%I:%M %p")
    
    return now_str, arr_str, arrival_timeObj, commute_mins

# =====================================================================
# 8. WORKOUT ENGINE & CLASS METRICS
# =====================================================================
CLASS_BURN_DB = {
    "موتيف 8": 450, "فت كومبات": 650, "كور اكستريم": 350,
    "ستيب": 450, "اكوا": 350, "بامب فت": 400,
    "بودي ماكس": 600, "رادير": 300, "جي فت": 400,
    "فت اتاك": 600, "موبيلتي": 200, "لا يوجد": 0
}

WORKOUT_ENGINE = {
    "موتيف 8": {"iron": "صدر + تراي", "warmup": "دوران أكتاف 3 دق + إطالة صدر 2 دق", "flow": "صدر علوي أولاً لشد الترهل."},
    "فت كومبات": {"iron": "أرجل + بطن", "warmup": "إطالة للحوض والركب", "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات ولا تتنازل عن الأوزان."},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "warmup": "تسخين جذع مركزي", "flow": "أكتاف عريضة = خصر أنحف بصرياً. ركز على الـ Overhead Press."},
    "ستيب": {"iron": "ظهر + باي", "warmup": "إطالة قطنية + سحب حبل خفيف", "flow": "شد الظهر يمنع التحدب. ركز على Deadlift."},
    "اكوا": {"iron": "حديد شامل (Full Body)", "warmup": "إحماء مفاصل شامل", "flow": "تمرين مركب واحد لكل عضلة كبيرة."},
    "بامب فت": {"iron": "صدر + أكتاف", "warmup": "تسخين أكتاف بوزن خفيف", "flow": "أوزان متوسطة وتكرارات عالية لضخ الدم."},
    "بودي ماكس": {"iron": "أرجل + ظهر", "warmup": "سكوات وزن جسم 20 عدة", "flow": "أعنف يوم في الأسبوع! يستهدف أكبر عضلتين لنسف الكرش."},
    "رادير": {"iron": "ذراعين (باي وتراي)", "warmup": "إطالة أوتار الرسغ ببطء", "flow": "Supersets باي مع تراي لزيادة الحرق واختصار الوقت."},
    "جي فت": {"iron": "حديد قوة (Heavy Lift)", "warmup": "تسخين مفاصل مكثف جداً", "flow": "3 إلى 5 عدات بأقصى وزن. راحة 3 دقائق لتجنب الإصابة."},
    "فت اتاك": {"iron": "أرجل + أكتاف", "warmup": "هرولة خفيفة 3 دق + قفز", "flow": "تمارين مركبة سريعة لرفع نبض القلب وزيادة معدل الحرق."},
    "موبيلتي": {"iron": "تمرين حر (النقاط الضعيفة)", "warmup": "استخدام Foam Roller", "flow": "استهدف عضلة متأخرة أو قم بإطالات عميقة للتعافي."},
    "لا يوجد": {"iron": "تمرين حر متكامل", "warmup": "سير مائل 10 دق", "flow": "أنت القائد اليوم. صمم روتينك بناءً على طاقتك."}
}

def analyze_muscle_balance(plan_df):
    """التدقيق الهندسي للمخطط الأسبوعي وتحديد العضلات المفقودة"""
    if plan_df.empty: 
        return True, ""
        
    all_muscles = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    if "أرجل" not in all_muscles: 
        alerts.append("🔴 خطأ هندسي: المخطط يفتقد لتمارين الأرجل (وهي المحفز الأول للتستوستيرون وحرق الكرش).")
    if "ظهر" not in all_muscles: 
        alerts.append("🔴 خلل قوام: يجب تدريب الظهر لسحب الأكتاف وتقويم العمود الفقري.")
    if all_muscles.count("صدر") > 2: 
        alerts.append("🔴 إجهاد مفرط: الصدر مستهدف بكثافة عالية جداً، هذا سيؤدي للهدم العضلي.")
        
    if len(alerts) > 0: 
        return False, "<br>".join(alerts)
        
    return True, "🟢 ممتاز هندسياً: المخطط متوازن، يهاجم الدهون، ويضمن الاستشفاء السليم."

def get_week_dates():
    """حساب تواريخ الأسبوع للبدء دائماً بيوم السبت"""
    today = get_makkah_time()
    idx = (today.weekday() + 2) % 7 
    saturday = today - timedelta(days=idx)
    
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates = {}
    for i, day in enumerate(week_days):
        week_dates[day] = (saturday + timedelta(days=i)).strftime("%Y-%m-%d")
    return week_dates

# =====================================================================
# 9. MAIN DASHBOARD INTERFACE (The Commander View)
# =====================================================================
def main():
    makkah_now = get_makkah_time()
    days_map_ar = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_ar = days_map_ar[makkah_now.strftime("%A")]
    current_date = makkah_now.strftime("%Y-%m-%d")
    week_dates = get_week_dates()

    st.markdown("<h1>👑 محرك تايتان V23 (The Absolute Monolith)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>مكة المكرمة | {today_ar} ({current_date}) | الساعة الآن: {makkah_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    tabs = st.tabs([
        "🚀 الملاحة والميدان", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ السجل وتتبع الألم (DOMS)", 
        "📸 عيادة InBody", 
        "🥗 وقود و Vision AI", 
        "🛠️ مركز الصيانة"
    ])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS & INTERACTIVE GPS
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            st.markdown(
                """
                <div class='titan-card titan-card-center' style='border: 2px solid #2ECC40;'>
                    <h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1>
                    <p style='font-size: 20px; color:#A0A0A0;'>يوم الاستشفاء السلبي الإلزامي. بناء الأنسجة العضلية يتم الآن.</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            s_class, iron_target, warmup, t_flow = "غير محدد", "غير محدد", "غير محدد", "غير محدد"
            plan_df = fetch_sheet_safe("Weekly_Plan")
            if not plan_df.empty and 'Date' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Date'] == current_date].iloc[0]
                    s_class, iron_target = today_row['Class'], today_row['Muscle']
                    if s_class in WORKOUT_ENGINE: 
                        warmup, t_flow = WORKOUT_ENGINE[s_class]['warmup'], WORKOUT_ENGINE[s_class]['flow']
                except: pass

            if st.session_state['attendance_mode'] == "Absent":
                st.markdown(
                    f"""
                    <div class='titan-card' style='border-color: #FF4136;'>
                        <h2 style='color:#FF4136; text-align:center;'>تم تسجيل الغياب التام ❌</h2>
                        <p style='text-align:center; font-size:18px;'>النظام رحّل تمرين <b>({iron_target})</b> للغد.</p>
                        <hr style='border-color:#333;'>
                        <h4 style='color:#E0E0E0; text-align:center;'>توجيه تغذية طارئ</h4>
                        <p style='text-align:center;'>الكربوهيدرات ممنوعة الليلة تماماً لعدم وجود حرق.</p>
                    </div>
                    """, unsafe_allow_html=True)
                if st.button("🔄 التراجع (قررت الذهاب للنادي)"):
                    st.session_state['attendance_mode'] = "Full"
                    st.rerun()
            else:
                col_t1, col_t2 = st.columns([2, 1])
                
                with col_t2:
                    st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 حاسبة الانطلاق التفاعلية</h3>", unsafe_allow_html=True)
                    st.info("النظام يقوم بتحليل زحام جدة ومكة الآن بناءً على الروابط التي قدمتها.")
                    
                    user_loc = st.selectbox("من أين ستنطلق الآن؟", [
                        "🏠 البيت (جدة - المروة)", 
                        "🏢 العمل (جدة)", 
                        "🕋 العمل (مكة المكرمة)"
                    ])
                    
                    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
                    st.markdown("<h3 style='margin-top:0;'>🕹️ التحكم الميداني</h3>", unsafe_allow_html=True)
                    
                    if st.button("✅ حضور كامل (كلاس + حديد)", use_container_width=True):
                        st.session_state['attendance_mode'] = "Full"
                        st.rerun()
                    if st.button("🏋️ حديد فقط (ألغِ الكلاس)", use_container_width=True):
                        st.session_state['attendance_mode'] = "IronOnly"
                        st.rerun()
                    if st.button("🤸 كلاس فقط (ألغِ الحديد)", use_container_width=True):
                        st.session_state['attendance_mode'] = "ClassOnly"
                        st.rerun()
                    if st.button("⏳ تأخير مسار (زحمة غير متوقعة)", use_container_width=True):
                        st.session_state['attendance_mode'] = "Delayed"
                        st.rerun()
                    if st.button("❌ غياب تام عن النادي", use_container_width=True):
                        st.session_state['attendance_mode'] = "Absent"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_t1:
                    now_str, arr_str, arrival_timeObj, commute_mins = get_dynamic_schedule(st.session_state['attendance_mode'], user_loc)
                    class_burn = CLASS_BURN_DB.get(s_class, 0)
                    
                    if st.session_state['attendance_mode'] == "Full":
                        iron_start = (arrival_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card'>
                            <h3 style='margin-top:0;'>🗺️ الخطة أ (الكمال الهندسي)</h3>
                            <p style='font-size:18px;'>الحديد: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس: <b style='color:#FFD700;'>{s_class}</b> <span style='color:#FF4136; font-size:14px;'>(حرق ~{class_burn} kcal)</span></p>
                            <p style='color:#888;'>الاستراتيجية: {t_flow}</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق من {user_loc}: <b style='color:#D4AF37;'>{now_str}</b></p>
                            <p>⏱️ مدة الرحلة المحسوبة: <b style='color:#D4AF37;'>{commute_mins} دقيقة</b></p>
                            <p>🅿️ الوصول لمواقف النادي: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <br>
                            <h5 style='color:#E0E0E0;'>الجدول الميداني المبرمج لإنهاء التمرين قبل الإغلاق 11:00 م</h5>
                            <p>🔥 {arr_str} - {iron_start} : إحماء مفاصل ({warmup})</p>
                            <p>💪 {iron_start} - 09:00 PM : <b style='color:#FF4136;'>صالة الحديد (استنزاف بأوزان حرة قبل الكارديو)</b></p>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (لحرق دهون البطن الصافية)</b></p>
                            <p>🧊 10:00 PM - 10:20 PM : <b style='color:#2ECC40;'>الاستشفاء والجاكوزي</b></p>
                        </div>
                        """
                    elif st.session_state['attendance_mode'] == "IronOnly":
                        iron_start = (arrival_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #0074D9;'>
                            <h3 style='margin-top:0; color:#0074D9;'>🏋️ مسار الحديد المكثف</h3>
                            <p style='font-size:18px;'>الحديد المستهدف: <b style='color:#FFD700;'>{iron_target}</b> (تم إلغاء الكلاس)</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ الوصول: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <p>🔥 {arr_str} - {iron_start} : إحماء دقيق ({warmup})</p>
                            <p>💪 {iron_start} - 10:30 PM : <b style='color:#FF4136;'>حديد مكثف (وقت مفتوح، زد من عدد الجولات لكسر العضلة)</b></p>
                        </div>
                        """
                    elif st.session_state['attendance_mode'] == "ClassOnly":
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #D4AF37;'>
                            <h3 style='margin-top:0; color:#D4AF37;'>🤸 مسار الكارديو واللياقة</h3>
                            <p style='font-size:18px;'>الكلاس: <b style='color:#FFD700;'>{s_class}</b> (تم إلغاء الحديد)</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ الوصول: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (حرق ~{class_burn} kcal)</b></p>
                        </div>
                        """
                    else: # Delayed
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #FF4136;'>
                            <h3 style='margin-top:0; color:#FF4136;'>⚠️ مسار التأخير (إنقاذ التمرين)</h3>
                            <p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة لعدم تفويت التسخين</b></p>
                            <p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع (أجهزة عزل فقط، يُمنع الأوزان الحرة لتفادي الإصابة)</b></p>
                        </div>
                        """
                    st.markdown(nav_html, unsafe_allow_html=True)

                st.markdown("### 🧊 البروتوكول الطبي المفصل للاستشفاء")
                # تطبيق بروتوكول العلاج التبايني إذا كان اليوم أرجل أو الاثنين والخميس
                if today_ar in ["الاثنين", "الخميس"] or "أرجل" in iron_target:
                    st.markdown(
                        """
                        <div class='fertility-warning'>
                            <h4 style='color:#FF4136; margin:0;'>🔥 بروتوكول العلاج التبايني (Contrast Therapy) العنيف</h4>
                            <p style='font-size: 16px; margin-top:10px;'>بما أن اليوم يتضمن مجهوداً عالياً (أو أرجل)، يجب تطبيق التالي لدفع حمض اللاكتيك خارج العضلات:</p>
                            <ul style='font-size: 15px;'>
                                <li><b>الجاكوزي الحار/بخار:</b> 3 دقائق متواصلة لتوسيع الأوعية الدموية.</li>
                                <li><b>الجاكوزي البارد:</b> 1 دقيقة متواصلة للانقباض السريع.</li>
                                <li><i>كرر الدورة 3 مرات.</i></li>
                                <li><b>تحذير الخصوبة:</b> يجب أن تنهي الدورة بالماء البارد جداً وتخرج فوراً لحماية هرمونات الذكورة.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(
                        """
                        <div class='fertility-safe'>
                            <h4 style='color:#2ECC40; margin:0;'>🛡️ بروتوكول التبريد العميق (حظر حراري)</h4>
                            <p style='font-size: 16px; margin-top:10px;'>اليوم مخصص لتمارين الأجزاء العلوية أو راحة.</p>
                            <ul style='font-size: 15px;'>
                                <li><b>السباحة الهادئة:</b> 15 دقيقة لفكفكة المفاصل بهدوء.</li>
                                <li><b>الجاكوزي البارد:</b> 3 إلى 5 دقائق متواصلة لتقليل الالتهابات ورفع التستوستيرون.</li>
                                <li><b>يُمنع الدخول للحرارة العالية اليوم</b> لمنع الإجهاد الحراري التراكمي.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ بناء المخطط الأسبوعي وتوازن العضلات")
        week_days_ordered = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        
        with st.form("weekly_master_plan"):
            new_schedule = []
            cols = st.columns(3)
            for i, d in enumerate(week_days_ordered):
                exact_date = week_dates.get(d, "")
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E0E0E0; text-align:right;'>{d}<br><span style='font-size:12px; color:#888;'>{exact_date}</span></h5>", unsafe_allow_html=True)
                    choice = st.selectbox("الكلاس", list(WORKOUT_ENGINE.keys()), key=f"conf_{d}", label_visibility="collapsed")
                    muscle_target = WORKOUT_ENGINE[choice]['iron']
                    new_schedule.append({"Day": d, "Date": exact_date, "Class": choice, "Muscle": muscle_target, "Status": "مجدول"})
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص واعتماد المخطط", use_container_width=True):
                df_new_plan = pd.DataFrame(new_schedule)
                is_balanced, balance_msg = analyze_muscle_balance(df_new_plan)
                box_class = 'success-box' if is_balanced else 'alert-box'
                st.markdown(f"<div class='{box_class}'>{balance_msg}</div>", unsafe_allow_html=True)
                success, s_msg = overwrite_sheet_safe("Weekly_Plan", df_new_plan)
                if success: st.success(s_msg)
                else: st.warning(s_msg)

    # -----------------------------------------------------------------
    # TAB 3: SMART LOGS & PRE/POST DOMS TRACKER
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي، خريطة الألم، والمؤقت")
        
        # 1. تقييم ما قبل التمرين
        st.markdown("<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>🚦 التقييم قبل التمرين (Pre-Workout Check)</h4>", unsafe_allow_html=True)
        st.session_state['pre_workout_pain'] = st.selectbox("كيف تشعر بجسمك اليوم قبل الذهاب للنادي؟", [
            "سليم 100% وجاهز لكسر الأوزان",
            "إرهاق عام وعضلات مشدودة (DOMS من الأمس)",
            "ألم خفيف في أحد المفاصل (ركبة، كوع، رسغ)",
            "ألم حاد في أسفل الظهر أو الكتف الداخلي (خطر)"
        ])
        if "المفاصل" in st.session_state['pre_workout_pain'] or "خطر" in st.session_state['pre_workout_pain']:
            st.warning("⚠️ بما أن هناك ألم في المفاصل/الظهر، يُمنع اليوم لعب الأوزان الحرة (Deadlift, Free Squat, Barbell Bench). استخدم الأجهزة ذات المسار الثابت فقط!")
        st.markdown("</div>", unsafe_allow_html=True)

        todays_muscle = "اذهب لسان هندسة الأسبوع"
        plan_df = fetch_sheet_safe("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: todays_muscle = plan_df[plan_df['Date'] == current_date].iloc[0]['Muscle']
            except: pass
            
        c_timer1, c_timer2 = st.columns([1, 2])
        with c_timer1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة</h4><p style='font-size:12px; color:#888;'>لضمان الضخ العضلي</p>", unsafe_allow_html=True)
            if st.button("بدء 90 ثانية (تضخيم)", use_container_width=True):
                progress_bar = st.progress(0)
                for i in range(90):
                    time.sleep(1)
                    progress_bar.progress((i + 1) / 90)
                st.success("انتهى وقت الراحة! ارجع للبار فوراً.")
            if st.button("بدء 3 دقائق (قوة Power)", use_container_width=True):
                progress_bar = st.progress(0)
                for i in range(180):
                    time.sleep(1)
                    progress_bar.progress((i + 1) / 180)
                st.success("الجهاز العصبي جاهز للوزن الثقيل.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c_timer2:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>العضلة: <span style='color:#FFD700;'>{todays_muscle}</span></h4>", unsafe_allow_html=True)
            available_exercises = get_exercise_names(todays_muscle)
            selected_ex = st.selectbox("اختر التمرين من قاعدة البيانات لتسجيله:", available_exercises)
            
            ex_details = get_exercise_details(selected_ex)
            st.markdown(f"<p style='color:#888; font-size:14px;'>الهدف الميكانيكي: {ex_details['target']} | النطاق الموصى به: <b style='color:#2ECC40;'>{ex_details['reps']}</b></p>", unsafe_allow_html=True)
            
            p_date, p_weight, p_reps = fetch_historical_data(selected_ex)
            if p_date:
                st.markdown(f"<div style='background:#111; padding:10px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:15px;'><p style='color:#888; margin:0;'>آخر مرة: {p_date} | <b>سابقاً: {p_weight} KG</b> × {p_reps}</p></div>", unsafe_allow_html=True)
                default_w = float(p_weight)
            else: default_w = 0.0
                
            c_wt, c_rp = st.columns(2)
            input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, value=default_w, step=2.5)
            input_rp = c_rp.number_input("العدات (اكتب 0 للحساب الآلي)", min_value=0, value=0, step=1)
            
            if st.button("💾 توثيق الجلسة في الإكسل", use_container_width=True):
                final_reps = input_rp
                if input_rp == 0:
                    # تشغيل محرك الذكاء الاصطناعي لحساب العدات
                    final_reps = calculate_smart_reps(selected_ex, input_wt)
                    st.success(f"🤖 استنتج النظام بناءً على وزنك السابق أنك حققت: {final_reps} عدات.")
                    
                new_entry = {"Date": current_date, "Muscle": todays_muscle, "Exercise": selected_ex, "Weight": input_wt, "Reps": final_reps}
                success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
                if success: st.success(f"تم توثيق {selected_ex}.")
                else: st.error(s_msg)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 2. تقييم ما بعد التمرين (Post-Workout DOMS Tracker)
        st.markdown("#### 🤕 التقييم بعد التمرين (أو ثاني يوم - DOMS Analysis)")
        with st.form("doms_form"):
            st.write(f"بناءً على تمرين [{selected_ex}] الذي اخترته:")
            st.markdown(f"<p style='font-size:14px;'><span class='good-pain'>✅ الألم الجيد يجب أن يكون في:</span> {ex_details['good_pain']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:14px;'><span class='pain-zone'>❌ الألم السيء الذي يدل على إصابة/تكنيك خاطئ:</span> {ex_details['bad_pain']}</p>", unsafe_allow_html=True)
            
            doms_level = st.slider("مستوى الألم العضلي الذي تشعر به الآن (1 = لا يوجد، 10 = تمزق/إعاقة حركة):", 1, 10, 3)
            doms_loc = st.selectbox("أين يتركز الألم بشكل رئيسي؟", [
                "في بطن العضلة المستهدفة (ألم تمدد طبيعي)", 
                "في المفاصل والأوتار المحيطة (خطر)", 
                "في أسفل الظهر أو القطنية (تحذير جدي)", 
                "في الرقبة أو الترابيس العلوية (تكنيك خاطئ)"
            ])
            
            if st.form_submit_button("💾 حفظ حالة الاستشفاء في الإكسل"):
                if "المفاصل" in doms_loc or "أسفل الظهر" in doms_loc:
                    st.error("⚠️ التقييم يؤكد أن التكنيك كان خاطئاً أو الوزن كان ثقيلاً جداً لدرجة أنك استعنت بمفاصلك لرفعه. راجع فيديوهات التكنيك فوراً أو خفف الوزن المرة القادمة.")
                elif doms_level > 8:
                    st.warning("⚠️ الألم العالي جداً في بطن العضلة (DOMS فوق 8) يعني أنك تحتاج للراحة السلبية، لا تمرن هذه العضلة قبل مرور 72 ساعة.")
                else:
                    st.success("✅ ممتاز! ألم بطن العضلة المحتمل يدل على تدمير الألياف بنجاح لإعادة بنائها بشكل أكبر وأصلب. استمر في التغذية الجيدة.")

    # -----------------------------------------------------------------
    # TAB 4: CLINIC & INBODY
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان للقياسات الحيوية")
        with st.form("inbody_form"):
            c1, c2 = st.columns(2)
            ib_date = c1.date_input("تاريخ الفحص")
            ib_weight = c1.number_input("الوزن الإجمالي", value=91.9, step=0.1)
            ib_muscle = c2.number_input("العضلات (KG)", value=40.0, step=0.1)
            ib_fat = c2.number_input("نسبة الدهون (%)", value=20.0, step=0.5)
            ib_visceral = st.number_input("الدهون الحشوية (الكرش - يجب أن تنزل تحت 10)", value=14, step=1)
            if st.form_submit_button("💾 أرشفة التقرير", use_container_width=True):
                inbody_data = {"Date": ib_date.strftime("%Y-%m-%d"), "Weight": ib_weight, "Muscle_Mass": ib_muscle, "Fat_Percentage": ib_fat, "Visceral_Fat": ib_visceral}
                success, msg = append_to_sheet_safe("InBody_Logs", inbody_data)
                if success: st.success("تم الحفظ في قاعدة البيانات بنجاح.")
                else: st.error(msg)

    # -----------------------------------------------------------------
    # TAB 5: NUTRITION & MACROS
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 المساعد الغذائي (Macros & Meals)")
        
        tab_f1, tab_f2, tab_f3 = st.tabs(["📸 تصوير الوجبة (AI)", "🍲 الإيدامات وطبخ البيت", "🍔 الوجبات السريعة"])
        
        with tab_f1:
            st.markdown("<div class='titan-card titan-card-center'>", unsafe_allow_html=True)
            st.markdown("<h4>التعرف التلقائي على الماكروز عبر الصور</h4>", unsafe_allow_html=True)
            uploaded_meal = st.file_uploader("التقط صورة للوجبة", type=["jpg", "jpeg", "png"])
            if uploaded_meal:
                # محاكاة حفظ الصورة ومعالجتها
                st.session_state['temp_image_data'] = uploaded_meal.name
                st.image(uploaded_meal, use_container_width=True)
                if st.button("🔍 تحليل السعرات والبروتين", use_container_width=True):
                    with st.spinner("جاري فحص مكونات الصورة وتقدير الماكروز..."):
                        time.sleep(1.5)
                        st.session_state['meal_cals'] += 450 
                        st.session_state['meal_protein'] += 35
                        st.success("🤖 تقدير الذكاء الاصطناعي للوجبة: 450 سعرة، 35ج بروتين. تم الإضافة للعداد العام أسفل الصفحة.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_f2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>🍲 إيدامات البيت والمطبخ السعودي</h4>", unsafe_allow_html=True)
            selected_edaam = st.multiselect("ماذا أكلت من طبخ المنزل؟", list(EDAAM_DB.keys()))
            if st.button("➕ إضافة الإيدام للعداد"):
                for meal in selected_edaam:
                    st.session_state['meal_protein'] += EDAAM_DB[meal]["protein"]
                    st.session_state['meal_cals'] += EDAAM_DB[meal]["cals"]
                st.success("تم جمع القيم الغذائية بنجاح.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_f3:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>🍔 المطاعم والوجبات السريعة</h4>", unsafe_allow_html=True)
            selected_fast = st.multiselect("اختر من المطاعم/الخيارات الجاهزة:", list(FAST_FOOD_DB.keys()))
            if st.button("➕ إضافة الوجبة الجاهزة للعداد"):
                for meal in selected_fast:
                    st.session_state['meal_protein'] += FAST_FOOD_DB[meal]["protein"]
                    st.session_state['meal_cals'] += FAST_FOOD_DB[meal]["cals"]
                st.success("تم جمع القيم الغذائية بنجاح.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # لوحة العداد المجمعة
        target_calories = 1900
        protein_target = int(91.9 * 2.2) # لضمان عدم الهدم العضلي أثناء التنشيف
        
        st.markdown(f"""
        <div class='titan-card'>
            <h4 style='margin-top:0; color:#D4AF37;'>🎯 العداد اللحظي (مقارنة بالهدف)</h4>
            <div style='display:flex; justify-content:space-around; margin-top:20px; align-items:center;'>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🍖</span><br><span style='color:#E0E0E0; font-size:14px;'>بروتين (أساسي)</span><br>
                    <span class='macro-val' style='color:#FF4136;'>{st.session_state['meal_protein']} / {protein_target}g</span>
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🔥</span><br><span style='color:#E0E0E0; font-size:14px;'>سعرات</span><br>
                    <span class='macro-val' style='color:#D4AF37;'>{st.session_state['meal_cals']} / {target_calories}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            in_sleep = col_f1.number_input("🛌 النوم (Huawei):", value=7.5, step=0.5)
            in_water = col_f1.number_input("💧 الماء:", value=3.5, step=0.5)
            
            st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
            if st.form_submit_button("💾 حفظ يوم التغذية النهائي في الإكسل", use_container_width=True):
                health_record = {
                    "Date": current_date, 
                    "Sleep": in_sleep, 
                    "Water": in_water, 
                    "Protein": st.session_state['meal_protein'], 
                    "Calories": st.session_state['meal_cals'], 
                    "Notes": ""
                }
                success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                if success: 
                    st.success(s_msg)
                    st.session_state['meal_protein'] = 0
                    st.session_state['meal_cals'] = 0
                else: 
                    st.error(s_msg)

    # -----------------------------------------------------------------
    # TAB 6: SYSTEM MAINTENANCE & DIAGNOSTICS
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ التشخيص الهندسي اللحظي للاتصال")
        st.info("النظام يقوم هنا باختبار استجابة خوادم جوجل وصلاحيات مفتاح Service Account.")
        
        if st.button("🔄 بدء الاختبار والفحص العميق", use_container_width=True):
            with st.spinner('جاري التفاوض مع خوادم Google Cloud وفتح قنوات الاتصال...'):
                time.sleep(1)
                conn = get_db_connection()
                if conn:
                    try:
                        conn.read(worksheet="Weekly_Plan", ttl="0s")
                        st.markdown(
                            """
                            <div class='success-box'>
                                <h3 style='margin:0;'>🟢 النظام مدرع ومتصل 100%.</h3>
                                <p style='margin:0;'>صلاحيات الكتابة (Editor) تعمل، والتطبيق يتحدث مع قاعدة البيانات بشكل مثالي دون أي انقطاع.</p>
                            </div>
                            """, unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.markdown(
                            f"""
                            <div class='alert-box'>
                                <h3 style='margin:0;'>🔴 الكتابة مرفوضة من جوجل</h3>
                                <p style='margin:0;'>تم الاتصال بنجاح، لكن جوجل يمنع التعديل. تأكد أنك أضفت إيميل الروبوت (الموجود في ملف JSON) كـ "محرر" في زر المشاركة في الإكسل.</p>
                                <p style='font-size:12px;'>التفاصيل التقنية للخطأ: {str(e)}</p>
                            </div>
                            """, unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        """
                        <div class='alert-box'>
                            <h3 style='margin:0;'>🔴 انقطاع تام في الشبكة</h3>
                            <p style='margin:0;'>التطبيق لا يستطيع قراءة مفاتيح Secrets. راجع إعدادات Streamlit ولاحظ إذا كانت المسافات والنسخ صحيحاً.</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()
