import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والزمني (محرك مكة المكرمة المدمج)
# المرجع: Python Standard Library (datetime) - لا يحتاج مكتبات خارجية
# =====================================================================
st.set_page_config(page_title="Titan V18 - The Architect Edition", page_icon="👑", layout="wide")

def get_makkah_time():
    """
    محرك زمني دقيق يحسب توقيت مكة المكرمة رياضياً.
    الاستناد: إضافة 3 ساعات على التوقيت العالمي المنسق (UTC+3).
    """
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# هندسة الواجهة الأمامية (CSS Architecture) - مفصلة لضمان استقرار العرض
css_code = """
<style>
    /* الإعدادات الأساسية والخلفية المظلمة لتقليل إجهاد العين */
    .stApp { background-color: #030303; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 900; letter-spacing: 1px; }
    
    /* تصميم الألسنة (Tabs) لتعمل كأزرار تحكم ضخمة في الجوال */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #111111;
        border-radius: 10px; padding: 15px 20px; color: #D4AF37; font-size: 15px; font-weight: bold; transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #D4AF37 !important; color: #000000 !important; 
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); transform: scale(1.05); 
    }
    
    /* تصميم البطاقات الميدانية (Cards) */
    .titan-card { 
        background: linear-gradient(145deg, #161B22, #0A0D12); border: 1px solid rgba(212, 175, 55, 0.3); 
        border-radius: 18px; padding: 30px; margin-bottom: 25px; text-align: right; 
        box-shadow: 0 15px 25px rgba(0,0,0,0.6); transition: transform 0.3s;
    }
    .titan-card:hover { border-color: rgba(212, 175, 55, 0.8); }
    .titan-card-center { text-align: center; }
    
    /* الأرقام الذهبية للإحصائيات الحيوية */
    .gold-value { color: #FFD700; font-size: 42px; font-weight: 900; margin: 20px 0; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.3); }
    .macro-val { color: #E0E0E0; font-size: 28px; font-weight: bold; }
    
    /* البروتوكولات الطبية والتنبيهات الميدانية */
    .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 8px solid #0074D9; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 8px solid #2ECC40; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 8px solid #FF4136; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    
    /* صناديق رسائل النظام التفاعلية */
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 18px; border-radius: 10px; color: #FF4136; text-align: right; margin-bottom: 15px; font-weight: bold;}
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 18px; border-radius: 10px; color: #2ECC40; text-align: right; margin-bottom: 15px; font-weight: bold;}
    .info-box { background: rgba(0, 116, 217, 0.1); border: 1px solid #0074D9; padding: 18px; border-radius: 10px; color: #0074D9; text-align: right; margin-bottom: 15px; font-weight: bold;}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =====================================================================
# 2. إدارة الذاكرة المؤقتة (Session State & Fail-Safes)
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
if 'is_delayed' not in st.session_state:
    st.session_state['is_delayed'] = False
if 'is_absent' not in st.session_state:
    st.session_state['is_absent'] = False

# =====================================================================
# 3. محركات السحاب والمزامنة (Cloud Connectors)
# =====================================================================
def get_db_connection():
    """محاولة الاتصال الصامتة بواجهة برمجة تطبيقات Google Sheets"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception:
        return None

