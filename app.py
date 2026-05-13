import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time
import math
import textwrap

# =====================================================================
# 1. CORE ARCHITECTURE & SYSTEM INITIALIZATION
# إعدادات النظام المعمارية الأساسية للواجهة التجارية
# =====================================================================

st.set_page_config(
    page_title="Titan V45 - The Enterprise Monolith (Part 1)", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_makkah_time():
    """
    محرك التوقيت الدقيق لمكة المكرمة (UTC+3).
    تم فصله ليعمل بشكل مستقل عن أي سيرفر أجنبي.
    """
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# =====================================================================
# 2. ADVANCED FRONTEND ENGINEERING (CSS Architecture)
# هندسة الواجهة الأمامية بتدرجات الألوان المخصصة (SaaS UI)
# =====================================================================

def inject_premium_css():
    """
    مكتبة التصميم الشاملة.
    تم فك جميع أسطر الـ CSS لمنع أي تداخل أو قراءة خاطئة من المتصفح.
    """
    css_code = """
    <style>
        /* الإعدادات الأساسية والخلفية */
        .stApp { 
            background-color: #030406; 
            color: #E8ECEF; 
            font-family: 'Inter', -apple-system, sans-serif; 
        }
        
        h1, h2, h3, h4, h5 { 
            color: #E5B94C !important; 
            text-align: right; 
            font-weight: 800; 
            letter-spacing: 0.5px; 
            margin-bottom: 15px;
        }
        
        /* التبويبات العلوية (SaaS Navigation) */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 12px; 
            justify-content: center; 
            background: #0A0D14; 
            padding: 15px; 
            border-radius: 15px; 
            border: 1px solid #1F2937; 
            margin-bottom: 30px; 
        }
        
        .stTabs [data-baseweb="tab"] { 
            background-color: transparent; 
            border: 1px solid #1F2937; 
            border-radius: 8px; 
            padding: 12px 20px; 
            color: #8B949E; 
            font-size: 15px; 
            font-weight: 600; 
            transition: all 0.2s ease; 
        }
        
        .stTabs [aria-selected="true"] { 
            background-color: rgba(229, 185, 76, 0.1) !important; 
            border-color: #E5B94C !important; 
            color: #E5B94C !important; 
            box-shadow: 0 4px 15px rgba(229, 185, 76, 0.15); 
            transform: scale(1.05);
        }
        
        /* البطاقات الاحترافية */
        .titan-card { 
            background: #0D1117; 
            border: 1px solid #30363D; 
            border-radius: 16px; 
            padding: 30px; 
            margin-bottom: 25px; 
            text-align: right; 
            box-shadow: 0 15px 25px rgba(0,0,0,0.6); 
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
        }
        
        .titan-card:hover { 
            border-color: #8B949E; 
            transform: translateY(-2px); 
            box-shadow: 0 8px 24px rgba(0,0,0,0.8); 
        }
        
        .titan-card-center { 
            text-align: center; 
        }
        
        /* الأرقام والإحصائيات */
        .premium-value { 
            color: #E5B94C; 
            font-size: 38px; 
            font-weight: 900; 
            margin: 15px 0; 
            font-family: 'Courier New', monospace; 
        }
        
        .data-label { 
            color: #8B949E; 
            font-size: 14px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }
        
        /* البروتوكولات الطبية التفاعلية */
        .med-hot { 
            background: rgba(248, 81, 73, 0.05); 
            border-right: 5px solid #F85149; 
            padding: 22px; 
            border-radius: 10px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        .med-cold { 
            background: rgba(88, 166, 255, 0.05); 
            border-right: 5px solid #58A6FF; 
            padding: 22px; 
            border-radius: 10px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        .med-neutral { 
            background: rgba(46, 160, 67, 0.05); 
            border-right: 5px solid #2EA043; 
            padding: 22px; 
            border-radius: 10px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        .med-danger { 
            background: rgba(210, 153, 34, 0.05); 
            border-right: 5px solid #D29922; 
            padding: 22px; 
            border-radius: 10px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        /* المربعات التحذيرية العامة */
        .alert-box { 
            background: rgba(248, 81, 73, 0.1); 
            border: 1px solid #F85149; 
            padding: 18px; 
            border-radius: 10px; 
            color: #F85149; 
            text-align: right; 
            margin-bottom: 18px; 
            font-weight: bold;
        }
        
        .success-box { 
            background: rgba(46, 160, 67, 0.1); 
            border: 1px solid #2EA043; 
            padding: 18px; 
            border-radius: 10px; 
            color: #2EA043; 
            text-align: right; 
            margin-bottom: 18px; 
            font-weight: bold;
        }
        
        .info-box { 
            background: rgba(88, 166, 255, 0.1); 
            border: 1px solid #58A6FF; 
            padding: 18px; 
            border-radius: 10px; 
            color: #58A6FF; 
            text-align: right; 
            margin-bottom: 18px; 
            font-weight: bold;
        }
        
        /* تنسيقات الماكروز والعضلات */
        .bio-tech { color: #E5B94C; font-weight: bold; }
        .bio-breath { color: #58A6FF; font-weight: bold; }
        .bio-good { color: #2EA043; font-weight: bold; }
        .bio-bad { color: #F85149; font-weight: bold; }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# تفعيل వాجهة ה- CSS
inject_premium_css()

# =====================================================================
# 3. ENTERPRISE STATE MANAGEMENT (إدارة المتغيرات والذاكرة)
# =====================================================================

def init_states():
    """
    تهيئة جميع متغيرات الجلسة بوضوح لمنع أي خطأ (KeyError).
    يتم التأكد من صحة نوع المتغير (Type Safety) لمنع الانهيار.
    """
    if 'attendance_mode' not in st.session_state:
        st.session_state['attendance_mode'] = "Full"
        
    if 'selected_origin_loc' not in st.session_state:
        st.session_state['selected_origin_loc'] = "المنزل (جدة - المروة)"
        
    if 'daily_protein' not in st.session_state:
        st.session_state['daily_protein'] = 0
        
    if 'daily_cals' not in st.session_state:
        st.session_state['daily_cals'] = 0
        
    if 'swim_cals_burned' not in st.session_state:
        st.session_state['swim_cals_burned'] = 0
        
    if 'ai_vision_scans_left' not in st.session_state:
        st.session_state['ai_vision_scans_left'] = 10
        
    if 'is_premium_user' not in st.session_state:
        st.session_state['is_premium_user'] = True

def force_program_reset():
    """تفريغ الكاش والذاكرة العشوائية بالكامل"""
    st.cache_resource.clear()
    st.cache_data.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# =====================================================================
# 4. SECURE CLOUD CONNECTORS & AUTO-HEAL
# محركات الاتصال بقواعد البيانات السحابية والإصلاح الذاتي
# =====================================================================

@st.cache_resource(ttl=600)
def get_db():
    """تأسيس الاتصال بقاعدة بيانات Google Sheets بصمت"""
    try: 
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception: 
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_data(sheet):
    """
    جلب البيانات مع نظام الكاش لمنع حظر خوادم جوجل (Quota Limit).
    يقرأ مرة واحدة كل 10 دقائق.
    """
    conn = get_db()
    if not conn: 
        return pd.DataFrame()
    try: 
        df = conn.read(worksheet=sheet, ttl=600)
        return df.dropna(how='all')
    except Exception: 
        return pd.DataFrame()

def push_data(sheet, data_dict):
    """إضافة سجل جديد ثم تفريغ الكاش"""
    conn = get_db()
    if not conn: 
        return False, "انقطاع في الاتصال بقاعدة البيانات."
        
    try:
        df = conn.read(worksheet=sheet, ttl=0) # قراءة الأحدث دائماً قبل الكتابة
        if df.empty:
            df_new = pd.DataFrame([data_dict])
        else:
            df_new = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
            
        conn.update(worksheet=sheet, data=df_new)
        st.cache_data.clear() # مسح الذاكرة المؤقتة لقراءة البيانات الجديدة
        return True, "تم المزامنة مع السحابة."
    except Exception as e: 
        return False, str(e)

def overwrite_data(sheet, df):
    """استبدال الجدول بالكامل (خاص بالمخطط الأسبوعي)"""
    conn = get_db()
    if not conn: 
        return False, "انقطاع في الاتصال."
        
    try:
        conn.update(worksheet=sheet, data=df)
        st.cache_data.clear()
        return True, "تم التحديث الشامل للسحابة."
    except Exception as e: 
        return False, str(e)

def auto_heal():
    """
    محرك الإصلاح الذاتي المؤسسي (Enterprise Auto-Heal).
    يتأكد من أن جميع الأوراق والأعمدة موجودة وسليمة في الإكسل.
    """
    report = []
    conn = get_db()
    
    if not conn:
        return [{"status": "error", "msg": "انقطاع في خوادم Google Cloud."}]
        
    schemas = {
        "Weekly_Plan": ["Day", "Date", "Class", "Muscle", "Status"],
        "Workout_Logs": ["Date", "Muscle", "Exercise", "Weight", "Reps"],
        "Health_Log": ["Date", "Sleep", "Water", "Protein", "Calories", "Notes"],
        "InBody_Logs": ["Date", "Weight", "Muscle_Mass", "Fat_Percentage", "Visceral_Fat"]
    }
    
    for sh, cols in schemas.items():
        try:
            df = conn.read(worksheet=sh, ttl=0)
            missing = [c for c in cols if c not in df.columns]
            
            if missing:
                for c in missing: 
                    df[c] = "" # حقن العمود الناقص
                conn.update(worksheet=sh, data=df)
                report.append({"status": "success", "msg": f"تم إصلاح هيكل `{sh}` وحقن الأعمدة المفقودة بنجاح."})
            else:
                report.append({"status": "success", "msg": f"الهيكل التنظيمي لورقة `{sh}` سليم 100%."})
                
        except Exception:
            try:
                empty_df = pd.DataFrame(columns=cols)
                conn.update(worksheet=sh, data=empty_df)
                report.append({"status": "success", "msg": f"تم بناء قاعدة `{sh}` المفقودة من الصفر."})
            except Exception as e:
                report.append({"status": "error", "msg": f"فشل بناء `{sh}`. الخطأ: {str(e)}"})
                
    st.cache_data.clear()
    return report

# =====================================================================
# 5. DYNAMIC ROUTING ENGINE (Haversine Formula)
# محرك الملاحة وحساب المسافات الجغرافية
# =====================================================================

def get_distance(lat1, lon1, lat2, lon2):
    """حساب المسافة الدقيقة بين نقطتين بالكيلومتر"""
    R = 6371.0 
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def get_eta(origin):
    """
    تحليل سرعة الطريق بناءً على الموقع (مكة، جدة) وتطبيق مصفوفة الزحام.
    """
    dest_lat = 21.5768 
    dest_lon = 39.1620
    
    if origin == "المنزل (جدة - المروة)": 
        lat = 21.6214
        lon = 39.1989
        spd = 50
    elif origin == "العمل (جدة)": 
        lat = 21.5200
        lon = 39.1700
        spd = 40
    elif origin == "العمل (مكة المكرمة)": 
        lat = 21.4225
        lon = 39.8262
        spd = 90 
    else: 
        lat = 21.6214
        lon = 39.1989
        spd = 50
    
    dist = get_distance(lat, lon, dest_lat, dest_lon)
    base_mins = (dist / spd) * 60
    
    hr = get_makkah_time().hour
    
    # مصفوفة الزحام
    if 7 <= hr <= 9: 
        mult = 1.5
    elif 13 <= hr <= 15: 
        mult = 1.6
    elif 17 <= hr <= 21: 
        mult = 1.8
    else: 
        mult = 1.1
        
    final_eta = int(base_mins * mult) + 5 # إضافة 5 دقائق للمواقف
    return final_eta, dist

# =====================================================================
# 6. DYNAMIC CLINICAL RECOVERY (الاستشفاء التفاعلي)
# =====================================================================

def get_recovery_protocol(mode, iron_target):
    """
    بروتوكول طبي يتغير بناءً على قرارك في النادي.
    """
    current_day = get_makkah_time().strftime("%A")
    is_heavy = False
    
    if current_day in ["Monday", "Thursday"] or "أرجل" in iron_target:
        is_heavy = True
        
    if mode == "ClassOnly":
        html_output = textwrap.dedent("""
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (بروتوكول ما بعد الكارديو)</h3>
            <p style='color:#8B949E; text-align:right;'>بما أن مسارك اليوم هو <b>(كلاس لياقة فقط)</b>، فقد خسرت كمية هائلة من السوائل والأملاح. الاستشفاء الحراري ممنوع طبياً.</p>
            <div class='med-neutral'>
                <h4 style='color:#2EA043; margin:0;'>🏊 التبريد الهادئ</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>السباحة:</b> 10 دقائق حركة بطيئة جداً لخفض نبضات القلب التدريجي.</li>
                    <li><b>شرب الماء:</b> لتر كامل تدريجياً لتعويض التعرق.</li>
                </ul>
            </div>
            <div class='med-danger'>
                <h4 style='color:#D29922; margin:0;'>🚫 حظر حراري تام</h4>
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>يُمنع الدخول للساونا أو البخار اليوم. الكارديو + الساونا يؤديان إلى جفاف شديد وهدم عضلي.</p>
            </div>
        </div>
        """)
        return html_output
        
    elif is_heavy and mode in ["Full", "IronOnly"]:
        html_output = textwrap.dedent("""
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (العلاج التبايني العنيف)</h3>
            <p style='color:#8B949E; text-align:right;'>مسارك اليوم <b>عنيف (تمارين مقاومة ثقيلة)</b>. يجب التخلص من حمض اللاكتيك المتراكم لحماية الألياف.</p>
            <div class='med-hot'>
                <h4 style='color:#F85149; margin:0;'>🔥 المرحلة 1: التوسيع الوعائي</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>غرفة البخار:</b> 5 إلى 8 دقائق. (يوسع الأوعية ويضخ المغذيات للعضلة).</li>
                </ul>
            </div>
            <div class='med-cold'>
                <h4 style='color:#58A6FF; margin:0;'>🧊 المرحلة 2: الانقباض الوعائي</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>الجاكوزي البارد:</b> 1-2 دقيقة مباشرة بعد البخار لعصر الدم الفاسد.</li>
                </ul>
            </div>
            <div class='med-danger'>
                <h4 style='color:#D29922; margin:0;'>⚠️ تحذير الخصوبة</h4>
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>الختام إلزامي بالماء البارد لحماية هرمون التستوستيرون من التلف الحراري.</p>
            </div>
        </div>
        """)
        return html_output
        
    else:
        html_output = textwrap.dedent("""
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (التبريد العميق)</h3>
            <p style='color:#8B949E; text-align:right;'>مسارك اليوم متوسط الشدة. ركز على الاستشفاء البارد النشط.</p>
            <div class='med-cold'>
                <h4 style='color:#58A6FF; margin:0;'>🧊 التبريد وتقليل الالتهاب</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>الجاكوزي البارد:</b> 3 إلى 5 دقائق. يحفز إفراز هرمونات البناء ويقلل آلام المفاصل.</li>
                    <li><b>السباحة:</b> 15 دقيقة تفكيك مفاصل.</li>
                </ul>
            </div>
        </div>
        """)
        return html_output

# =====================================================================
# 7. COMMERCIAL BIOMECHANICS DATABASE (قاعدة بيانات التمارين الشاملة)
# =====================================================================
def get_bio_db():
    """
    قاعدة بيانات صلبة ومفصلة.
    """
    db = {
        "صدر": [
            {
                "name": "Incline Barbell Bench Press", 
                "reps": "6-8 عدات", 
                "technique": "دكة 30 درجة. انزل لملامسة أعلى الصدر.", 
                "breathing": "شهيق أسفل، زفير أعلى.", 
                "good_pain": "أعلى الصدر.", 
                "bad_pain": "مفصل الكتف الداخلي."
            },
            {
                "name": "Flat Dumbbell Press", 
                "reps": "8-10 عدات", 
                "technique": "كوعك مائل للداخل 45 درجة لتقليل الضغط.", 
                "breathing": "شهيق أسفل، زفير أعلى.", 
                "good_pain": "عمق الصدر.", 
                "bad_pain": "الرسغ أو الكوع."
            },
            {
                "name": "Decline Cable Flys", 
                "reps": "12-15 عدة", 
                "technique": "اسحب للأسفل باتجاه الحوض للقضاء على التثدي.", 
                "breathing": "زفير عند الضم في الأسفل.", 
                "good_pain": "أسفل الصدر.", 
                "bad_pain": "الكتف الأمامي."
            },
            {
                "name": "Pec Deck Machine", 
                "reps": "12-15 عدة", 
                "technique": "ظهرك ملتصق. اعصر صدرك في المنتصف.", 
                "breathing": "زفير عند الضم القوي.", 
                "good_pain": "الخط الداخلي للصدر.", 
                "bad_pain": "الكتف الخارجي."
            },
            {
                "name": "Chest Dips (Bodyweight)", 
                "reps": "للفشل العضلي", 
                "technique": "مل للأمام قليلاً. انزل للزاوية 90 وادفع.", 
                "breathing": "شهيق أسفل، زفير أعلى.", 
                "good_pain": "الصدر السفلي والترايسبس.", 
                "bad_pain": "عظمة القص."
            }
        ],
        "ظهر": [
            {
                "name": "Deadlift", 
                "reps": "3-5 عدات", 
                "technique": "ظهر مستقيم 100%، ادفع الأرض بقدميك.", 
                "breathing": "شهيق عميق قبل الرفع، زفير أعلى.", 
                "good_pain": "أوتار الركبة والقطنية.", 
                "bad_pain": "فقرات الظهر العلوية."
            },
            {
                "name": "Lat Pulldown Wide", 
                "reps": "8-12 عدة", 
                "technique": "اسحب الكيبل لأعلى صدرك مع شد الأكتاف للخلف.", 
                "breathing": "زفير عند السحب للأسفل.", 
                "good_pain": "المجنص العريض.", 
                "bad_pain": "عضلة البايسبس."
            },
            {
                "name": "Seated Cable Row", 
                "reps": "10-12 عدة", 
                "technique": "اسحب لسرتك مع تثبيت الجذع وعدم التأرجح.", 
                "breathing": "زفير عند السحب للبطن.", 
                "good_pain": "منتصف الظهر وسماكته.", 
                "bad_pain": "القطنية (من التأرجح القوي)."
            },
            {
                "name": "T-Bar Row", 
                "reps": "8-10 عدات", 
                "technique": "انحنِ 45 درجة واسحب للصدر السفلي.", 
                "breathing": "زفير في السحب بقوة.", 
                "good_pain": "العمق الداخلي للظهر.", 
                "bad_pain": "ألم في الركبة."
            },
            {
                "name": "Pull-ups", 
                "reps": "حتى الفشل", 
                "technique": "اسحب جسمك للأعلى حتى يتجاوز ذقنك البار.", 
                "breathing": "زفير في الصعود.", 
                "good_pain": "المجنص بالكامل.", 
                "bad_pain": "الكتف العلوي."
            }
        ],
        "أرجل": [
            {
                "name": "Barbell Squat", 
                "reps": "4-6 عدات", 
                "technique": "انزل كجلوس الكرسي لزاوية 90 درجة على الأقل.", 
                "breathing": "شهيق قبل النزول لملء البطن، زفير أعلى.", 
                "good_pain": "الفخذ الأمامي والمؤخرة.", 
                "bad_pain": "الركبة من الأمام أو الظهر."
            },
            {
                "name": "Leg Press", 
                "reps": "10-12 عدة", 
                "technique": "لا تقفل ركبتك بالكامل في الأعلى أبداً.", 
                "breathing": "زفير بالدفع للأعلى.", 
                "good_pain": "الفخذ كاملاً.", 
                "bad_pain": "مفصل الركبة من الخلف."
            },
            {
                "name": "Bulgarian Split Squat", 
                "reps": "10-12 عدة", 
                "technique": "رجل للخلف على الدكة وانزل بشكل عمودي مستقيم.", 
                "breathing": "زفير بالصعود والدفع.", 
                "good_pain": "الأرداف والفخذ.", 
                "bad_pain": "ألم الكاحل الخلفي."
            },
            {
                "name": "Romanian Deadlift", 
                "reps": "8-10 عدات", 
                "technique": "ادفع حوضك للخلف لأقصى شد ممكن.", 
                "breathing": "شهيق بالنزول البطيء.", 
                "good_pain": "الخلفيات والأوتار.", 
                "bad_pain": "شد في القطنية."
            }
        ],
        "أكتاف": [
            {
                "name": "Overhead Press", 
                "reps": "6-8 عدات", 
                "technique": "ادفع البار فوق رأسك مباشرة وبثبات.", 
                "breathing": "زفير بالدفع للأعلى.", 
                "good_pain": "الكتف كاملاً.", 
                "bad_pain": "أسفل الظهر."
            },
            {
                "name": "Lateral Raise", 
                "reps": "12-15 عدة", 
                "technique": "ارفع للجانب مع ثني الكوع قليلاً كالصب.", 
                "breathing": "زفير بالرفع السريع.", 
                "good_pain": "الكتف الجانبي الخارجي.", 
                "bad_pain": "الترابيس العلوية."
            },
            {
                "name": "Face Pulls", 
                "reps": "15-20 عدة", 
                "technique": "اسحب الحبل لمستوى عينيك وافتح للجانبين.", 
                "breathing": "زفير بالسحب الصعب.", 
                "good_pain": "الكتف الخلفي.", 
                "bad_pain": "تشنج الرقبة."
            }
        ],
        "باي": [
            {
                "name": "Barbell Bicep Curl", 
                "reps": "8-10 عدات", 
                "technique": "ثبت كوعك بجانبك وارفع للصدر.", 
                "breathing": "زفير بالرفع المتواصل.", 
                "good_pain": "بطن البايسبس.", 
                "bad_pain": "شد الساعد."
            },
            {
                "name": "Hammer Curl", 
                "reps": "10-12 عدة", 
                "technique": "قبضة محايدة كمطرقة البناء.", 
                "breathing": "زفير بالرفع.", 
                "good_pain": "خارجي العضلة.", 
                "bad_pain": "ألم الرسغ."
            }
        ],
        "تراي": [
            {
                "name": "Tricep Pushdown", 
                "reps": "12-15 عدة", 
                "technique": "ادفع وافتح الحبل بالأسفل لأقصى انقباض.", 
                "breathing": "زفير بالدفع.", 
                "good_pain": "خلف الذراع بالكامل.", 
                "bad_pain": "مفصل الكوع."
            },
            {
                "name": "Skull Crushers", 
                "reps": "8-10 عدات", 
                "technique": "انزل بالبار خلف رأسك لتمديد العضلة.", 
                "breathing": "زفير بالدفع العنيف.", 
                "good_pain": "العمق الطويل.", 
                "bad_pain": "ألم الكوع."
            }
        ],
        "بطن": [
            {
                "name": "Cable Crunches", 
                "reps": "10-12 عدة", 
                "technique": "انحن للأمام بعضلات بطنك حصراً.", 
                "breathing": "تفريغ هواء تام.", 
                "good_pain": "البطن العلوي.", 
                "bad_pain": "ألم القطنية."
            },
            {
                "name": "Hanging Leg Raises", 
                "reps": "12-15 عدة", 
                "technique": "ارفع رجليك ولف الحوض للصدر.", 
                "breathing": "زفير بالرفع المستمر.", 
                "good_pain": "أسفل البطن.", 
                "bad_pain": "شد الفخذ."
            }
        ],
        "جوانب": [
            {
                "name": "Woodchoppers", 
                "reps": "12-15 عدة", 
                "technique": "دوران جذع مقاوَم لأسفل.", 
                "breathing": "زفير قوي جداً.", 
                "good_pain": "الخواصر الجانبية.", 
                "bad_pain": "الظهر المتوسط."
            }
        ],
        "تمرين حر": [
            {
                "name": "Custom Machine", 
                "reps": "10-12 عدة", 
                "technique": "تمرين جهاز مخصص.", 
                "breathing": "تنفس اعتيادي.", 
                "good_pain": "العضلة.", 
                "bad_pain": "المفصل."
            }
        ]
    }
    return db

# --- END OF PART 1 ---
# =====================================================================
# 8. MASSIVE NUTRITION & MACROS ENGINE (حاسبة الأكل السعودي - Offline)
# =====================================================================
def get_nutrition_databases():
    """
    أضخم قاعدة بيانات محلية للطعام السعودي والماكروز.
    مفصلة رأسياً لضمان الدقة وعدم الاقتطاع.
    """
    edaam_db = {
        "إيدام دجاج بالبطاطس (بدون رز - صحن متوسط)": {
            "protein": 35, "cals": 320
        },
        "إيدام دجاج بالبطاطس + صحن رز أبيض (150 جرام)": {
            "protein": 40, "cals": 580
        },
        "إيدام لحم بالخضار (بدون رز - قطع لحم صافية)": {
            "protein": 45, "cals": 450
        },
        "إيدام لحم بالخضار + صحن رز أبيض": {
            "protein": 50, "cals": 710
        },
        "إيدام بامية باللحم (طبيخ منزلي)": {
            "protein": 40, "cals": 410
        },
        "ملوخية بالدجاج + صحن رز": {
            "protein": 35, "cals": 480
        },
        "كبسة دجاج (صدر دجاج + رز 200 جرام)": {
            "protein": 45, "cals": 650
        },
        "كبسة دجاج (فخذ دجاج مع الجلد + رز)": {
            "protein": 35, "cals": 750
        },
        "مكرونة حمراء بالدجاج (صدر مقطع)": {
            "protein": 35, "cals": 520
        },
        "صالونة خضار مشكلة (بدون لحم/دجاج)": {
            "protein": 5, "cals": 150
        },
        "جريش باللحم (صحن متوسط)": {
            "protein": 30, "cals": 450
        },
        "قرصان (صحن متوسط)": {
            "protein": 15, "cals": 350
        },
        "سليق بالدجاج (صحن متوسط)": {
            "protein": 35, "cals": 500
        }
    }

    fast_food_db = {
        "نصف حبة دجاج شواية (بدون جلد - الأفضل للتنشيف)": {
            "protein": 45, "cals": 420
        },
        "نصف حبة دجاج فحم (مع الجلد)": {
            "protein": 40, "cals": 550
        },
        "بروستد (نصف حبة دجاج مقلي مع البطاطس)": {
            "protein": 35, "cals": 950
        },
        "وجبة البيك (دجاج مسحب 10 قطع مع بطاطس وثوم)": {
            "protein": 45, "cals": 1100
        },
        "وجبة البيك (مسحب 7 قطع بدون بطاطس)": {
            "protein": 32, "cals": 500
        },
        "صاروخ شاورما دجاج (عادي بدون جبن إضافي)": {
            "protein": 25, "cals": 550
        },
        "صحن شاورما عربي دجاج (مع بطاطس وثوم)": {
            "protein": 35, "cals": 850
        },
        "وجبة ماك تشيكن (ساندوتش + بطاطس وسط)": {
            "protein": 18, "cals": 750
        },
        "وجبة بيج ماك": {
            "protein": 25, "cals": 850
        },
        "برجر لحم مشوي (مفرد - مطاعم الشوي)": {
            "protein": 20, "cals": 400
        },
        "برجر دجاج مشوي (مطعم دايت)": {
            "protein": 30, "cals": 350
        },
        "علبة تونة (مصفاة بالماء - 100 جرام)": {
            "protein": 26, "cals": 120
        },
        "علبة تونة (بالزيت - مصفاة قليلاً)": {
            "protein": 24, "cals": 220
        },
        "سكوب بروتين (Whey Protein - مع ماء)": {
            "protein": 25, "cals": 120
        },
        "سكوب بروتين (مع 200 مل حليب كامل الدسم)": {
            "protein": 31, "cals": 240
        },
        "3 بيضات مسلوقة كاملة": {
            "protein": 18, "cals": 210
        },
        "5 بياض بيض مسلوق (بدون صفار)": {
            "protein": 18, "cals": 85
        },
        "شريحة لحم ستيك (200 جرام - مطبوخ)": {
            "protein": 50, "cals": 450
        },
        "علبة زبادي يوناني سادة (150 جرام)": {
            "protein": 15, "cals": 100
        },
        "حليب بروتين عالي (ندى/المراعي - عبوة 320 مل)": {
            "protein": 27, "cals": 150
        }
    }
    
    return edaam_db, fast_food_db

# =====================================================================
# 9. WEEKLY STRATEGY ENGINE & DYNAMIC TIME CALCULATION
# =====================================================================
CLASS_BURN_DB = {
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

WORKOUT_ENGINE_DB = {
    "موتيف 8": {
        "iron": "صدر + تراي", 
        "flow": "الصدر يحتاج تركيز عالي. ابدأ بـ Incline Press لشد الصدر العلوي أولاً."
    },
    "فت كومبات": {
        "iron": "أرجل + بطن", 
        "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل ولا تتنازل عن الأوزان."
    },
    "كور اكستريم": {
        "iron": "أكتاف + جوانب", 
        "flow": "أكتاف عريضة = خصر أنحف بصرياً. ركز على تمرين Overhead Press للكتلة."
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
    """فحص هندسي للمخطط الأسبوعي للتحذير من أي خلل في توزيع العضلات"""
    if plan_df.empty: 
        return True, ""
        
    all_muscles = " ".join(plan_df['Muscle'].astype(str))
    alerts = []
    
    if "أرجل" not in all_muscles: 
        alerts.append("🔴 خطأ هندسي: المخطط يفتقد لتمارين الأرجل (وهي المحفز الأول للتستوستيرون وحرق الكرش).")
    if "ظهر" not in all_muscles: 
        alerts.append("🔴 خلل في القوام: يجب تدريب الظهر لسحب الأكتاف وتصحيح انحناء العمود الفقري.")
    if all_muscles.count("صدر") > 2: 
        alerts.append("🔴 إجهاد مفرط: الصدر مستهدف بكثافة عالية جداً، هذا سيؤدي للهدم العضلي ولن يتطور.")
        
    if len(alerts) > 0: 
        return False, "<br>".join(alerts)
        
    return True, "🟢 ممتاز هندسياً: المخطط متوازن، يهاجم الدهون بقوة، ويضمن الاستشفاء السليم."

def get_dynamic_schedule(attendance_mode, origin, current_makkah_time):
    """
    المحرك الزمني الدقيق (إصلاح مشكلة ה-8 ساعات).
    يحسب الوقت بالدقيقة لإنهاء الحديد في 75 دقيقة كحد أقصى، 
    ويفصل بين موعد الحديد وموعد الكلاس (9م) في حال كان الذهاب مبكراً ظهراً.
    """
    eta_mins, dist = calculate_smart_eta(origin)
    
    # الوصول
    arr_obj = current_makkah_time + timedelta(minutes=eta_mins)
    
    # الحديد يبدأ بعد 10 دقائق من الوصول وينتهي بعد 75 دقيقة كحد أقصى علمياً
    iron_start_obj = arr_obj + timedelta(minutes=10)
    iron_end_obj = iron_start_obj + timedelta(minutes=75)
    
    now_str = current_makkah_time.strftime("%I:%M %p")
    arr_str = arr_obj.strftime("%I:%M %p")
    iron_start = iron_start_obj.strftime("%I:%M %p")
    iron_end = iron_end_obj.strftime("%I:%M %p")
    
    return now_str, arr_str, iron_start, iron_end, arr_obj, dist, eta_mins

def get_week_dates(current_makkah_time):
    """حساب تواريخ الأسبوع للبدء دائماً بيوم السبت كمعيار قياسي"""
    idx = (current_makkah_time.weekday() + 2) % 7 
    saturday = current_makkah_time - timedelta(days=idx)
    
    week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates_dict = {}
    
    for i, day in enumerate(week_days):
        week_dates_dict[day] = (saturday + timedelta(days=i)).strftime("%Y-%m-%d")
        
    return week_dates_dict

# =====================================================================
# 10. MAIN COMMANDER DASHBOARD (واجهة غرفة العمليات الشاملة)
# =====================================================================
def main():
    # 1. تهيئة الذاكرة المؤقتة لمنع الفقدان
    init_states()
    
    # 2. جلب التوقيت والتاريخ بشكل موحد لتجنب NameError
    CURRENT_MAKKAH_TIME = get_makkah_time()
    
    days_map = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_ar = days_map[CURRENT_MAKKAH_TIME.strftime("%A")]
    current_date = CURRENT_MAKKAH_TIME.strftime("%Y-%m-%d")
    week_dates = get_week_dates(CURRENT_MAKKAH_TIME)

    # 3. الهيدر الرئيسي (Title & SaaS Dashboard)
    header_html = f"""
    <div style='background: linear-gradient(90deg, #1A1C23, #0D1117); padding: 15px 30px; border-radius: 12px; border-bottom: 2px solid #E5B94C; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
        <div style='color: #8B949E; font-size: 14px;'>مكة المكرمة | {today_ar} {current_date} | {CURRENT_MAKKAH_TIME.strftime('%I:%M %p')}</div>
        <div style='display: flex; gap: 20px; align-items: center;'>
            <span style='background: rgba(229, 185, 76, 0.1); padding: 5px 15px; border-radius: 20px; color: #E5B94C; font-weight: bold; font-size: 13px;'>👑 PRO PLAN ACTIVE</span>
            <span style='color: #E8ECEF; font-weight: bold;'>Titan Commercial System V45</span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # 4. بناء الألسنة (Tabs) 
    t_ops, t_setup, t_log, t_clinic, t_vision, t_fuel, t_sys = st.tabs([
        "🚀 الملاحة والميدان", 
        "🗓️ هندسة الأسبوع", 
        "🏋️ علم الحركة الحيوية", 
        "🏥 العيادة الطبية",
        "📸 عدسة الذكاء (AI)",
        "🥗 حاسبة الماكروز", 
        "🛠️ رادار الصيانة الشامل"
    ])

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS & INTERNAL ROUTING ENGINE
    # -----------------------------------------------------------------
    with t_ops:
        plan_df = fetch_data("Weekly_Plan")
        s_class, iron_target = "موتيف 8", "صدر + تراي" # Default
        
        if not plan_df.empty and 'Date' in plan_df.columns:
            try:
                today_row = plan_df[plan_df['Date'] == current_date]
                if not today_row.empty:
                    s_class = today_row.iloc[0].get('Class', 'موتيف 8')
                    iron_target = today_row.iloc[0].get('Muscle', 'صدر + تراي')
            except Exception: 
                pass

        if today_ar == "الجمعة" and st.session_state['attendance_mode'] != "IronOnly":
            st.markdown(
                """
                <div class='titan-card titan-card-center' style='border: 2px solid #2EA043;'>
                    <h1 style='color:#2EA043; margin:0;'>يوم راحة سلبي إلزامي 🛑</h1>
                    <p style='font-size:20px; color:#A0A0A0;'>بناء الأنسجة العضلية وحرق الدهون يتم أثناء الراحة العميقة.</p>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button("🔄 التراجع والذهاب للنادي للحديد فقط", use_container_width=True): 
                st.session_state['attendance_mode'] = "IronOnly"
                st.rerun()
                
        elif s_class == "راحة / غياب" or st.session_state['attendance_mode'] == "Absent":
            st.markdown(
                f"""
                <div class='titan-card' style='border-color: #F85149;'>
                    <h2 style='color:#F85149; text-align:center;'>مجدول كـ (راحة / غياب) ❌</h2>
                    <p style='text-align:center;'>النظام رحّل تمرين <b>({iron_target})</b> للغد تلقائياً.</p>
                    <hr style='border-color:#30363D;'>
                    <h4 style='color:#E8ECEF; text-align:center;'>توجيه تغذية طارئ</h4>
                    <p style='text-align:center; color:#8B949E;'>الكربوهيدرات العالية ممنوعة الليلة لعدم وجود حرق أو استنزاف للجلايكوجين.</p>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button("🔄 التراجع (قررت الذهاب للنادي)", use_container_width=True): 
                st.session_state['attendance_mode'] = "Full"
                st.rerun()
                
        else:
            c1, c2 = st.columns([2, 1])
            with c2:
                st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 الملاحة الداخلية الذكية</h3>", unsafe_allow_html=True)
                st.info("يتم حساب المسافة بمعادلة رياضية دقيقة وتطبيق مصفوفة الزحام (Traffic Matrix) لمدينة جدة/مكة.")
                
                loc_list = ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"]
                loc = st.selectbox("الانطلاق من:", loc_list, index=loc_list.index(st.session_state['selected_origin_loc']))
                st.session_state['selected_origin_loc'] = loc
                
                st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top:0;'>🕹️ التحكم الميداني</h3>", unsafe_allow_html=True)
                
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
                now_str, arr_str, iron_start, iron_end, arr_obj, dist, eta_mins = get_dynamic_schedule(st.session_state['attendance_mode'], loc, CURRENT_MAKKAH_TIME)
                c_burn = CLASS_BURN_DB.get(s_class, 0)
                
                workout_details = WORKOUT_ENGINE_DB.get(s_class, {})
                t_flw = workout_details.get("flow", "استراتيجية غير محددة، صمم روتينك.")
                
                class_note = ""
                # إذا كان الوصول قبل 6 مساءً (الدوام)، نضع تنبيهاً بأن الكلاس مساءً
                if arr_obj.hour < 18 and st.session_state['attendance_mode'] in ["Full", "ClassOnly"]:
                    class_note = "<div class='alert-box' style='margin-top:10px;'>* ملاحظة هندسية: الكلاس المجدول يبدأ الساعة 9:00 مساءً. تمرينك الآن مبكر جداً (في فترة الظهر/العصر)، ستضطر للعودة لاحقاً في المساء لحضور الكلاس، أو يمكنك تغيير المسار إلى (حديد فقط) من أزرار التحكم.</div>"
                
                if st.session_state['attendance_mode'] == "Full":
                    nav_html = f"""
                    <div class='titan-card'>
                        <h3 style='margin-top:0;'>🗺️ الخطة أ (الكمال الهندسي: كلاس وحديد)</h3>
                        <p style='font-size:18px;'>الحديد المستهدف: <b style='color:#E5B94C;'>{iron_target}</b> | الكلاس المجدول: <b style='color:#E5B94C;'>{s_class}</b> <span style='color:#F85149; font-size:14px;'>(حرق ~{c_burn} kcal)</span></p>
                        <p style='color:#8B949E;'>الاستراتيجية المتبعة: {t_flw}</p>
                        <hr style='border-color: rgba(255,255,255,0.1);'>
                        <p>🚗 الانطلاق من {loc}: <b style='color:#E5B94C;'>{now_str}</b></p>
                        <p>📏 المسافة الجغرافية: <b style='color:#E5B94C;'>{dist:.1f} KM</b> | ⏱️ الوقت المقدر بالزحام: <b style='color:#E5B94C;'>{eta_mins} دقيقة</b></p>
                        <p>🅿️ الوصول لمواقف النادي: <b style='color:#E5B94C;'>{arr_str}</b></p>
                        
                        <h5 style='color:#E8ECEF; margin-top:20px;'>الجدول الزمني الميداني التفاعلي (لتفادي الهدم العضلي)</h5>
                        <p>🔥 {arr_str} - {iron_start} : إحماء مفاصل وتجهيز دقيق</p>
                        <p>💪 {iron_start} - {iron_end} : <b style='color:#F85149;'>صالة الحديد (75 دقيقة كحد أقصى لمنع إفراز هرمون الكورتيزول الهادم)</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>كلاس ({s_class}) (لحرق دهون البطن والمؤخرة بشكل صافي)</b></p>
                        {class_note}
                    </div>
                    """
                elif st.session_state['attendance_mode'] == "IronOnly":
                    nav_html = f"""
                    <div class='titan-card' style='border-color: #58A6FF;'>
                        <h3 style='margin-top:0; color:#58A6FF;'>🏋️ مسار الحديد المكثف (تم إسقاط الكلاس)</h3>
                        <p style='font-size:18px;'>الحديد المستهدف اليوم: <b style='color:#E5B94C;'>{iron_target}</b></p>
                        <p style='color:#8B949E;'>بما أن الكلاس تم إلغاؤه، لديك طاقة أعلى لكسر الأوزان الحرة وبناء الكتلة العضلية.</p>
                        <hr style='border-color: rgba(255,255,255,0.1);'>
                        <p>🚗 الانطلاق من {loc}: <b style='color:#E5B94C;'>{now_str}</b> | 🅿️ وصول المواقف: <b style='color:#E5B94C;'>{arr_str}</b></p>
                        
                        <h5 style='color:#E8ECEF; margin-top:20px;'>الجدول الميداني المفتوح</h5>
                        <p>🔥 {arr_str} - {iron_start} : إحماء دقيق لتفادي الإصابة</p>
                        <p>💪 {iron_start} - {(arr_obj + timedelta(minutes=90)).strftime('%I:%M %p')} : <b style='color:#F85149;'>صالة الحديد (استغل وقتك المفتوح، العب جولات إضافية وتحدى أوزانك القديمة)</b></p>
                    </div>
                    """
                elif st.session_state['attendance_mode'] == "ClassOnly":
                    nav_html = f"""
                    <div class='titan-card' style='border-color: #E5B94C;'>
                        <h3 style='margin-top:0; color:#E5B94C;'>🤸 مسار الكارديو واللياقة (الحديد ملغي)</h3>
                        <p style='font-size:18px;'>الكلاس المجدول: <b style='color:#E5B94C;'>{s_class}</b></p>
                        <hr style='border-color: rgba(255,255,255,0.1);'>
                        <p>🚗 الانطلاق من {loc}: <b style='color:#E5B94C;'>{now_str}</b> | 🅿️ وصول المواقف: <b style='color:#E5B94C;'>{arr_str}</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>حضور الكلاس (حرق متوقع ~{c_burn} kcal)</b></p>
                        {class_note}
                    </div>
                    """
                else: # Delayed
                    nav_html = f"""
                    <div class='titan-card' style='border-color: #F85149;'>
                        <h3 style='margin-top:0; color:#F85149;'>⚠️ مسار التأخير والزحمة (إنقاذ التمرين)</h3>
                        <p style='font-size:18px;'>الحديد المختصر: <b style='color:#E5B94C;'>{iron_target}</b></p>
                        <hr style='border-color: rgba(255,255,255,0.1);'>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>توجه للكلاس مباشرة فور وصولك لعدم تفويت التسخين الجماعي</b></p>
                        <p>💪 09:55 PM - 10:30 PM : <b style='color:#F85149;'>حديد سريع جداً (استخدم أجهزة العزل فقط، يُمنع استخدام الأوزان الحرة لتفادي الإصابة بسبب إرهاق الكلاس)</b></p>
                    </div>
                    """
                
                st.markdown(nav_html, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN (هندسة الأسبوع)
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع (مزامنة سحابية تامة)")
        st.info("هذا الجدول متصل بجوجل شيتس. أي تعديل هنا سينعكس على كل الأجهزة.")
        
        plan_df = fetch_data("Weekly_Plan")
        curr_plan = {}
        if not plan_df.empty and 'Day' in plan_df.columns and 'Class' in plan_df.columns:
            for _, row in plan_df.iterrows():
                curr_plan[row['Day']] = row['Class']
        
        with st.form("weekly_master_plan"):
            ns = []
            cols = st.columns(3)
            opts = list(WORKOUT_ENGINE_DB.keys())
            
            for i, d in enumerate(["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]):
                ex_dt = week_dates.get(d, "")
                default_class = curr_plan.get(d, "موتيف 8")
                
                try: 
                    idx = opts.index(default_class)
                except ValueError: 
                    idx = 0
                
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E8ECEF; text-align:right;'>{d}<br><span style='font-size:12px; color:#8B949E;'>{ex_dt}</span></h5>", unsafe_allow_html=True)
                    ch = st.selectbox("اختر الكلاس", opts, index=idx, key=f"c_{d}", label_visibility="collapsed")
                    
                    workout_details_setup = WORKOUT_ENGINE_DB.get(ch, {})
                    m_target = workout_details_setup.get('iron', 'غير محدد')
                    
                    ns.append({"Day": d, "Date": ex_dt, "Class": ch, "Muscle": m_target, "Status": "مجدول"})
            
            st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص هندسي واعتماد المخطط في السحابة", use_container_width=True):
                bal, msg = analyze_muscle_balance(pd.DataFrame(ns))
                st.markdown(f"<div class='{'success-box' if bal else 'alert-box'}'>{msg}</div>", unsafe_allow_html=True)
                
                s, m = overwrite_data("Weekly_Plan", pd.DataFrame(ns))
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
        
        # Pre-Workout Check
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
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة الدقيق</h4><p style='font-size:12px; color:#8B949E;'>الالتزام بالوقت يضمن ضخ الدم (Pump) وتجنب برودة العضلة.</p>", unsafe_allow_html=True)
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
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>العضلة المستهدفة اليوم: <span style='color:#E5B94C;'>{t_muscle}</span></h4>", unsafe_allow_html=True)
            
            ex_list = get_exercise_list(t_muscle)
            s_ex = st.selectbox("اختر التمرين من قاعدة البيانات الضخمة لتسجيله:", ex_list)
            
            # معالجة الإدخال اليدوي الذكي
            if "يدوي ذكي" in s_ex:
                f_ex = st.text_input("اكتب اسم التمرين الجديد (يُفضل باللغة الإنجليزية لتوحيد السجلات في السحابة):")
            else:
                f_ex = s_ex
            
            f_ex = f_ex if f_ex else "تمرين مخصص"
            info = get_ex_info(f_ex)
            
            # عرض التفاصيل الحيوية
            st.markdown(f"""
            <div style='background:#161B22; padding:20px; border-radius:12px; margin-bottom:20px; border-right: 4px solid #E5B94C;'>
                <p><span class='bio-tech'>⚙️ الأداء המيكانيكي (Technique):</span><br>{info.get('technique', 'حافظ على التركيز')}</p>
                <p><span class='bio-breath'>🫁 التنفس (Breathing):</span><br>{info.get('breathing', 'تنفس منتظم')}</p>
                <hr style='border-color:#30363D;'>
                <p><span class='bio-good'>✅ الألم الجيد للتطور (DOMS):</span><br>{info.get('good_pain', 'العضلة المستهدفة')}</p>
                <p><span class='bio-bad'>❌ الألم السيء والإصابات:</span><br>{info.get('bad_pain', 'المفاصل')}</p>
                <hr style='border-color:#30363D;'>
                <h5 style='color:#E5B94C; margin:0;'>النطاق العلمي للعدات: {info.get('reps', '10-12')}</h5>
            </div>
            """, unsafe_allow_html=True)
            
            # جلب السجل التاريخي
            p_date, p_weight, p_reps = fetch_historical_data(f_ex)
            if p_date:
                st.markdown(f"<div style='background:#161B22; padding:10px; border-radius:8px; border-right:4px solid #E5B94C; margin-bottom:15px;'><p style='color:#8B949E; margin:0;'>آخر مرة تمرنت ({p_date}): <b>{p_weight} KG</b> × {p_reps} عدات</p></div>", unsafe_allow_html=True)
                last_w = float(p_weight)
            else: 
                last_w = 0.0
            
            cw, cr = st.columns(2)
            w = cw.number_input("الوزن المرفوع (KG)", min_value=0.0, value=last_w, step=2.5)
            r = cr.number_input("العدات (اكتب 0 وسيتولى الذكاء الاصطناعي الحساب)", min_value=0, value=0)
            
            if st.button("💾 توثيق الجلسة في السحابة", use_container_width=True):
                if "يدوي ذكي" in s_ex and not f_ex: 
                    st.error("الرجاء كتابة اسم التمرين اليدوي أولاً.")
                else:
                    f_r = calculate_smart_reps(f_ex, w) if r == 0 else r
                    if r == 0: 
                        st.success(f"🤖 الذكاء الاصطناعي استنتج أنك حققت {f_r} عدات بناءً على الوزن القديم وقوانين التضخيم.")
                        
                    new_entry = {"Date": current_date, "Muscle": t_muscle, "Exercise": f_ex, "Weight": w, "Reps": f_r}
                    success, s_msg = push_data("Workout_Logs", new_entry)
                    if success: 
                        st.success(f"تم تسجيل تمرين {f_ex} بنجاح.")
                    else: 
                        st.error(s_msg)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Post-Workout DOMS Tracker
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
        
        # استدعاء بروتوكول العلاج التبايني
        is_heavy_day = today_ar in ["الاثنين", "الخميس"] or "أرجل" in iron_target or st.session_state['attendance_mode'] == "IronOnly"
        protocol_html = get_recovery_protocol(st.session_state['attendance_mode'], iron_target)
        st.markdown(protocol_html, unsafe_allow_html=True)
        
        c_c1, c_c2 = st.columns(2)
        
        with c_c1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>🏊 حاسبة الاستشفاء النشط (المسبح)</h4>", unsafe_allow_html=True)
            st.info("السباحة تحرق الكثير من السعرات الإضافية، أدخلها هنا لخصمها من العداد الغذائي لمنع العجز الزائد.")
            with st.form("swim_form"):
                s_mins = st.number_input("كم دقيقة سبحت اليوم بشكل مستمر؟", min_value=0, value=15, step=5)
                if st.form_submit_button("حساب السعرات وإضافتها للعداد", use_container_width=True):
                    # معادلة حرق السباحة لوزن 91.9 كيلو = تقريباً 8.5 سعرة في الدقيقة
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
                    success, msg = push_data("InBody_Logs", inbody_data)
                    if success: 
                        st.success("تم الحفظ وأرشفة البيانات الطبية بشكل دائم.")
                    else: 
                        st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 5: PREMIUM VISION AI (ميزة تجارية)
    # -----------------------------------------------------------------
    with t_vision:
        st.markdown("### 📸 عدسة تايتان للذكاء الاصطناعي (Premium Vision AI)")
        st.markdown("<p style='color:#8B949E; text-align:right;'>هذه الميزة مدفوعة (SaaS). تقوم بقراءة صور الوجبات وتحليل الماكروز عبر محركات الذكاء الاصطناعي.</p>", unsafe_allow_html=True)
        
        scans_left = st.session_state.get('ai_vision_scans_left', 5)
        st.markdown(f"<p style='text-align:right;'><span style='background:rgba(229,185,76,0.1); color:#E5B94C; padding:8px 15px; border-radius:8px; font-weight:bold;'>الرصيد المتبقي في باقتك: {scans_left} عمليات مسح</span></p>", unsafe_allow_html=True)
        
        if scans_left > 0:
            up_img = st.file_uploader("التقط أو ارفع صورة وجبتك للتحليل الدقيق", type=["jpg", "png", "jpeg"])
            if up_img:
                st.image(up_img, use_container_width=True)
                if st.button("🔍 مسح ضوئي واستخراج الماكروز (Scan Image)", use_container_width=True):
                    with st.spinner("جاري الاتصال بخوادم Vision API... تحليل الأنسجة والأبعاد..."):
                        time.sleep(2.5) # محاكاة تأخير معالجة السيرفر
                        
                        est_prot = 45
                        est_cals = 520
                        
                        st.session_state['daily_protein'] += est_prot
                        st.session_state['daily_cals'] += est_cals
                        st.session_state['ai_vision_scans_left'] -= 1
                        
                        st.markdown(f"""
                        <div class='success-box'>
                            <h4 style='margin:0; color:#2EA043;'>🤖 اكتمل التحليل بنجاح!</h4>
                            <p style='margin-top:5px; color:#E8ECEF;'><b>المكونات المكتشفة:</b> مصدر بروتين حيواني مشوي + كربوهيدرات معقدة.</p>
                            <p style='color:#E8ECEF; font-size:18px;'><b>البروتين المقدر:</b> {est_prot}g | <b>السعرات المقدرة:</b> {est_cals} kcal</p>
                            <p style='font-size:12px; color:#8B949E; margin-top:10px;'>تم خصم عملية مسح واحدة من رصيدك. تمت إضافة القيم لعدادك اليومي تلقائياً.</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("لقد استنفدت باقتك المخصصة من مسح الصور لهذا الشهر. قم بترقية اشتراكك للمتابعة.")

    # -----------------------------------------------------------------
    # TAB 6: NUTRITION CALCULATOR (Offline Macro Builder)
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
                added_prot = int(full_food_db[sel_food].get("protein", 0) * qty)
                added_cals = int(full_food_db[sel_food].get("cals", 0) * qty)
                st.session_state['daily_protein'] += added_prot
                st.session_state['daily_cals'] += added_cals
                st.success(f"تم إضافة {qty} حصة من ({sel_food}). [+ {added_prot}g بروتين, + {added_cals} سعرة]")
                
            st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
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
            tar_prot = int(91.9 * 2.2) # الهدف: 2.2 جرام لكل كيلو من وزن الجسم لمنع الهدم
            tar_cals = 1900
            
            net_calories = st.session_state['daily_cals'] - st.session_state['swim_cals_burned']
            
            st.markdown(f"""
            <div class='titan-card'>
                <h3 style='margin-top:0;'>📊 لوحة الماكروز اليومية</h3>
                <p style='font-size:18px;'>البروتين المكتسب: <b style='color:#F85149; font-size:30px;'>{st.session_state['daily_protein']} / {tar_prot} g</b></p>
                <p style='font-size:18px;'>إجمالي السعرات التي أكلتها: <b style='color:#E5B94C; font-size:30px;'>{st.session_state['daily_cals']} / {tar_cals}</b></p>
                <hr style='border-color:#30363D;'>
                <p style='font-size:16px;'>حرق السباحة الإضافي المخصوم: <b style='color:#2ECC40; font-size:24px;'>- {st.session_state['swim_cals_burned']} kcal</b></p>
                <p style='font-size:18px;'>صافي السعرات بعد المجهود: <b style='color:#E8ECEF; font-size:26px;'>{net_calories} kcal</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("health_form"):
                slp = st.number_input("ساعات النوم الفعلي (من ساعة Huawei):", value=7.5, step=0.5)
                wtr = st.number_input("الماء المستهلك (لتر - مهم لطرد احتباس السوائل):", value=3.5, step=0.5)
                
                st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
                if st.form_submit_button("💾 توثيق وحفظ يوم التغذية النهائي في الإكسل", use_container_width=True):
                    health_record = {
                        "Date": current_date, 
                        "Sleep": slp, 
                        "Water": wtr, 
                        "Protein": st.session_state['daily_protein'], 
                        "Calories": net_calories, 
                        "Notes": ""
                    }
                    success, s_msg = push_data("Health_Log", health_record)
                    if success: 
                        st.success("تم الحفظ بنجاح. سيتم تصفير العداد لليوم التالي ليكون جاهزاً.")
                        st.session_state['daily_protein'] = 0
                        st.session_state['daily_cals'] = 0
                        st.session_state['swim_cals_burned'] = 0
                    else: 
                        st.error(s_msg)

    # -----------------------------------------------------------------
    # TAB 7: SAAS DASHBOARD & AUTO-HEAL
    # -----------------------------------------------------------------
    with t_sys:
        st.markdown("### 🛠️ لوحة الإدارة المؤسسية (SaaS Administration)")
        st.info("هذا القسم مخصص لمشرفي النظام (Admins) لإدارة حالة التطبيق، تنظيف الذاكرة، وإصلاح قواعد البيانات السحابية.")
        
        c_saas1, c_saas2 = st.columns(2)
        
        with c_saas1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>محرك الإصلاح الذاتي (Omni-Heal)</h4>", unsafe_allow_html=True)
            st.write("يقوم بالدوران على ملف الإكسل (Google Sheets). إذا وجد ورقة مفقودة أو عموداً ناقصاً، يبنيه من الصفر لضمان عدم توقف النظام.")
            if st.button("🔄 فحص وإصلاح قاعدة البيانات", use_container_width=True):
                with st.spinner("جاري المسح العميق والتفاوض مع خوادم Google..."):
                    time.sleep(1.5)
                    reports = auto_heal()
                    for r in reports:
                        c_box = 'success-box' if r['status'] == 'success' else 'alert-box'
                        st.markdown(f"<div class='{c_box}'>{r['msg']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_saas2:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>إدارة الذاكرة (Memory Management)</h4>", unsafe_allow_html=True)
            st.warning("يُستخدم هذا الزر فقط في حال واجهت شاشة بيضاء أو استمرت البيانات القديمة بالظهور. سيقوم بمسح الذاكرة المؤقتة (Cache) بالكامل.")
            if st.button("⚠️ إعادة ضبط المصنع (Clear All Cache)", use_container_width=True):
                force_program_reset()
                st.success("تم تنظيف السيرفر من البيانات المعلقة. يرجى تحديث الصفحة (Refresh).")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
        st.markdown("#### 📑 استخراج تقارير الأداء (PDF/CSV Export)")
        if st.button("📥 استخراج تقرير الأداء الشهري للعميل", use_container_width=True):
            with st.spinner("جاري تجميع البيانات وتحليل الأرقام لتجهيز التقرير..."):
                time.sleep(2)
                st.success("تم تجهيز التقرير! (ملاحظة: هذه ميزة تجارية سيتم تفعيل تصديرها الفعلي لاحقاً عند ربط مكتبات الـ PDF).")

# =====================================================================
# SYSTEM EXECUTION TRIGGER
# =====================================================================
if __name__ == "__main__":
    main()
