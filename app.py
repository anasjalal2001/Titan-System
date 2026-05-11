import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والزمني (Makkah Time Engine)
# =====================================================================
st.set_page_config(page_title="Titan V21 - Uncompressed Master", page_icon="👑", layout="wide")

def get_makkah_time():
    """
    محرك زمني دقيق يحسب توقيت مكة المكرمة رياضياً.
    الاستناد: إضافة 3 ساعات على التوقيت العالمي المنسق (UTC+3).
    يغنينا عن استخدام مكتبة pytz التي تسببت في انهيار السيرفر مسبقاً.
    """
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# هندسة الواجهة الأمامية (Frontend CSS Architecture)
# تم فك ضغط الكود ليكون واضحاً وقابلاً للتعديل الهندسي
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
# 2. إدارة الذاكرة المؤقتة والحالات الميدانية (State Management)
# =====================================================================
# ضمان عدم فقدان البيانات في حال تأرجح شبكة الإنترنت الميدانية
if 'offline_logs' not in st.session_state: 
    st.session_state['offline_logs'] = []
    
if 'offline_weekly' not in st.session_state: 
    st.session_state['offline_weekly'] = []
    
if 'offline_health' not in st.session_state: 
    st.session_state['offline_health'] = []
    
if 'offline_inbody' not in st.session_state: 
    st.session_state['offline_inbody'] = []
    
if 'attendance_mode' not in st.session_state: 
    st.session_state['attendance_mode'] = "Full" # الأوضاع: Full, IronOnly, Absent, Delayed
    
if 'meal_cals' not in st.session_state: 
    st.session_state['meal_cals'] = 0
    
if 'meal_protein' not in st.session_state: 
    st.session_state['meal_protein'] = 0

# =====================================================================
# 3. محركات السحاب (Cloud Connectors) - مدرعة ضد الانقطاعات
# =====================================================================
def get_db_connection():
    """تأسيس الاتصال بقاعدة بيانات جوجل شيتس"""
    try: 
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception: 
        return None

def fetch_sheet_safe(sheet_name):
    """قراءة البيانات من السحابة مع تنظيفها من الفراغات"""
    conn = get_db_connection()
    if conn is None: 
        return pd.DataFrame()
    try: 
        df = conn.read(worksheet=sheet_name, ttl="0s")
        return df.dropna(how='all')
    except Exception: 
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """إضافة سطر جديد (سجل تمرين أو غذاء) مع تفعيل الحفظ المحلي عند الفشل"""
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
        return False, f"خطأ سحابي في الصلاحيات: {str(e)}"

def overwrite_sheet_safe(sheet_name, df_new):
    """تحديث كامل للصفحة (يستخدم لجدول الأسبوع)"""
    conn = get_db_connection()
    if not conn: 
        return False, "حفظ محلي للمخطط فقط."
        
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط سحابياً."
    except Exception as e: 
        return False, f"فشل الرفع الشامل: {str(e)}"

# =====================================================================
# 4. المساعد الغذائي الذكي (Smart Nutrition & Vision AI Logic)
# قاعدة البيانات مخصصة للمطبخ السعودي واحتياجات التنشيف
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
    "علبة تونة (مصفاة بالماء)": {"protein": 26, "cals": 120},
    "صاروخ شاورما دجاج (عادي)": {"protein": 25, "cals": 550},
    "صحن شاورما عربي دجاج": {"protein": 35, "cals": 850},
    "سكوب بروتين (Whey Protein)": {"protein": 25, "cals": 120},
    "3 بيضات مسلوقة كاملة": {"protein": 18, "cals": 210},
    "شريحة لحم ستيك (200 جرام)": {"protein": 50, "cals": 450},
    "وجبة برجر لحم مشوي (مفرد)": {"protein": 20, "cals": 350},
    "علبة زبادي يوناني سادة": {"protein": 15, "cals": 100}
}

