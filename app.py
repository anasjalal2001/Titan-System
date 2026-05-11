import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Black & Gold - Honor Magic 6 Pro Optimized)
# =====================================================================
st.set_page_config(page_title="Titan Cloud V10 - Master Suite", page_icon="👑", layout="wide")

# CSS شامل ومفصل للتحكم في كل بكسل في الشاشة لضمان عدم تداخل العناصر
st.markdown("""
<style>
    /* الإعدادات الأساسية للخلفية والخطوط */
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    
    /* تصميم الألسنة العلوية (Tabs) بشكل احترافي للجوال */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #111111;
        border-radius: 8px; padding: 12px 18px; color: #D4AF37; font-size: 14px; font-weight: bold; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    
    /* البطاقات التفاعلية (Cards) */
    .titan-card { 
        background: linear-gradient(145deg, #161B22, #0d1117); border: 1px solid rgba(212, 175, 55, 0.3); 
        border-radius: 16px; padding: 25px; margin-bottom: 22px; text-align: center; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: transform 0.2s;
    }
    .titan-card:hover { transform: translateY(-2px); border-color: rgba(212, 175, 55, 0.8); }
    
    /* النصوص والأرقام البارزة */
    .gold-value { color: #FFD700; font-size: 38px; font-weight: 900; margin: 15px 0; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.2); }
    .sub-text { color: #8B949E; font-size: 14px; line-height: 1.6; }
    
    /* بروتوكولات الاستشفاء والطب (تنسيق لوني دقيق) */
    .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 6px solid #0074D9; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 6px solid #2ECC40; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 6px solid #FF4136; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    
    /* صناديق التنبيهات الخاصة */
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 8px; color: #FF4136; text-align: right; margin-bottom: 15px;}
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 8px; color: #2ECC40; text-align: right; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. الذاكرة المؤقتة (Session State Initialization)
# =====================================================================
# هذا الجزء يضمن أن التطبيق لا ينهار أبداً حتى لو فشل الاتصال بجوجل
if 'offline_logs' not in st.session_state:
    st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state:
    st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state:
    st.session_state['offline_health'] = []

# =====================================================================
# 3. محرك الاتصال السحابي (المدرع ضد الأخطاء)
# =====================================================================
def get_db_connection():
    """محاولة الاتصال بالسحاب مع معالجة صامتة للأخطاء لمنع الانهيار"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception as e:
        return None

def fetch_sheet_safe(sheet_name):
    """جلب البيانات بأمان. إذا فشل، يعيد جدول فارغ لكي تستمر الواجهة بالعمل"""
    conn = get_db_connection()
    if conn is None: return pd.DataFrame()
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        # تنظيف البيانات من القيم الفارغة التي قد تسبب أخطاء
        return df.dropna(how='all')
    except Exception as e:
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """إضافة سطر جديد بأمان. إذا فشل السحاب، يحفظ في الذاكرة المؤقتة"""
    conn = get_db_connection()
    if not conn:
        # حفظ محلي (Offline Fallback)
        if sheet_name == "Workout_Logs": st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": st.session_state['offline_health'].append(new_data_dict)
        return False, "تم الحفظ في الذاكرة المؤقتة (فشل الاتصال السحابي)."
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        new_row = pd.DataFrame([new_data_dict])
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ في قاعدة بيانات جوجل بنجاح."
    except Exception as e:
        return False, f"جوجل ترفض التعديل. تأكد من صلاحيات المحرر. الخطأ: {e}"

def overwrite_sheet_safe(sheet_name, df_new):
    """استبدال كامل للبيانات (يستخدم للجدول الأسبوعي)"""
    conn = get_db_connection()
    if not conn:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "حفظ محلي فقط للجدول الأسبوعي."
    
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الأسبوعي سحابياً."
    except Exception as e:
        return False, f"فشل رفع المخطط الأسبوعي. الخطأ: {e}"

# =====================================================================
# 4. محرك الاستراتيجية وتوازن العضلات (النسخة المفصلة)
# =====================================================================
# القاموس المفصل لكل كلاس، يشمل الحديد المستهدف، والتسخين المطلوب
WORKOUT_ENGINE = {
    "موتيف 8": {"iron": "صدر + تراي", "warmup": "دوران أكتاف + إطالة صدر 5 دق"},
    "فت كومبات": {"iron": "أرجل + بطن", "warmup": "إطالة ديناميكية للحوض والركب"},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "warmup": "تسخين جذع مركزي + دوران خصر"},
    "ستيب": {"iron": "ظهر + باي", "warmup": "إطالة أسفل الظهر + تسخين كاحل"},
    "اكوا": {"iron": "حديد شامل (Full Body)", "warmup": "إحماء مفاصل شامل"},
    "بامب فت": {"iron": "صدر + أكتاف", "warmup": "تسخين أكتاف باستخدام أوزان خفيفة"},
    "بودي ماكس": {"iron": "أرجل + ظهر", "warmup": "سكوات وزن الجسم + إطالة قطنية"},
    "رادير": {"iron": "ذراعين (باي وتراي)", "warmup": "إطالة أوتار الذراعين والرسغ"},
    "جي فت": {"iron": "حديد قوة (Heavy Lift)", "warmup": "تسخين دقيق ومكثف للمفاصل الكبيرة"},
    "فت اتاك": {"iron": "أرجل + أكتاف", "warmup": "هرولة خفيفة + قفز مكاني"},
    "موبيلتي": {"iron": "تمرين حر (العضلة الضعيفة)", "warmup": "استهداف مناطق الشد العضلي"},
    "لا يوجد": {"iron": "تمرين حر متكامل", "warmup": "حسب العضلة المختارة"}
}

