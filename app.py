import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time
import math

# =====================================================================
# 1. CORE ARCHITECTURE & SYSTEM INITIALIZATION
# =====================================================================

st.set_page_config(
    page_title="Titan V36 - Enterprise Monolith", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_makkah_time():
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# =====================================================================
# 2. ADVANCED FRONTEND ENGINEERING (CSS Architecture)
# =====================================================================

def inject_custom_css():
    css_code = (
        "<style>\n"
        ".stApp { background-color: #050505; color: #F0F0F0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }\n"
        "h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 900; letter-spacing: 1px; margin-bottom: 15px; }\n"
        ".stTabs [data-baseweb='tab-list'] { gap: 8px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap; }\n"
        ".stTabs [data-baseweb='tab'] { border: 2px solid #D4AF37; background-color: #0A0A0A; border-radius: 12px; padding: 12px 18px; color: #D4AF37; font-size: 15px; font-weight: bold; transition: all 0.3s ease; }\n"
        ".stTabs [aria-selected='true'] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); transform: scale(1.05); }\n"
        ".titan-card { background: linear-gradient(145deg, #11151A, #080A0F); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 20px; padding: 30px; margin-bottom: 25px; text-align: right; box-shadow: 0 15px 25px rgba(0,0,0,0.8); }\n"
        ".titan-card-center { text-align: center; }\n"
        ".gold-value { color: #FFD700; font-size: 40px; font-weight: 900; margin: 15px 0; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.3); }\n"
        ".macro-val { color: #E0E0E0; font-size: 28px; font-weight: bold; }\n"
        ".medical-hot { background: rgba(255, 65, 54, 0.05); border-right: 6px solid #FF4136; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: right; }\n"
        ".medical-cold { background: rgba(0, 116, 217, 0.05); border-right: 6px solid #0074D9; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: right; }\n"
        ".medical-swim { background: rgba(46, 204, 64, 0.05); border-right: 6px solid #2ECC40; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: right; }\n"
        ".medical-warning { background: rgba(255, 133, 27, 0.05); border-right: 6px solid #FF851B; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: right; }\n"
        ".alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 10px; color: #FF4136; text-align: right; margin-bottom: 15px; font-weight: bold; }\n"
        ".success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 10px; color: #2ECC40; text-align: right; margin-bottom: 15px; font-weight: bold; }\n"
        ".bio-good { color: #2ECC40; font-weight: bold; }\n"
        ".bio-bad { color: #FF4136; font-weight: bold; }\n"
        ".bio-breath { color: #0074D9; font-weight: bold; }\n"
        ".bio-tech { color: #FFD700; font-weight: bold; }\n"
        "</style>"
    )
    st.markdown(css_code, unsafe_allow_html=True)

inject_custom_css()

# =====================================================================
# 3. ROBUST SESSION STATE MANAGEMENT & APP AUTO-HEAL
# =====================================================================
def initialize_session_states():
    if 'attendance_mode' not in st.session_state or not isinstance(st.session_state['attendance_mode'], str): 
        st.session_state['attendance_mode'] = "Full"
    if 'selected_origin_loc' not in st.session_state or not isinstance(st.session_state['selected_origin_loc'], str): 
        st.session_state['selected_origin_loc'] = "المنزل (جدة - المروة)"
    if 'daily_protein' not in st.session_state: st.session_state['daily_protein'] = 0
    else:
        try: st.session_state['daily_protein'] = int(st.session_state['daily_protein'])
        except: st.session_state['daily_protein'] = 0
    if 'daily_cals' not in st.session_state: st.session_state['daily_cals'] = 0
    else:
        try: st.session_state['daily_cals'] = int(st.session_state['daily_cals'])
        except: st.session_state['daily_cals'] = 0
    if 'swim_cals_burned' not in st.session_state: st.session_state['swim_cals_burned'] = 0
    else:
        try: st.session_state['swim_cals_burned'] = int(st.session_state['swim_cals_burned'])
        except: st.session_state['swim_cals_burned'] = 0

def force_program_reset():
    st.cache_resource.clear()
    st.cache_data.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]

initialize_session_states()

# =====================================================================
# 4. CLOUD DATABASE CONNECTORS (Google Sheets) & EXCEL AUTO-HEAL
# =====================================================================
@st.cache_resource(ttl="10m")
def get_db_connection():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except Exception: return None

def run_excel_auto_heal():
    report = []
    conn = get_db_connection()
    if not conn:
        report.append({"status": "error", "msg": "🔴 انقطاع الاتصال بالسحابة. لا يمكن تنفيذ الإصلاح الذاتي."})
        return report
        
    schemas = {
        "Weekly_Plan": ["Day", "Date", "Class", "Muscle", "Status"],
        "Workout_Logs": ["Date", "Muscle", "Exercise", "Weight", "Reps"],
        "Health_Log": ["Date", "Sleep", "Water", "Protein", "Calories", "Notes"],
        "InBody_Logs": ["Date", "Weight", "Muscle_Mass", "Fat_Percentage", "Visceral_Fat"]
    }
    
    for sheet_name, required_cols in schemas.items():
        try:
            df = conn.read(worksheet=sheet_name, ttl="0s")
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                for col in missing_cols: df[col] = ""
                conn.update(worksheet=sheet_name, data=df)
                report.append({"status": "success", "msg": f"🛠️ الإصلاح الذاتي: تم حقن الأعمدة الناقصة في ورقة `{sheet_name}`."})
            else:
                report.append({"status": "success", "msg": f"🟢 الورقة `{sheet_name}` سليمة بنيوياً 100%."})
        except Exception:
            empty_df = pd.DataFrame(columns=required_cols)
            try:
                conn.update(worksheet=sheet_name, data=empty_df)
                report.append({"status": "success", "msg": f"🛠️ الإصلاح الذاتي: تم بناء ورقة `{sheet_name}` المفقودة."})
            except Exception as creation_error:
                report.append({"status": "error", "msg": f"🔴 فشل البناء لورقة `{sheet_name}`. تأكد من صلاحية المحرر. الخطأ: {str(creation_error)}"})
    return report