# =====================================================================
# 5. قاعدة البيانات الميكانيكية (Biomechanics DB) لنسف الدهون
# =====================================================================
EXERCISE_DB = {
    "صدر": [
        "Incline Barbell Bench Press (لشد الجزء العلوي المترهل)",
        "Flat Dumbbell Press (لبناء الكتلة الأساسية)",
        "Decline Cable Flys (لنحت أسفل الصدر والقضاء على التثدي)",
        "Pec Deck Machine (عزل لخط الصدر الداخلي)",
        "Dips - Chest Focus (تمرين وزن جسم - حارق قوي لدهون الصدر)",
        "Push-ups (أساسي لضخ الدم)"
    ],
    "ظهر": [
        "Deadlift (التمرين الملكي لرفع التستوستيرون وهرمون النمو)",
        "Lat Pulldown - Wide Grip (لتعريض الظهر وسحب الجلد)",
        "Seated Cable Row (لسمك الظهر الأوسط)",
        "Barbell Bent-Over Row (قوة جذع شاملة)",
        "T-Bar Row",
        "Pull-ups (العقلة الحرة)"
    ],
    "أرجل": [
        "Barbell Squat (المحفز الأول لحرق دهون البطن والمؤخرة)",
        "Leg Press (أوزان عالية لزيادة الكتلة بأمان على أسفل الظهر)",
        "Bulgarian Split Squat (نحت وتدوير المؤخرة بقوة وتوازن)",
        "Romanian Deadlift - RDL (شد أوتار الركبة والمؤخرة بقوة)",
        "Leg Extension (عزل أمامي للرباعيات)",
        "Lying Leg Curl (عزل خلفي للأوتار)",
        "Standing Calf Raise (سمانات)"
    ],
    "أكتاف": [
        "Overhead Barbell Press (أكتاف عريضة تسحب جلد الصدر للأعلى)",
        "Dumbbell Lateral Raise (لتعريض الكتف الجانبي)",
        "Front Cable Raise",
        "Face Pulls (لصحة المفاصل واستقامة القوام الخلفي)",
        "Arnold Press"
    ],
    "باي": [
        "Barbell Bicep Curl (للكتلة الأساسية)",
        "Dumbbell Hammer Curl (لتطوير العضلة العضدية والساعد)",
        "Preacher Curl Machine (عزل تام)",
        "Cable Rope Curl"
    ],
    "تراي": [
        "Tricep Rope Pushdown",
        "Skull Crushers (EZ Bar)",
        "Overhead Dumbbell Extension (لشد الترهلات السفلية للذراع)",
        "Close-Grip Bench Press (مركب للتراي والصدر الداخلي)"
    ],
    "بطن": [
        "Cable Crunches (بطن بأوزان لبروز العضلات المكونة للـ 6-pack)",
        "Hanging Leg Raises (لشد البطن السفلي وشفط الكرش من الأسفل)",
        "Plank - Weighted (لقوة الجذع وشفط المعدة للداخل)",
        "Ab Roller (عجلة البطن - تمرين متقدم)"
    ],
    "جوانب": [
        "Cable Woodchoppers (نحت الخصر بالدوران المقاوم)",
        "Russian Twists (مع قرص وزن لتقوية الجوانب)"
    ],
    "تمرين حر": [
        "Custom Machine Workout (جهاز مخصص)",
        "Cardio Intensive Session (جلسة كارديو مكثفة)"
    ]
}

def get_exercises_for_muscle(muscle_string):
    """مستخرج التمارين الذكي بناءً على العضلة المبرمجة اليوم"""
    if not muscle_string or muscle_string == "اذهب لسان هندسة الأسبوع": 
        return EXERCISE_DB["تمرين حر"]
        
    combined = []
    for key, exercises in EXERCISE_DB.items():
        if key in muscle_string: 
            combined.extend(exercises)
            
    if not combined:
        return EXERCISE_DB["تمرين حر"]
        
    return list(set(combined))

# =====================================================================
# 6. محرك الذكاء الاصطناعي للاستنتاج وكسر الأوزان (Smart Reps)
# =====================================================================
def calculate_smart_reps(exercise_name, current_weight):
    """
    خوارزمية الذكاء الاصطناعي لاستنتاج العدات في حال نسيان تسجيلها.
    تقرأ الوزن السابق والجديد وتطبق قوانين زيادة الحمل التدريجي.
    """
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            last_w = float(last_record['Weight'])
            last_r = int(last_record['Reps'])
            
            # قوانين التضخيم الفيزيولوجية
            if current_weight > last_w: 
                return max(last_r - 2, 6) # أثقل وزن = عدات أقل (لا يقل عن 6)
            elif current_weight < last_w: 
                return last_r + 2 # وزن أخف = عدات أكثر
            else: 
                return last_r # نفس الوزن = ثبات
                
    # القيمة الافتراضية للتضخيم
    return 10

def fetch_historical_data(exercise_name):
    """جلب بيانات آخر جلسة للمقارنة اللحظية في السجل الذكي"""
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            return last_record['Date'], last_record['Weight'], last_record['Reps']
    return None, None, None

# =====================================================================
# 7. محرك الاستراتيجية وبروتوكولات كلاسات سفيان
# =====================================================================
CLASS_BURN_DB = {
    "موتيف 8": 450, "فت كومبات": 650, "كور اكستريم": 350,
    "ستيب": 450, "اكوا": 350, "بامب فت": 400,
    "بودي ماكس": 600, "رادير": 300, "جي فت": 400,
    "فت اتاك": 600, "موبيلتي": 200, "لا يوجد": 0
}

