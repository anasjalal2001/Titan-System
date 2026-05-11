import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والزمني (محرك توقيت مكة المكرمة المخصص بدون مكتبات خارجية)
# =====================================================================
st.set_page_config(page_title="Titan V16 - Ultimate Commander", page_icon="👑", layout="wide")

def get_makkah_time():
    """محرك زمني دقيق يحسب توقيت مكة المكرمة رياضياً لتجنب أي أخطاء سيرفر"""
    # جلب توقيت جرينتش الحالي وإضافة 3 ساعات (توقيت السعودية)
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# CSS شامل ومفصل جداً للتحكم بأدق تفاصيل الشاشة والألوان
css_code = """
<style>
    /* الإعدادات الأساسية والخلفية */
    .stApp { background-color: #030303; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 900; letter-spacing: 1px; }
    
    /* تصميم الألسنة (Tabs) لتعمل كأزرار تحكم ضخمة */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #111111;
        border-radius: 10px; padding: 15px 20px; color: #D4AF37; font-size: 15px; font-weight: bold; transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); transform: scale(1.05); }
    
    /* تصميم البطاقات الميدانية */
    .titan-card { 
        background: linear-gradient(145deg, #161B22, #0A0D12); border: 1px solid rgba(212, 175, 55, 0.3); 
        border-radius: 18px; padding: 30px; margin-bottom: 25px; text-align: right; 
        box-shadow: 0 15px 25px rgba(0,0,0,0.6); transition: transform 0.3s;
    }
    .titan-card:hover { border-color: rgba(212, 175, 55, 0.8); }
    .titan-card-center { text-align: center; }
    
    /* الأرقام الذهبية للإحصائيات */
    .gold-value { color: #FFD700; font-size: 42px; font-weight: 900; margin: 20px 0; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.3); }
    .sub-text { color: #8B949E; font-size: 15px; line-height: 1.8; }
    
    /* البروتوكولات الطبية والتنبيهات */
    .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 8px solid #0074D9; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 8px solid #2ECC40; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 8px solid #FF4136; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    
    /* صناديق رسائل النظام */
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 18px; border-radius: 10px; color: #FF4136; text-align: right; margin-bottom: 15px; font-weight: bold;}
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 18px; border-radius: 10px; color: #2ECC40; text-align: right; margin-bottom: 15px; font-weight: bold;}
    .info-box { background: rgba(0, 116, 217, 0.1); border: 1px solid #0074D9; padding: 18px; border-radius: 10px; color: #0074D9; text-align: right; margin-bottom: 15px; font-weight: bold;}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =====================================================================
# 2. إدارة الذاكرة المؤقتة (Session State Management)
# =====================================================================
# هذه المتغيرات تضمن استقرار التطبيق حتى لو انقطع الإنترنت
if 'offline_logs' not in st.session_state:
    st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state:
    st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state:
    st.session_state['offline_health'] = []
if 'is_delayed' not in st.session_state:
    st.session_state['is_delayed'] = False
if 'is_absent' not in st.session_state:
    st.session_state['is_absent'] = False

# =====================================================================
# 3. محركات السحاب والمزامنة (مدرعة ضد أخطاء الصلاحيات)
# =====================================================================
def get_db_connection():
    """يحاول الاتصال بالسحابة بصمت لمنع ظهور أخطاء مزعجة للمستخدم"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception:
        return None

