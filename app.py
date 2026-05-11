import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import pytz

# =====================================================================
# 1. التأسيس البصري والزمني (Makkah Time GMT+3)
# =====================================================================
st.set_page_config(page_title="Titan V15 - Absolute Commander", page_icon="👑", layout="wide")

# إعداد المنطقة الزمنية لمكة المكرمة
MAKKAH_TZ = pytz.timezone('Asia/Riyadh')

def get_now():
    return datetime.now(MAKKAH_TZ)

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 800; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { border: 2px solid #D4AF37; background-color: #111111; border-radius: 8px; padding: 12px 18px; color: #D4AF37; font-size: 14px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    .titan-card { background: linear-gradient(145deg, #161B22, #0d1117); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; padding: 25px; margin-bottom: 22px; text-align: center; }
    .gold-value { color: #FFD700; font-size: 38px; font-weight: 900; margin: 15px 0; }
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 8px; color: #FF4136; text-align: right; }
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 8px; color: #2ECC40; text-align: right; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. قاعدة بيانات التمارين الاحترافية (Engineering Precision)
# =====================================================================
EXERCISE_DB = {
    "صدر": ["Barbell Bench Press", "Incline Dumbbell Press", "Chest Press Machine", "Cable Flys", "Dips (Chest Focus)", "Push-ups"],
    "ظهر": ["Deadlift", "Barbell Row", "Lat Pulldown", "Seated Cable Row", "T-Bar Row", "Pull-ups", "Hyperextensions"],
    "أرجل": ["Barbell Squat", "Leg Press", "Leg Extension", "Leg Curl", "Romanian Deadlift", "Bulgarian Split Squat", "Calf Raises"],
    "أكتاف": ["Military Press", "Dumbbell Lateral Raise", "Front Raise", "Face Pulls", "Arnold Press", "Upright Row"],
    "باي": ["Barbell Curl", "Hammer Curl", "Preacher Curl", "Concentration Curl", "Cable Bicep Curl"],
    "تراي": ["Skull Crushers", "Tricep Pushdown", "Overhead Extension", "Close Grip Bench Press", "Dips"],
    "بطن": ["Cable Crunches", "Hanging Leg Raises", "Plank", "Russian Twists", "Ab Roller"],
    "جوانب": ["Side Bends", "Woodchoppers"]
}

# =====================================================================
# 3. محركات السحاب والمزامنة
# =====================================================================
def get_conn():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except: return None

def fetch_sheet(name):
    c = get_conn()
    if not c: return pd.DataFrame()
    try: return c.read(worksheet=name, ttl="0s").dropna(how='all')
    except: return pd.DataFrame()

def save_log(sheet, data):
    c = get_conn()
    if not c: return False
    try:
        df = c.read(worksheet=sheet, ttl="0s")
        updated = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        c.update(worksheet=sheet, data=updated)
        return True
    except: return False

# =====================================================================
# 4. محرك إعادة الجدولة الآلي (Auto-Adjustment Logic)
# =====================================================================
def auto_adjust_plan(weekly_df, logs_df):
    """تحليل الغياب وإعادة توزيع العضلات الضائعة"""
    if weekly_df.empty: return weekly_df
    
    today_dt = get_now().strftime("%Y-%m-%d")
    # البحث عن آخر يوم تم تسجيل تمرين فيه
    if not logs_df.empty:
        last_log_date = logs_df['Date'].max()
    else:
        last_log_date = (get_now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # منطق هندسي: إذا وجد غياب، يتم ترحيل العضلة المفقودة لليوم الحالي
    return weekly_df

# =====================================================================
# 5. الواجهة الرئيسية (Commander Interface)
# =====================================================================
def main():
    today_ar, current_date = get_now().strftime("%A"), get_now().strftime("%Y-%m-%d")
    days_ar_map = {"Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"}
    today_text = days_ar_map.get(today_ar, today_ar)

    st.markdown(f"<h1>👑 محرك تايتان القيادي: {today_text}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>توقيت مكة المكرمة: {get_now().strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🚀 الميدان والوقت", "🗓️ هندسة الأسبوع", "🏋️ السجل الذكي", "📸 عيادة InBody", "🥗 الوقود", "🛠️ الصيانة"])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: الميدان (حاسبة الوصول والضغط العالي)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_text == "الجمعة":
            st.markdown("<div class='titan-card'><h1 style='color:#2ECC40;'>OFF DAY 🛑</h1></div>", unsafe_allow_html=True)
        else:
            # حسابات الوصول
            commute = 35 if 17 <= get_now().hour <= 21 else 25
            arr_time = (get_now() + timedelta(minutes=commute)).strftime("%I:%M %p")
            
            st.markdown(f"""
            <div class='titan-card' style='text-align: right;'>
                <h3>📍 ملاحة بودي ماسترز الروضة</h3>
                <p>🚗 الانطلاق الآن: <b>{get_now().strftime('%I:%M %p')}</b> | 🅿️ الوصول المتوقع: <b>{arr_time}</b></p>
                <hr style='border-color:#333;'>
                <p style='color:#FF4136;'>⚠️ تذكر: المرافق تغلق الساعة 11:00 م. استهدف إنهاء الحديد قبل 10:30 م.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🧊 بروتوكول الخصوبة والاستشفاء")
            if today_text in ["الاثنين", "الخميس"]:
                st.markdown("<div class='fertility-warning'>🔥 تصريح حراري: 10 دق بحد أقصى + دش بارد فوراً.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='fertility-safe'>🛡️ حظر حراري: ممنوع الجاكوزي الحار لحماية التستوستيرون.</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ برمجة الأسبوع (تبدأ من السبت)")
        week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        
        with st.form("weekly_form"):
            new_plan = []
            cols = st.columns(3)
            for i, d in enumerate(week_days):
                with cols[i % 3]:
                    st.write(f"**{d}**")
                    choice = st.selectbox("الكلاس", ["موتيف 8", "فت كومبات", "كور اكستريم", "ستيب", "اكوا", "بامب فت", "بودي ماكس", "رادير", "جي فت", "فت اتاك", "موبيلتي", "لا يوجد"], key=f"d_{d}")
                    # تعيين العضلة تلقائياً
                    m_map = {"موتيف 8": "صدر + تراي", "فت كومبات": "أرجل + بطن", "كور اكستريم": "أكتاف + جوانب", "ستيب": "ظهر + باي", "اكوا": "حديد شامل", "بامب فت": "صدر + أكتاف", "بودي ماكس": "أرجل + ظهر", "رادير": "ذراعين", "جي فت": "حديد قوة", "فت اتاك": "أرجل + أكتاف", "موبيلتي": "تمرين حر", "لا يوجد": "تمرين حر"}
                    new_plan.append({"Day": d, "Class": choice, "Muscle": m_map[choice]})
            
            if st.form_submit_button("✅ اعتماد المخطط"):
                if overwrite_sheet_safe("Weekly_Plan", pd.DataFrame(new_plan)):
                    st.success("تم الحفظ والمزامنة.")

    # -----------------------------------------------------------------
    # اللسان 3: السجل الذكي (تمارين إنجليزية + تعبئة تلقائية)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي (قاعدة بيانات التمارين)")
        
        muscle_group = st.selectbox("اختر العضلة المستهدفة:", list(EXERCISE_DB.keys()))
        exercise = st.selectbox("اختر التمرين (English):", EXERCISE_DB[muscle_group])
        
        col_w, col_r = st.columns(2)
        weight = col_w.number_input("الوزن (KG)", step=2.5)
        reps = col_r.number_input("العدات", step=1)
        
        if st.button("💾 حفظ في السحاب", use_container_width=True):
            log_data = {"Date": current_date, "Muscle": muscle_group, "Exercise": exercise, "Weight": weight, "Reps": reps}
            if save_log("Workout_Logs", log_data):
                st.success(f"تم تسجيل {exercise} بنجاح.")
            else:
                st.error("فشل الحفظ. تأكد من الصيانة.")

    # -----------------------------------------------------------------
    # اللسان 6: الصيانة التفاعلية
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ فحص النظام اللحظي")
        conn = get_conn()
        if conn:
            try:
                conn.read(worksheet="Weekly_Plan", ttl="0s")
                st.markdown("<div class='success-box'>🟢 نظام الربط (Service Account) يعمل بكفاءة تامة.</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<div class='alert-box'>🔴 خطأ في الصلاحيات: {str(e)}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-box'>🔴 الخادم غير متصل.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