def fetch_sheet_safe(sheet_name):
    conn = get_db_connection()
    if conn is None: return pd.DataFrame()
    try: return conn.read(worksheet=sheet_name, ttl="0s").dropna(how='all')
    except Exception: return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    conn = get_db_connection()
    if not conn: return False, "لا يوجد اتصال، لم يتم الحفظ."
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        if df.empty: updated_df = pd.DataFrame([new_data_dict])
        else: updated_df = pd.concat([df, pd.DataFrame([new_data_dict])], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم التوثيق والتشفير بنجاح."
    except Exception as e: return False, f"تم الرفض من جوجل: {str(e)}"

def overwrite_sheet_safe(sheet_name, df_new):
    conn = get_db_connection()
    if not conn: return False, "فشل الاتصال."
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الاستراتيجي."
    except Exception as e: return False, f"فشل الرفع الشامل: {str(e)}"

# =====================================================================
# 5. INTERNAL ROUTING ENGINE
# =====================================================================
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_smart_eta(origin_name):
    dest_lat, dest_lon = 21.5768, 39.1620 
    if origin_name == "المنزل (جدة - المروة)": origin_lat, origin_lon, base_speed = 21.6214, 39.1989, 50
    elif origin_name == "العمل (جدة)": origin_lat, origin_lon, base_speed = 21.5200, 39.1700, 40
    elif origin_name == "العمل (مكة المكرمة)": origin_lat, origin_lon, base_speed = 21.4225, 39.8262, 90 
    else: origin_lat, origin_lon, base_speed = 21.6214, 39.1989, 50
    
    distance_km = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    base_time_mins = (distance_km / base_speed) * 60
    hour = get_makkah_time().hour
    
    if 7 <= hour <= 9: multiplier = 1.5
    elif 13 <= hour <= 15: multiplier = 1.6
    elif 17 <= hour <= 21: multiplier = 1.8
    else: multiplier = 1.1
        
    return int(base_time_mins * multiplier) + 5, distance_km

# =====================================================================
# 6. CLINICAL RECOVERY PROTOCOL (Fixed Markdown Rendering)
# =====================================================================
def get_medical_recovery_protocol(is_high_intensity):
    if is_high_intensity:
        html = (
            "<div class='titan-card'>\n"
            "<h3 style='margin-top:0;'>🏥 العيادة الطبية (بروتوكول اليوم العنيف)</h3>\n"
            "<p style='color:#888; text-align:right;'>المجهود عالي (تمارين أرجل أو مقاومة عنيفة). حمض اللاكتيك متراكم. سنطبق (العلاج التبايني).</p>\n"
            "<div class='medical-hot'>\n"
            "<h4 style='color:#FF4136; margin:0;'>🔥 المرحلة 1: التوسيع الوعائي (Vasodilation)</h4>\n"
            "<p style='margin-top:5px; font-size:15px;'>الهدف: ضخ الدم المحمل بالغذاء للعضلات الممزقة.</p>\n"
            "<ul style='font-size:14px;'>\n"
            "<li><b>غرفة البخار (Steam Room):</b> من 5 إلى 8 دقائق. (أفضل من الساونا الجافة لترطيب الشعب الهوائية).</li>\n"
            "<li><b>أو الجاكوزي الحار:</b> 5 دقائق متواصلة.</li>\n"
            "</ul>\n"
            "</div>\n"
            "<div class='medical-cold'>\n"
            "<h4 style='color:#0074D9; margin:0;'>🧊 المرحلة 2: الانقباض الوعائي (Vasoconstriction)</h4>\n"
            "<p style='margin-top:5px; font-size:15px;'>الهدف: عصر الدم الفاسد وحمض اللاكتيك وتقليل الالتهاب.</p>\n"
            "<ul style='font-size:14px;'>\n"
            "<li><b>الجاكوزي البارد:</b> انزل مباشرة من الحار إلى البارد لمدة دقيقة إلى دقيقتين فقط.</li>\n"
            "</ul>\n"
            "</div>\n"
            "<div class='medical-warning'>\n"
            "<h4 style='color:#FF851B; margin:0;'>⚠️ تحذير طبي للخصوبة (Fertility & CNS)</h4>\n"
            "<p style='margin-top:5px; font-size:15px;'>كرر الانتقال بين الحار والبارد <b>3 مرات متتالية</b>. <br><br><b>قاعدة طبية صارمة:</b> يجب أن تنهي الدورة (بالماء البارد). الخروج وجسمك حار يرفع حرارة الخصيتين ويدمر التستوستيرون.</p>\n"
            "</div>\n"
            "</div>"
        )
    else:
        html = (
            "<div class='titan-card'>\n"
            "<h3 style='margin-top:0;'>🏥 العيادة الطبية (بروتوكول التبريد العميق)</h3>\n"
            "<p style='color:#888; text-align:right;'>المجهود متوسط. سنركز على الاستشفاء النشط ورفع المناعة.</p>\n"
            "<div class='medical-swim'>\n"
            "<h4 style='color:#2ECC40; margin:0;'>🏊 المرحلة 1: الاستشفاء النشط (Active Recovery)</h4>\n"
            "<p style='margin-top:5px; font-size:15px;'>الهدف: تحريك المفاصل بدون ضغط أو أوزان.</p>\n"
            "<ul style='font-size:14px;'>\n"
            "<li><b>السباحة الهادئة:</b> 15 إلى 20 دقيقة سباحة حرة مستمرة لفكفكة تيبس فقرات الظهر.</li>\n"
            "</ul>\n"
            "</div>\n"
            "<div class='medical-cold'>\n"
            "<h4 style='color:#0074D9; margin:0;'>🧊 المرحلة 2: التبريد العميق (Cold Exposure)</h4>\n"
            "<p style='margin-top:5px; font-size:15px;'>الهدف: رفع مستويات التستوستيرون وتقوية المناعة.</p>\n"
            "<ul style='font-size:14px;'>\n"
            "<li><b>الجاكوزي البارد:</b> 3 إلى 5 دقائق متواصلة. التركيز على التنفس العميق.</li>\n"
            "</ul>\n"
            "</div>\n"
            "<div class='medical-warning'>\n"
            "<h4 style='color:#FF851B; margin:0;'>🚫 حظر حراري (No Heat Protocol)</h4>\n"
            "<p style='margin-top:5px; font-size:15px;'><b>يُمنع منعاً باتاً</b> الدخول للساونا، البخار، أو الجاكوزي الحار اليوم. الحرارة المتكررة تسبب جفافاً يمنع حرق دهون الكرش.</p>\n"
            "</div>\n"
            "</div>"
        )
    return html

# =====================================================================
# 7. BIOMECHANICS & EXERCISE DATABASE
# =====================================================================
def get_biomechanics_db():
    db = {
        "صدر": [
            {
                "name": "Incline Barbell Bench Press", 
                "reps": "6-8 عدات (للتضخيم وبناء الكتلة)",
                "technique": "اضبط الدكة على زاوية 30 درجة فقط. انزل بالبار حتى يلمس أعلى صدرك ببطء، وادفع بقوة.",
                "breathing": "خذ شهيق عميق وأنت تنزل بالبار، وازفر الهواء بقوة وأنت تدفع للأعلى.",
                "good_pain": "أعلى الصدر، والجزء الأمامي من الكتف.",
                "bad_pain": "ألم وخز في مفصل الكتف الداخلي (كوعك مفتوح 90 درجة، ضمه للداخل زاوية 45)."
            },
            {
                "name": "Flat Dumbbell Press", 
                "reps": "8-10 عدات (كتلة شاملة)",
                "technique": "استلقِ على الدكة المسطحة. ادفع الدنابل للأعلى مع إبقاء الكوع للداخل قليلاً لتقليل الضغط على الكتف.",
                "breathing": "شهيق في النزول، زفير في الدفع.",
                "good_pain": "منتصف الصدر وعمقه.",
                "bad_pain": "ألم في الرسغ (يجب أن يكون الرسغ مستقيماً غير مثني) أو الكوع."
            },
            {
                "name": "Decline Cable Flys", 
                "reps": "12-15 عدة (للنحت والقضاء على التثدي)",
                "technique": "قف في منتصف الكيبل. اسحب المقابض من الأعلى إلى الأسفل باتجاه حوضك واعصر عضلة الصدر في الأسفل.",
                "breathing": "شهيق عند فتح الذراعين، زفير عند العصر في الأسفل.",
                "good_pain": "أسفل الصدر، والخط الفاصل بين الصدرين.",
                "bad_pain": "ألم في الكتف الأمامي (هذا يعني أنك تدفع الكيبل دفعاً ولا تقوم بحركة 'العناق')."
            },
            {
                "name": "Pec Deck Machine", 
                "reps": "12-15 عدة (عزل الخط الداخلي)",
                "technique": "اجلس وظهرك ملتصق بالمسند. ضم المقابض حتى تتلامس واعصر صدرك. افتح ببطء.",
                "breathing": "شهيق عند الفتح، زفير عند الضم.",
                "good_pain": "عمق الصدر والخط الداخلي.",
                "bad_pain": "ألم في مفصل الكتف (يعني أن الوزن أثقل من قدرتك وأنك تستخدم كتفك للضم)."
            },
            {
                "name": "Dips - Chest Focus", 
                "reps": "حتى الفشل العضلي (وزن جسم)",
                "technique": "مل بجذعك للأمام قليلاً وانزل حتى يصبح كتفك بموازاة كوعك، ثم ادفع.",
                "breathing": "شهيق في النزول، زفير في الصعود.",
                "good_pain": "الصدر السفلي والترايسبس.",
                "bad_pain": "ألم شديد في عظمة القص (منتصف الصدر)، يحدث إذا نزلت بعمق مبالغ فيه."
            },
            {
                "name": "Push-ups", 
                "reps": "15-20 عدة (لضخ الدم النهائي)",
                "technique": "حافظ على استقامة ظهرك وحوضك. انزل حتى يلامس صدرك الأرض.",
                "breathing": "شهيق في النزول، زفير في الدفع.",
                "good_pain": "عضلة الصدر والتراي والجذع.",
                "bad_pain": "ألم في أسفل الظهر (أنت ترخي حوضك للأسفل، ارفعه قليلاً)."
            }
        ],
        "ظهر": [
            {
                "name": "Deadlift", 
                "reps": "3-5 عدات (قوة عصبية ورفع تستوستيرون)",
                "technique": "قف والبار يلامس قصبة ساقك. انزل بحوضك للخلف مع إبقاء ظهرك مستقيماً 100%. ادفع الأرض بقدميك.",
                "breathing": "خذ نفساً عميقاً جداً واحبسه في بطنك قبل الرفع (Bracing)، ازفر بعد أن تتجاوز الركبة في الصعود.",
                "good_pain": "القطنية (أسفل الظهر العضلي)، أوتار الركبة، والمؤخرة.",
                "bad_pain": "ألم حاد أو 'طقطقة' في فقرات العمود الفقري (هذا يعني أن ظهرك كان مقوساً كالقطة، توقف فوراً)."
            },
            {
                "name": "Lat Pulldown - Wide Grip", 
                "reps": "8-12 عدة (لتعريض الظهر وسحب الجلد)",
                "technique": "أمسك البار بقبضة واسعة. اسحب البار باتجاه أعلى صدرك مع إرجاع لوحي كتفك للخلف.",
                "breathing": "زفير أثناء السحب للأسفل، شهيق أثناء إرجاع البار للأعلى ببطء.",
                "good_pain": "عضلة المجنص (تحت الإبط والظهر الجانبي).",
                "bad_pain": "ألم أو شد في البايسبس أو الساعد (أنت تسحب بيدك، تخيل أن يدك مجرد 'خطاف' واسحب بكوع)."
            },
            {
                "name": "Seated Cable Row", 
                "reps": "10-12 عدة (لسمك الظهر الأوسط)",
                "technique": "اجلس وظهرك مستقيم. اسحب المقبض باتجاه بطنك واعصر لوحي كتفك معاً.",
                "breathing": "زفير في السحب، شهيق في العودة.",
                "good_pain": "منتصف الظهر وبين لوحي الكتف.",
                "bad_pain": "ألم في القطنية (أنت تتأرجح بظهرك للأمام والخلف، يجب أن يكون ظهرك ثابتاً)."
            },
            {
                "name": "Barbell Bent-Over Row", 
                "reps": "6-8 عدات (كتلة شاملة)",
                "technique": "انحنِ للأمام بزاوية 45 درجة وظهرك مستقيم. اسحب البار باتجاه سرتك.",
                "breathing": "شهيق قبل السحب، زفير عند ملامسة البار للبطن.",
                "good_pain": "الظهر الأوسط والمجنص.",
                "bad_pain": "ألم أسفل الظهر (الوزن ثقيل جداً ولا تستطيع تثبيت الجذع)."
            },
            {
                "name": "Pull-ups", 
                "reps": "حتى الفشل العضلي (تعريض خالص)",
                "technique": "اسحب جسمك للأعلى حتى يتجاوز ذقنك البار. انزل ببطء.",
                "breathing": "زفير في الصعود، شهيق في النزول.",
                "good_pain": "المجنص بالكامل.",
                "bad_pain": "الكتف العلوي (أنت تستخدم ترابيسك للسحب بدل المجنص)."
            }
        ],
        "أرجل": [
            {
                "name": "Barbell Squat", 
                "reps": "4-6 عدات (محفز التستوستيرون الأول)",
                "technique": "ضع البار على ترابيسك. افتح قدميك باتساع الكتف. انزل للخلف وكأنك تجلس على كرسي حتى توازي فخذيك الأرض.",
                "breathing": "شهيق عميق قبل النزول لملء البطن (Bracing)، زفير قوي عند الدفع للوقوف.",
                "good_pain": "الفخذ الأمامي (الرباعيات) وعضلات المؤخرة (الجلوتس).",
                "bad_pain": "ألم في صابونة الركبة من الأمام، أو أسفل الظهر (دليل على انحناء الظهر للأمام أثناء النزول)."
            },
            {
                "name": "Leg Press", 
                "reps": "10-12 عدة (ضغط الكتلة بأمان)",
                "technique": "ضع قدميك في منتصف اللوح. انزل بالوزن حتى تصل ركبتك لزاوية 90 درجة، ادفع للأعلى ولا تقفل ركبتك بالكامل.",
                "breathing": "شهيق في النزول، زفير في الدفع.",
                "good_pain": "الفخذ بالكامل يحترق.",
                "bad_pain": "ألم حاد في الركبة (يحدث عند قفل الركبة 100% في الأعلى والوزن ثقيل، خطر جداً)."
            },
            {
                "name": "Bulgarian Split Squat", 
                "reps": "10-12 عدة لكل رجل (نحت المؤخرة والأرجل)",
                "technique": "ضع قدمك الخلفية على دكة. انزل بحوضك للأسفل بشكل عمودي. حافظ على استقامة الجذع.",
                "breathing": "شهيق في النزول، زفير في الصعود.",
                "good_pain": "المؤخرة بشدة، الفخذ الأمامي للرجل الأمامية.",
                "bad_pain": "ألم في كاحل الرجل الخلفية (موقع القدم خاطئ على الدكة)."
            },
            {
                "name": "Romanian Deadlift - RDL", 
                "reps": "8-10 عدات (شد الخلفيات والمؤخرة)",
                "technique": "امسك البار أو الدنابل. اثنِ ركبتيك قليلاً جداً. ادفع حوضك للخلف لأقصى حد حتى تشعر بشد في فخذك الخلفي، ثم ارجع.",
                "breathing": "شهيق أثناء دفع الحوض للخلف، زفير عند العودة للأعلى وعصر المؤخرة.",
                "good_pain": "شد وتمزق إيجابي قوي في الفخذ الخلفي والمؤخرة.",
                "bad_pain": "ألم في القطنية (أنت تثني ظهرك، حافظ عليه مستقيماً)."
            },
            {
                "name": "Leg Extension", 
                "reps": "12-15 عدة (عزل الرباعيات الأمامية)",
                "technique": "اجلس وثبت ظهرك. ادفع الوزن للأعلى واعصر الفخذ الأمامي لثانية في القمة.",
                "breathing": "زفير عند الدفع، شهيق في النزول البطيء.",
                "good_pain": "الفخذ الأمامي فقط (قطرة الدم فوق الركبة).",
                "bad_pain": "ألم تحت صابونة الركبة مباشرة (الوزن عالي جداً أو الكرسي غير مضبوط على مقاسك)."
            },
            {
                "name": "Lying Leg Curl", 
                "reps": "12-15 عدة (عزل الأوتار الخلفية)",
                "technique": "استلقِ على بطنك. اسحب الوزن باتجاه مؤخرتك وتحكم بالنزول.",
                "breathing": "زفير عند السحب، شهيق في النزول.",
                "good_pain": "الفخذ الخلفي بالكامل.",
                "bad_pain": "شد عضلي في السمانة (أنت تسحب بمشط قدمك، اجعل مشط قدمك مرخياً)."
            },
            {
                "name": "Standing Calf Raise", 
                "reps": "15-20 عدة (تكبير السمانة)",
                "technique": "قف على حافة درجة. انزل بكعبك للأسفل لأقصى تمدد، ثم ادفع للأعلى لأقصى انقباض.",
                "breathing": "شهيق في النزول، زفير في الدفع.",
                "good_pain": "احتراق تام في السمانة (عضلة عنيدة تحتاج تكرار عالي).",
                "bad_pain": "ألم في وتر أخيل (أنت تنزل بسرعة وبشكل مفاجئ، انزل ببطء وتحكم)."
            }
        ],
        "أكتاف": [
            {
                "name": "Overhead Barbell Press", 
                "reps": "6-8 عدات (بناء الأكتاف العريضة)",
                "technique": "قف مستقيماً. ادفع البار للأعلى فوق رأسك مباشرة، وأدخل رأسك قليلاً للأمام عند وصول البار للقمة.",
                "breathing": "شهيق قبل الدفع، زفير في الأعلى.",
                "good_pain": "الكتف الأمامي والجانبي بشكل كامل.",
                "bad_pain": "ألم في أسفل الظهر (أنت تقوس ظهرك للخلف بشكل مبالغ فيه لرفع الوزن)."
            },
            {
                "name": "Dumbbell Lateral Raise", 
                "reps": "12-15 عدة (التعريض الجانبي البصري)",
                "technique": "ارفع الدنابل للجانبين مع ثني الكوعين قليلاً، تخيل أنك تصب الماء من إبريقين في الأعلى.",
                "breathing": "زفير عند الرفع، شهيق في النزول.",
                "good_pain": "الكتف الجانبي يحترق.",
                "bad_pain": "ألم في الترابيس والرقبة (أنت ترفع كتفك بالكامل بدل أن ترفع ذراعك فقط)."
            },
            {
                "name": "Front Cable Raise", 
                "reps": "12-15 عدة (الكتف الأمامي)",
                "technique": "اسحب الكيبل للأمام حتى مستوى نظرك وتحكم بالنزول.",
                "breathing": "زفير عند الرفع، شهيق في النزول.",
                "good_pain": "الكتف الأمامي.",
                "bad_pain": "ألم مفاجئ في مفصل الكتف (الوزن ثقيل)."
            },
            {
                "name": "Face Pulls", 
                "reps": "15-20 عدة (صحة المفاصل والكتف الخلفي)",
                "technique": "اسحب الحبل باتجاه وجهك (عند مستوى العين) وافتح يديك للخارج كأنك تستعرض عضلات البايسبس.",
                "breathing": "زفير عند السحب للوجه، شهيق في العودة.",
                "good_pain": "الكتف الخلفي وبين لوحي الكتف.",
                "bad_pain": "ألم في الرقبة (تسحب الحبل لأسفل جداً)."
            }
        ],
        "باي": [
            {
                "name": "Barbell Bicep Curl", 
                "reps": "8-10 عدات (الكتلة الأساسية)",
                "technique": "قف مستقيماً. ارفع البار مع تثبيت كوعك بجانب خصرك. لا تتأرجح بجسمك للخلف.",
                "breathing": "زفير عند الرفع، شهيق عند النزول ببطء.",
                "good_pain": "بطن عضلة البايسبس (التكوير).",
                "bad_pain": "ألم في أسفل الظهر (أنت تتأرجح)، أو ألم في الساعد الداخلي (استخدم EZ Bar بدل البار المستقيم)."
            },
            {
                "name": "Dumbbell Hammer Curl", 
                "reps": "10-12 عدة (العضدية وتضخيم الساعد)",
                "technique": "امسك الدنابل بقبضة محايدة (كأنك تمسك مطرقة). ارفع بالتناوب أو معاً.",
                "breathing": "زفير عند الرفع، شهيق في النزول.",
                "good_pain": "الجانب الخارجي للبايسبس والساعد.",
                "bad_pain": "ألم في الرسغ (حافظ على استقامة الرسغ)."
            },
            {
                "name": "Preacher Curl Machine", 
                "reps": "12-15 عدة (عزل وإطالة تامة)",
                "technique": "ثبت إبطك على المسند. اسحب الوزن للأعلى وتحكم بالنزول.",
                "breathing": "زفير في السحب، شهيق في النزول.",
                "good_pain": "الجزء السفلي القريب من الكوع للبايسبس.",
                "bad_pain": "ألم في وتر الكوع (يحدث عندما تفرد يدك 100% في النزول والوزن ثقيل، اترك ثنية بسيطة جداً)."
            }
        ],
        "تراي": [
            {
                "name": "Tricep Rope Pushdown", 
                "reps": "12-15 عدة (نحت الرأس الجانبي)",
                "technique": "ثبت كوعك بجانب خصرك كأنه مسمر. ادفع الحبل للأسفل وافتح يديك للخارج في نهاية الحركة لزيادة العصر.",
                "breathing": "زفير عند الدفع للأسفل، شهيق عند الصعود لزاوية 90 درجة.",
                "good_pain": "خلف الذراع الخارجي (حدوة الحصان).",
                "bad_pain": "ألم حاد في مفصل الكوع (الوزن ثقيل جداً)."
            },
            {
                "name": "Skull Crushers (EZ Bar)", 
                "reps": "8-10 عدات (الكتلة والتمدد العميق)",
                "technique": "استلقِ على الدكة. انزل بالبار خلف رأسك قليلاً (ليس لجبهتك) لزيادة تمدد الرأس الطويل للترايسبس.",
                "breathing": "شهيق في النزول، زفير في الدفع للأعلى.",
                "good_pain": "خلف الذراع العميق (الرأس الطويل).",
                "bad_pain": "ألم حاد في الكوع (تمرين قاسي على الكوع، يجب التسخين جيداً قبله بالكيبل)."
            },
            {
                "name": "Overhead Dumbbell Extension", 
                "reps": "10-12 عدة (شد الترهل السفلي للذراع)",
                "technique": "امسك دنبل بكلتا يديك فوق رأسك. انزل بالدنبل خلف رقبتك لأقصى تمدد ثم ادفع للأعلى.",
                "breathing": "شهيق عميق في النزول، زفير في الدفع.",
                "good_pain": "طول الترايسبس من الأسفل للأعلى.",
                "bad_pain": "ألم في الكتف الداخلي أو الرقبة."
            }
        ],
        "بطن": [
            {
                "name": "Cable Crunches", 
                "reps": "10-12 عدة بوزن ثقيل (لبروز الـ 6-pack)",
                "technique": "اجلس على ركبتيك. أمسك الحبل خلف رقبتك. انحنِ للأمام محاولاً إيصال كوعك لركبتك باستخدام عضلات بطنك فقط.",
                "breathing": "زفير قوي وتفريغ الهواء بالكامل عند الانحناء للعصر (مهم جداً)، شهيق عند الصعود.",
                "good_pain": "عضلات البطن العلوية والوسطى تتقلص بقوة.",
                "bad_pain": "ألم في القطنية (أنت تستخدم ظهرك للسحب وليس بطنك، ثبت حوضك)."
            },
            {
                "name": "Hanging Leg Raises", 
                "reps": "12-15 عدة (للبطن السفلي وشفط الكرش)",
                "technique": "تعلق بالبار. ارفع رجليك (أو ركبتيك إذا كان صعباً) للأعلى مع لف الحوض قليلاً في الأعلى.",
                "breathing": "زفير أثناء رفع الأرجل، شهيق أثناء النزول ببطء.",
                "good_pain": "أسفل البطن بقوة.",
                "bad_pain": "ألم في الفخذ الأمامي (الرِجل مستقيمة جداً، اثنِ الركبة قليلاً)."
            },
            {
                "name": "Plank - Weighted", 
                "reps": "60 ثانية (قوة الجذع للداخل)",
                "technique": "استند على كوعيك وقدميك. حافظ على ظهرك مستقيماً مثل اللوح، واشفط بطنك للداخل.",
                "breathing": "تنفس سطحي ومنتظم ولا تحبس أنفاسك.",
                "good_pain": "الارتجاف في كامل جدار البطن الداخلي.",
                "bad_pain": "انهيار أسفل الظهر للأسفل (ارفع حوضك قليلاً)."
            }
        ],
        "جوانب": [
            {
                "name": "Cable Woodchoppers", 
                "reps": "12-15 عدة (نحت الخصر بالدوران المقاوم)",
                "technique": "قف بجانب الكيبل (مستوى عالي). اسحب المقبض لأسفل وبشكل قطري لركبتك المعاكسة مع دوران الجذع.",
                "breathing": "زفير قوي مع الدوران والنزول، شهيق في العودة.",
                "good_pain": "الخواصر الجانبية.",
                "bad_pain": "ألم في العمود الفقري (أنت تدور بظهرك وليس بعضلات خصرك)."
            },
            {
                "name": "Russian Twists", 
                "reps": "20-30 عدة (تحمل الجوانب)",
                "technique": "اجلس وارفع قدميك عن الأرض قليلاً. امسك قرص وزن ودر بجذعك يميناً ويساراً.",
                "breathing": "تنفس منتظم مع كل دورة.",
                "good_pain": "الخواصر تشتعل.",
                "bad_pain": "ألم في القطنية (النزول للخلف مبالغ فيه، اجلس بشكل أكثر استقامة)."
            }
        ]
    }
    
    default_ex = {
        "name": "تمرين مخصص", 
        "reps": "10-12 عدة", 
        "technique": "حافظ على التكنيك السليم وتدرج في الوزن המرفوع.", 
        "breathing": "زفير عند الدفع/السحب القوي، شهيق في العودة.", 
        "good_pain": "في بطن العضلة التي تمرنها.", 
        "bad_pain": "ألم حاد في المفاصل أو الأربطة (خطر)."
    }
    
    for m in ["تمرين حر"]:
        db[m] = [
            {"name": "Custom Machine Workout", "reps": "10-12", "technique": "استخدم الجهاز وتدرج بالأوزان.", "breathing": "زفير بالدفع، شهيق بالعودة.", "good_pain": "العضلة المستهدفة.", "bad_pain": "ألم المفاصل."},
            {"name": "Cardio Intensive Session", "reps": "30 دقيقة", "technique": "حافظ على نبض قلب مرتفع لحرق الدهون المستعصية.", "breathing": "تنفس عميق من الأنف.", "good_pain": "تسارع التنفس والتعرق الغزير.", "bad_pain": "ألم حاد في الركبة (غير الجهاز إلى الدراجة أو الإليبتيكال)."}
        ]
        
    return db

def get_exercise_list(muscle):
    db = get_biomechanics_db()
    if not muscle or muscle == "راحة / غياب": 
        return ["➕ إدخال تمرين جديد (يدوي ذكي)"]
        
    names = []
    for k, v in db.items():
        if k in muscle: 
            for ex in v:
                names.append(ex["name"])
                
    if not names: 
        return ["تمرين مخصص", "➕ إدخال تمرين جديد (يدوي ذكي)"]
        
    names = list(set(names))
    names.sort()
    names.append("➕ إدخال تمرين جديد (يدوي ذكي)")
    return names

def get_exercise_info(ex_name):
    db = get_biomechanics_db()
    for group in db.values():
        for ex in group:
            if ex["name"] == ex_name:
                return ex
                
    return {
        "name": ex_name, 
        "reps": "10-12 عدة", 
        "technique": "أداء حركي كامل المدى (Full ROM). حافظ على التركيز العضلي الذهني.",
        "breathing": "شهيق في مرحلة التمدد، زفير في مرحلة الانقباض والدفع.", 
        "good_pain": "شد في بطن العضلة المستهدفة.", 
        "bad_pain": "ألم حاد في المفصل أو وتر مجاور."
    }

def fetch_historical_data(exercise_name):
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past = df[df['Exercise'] == exercise_name]
        if not past.empty:
            last_record = past.iloc[-1]
            return last_record.get('Date', 'N/A'), last_record.get('Weight', 0.0), last_record.get('Reps', 0)
    return None, None, None

def calculate_smart_reps(exercise_name, current_weight):
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past = df[df['Exercise'] == exercise_name]
        if not past.empty:
            last_record = past.iloc[-1]
            lw = float(last_record.get('Weight', 0.0))
            lr = int(last_record.get('Reps', 10))
            
            if current_weight > lw: 
                return max(lr - 2, 6)
            elif current_weight < lw: 
                return lr + 2
            else: 
                return lr
    return 10

# =====================================================================
# 8. MASSIVE NUTRITION & MACROS ENGINE (حاسبة الأكل السعودي)
# =====================================================================
def get_nutrition_databases():
    edaam_db = {
        "إيدام دجاج بالبطاطس (بدون رز - صحن متوسط)": {"protein": 35, "cals": 320},
        "إيدام دجاج بالبطاطس + صحن رز أبيض (150 جرام)": {"protein": 40, "cals": 580},
        "إيدام لحم بالخضار (بدون رز - قطع لحم صافية)": {"protein": 45, "cals": 450},
        "إيدام لحم بالخضار + صحن رز أبيض": {"protein": 50, "cals": 710},
        "إيدام بامية باللحم (طبيخ منزلي)": {"protein": 40, "cals": 410},
        "ملوخية بالدجاج + صحن رز": {"protein": 35, "cals": 480},
        "كبسة دجاج (صدر دجاج + رز 200 جرام)": {"protein": 45, "cals": 650},
        "كبسة دجاج (فخذ دجاج مع الجلد + رز)": {"protein": 35, "cals": 750},
        "مكرونة حمراء بالدجاج (صدر مقطع)": {"protein": 35, "cals": 520},
        "صالونة خضار مشكلة (بدون لحم/دجاج)": {"protein": 5, "cals": 150},
        "جريش باللحم (صحن متوسط)": {"protein": 30, "cals": 450},
        "قرصان (صحن متوسط)": {"protein": 15, "cals": 350},
        "سليق بالدجاج (صحن متوسط)": {"protein": 35, "cals": 500}
    }

    fast_food_db = {
        "نصف حبة دجاج شواية (بدون جلد - الأفضل للتنشيف)": {"protein": 45, "cals": 420},
        "نصف حبة دجاج فحم (مع الجلد)": {"protein": 40, "cals": 550},
        "بروستد (نصف حبة دجاج مقلي مع البطاطس)": {"protein": 35, "cals": 950},
        "وجبة البيك (دجاج مسحب 10 قطع مع بطاطس وثوم)": {"protein": 45, "cals": 1100},
        "وجبة البيك (مسحب 7 قطع بدون بطاطس)": {"protein": 32, "cals": 500},
        "صاروخ شاورما دجاج (عادي بدون جبن إضافي)": {"protein": 25, "cals": 550},
        "صحن شاورما عربي دجاج (مع بطاطس وثوم)": {"protein": 35, "cals": 850},
        "وجبة ماك تشيكن (ساندوتش + بطاطس وسط)": {"protein": 18, "cals": 750},
        "وجبة بيج ماك": {"protein": 25, "cals": 850},
        "برجر لحم مشوي (مفرد - مطاعم الشوي)": {"protein": 20, "cals": 400},
        "برجر دجاج مشوي (مطعم دايت)": {"protein": 30, "cals": 350},
        "علبة تونة (مصفاة بالماء - 100 جرام)": {"protein": 26, "cals": 120},
        "علبة تونة (بالزيت - مصفاة قليلاً)": {"protein": 24, "cals": 220},
        "سكوب بروتين (Whey Protein - مع ماء)": {"protein": 25, "cals": 120},
        "سكوب بروتين (مع 200 مل حليب كامل الدسم)": {"protein": 31, "cals": 240},
        "3 بيضات مسلوقة كاملة": {"protein": 18, "cals": 210},
        "5 بياض بيض مسلوق (بدون صفار)": {"protein": 18, "cals": 85},
        "شريحة لحم ستيك (200 جرام - مطبوخ)": {"protein": 50, "cals": 450},
        "علبة زبادي يوناني سادة (150 جرام)": {"protein": 15, "cals": 100},
        "حليب بروتين عالي (ندى/المراعي - عبوة 320 مل)": {"protein": 27, "cals": 150}
    }
    
    return edaam_db, fast_food_db

# =====================================================================
# 9. WEEKLY STRATEGY ENGINE & DYNAMIC TIME FIX
# =====================================================================
CLASS_BURN = {
    "موتيف 8": 450, 
    "فت كومبات": 650, 
    "كور اكستريم": 350, 
    "ستيب": 450, 
    "اكوا": 350, 
    "بامب فت": 400, 
    "بودي ماكس": 600, 
    "رادير": 300, 
    "جي فت": 400, 
    "فت اتاك": 600, 
    "موبيلتي": 200, 
    "لا يوجد": 0, 
    "راحة / غياب": 0
}

W_ENG = {
    "موتيف 8": {
        "iron": "صدر + تراي", 
        "flow": "الصدر يحتاج تركيز عالي. ابدأ بـ Incline Press لشد الصدر العلوي."
    },
    "فت كومبات": {
        "iron": "أرجل + بطن", 
        "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل ولا تتنازل عن الأوزان."
    },
    "كور اكستريم": {
        "iron": "أكتاف + جوانب", 
        "flow": "أكتاف عريضة = خصر أنحف بصرياً. ركز على تمرين Overhead Press."
    },
    "ستيب": {
        "iron": "ظهر + باي", 
        "flow": "شد الظهر يمنع التحدب ويصحح القوام. ركز على الـ Deadlift و السحب."
    },
    "اكوا": {
        "iron": "حديد شامل (Full Body)", 
        "flow": "اختر تمرين مركب واحد لكل عضلة كبيرة (بنش، سكوات، سحب عالي)."
    },
    "بامب فت": {
        "iron": "صدر + أكتاف", 
        "flow": "أوزان متوسطة وتكرارات عالية للـ Pump وضخ الدم بقوة للألياف."
    },
    "بودي ماكس": {
        "iron": "أرجل + ظهر", 
        "flow": "أعنف يوم في الأسبوع! يستهدف أكبر عضلتين لنسف الكرش. حافظ على طاقتك."
    },
    "رادير": {
        "iron": "ذراعين (باي وتراي)", 
        "flow": "العب (Supersets) باي مع تراي بشكل متتالي لزيادة الحرق واختصار وقت النادي."
    },
    "جي فت": {
        "iron": "حديد قوة (Heavy Lift)", 
        "flow": "3 إلى 5 عدات بأقصى وزن حر. راحة 3 دقائق كاملة بين الجولات لتجنب إصابة الجهاز العصبي."
    },
    "فت اتاك": {
        "iron": "أرجل + أكتاف", 
        "flow": "تمارين مركبة سريعة لرفع نبض القلب وزيادة معدل الحرق الأيضي."
    },
    "موبيلتي": {
        "iron": "تمرين حر (النقاط الضعيفة)", 
        "flow": "استهدف عضلة متأخرة وضعيفة، أو قم بجلسة إطالات عميقة للتعافي."
    },
    "لا يوجد": {
        "iron": "تمرين حر متكامل", 
        "flow": "أنت القائد اليوم. صمم روتينك بناءً على مستوى طاقتك ونشاطك."
    },
    "راحة / غياب": {
        "iron": "راحة", 
        "flow": "استشفاء سلبي وبناء أنسجة. قلل من الكربوهيدرات لعدم وجود مجهود عالي اليوم."
    }
}

def analyze_muscle_balance(plan_df):
    if plan_df.empty: return True, ""
    all_muscles = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    if "أرجل" not in all_muscles: alerts.append("🔴 خطأ هندسي: المخطط يفتقد لتمارين الأرجل (وهي المحفز الأول للتستوستيرون وحرق الكرش).")
    if "ظهر" not in all_muscles: alerts.append("🔴 خلل في القوام: يجب تدريب الظهر لسحب الأكتاف وتصحيح انحناء العمود الفقري.")
    if all_muscles.count("صدر") > 2: alerts.append("🔴 إجهاد مفرط: الصدر مستهدف بكثافة عالية جداً، هذا سيؤدي للهدم العضلي ولن يتطور.")
    if len(alerts) > 0: return False, "<br>".join(alerts)
    return True, "🟢 ممتاز هندسياً: المخطط متوازن، يهاجم الدهون بقوة، ويضمن الاستشفاء السليم."

def get_dynamic_schedule(attendance_mode, origin):
    now = get_makkah_time()
    eta_mins, dist = calculate_smart_eta(origin)
    
    arr_obj = now + timedelta(minutes=eta_mins)
    iron_start_obj = arr_obj + timedelta(minutes=10)
    iron_end_obj = iron_start_obj + timedelta(minutes=75)
    
    now_str = now.strftime("%I:%M %p")
    arr_str = arr_obj.strftime("%I:%M %p")
    iron_start = iron_start_obj.strftime("%I:%M %p")
    iron_end = iron_end_obj.strftime("%I:%M %p")
    
    return now_str, arr_str, iron_start, iron_end, arr_obj, dist, eta_mins

def get_week_dates():
    today = get_makkah_time()
    idx = (today.weekday() + 2) % 7 
    saturday = today - timedelta(days=idx)
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates_dict = {}
    for i, day in enumerate(week_days):
        week_dates_dict[day] = (saturday + timedelta(days=i)).strftime("%Y-%m-%d")
    return week_dates_dict

# =====================================================================
# 10. MAIN COMMANDER DASHBOARD (واجهة غرفة العمليات الشاملة)
# =====================================================================
def main():
    initialize_session_states()
    makkah_now = get_makkah_time()
    days_map = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_ar = days_map[makkah_now.strftime("%A")]
    current_date = makkah_now.strftime("%Y-%m-%d")
    week_dates = get_week_dates()

    st.markdown("<h1>👑 محرك تايتان V36 (The Flawless UI)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>المنطقة: مكة المكرمة | اليوم: {today_ar} ({current_date}) | الساعة اللحظية: {makkah_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    t_ops, t_setup, t_log, t_clinic, t_fuel, t_sys = st.tabs([
        "🚀 الملاحة والميدان", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ علم الحركة الحيوية", 
        "🏥 العيادة الطبية", 
        "🥗 حاسبة الماكروز", 
        "🛠️ رادار الإصلاح الذاتي"
    ])

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS & INTERNAL ROUTING ENGINE
    # -----------------------------------------------------------------
    with t_ops:
        plan_df = fetch_sheet_safe("Weekly_Plan")
        s_class, iron_target = "موتيف 8", "صدر + تراي" 
        
        if not plan_df.empty and 'Date' in plan_df.columns:
            try:
                r = plan_df[plan_df['Date'] == current_date].iloc[0]
                s_class = r.get('Class', 'موتيف 8')
                iron_target = r.get('Muscle', 'صدر + تراي')
            except Exception: 
                pass

        if today_ar == "الجمعة" and st.session_state['attendance_mode'] != "IronOnly":
            st.markdown(
                "<div class='titan-card titan-card-center' style='border: 2px solid #2ECC40;'>\n"
                "<h1 style='color:#2ECC40; margin:0;'>يوم راحة سلبي إلزامي 🛑</h1>\n"
                "<p style='font-size:20px; color:#A0A0A0;'>بناء الأنسجة العضلية وحرق الدهون يتم أثناء الراحة العميقة.</p>\n"
                "</div>", 
                unsafe_allow_html=True
            )
            if st.button("🔄 التراجع والذهاب للنادي للحديد فقط", use_container_width=True): 
                st.session_state['attendance_mode'] = "IronOnly"
                st.rerun()
                
        elif s_class == "راحة / غياب" or st.session_state['attendance_mode'] == "Absent":
            st.markdown(
                f"<div class='titan-card' style='border-color: #FF4136;'>\n"
                f"<h2 style='color:#FF4136; text-align:center;'>مجدول كـ (راحة / غياب) ❌</h2>\n"
                f"<p style='text-align:center;'>النظام رحّل تمرين <b>({iron_target})</b> للغد تلقائياً.</p>\n"
                "<hr style='border-color:#333;'>\n"
                "<h4 style='color:#E0E0E0; text-align:center;'>توجيه تغذية طارئ</h4>\n"
                "<p style='text-align:center;'>الكربوهيدرات العالية ممنوعة الليلة لعدم وجود حرق أو استنزاف للجلايكوجين.</p>\n"
                "</div>", 
                unsafe_allow_html=True
            )
            if st.button("🔄 التراجع (قررت الذهاب للنادي)", use_container_width=True): 
                st.session_state['attendance_mode'] = "Full"
                st.rerun()
                
        else:
            c1, c2 = st.columns([2, 1])
            with c2:
                st.markdown("<div class='titan-card titan-card-center'>\n<h3 style='margin-top:0;'>📍 الملاحة الداخلية الذكية</h3>", unsafe_allow_html=True)
                st.info("يتم حساب المسافة بمعادلة Haversine الرياضية وتطبيق مصفوفة الزحام لمدينة جدة/مكة.")
                
                loc_list = ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"]
                loc = st.selectbox("الانطلاق من:", loc_list, index=loc_list.index(st.session_state['selected_origin_loc']))
                st.session_state['selected_origin_loc'] = loc
                
                st.markdown("<hr style='border-color:#333;'>\n<h3 style='margin-top:0;'>🕹️ التحكم الميداني</h3>", unsafe_allow_html=True)
                
                if st.button("✅ حضور كامل (كلاس + حديد)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "Full"
                    st.rerun()
                if st.button("🏋️ حديد فقط (إلغاء الكلاس)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "IronOnly"
                    st.rerun()
                if st.button("🤸 كلاس فقط (إلغاء الحديد)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "ClassOnly"
                    st.rerun()
                if st.button("⏳ تأخير مسار (زحمة غير متوقعة)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "Delayed"
                    st.rerun()
                if st.button("❌ غياب تام عن النادي", use_container_width=True): 
                    st.session_state['attendance_mode'] = "Absent"
                    st.rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)

            with c1:
                now_str, arr_str, iron_start, iron_end, arr_obj, dist, eta_mins = get_dynamic_schedule(st.session_state['attendance_mode'], loc)
                c_burn = CLASS_BURN.get(s_class, 0)
                
                workout_details = W_ENG.get(s_class, {})
                t_flw = workout_details.get("flow", "استراتيجية غير محددة، صمم روتينك.")
                
                class_note = ""
                if arr_obj.hour < 18 and st.session_state['attendance_mode'] in ["Full", "ClassOnly"]:
                    class_note = "<div class='info-box' style='margin-top:10px;'>* ملاحظة هندسية: الكلاس المجدول يبدأ الساعة 9:00 مساءً. تمرينك الآن مبكر جداً (في فترة الظهر/العصر)، ستضطر للعودة لاحقاً في المساء لحضور الكلاس، أو يمكنك تغيير المسار إلى (حديد فقط) من أزرار التحكم.</div>\n"
                
                if st.session_state['attendance_mode'] == "Full":
                    nav_html = (
                        "<div class='titan-card'>\n"
                        f"<h3 style='margin-top:0;'>🗺️ الخطة أ (الكمال الهندسي: كلاس وحديد)</h3>\n"
                        f"<p style='font-size:18px;'>الحديد المستهدف: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس المجدول: <b style='color:#FFD700;'>{s_class}</b> <span style='color:#FF4136; font-size:14px;'>(حرق ~{c_burn} kcal)</span></p>\n"
                        f"<p style='color:#888;'>الاستراتيجية المتبعة: {t_flw}</p>\n"
                        "<hr style='border-color: rgba(255,255,255,0.1);'>\n"
                        f"<p>🚗 الانطلاق من {loc}: <b style='color:#D4AF37;'>{now_str}</b></p>\n"
                        f"<p>📏 المسافة الجغرافية: <b style='color:#D4AF37;'>{dist:.1f} KM</b> | ⏱️ الوقت المقدر بالزحام: <b style='color:#D4AF37;'>{eta_mins} دقيقة</b></p>\n"
                        f"<p>🅿️ الوصول لمواقف النادي: <b style='color:#D4AF37;'>{arr_str}</b></p>\n"
                        "<h5 style='color:#E0E0E0; margin-top:20px;'>الجدول الزمني الميداني التفاعلي (لتفادي الهدم العضلي)</h5>\n"
                        f"<p>🔥 {arr_str} - {iron_start} : إحماء مفاصل وتجهيز دقيق</p>\n"
                        f"<p>💪 {iron_start} - {iron_end} : <b style='color:#FF4136;'>صالة الحديد (75 دقيقة كحد أقصى لمنع إفراز هرمون الكورتيزول الهادم)</b></p>\n"
                        f"<p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>كلاس ({s_class}) (لحرق دهون البطن والمؤخرة بشكل صافي)</b></p>\n"
                        f"{class_note}"
                        "</div>"
                    )
                elif st.session_state['attendance_mode'] == "IronOnly":
                    nav_html = (
                        "<div class='titan-card' style='border-color: #0074D9;'>\n"
                        "<h3 style='margin-top:0; color:#0074D9;'>🏋️ مسار الحديد المكثف (تم إسقاط الكلاس)</h3>\n"
                        f"<p style='font-size:18px;'>الحديد المستهدف اليوم: <b style='color:#FFD700;'>{iron_target}</b></p>\n"
                        "<p style='color:#888;'>بما أن الكلاس تم إلغاؤه، لديك طاقة أعلى لكسر الأوزان الحرة وبناء الكتلة العضلية.</p>\n"
                        "<hr style='border-color: rgba(255,255,255,0.1);'>\n"
                        f"<p>🚗 الانطلاق من {loc}: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ وصول المواقف: <b style='color:#D4AF37;'>{arr_str}</b></p>\n"
                        "<h5 style='color:#E0E0E0; margin-top:20px;'>الجدول الميداني المفتوح</h5>\n"
                        f"<p>🔥 {arr_str} - {iron_start} : إحماء دقيق لتفادي الإصابة</p>\n"
                        f"<p>💪 {iron_start} - {(arr_obj + timedelta(minutes=90)).strftime('%I:%M %p')} : <b style='color:#FF4136;'>صالة الحديد (استغل وقتك المفتوح، العب جولات إضافية وتحدى أوزانك القديمة)</b></p>\n"
                        "</div>"
                    )
                elif st.session_state['attendance_mode'] == "ClassOnly":
                    nav_html = (
                        "<div class='titan-card' style='border-color: #D4AF37;'>\n"
                        "<h3 style='margin-top:0; color:#D4AF37;'>🤸 مسار الكارديو واللياقة (الحديد ملغي)</h3>\n"
                        f"<p style='font-size:18px;'>الكلاس المجدول: <b style='color:#FFD700;'>{s_class}</b></p>\n"
                        "<hr style='border-color: rgba(255,255,255,0.1);'>\n"
                        f"<p>🚗 الانطلاق من {loc}: <b style='color:#D4AF37;'>{now_str}</b> | 🅿️ وصول المواقف: <b style='color:#D4AF37;'>{arr_str}</b></p>\n"
                        f"<p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>حضور الكلاس (حرق متوقع ~{c_burn} kcal)</b></p>\n"
                        f"{class_note}"
                        "</div>"
                    )
                else:
                    nav_html = (
                        "<div class='titan-card' style='border-color: #FF4136;'>\n"
                        "<h3 style='margin-top:0; color:#FF4136;'>⚠️ مسار التأخير والزحمة (إنقاذ التمرين)</h3>\n"
                        f"<p style='font-size:18px;'>الحديد المختصر: <b style='color:#FFD700;'>{iron_target}</b></p>\n"
                        "<hr style='border-color: rgba(255,255,255,0.1);'>\n"
                        "<p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>توجه للكلاس مباشرة فور وصولك لعدم تفويت التسخين الجماعي</b></p>\n"
                        "<p>💪 09:55 PM - 10:30 PM : <b style='color:#FF4136;'>حديد سريع جداً (استخدم أجهزة العزل فقط، يُمنع استخدام الأوزان الحرة لتفادي الإصابة بسبب إرهاق الكلاس)</b></p>\n"
                        "</div>"
                    )
                
                st.markdown(nav_html, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع (مزامنة سحابية تامة)")
        st.info("هذا الجدول متصل بجوجل شيتس. أي تعديل هنا سينعكس على كل الأجهزة.")
        
        plan_df = fetch_sheet_safe("Weekly_Plan")
        curr_plan = {}
        if not plan_df.empty and 'Day' in plan_df.columns and 'Class' in plan_df.columns:
            for _, row in plan_df.iterrows():
                curr_plan[row['Day']] = row['Class']
        
        with st.form("weekly_master_plan"):
            ns = []
            cols = st.columns(3)
            opts = list(W_ENG.keys())
            
            for i, d in enumerate(["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]):
                ex_dt = week_dates.get(d, "")
                default_class = curr_plan.get(d, "موتيف 8")
                
                try: 
                    idx = opts.index(default_class)
                except ValueError: 
                    idx = 0
                
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E0E0E0; text-align:right;'>{d}<br><span style='font-size:12px; color:#888;'>{ex_dt}</span></h5>", unsafe_allow_html=True)
                    ch = st.selectbox("اختر الكلاس", opts, index=idx, key=f"c_{d}", label_visibility="collapsed")
                    
                    workout_details_setup = W_ENG.get(ch, {})
                    m_target = workout_details_setup.get('iron', 'غير محدد')
                    
                    ns.append({"Day": d, "Date": ex_dt, "Class": ch, "Muscle": m_target, "Status": "مجدول"})
            
            st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص هندسي واعتماد المخطط في السحابة", use_container_width=True):
                bal, msg = analyze_muscle_balance(pd.DataFrame(ns))
                st.markdown(f"<div class='{'success-box' if bal else 'alert-box'}'>{msg}</div>", unsafe_allow_html=True)
                
                s, m = overwrite_sheet_safe("Weekly_Plan", pd.DataFrame(ns))
                if s: 
                    st.success(m)
                else: 
                    st.error(m)

    # -----------------------------------------------------------------
    # TAB 3: BIOMECHANICS & SMART LOGS
    # -----------------------------------------------------------------
    with t_log:
        st.markdown("### 🏋️ علم الحركة الحيوية (Biomechanics) وتسجيل الأوزان")
        t_muscle = iron_target
        
        st.markdown("<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>🚦 التقييم قبل التمرين (Pre-Workout Check)</h4>", unsafe_allow_html=True)
        st.session_state['pre_workout_pain'] = st.selectbox("كيف تشعر بجسمك ومفاصلك اليوم قبل البدء؟", [
            "سليم 100% وجاهز لكسر الأوزان الحرة",
            "إرهاق عام وعضلات مشدودة (DOMS من الأمس)",
            "ألم خفيف في أحد المفاصل (ركبة، كوع، رسغ)",
            "ألم حاد في أسفل الظهر أو الكتف الداخلي (خطر)"
        ])
        
        if "المفاصل" in st.session_state['pre_workout_pain'] or "خطر" in st.session_state['pre_workout_pain']:
            st.warning("⚠️ بما أن هناك ألم في المفاصل أو الظهر، يُمنع اليوم لعب الأوزان الحرة (Deadlift, Squat, Barbell Press) تماماً. استخدم الأجهزة ذات المسار الثابت فقط لحماية الأربطة!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة الدقيق</h4><p style='font-size:12px; color:#888;'>الالتزام بالوقت يضمن ضخ الدم (Pump) وتجنب برودة العضلة.</p>", unsafe_allow_html=True)
            if st.button("بدء 90 ثانية (تضخيم وبناء)", use_container_width=True): 
                pb = st.progress(0)
                for i in range(90): 
                    time.sleep(1)
                    pb.progress((i+1)/90)
                st.success("انتهت الراحة! ارجع للبار فوراً.")
                
            if st.button("بدء 3 دقائق (قوة Power)", use_container_width=True): 
                pb = st.progress(0)
                for i in range(180): 
                    time.sleep(1)
                    pb.progress((i+1)/180)
                st.success("الجهاز العصبي تعافى، أنت جاهز للوزن الثقيل.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>العضلة المستهدفة اليوم: <span style='color:#FFD700;'>{t_muscle}</span></h4>", unsafe_allow_html=True)
            
            ex_list = get_exercise_list(t_muscle)
            s_ex = st.selectbox("اختر التمرين من قاعدة البيانات الضخمة لتسجيله:", ex_list)
            
            if "يدوي ذكي" in s_ex:
                f_ex = st.text_input("اكتب اسم التمرين الجديد (يُفضل باللغة الإنجليزية لتوحيد السجلات في السحابة):")
            else:
                f_ex = s_ex
            
            f_ex = f_ex if f_ex else "تمرين مخصص"
            info = get_exercise_info(f_ex)
            
            # HTML بدون مسافات بادئة لمنع تحويله لكود
            ex_info_html = (
                "<div style='background:#111; padding:20px; border-radius:12px; margin-bottom:20px; border-right: 4px solid #D4AF37;'>\n"
                f"<p><span class='bio-tech'>⚙️ الأداء الميكانيكي (Technique):</span><br>{info.get('technique', 'حافظ على التركيز')}</p>\n"
                f"<p><span class='bio-breath'>🫁 التنفس (Breathing):</span><br>{info.get('breathing', 'تنفس منتظم')}</p>\n"
                "<hr style='border-color:#333;'>\n"
                f"<p><span class='bio-good'>✅ الألم الجيد للتطور (DOMS):</span><br>{info.get('good_pain', 'العضلة المستهدفة')}</p>\n"
                f"<p><span class='bio-bad'>❌ الألم السيء والإصابات:</span><br>{info.get('bad_pain', 'المفاصل')}</p>\n"
                "<hr style='border-color:#333;'>\n"
                f"<h5 style='color:#FFD700; margin:0;'>النطاق العلمي للعدات: {info.get('reps', '10-12')}</h5>\n"
                "</div>"
            )
            st.markdown(ex_info_html, unsafe_allow_html=True)
            
            p_date, p_weight, p_reps = fetch_historical_data(f_ex)
            if p_date:
                st.markdown(f"<div style='background:#111; padding:10px; border-radius:8px; border-right:4px solid #D4AF37; margin-bottom:15px;'><p style='color:#888; margin:0;'>آخر مرة تمرنت ({p_date}): <b>{p_weight} KG</b> × {p_reps} عدات</p></div>", unsafe_allow_html=True)
                last_w = float(p_weight)
            else: 
                last_w = 0.0
            
            cw, cr = st.columns(2)
            w = cw.number_input("الوزن המرفوع (KG)", min_value=0.0, value=last_w, step=2.5)
            r = cr.number_input("العدات (اكتب 0 وسيتولى الذكاء الاصطناعي الحساب)", min_value=0, value=0)
            
            if st.button("💾 توثيق الجلسة في السحابة", use_container_width=True):
                if "يدوي ذكي" in s_ex and not f_ex: 
                    st.error("الرجاء كتابة اسم التمرين اليدوي أولاً.")
                else:
                    f_r = calculate_smart_reps(f_ex, w) if r == 0 else r
                    if r == 0: 
                        st.success(f"🤖 الذكاء الاصطناعي استنتج أنك حققت {f_r} عدات بناءً على الوزن القديم وقوانين التضخيم.")
                        
                    new_entry = {"Date": current_date, "Muscle": t_muscle, "Exercise": f_ex, "Weight": w, "Reps": f_r}
                    success, s_msg = append_to_sheet_safe("Workout_Logs", new_entry)
                    if success: 
                        st.success(f"تم تسجيل تمرين {f_ex} بنجاح.")
                    else: 
                        st.error(s_msg)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("#### 🤕 التقييم بعد التمرين (أو ثاني يوم - DOMS Analysis)")
        with st.form("doms_form"):
            st.write(f"بناءً على تمرين [{f_ex}] الذي تمرنته:")
            st.markdown(f"<p style='font-size:14px;'><span class='good-pain'>✅ الألم الجيد الذي يدل على التطور يجب أن يكون في:</span> {info.get('good_pain', 'بطن العضلة')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:14px;'><span class='pain-zone'>❌ الألم السيء الذي يدل على إصابة/تكنيك خاطئ:</span> {info.get('bad_pain', 'المفصل')}</p>", unsafe_allow_html=True)
            
            doms_level = st.slider("مستوى الألم العضلي الذي تشعر به الآن (1 = لا يوجد، 10 = تمزق/إعاقة حركة تامة):", 1, 10, 3)
            doms_loc = st.selectbox("أين يتركز الألم بشكل رئيسي؟", [
                "في بطن العضلة المستهدفة (ألم تمدد طبيعي ممتاز)", 
                "في المفاصل والأوتار المحيطة (خطر)", 
                "في أسفل الظهر أو القطنية (تحذير جدي)", 
                "في الرقبة أو الترابيس العلوية (تكنيك خاطئ)"
            ])
            
            if st.form_submit_button("💾 حفظ حالة الاستشفاء وتأكيدها"):
                if "المفاصل" in doms_loc or "أسفل الظهر" in doms_loc:
                    st.error("⚠️ التقييم يؤكد أن التكنيك كان خاطئاً أو الوزن كان ثقيلاً جداً لدرجة أنك استعنت بمفاصلك لرفعه. راجع فيديوهات التكنيك فوراً أو خفف الوزن المرة القادمة.")
                elif doms_level > 8:
                    st.warning("⚠️ الألم العالي جداً في بطن العضلة (DOMS فوق 8) يعني أنك تحتاج للراحة السلبية، لا تمرن هذه العضلة قبل مرور 72 ساعة.")
                else:
                    st.success("✅ ممتاز! ألم بطن العضلة المحتمل يدل على تدمير الألياف بنجاح لإعادة بنائها بشكل أكبر وأصلب. استمر في التغذية الجيدة والراحة.")

    # -----------------------------------------------------------------
    # TAB 4: CLINICAL RECOVERY & INBODY
    # -----------------------------------------------------------------
    with t_clinic:
        st.markdown("### 🏥 العيادة الطبية والاستشفاء (Medical Recovery)")
        
        is_heavy_day = today_ar in ["الاثنين", "الخميس"] or "أرجل" in iron_target or st.session_state['attendance_mode'] == "IronOnly"
        protocol_html = get_medical_recovery_protocol(is_heavy_day)
        st.markdown(protocol_html, unsafe_allow_html=True)
        
        c_c1, c_c2 = st.columns(2)
        
        with c_c1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>🏊 حاسبة الاستشفاء النشط (المسبح)</h4>", unsafe_allow_html=True)
            st.info("السباحة تحرق الكثير من السعرات الإضافية، أدخلها هنا لخصمها من العداد الغذائي لمنع العجز الزائد.")
            with st.form("swim_form"):
                s_mins = st.number_input("كم دقيقة سبحت اليوم بشكل مستمر؟", min_value=0, value=15, step=5)
                if st.form_submit_button("حساب السعرات وإضافتها للعداد", use_container_width=True):
                    c_burn = int(s_mins * 8.5) 
                    st.session_state['swim_cals_burned'] = c_burn
                    st.success(f"ممتاز! تم حرق {c_burn} سعرة حرارية من السباحة. (تم خصمها في نظام الوقود والماكروز)")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_c2:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>📸 أرشفة تقرير InBody السحابي</h4>", unsafe_allow_html=True)
            with st.form("ib_form"):
                ib_dt = st.date_input("تاريخ الفحص الطبي")
                c_ib1, c_ib2 = st.columns(2)
                ib_wt = c_ib1.number_input("الوزن الإجمالي (KG)", value=91.9, step=0.1)
                ib_ms = c_ib2.number_input("العضلات (SMM - KG)", value=40.0, step=0.1)
                ib_ft = c_ib1.number_input("نسبة الدهون (%)", value=20.0, step=0.5)
                ib_vs = c_ib2.number_input("الدهون الحشوية (الكرش - يجب أن تنزل تحت 10)", value=14, step=1)
                
                if st.form_submit_button("💾 أرشفة البيانات في قاعدة جوجل", use_container_width=True):
                    inbody_data = {
                        "Date": ib_dt.strftime("%Y-%m-%d"), 
                        "Weight": ib_wt, 
                        "Muscle_Mass": ib_ms, 
                        "Fat_Percentage": ib_ft, 
                        "Visceral_Fat": ib_vs
                    }
                    success, msg = append_to_sheet_safe("InBody_Logs", inbody_data)
                    if success: 
                        st.success("تم الحفظ وأرشفة البيانات الطبية بشكل دائم.")
                    else: 
                        st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 5: NUTRITION CALCULATOR (Offline Macro Builder)
    # -----------------------------------------------------------------
    with t_fuel:
        st.markdown("### 🥗 حاسبة الماكروز العميقة (المطبخ السعودي - Offline)")
        st.info("قم ببناء وجباتك بدقة من خلال إضافة الأصناف والكميات. النظام سيجمع السعرات والبروتين ويخصم منها حرق السباحة تلقائياً وبالمجان مدى الحياة.")
        
        c_f1, c_f2 = st.columns([1, 1.2])
        e_db, f_db = get_nutrition_databases()
        full_food_db = {**e_db, **f_db} 
        
        with c_f2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>أضف مكونات طعامك للعداد</h4>", unsafe_allow_html=True)
            
            sel_food = st.selectbox("ابحث واختر الصنف (من المطاعم وطبخ البيت السعودي):", list(full_food_db.keys()))
            qty = st.number_input("الكمية (عدد الحصص المذكورة في اسم الصنف):", min_value=1.0, value=1.0, step=0.5)
            
            if st.button("➕ إضافة الوجبة للعداد اليومي", use_container_width=True):
                added_prot = int(full_food_db[sel_food]["protein"] * qty)
                added_cals = int(full_food_db[sel_food]["cals"] * qty)
                st.session_state['daily_protein'] += added_prot
                st.session_state['daily_cals'] += added_cals
                st.success(f"تم إضافة {qty} حصة من ({sel_food}). [+ {added_prot}g بروتين, + {added_cals} سعرة]")
                
            st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
            st.write("**هل قرأت السعرات من غلاف منتج آخر؟ أدخله يدوياً هنا:**")
            
            cm1, cm2 = st.columns(2)
            m_p = cm1.number_input("بروتين (جرام)", min_value=0)
            m_c = cm2.number_input("سعرات حرارية", min_value=0, step=50)
            
            if st.button("➕ إضافة الإدخال اليدوي للعداد", use_container_width=True):
                st.session_state['daily_protein'] += m_p
                st.session_state['daily_cals'] += m_c
                st.success("تم جمع القيم المدخلة يدوياً للعداد النهائي.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_f1:
            tar_prot = int(91.9 * 2.2) 
            tar_cals = 1900
            
            net_calories = st.session_state['daily_cals'] - st.session_state['swim_cals_burned']
            
            fuel_html = (
                "<div class='titan-card'>\n"
                "<h3 style='margin-top:0;'>📊 لوحة الماكروز اليومية</h3>\n"
                f"<p style='font-size:18px;'>البروتين المكتسب: <b style='color:#FF4136; font-size:30px;'>{st.session_state['daily_protein']} / {tar_prot} g</b></p>\n"
                f"<p style='font-size:18px;'>إجمالي السعرات التي أكلتها: <b style='color:#D4AF37; font-size:30px;'>{st.session_state['daily_cals']} / {tar_cals}</b></p>\n"
                "<hr style='border-color:#333;'>\n"
                f"<p style='font-size:16px;'>حرق السباحة الإضافي المخصوم: <b style='color:#2ECC40; font-size:24px;'>- {st.session_state['swim_cals_burned']} kcal</b></p>\n"
                f"<p style='font-size:18px;'>صافي السعرات بعد المجهود: <b style='color:#E0E0E0; font-size:26px;'>{net_calories} kcal</b></p>\n"
                "</div>"
            )
            st.markdown(fuel_html, unsafe_allow_html=True)
            
            with st.form("health_form"):
                slp = st.number_input("ساعات النوم الفعلي (من ساعة Huawei):", value=7.5, step=0.5)
                wtr = st.number_input("الماء المستهلك (لتر - مهم لطرد احتباس السوائل):", value=3.5, step=0.5)
                
                st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
                if st.form_submit_button("💾 توثيق وحفظ يوم التغذية النهائي في الإكسل", use_container_width=True):
                    health_record = {
                        "Date": current_date, 
                        "Sleep": slp, 
                        "Water": wtr, 
                        "Protein": st.session_state['daily_protein'], 
                        "Calories": net_calories, 
                        "Notes": ""
                    }
                    success, s_msg = append_to_sheet_safe("Health_Log", health_record)
                    if success: 
                        st.success("تم الحفظ بنجاح. سيتم تصفير العداد لليوم التالي ليكون جاهزاً.")
                        st.session_state['daily_protein'] = 0
                        st.session_state['daily_cals'] = 0
                        st.session_state['swim_cals_burned'] = 0
                    else: 
                        st.error(s_msg)

    # -----------------------------------------------------------------
    # TAB 6: SYSTEM DIAGNOSTICS & AUTO-HEAL
    # -----------------------------------------------------------------
    with t_sys:
        st.markdown("### 🛠️ مركز الصيانة الشامل ورادار الإصلاح الذاتي")
        st.info("يقوم هذا القسم بمسح شامل لقاعدة البيانات. إذا وجد صفحة أو عموداً ناقصاً، سيقوم بإنشائه وإصلاحه تلقائياً لمنع انهيار التطبيق.")
        
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.markdown("<div class='titan-card titan-card-center'>\n<h4 style='margin-top:0;'>مسح وإصلاح الإكسل</h4>", unsafe_allow_html=True)
            if st.button("🔄 فحص الرادار والإصلاح الذاتي", use_container_width=True):
                with st.spinner("جاري المسح العميق والتفاوض مع خوادم Google Cloud..."):
                    time.sleep(1) 
                    reports = run_auto_heal_system()
                    for r in reports:
                        c_box = 'success-box' if r['status'] == 'success' else 'alert-box' if r['status'] == 'error' else 'info-box'
                        st.markdown(f"<div class='{c_box}'>{r['msg']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_sys2:
            st.markdown("<div class='titan-card titan-card-center'>\n<h4 style='margin-top:0;'>إصلاح البرنامج المعلق</h4>", unsafe_allow_html=True)
            st.warning("استخدم هذا الزر فقط إذا توقف التطبيق عن الاستجابة أو أظهر بيانات خاطئة. سيقوم بمسح الذاكرة المؤقتة بالكامل.")
            if st.button("⚠️ إعادة ضبط المصنع (Hard Reset)", use_container_width=True):
                force_program_reset()
                st.success("تم مسح الكاش والذاكرة العشوائية. يرجى تحديث الصفحة (Refresh).")
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