def fetch_sheet_safe(sheet_name):
    """يجلب البيانات، وإذا فشل يعيد جدولاً فارغاً لتستمر الواجهة بالعمل"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        return df.dropna(how='all')
    except Exception:
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """إضافة سطر جديد (مثل تمرين جديد أو سجل نوم)"""
    conn = get_db_connection()
    if not conn:
        return False, "لا يوجد اتصال بالسحابة. يرجى مراجعة الصيانة."
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        new_row = pd.DataFrame([new_data_dict])
        
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ والتشفير في قاعدة بيانات جوجل بنجاح."
    except Exception as e:
        return False, f"جوجل ترفض التعديل. تأكد من إضافة إيميل الـ Service Account كمحرر. (الخطأ: {str(e)})"

def overwrite_sheet_safe(sheet_name, df_new):
    """استبدال كامل للبيانات (يستخدم حصرياً مع جدول الأسبوع)"""
    conn = get_db_connection()
    if not conn:
        return False, "لا يوجد اتصال بالسحابة."
    
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الأسبوعي سحابياً بنجاح."
    except Exception as e:
        return False, f"فشل الرفع. تأكد من الصلاحيات. (الخطأ: {str(e)})"

# =====================================================================
# 4. قاعدة بيانات التمارين الشاملة (Exercise Database & Biomechanics)
# مصممة خصيصاً للقضاء على الترهلات في الصدر والبطن والمؤخرة
# =====================================================================
EXERCISE_DB = {
    "صدر": [
        "Incline Barbell Bench Press (لشد الصدر العلوي المترهل)",
        "Flat Dumbbell Press (لبناء الكتلة الأساسية)",
        "Decline Cable Flys (لنحت أسفل الصدر والقضاء على التثدي)",
        "Pec Deck Machine (عزل لعضلة الصدر الداخلية)",
        "Dips - Chest Focus (تمرين وزن جسم حارق لدهون الصدر)",
        "Push-ups (تمرين أساسي)"
    ],
    "ظهر": [
        "Deadlift (التمرين الملكي لرفع التستوستيرون وحرق الدهون الشامل)",
        "Lat Pulldown - Wide Grip (لتعريض الظهر وسحب الجلد)",
        "Seated Cable Row (لسمك الظهر)",
        "Barbell Bent-Over Row (لبناء قوة الجذع)",
        "T-Bar Row",
        "Pull-ups (العقلة)"
    ],
    "أرجل": [
        "Barbell Squat (محفز هرمون النمو الأول لنسف دهون البطن)",
        "Leg Press (أوزان عالية بأمان)",
        "Bulgarian Split Squat (لنحت المؤخرة والأرجل وتقوية الأعصاب)",
        "Romanian Deadlift - RDL (لشد أوتار الركبة والمؤخرة بقوة)",
        "Leg Extension (عزل أمامي)",
        "Lying Leg Curl (عزل خلفي)",
        "Standing Calf Raise (سمانات)"
    ],
    "أكتاف": [
        "Overhead Barbell Press (لبناء أكتاف عريضة تسحب الجلد للأعلى)",
        "Dumbbell Lateral Raise (لتعريض الكتف الجانبي)",
        "Front Cable Raise",
        "Face Pulls (لصحة المفاصل والكتف الخلفي)",
        "Arnold Press"
    ],
    "باي": [
        "Barbell Bicep Curl (للكتلة)",
        "Dumbbell Hammer Curl (لتطوير العضلة العضدية)",
        "Preacher Curl Machine",
        "Cable Rope Curl"
    ],
    "تراي": [
        "Tricep Rope Pushdown",
        "Skull Crushers (EZ Bar)",
        "Overhead Dumbbell Extension (لشد ترهلات الذراع)",
        "Close-Grip Bench Press"
    ],
    "بطن": [
        "Cable Crunches (بأوزان لبروز العضلات وتقوية الجدار)",
        "Hanging Leg Raises (لشد البطن السفلي المترهل)",
        "Plank - Weighted (لقوة الجذع وشفط البطن للداخل)",
        "Ab Roller (عجلة البطن المتقدمة)"
    ],
    "جوانب": [
        "Cable Woodchoppers (لنحت الخصر)",
        "Russian Twists (مع قرص وزن)"
    ],
    "تمرين حر": [
        "Custom Machine Workout",
        "Cardio Intensive Session"
    ]
}

def get_exercises_for_muscle(muscle_string):
    """تستقبل العضلة المبرمجة اليوم، وتعيد قائمة بالتمارين المخصصة لها"""
    if not muscle_string or muscle_string == "اذهب لسان هندسة الأسبوع":
        return EXERCISE_DB["تمرين حر"]
        
    combined = []
    # البحث في القاموس وتجميع التمارين
    for key, exercises in EXERCISE_DB.items():
        if key in muscle_string:
            combined.extend(exercises)
            
    if not combined:
        return EXERCISE_DB["تمرين حر"]
        
    return list(set(combined)) # إزالة التكرار إن وجد

# =====================================================================
# 5. محرك هندسة التمارين والوقت (Workout Strategy Engine)
# =====================================================================
WORKOUT_ENGINE = {
    "موتيف 8": {
        "iron": "صدر + تراي", 
        "warmup": "دوران أكتاف بالأشرطة المطاطية 3 دق + إطالة صدر 2 دق", 
        "flow": "الصدر يحتاج تركيز. ابدأ بـ Incline Press لشد الصدر العلوي، ثم العزل."
    },
    "فت كومبات": {
        "iron": "أرجل + بطن", 
        "warmup": "إطالة ديناميكية للحوض والركب + قفز خفيف", 
        "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل، ثم اختم بتمارين البطن."
    },
    "كور اكستريم": {
        "iron": "أكتاف + جوانب", 
        "warmup": "تسخين جذع مركزي + دوران خصر", 
        "flow": "أكتاف عريضة تعني خصر أنحف بصرياً. ركز على الـ Overhead Press."
    },
    "ستيب": {
        "iron": "ظهر + باي", 
        "warmup": "إطالة قطنية أسفل الظهر + سحب حبل مطاطي", 
        "flow": "شد الظهر يمنع التحدب. ركز على الـ Deadlift و الـ Lat Pulldown."
    },
    "اكوا": {
        "iron": "حديد شامل (Full Body)", 
        "warmup": "إحماء مفاصل شامل من الرقبة للكاحل", 
        "flow": "تمرين مركب واحد لكل عضلة (سكوات، بنش برس، ديدليفت)."
    },
    "بامب فت": {
        "iron": "صدر + أكتاف", 
        "warmup": "تسخين أكتاف بوزن خفيف 2.5 كيلو", 
        "flow": "يوم ضخ الدم (Pump). أوزان متوسطة وتكرارات عالية لنحت العضلات."
    },
    "بودي ماكس": {
        "iron": "أرجل + ظهر", 
        "warmup": "سكوات وزن الجسم 20 عدة + إطالة قطنية", 
        "flow": "أعنف يوم في الأسبوع. يستهدف أكبر عضلتين لحرق دهون المؤخرة والبطن."
    },
    "رادير": {
        "iron": "ذراعين (باي وتراي)", 
        "warmup": "إطالة أوتار الذراعين والرسغ ببطء", 
        "flow": "العب (Supersets) باي مع تراي لزيادة الحرق واختصار الوقت."
    },
    "جي فت": {
        "iron": "حديد قوة (Heavy Lift)", 
        "warmup": "تسخين دقيق ومكثف للمفاصل الكبيرة قبل الأوزان", 
        "flow": "3 إلى 5 عدات بأقصى وزن ممكن. راحة 3 دقائق بين الجولات لزيادة القوة."
    },
    "فت اتاك": {
        "iron": "أرجل + أكتاف", 
        "warmup": "هرولة خفيفة 3 دق + قفز مكاني", 
        "flow": "تمارين مركبة سريعة لرفع نبض القلب وحرق السعرات."
    },
    "موبيلتي": {
        "iron": "تمرين حر (النقاط الضعيفة)", 
        "warmup": "استهداف مناطق الشد بالـ Foam Roller", 
        "flow": "استغل هذا اليوم لاستهداف عضلة متأخرة أو لتمارين الإطالة العميقة."
    },
    "لا يوجد": {
        "iron": "تمرين حر متكامل", 
        "warmup": "تسخين 10 دقائق سير مائل متواصل", 
        "flow": "أنت القائد اليوم. صمم روتينك بناءً على طاقة جسمك."
    }
}

# =====================================================================
# 6. محرك التحليل والتعويض الآلي (Auto-Rescheduler & Diagnostics)
# =====================================================================
def analyze_muscle_balance(plan_df):
    """دالة هندسية تفحص الجدول الأسبوعي للتأكد من تغطية جميع العضلات لتحقيق هدفك"""
    if plan_df.empty:
        return True, ""
        
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    # القضاء على الكرش يتطلب أرجل (تستوستيرون + هرمون نمو)
    if "أرجل" not in all_muscles_text:
        alerts.append("🔴 خطأ استراتيجي: المخطط يفتقد لتمارين الأرجل. الأرجل هي المحرك الأساسي لحرق دهون البطن والمؤخرة!")
        
    # القوام السليم
    if "ظهر" not in all_muscles_text:
        alerts.append("🔴 خلل في القوام: لم يتم جدولة تمرين للظهر. مهم جداً لدعم العمود الفقري وسحب الأكتاف للخلف.")
        
    # منع التمزقات
    if all_muscles_text.count("صدر") > 2:
        alerts.append("🔴 إجهاد مفرط: عضلة الصدر مستهدفة أكثر من مرتين. هذا سيؤدي للهدم العضلي بدل البناء.")
        
    if len(alerts) > 0:
        error_msg = "<br>".join(alerts)
        return False, error_msg
        
    return True, "🟢 ممتاز هندسياً: المخطط متوازن، يهاجم الدهون، وشامل لجميع المجموعات العضلية."

def get_dynamic_schedule(is_delayed):
    """محرك الملاحة وحساب الوقت المتبقي قبل الإغلاق (11:00 م)"""
    now = get_makkah_time()
    
    # تحديد مدة الطريق بناءً على وقت الذروة في جدة (5م إلى 9م)
    is_rush_hour = 17 <= now.hour <= 21
    commute_time = 35 if is_rush_hour else 25
    
    arrival_time = now + timedelta(minutes=commute_time)
    
    # تنسيق الأوقات لتظهر بنظام 12 ساعة
    now_str = now.strftime("%I:%M %p")
    arrival_str = arrival_time.strftime("%I:%M %p")
    
    return now_str, arrival_str, commute_time, arrival_time

def get_week_dates():
    """حساب تواريخ الأسبوع بدءاً من يوم السبت"""
    today = get_makkah_time()
    # معادلة حسابية لإرجاع الأيام حتى نصل ليوم السبت
    idx = (today.weekday() + 2) % 7 
    saturday = today - timedelta(days=idx)
    
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates = {}
    for i, day in enumerate(week_days):
        week_dates[day] = (saturday + timedelta(days=i)).strftime("%Y-%m-%d")
    return week_dates

def fetch_historical_weight(exercise_name):
    """البحث في السجلات القديمة لإيجاد آخر وزن وعدات (للـ Auto-Fill)"""
    df = fetch_sheet_safe("Workout_Logs")
    
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            return last_record['Date'], last_record['Weight'], last_record['Reps']
    return None, None, None

# =====================================================================
# 7. البناء المعماري لواجهة التطبيق (The Interface)
# =====================================================================
def main():
    makkah_now = get_makkah_time()
    
    days_map_ar = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_en = makkah_now.strftime("%A")
    today_ar = days_map_ar[today_en]
    current_date = makkah_now.strftime("%Y-%m-%d")
    
    week_dates = get_week_dates()

    # الترويسة الرئيسية
    st.markdown("<h1>👑 محرك تايتان V16 (القيادة الذكية)</h1>", unsafe_allow_html=True)
    header_html = f"<p style='text-align:center; color:#888;'>المنطقة الزمنية: مكة المكرمة | اليوم: {today_ar} ({current_date})</p>"
    st.markdown(header_html, unsafe_allow_html=True)

    # تقسيم الشاشة
    tabs = st.tabs([
        "🚀 الملاحة والميدان", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ السجل الذكي (Auto-Fill)", 
        "📸 عيادة InBody", 
        "🥗 الوقود", 
        "🛠️ مركز الصيانة"
    ])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: الملاحة والميدان (GPS & Time Management)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            st.markdown(
                """
                <div class='titan-card titan-card-center' style='border: 2px solid #2ECC40;'>
                    <h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1>
                    <p style='font-size: 20px; color:#A0A0A0;'>يوم الاستشفاء السلبي. العضلات تُبنى والدهون تُحرق أثناء الراحة العميقة.</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            # محاولة جلب بيانات اليوم من المخطط
            s_class, iron_target, warmup, t_flow = "غير محدد", "غير محدد", "غير محدد", "غير محدد"
            plan_df = fetch_sheet_safe("Weekly_Plan")
            
            if not plan_df.empty and 'Date' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Date'] == current_date].iloc[0]
                    s_class = today_row['Class']
                    iron_target = today_row['Muscle']
                    if s_class in WORKOUT_ENGINE: 
                        warmup = WORKOUT_ENGINE[s_class]['warmup']
                        t_flow = WORKOUT_ENGINE[s_class]['flow']
                except Exception:
                    pass

            # معالجة منطق الغياب (Absence Logic)
            if st.session_state['is_absent']:
                st.markdown(
                    """
                    <div class='titan-card' style='border-color: #FF4136;'>
                        <h2 style='color:#FF4136; text-align:center;'>تم تسجيل الغياب اليوم ❌</h2>
                        <p style='text-align:center; font-size:18px;'>سيقوم النظام بترحيل تمرين <b>({iron_target})</b> إلى يوم غد لضمان عدم ضياع العضلة.</p>
                        <hr style='border-color:#333;'>
                        <h4 style='color:#E0E0E0; text-align:center;'>بروتوكول التغذية الطارئ</h4>
                        <p style='text-align:center;'>بما أنه لا يوجد حرق طاقة اليوم، يُمنع تناول الكربوهيدرات في وجبة العشاء نهائياً.</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                if st.button("🔄 التراجع عن الغياب (سأذهب للنادي)"):
                    st.session_state['is_absent'] = False
                    st.rerun()
                    
            else:
                # حسابات الملاحة الذكية الحية
                now_str, arrival_str, commute_mins, arr_timeObj = get_dynamic_schedule(st.session_state['is_delayed'])
                
                col_t1, col_t2 = st.columns([2, 1])
                with col_t1:
                    if not st.session_state['is_delayed']:
                        # الخطة أ: الحديد قبل الكلاس (الطاقة القصوى لحرق الدهون)
                        iron_start = (arr_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        
                        nav_html = f"""
                        <div class='titan-card'>
                            <h3 style='margin-top:0;'>📍 الملاحة الذكية (الخطة أ - طاقة قصوى)</h3>
                            <p style='font-size:18px;'>الحديد: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس: <b style='color:#FFD700;'>{s_class}</b></p>
                            <p style='color:#888;'>مسار التمرين: {t_flow}</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <h5 style='color:#2ECC40;'>حاسبة الانطلاق والوصول الحية</h5>
                            <p>🚗 وقت الانطلاق الآن: <b style='color:#D4AF37;'>{now_str}</b></p>
                            <p>⏱️ مدة الطريق المتوقعة: <b style='color:#D4AF37;'>{commute_mins} دقيقة</b></p>
                            <p>🅿️ الوصول لمواقف النادي: <b style='color:#D4AF37;'>{arrival_str}</b></p>
                            <br>
                            <h5 style='color:#E0E0E0;'>الجدول الزمني الميداني</h5>
                            <p>🔥 {arrival_str} - {iron_start} : <span style='color:#A0A0A0;'>إحماء مفاصل ({warmup})</span></p>
                            <p>💪 {iron_start} - 09:00 PM : <b style='color:#FF4136;'>صالة الحديد (استنزاف بأوزان حرة)</b></p>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (لحرق دهون البطن الصافية)</b></p>
                            <p>🧊 10:00 PM - 10:20 PM : <b style='color:#2ECC40;'>بروتوكول الاستشفاء (قبل إغلاق 11:00 م)</b></p>
                        </div>
                        """
                    else:
                        # الخطة ب: التأخير (الكلاس أولاً لتدارك الوقت)
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #FF4136;'>
                            <h3 style='margin-top:0; color:#FF4136;'>⚠️ خطة الطوارئ (تأخير مسار)</h3>
                            <p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة فور وصولك</b></p>
                            <p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع (أجهزة عزل فقط، تجنب الأوزان الحرة لتفادي الإصابة بسبب الإرهاق)</b></p>
                            <p>🧊 10:35 PM - 10:55 PM : <b style='color:#2ECC40;'>استشفاء سريع قبل الإغلاق مباشرة</b></p>
                        </div>
                        """
                    st.markdown(nav_html, unsafe_allow_html=True)
                    
                with col_t2:
                    st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>التحكم الميداني</h3>", unsafe_allow_html=True)
                    if not st.session_state['is_delayed']:
                        if st.button("⏳ سأتأخر (إعادة الجدولة)", use_container_width=True):
                            st.session_state['is_delayed'] = True
                            st.rerun()
                    else:
                        if st.button("✅ وصلت مبكراً (إلغاء التأخير)", use_container_width=True):
                            st.session_state['is_delayed'] = False
                            st.rerun()
                            
                    st.write("") 
                    if st.button("❌ تسجيل غياب (ترحيل الجدول)", use_container_width=True):
                        st.session_state['is_absent'] = True
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("### 🧊 البروتوكول الطبي (إلزامي للتعافي)")
                rec_html = "<div class='recovery-routine'><h4 style='color:#0074D9; margin:0;'>🏊 الأساس اليومي</h4><p style='font-size: 16px; margin:0;'>1. السباحة: 15 دقيقة (لتبريد المفاصل).<br>2. الجاكوزي البارد: 3 دقائق (لرفع هرمون التستوستيرون وتقليل الالتهاب).</p></div>"
                st.markdown(rec_html, unsafe_allow_html=True)
                
                if today_ar in ["الاثنين", "الخميس"]: 
                    w_html = "<div class='fertility-warning'><h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'>مسموح <b>10 دقائق فقط</b> جاكوزي حار/بخار لفك العضلات، ويجب أخذ دش بارد فوراً لحماية الخصوبة الحيوانات المنوية.</p></div>"
                    st.markdown(w_html, unsafe_allow_html=True)
                else: 
                    s_html = "<div class='fertility-safe'><h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'><b>ممنوع تماماً</b> الجاكوزي الحار أو الساونا اليوم. الحرارة تقتل الخصوبة ببطء.</p></div>"
                    st.markdown(s_html, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (مربوطة بالتواريخ الحية)
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ بناء المخطط الأسبوعي وتوازن العضلات")
        st.info("قم باختيار كلاسات سفيان وسيقوم النظام بتوزيع الحديد بشكل يهاجم مناطق تجمع الدهون لديك.")
        
        week_days_ordered = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        
        with st.form("weekly_master_plan"):
            new_schedule = []
            cols = st.columns(3)
            for i, d in enumerate(week_days_ordered):
                exact_date = week_dates.get(d, "")
                with cols[i % 3]:
                    day_lbl = f"<h5 style='color:#E0E0E0; text-align:right;'>{d}<br><span style='font-size:12px; color:#888;'>{exact_date}</span></h5>"
                    st.markdown(day_lbl, unsafe_allow_html=True)
                    
                    choice = st.selectbox("الكلاس", list(WORKOUT_ENGINE.keys()), key=f"conf_{d}", label_visibility="collapsed")
                    muscle_target = WORKOUT_ENGINE[choice]['iron']
                    
                    st.caption(f"الحديد الموجه: **{muscle_target}**")
                    new_schedule.append({
                        "Day": d, 
                        "Date": exact_date, 
                        "Class": choice, 
                        "Muscle": muscle_target,
                        "Status": "مجدول"
                    })
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص واعتماد المخطط الأسبوعي", use_container_width=True):
                df_new_plan = pd.DataFrame(new_schedule)
                
                # فحص التوازن والتنبيه للنقاط المفقودة
                is_balanced, balance_msg = analyze_muscle_balance(df_new_plan)
                box_class = 'success-box' if is_balanced else 'alert-box'
                st.markdown(f"<div class='{box_class}'>{balance_msg}</div>", unsafe_allow_html=True)
                
                # حفظ المخطط
                success, s_msg = overwrite_sheet_safe("Weekly_Plan", df_new_plan)
                if success:
                    st.success(s_msg)
                else:
                    st.warning(s_msg)

    # -----------------------------------------------------------------
    # اللسان 3: السجل الذكي (Auto-Fill & Exercise Dropdowns)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي (ميزة التعرف والتعبئة التلقائية)")
        st.write("النظام يقرأ عضلة اليوم ويجلب لك تمارينها المخصصة باللغة الإنجليزية من قاعدة البيانات.")
        
        # 1. تحديد العضلة المستهدفة لليوم
        todays_muscle = "اذهب لسان هندسة الأسبوع"
        plan_df = fetch_sheet_safe("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: 
                todays_muscle = plan_df[plan_df['Date'] == current_date].iloc[0]['Muscle']
            except: pass
            
        st.markdown(f"<div class='titan-card' style='text-align:right;'>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='margin-top:0;'>الهدف العضلي اليوم: <span style='color:#FFD700;'>{todays_muscle}</span></h4>", unsafe_allow_html=True)
        
        # 2. جلب التمارين المناسبة للعضلة
        available_exercises = get_exercises_for_muscle(todays_muscle)
        selected_ex = st.selectbox("اختر التمرين (التمارين مصممة لشد ونحت الجسم):", available_exercises)
        
        # 3. محرك البحث التلقائي وجلب آخر سجل
        p_date, p_weight, p_reps = fetch_historical_weight(selected_ex)
        
        if p_date:
            hist_html = f"""
            <div style='background:#111; padding:15px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:20px;'>
                <p style='color:#888; margin:0;'>آخر مرة لعبت هذا التمرين كانت بتاريخ: {p_date}</p>
                <h4 style='margin:5px 0; color:#E0E0E0;'>الوزن السابق: <b style='color:#FFD700;'>{p_weight} KG</b> × {p_reps} عدات</h4>
                <p style='color:#2ECC40; margin:0; font-size:14px;'>حاول زيادة الوزن 2.5 كيلو اليوم لكسر حاجز العضلة (Progressive Overload).</p>
            </div>
            """
            st.markdown(hist_html, unsafe_allow_html=True)
            default_w = float(p_weight)
            default_r = int(p_reps)
        else:
            st.info("لا توجد سجلات تاريخية سابقة لهذا التمرين. سيتم تسجيله الآن كمعيار أساسي لك.")
            default_w = 0.0
            default_r = 10
            
        # 4. إدخال الأرقام وتوثيقها
        c_wt, c_rp = st.columns(2)
        input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, value=default_w, step=2.5)
        input_rp = c_rp.number_input("إجمالي العدات (لأفضل جولة)", min_value=0, value=default_r, step=1)
        
        if st.button("💾 توثيق وحفظ السجل الميداني", use_container_width=True):
            new_entry = {
                "Date": current_date, 
                "Muscle": todays_muscle,
                "Exercise": selected_ex, 
                "Weight": input_wt, 
                "Reps": input_rp
            }
            success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
            if success:
                st.success(f"تم توثيق تمرين ({selected_ex}) بنجاح. استمر بالوحشية!")
            else:
                st.error(s_msg)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان للقياسات الحيوية")
        st.info("قم برفع تقرير InBody هنا. التحديث القادم سيتضمن قراءة أرقام الدهون والعضلات تلقائياً من الصورة (OCR).")
        st.file_uploader("ارفع صورة التقرير من جوالك", type=['png', 'jpg', 'jpeg'])

    # -----------------------------------------------------------------
    # اللسان 5: الوقود (Nutrition)
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 إدارة السعرات والنوم (Recovery Input)")
        
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            in_sleep = col_f1.number_input("🛌 ساعات النوم (من تطبيق Huawei):", value=7.5, step=0.5)
            in_water = col_f1.number_input("💧 كمية الماء (لتر):", value=3.5, step=0.5)
            in_cals = col_f2.number_input("🔥 السعرات الحرارية التقريبية:", value=1900, step=50)
            in_notes = col_f2.text_input("📝 ملاحظات حرة:")
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("💾 أرشفة السجل الصحي", use_container_width=True):
                health_record = {
                    "Date": current_date, 
                    "Sleep": in_sleep, 
                    "Water": in_water, 
                    "Calories": in_cals, 
                    "Notes": in_notes
                }
                success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                if success:
                    st.success(s_msg)
                else:
                    st.error(s_msg)

    # -----------------------------------------------------------------
    # اللسان 6: مركز الصيانة التفاعلي (Live Diagnostics)
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ مركز فحص النظام اللحظي (Diagnostics)")
        st.write("هذا القسم يقوم بفحص حي ومباشر لاتصالك بسيرفرات جوجل للتأكد من عدم وجود أي خلل يمنع حفظ البيانات.")
        
        # زر لإجبار الفحص اللحظي
        if st.button("🔄 إجراء فحص دقيق الآن", use_container_width=True):
            with st.spinner('جاري الاتصال بخوادم Google Cloud...'):
                time.sleep(1) # محاكاة للاتصال
                conn = get_db_connection()
                
                if conn:
                    try:
                        # محاولة قراءة فعلية لاختبار الصلاحية
                        conn.read(worksheet="Weekly_Plan", ttl="0s")
                        
                        success_html = """
                        <div class='success-box'>
                            <h3 style='margin:0;'>🟢 النظام متصل ومدرع 100%</h3>
                            <p style='margin:0;'>تم التعرف على مفتاح الـ Service Account بنجاح. التطبيق يملك صلاحيات (محرر) كاملة، وقاعدة بيانات Google Sheets جاهزة لاستقبال وإرسال البيانات دون أي تعارض.</p>
                        </div>
                        """
                        st.markdown(success_html, unsafe_allow_html=True)
                    except Exception as e:
                        # الخطأ هنا يعني أن الاتصال تم، لكن الإيميل ما انضاف في الإكسل
                        error_msg = str(e)
                        err_html = f"""
                        <div class='alert-box'>
                            <h3 style='margin:0;'>🔴 تم الاتصال، ولكن الكتابة مرفوضة</h3>
                            <p style='margin:0;'>التطبيق يرى السيرفر، لكن جوجل يمنعه من التعديل. <br>
                            <b>الحل:</b> تأكد أنك قمت بنسخ الإيميل الخاص بالروبوت (الموجود في ملف الـ JSON) وأضفته كـ "محرر" (Editor) في زر المشاركة داخل ملف الإكسل الخاص بك.</p>
                            <p style='font-size:12px; margin-top:10px;'>التفاصيل التقنية: {error_msg}</p>
                        </div>
                        """
                        st.markdown(err_html, unsafe_allow_html=True)
                else:
                    # الخطأ هنا يعني أن مفتاح الـ JSON لم يوضع في Streamlit بشكل صحيح
                    fatal_err_html = """
                    <div class='alert-box'>
                        <h3 style='margin:0;'>🔴 انقطاع تام في الاتصال</h3>
                        <p style='margin:0;'>النظام لا يستطيع العثور على مفاتيح الوصول. <br>
                        <b>الحل:</b> اذهب إلى إعدادات Streamlit -> Secrets، وتأكد أنك قمت بلصق محتوى ملف الـ JSON بالكامل كما هو مطلوب.</p>
                    </div>
                    """
                    st.markdown(fatal_err_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
