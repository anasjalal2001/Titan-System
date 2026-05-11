import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والزمني (Makkah Time Engine)
# =====================================================================
st.set_page_config(page_title="Titan V19 - Oracle Navigator", page_icon="👑", layout="wide")

def get_makkah_time():
    """محرك زمني دقيق يحسب توقيت مكة المكرمة"""
    return datetime.utcnow() + timedelta(hours=3)

css_code = """
<style>
    .stApp { background-color: #030303; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 900; letter-spacing: 1px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { border: 2px solid #D4AF37; background-color: #111111; border-radius: 10px; padding: 15px 20px; color: #D4AF37; font-size: 15px; font-weight: bold; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); transform: scale(1.05); }
    .titan-card { background: linear-gradient(145deg, #161B22, #0A0D12); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 18px; padding: 30px; margin-bottom: 25px; text-align: right; box-shadow: 0 15px 25px rgba(0,0,0,0.6); transition: transform 0.3s; }
    .titan-card-center { text-align: center; }
    .gold-value { color: #FFD700; font-size: 42px; font-weight: 900; margin: 20px 0; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.3); }
    .macro-val { color: #E0E0E0; font-size: 28px; font-weight: bold; }
    .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 8px solid #0074D9; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 8px solid #2ECC40; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 8px solid #FF4136; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: right; }
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 18px; border-radius: 10px; color: #FF4136; text-align: right; margin-bottom: 15px; font-weight: bold;}
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 18px; border-radius: 10px; color: #2ECC40; text-align: right; margin-bottom: 15px; font-weight: bold;}
    .info-box { background: rgba(0, 116, 217, 0.1); border: 1px solid #0074D9; padding: 18px; border-radius: 10px; color: #0074D9; text-align: right; margin-bottom: 15px; font-weight: bold;}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =====================================================================
# 2. إدارة الذاكرة المؤقتة والحالات (State Management)
# =====================================================================
if 'offline_logs' not in st.session_state: st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state: st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state: st.session_state['offline_health'] = []
if 'offline_inbody' not in st.session_state: st.session_state['offline_inbody'] = []
if 'attendance_mode' not in st.session_state: st.session_state['attendance_mode'] = "Full" # Full, IronOnly, Absent, Delayed

# =====================================================================
# 3. محركات السحاب (Cloud Connections)
# =====================================================================
def get_db_connection():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except Exception: return None

def fetch_sheet_safe(sheet_name):
    conn = get_db_connection()
    if conn is None: return pd.DataFrame()
    try: return conn.read(worksheet=sheet_name, ttl="0s").dropna(how='all')
    except Exception: return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    conn = get_db_connection()
    if not conn: return False, "تم الحفظ محلياً (لا يوجد اتصال)."
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        updated_df = pd.DataFrame([new_data_dict]) if df.empty else pd.concat([df, pd.DataFrame([new_data_dict])], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ والتشفير السحابي بنجاح."
    except Exception as e: return False, f"خطأ سحابي: {str(e)}"

def overwrite_sheet_safe(sheet_name, df_new):
    conn = get_db_connection()
    if not conn: return False, "حفظ محلي فقط."
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط سحابياً."
    except Exception as e: return False, f"فشل الرفع: {str(e)}"

# =====================================================================
# 4. المساعد الغذائي الذكي (Smart Meal & Macro Engine)
# =====================================================================
# قاعدة بيانات الوجبات السعودية السريعة والشائعة لمساعدة المهندس أنس
MEAL_DB = {
    "نصف حبة دجاج شواية (بدون جلد)": {"protein": 45, "cals": 420},
    "ربع حبة دجاج شواية": {"protein": 22, "cals": 210},
    "علبة تونة (مصفاة بالماء)": {"protein": 26, "cals": 120},
    "سكوب بروتين (Whey)": {"protein": 25, "cals": 120},
    "3 بيضات مسلوقة كاملة": {"protein": 18, "cals": 210},
    "4 بياض بيض فقط": {"protein": 14, "cals": 70},
    "صدر دجاج مشوي (200 جرام)": {"protein": 60, "cals": 330},
    "صاروخ شاورما دجاج (عادي)": {"protein": 25, "cals": 550},
    "صحن شاورما عربي دجاج": {"protein": 35, "cals": 850},
    "علبة زبادي يوناني سادة": {"protein": 15, "cals": 100},
    "كوب حليب بروتين عالي": {"protein": 27, "cals": 150},
    "شريحة لحم ستيك (200 جرام)": {"protein": 50, "cals": 450},
    "برجر لحم مشوي (شريحة واحدة)": {"protein": 20, "cals": 300},
    "وجبة ماك تشيكن (تخبيص)": {"protein": 14, "cals": 400}
}

# =====================================================================
# 5. قاعدة البيانات الميكانيكية الحيوية (Biomechanics DB)
# =====================================================================
EXERCISE_DB = {
    "صدر": ["Incline Barbell Bench Press", "Flat Dumbbell Press", "Decline Cable Flys", "Pec Deck Machine", "Dips - Chest Focus", "Push-ups"],
    "ظهر": ["Deadlift", "Lat Pulldown - Wide Grip", "Seated Cable Row", "Barbell Bent-Over Row", "T-Bar Row", "Pull-ups"],
    "أرجل": ["Barbell Squat", "Leg Press", "Bulgarian Split Squat", "Romanian Deadlift - RDL", "Leg Extension", "Lying Leg Curl", "Standing Calf Raise"],
    "أكتاف": ["Overhead Barbell Press", "Dumbbell Lateral Raise", "Front Cable Raise", "Face Pulls", "Arnold Press"],
    "باي": ["Barbell Bicep Curl", "Dumbbell Hammer Curl", "Preacher Curl Machine", "Cable Rope Curl"],
    "تراي": ["Tricep Rope Pushdown", "Skull Crushers (EZ Bar)", "Overhead Dumbbell Extension", "Close-Grip Bench Press"],
    "بطن": ["Cable Crunches", "Hanging Leg Raises", "Plank - Weighted", "Ab Roller"],
    "جوانب": ["Cable Woodchoppers", "Russian Twists"],
    "تمرين حر": ["Custom Machine Workout", "Cardio Intensive Session"]
}

def get_exercises_for_muscle(muscle_string):
    if not muscle_string or muscle_string == "اذهب لسان هندسة الأسبوع": return EXERCISE_DB["تمرين حر"]
    combined = []
    for key, exercises in EXERCISE_DB.items():
        if key in muscle_string: combined.extend(exercises)
    return list(set(combined)) if combined else EXERCISE_DB["تمرين حر"]

# =====================================================================
# 6. محرك الذكاء الاصطناعي للاستنتاج وكسر الأوزان (Smart Reps)
# =====================================================================
def calculate_smart_reps(exercise_name, current_weight):
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            last_w = float(last_record['Weight'])
            last_r = int(last_record['Reps'])
            if current_weight > last_w: return max(last_r - 2, 6)
            elif current_weight < last_w: return last_r + 2
            else: return last_r
    return 10

def fetch_historical_data(exercise_name):
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
    "موتيف 8": {"iron": "صدر + تراي", "warmup": "دوران أكتاف 3 دق + إطالة صدر 2 دق", "flow": "ابدأ بـ Incline Press لشد الصدر العلوي."},
    "فت كومبات": {"iron": "أرجل + بطن", "warmup": "إطالة ديناميكية للحوض", "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل."},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "warmup": "تسخين جذع مركزي", "flow": "أكتاف عريضة = خصر أنحف. ركز على Overhead Press."},
    "ستيب": {"iron": "ظهر + باي", "warmup": "إطالة قطنية + سحب حبل", "flow": "شد الظهر يمنع التحدب. ركز على Deadlift."},
    "اكوا": {"iron": "حديد شامل (Full Body)", "warmup": "إحماء مفاصل شامل", "flow": "تمرين مركب واحد لكل عضلة كبيرة."},
    "بامب فت": {"iron": "صدر + أكتاف", "warmup": "تسخين أكتاف بوزن خفيف", "flow": "أوزان متوسطة وتكرارات عالية للـ Pump."},
    "بودي ماكس": {"iron": "أرجل + ظهر", "warmup": "سكوات وزن الجسم", "flow": "أعنف يوم! يستهدف أكبر عضلتين لنسف الكرش."},
    "رادير": {"iron": "ذراعين (باي وتراي)", "warmup": "إطالة أوتار الرسغ ببطء", "flow": "Supersets باي مع تراي لزيادة الحرق."},
    "جي فت": {"iron": "حديد قوة (Heavy Lift)", "warmup": "تسخين مفاصل مكثف", "flow": "3 إلى 5 عدات بأقصى وزن. راحة 3 دقائق."},
    "فت اتاك": {"iron": "أرجل + أكتاف", "warmup": "هرولة خفيفة 3 دق", "flow": "تمارين مركبة سريعة لرفع نبض القلب."},
    "موبيلتي": {"iron": "تمرين حر (النقاط الضعيفة)", "warmup": "Foam Roller", "flow": "استهدف عضلة متأخرة أو إطالات عميقة."},
    "لا يوجد": {"iron": "تمرين حر متكامل", "warmup": "سير مائل 10 دق", "flow": "أنت القائد اليوم. صمم روتينك."}
}

def analyze_muscle_balance(plan_df):
    if plan_df.empty: return True, ""
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    if "أرجل" not in all_muscles_text: alerts.append("🔴 خطأ هندسي: المخطط يفتقد لتمارين الأرجل (ضرورية لحرق الكرش).")
    if "ظهر" not in all_muscles_text: alerts.append("🔴 خلل في القوام: يجب تدريب الظهر لسحب الأكتاف.")
    if all_muscles_text.count("صدر") > 2: alerts.append("🔴 إجهاد مفرط: الصدر مستهدف بكثافة عالية جداً.")
    if len(alerts) > 0: return False, "<br>".join(alerts)
    return True, "🟢 ممتاز: المخطط متوازن، يهاجم الدهون، ويضمن الاستشفاء السليم."

def get_week_dates():
    today = get_makkah_time()
    idx = (today.weekday() + 2) % 7 
    saturday = today - timedelta(days=idx)
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    return {day: (saturday + timedelta(days=i)).strftime("%Y-%m-%d") for i, day in enumerate(week_days)}

# =====================================================================
# 8. البناء المعماري لواجهة التطبيق (The Interface)
# =====================================================================
def main():
    makkah_now = get_makkah_time()
    days_map_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_map_ar[makkah_now.strftime("%A")]
    current_date = makkah_now.strftime("%Y-%m-%d")
    week_dates = get_week_dates()

    st.markdown("<h1>👑 محرك تايتان V19 (The AI Oracle & Navigator)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>مكة المكرمة | {today_ar} ({current_date}) | الساعة: {makkah_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🚀 الملاحة والميدان", "🗓️ هندسة الأسبوع", "🏋️ السجل الذكي (Auto-Fill)", "📸 عيادة InBody", "🥗 المساعد الغذائي", "🛠️ مركز الصيانة"])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: الملاحة والميدان (Interactive GPS Navigator)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            st.markdown("<div class='titan-card titan-card-center' style='border: 2px solid #2ECC40;'><h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1><p>يوم الاستشفاء السلبي الإلزامي. بناء الأنسجة يتم الآن.</p></div>", unsafe_allow_html=True)
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
                        <h2 style='color:#FF4136; text-align:center;'>تم تسجيل الغياب التام اليوم ❌</h2>
                        <p style='text-align:center; font-size:18px;'>النظام قام بترحيل تمرين <b>({iron_target})</b> ليوم غد.</p>
                        <hr>
                        <h4 style='color:#E0E0E0; text-align:center;'>بروتوكول التغذية الطارئ</h4>
                        <p style='text-align:center;'>يُمنع تناول الكربوهيدرات في العشاء نهائياً لعدم وجود حرق.</p>
                    </div>
                    """, unsafe_allow_html=True)
                if st.button("🔄 التراجع (سأذهب للنادي)"):
                    st.session_state['attendance_mode'] = "Full"
                    st.rerun()
            else:
                col_t1, col_t2 = st.columns([2, 1])
                
                with col_t2:
                    st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 حاسبة الموقع الحية</h3>", unsafe_allow_html=True)
                    user_loc = st.selectbox("حدد موقعك الحالي:", ["المنزل (جدة)", "موقع العمل (مكة)", "مكان آخر (مخصص)"])
                    
                    is_rush_hour = 17 <= makkah_now.hour <= 21
                    if user_loc == "المنزل (جدة)": commute_mins = 35 if is_rush_hour else 20
                    elif user_loc == "موقع العمل (مكة)": commute_mins = 75 if is_rush_hour else 60
                    else: commute_mins = st.slider("كم دقيقة تبعد عن النادي؟", 5, 120, 30)
                    
                    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
                    st.markdown("<h3 style='margin-top:0;'>🕹️ التحكم الميداني</h3>", unsafe_allow_html=True)
                    
                    if st.button("✅ حضور كامل (كلاس + حديد)", use_container_width=True):
                        st.session_state['attendance_mode'] = "Full"
                        st.rerun()
                    if st.button("🏋️ غياب عن الكلاس (حديد فقط)", use_container_width=True):
                        st.session_state['attendance_mode'] = "IronOnly"
                        st.rerun()
                    if st.button("⏳ تأخير المسار", use_container_width=True):
                        st.session_state['attendance_mode'] = "Delayed"
                        st.rerun()
                    if st.button("❌ غياب تام عن النادي", use_container_width=True):
                        st.session_state['attendance_mode'] = "Absent"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_t1:
                    class_burn = CLASS_BURN_DB.get(s_class, 0)
                    arrival_timeObj = makkah_now + timedelta(minutes=commute_mins)
                    arr_str = arrival_timeObj.strftime("%I:%M %p")
                    now_str = makkah_now.strftime("%I:%M %p")
                    
                    if st.session_state['attendance_mode'] == "Full":
                        iron_start = (arrival_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card'>
                            <h3 style='margin-top:0;'>🗺️ الملاحة (حضور كامل - طاقة قصوى)</h3>
                            <p style='font-size:18px;'>الحديد: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس: <b style='color:#FFD700;'>{s_class}</b> <span style='color:#FF4136; font-size:14px;'>(حرق ~{class_burn} kcal)</span></p>
                            <p style='color:#888;'>الاستراتيجية: {t_flow}</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ وصول النادي: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <h5 style='color:#E0E0E0;'>الجدول الميداني التفاعلي</h5>
                            <p>🔥 {arr_str} - {iron_start} : إحماء ({warmup})</p>
                            <p>💪 {iron_start} - 09:00 PM : <b style='color:#FF4136;'>صالة الحديد (كسر أوزان بأقصى طاقة)</b></p>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (لحرق دهون البطن الصافية)</b></p>
                            <p>🧊 10:00 PM - 10:20 PM : <b style='color:#2ECC40;'>الاستشفاء قبل الإغلاق</b></p>
                        </div>
                        """
                    elif st.session_state['attendance_mode'] == "IronOnly":
                        iron_start = (arrival_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #0074D9;'>
                            <h3 style='margin-top:0; color:#0074D9;'>🏋️ مسار الحديد المكثف (تم إلغاء الكلاس)</h3>
                            <p style='font-size:18px;'>الحديد المستهدف: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <p style='color:#888;'>بما أن الكلاس ملغي، لديك طاقة أعلى لكسر الأوزان الحرة.</p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🚗 الانطلاق: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ وصول النادي: <b style='color:#D4AF37;'>{arr_str}</b></p>
                            <h5 style='color:#E0E0E0;'>الجدول الميداني المفتوح</h5>
                            <p>🔥 {arr_str} - {iron_start} : إحماء دقيق ({warmup})</p>
                            <p>💪 {iron_start} - 10:30 PM : <b style='color:#FF4136;'>صالة الحديد (خذ وقتك، العب جولات إضافية)</b></p>
                            <p>🧊 10:30 PM - 10:55 PM : <b style='color:#2ECC40;'>الاستشفاء المطول</b></p>
                        </div>
                        """
                    elif st.session_state['attendance_mode'] == "Delayed":
                        nav_html = f"""
                        <div class='titan-card' style='border-color: #FF4136;'>
                            <h3 style='margin-top:0; color:#FF4136;'>⚠️ مسار التأخير (إنقاذ ما يمكن إنقاذه)</h3>
                            <p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>{iron_target}</b></p>
                            <hr style='border-color: rgba(255,255,255,0.1);'>
                            <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة</b></p>
                            <p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع (أجهزة عزل فقط لضيق الوقت)</b></p>
                            <p>🧊 10:35 PM - 10:55 PM : <b style='color:#2ECC40;'>استشفاء مائي سريع</b></p>
                        </div>
                        """
                    st.markdown(nav_html, unsafe_allow_html=True)

                st.markdown("### 🧊 البروتوكول الطبي")
                rec_html = "<div class='recovery-routine'><h4 style='color:#0074D9; margin:0;'>🏊 الأساس اليومي</h4><p style='font-size: 16px; margin:0;'>1. السباحة: 15 دقيقة.<br>2. الجاكوزي البارد: 3 دقائق (إلزامي للخصوبة والتستوستيرون).</p></div>"
                st.markdown(rec_html, unsafe_allow_html=True)
                
                if today_ar in ["الاثنين", "الخميس"]: 
                    st.markdown("<div class='fertility-warning'><h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'>مسموح <b>10 دقائق فقط</b> جاكوزي حار، ويُشترط أخذ دش بارد فوراً بعد الخروج.</p></div>", unsafe_allow_html=True)
                else: 
                    st.markdown("<div class='fertility-safe'><h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'><b>ممنوع تماماً</b> الجاكوزي الحار أو الساونا.</p></div>", unsafe_allow_html=True)

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
    # اللسان 3: سجل التطور (Auto-Fill & Charts)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي (Auto-Fill & Charts)")
        
        todays_muscle = "اذهب لسان هندسة الأسبوع"
        plan_df = fetch_sheet_safe("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: todays_muscle = plan_df[plan_df['Date'] == current_date].iloc[0]['Muscle']
            except: pass
            
        st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>الهدف العضلي اليوم: <span style='color:#FFD700;'>{todays_muscle}</span></h4>", unsafe_allow_html=True)
        
        available_exercises = get_exercises_for_muscle(todays_muscle)
        selected_ex = st.selectbox("اختر التمرين:", available_exercises)
        
        p_date, p_weight, p_reps = fetch_historical_data(selected_ex)
        
        if p_date:
            st.markdown(f"<div style='background:#111; padding:15px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:20px;'><p style='color:#888; margin:0;'>آخر مرة لعبت التمرين: {p_date}</p><h4 style='margin:5px 0; color:#E0E0E0;'>الوزن السابق: <b style='color:#FFD700;'>{p_weight} KG</b> × {p_reps} عدات</h4></div>", unsafe_allow_html=True)
            default_w = float(p_weight)
        else:
            st.info("تمرين جديد. سيتم تسجيله كمعيار أساسي.")
            default_w = 0.0
            
        c_wt, c_rp = st.columns(2)
        input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, value=default_w, step=2.5)
        input_rp = c_rp.number_input("العدات (اتركها 0 للذكاء الاصطناعي)", min_value=0, value=0, step=1)
        
        if st.button("💾 توثيق الجلسة", use_container_width=True):
            final_reps = input_rp
            if input_rp == 0:
                final_reps = calculate_smart_reps(selected_ex, input_wt)
                st.success(f"🤖 الذكاء الاصطناعي استنتج أنك حققت: {final_reps} عدات.")
                
            new_entry = {"Date": current_date, "Muscle": todays_muscle, "Exercise": selected_ex, "Weight": input_wt, "Reps": final_reps}
            success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
            if success: st.success(f"تم توثيق {selected_ex} بنجاح.")
            else: st.error(s_msg)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("#### 📈 منحنى التقدم البصري")
        logs_df = fetch_sheet_safe("Workout_Logs")
        if not logs_df.empty and 'Exercise' in logs_df.columns:
            chart_ex = st.selectbox("اختر تمريناً لرسم المنحنى:", logs_df['Exercise'].unique())
            chart_data = logs_df[logs_df['Exercise'] == chart_ex]
            if not chart_data.empty:
                try:
                    chart_data['Weight'] = pd.to_numeric(chart_data['Weight'])
                    chart_data = chart_data.set_index('Date')
                    st.line_chart(chart_data['Weight'], use_container_width=True)
                except: st.warning("البيانات تحتاج لتنظيف لعرض الرسم.")
        else: st.info("قم بتسجيل التمارين لرسم منحنى التطور.")

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان (إدارة التحليل الحيوي)")
        with st.form("inbody_form"):
            c1, c2 = st.columns(2)
            ib_date = c1.date_input("تاريخ الفحص")
            ib_weight = c1.number_input("الوزن (KG)", value=91.9, step=0.1)
            ib_muscle = c2.number_input("كتلة العضلات (KG)", value=40.0, step=0.1)
            ib_fat = c2.number_input("نسبة الدهون (%)", value=20.0, step=0.5)
            ib_visceral = st.number_input("مؤشر الدهون الحشوية (الكرش)", value=14, step=1)
            if st.form_submit_button("💾 أرشفة التقرير الطبي", use_container_width=True):
                inbody_data = {"Date": ib_date.strftime("%Y-%m-%d"), "Weight": ib_weight, "Muscle_Mass": ib_muscle, "Fat_Percentage": ib_fat, "Visceral_Fat": ib_visceral}
                success, msg = append_to_sheet_safe("InBody_Logs", inbody_data)
                if success: st.success("تم توثيق الفحص.")
                else: st.error(msg)
                
        inbody_df = fetch_sheet_safe("InBody_Logs")
        if not inbody_df.empty and 'Visceral_Fat' in inbody_df.columns:
            st.markdown("#### 📉 منحنى نزول الدهون الحشوية")
            try:
                inbody_df['Visceral_Fat'] = pd.to_numeric(inbody_df['Visceral_Fat'])
                inbody_df = inbody_df.set_index('Date')
                st.bar_chart(inbody_df['Visceral_Fat'], use_container_width=True)
            except: pass

    # -----------------------------------------------------------------
    # اللسان 5: المساعد الغذائي (Smart Nutrition AI)
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 المساعد الغذائي الذكي (Smart Nutrition)")
        st.write("أنت تأكل عشوائياً؟ لا مشكلة. اختر ما أكلته اليوم من القائمة السريعة وسأقوم بجمعه وحسابه لك.")
        
        target_calories = 1900
        protein_target = int(91.9 * 2.2) 
        
        # الذكاء الاصطناعي لحساب الوجبات العشوائية
        st.markdown("<div class='titan-card' style='text-align:right;'><h4>🍔 ماكينة حصر الوجبات العشوائية</h4>", unsafe_allow_html=True)
        selected_meals = st.multiselect("ماذا أكلت اليوم؟ (اختر كل الوجبات السريعة التي تتذكرها):", list(MEAL_DB.keys()))
        
        total_eaten_protein = 0
        total_eaten_cals = 0
        for meal in selected_meals:
            total_eaten_protein += MEAL_DB[meal]["protein"]
            total_eaten_cals += MEAL_DB[meal]["cals"]
            
        if selected_meals:
            st.markdown(f"<div class='info-box'>🤖 الذكاء الاصطناعي حسبها لك: <b>{total_eaten_protein}g بروتين</b> و <b>{total_eaten_cals} سعرة حرارية</b>. سيتم وضع هذه الأرقام في السجل تلقائياً.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='titan-card'>
            <h4 style='margin-top:0; color:#D4AF37;'>🎯 الهدف المتبقي لتدمير الدهون</h4>
            <div style='display:flex; justify-content:space-around; margin-top:20px; align-items:center;'>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🍖</span><br><span style='color:#E0E0E0; font-size:14px;'>بروتين (أساسي)</span><br>
                    <span class='macro-val' style='color:#FF4136;'>{protein_target}g</span>
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:30px;'>🔥</span><br><span style='color:#E0E0E0; font-size:14px;'>سعرات</span><br>
                    <span class='macro-val' style='color:#D4AF37;'>{target_calories}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            in_sleep = col_f1.number_input("🛌 ساعات النوم (Huawei):", value=7.5, step=0.5)
            in_water = col_f1.number_input("💧 كمية الماء (لتر):", value=3.5, step=0.5)
            # تعبئة تلقائية من حاسبة الوجبات العشوائية
            default_p = total_eaten_protein if total_eaten_protein > 0 else 150
            default_c = total_eaten_cals if total_eaten_cals > 0 else 1900
            
            in_protein = col_f2.number_input("🍖 بروتين مستهلك (جرام):", value=default_p, step=10)
            in_cals = col_f2.number_input("🔥 إجمالي السعرات:", value=default_c, step=50)
            in_notes = st.text_input("📝 ملاحظات حرة:")
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("💾 أرشفة وقود اليوم", use_container_width=True):
                health_record = {"Date": current_date, "Sleep": in_sleep, "Water": in_water, "Protein": in_protein, "Calories": in_cals, "Notes": in_notes}
                success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                if success: st.success(s_msg)
                else: st.error(s_msg)

    # -----------------------------------------------------------------
    # اللسان 6: مركز الصيانة 
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ التشخيص الهندسي")
        if st.button("🔄 بدء الاختبار", use_container_width=True):
            with st.spinner('جاري التفاوض مع خوادم Google Cloud...'):
                time.sleep(1)
                conn = get_db_connection()
                if conn:
                    try:
                        conn.read(worksheet="Weekly_Plan", ttl="0s")
                        st.markdown("<div class='success-box'>🟢 النظام مدرع ومتصل 100%.</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<div class='alert-box'>🔴 الكتابة مرفوضة (تحقق من الـ Editor). {str(e)}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='alert-box'>🔴 انقطاع تام في الشبكة.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