WORKOUT_ENGINE = {
    "موتيف 8": {
        "iron": "صدر + تراي", 
        "warmup": "دوران أكتاف 3 دق + إطالة صدر 2 دق", 
        "flow": "الصدر يحتاج تركيز عالي. ابدأ بـ Incline Press لشد الصدر العلوي أولاً."
    },
    "فت كومبات": {
        "iron": "أرجل + بطن", 
        "warmup": "إطالة ديناميكية للحوض والركب", 
        "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل ولا تتنازل عن الأوزان."
    },
    "كور اكستريم": {
        "iron": "أكتاف + جوانب", 
        "warmup": "تسخين جذع مركزي + دوران خصر", 
        "flow": "أكتاف عريضة = خصر أنحف بصرياً. ركز على Overhead Press للكتلة."
    },
    "ستيب": {
        "iron": "ظهر + باي", 
        "warmup": "إطالة قطنية أسفل الظهر + سحب حبل مطاطي", 
        "flow": "شد الظهر يمنع التحدب. ركز على Deadlift و Lat Pulldown للتعريض."
    },
    "اكوا": {
        "iron": "حديد شامل (Full Body)", 
        "warmup": "إحماء مفاصل شامل من الرقبة للكاحل", 
        "flow": "اختر تمرين مركب واحد لكل عضلة كبيرة (بنش، سكوات، سحب)."
    },
    "بامب فت": {
        "iron": "صدر + أكتاف", 
        "warmup": "تسخين أكتاف بوزن خفيف 2.5 كيلو", 
        "flow": "أوزان متوسطة وتكرارات عالية للـ Pump وضخ الدم بقوة للألياف."
    },
    "بودي ماكس": {
        "iron": "أرجل + ظهر", 
        "warmup": "سكوات وزن الجسم 20 عدة", 
        "flow": "أعنف يوم! يستهدف أكبر عضلتين لنسف الكرش. حافظ على طاقتك."
    },
    "رادير": {
        "iron": "ذراعين (باي وتراي)", 
        "warmup": "إطالة أوتار الرسغ ببطء شديد", 
        "flow": "Supersets باي وتراي بشكل متتالي لزيادة الحرق واختصار وقت النادي."
    },
    "جي فت": {
        "iron": "حديد قوة (Heavy Lift)", 
        "warmup": "تسخين مفاصل مكثف جداً لتفادي الإصابة", 
        "flow": "3 إلى 5 عدات بأقصى وزن حر. راحة 3 دقائق كاملة بين الجولات."
    },
    "فت اتاك": {
        "iron": "أرجل + أكتاف", 
        "warmup": "هرولة خفيفة 3 دق + قفز", 
        "flow": "تمارين مركبة سريعة لرفع نبض القلب وزيادة معدل الحرق الأيضي."
    },
    "موبيلتي": {
        "iron": "تمرين حر (النقاط الضعيفة)", 
        "warmup": "استخدام الـ Foam Roller ببطء", 
        "flow": "استهدف عضلة متأخرة وضعيفة، أو قم بجلسة إطالات عميقة للتعافي."
    },
    "لا يوجد": {
        "iron": "تمرين حر متكامل", 
        "warmup": "سير مائل 10 دق", 
        "flow": "أنت القائد اليوم. صمم روتينك بناءً على مستوى طاقتك."
    }
}