def analyze_muscle_balance(plan_df):
    """دالة هندسية تفحص الجدول الأسبوعي للتأكد من تغطية جميع العضلات وتجنب الإرهاق"""
    if plan_df.empty: return True, ""
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    
    alerts = []
    # فحص الأرجل
    if "أرجل" not in all_muscles_text:
        alerts.append("⚠️ نقص حاد: المخطط يفتقد لتمارين الأرجل الأساسية. هذا يضعف إفراز هرمون النمو.")
    # فحص الظهر
    if "ظهر" not in all_muscles_text:
        alerts.append("⚠️ خلل في القوام: لم يتم جدولة تمرين للظهر. مهم لدعم العمود الفقري.")
    # فحص التكرار المفرط (Overtraining)
    if all_muscles_text.count("صدر") > 2:
        alerts.append("⚠️ إجهاد محتمل: عضلة الصدر مستهدفة أكثر من مرتين. قد يؤدي لتمزقات.")
        
    if alerts:
        return False, "<br>".join(alerts)
    return True, "✅ المخطط متوازن، جميع العضلات الكبيرة مغطاة بشكل ممتاز."

# =====================================================================
# 5. دوال مساعدة لترتيب الواجهة وحسابات الوقت
# =====================================================================
def get_today_details():
    """جلب معلومات اليوم الحالي بدقة لضمان التزامن الميداني"""
    days_map_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_en = datetime.now().strftime("%A")
    return days_map_ar[today_en], datetime.now().strftime("%Y-%m-%d")

def fetch_historical_weight(exercise_name):
    """البحث في السجلات القديمة لإيجاد آخر وزن للتمرين المحدد"""
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            return last_record['Date'], last_record['Weight'], last_record['Reps']
    
    # البحث في السجل المؤقت المحلي (لو كان النت مفصول)
    for log in reversed(st.session_state['offline_logs']):
        if log['Exercise'] == exercise_name:
            return log['Date'], log['Weight'], log['Reps']
            
    return None, None, None

