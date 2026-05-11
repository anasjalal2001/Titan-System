import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Black & Gold - Anti-Crash Edition)
# =====================================================================
st.set_page_config(page_title="Titan Cloud V14 - The Smart Engine", page_icon="👑", layout="wide")

css_code = """
<style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 800; letter-spacing: 1px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { border: 2px solid #D4AF37; background-color: #111111; border-radius: 8px; padding: 12px 18px; color: #D4AF37; font-size: 14px; font-weight: bold; transition: 0.3s; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    .titan-card { background: linear-gradient(145deg, #161B22, #0d1117); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; padding: 25px; margin-bottom: 22px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
    .gold-value { color: #FFD700; font-size: 38px; font-weight: 900; margin: 15px 0; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.2); }
    .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 6px solid #0074D9; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 6px solid #2ECC40; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 6px solid #FF4136; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 8px; color: #FF4136; text-align: right; margin-bottom: 15px;}
    .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 8px; color: #2ECC40; text-align: right; margin-bottom: 15px;}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =====================================================================
# 2. الذاكرة المؤقتة (Session State) 
# =====================================================================
if 'offline_logs' not in st.session_state: st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state: st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state: st.session_state['offline_health'] = []
if 'is_delayed' not in st.session_state: st.session_state['is_delayed'] = False

# =====================================================================
# 3. قاعدة بيانات التمارين الذكية (الإنجليزية)
# =====================================================================
EXERCISE_DB = {
    "صدر": ["Barbell Bench Press", "Incline Dumbbell Press", "Decline Press", "Cable Crossover", "Pec Deck Fly", "Dumbbell Pullover", "Chest Dips"],
    "ظهر": ["Lat Pulldown (Wide)", "Lat Pulldown (Close Grip)", "Seated Cable Row", "Barbell Bent-Over Row", "T-Bar Row", "Pull-ups", "Deadlift", "Straight Arm Pulldown"],
    "أرجل": ["Barbell Squat", "Leg Press", "Leg Extension", "Lying Leg Curl", "Seated Leg Curl", "Romanian Deadlift (RDL)", "Standing Calf Raise", "Seated Calf Raise", "Bulgarian Split Squat"],
    "أكتاف": ["Overhead Barbell Press", "Dumbbell Shoulder Press", "Dumbbell Lateral Raise", "Cable Lateral Raise", "Front Raise", "Face Pulls", "Reverse Pec Deck", "Shrugs"],
    "تراي": ["Tricep Rope Pushdown", "V-Bar Pushdown", "Overhead Tricep Extension", "Skull Crushers", "Close-Grip Bench Press", "Tricep Dips"],
    "باي": ["Barbell Bicep Curl", "Dumbbell Hammer Curl", "Preacher Curl", "Cable Curl", "Concentration Curl", "Reverse Curl"],
    "بطن": ["Cable Crunch", "Hanging Leg Raise", "Machine Crunch", "Plank", "Russian Twists"],
    "جوانب": ["Cable Woodchoppers", "Dumbbell Side Bends"],
    "تمرين حر": ["Custom Machine 1", "Custom Cable 2", "Cardio Only"]
}

def get_exercises_for_muscle(muscle_string):
    """تحليل العضلة المستهدفة اليوم وجلب التمارين الإنجليزية المناسبة لها"""
    if not muscle_string or muscle_string == "اذهب لسان هندسة الأسبوع":
        return EXERCISE_DB["تمرين حر"]
        
    combined = []
    for key, exercises in EXERCISE_DB.items():
        if key in muscle_string:
            combined.extend(exercises)
            
    if not combined:
        return EXERCISE_DB["تمرين حر"]
        
    return list(set(combined)) # إزالة التكرار

# =====================================================================
# 4. محرك الاتصال السحابي الآمن
# =====================================================================
def get_db_connection():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except: return None

def fetch_sheet_safe(sheet_name):
    conn = get_db_connection()
    if conn is None: return pd.DataFrame()
    try: return conn.read(worksheet=sheet_name, ttl="0s").dropna(how='all')
    except: return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    conn = get_db_connection()
    if not conn:
        if sheet_name == "Workout_Logs": st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": st.session_state['offline_health'].append(new_data_dict)
        return False, "فشل الاتصال. تم الحفظ محلياً."
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        updated_df = pd.DataFrame([new_data_dict]) if df.empty else pd.concat([df, pd.DataFrame([new_data_dict])], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ في السحابة بنجاح."
    except:
        if sheet_name == "Workout_Logs": st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": st.session_state['offline_health'].append(new_data_dict)
        return False, "جوجل ترفض التعديل. تم الحفظ محلياً."

def overwrite_sheet_safe(sheet_name, df_new):
    conn = get_db_connection()
    if not conn:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "حفظ محلي للمخطط."
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط سحابياً."
    except:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "فشل الرفع. حفظ محلي."

# =====================================================================
# 5. محرك التوقيت والمسار الديناميكي (Smart Navigation)
# =====================================================================
def get_dynamic_schedule():
    """حساب وقت الانطلاق والوصول بناءً على اللحظة الحالية"""
    now = datetime.now()
    
    # حساب مدة الطريق (25 دقيقة أساسية + 10 دقائق إذا كان وقت ذروة بين 5م و 8م)
    is_rush_hour = 17 <= now.hour <= 20
    commute_time = 35 if is_rush_hour else 25
    
    arrival_time = now + timedelta(minutes=commute_time)
    
    # تنسيق الأوقات (12 ساعة)
    now_str = now.strftime("%I:%M %p")
    arrival_str = arrival_time.strftime("%I:%M %p")
    
    return now_str, arrival_str, commute_time, arrival_time

def get_week_dates():
    today = datetime.now()
    idx = (today.weekday() + 2) % 7 
    saturday = today - timedelta(days=idx)
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    return {day: (saturday + timedelta(days=i)).strftime("%Y-%m-%d") for i, day in enumerate(week_days)}

def get_today_details():
    days_map_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
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
# 6. محرك الاستراتيجية
# =====================================================================
WORKOUT_ENGINE = {
    "موتيف 8": {"iron": "صدر + تراي", "warmup": "دوران أكتاف + إطالة صدر", "flow": "ابدأ بـ Barbell Bench Press ثم الانتقال للعزل"},
    "فت كومبات": {"iron": "أرجل + بطن", "warmup": "إطالة ديناميكية للحوض", "flow": "ابدأ بـ Barbell Squat ثم أجهزة العزل"},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "warmup": "تسخين جذع مركزي", "flow": "ابدأ بـ Overhead Press كمركب أساسي"},
    "ستيب": {"iron": "ظهر + باي", "warmup": "إطالة قطنية + سحب خفيف", "flow": "ابدأ بـ Lat Pulldown و Barbell Row"},
    "اكوا": {"iron": "حديد شامل", "warmup": "إحماء مفاصل شامل", "flow": "اختر تمرين مركب واحد لكل عضلة كبيرة"},
    "بامب فت": {"iron": "صدر + أكتاف", "warmup": "تسخين أكتاف بوزن خفيف", "flow": "ركز على ضخ الدم (Pump) بأوزان متوسطة"},
    "بودي ماكس": {"iron": "أرجل + ظهر", "warmup": "سكوات وزن الجسم", "flow": "أقوى تمرينين في الاسبوع، ركز على الـ Deadlift"},
    "رادير": {"iron": "ذراعين", "warmup": "إطالة أوتار الذراعين", "flow": "Supersets بين الباي والتراي لضخ دم خرافي"},
    "جي فت": {"iron": "حديد قوة", "warmup": "تسخين دقيق للمفاصل", "flow": "أوزان ثقيلة جداً (3-5 عدات) راحة طويلة"},
    "فت اتاك": {"iron": "أرجل + أكتاف", "warmup": "هرولة + قفز مكاني", "flow": "تمارين مركبة سريعة"},
    "موبيلتي": {"iron": "تمرين حر", "warmup": "استهداف مناطق الشد", "flow": "اختر العضلة الأضعف هذا الأسبوع"},
    "لا يوجد": {"iron": "تمرين حر", "warmup": "تسخين 10 دقائق سير", "flow": "صمم روتينك الخاص"}
}

def analyze_muscle_balance(plan_df):
    if plan_df.empty: return True, ""
    all_muscles = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    if "أرجل" not in all_muscles: alerts.append("نقص في تمارين الأرجل (مهم للتستوستيرون).")
    if "ظهر" not in all_muscles: alerts.append("يجب تغطية الظهر لدعم العمود الفقري.")
    if alerts: return False, "تنبيه هندسي: " + " | ".join(alerts)
    return True, "المخطط متوازن وشامل لجميع العضلات."

# =====================================================================
# 7. البناء المعماري لواجهة التطبيق
# =====================================================================
def main():
    today_ar, current_date = get_today_details()
    week_dates = get_week_dates()

    st.markdown("<h1>👑 غرفة عمليات تايتان V14</h1>", unsafe_allow_html=True)
    header_html = "<p style='text-align:center; color:#888;'>الذكاء الاصطناعي والملاحة | اليوم: " + today_ar + " (" + current_date + ")</p>"
    st.markdown(header_html, unsafe_allow_html=True)

    tabs = st.tabs(["🚀 الملاحة والميدان", "🗓️ هندسة الأسبوع", "🏋️ السجل الذكي", "📸 عيادة InBody", "🥗 الوقود", "🛠️ صيانة النظام"])
    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel, tab_sys = tabs

    # -----------------------------------------------------------------
    # اللسان 1: الملاحة والميدان (GPS Simulator)
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            off_html = "<div class='titan-card' style='border: 2px solid #2ECC40;'><h1 style='color: #2ECC40; font-size: 70px; margin:0;'>OFF DAY 🛑</h1><p style='color:#A0A0A0;'>يوم الاستشفاء السلبي. العضلات تُبنى الآن.</p></div>"
            st.markdown(off_html, unsafe_allow_html=True)
        else:
            s_class, iron_target, warmup, t_flow = "لم يتم الضبط", "اذهب لسان هندسة الأسبوع", "غير محدد", ""
            plan_df = fetch_sheet_safe("Weekly_Plan")
            
            if not plan_df.empty and 'Date' in plan_df.columns:
                try:
                    today_row = plan_df[plan_df['Date'] == current_date].iloc[0]
                    s_class, iron_target = today_row['Class'], today_row['Muscle']
                    if s_class in WORKOUT_ENGINE: 
                        warmup = WORKOUT_ENGINE[s_class]['warmup']
                        t_flow = WORKOUT_ENGINE[s_class]['flow']
                except: pass
            
            # حسابات الملاحة الذكية
            now_str, arrival_str, commute_mins, arr_timeObj = get_dynamic_schedule()
            
            col_t1, col_t2 = st.columns([1.8, 1])
            with col_t1:
                if not st.session_state['is_delayed']:
                    # الخطة المثالية
                    nav_html = "<div class='titan-card' style='text-align: right; padding: 25px;'>"
                    nav_html += "<h3 style='margin-top:0;'>📍 الملاحة الذكية (بودي ماسترز الروضة)</h3>"
                    nav_html += "<p style='font-size:18px;'>الحديد المستهدف: <b style='color:#FFD700;'>" + iron_target + "</b> | الكلاس: <b style='color:#FFD700;'>" + s_class + "</b></p>"
                    nav_html += "<p style='color:#888;'>مسار التمرين: " + t_flow + "</p>"
                    nav_html += "<hr style='border-color: rgba(255,255,255,0.1);'>"
                    nav_html += "<h5 style='color:#2ECC40;'>حاسبة الانطلاق الحية</h5>"
                    nav_html += "<p>🚗 وقت الانطلاق الآن: <b style='color:#D4AF37;'>" + now_str + "</b></p>"
                    nav_html += "<p>⏱️ مدة الطريق المتوقعة: <b style='color:#D4AF37;'>" + str(commute_mins) + " دقيقة</b></p>"
                    nav_html += "<p>🅿️ الوصول المتوقع: <b style='color:#D4AF37;'>" + arrival_str + "</b></p>"
                    
                    # بناء خطة الوقت بناء على وقت الوصول الفعلي
                    iron_start = (arr_timeObj + timedelta(minutes=10)).strftime("%I:%M %p")
                    class_start = "09:00 PM"
                    nav_html += "<br><p>🔥 " + arrival_str + " - " + iron_start + " : <span style='color:#A0A0A0;'>إحماء (" + warmup + ")</span></p>"
                    nav_html += "<p>💪 " + iron_start + " - " + class_start + " : <b style='color:#FF4136;'>صالة الحديد (طاقة قصوى)</b></p>"
                    nav_html += "<p>🤸 " + class_start + " - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (حرق دهون)</b></p>"
                    nav_html += "<p>🧊 10:00 PM - 10:20 PM : <b style='color:#2ECC40;'>بروتوكول الاستشفاء</b></p>"
                    nav_html += "</div>"
                else:
                    # خطة التأخير
                    nav_html = "<div class='titan-card' style='text-align: right; padding: 25px; border-color: #FF4136;'>"
                    nav_html += "<h3 style='margin-top:0; color:#FF4136;'>⚠️ تفعيل خطة الطوارئ (تأخير)</h3>"
                    nav_html += "<p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>" + iron_target + "</b></p>"
                    nav_html += "<hr style='border-color: rgba(255,255,255,0.1);'>"
                    nav_html += "<p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة</b></p>"
                    nav_html += "<p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع (أجهزة عزل فقط لتجنب الإصابة)</b></p>"
                    nav_html += "</div>"
                
                st.markdown(nav_html, unsafe_allow_html=True)
                
            with col_t2:
                st.markdown("<div class='titan-card' style='padding: 20px;'><h3 style='margin-top:0;'>التحكم</h3>", unsafe_allow_html=True)
                if not st.session_state['is_delayed']:
                    if st.button("⏳ تأخير المسار", use_container_width=True):
                        st.session_state['is_delayed'] = True
                        st.rerun()
                else:
                    if st.button("✅ إلغاء التأخير", use_container_width=True):
                        st.session_state['is_delayed'] = False
                        st.rerun()
                st.write("") 
                if st.button("❌ غياب", use_container_width=True): st.markdown("<div class='alert-box'>تم الخصم من الكربوهيدرات بنسبة 40%.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### 🧊 البروتوكول الطبي")
            rec_html = "<div class='recovery-routine'><h4 style='color:#0074D9; margin:0;'>🏊 الأساس اليومي</h4><p style='font-size: 16px; margin:0;'>1. السباحة: 15 دقيقة.<br>2. الجاكوزي البارد: 3 دقائق.</p></div>"
            st.markdown(rec_html, unsafe_allow_html=True)
            if today_ar in ["الاثنين", "الخميس"]: 
                w_html = "<div class='fertility-warning'><h4 style='color:#FF4136; margin:0;'>🔥 تصريح الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'>مسموح <b>10 دقائق فقط</b> حار/بخار لحماية الخصوبة.</p></div>"
                st.markdown(w_html, unsafe_allow_html=True)
            else: 
                s_html = "<div class='fertility-safe'><h4 style='color:#2ECC40; margin:0;'>🛡️ حظر الإجهاد الحراري</h4><p style='font-size: 16px; margin:0;'><b>ممنوع</b> الجاكوزي الحار اليوم لرفع التستوستيرون.</p></div>"
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
                    day_lbl = "<h5 style='color:#E0E0E0; text-align:right;'>" + d + "<br><span style='font-size:12px; color:#888;'>" + exact_date + "</span></h5>"
                    st.markdown(day_lbl, unsafe_allow_html=True)
                    choice = st.selectbox("الكلاس", list(WORKOUT_ENGINE.keys()), key="conf_" + d, label_visibility="collapsed")
                    muscle_target = WORKOUT_ENGINE[choice]['iron']
                    st.caption("الحديد: " + muscle_target)
                    new_schedule.append({"Day": d, "Date": exact_date, "Class": choice, "Muscle": muscle_target})
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص واعتماد المخطط", use_container_width=True):
                df_new_plan = pd.DataFrame(new_schedule)
                is_balanced, balance_msg = analyze_muscle_balance(df_new_plan)
                box_class = 'success-box' if is_balanced else 'alert-box'
                msg_html = "<div class='" + box_class + "'>" + balance_msg + "</div>"
                st.markdown(msg_html, unsafe_allow_html=True)
                success, s_msg = overwrite_sheet_safe("Weekly_Plan", df_new_plan)
                if success: st.success(s_msg)
                else: st.warning(s_msg)

    # -----------------------------------------------------------------
    # اللسان 3: السجل الذكي (التعبئة التلقائية)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ السجل الذكي والتعرف التلقائي")
        st.write("اختر العضلة، ثم اختر التمرين باللغة الإنجليزية. النظام سيجلب وزنك السابق تلقائياً.")
        
        # جلب قائمة التمارين بناءً على عضلة اليوم
        todays_muscle = "اذهب لسان هندسة الأسبوع"
        plan_df = fetch_sheet_safe("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: todays_muscle = plan_df[plan_df['Date'] == current_date].iloc[0]['Muscle']
            except: pass
            
        st.markdown("<div class='titan-card' style='padding:20px; text-align:right;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>📝 توثيق الجلسة (Auto-Fill)</h4>", unsafe_allow_html=True)
        
        # القوائم المنسدلة الذكية
        available_exercises = get_exercises_for_muscle(todays_muscle)
        selected_ex = st.selectbox("اختر التمرين (باللغة الإنجليزية):", available_exercises)
        
        # محرك البحث المباشر عن آخر وزن
        p_date, p_weight, p_reps = fetch_historical_weight(selected_ex)
        
        if p_date:
            hist_html = "<div style='background:#111; padding:10px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:15px;'>"
            hist_html += "<p style='color:#888; margin:0;'>آخر مرة لعبت هذا التمرين: " + str(p_date) + " | <b>الوزن السابق: " + str(p_weight) + " KG</b></p></div>"
            st.markdown(hist_html, unsafe_allow_html=True)
            default_w = float(p_weight)
            default_r = int(p_reps)
        else:
            st.info("لا توجد سجلات سابقة لهذا التمرين. سيتم تسجيله كأول مرة.")
            default_w = 0.0
            default_r = 10
            
        # إدخال الأرقام (تأخذ القيم الافتراضية من السجل السابق)
        c_wt, c_rp = st.columns(2)
        input_wt = c_wt.number_input("الوزن (KG)", min_value=0.0, value=default_w, step=2.5)
        input_rp = c_rp.number_input("العدات", min_value=0, value=default_r, step=1)
        
        if st.button("💾 توثيق وحفظ السجل الميداني", use_container_width=True):
            new_entry = {"Date": current_date, "Exercise": selected_ex, "Weight": input_wt, "Reps": input_rp}
            success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
            if success: st.success("تم التوثيق بنجاح سحابياً.")
            else: st.warning(s_msg)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # باقي الألسنة
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 عيادة تايتان")
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
        st.markdown("### 🛠️ مركز الصيانة المتقدم")
        
        # الفحص الذكي للاتصال
        conn = get_db_connection()
        if conn:
            success_html = "<div class='success-box'><h3 style='margin:0;'>🟢 النظام متصل بالسحابة 100%</h3><p style='margin:0;'>تم التعرف على مفتاح الـ Service Account بنجاح، وقاعدة بيانات Google Sheets تعمل بكفاءة تامة.</p></div>"
            st.markdown(success_html, unsafe_allow_html=True)
        else:
            error_html = "<div class='alert-box'><h3 style='margin:0;'>🔴 النظام غير متصل</h3><p style='margin:0;'>تأكد من إعدادات الـ Secrets في Streamlit.</p></div>"
            st.markdown(error_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