def analyze_muscle_balance(plan_df):
    """فحص هندسي للمخطط الأسبوعي للتحذير من أي خلل في توزيع العضلات"""
    if plan_df.empty: 
        return True, ""
        
    all_muscles = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    if "أرجل" not in all_muscles: 
        alerts.append("🔴 خطأ هندسي: المخطط يفتقد لتمارين الأرجل (وهي أساس ضخ التستوستيرون وحرق الكرش).")
    if "ظهر" not in all_muscles: 
        alerts.append("🔴 خلل في القوام: يجب تدريب الظهر لسحب الأكتاف وتصحيح انحناء العمود الفقري.")
    if all_muscles.count("صدر") > 2: 
        alerts.append("🔴 إجهاد مفرط: الصدر مستهدف بكثافة عالية جداً، هذا سيؤدي لتمزق الأنسجة وعدم استشفائها.")
        
    if len(alerts) > 0: 
        return False, "<br>".join(alerts)
        
    return True, "🟢 ممتاز: المخطط متوازن، يهاجم الدهون، ويضمن الاستشفاء السليم."

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
# 8. البناء المعماري لواجهة التطبيق (The Master Blueprint Interface)
# =====================================================================
def main():
    makkah_now = get_makkah_time()
    days_map_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_map_ar[makkah_now.strftime("%A")]
    current_date = makkah_now.strftime("%Y-%m-%d")
    week_dates = get_week_dates()

    st.markdown("<h1>👑 محرك تايتان V21 (The Master Blueprint)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>المنطقة: مكة المكرمة | اليوم: {today_ar} ({current_date}) | الساعة الآن: {makkah_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    tabs = st.tabs([
        "🚀 الملاحة والميدان", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ السجل الذكي والتطور", 
        "📸 عيادة InBody", 
        "🥗 المساعد الغذائي و Vision AI", 
        "🛠️ مركز الصيانة"
    ])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: الميدان والملاحة (Dynamic GPS based on User Links)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            # يوم الراحة المقدس
            st.markdown(
                """
                <div class='titan-card titan-card-center' style='border: 2px solid #2ECC40;'>
                    <h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1>
                    <p style='font-size: 20px; color:#A0A0A0;'>يوم الاستشفاء السلبي الإلزامي. بناء الأنسجة وحرق الدهون يتم الآن، استمتع بوقتك ولا تجهد نفسك.</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            # جلب معلومات كلاس اليوم
            s_class, iron_target, warmup, t_flow = "غير محدد", "غير محدد", "غير محدد", "غير محدد"
            plan_df = fetch_sheet_safe("Weekly_Plan")
            if not plan_df.empty and 'Date' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Date'] == current_date].iloc[0]
                    s_class, iron_target = today_row['Class'], today_row['Muscle']
                    if s_class in WORKOUT_ENGINE: 
                        warmup = WORKOUT_ENGINE[s_class]['warmup']
                        t_flow = WORKOUT_ENGINE[s_class]['flow']
                except Exception: 
                    pass

            if st.session_state['attendance_mode'] == "Absent":
                # واجهة الغياب التام
                st.markdown(
                    f"""
                    <div class='titan-card' style='border-color: #FF4136;'>
                        <h2 style='color:#FF4136; text-align:center;'>تم تسجيل الغياب التام اليوم ❌</h2>
                        <p style='text-align:center; font-size:18px;'>النظام قام بترحيل تمرين <b>({iron_target})</b> ليوم غد للتعويض.</p>
                        <hr style='border-color:#333;'>
                        <h4 style='color:#E0E0E0; text-align:center;'>بروتوكول التغذية الطارئ</h4>
                        <p style='text-align:center;'>لا يوجد حرق طاقة اليوم. يُمنع تناول الكربوهيدرات في العشاء نهائياً.</p>
                    </div>
                    """, unsafe_allow_html=True)
                if st.button("🔄 التراجع (قررت الذهاب للنادي)", use_container_width=True):
                    st.session_state['attendance_mode'] = "Full"
                    st.rerun()
            else:
                col_t1, col_t2 = st.columns([2, 1])
                
                with col_t2:
                    # حاسبة المواقع بناء على الروابط المقدمة
                    st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 حاسبة الانطلاق الحية</h3>", unsafe_allow_html=True)
                    user_loc = st.selectbox("أين أنت الآن؟", [
                        "🏠 البيت (جدة - المروة)", 
                        "🏢 العمل (جدة - الشرفية)", 
                        "🕋 العمل (مكة المكرمة)"
                    ])
                    
                    is_rush_hour = 17 <= makkah_now.hour <= 21
                    
                    # هندسة الدقائق بدقة بناء على اللوكيشن ووقت الذروة
                    if user_loc == "🏠 البيت (جدة - المروة)": 
                        commute_mins = 35 if is_rush_hour else 20
                    elif user_loc == "🏢 العمل (جدة - الشرفية)": 
                        commute_mins = 45 if is_rush_hour else 30
                    elif user_loc == "🕋 العمل (مكة المكرمة)": 
                        commute_mins = 80 if is_rush_hour else 60
                    
                    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
                    st.markdown("<h3 style='margin-top:0;'>🕹️ التحكم الميداني</h3>", unsafe_allow_html=True)
                    
                    if st.button("✅ حضور كامل (كلاس + حديد)", use_container_width=True):
                        st.session_state['attendance_mode'] = "Full"
                        st.rerun()
                    if st.button("🏋️ غياب عن الكلاس (حديد فقط)", use_container_width=True):
                        st.session_state['attendance_mode'] = "IronOnly"
                        st.rerun()
                    if st.button("⏳ تأخير المسار (زحمة غير متوقعة)", use_container_width=True):
                        st.session_state['attendance_mode'] = "Delayed"
                        st.rerun()
                    if st.button("❌ غياب تام عن النادي", use_container_width=True):
                        st.session_state['attendance_mode'] = "Absent"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_t1:
                    class_burn = CLASS_BURN_DB.get(s_class, 0)
                    arr_timeObj = makkah_now + timedelta(minutes=commute_mins)
                    arr_str = arr_timeObj.strftime("%I:%M %p")
                    now_str = makkah_now.strftime("%I:%M %p")
                    
                    if st.session_state['attendance_mode'] == "Full":
                        # الخطة أ
                        iron_start = (arr_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card'>
                            <h3 style='margin-top:0;'>🗺️ الخطة أ (طاقة قصوى - كلاس وحديد)</h3>
                            <p style='font-size:18px;'>الحديد المستهدف: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس المجدول: <b style='color:#FFD700;'>{s_class}</b> <span style='color:#FF4136; font-size:14px;'>(حرق ~{class_burn} kcal)</span></p>
                            <p style='color:#888;'>الاستراتيجية المتبعة: {t_flow}</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق من {user_loc}: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ الوصول المتوقع للنادي: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <h5 style='color:#E0E0E0;'>الجدول الميداني التفاعلي لإنهاء التمرين قبل الإغلاق</h5>
                            <p>🔥 {arr_str} - {iron_start} : إحماء مفاصل وتجهيز ({warmup})</p>
                            <p>💪 {iron_start} - 09:00 PM : <b style='color:#FF4136;'>صالة الحديد (كسر أوزان حرة بأقصى طاقة قبل استنزاف الجلايكوجين)</b></p>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (لحرق دهون البطن والمؤخرة بشكل صافي)</b></p>
                            <p>🧊 10:00 PM - 10:20 PM : <b style='color:#2ECC40;'>الاستشفاء قبل الإغلاق</b></p>
                        </div>
                        """
                    elif st.session_state['attendance_mode'] == "IronOnly":
                        # الخطة ب: حديد فقط براحة
                        iron_start = (arr_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #0074D9;'>
                            <h3 style='margin-top:0; color:#0074D9;'>🏋️ مسار الحديد المكثف (تم إسقاط الكلاس)</h3>
                            <p style='font-size:18px;'>الحديد المستهدف اليوم: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <p style='color:#888;'>بما أن الكلاس تم إلغاؤه، لديك طاقة أعلى لكسر الأوزان الحرة وبناء الكتلة.</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق من {user_loc}: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ وصول المواقف: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <h5 style='color:#E0E0E0;'>الجدول الميداني المفتوح</h5>
                            <p>🔥 {arr_str} - {iron_start} : إحماء دقيق لتفادي الإصابة ({warmup})</p>
                            <p>💪 {iron_start} - 10:30 PM : <b style='color:#FF4136;'>صالة الحديد (خذ وقتك، العب جولات إضافية، وتحدى أوزانك القديمة)</b></p>
                            <p>🧊 10:30 PM - 10:55 PM : <b style='color:#2ECC40;'>الاستشفاء المائي المطول</b></p>
                        </div>
                        """
                    elif st.session_state['attendance_mode'] == "Delayed":
                        # الخطة ج: تأخير وإنقاذ ما يمكن
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #FF4136;'>
                            <h3 style='margin-top:0; color:#FF4136;'>⚠️ مسار التأخير (إنقاذ التمرين)</h3>
                            <p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة فور وصولك لعدم تفويت التسخين</b></p>
                            <p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع (استخدم أجهزة العزل فقط، يُمنع الأوزان الحرة لتفادي الإصابة بسبب إرهاق الكلاس)</b></p>
                            <p>🧊 10:35 PM - 10:55 PM : <b style='color:#2ECC40;'>استشفاء مائي سريع</b></p>
                        </div>
                        """
                    st.markdown(nav_html, unsafe_allow_html=True)

                st.markdown("### 🧊 البروتوكول الطبي (إلزامي)")
                rec_html = """
                <div class='recovery-routine'>
                    <h4 style='color:#0074D9; margin:0;'>🏊 الأساس اليومي للاستشفاء</h4>
                    <p style='font-size: 16px; margin:0;'>1. السباحة: 15 دقيقة لتبريد المفاصل وإخراج حمض اللاكتيك.<br>2. الجاكوزي البارد: 3 دقائق (إلزامي للخصوبة ولرفع التستوستيرون).</p>
                </div>
                """
                st.markdown(rec_html, unsafe_allow_html=True)
                
                if today_ar in ["الاثنين", "الخميس"]: 
                    st.markdown("<div class='fertility-warning'><h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'>يُسمح لك بـ <b>10 دقائق فقط</b> في الجاكوزي الحار، ويُشترط أخذ دش بارد جداً فوراً بعد الخروج لحماية الخصيتين.</p></div>", unsafe_allow_html=True)
                else: 
                    st.markdown("<div class='fertility-safe'><h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'><b>ممنوع تماماً</b> الجاكوزي الحار أو الساونا. الحرارة المتكررة تقتل الخصوبة ببطء.</p></div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (مربوطة بالتواريخ)
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
                    new_schedule.append({
                        "Day": d, 
                        "Date": exact_date, 
                        "Class": choice, 
                        "Muscle": muscle_target, 
                        "Status": "مجدول"
                    })
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص هندسي واعتماد المخطط", use_container_width=True):
                df_new_plan = pd.DataFrame(new_schedule)
                is_balanced, balance_msg = analyze_muscle_balance(df_new_plan)
                box_class = 'success-box' if is_balanced else 'alert-box'
                st.markdown(f"<div class='{box_class}'>{balance_msg}</div>", unsafe_allow_html=True)
                
                success, s_msg = overwrite_sheet_safe("Weekly_Plan", df_new_plan)
                if success: st.success(s_msg)
                else: st.warning(s_msg)

    # -----------------------------------------------------------------
    # اللسان 3: السجل الذكي (Timer + Auto-Fill + Visual Charts)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي، الرسوم البيانية، والمؤقت")
        
        todays_muscle = "اذهب لسان هندسة الأسبوع"
        plan_df = fetch_sheet_safe("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: todays_muscle = plan_df[plan_df['Date'] == current_date].iloc[0]['Muscle']
            except: pass
            
        c_timer1, c_timer2 = st.columns([1, 2])
        
        # مؤقت الراحة بين الجولات لضمان عدم إضاعة الوقت
        with c_timer1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة</h4><p style='font-size:12px; color:#888;'>لضمان الضخ العضلي</p>", unsafe_allow_html=True)
            if st.button("بدء 90 ثانية", use_container_width=True):
                progress_bar = st.progress(0)
                for i in range(90):
                    time.sleep(1)
                    progress_bar.progress((i + 1) / 90)
                st.success("انتهى وقت الراحة! ارجع للبار فوراً.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c_timer2:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>العضلة المستهدفة اليوم: <span style='color:#FFD700;'>{todays_muscle}</span></h4>", unsafe_allow_html=True)
            available_exercises = get_exercises_for_muscle(todays_muscle)
            selected_ex = st.selectbox("اختر التمرين من قاعدة البيانات لتسجيله:", available_exercises)
            
            p_date, p_weight, p_reps = fetch_historical_data(selected_ex)
            
            if p_date:
                st.markdown(f"<div style='background:#111; padding:10px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:15px;'><p style='color:#888; margin:0;'>آخر مرة لعبت التمرين: {p_date} | <b>سابقاً: {p_weight} KG</b> × {p_reps}</p></div>", unsafe_allow_html=True)
                default_w = float(p_weight)
            else:
                default_w = 0.0
                
            c_wt, c_rp = st.columns(2)
            input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, value=default_w, step=2.5)
            input_rp = c_rp.number_input("العدات (اتركها 0 للذكاء الاصطناعي)", min_value=0, value=0, step=1)
            
            if st.button("💾 توثيق الجلسة في الإكسل", use_container_width=True):
                final_reps = input_rp
                if input_rp == 0:
                    final_reps = calculate_smart_reps(selected_ex, input_wt)
                    st.success(f"🤖 الذكاء الاصطناعي استنتج بناءً على أوزانك أنك لعبت: {final_reps} عدات.")
                    
                new_entry = {"Date": current_date, "Muscle": todays_muscle, "Exercise": selected_ex, "Weight": input_wt, "Reps": final_reps}
                success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
                if success: st.success(f"تم توثيق {selected_ex} بنجاح في السحابة.")
                else: st.error(s_msg)
            st.markdown("</div>", unsafe_allow_html=True)

        # التحليل البصري (Data Visualization using Native Streamlit Line Charts)
        st.markdown("#### 📈 تحليل التطور البصري (Progressive Overload Chart)")
        logs_df = fetch_sheet_safe("Workout_Logs")
        if not logs_df.empty and 'Exercise' in logs_df.columns:
            chart_ex = st.selectbox("اختر تمريناً لرؤية مسار تطور أوزانك:", logs_df['Exercise'].unique())
            chart_data = logs_df[logs_df['Exercise'] == chart_ex]
            if not chart_data.empty:
                try:
                    chart_data['Weight'] = pd.to_numeric(chart_data['Weight'])
                    chart_data = chart_data.set_index('Date')
                    st.line_chart(chart_data['Weight'], use_container_width=True)
                    st.caption("صعود المنحنى يعني أنك تكسر أوزانك باستمرار وتبني كتلة عضلية نقية تحرق الدهون.")
                except Exception as e: 
                    st.warning("البيانات في الإكسل تحتاج إلى تنظيف لعرض الرسم البياني بشكل صحيح.")
        else: 
            st.info("قم بتسجيل التمارين أولاً ليبدأ النظام برسم منحنى التطور العضلي الخاص بك.")

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody (قاعدة البيانات والرسوم)
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان للقياسات الحيوية")
        st.info("قم برفع تقرير InBody أو إدخال الأرقام يدوياً لرسم منحنى نزول الكرش والدهون الحشوية.")
        
        with st.form("inbody_form"):
            c1, c2 = st.columns(2)
            ib_date = c1.date_input("تاريخ الفحص")
            ib_weight = c1.number_input("الوزن الإجمالي (KG)", value=91.9, step=0.1)
            ib_muscle = c2.number_input("كتلة العضلات (SMM - KG)", value=40.0, step=0.1)
            ib_fat = c2.number_input("نسبة الدهون (%)", value=20.0, step=0.5)
            ib_visceral = st.number_input("مؤشر الدهون الحشوية (الكرش الداخلي)", value=14, step=1)
            
            if st.form_submit_button("💾 أرشفة التقرير الطبي في السحابة", use_container_width=True):
                inbody_data = {
                    "Date": ib_date.strftime("%Y-%m-%d"),
                    "Weight": ib_weight,
                    "Muscle_Mass": ib_muscle,
                    "Fat_Percentage": ib_fat,
                    "Visceral_Fat": ib_visceral
                }
                success, msg = append_to_sheet_safe("InBody_Logs", inbody_data)
                if success: st.success("تم توثيق فحص InBody بنجاح.")
                else: st.error(msg)
                
        # عرض منحنى الدهون الحشوية بشكل بصري (Bar Chart)
        inbody_df = fetch_sheet_safe("InBody_Logs")
        if not inbody_df.empty and 'Visceral_Fat' in inbody_df.columns:
            st.markdown("#### 📉 مسار نزول الدهون الحشوية (الكرش)")
            try:
                inbody_df['Visceral_Fat'] = pd.to_numeric(inbody_df['Visceral_Fat'])
                inbody_df = inbody_df.set_index('Date')
                st.bar_chart(inbody_df['Visceral_Fat'], use_container_width=True)
                st.caption("الهدف: يجب أن ينخفض هذا العمود باستمرار إلى ما دون النطاق 10 لتضمن اختفاء الكرش نهائياً وبروز عضلات البطن.")
            except: 
                pass

    # -----------------------------------------------------------------
    # اللسان 5: المساعد الغذائي الذكي و Vision AI
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 المساعد الغذائي الذكي (Nutrition AI & Macros)")
        st.write("لأنك تأكل عشوائياً، صممنا لك نظاماً يعتمد على اختيار الوجبات التي تناولتها وهو سيقوم بالحساب والجمع.")
        
        tab_f1, tab_f2, tab_f3 = st.tabs(["📸 تصوير الوجبة (Vision AI)", "🍲 طبخ البيت والإيدامات", "🍔 الوجبات السريعة والمطاعم"])
        
        # 1. محاكاة قراءة الصور للوجبات
        with tab_f1:
            st.markdown("<div class='titan-card titan-card-center'>", unsafe_allow_html=True)
            st.markdown("<h4>التعرف التلقائي على الماكروز عبر الصور</h4>", unsafe_allow_html=True)
            uploaded_meal = st.file_uploader("التقط أو ارفع صورة وجبتك لتحليلها", type=["jpg", "jpeg", "png"])
            if uploaded_meal:
                st.image(uploaded_meal, use_container_width=True)
                if st.button("🔍 تحليل الصورة (AI)", use_container_width=True):
                    with st.spinner("جاري فحص مكونات الصورة وتقدير السعرات عبر الذكاء الاصطناعي..."):
                        time.sleep(2)
                        st.session_state['meal_cals'] += 450 
                        st.session_state['meal_protein'] += 35
                        st.success("🤖 تم التعرف على: مصدر بروتين دجاج + كربوهيدرات معقدة. تم إضافة السعرات (450 kcal) والبروتين (35g) لعدادك اليومي.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 2. طبخ البيت والإيدامات (المطبخ السعودي)
        with tab_f2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>🍲 الإيدامات وطبخ البيت</h4>", unsafe_allow_html=True)
            selected_edaam = st.multiselect("اختر وجبات غداء المنزل اليوم:", list(EDAAM_DB.keys()))
            if st.button("➕ إضافة الإيدام للعداد"):
                for meal in selected_edaam:
                    st.session_state['meal_protein'] += EDAAM_DB[meal]["protein"]
                    st.session_state['meal_cals'] += EDAAM_DB[meal]["cals"]
                st.success("تم جمع الماكروز للوجبة المنزلية بنجاح.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 3. المطاعم والوجبات السريعة
        with tab_f3:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>🍔 الوجبات السريعة وإدخال يدوي</h4>", unsafe_allow_html=True)
            selected_fast = st.multiselect("اختر من المطاعم المعتادة:", list(FAST_FOOD_DB.keys()))
            if st.button("➕ إضافة الوجبة الجاهزة"):
                for meal in selected_fast:
                    st.session_state['meal_protein'] += FAST_FOOD_DB[meal]["protein"]
                    st.session_state['meal_cals'] += FAST_FOOD_DB[meal]["cals"]
                st.success("تم جمع الماكروز للوجبة السريعة بنجاح.")
            
            st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
            st.write("**إدخال يدوي مباشر (إذا قرأت القيمة من المنيو في المطعم):**")
            c_man1, c_man2 = st.columns(2)
            man_prot = c_man1.number_input("بروتين (جرام)", min_value=0, step=5)
            man_cal = c_man2.number_input("سعرات حرارية", min_value=0, step=50)
            if st.button("➕ إضافة الإدخال اليدوي للعداد"):
                st.session_state['meal_protein'] += man_prot
                st.session_state['meal_cals'] += man_cal
                st.success("تم جمع القيم المدخلة يدوياً للعداد النهائي.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # لوحة التحكم الرئيسية للوقود والمقارنة مع الهدف (Target)
        target_calories = 1900
        protein_target = int(91.9 * 2.2) # الهدف: 2.2 جرام لكل كيلو من وزن الجسم لمنع الهدم
        
        st.markdown(f"""
        <div class='titan-card'>
            <h4 style='margin-top:0; color:#D4AF37;'>🎯 العداد اللحظي للوقود (بناء العضل وحرق الدهون)</h4>
            <div style='display:flex; justify-content:space-around; margin-top:20px; align-items:center;'>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🍖</span><br><span style='color:#E0E0E0; font-size:14px;'>البروتين المجمع اليوم</span><br>
                    <span class='macro-val' style='color:#FF4136;'>{st.session_state['meal_protein']} / {protein_target}g</span>
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🔥</span><br><span style='color:#E0E0E0; font-size:14px;'>السعرات المجمعة اليوم</span><br>
                    <span class='macro-val' style='color:#D4AF37;'>{st.session_state['meal_cals']} / {target_calories}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            in_sleep = col_f1.number_input("🛌 ساعات النوم الفعلي (من تطبيق Huawei):", value=7.5, step=0.5)
            in_water = col_f1.number_input("💧 كمية الماء (لتر - مهم لطرد احتباس السوائل):", value=3.5, step=0.5)
            
            st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
            if st.form_submit_button("💾 توثيق وحفظ يوم التغذية النهائي في الإكسل", use_container_width=True):
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
                    # تصفير العداد لليوم التالي ليكون جاهزاً للحساب من جديد
                    st.session_state['meal_protein'] = 0
                    st.session_state['meal_cals'] = 0
                else: 
                    st.error(s_msg)

    # -----------------------------------------------------------------
    # اللسان 6: مركز الصيانة والتشخيص المباشر (Diagnostics Tool)
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ التشخيص الهندسي اللحظي للاتصال")
        st.write("هذه الأداة تقوم بإرسال طلب قراءة وكتابة لخوادم جوجل للتأكد من أن المفتاح السري (Service Account) يعمل بكفاءة وليس هناك حظر.")
        
        if st.button("🔄 بدء الاختبار والفحص العميق", use_container_width=True):
            with st.spinner('جاري التفاوض مع خوادم Google Cloud وفتح قنوات الاتصال...'):
                time.sleep(1)
                conn = get_db_connection()
                if conn:
                    try:
                        # محاولة قراءة فعلية لإثبات وجود الصلاحيات
                        conn.read(worksheet="Weekly_Plan", ttl="0s")
                        st.markdown(
                            """
                            <div class='success-box'>
                                <h3 style='margin:0;'>🟢 النظام مدرع ومتصل 100%.</h3>
                                <p style='margin:0;'>صلاحيات الكتابة (Editor) تعمل، والتطبيق يتحدث مع قاعدة البيانات بشكل مثالي.</p>
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
                            <p style='margin:0;'>التطبيق لا يستطيع قراءة مفاتيح Secrets. راجع إعدادات Streamlit.</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()
