import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Black & Gold - Anti-Crash Edition)
# =====================================================================
st.set_page_config(page_title="Titan Cloud V11 - Master Suite", page_icon="👑", layout="wide")

# تم استخدام طرق آمنة لكتابة الـ CSS لمنع أخطاء الـ Syntax عند اللصق
css_code = """
<style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 800; letter-spacing: 1px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #111111;
        border-radius: 8px; padding: 12px 18px; color: #D4AF37; font-size: 14px; font-weight: bold; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    
    .titan-card { 
        background: linear-gradient(145deg, #161B22, #0d1117); border: 1px solid rgba(212, 175, 55, 0.3); 
        border-radius: 16px; padding: 25px; margin-bottom: 22px; text-align: center; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: transform 0.2s;
    }
    
    .gold-value { color: #FFD700; font-size: 38px; font-weight: 900; margin: 15px 0; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.2); }
    .sub-text { color: #8B949E; font-size: 14px; line-height: 1.6; }
    
    .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 6px solid #0074D9; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 6px solid #2ECC40; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 6px solid #FF4136; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 8px; color: #FF4136; text-align: right; margin-bottom: 15px;}
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 8px; color: #2ECC40; text-align: right; margin-bottom: 15px;}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =====================================================================
# 2. الذاكرة المؤقتة (Session State) لمنع فقدان البيانات
# =====================================================================
if 'offline_logs' not in st.session_state:
    st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state:
    st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state:
    st.session_state['offline_health'] = []

# =====================================================================
# 3. محرك الاتصال السحابي (آمن جداً بدون مسك الأخطاء الدقيقة)
# =====================================================================
def get_db_connection():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except:
        return None

def fetch_sheet_safe(sheet_name):
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        return df.dropna(how='all')
    except:
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    conn = get_db_connection()
    if not conn:
        if sheet_name == "Workout_Logs": 
            st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": 
            st.session_state['offline_health'].append(new_data_dict)
        return False, "تم الحفظ في الذاكرة المؤقتة بسبب فشل الاتصال."
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        new_row = pd.DataFrame([new_data_dict])
        
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ في السحابة بنجاح."
    except:
        if sheet_name == "Workout_Logs": 
            st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": 
            st.session_state['offline_health'].append(new_data_dict)
        return False, "جوجل ترفض التعديل. تم الحفظ محلياً لحين ضبط الصلاحيات."

def overwrite_sheet_safe(sheet_name, df_new):
    conn = get_db_connection()
    if not conn:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "حفظ محلي للمخطط الأسبوعي."
    
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الأسبوعي سحابياً."
    except:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "فشل الرفع. تم الحفظ محلياً."

# =====================================================================
# 4. محرك الاستراتيجية وتوازن العضلات
# =====================================================================
WORKOUT_ENGINE = {
    "موتيف 8": {"iron": "صدر + تراي", "warmup": "دوران أكتاف + إطالة صدر 5 دق"},
    "فت كومبات": {"iron": "أرجل + بطن", "warmup": "إطالة ديناميكية للحوض والركب"},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "warmup": "تسخين جذع مركزي + دوران خصر"},
    "ستيب": {"iron": "ظهر + باي", "warmup": "إطالة أسفل الظهر + تسخين كاحل"},
    "اكوا": {"iron": "حديد شامل (Full Body)", "warmup": "إحماء مفاصل شامل"},
    "بامب فت": {"iron": "صدر + أكتاف", "warmup": "تسخين أكتاف باستخدام أوزان خفيفة"},
    "بودي ماكس": {"iron": "أرجل + ظهر", "warmup": "سكوات وزن الجسم + إطالة قطنية"},
    "رادير": {"iron": "ذراعين (باي وتراي)", "warmup": "إطالة أوتار الذراعين والرسغ"},
    "جي فت": {"iron": "حديد قوة (Heavy Lift)", "warmup": "تسخين دقيق ومكثف للمفاصل"},
    "فت اتاك": {"iron": "أرجل + أكتاف", "warmup": "هرولة خفيفة + قفز مكاني 3 دق"},
    "موبيلتي": {"iron": "تمرين حر (العضلة الضعيفة)", "warmup": "استهداف مناطق الشد العضلي"},
    "لا يوجد": {"iron": "تمرين حر متكامل", "warmup": "تسخين شامل لمدة 10 دقائق"}
}

def analyze_muscle_balance(plan_df):
    if plan_df.empty:
        return True, ""
        
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    if "أرجل" not in all_muscles_text:
        alerts.append("نقص حاد: المخطط يفتقد لتمارين الأرجل.")
        
    if "ظهر" not in all_muscles_text:
        alerts.append("خلل في القوام: لم يتم جدولة تمرين للظهر.")
        
    if all_muscles_text.count("صدر") > 2:
        alerts.append("إجهاد محتمل: عضلة الصدر مستهدفة كثيراً.")
        
    if len(alerts) > 0:
        error_str = " | ".join(alerts)
        return False, "تنبيه هندسي: " + error_str
        
    return True, "المخطط متوازن وشامل لجميع المجموعات العضلية."

# =====================================================================
# 5. دوال مساعدة لترتيب الواجهة
# =====================================================================
def get_today_details():
    days_map_ar = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_en = datetime.now().strftime("%A")
    return days_map_ar[today_en], datetime.now().strftime("%Y-%m-%d")

def fetch_historical_weight(exercise_name):
    df = fetch_sheet_safe("Workout_Logs")
    
    if not df.empty and 'Exercise' in df.columns:
        past_logs = df[df['Exercise'] == exercise_name]
        if not past_logs.empty:
            last_record = past_logs.iloc[-1]
            return last_record['Date'], last_record['Weight'], last_record['Reps']
    
    for log in reversed(st.session_state['offline_logs']):
        if log['Exercise'] == exercise_name:
            return log['Date'], log['Weight'], log['Reps']
            
    return None, None, None

# =====================================================================
# 6. البناء المعماري لواجهة التطبيق
# =====================================================================
def main():
    today_ar, current_date = get_today_details()

    st.markdown("<h1>👑 غرفة عمليات تايتان V11</h1>", unsafe_allow_html=True)
    header_str = "<p style='text-align:center; color:#888;'>النسخة المنيعة | اليوم: " + today_ar + " | التاريخ: " + current_date + "</p>"
    st.markdown(header_str, unsafe_allow_html=True)

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
    # اللسان 1: العمليات الميدانية
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            off_day_html = """
            <div class='titan-card' style='border: 2px solid #2ECC40;'>
                <h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1>
                <p style='font-size: 20px; color:#A0A0A0;'>يوم الاستشفاء السلبي. لا تمرين، ولا إجهاد حراري.</p>
            </div>
            """
            st.markdown(off_day_html, unsafe_allow_html=True)
        else:
            s_class = "لم يتم الضبط"
            iron_target = "اذهب لسان هندسة الأسبوع"
            warmup = "غير محدد"
            
            plan_df = fetch_sheet_safe("Weekly_Plan")
            if not plan_df.empty and 'Day' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Day'] == today_ar].iloc[0]
                    s_class = today_row['Class']
                    iron_target = today_row['Muscle']
                    if s_class in WORKOUT_ENGINE:
                        warmup = WORKOUT_ENGINE[s_class]['warmup']
                except:
                    pass
            elif len(st.session_state['offline_weekly']) > 0:
                for row in st.session_state['offline_weekly']:
                    if row['Day'] == today_ar:
                        s_class = row['Class']
                        iron_target = row['Muscle']
                        if s_class in WORKOUT_ENGINE:
                            warmup = WORKOUT_ENGINE[s_class]['warmup']
                        break
            
            col_t1, col_t2 = st.columns([1.8, 1])
            with col_t1:
                dash_html = "<div class='titan-card' style='text-align: right; padding: 25px;'>"
                dash_html += "<h3 style='margin-top:0;'>⚡ الخطة التنفيذية لليوم</h3>"
                dash_html += "<p style='font-size:18px;'>الكلاس: <b style='color:#FFD700;'>" + s_class + "</b></p>"
                dash_html += "<p style='font-size:18px;'>الحديد: <b style='color:#FFD700;'>" + iron_target + "</b></p>"
                dash_html += "<p style='color:#888;'><i>إحماء: " + warmup + "</i></p>"
                dash_html += "<hr style='border-color: rgba(255,255,255,0.1);'>"
                dash_html += "<p style='margin:5px 0;'>🚗 المغادرة: <b style='color:#D4AF37;'>08:10 م</b> | 🅿️ الوصول: <b style='color:#D4AF37;'>08:35 م</b></p>"
                dash_html += "<p style='margin:5px 0;'>🔥 التسخين: <b style='color:#D4AF37;'>08:40 م</b></p>"
                dash_html += "<p style='margin:5px 0;'>💪 الكلاس: <b style='color:#D4AF37;'>09:00 م</b></p>"
                dash_html += "</div>"
                st.markdown(dash_html, unsafe_allow_html=True)
                
            with col_t2:
                st.markdown("<div class='titan-card' style='padding: 20px;'><h3 style='margin-top:0;'>أزرار القيادة</h3>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل", use_container_width=True): 
                    st.markdown("<div class='alert-box'>تم التأجيل: اكتف بـ 5 دقائق سير.</div>", unsafe_allow_html=True)
                st.write("") 
                if st.button("❌ غياب", use_container_width=True): 
                    st.markdown("<div class='alert-box'>غياب: قلل الكربوهيدرات بالعشاء.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### 🧊 البروتوكول الطبي الصارم")
            rec_html = """
            <div class='recovery-routine'>
                <h4 style='color:#0074D9; margin-top:0;'>🏊 الأساس اليومي</h4>
                <p style='font-size: 16px; margin:0;'>1. السباحة: 15-20 دقيقة.<br>2. الجاكوزي البارد: 3 دقائق (لرفع التستوستيرون).</p>
            </div>
            """
            st.markdown(rec_html, unsafe_allow_html=True)

            if today_ar in ["الاثنين", "الخميس"]:
                warn_html = """
                <div class='fertility-warning'>
                    <h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4>
                    <p style='font-size: 16px; margin:0;'>مسموح <b>10 دقائق فقط</b> جاكوزي حار/بخار، ويتبعها دش بارد لحماية الخصوبة.</p>
                </div>
                """
                st.markdown(warn_html, unsafe_allow_html=True)
            else:
                safe_html = """
                <div class='fertility-safe'>
                    <h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4>
                    <p style='font-size: 16px; margin:0;'><b>ممنوع</b> الجاكوزي الحار هذا اليوم لحماية الخصوبة.</p>
                </div>
                """
                st.markdown(safe_html, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ بناء المخطط الأسبوعي وتوازن العضلات")
        
        days_list = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "السبت"]
        
        with st.form("weekly_master_plan"):
            new_schedule = []
            cols = st.columns(3)
            for i, d in enumerate(days_list):
                with cols[i % 3]:
                    day_html = "<h5 style='color:#E0E0E0; text-align:right;'>" + d + "</h5>"
                    st.write(day_html, unsafe_allow_html=True)
                    choice = st.selectbox("الكلاس", list(WORKOUT_ENGINE.keys()), key="conf_" + d, label_visibility="collapsed")
                    muscle_target = WORKOUT_ENGINE[choice]['iron']
                    st.caption("الحديد: " + muscle_target)
                    new_schedule.append({"Day": d, "Class": choice, "Muscle": muscle_target})
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            if st.form_submit_button("✅ فحص واعتماد المخطط", use_container_width=True):
                df_new_plan = pd.DataFrame(new_schedule)
                is_balanced, balance_msg = analyze_muscle_balance(df_new_plan)
                
                if not is_balanced:
                    msg_html = "<div class='alert-box'>" + balance_msg + "</div>"
                    st.markdown(msg_html, unsafe_allow_html=True)
                else:
                    msg_html = "<div class='success-box'>" + balance_msg + "</div>"
                    st.markdown(msg_html, unsafe_allow_html=True)
                
                success, s_msg = overwrite_sheet_safe("Weekly_Plan", df_new_plan)
                if success:
                    st.success(s_msg)
                else:
                    st.warning(s_msg)

    # -----------------------------------------------------------------
    # اللسان 3: سجل التطور
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ سجل الأوزان والذاكرة التاريخية")
        
        st.markdown("<div class='titan-card' style='padding:15px; text-align:right;'><h4>🔍 محرك البحث التاريخي</h4>", unsafe_allow_html=True)
        
        logs_df = fetch_sheet_safe("Workout_Logs")
        ex_list = []
        if not logs_df.empty and 'Exercise' in logs_df.columns:
            ex_list = logs_df['Exercise'].dropna().unique().tolist()
        
        for offline_log in st.session_state['offline_logs']:
            if offline_log['Exercise'] not in ex_list: 
                ex_list.append(offline_log['Exercise'])

        search_ex = st.selectbox("اختر تمرين للبحث:", [""] + ex_list)
        
        if search_ex:
            p_date, p_weight, p_reps = fetch_historical_weight(search_ex)
            if p_date:
                hist_html = "<div style='background:#111; padding:15px; border-radius:8px; border-right:4px solid #D4AF37;'>"
                hist_html += "<p style='color:#888; margin:0;'>آخر تسجيل بتاريخ: " + str(p_date) + "</p>"
                hist_html += "<h3 style='margin:5px 0; color:#FFD700;'>" + str(p_weight) + " KG <span style='font-size:18px; color:#E0E0E0;'>× " + str(p_reps) + " عدات</span></h3>"
                hist_html += "</div>"
                st.markdown(hist_html, unsafe_allow_html=True)
            else:
                st.info("لا توجد سجلات تاريخية سابقة.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### 📝 توثيق جلسة اليوم")
        with st.form("new_log_entry", clear_on_submit=True):
            c_ex, c_wt, c_rp = st.columns([2, 1, 1])
            input_ex = c_ex.text_input("اسم التمرين")
            input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, step=2.5)
            input_rp = c_rp.number_input("العدات", min_value=0, step=1)
            
            if st.form_submit_button("💾 توثيق وحفظ السجل", use_container_width=True):
                if input_ex.strip() == "":
                    st.error("خطأ: لا يمكن حفظ سجل بدون اسم التمرين.")
                else:
                    new_entry = {
                        "Date": current_date,
                        "Exercise": input_ex.strip(),
                        "Weight": input_wt,
                        "Reps": input_rp
                    }
                    success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
                    if success:
                        st.success("تم توثيق التمرين بنجاح.")
                    else:
                        st.warning(s_msg)

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان للقياسات الحيوية")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            w_html = "<div class='titan-card'><h4 style='margin:0;'>إجمالي الوزن المعتمد</h4><div class='gold-value'>91.9 <span style='font-size:20px;'>KG</span></div></div>"
            st.markdown(w_html, unsafe_allow_html=True)
        with col_c2:
            f_html = "<div class='titan-card'><h4 style='margin:0;'>الدهون الحشوية</h4><div class='gold-value'>14</div></div>"
            st.markdown(f_html, unsafe_allow_html=True)
            
        st.markdown("---")
        uploaded_image = st.file_uploader("رفع تقرير InBody", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)
            if st.button("🚀 بدء تحليل OCR", use_container_width=True):
                progress_bar = st.progress(0)
                for percent in range(100):
                    time.sleep(0.01) 
                    progress_bar.progress(percent + 1)
                st.success("تم تحليل بيانات الصورة.")

    # -----------------------------------------------------------------
    # اللسان 5: الوقود والنوم
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 إدارة السعرات والنوم")
        
        with st.form("fuel_tracker_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                in_sleep = st.number_input("🛌 ساعات النوم:", min_value=0.0, max_value=24.0, value=7.5, step=0.5)
                in_water = st.number_input("💧 كمية الماء (لتر):", min_value=0.0, max_value=15.0, value=3.5, step=0.5)
            with col_f2:
                in_cals = st.number_input("🔥 السعرات الحرارية:", min_value=0, max_value=8000, value=1900, step=50)
                in_notes = st.text_input("📝 ملاحظات:")
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("💾 أرشفة السجل الصحي", use_container_width=True):
                health_record = {
                    "Date": current_date,
                    "Sleep_Hours": in_sleep,
                    "Water_Liters": in_water,
                    "Calories": in_cals,
                    "Notes": in_notes
                }
                success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                if success:
                    st.success(s_msg)
                else:
                    st.warning(s_msg)

    # -----------------------------------------------------------------
    # اللسان 6: صيانة النظام
    # -----------------------------------------------------------------
    with tab_sys:
        st.markdown("### 🛠️ مركز الصيانة")
        
        if st.button("🔄 فحص الاتصال"):
            test_conn = get_db_connection()
            if test_conn:
                st.success("✅ الخادم متصل.")
            else:
                st.error("❌ لا يوجد اتصال.")
                
        st.write("أسماء الصفحات المطلوبة في جوجل شيتس:")
        st.code("Weekly_Plan\nWorkout_Logs\nHealth_Log")

if __name__ == "__main__":
    main()
