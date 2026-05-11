import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والهوية
# =====================================================================
st.set_page_config(page_title="Titan Cloud V12 - Master Suite", page_icon="👑", layout="wide")

st.markdown(
    """
    <style>
        .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
        h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 800; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
        .stTabs [data-baseweb="tab"] { border: 2px solid #D4AF37; background-color: #111111; border-radius: 8px; padding: 12px 18px; color: #D4AF37; font-size: 14px; font-weight: bold; transition: 0.3s; }
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
        .titan-card { background: linear-gradient(145deg, #161B22, #0d1117); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; padding: 25px; margin-bottom: 22px; text-align: center; }
        .gold-value { color: #FFD700; font-size: 38px; font-weight: 900; margin: 15px 0; }
        .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 6px solid #0074D9; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
        .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 6px solid #2ECC40; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
        .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 6px solid #FF4136; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
        .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 8px; color: #FF4136; text-align: right; margin-bottom: 15px;}
        .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 8px; color: #2ECC40; text-align: right; margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True
)

# =====================================================================
# 2. الذاكرة المؤقتة ومحرك السحاب
# =====================================================================
if 'offline_logs' not in st.session_state: st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state: st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state: st.session_state['offline_health'] = []

def get_db_connection():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except: return None

def fetch_sheet_safe(sheet_name):
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    try: return conn.read(worksheet=sheet_name, ttl="0s").dropna(how='all')
    except: return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    conn = get_db_connection()
    if not conn:
        if sheet_name == "Workout_Logs": st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": st.session_state['offline_health'].append(new_data_dict)
        return False, "جوجل ترفض التعديل. تم الحفظ محلياً لحين ضبط الصلاحيات (انظر قسم الصيانة)."
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        updated_df = pd.DataFrame([new_data_dict]) if df.empty else pd.concat([df, pd.DataFrame([new_data_dict])], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ في قاعدة بيانات جوجل بنجاح."
    except:
        if sheet_name == "Workout_Logs": st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": st.session_state['offline_health'].append(new_data_dict)
        return False, "جوجل ترفض التعديل. تم الحفظ محلياً لحين ضبط الصلاحيات."

def overwrite_sheet_safe(sheet_name, df_new):
    conn = get_db_connection()
    if not conn:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "فشل الرفع. تم الحفظ محلياً."
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الأسبوعي سحابياً."
    except:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "فشل الرفع. تم الحفظ محلياً."

# =====================================================================
# 3. هندسة الوقت والتاريخ
# =====================================================================
def get_week_dates():
    """حساب تواريخ الأسبوع بدءاً من يوم السبت الماضي أو الحالي"""
    today = datetime.now()
    # العثور على آخر يوم سبت (إذا كان اليوم سبت، فهو نفسه)
    idx = (today.weekday() + 2) % 7 # جعل السبت هو بداية الأسبوع
    saturday = today - timedelta(days=idx)
    
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates = {}
    for i, day in enumerate(week_days):
        date_str = (saturday + timedelta(days=i)).strftime("%Y-%m-%d")
        week_dates[day] = date_str
    return week_dates

def get_today_details():
    days_map_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_en = datetime.now().strftime("%A")
    return days_map_ar[today_en], datetime.now().strftime("%Y-%m-%d")

# =====================================================================
# 4. محرك الاستراتيجية
# =====================================================================
WORKOUT_ENGINE = {
    "موتيف 8": {"iron": "صدر + تراي", "warmup": "دوران أكتاف (Rotator Cuff) + إطالة صدر ديناميكية 5 دق"},
    "فت كومبات": {"iron": "أرجل + بطن", "warmup": "إطالة ديناميكية للحوض والركب (Leg Swings)"},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "warmup": "تسخين جذع مركزي (Core Activation)"},
    "ستيب": {"iron": "ظهر + باي", "warmup": "إطالة أسفل الظهر القطنية + سحب مطاطي خفيف"},
    "اكوا": {"iron": "حديد شامل (Full Body)", "warmup": "إحماء مفاصل شامل"},
    "بامب فت": {"iron": "صدر + أكتاف", "warmup": "تسخين أكتاف بأوزان خفيفة 2.5 كيلو"},
    "بودي ماكس": {"iron": "أرجل + ظهر", "warmup": "سكوات وزن الجسم 20 عدة + إطالة قطنية"},
    "رادير": {"iron": "ذراعين (باي وتراي)", "warmup": "إطالة أوتار الذراعين والرسغ"},
    "جي فت": {"iron": "حديد قوة (Heavy Lift)", "warmup": "تسخين دقيق ومكثف للمفاصل الكبيرة"},
    "فت اتاك": {"iron": "أرجل + أكتاف", "warmup": "هرولة خفيفة لرفع النبض + قفز مكاني"},
    "موبيلتي": {"iron": "تمرين حر (العضلة الضعيفة)", "warmup": "استهداف مناطق الشد بالـ Foam Roller"},
    "لا يوجد": {"iron": "تمرين حر متكامل", "warmup": "تسخين شامل لمدة 10 دقائق سير مائل"}
}

def analyze_muscle_balance(plan_df):
    if plan_df.empty: return True, ""
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    if "أرجل" not in all_muscles_text: alerts.append("نقص حاد في تمارين الأرجل.")
    if "ظهر" not in all_muscles_text: alerts.append("يجب تغطية الظهر لدعم العمود الفقري.")
    if all_muscles_text.count("صدر") > 2: alerts.append("إجهاد محتمل: عضلة الصدر مستهدفة أكثر من مرتين.")
        
    if alerts: return False, "تنبيه هندسي: " + " | ".join(alerts)
    return True, "المخطط متوازن وشامل لجميع العضلات وتم أرشفته بالتواريخ الدقيقة."

# =====================================================================
# 5. التطبيق الرئيسي
# =====================================================================
def main():
    today_ar, current_date = get_today_details()
    week_dates = get_week_dates()

    st.markdown("<h1>👑 غرفة عمليات تايتان V12</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>النسخة الزمنية الدقيقة | اليوم: {today_ar} ({current_date})</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🚀 الميدان والوقت", "🗓️ هندسة الأسبوع", "🏋️ سجل التطور", "📸 عيادة InBody", "🥗 الوقود والنوم", "🛠️ صيانة النظام"])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: الميدان (مع خريطة الوقت الصارمة)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            st.markdown("<div class='titan-card' style='border: 2px solid #2ECC40;'><h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1><p style='font-size: 20px; color:#A0A0A0;'>يوم الاستشفاء السلبي. لا تمرين، ولا إجهاد حراري.</p></div>", unsafe_allow_html=True)
        else:
            s_class, iron_target, warmup = "لم يتم الضبط", "اذهب لسان هندسة الأسبوع", "غير محدد"
            plan_df = fetch_sheet_safe("Weekly_Plan")
            
            if not plan_df.empty and 'Date' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Date'] == current_date].iloc[0]
                    s_class, iron_target = today_row['Class'], today_row['Muscle']
                    if s_class in WORKOUT_ENGINE: warmup = WORKOUT_ENGINE[s_class]['warmup']
                except: pass
            
            col_t1, col_t2 = st.columns([1.8, 1])
            with col_t1:
                st.markdown(f"""
                <div class='titan-card' style='text-align: right; padding: 25px;'>
                    <h3 style='margin-top:0;'>⚡ خريطة الطاقة والميدان</h3>
                    <p style='font-size:18px;'>الكلاس: <b style='color:#FFD700;'>{s_class}</b> | الحديد المستهدف: <b style='color:#FFD700;'>{iron_target}</b></p>
                    <p style='color:#888;'><i>الإحماء المطلوب: {warmup}</i></p>
                    <hr style='border-color: rgba(255,255,255,0.1);'>
                    <h5 style='color:#E0E0E0;'>الجدول الزمني الإجباري (المرافق تغلق 11:00 م)</h5>
                    <p style='margin:5px 0;'>🚗 08:10 م - 08:35 م : <span style='color:#A0A0A0;'>القيادة والوصول</span></p>
                    <p style='margin:5px 0;'>🔥 08:40 م - 08:55 م : <span style='color:#A0A0A0;'>الإحماء الحركي</span></p>
                    <p style='margin:5px 0;'>🤸 09:00 م - 09:50 م : <b style='color:#D4AF37;'>كلاس سفيان (طاقة عالية)</b></p>
                    <p style='margin:5px 0;'>💪 09:55 م - 10:35 م : <b style='color:#FF4136;'>الحديد (يُمنع قبله لضيق الوقت ولضمان هدم الألياف بعد الكارديو)</b></p>
                    <p style='margin:5px 0;'>🧊 10:35 م - 10:55 م : <b style='color:#2ECC40;'>الاستشفاء المائي قبل الإغلاق</b></p>
                </div>
                """, unsafe_allow_html=True)
            with col_t2:
                st.markdown("<div class='titan-card' style='padding: 20px;'><h3 style='margin-top:0;'>أزرار القيادة</h3>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل", use_container_width=True): st.markdown("<div class='alert-box'>تم التأجيل: اكتف بـ 5 دقائق سير.</div>", unsafe_allow_html=True)
                st.write("") 
                if st.button("❌ غياب", use_container_width=True): st.markdown("<div class='alert-box'>غياب: قلل الكربوهيدرات بالعشاء 40%.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### 🧊 البروتوكول الطبي الصارم")
            st.markdown("<div class='recovery-routine'><h4 style='color:#0074D9; margin:0;'>🏊 الأساس اليومي (الوقت يداهمك)</h4><p style='font-size: 16px; margin:0;'>1. السباحة: 15 دقيقة.<br>2. الجاكوزي البارد: 3 دقائق.</p></div>", unsafe_allow_html=True)
            if today_ar in ["الاثنين", "الخميس"]: st.markdown("<div class='fertility-warning'><h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'>مسموح <b>10 دقائق فقط</b> جاكوزي حار/بخار، ويتبعها دش بارد.</p></div>", unsafe_allow_html=True)
            else: st.markdown("<div class='fertility-safe'><h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'><b>ممنوع</b> الجاكوزي الحار هذا اليوم لحماية الخصوبة.</p></div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (مربوطة بالتواريخ وتبدأ السبت)
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ بناء المخطط الأسبوعي وتوازن العضلات")
        week_days_ordered = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        
        with st.form("weekly_master_plan"):
            new_schedule = []
            cols = st.columns(3)
            for i, d in enumerate(week_days_ordered):
                exact_date = week_dates[d]
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E0E0E0; text-align:right;'>{d}<br><span style='font-size:12px; color:#888;'>{exact_date}</span></h5>", unsafe_allow_html=True)
                    choice = st.selectbox("الكلاس", list(WORKOUT_ENGINE.keys()), key=f"conf_{d}", label_visibility="collapsed")
                    muscle_target = WORKOUT_ENGINE[choice]['iron']
                    st.caption("الحديد: " + muscle_target)
                    new_schedule.append({"Day": d, "Date": exact_date, "Class": choice, "Muscle": muscle_target})
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص واعتماد المخطط", use_container_width=True):
                df_new_plan = pd.DataFrame(new_schedule)
                is_balanced, balance_msg = analyze_muscle_balance(df_new_plan)
                st.markdown(f"<div class='{'success-box' if is_balanced else 'alert-box'}'>{balance_msg}</div>", unsafe_allow_html=True)
                success, s_msg = overwrite_sheet_safe("Weekly_Plan", df_new_plan)
                if success: st.success(s_msg)
                else: st.warning(s_msg)

    # -----------------------------------------------------------------
    # الألسنة الأخرى (نفس الهيكل الآمن)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ سجل الأوزان والذاكرة التاريخية")
        with st.form("new_log_entry", clear_on_submit=True):
            c_ex, c_wt, c_rp = st.columns([2, 1, 1])
            input_ex = c_ex.text_input("اسم التمرين")
            input_wt = c_wt.number_input("الوزن (KG)", step=2.5)
            input_rp = c_rp.number_input("العدات", step=1)
            if st.form_submit_button("💾 توثيق وحفظ הסجل"):
                if input_ex.strip() == "": st.error("أدخل اسم التمرين.")
                else:
                    new_entry = {"Date": current_date, "Exercise": input_ex.strip(), "Weight": input_wt, "Reps": input_rp}
                    success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
                    if success: st.success("تم التوثيق.")
                    else: st.warning(s_msg)

    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان للقياسات الحيوية")
        st.file_uploader("رفع تقرير InBody", type=['png', 'jpg', 'jpeg'])

    with tab_fuel:
        st.markdown("### 🥗 إدارة السعرات والنوم")
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            in_sleep = col_f1.number_input("🛌 ساعات النوم:", value=7.5, step=0.5)
            in_water = col_f1.number_input("💧 الماء (لتر):", value=3.5, step=0.5)
            in_cals = col_f2.number_input("🔥 السعرات:", value=1900, step=50)
            in_notes = col_f2.text_input("📝 ملاحظات:")
            if st.form_submit_button("💾 أرشفة السجل"):
                health_record = {"Date": current_date, "Sleep": in_sleep, "Water": in_water, "Calories": in_cals, "Notes": in_notes}
                success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                if success: st.success(s_msg)
                else: st.warning(s_msg)

    with tab_sys:
        st.markdown("### 🛠️ مركز الصيانة (إصلاح ربط جوجل)")
        st.markdown("""
        لتحل مشكلة الحفظ وتطبع البيانات في إكسل، نفذ التالي:
        1. ابحث في يوتيوب عن: **How to connect Streamlit to Google Sheets using Service Account**.
        2. من منصة (Google Cloud Console)، قم بإنشاء Service Account.
        3. قم بتنزيل ملف الـ JSON، والصق محتواه بالكامل في خانة الـ `Secrets` في Streamlit تحت رابط الشيت الخاص بك.
        4. انسخ الإيميل الموجود في ملف JSON وشاركه كـ (محرر) في ملف Google Sheets.
        """)

if __name__ == "__main__":
    main()