# =====================================================================
# 6. البناء المعماري لواجهة التطبيق (The Core Engine)
# =====================================================================
def main():
    today_ar, current_date = get_today_details()

    # الترويسة الرئيسية للغرفة
    st.markdown(f"<h1>👑 غرفة عمليات تايتان V10</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>النسخة المدرعة | اليوم: {today_ar} | التاريخ: {current_date}</p>", unsafe_allow_html=True)

    # تقسيم الشاشة إلى 6 ألسنة شاملة الصيانة
    tabs = st.tabs([
        "🚀 العمليات המيدانية", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ سجل التطور", 
        "📸 عيادة InBody", 
        "🥗 الوقود والنوم",
        "🛠️ صيانة النظام"
    ])
    
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: العمليات الميدانية والتحكم اللحظي (Dashboard)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            # يوم راحة كامل مبرمج مسبقاً ولا يتأثر بالسحاب
            st.markdown("""
            <div class='titan-card' style='border: 2px solid #2ECC40;'>
                <h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1>
                <p style='font-size: 20px; color:#A0A0A0;'>اليوم هو يوم الاستشفاء السلبي. لا تمرين، لا إجهاد حراري.<br>استمتع بوقتك، بناء العضلات والخصوبة يحدث الآن.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # محاولة جلب خطة اليوم من السحاب أو المحلي
            s_class, iron_target, warmup = "لم يتم الضبط", "اذهب لسان هندسة الأسبوع", "غير محدد"
            
            plan_df = fetch_sheet_safe("Weekly_Plan")
            if not plan_df.empty and 'Day' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Day'] == today_ar].iloc[0]
                    s_class = today_row['Class']
                    iron_target = today_row['Muscle']
                    # استخراج التسخين من القاموس
                    if s_class in WORKOUT_ENGINE:
                        warmup = WORKOUT_ENGINE[s_class]['warmup']
                except: pass
            
            # قسم التوقيت الميداني
            col_t1, col_t2 = st.columns([1.8, 1])
            with col_t1:
                st.markdown(f"""
                <div class='titan-card' style='text-align: right; padding: 25px;'>
                    <h3 style='margin-top:0;'>⚡ الخطة التنفيذية لليوم</h3>
                    <p style='font-size:18px;'>الكلاس المجدول: <b style='color:#FFD700;'>{s_class}</b></p>
                    <p style='font-size:18px;'>تمرين الحديد: <b style='color:#FFD700;'>{iron_target}</b></p>
                    <p style='color:#888;'><i>إحماء مخصص: {warmup}</i></p>
                    <hr style='border-color: rgba(255,255,255,0.1);'>
                    <h5 style='color:#E0E0E0;'>الجدول الزمني للتحرك (بودي ماسترز)</h5>
                    <p style='margin:5px 0;'>🚗 المغادرة: <b style='color:#D4AF37;'>08:10 م</b> | 🅿️ الوصول: <b style='color:#D4AF37;'>08:35 م</b></p>
                    <p style='margin:5px 0;'>🔥 التسخين: <b style='color:#D4AF37;'>08:40 م</b> (10 سير + 10 أوبتيكال)</p>
                    <p style='margin:5px 0;'>💪 الكلاس: <b style='color:#D4AF37;'>09:00 م</b></p>
                </div>
                """, unsafe_allow_html=True)
            with col_t2:
                # أزرار الطوارئ التفاعلية
                st.markdown("<div class='titan-card' style='padding: 20px;'><h3 style='margin-top:0;'>أزرار القيادة</h3>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل (زحمة طريق)", use_container_width=True): 
                    st.markdown("<div class='alert-box'>تم تفعيل بروتوكول التأخير: اقطع الأوبتيكال فوراً واكتفِ بـ 5 دقائق سير مائل كإحماء سريع لتدارك الكلاس.</div>", unsafe_allow_html=True)
                st.write("") 
                if st.button("❌ غياب واعتذار", use_container_width=True): 
                    st.markdown("<div class='alert-box'>تم تسجيل الغياب. <b>أمر طبي:</b> قم بتقليل الكربوهيدرات بنسبة 40% في وجبة العشاء لعدم وجود حرق.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # --- قسم البروتوكول الطبي الدقيق (الخصوبة والاستشفاء) ---
            st.markdown("### 🧊 البروتوكول الطبي الصارم (لا مجال للتجاوز)")
            
            st.markdown("""
            <div class='recovery-routine'>
                <h4 style='color:#0074D9; margin-top:0;'>🏊 الأساس اليومي الثابت (الاستشفاء العميق)</h4>