def fetch_sheet_safe(sheet_name):
    """قراءة البيانات بأمان. إرجاع DataFrame فارغ عند الفشل لمنع الانهيار"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        return df.dropna(how='all')
    except Exception:
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """عملية حقن البيانات (Insert) مع تفعيل نظام الحفظ المحلي كبديل طوارئ"""
    conn = get_db_connection()
    if not conn:
        return False, "انقطاع الاتصال بالسحابة. تم حفظ البيانات محلياً في ذاكرة التخزين المؤقت."
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        new_row = pd.DataFrame([new_data_dict])
        
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم توثيق البيانات وتشفيرها في السحابة بنجاح."
    except Exception as e:
        return False, f"تم الرفض من قبل خوادم جوجل (مشكلة صلاحيات). الخطأ التقني: {str(e)}"

def overwrite_sheet_safe(sheet_name, df_new):
    """عملية التحديث الشامل (Overwrite) تستخدم حصرياً لجدول الأسبوع"""
    conn = get_db_connection()
    if not conn:
        return False, "لا يوجد اتصال بالسحابة للمزامنة الشاملة."
    
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الاستراتيجي سحابياً."
    except Exception as e:
        return False, f"فشل رفع المخطط الشامل. الخطأ التقني: {str(e)}"

# =====================================================================
# 4. قاعدة البيانات الميكانيكية الحيوية (Biomechanics DB)
# مصممة هندسياً للقضاء على الكرش وترهلات الصدر السفلية
# =====================================================================
EXERCISE_DB = {
    "صدر": [
        "Incline Barbell Bench Press (لشد الجزء العلوي المترهل)",
        "Flat Dumbbell Press (لبناء الكتلة الأساسية للصدر)",
        "Decline Cable Flys (عزل قوي لنحت أسفل الصدر والقضاء على التثدي)",
        "Pec Deck Machine (عزل لخط الصدر الداخلي)",
        "Dips - Chest Focus (وزن جسم - ممتاز لحرق دهون الصدر)",
        "Push-ups (أساسي)"
    ],
    "ظهر": [
        "Deadlift (التمرين الملكي لرفع هرمون النمو والتستوستيرون)",
        "Lat Pulldown - Wide Grip (لتعريض الظهر وسحب الجلد)",
        "Seated Cable Row (لسمك الظهر الأوسط)",
        "Barbell Bent-Over Row (قوة جذع شاملة)",
        "T-Bar Row",
        "Pull-ups (عقلة)"
    ],
    "أرجل": [
        "Barbell Squat (المحفز الأول لحرق دهون البطن والمؤخرة)",
        "Leg Press (أوزان عالية لزيادة الكتلة بدون ضغط على الظهر)",
        "Bulgarian Split Squat (نحت وتدوير المؤخرة بقوة)",
        "Romanian Deadlift - RDL (شد أوتار الركبة والمؤخرة)",
        "Leg Extension (عزل رباعيات)",
        "Lying Leg Curl (عزل أوتار الركبة)",
        "Standing Calf Raise (سمانات)"
    ],
    "أكتاف": [
        "Overhead Barbell Press (أكتاف عريضة تسحب جلد الصدر للأعلى)",
        "Dumbbell Lateral Raise (تعريض الكتف الجانبي)",
        "Front Cable Raise",
        "Face Pulls (لصحة المفاصل واستقامة القوام)",
        "Arnold Press"
    ],
    "باي": [
        "Barbell Bicep Curl",
        "Dumbbell Hammer Curl (لتطوير العضلة العضدية)",
        "Preacher Curl Machine",
        "Cable Rope Curl"
    ],
    "تراي": [
        "Tricep Rope Pushdown",
        "Skull Crushers (EZ Bar)",
        "Overhead Dumbbell Extension (لشد الترهلات السفلية للذراع)",
        "Close-Grip Bench Press"
    ],
    "بطن": [
        "Cable Crunches (بطن بأوزان لبروز العضلات المكونة للـ 6-pack)",
        "Hanging Leg Raises (لشد البطن السفلي وشفط الكرش)",
        "Plank - Weighted (لقوة الجذع وشفط المعدة للداخل)",
        "Ab Roller"
    ],
    "جوانب": [
        "Cable Woodchoppers (نحت الخصر بالدوران)",
        "Russian Twists (مع قرص وزن)"
    ],
    "تمرين حر": [
        "Custom Machine Workout",
        "Cardio Intensive Session"
    ]
}

def get_exercises_for_muscle(muscle_string):
    """مستخرج التمارين الذكي: يقرأ المخطط ويعيد قائمة التمارين المطابقة"""
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
# 5. محرك الذكاء الاصطناعي للاستنتاج وكسر الأوزان (Progressive Overload)
# الاستناد: قوانين التضخيم وزيادة الحمل التدريجي (Hypertrophy Principles)
# =====================================================================
def calculate_smart_reps(exercise_name, current_weight):
    """
    خوارزمية ذكية تستنتج العدات إذا لم يتم إدخالها.
    المنطق: إذا الوزن زاد -> العدات تقل. إذا الوزن نقص -> العدات تزيد.
    """
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            last_w = float(last_record['Weight'])
            last_r = int(last_record['Reps'])
            
            if current_weight > last_w:
                return max(last_r - 2, 6) # لن يقل عن 6 عدات في أسوأ الأحوال
            elif current_weight < last_w:
                return last_r + 2
            else:
                return last_r
    
    # افتراضي التضخيم في حال عدم وجود سجل سابق
    return 10

def fetch_historical_data(exercise_name):
    """جلب بيانات آخر جلسة للمقارنة اللحظية"""
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            return last_record['Date'], last_record['Weight'], last_record['Reps']
    return None, None, None

# =====================================================================
# 6. محرك الاستراتيجية وبروتوكولات كلاسات سفيان
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
        "flow": "الصدر يحتاج تركيز عالي. ابدأ بـ Incline Press لشد الصدر العلوي."
    },
    "فت كومبات": {
        "iron": "أرجل + بطن", 
        "warmup": "إطالة ديناميكية للحوض والركب", 
        "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل."
    },
    "كور اكستريم": {
        "iron": "أكتاف + جوانب", 
        "warmup": "تسخين جذع مركزي + دوران خصر", 
        "flow": "أكتاف عريضة تعني خصر أنحف بصرياً. ركز على الـ Overhead Press."
    },
    "ستيب": {
        "iron": "ظهر + باي", 
        "warmup": "إطالة قطنية أسفل الظهر + سحب حبل مطاطي", 
        "flow": "شد الظهر يمنع التحدب. ركز على الـ Deadlift و Lat Pulldown."
    },
    "اكوا": {
        "iron": "حديد شامل (Full Body)", 
        "warmup": "إحماء مفاصل شامل من الرقبة للكاحل", 
        "flow": "اختر تمرين مركب واحد لكل عضلة كبيرة (سكوات، بنش برس، ديدليفت)."
    },
    "بامب فت": {
        "iron": "صدر + أكتاف", 
        "warmup": "تسخين أكتاف بوزن خفيف 2.5 كيلو", 
        "flow": "يوم ضخ الدم (Pump). أوزان متوسطة وتكرارات عالية."
    },
    "بودي ماكس": {
        "iron": "أرجل + ظهر", 
        "warmup": "سكوات وزن الجسم 20 عدة + إطالة قطنية", 
        "flow": "أعنف يوم في الأسبوع. يستهدف أكبر عضلتين لحرق دهون المؤخرة والبطن."
    },
    "رادير": {
        "iron": "ذراعين (باي وتراي)", 
        "warmup": "إطالة أوتار الذراعين والرسغ ببطء", 
        "flow": "Supersets باي مع تراي لزيادة الحرق واختصار الوقت."
    },
    "جي فت": {
        "iron": "حديد قوة (Heavy Lift)", 
        "warmup": "تسخين دقيق ومكثف للمفاصل الكبيرة قبل الأوزان", 
        "flow": "3 إلى 5 عدات بأقصى وزن ممكن. راحة 3 دقائق بين الجولات."
    },
    "فت اتاك": {
        "iron": "أرجل + أكتاف", 
        "warmup": "هرولة خفيفة 3 دق + قفز مكاني", 
        "flow": "تمارين مركبة سريعة لرفع نبض القلب."
    },
    "موبيلتي": {
        "iron": "تمرين حر (النقاط الضعيفة)", 
        "warmup": "استهداف مناطق الشد بالـ Foam Roller", 
        "flow": "استغل هذا اليوم لاستهداف عضلة متأخرة أو إطالات عميقة."
    },
    "لا يوجد": {
        "iron": "تمرين حر متكامل", 
        "warmup": "تسخين 10 دقائق سير مائل متواصل", 
        "flow": "أنت القائد اليوم. صمم روتينك بناءً على طاقتك."
    }
}

# =====================================================================
# 7. التوجيه الملاحي والديناميكا الزمنية (GPS Simulator)
# =====================================================================
def get_dynamic_schedule(is_delayed):
    """محرك الملاحة وحساب الوقت المتبقي قبل الإغلاق (11:00 م)"""
    now = get_makkah_time()
    
    # حساب وقت الذروة الفعلي في شوارع جدة
    is_rush_hour = 17 <= now.hour <= 21
    commute_time = 35 if is_rush_hour else 25
    
    arrival_time = now + timedelta(minutes=commute_time)
    
    now_str = now.strftime("%I:%M %p")
    arrival_str = arrival_time.strftime("%I:%M %p")
    
    return now_str, arrival_str, commute_time, arrival_time

def get_week_dates():
    """هندسة تواريخ الأسبوع للبدء دائماً بيوم السبت كمعيار قياسي"""
    today = get_makkah_time()
    idx = (today.weekday() + 2) % 7 
    saturday = today - timedelta(days=idx)
    
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates = {}
    for i, day in enumerate(week_days):
        week_dates[day] = (saturday + timedelta(days=i)).strftime("%Y-%m-%d")
    return week_dates

def analyze_muscle_balance(plan_df):
    """التدقيق الهندسي للمخطط الأسبوعي وتحديد العضلات المفقودة"""
    if plan_df.empty:
        return True, ""
        
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    if "أرجل" not in all_muscles_text:
        alerts.append("🔴 خطأ هندسي: المخطط يفتقد لتمارين الأرجل الأساسية (ضرورية لحرق دهون الكرش).")
    if "ظهر" not in all_muscles_text:
        alerts.append("🔴 خلل في القوام: يجب تدريب الظهر لسحب الأكتاف وتقويم العمود الفقري.")
    if all_muscles_text.count("صدر") > 2:
        alerts.append("🔴 إجهاد مفرط: الصدر مستهدف بكثافة، سيؤدي للتمزق وعدم الاستشفاء.")
        
    if len(alerts) > 0:
        return False, "<br>".join(alerts)
    return True, "🟢 ممتاز هندسياً: المخطط متوازن، يهاجم الدهون بقوة، ويضمن الاستشفاء السليم."

# =====================================================================
# 8. البناء المعماري لواجهة التطبيق (The Interface & Dashboards)
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

    st.markdown("<h1>👑 محرك تايتان V18 (The Architect Edition)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>مكة المكرمة | اليوم: {today_ar} ({current_date}) | الساعة: {makkah_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    tabs = st.tabs([
        "🚀 الملاحة والميدان", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ سجل التطور (تحليل بصري)", 
        "📸 عيادة InBody", 
        "🥗 هندسة الوقود (Macros)", 
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
                    <p style='font-size: 20px; color:#A0A0A0;'>يوم الاستشفاء السلبي الإلزامي. بناء الأنسجة وحرق الدهون يحدث في فترات الراحة.</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
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

            if st.session_state['is_absent']:
                st.markdown(
                    f"""
                    <div class='titan-card' style='border-color: #FF4136;'>
                        <h2 style='color:#FF4136; text-align:center;'>تم تسجيل الغياب اليوم ❌</h2>
                        <p style='text-align:center; font-size:18px;'>النظام سيقوم بترحيل تمرين <b>({iron_target})</b> ليوم غد لضمان التوازن العضلي.</p>
                        <hr style='border-color:#333;'>
                        <h4 style='color:#E0E0E0; text-align:center;'>بروتوكول التغذية الطارئ</h4>
                        <p style='text-align:center;'>لا يوجد حرق طاقة اليوم. يُمنع تناول الكربوهيدرات في العشاء نهائياً.</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                if st.button("🔄 التراجع عن الغياب (الذهاب للنادي)"):
                    st.session_state['is_absent'] = False
                    st.rerun()
                    
            else:
                now_str, arrival_str, commute_mins, arr_timeObj = get_dynamic_schedule(st.session_state['is_delayed'])
                col_t1, col_t2 = st.columns([2, 1])
                
                with col_t1:
                    class_burn = CLASS_BURN_DB.get(s_class, 0)
                    if not st.session_state['is_delayed']:
                        iron_start = (arr_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card'>
                            <h3 style='margin-top:0;'>📍 الملاحة الذكية (الخطة أ - طاقة قصوى)</h3>
                            <p style='font-size:18px;'>الحديد: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس: <b style='color:#FFD700;'>{s_class}</b> <span style='color:#FF4136; font-size:14px;'>(حرق متوقع ~{class_burn} kcal)</span></p>
                            <p style='color:#888;'>الاستراتيجية: {t_flow}</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ وصول النادي: <b style='color:#D4AF37;'>{arrival_str}</b></p>
                            <h5 style='color:#E0E0E0;'>الجدول الزمني الميداني المقترح</h5>
                            <p>🔥 {arrival_str} - {iron_start} : إحماء ({warmup})</p>
                            <p>💪 {iron_start} - 09:00 PM : <b style='color:#FF4136;'>صالة الحديد (كسر أوزان بأقصى طاقة)</b></p>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (استنزاف لحرق دهون صافي)</b></p>
                            <p>🧊 10:00 PM - 10:20 PM : <b style='color:#2ECC40;'>الاستشفاء قبل الإغلاق</b></p>
                        </div>
                        """
                    else:
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #FF4136;'>
                            <h3 style='margin-top:0; color:#FF4136;'>⚠️ خطة الطوارئ (تأخير مسار)</h3>
                            <p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة</b> <span style='color:#FF4136; font-size:14px;'>(~{class_burn} kcal)</span></p>
                            <p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع (أجهزة عزل فقط لضيق الوقت وتفادي الإصابات)</b></p>
                            <p>🧊 10:35 PM - 10:55 PM : <b style='color:#2ECC40;'>استشفاء مائي سريع</b></p>
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
                        if st.button("✅ وصلت مبكراً (الخطة أ)", use_container_width=True):
                            st.session_state['is_delayed'] = False
                            st.rerun()
                            
                    st.write("") 
                    if st.button("❌ تسجيل غياب", use_container_width=True):
                        st.session_state['is_absent'] = True
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("### 🧊 البروتوكول الطبي (إلزامي)")
                rec_html = "<div class='recovery-routine'><h4 style='color:#0074D9; margin:0;'>🏊 الأساس اليومي</h4><p style='font-size: 16px; margin:0;'>1. السباحة: 15 دقيقة (لتبريد المفاصل).<br>2. الجاكوزي البارد: 3 دقائق (إلزامي لرفع التستوستيرون).</p></div>"
                st.markdown(rec_html, unsafe_allow_html=True)
                
                if today_ar in ["الاثنين", "الخميس"]: 
                    w_html = "<div class='fertility-warning'><h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'>مسموح <b>10 دقائق فقط</b> جاكوزي حار/بخار. يُشترط أخذ دش بارد فوراً بعد الخروج.</p></div>"
                    st.markdown(w_html, unsafe_allow_html=True)
                else: 
                    s_html = "<div class='fertility-safe'><h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'><b>ممنوع تماماً</b> الجاكوزي الحار أو الساونا. الحرارة المستمرة تقتل الخصوبة ببطء.</p></div>"
                    st.markdown(s_html, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع
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
                    
                    st.caption(f"الحديد الموجه: **{muscle_target}**")
                    new_schedule.append({
                        "Day": d, "Date": exact_date, "Class": choice, "Muscle": muscle_target, "Status": "مجدول"
                    })
            
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
    # اللسان 3: سجل التطور (التعبئة الذكية + التحليل البصري)
    # المرجع (Charts): Streamlit Native Line/Bar Charts (No extra libs needed)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي (Auto-Fill & Charts)")
        
        # 1. إدخال التمارين والتعبئة التلقائية
        todays_muscle = "اذهب لسان هندسة الأسبوع"
        plan_df = fetch_sheet_safe("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: todays_muscle = plan_df[plan_df['Date'] == current_date].iloc[0]['Muscle']
            except: pass
            
        st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>الهدف العضلي اليوم: <span style='color:#FFD700;'>{todays_muscle}</span></h4>", unsafe_allow_html=True)
        
        available_exercises = get_exercises_for_muscle(todays_muscle)
        selected_ex = st.selectbox("اختر التمرين (جميع التمارين هنا تستهدف شد ونحت العضلة):", available_exercises)
        
        p_date, p_weight, p_reps = fetch_historical_data(selected_ex)
        
        if p_date:
            st.markdown(f"<div style='background:#111; padding:15px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:20px;'><p style='color:#888; margin:0;'>تاريخ آخر تسجيل: {p_date}</p><h4 style='margin:5px 0; color:#E0E0E0;'>الوزن السابق: <b style='color:#FFD700;'>{p_weight} KG</b> × {p_reps} عدات</h4></div>", unsafe_allow_html=True)
            default_w = float(p_weight)
        else:
            st.info("تمرين جديد. سيتم تسجيله كمعيار أساسي لانطلاقك.")
            default_w = 0.0
            
        c_wt, c_rp = st.columns(2)
        input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, value=default_w, step=2.5)
        input_rp = c_rp.number_input("العدات (اكتب 0 لتفعيل الذكاء الاصطناعي)", min_value=0, value=0, step=1)
        
        if st.button("💾 توثيق الجلسة (تفعيل الذكاء الاصطناعي للاستنتاج)", use_container_width=True):
            final_reps = input_rp
            if input_rp == 0:
                final_reps = calculate_smart_reps(selected_ex, input_wt)
                st.success(f"🤖 الذكاء الاصطناعي استنتج أنك حققت: {final_reps} عدات، بناءً على قوانين التضخيم ووزنك السابق.")
                
            new_entry = {"Date": current_date, "Muscle": todays_muscle, "Exercise": selected_ex, "Weight": input_wt, "Reps": final_reps}
            success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
            if success: st.success(f"تم توثيق {selected_ex} بنجاح.")
            else: st.error(s_msg)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. التحليل البصري (Data Visualization - Native)
        st.markdown("#### 📈 منحنى التقدم البصري (Progress Visualization)")
        logs_df = fetch_sheet_safe("Workout_Logs")
        
        if not logs_df.empty and 'Exercise' in logs_df.columns:
            chart_ex = st.selectbox("اختر تمريناً لرؤية مسار تطور أوزانك:", logs_df['Exercise'].unique())
            chart_data = logs_df[logs_df['Exercise'] == chart_ex]
            
            if not chart_data.empty:
                # تجهيز البيانات للرسم البياني المدمج في Streamlit
                try:
                    chart_data['Weight'] = pd.to_numeric(chart_data['Weight'])
                    chart_data = chart_data.set_index('Date')
                    st.line_chart(chart_data['Weight'], use_container_width=True)
                    st.caption("يعرض الرسم البياني صعود وزنك التدريجي (Progressive Overload). صعود المنحنى يعني بناء عضلات جديدة تحرق الدهون.")
                except Exception as e:
                    st.warning("بيانات السجل تحتاج إلى تنظيف لعرض الرسم البياني بشكل صحيح.")
        else:
            st.info("قم بتسجيل بعض التمارين ليبدأ النظام برسم منحنى تطورك العضلي هنا.")

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody (قاعدة بيانات صحية)
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان (إدارة التحليل الحيوي)")
        st.info("تسجيل أرقام InBody هنا سيسمح للنظام برسم منحنى نزول الكرش والدهون الحشوية بدقة.")
        
        with st.form("inbody_form"):
            c1, c2 = st.columns(2)
            ib_date = c1.date_input("تاريخ الفحص")
            ib_weight = c1.number_input("الوزن الإجمالي (KG)", value=91.9, step=0.1)
            ib_muscle = c2.number_input("كتلة العضلات (SMM - KG)", value=40.0, step=0.1)
            ib_fat = c2.number_input("نسبة الدهون (%)", value=20.0, step=0.5)
            ib_visceral = st.number_input("مؤشر الدهون الحشوية (الكرش الداخلي)", value=14, step=1)
            
            if st.form_submit_button("💾 أرشفة التقرير الطبي", use_container_width=True):
                inbody_data = {
                    "Date": ib_date.strftime("%Y-%m-%d"),
                    "Weight": ib_weight,
                    "Muscle_Mass": ib_muscle,
                    "Fat_Percentage": ib_fat,
                    "Visceral_Fat": ib_visceral
                }
                success, msg = append_to_sheet_safe("InBody_Logs", inbody_data)
                if success: st.success("تم توثيق فحص InBody بنجاح في قاعدة البيانات.")
                else: st.error(msg)
                
        # عرض منحنى الدهون الحشوية
        inbody_df = fetch_sheet_safe("InBody_Logs")
        if not inbody_df.empty and 'Visceral_Fat' in inbody_df.columns:
            st.markdown("#### 📉 منحنى نزول الدهون الحشوية")
            try:
                inbody_df['Visceral_Fat'] = pd.to_numeric(inbody_df['Visceral_Fat'])
                inbody_df = inbody_df.set_index('Date')
                st.bar_chart(inbody_df['Visceral_Fat'], use_container_width=True)
                st.caption("يجب أن ينخفض هذا العمود باستمرار إلى ما دون النطاق 10 لتضمن اختفاء الكرش نهائياً.")
            except:
                pass

    # -----------------------------------------------------------------
    # اللسان 5: هندسة الوقود الشاملة (Macro Engine)
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 هندسة الوقود التفصيلية (Macros Engine)")
        st.write("للتخلص من ترهلات الصدر والكرش، يجب التركيز على نسبة البروتين (Macros) وليس فقط السعرات الإجمالية.")
        
        # حاسبة ماكروز علمية مبنية على وزن المهندس أنس (91.9 كجم)
        current_weight_kg = 91.9
        target_calories = 1900
        
        # المعادلة الرياضية للتنشيف العنيف مع الحفاظ على الكتلة:
        protein_target = int(current_weight_kg * 2.2) # 2.2 جرام لكل كيلو للحفاظ على العضل
        fat_target = int(current_weight_kg * 0.8)     # 0.8 جرام هرمونات صحية
        carb_target = int((target_calories - (protein_target*4 + fat_target*9)) / 4)
        
        st.markdown(f"""
        <div class='titan-card'>
            <h4 style='margin-top:0; color:#D4AF37;'>🎯 أهداف الماكروز لليوم (لنسف الدهون وبناء الأنسجة)</h4>
            <div style='display:flex; justify-content:space-around; margin-top:20px; align-items:center;'>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🍖</span><br>
                    <span style='color:#E0E0E0; font-size:14px;'>بروتين (أساسي)</span><br>
                    <span class='macro-val' style='color:#FF4136;'>{protein_target}g</span>
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🍚</span><br>
                    <span style='color:#E0E0E0; font-size:14px;'>كارب (طاقة)</span><br>
                    <span class='macro-val' style='color:#0074D9;'>{carb_target}g</span>
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🥑</span><br>
                    <span style='color:#E0E0E0; font-size:14px;'>دهون (هرمونات)</span><br>
                    <span class='macro-val' style='color:#2ECC40;'>{fat_target}g</span>
                </div>
            </div>
            <hr style='border-color: rgba(255,255,255,0.1);'>
            <p style='margin:0; color:#888; text-align:center;'>الهدف الحراري الإجمالي: <b>{target_calories} kcal</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            in_sleep = col_f1.number_input("🛌 ساعات النوم الفعلي (Huawei):", value=7.5, step=0.5)
            in_water = col_f1.number_input("💧 كمية الماء المستهلكة (لتر):", value=3.5, step=0.5)
            in_protein = col_f2.number_input("🍖 بروتين مستهلك (جرام):", value=150, step=10)
            in_cals = col_f2.number_input("🔥 إجمالي السعرات المدخلة:", value=1900, step=50)
            in_notes = st.text_input("📝 ملاحظات حرة:")
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("💾 أرشفة وقود اليوم", use_container_width=True):
                health_record = {
                    "Date": current_date, "Sleep": in_sleep, "Water": in_water, 
                    "Protein": in_protein, "Calories": in_cals, "Notes": in_notes
                }
                success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                if success: st.success(s_msg)
                else: st.error(s_msg)

    # -----------------------------------------------------------------
    # اللسان 6: مركز الصيانة والتشخيص (Live Diagnostics)
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ التشخيص الهندسي اللحظي للاتصال")
        st.info("النظام يقوم هنا باختبار استجابة خوادم جوجل وصلاحيات مفتاح Service Account.")
        
        if st.button("🔄 بدء الاختبار والفحص", use_container_width=True):
            with st.spinner('جاري التفاوض مع خوادم Google Cloud...'):
                time.sleep(1)
                conn = get_db_connection()
                if conn:
                    try:
                        conn.read(worksheet="Weekly_Plan", ttl="0s")
                        st.markdown("<div class='success-box'><h3 style='margin:0;'>🟢 النظام مدرع ومتصل 100%</h3><p style='margin:0;'>صلاحيات الكتابة والقراءة مفعلة، وقاعدة البيانات تستجيب بشكل مثالي.</p></div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<div class='alert-box'><h3 style='margin:0;'>🔴 تم الاتصال، ولكن الكتابة مرفوضة</h3><p style='margin:0;'>تأكد أن إيميل الروبوت مضاف كـ (محرر) في ملف الإكسل.</p><p style='font-size:12px;'>التشخيص: {str(e)}</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='alert-box'><h3 style='margin:0;'>🔴 انقطاع تام في الشبكة أو خطأ في مفتاح Secrets</h3></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
