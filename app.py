import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time
import math
import textwrap

# =====================================================================
# 1. CORE ARCHITECTURE & SAAS INITIALIZATION
# إعدادات النظام المعمارية الأساسية للواجهة التجارية
# =====================================================================

st.set_page_config(
    page_title="Titan V43 - The Maximum Enterprise Capacity", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_makkah_time():
    """
    محرك التوقيت الدقيق لمكة المكرمة (UTC+3).
    يتم استدعاء هذه الدالة في كل حركة لضمان التزامن اللحظي الميداني.
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
    مكتبة التصميم الشاملة بتدرجات OLED لتقليل استهلاك البطارية.
    تم فك جميع أسطر الـ CSS لمنع أي تداخل.
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
        }
        
        /* التبويبات العلوية (SaaS Navigation) */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 10px; 
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
            padding: 10px 20px; 
            color: #8B949E; 
            font-size: 14px; 
            font-weight: 600; 
            transition: all 0.2s ease; 
        }
        
        .stTabs [aria-selected="true"] { 
            background-color: rgba(229, 185, 76, 0.1) !important; 
            border-color: #E5B94C !important; 
            color: #E5B94C !important; 
            box-shadow: 0 4px 15px rgba(229, 185, 76, 0.15); 
        }
        
        /* البطاقات الاحترافية */
        .titan-card { 
            background: #0D1117; 
            border: 1px solid #30363D; 
            border-radius: 16px; 
            padding: 25px; 
            margin-bottom: 20px; 
            text-align: right; 
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
        }
        
        .titan-card:hover { 
            border-color: #8B949E; 
            transform: translateY(-2px); 
            box-shadow: 0 8px 24px rgba(0,0,0,0.4); 
        }
        
        .titan-card-center { 
            text-align: center; 
        }
        
        /* البروتوكولات الطبية التفاعلية */
        .med-hot { 
            background: rgba(248, 81, 73, 0.05); 
            border-right: 4px solid #F85149; 
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        .med-cold { 
            background: rgba(88, 166, 255, 0.05); 
            border-right: 4px solid #58A6FF; 
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        .med-neutral { 
            background: rgba(46, 160, 67, 0.05); 
            border-right: 4px solid #2EA043; 
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        .med-danger { 
            background: rgba(210, 153, 34, 0.05); 
            border-right: 4px solid #D29922; 
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 15px; 
            text-align: right; 
        }
        
        /* المربعات التحذيرية */
        .alert-box { 
            background: rgba(248, 81, 73, 0.1); 
            border: 1px solid #F85149; 
            padding: 15px; 
            border-radius: 8px; 
            color: #F85149; 
            text-align: right; 
            margin-bottom: 15px; 
        }
        
        .success-box { 
            background: rgba(46, 160, 67, 0.1); 
            border: 1px solid #2EA043; 
            padding: 15px; 
            border-radius: 8px; 
            color: #2EA043; 
            text-align: right; 
            margin-bottom: 15px; 
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
# 3. ENTERPRISE STATE MANAGEMENT (إدارة الذاكرة والمتغيرات)
# =====================================================================

def init_states():
    """
    تهيئة جميع متغيرات الجلسة بوضوح لمنع أي خطأ (KeyError).
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
        st.session_state['ai_vision_scans_left'] = 5
        
    if 'is_premium_user' not in st.session_state:
        st.session_state['is_premium_user'] = True

init_states()

# =====================================================================
# 4. SECURE CLOUD CONNECTORS & AUTO-HEAL
# محركات الاتصال بقواعد البيانات السحابية والإصلاح الذاتي
# =====================================================================

@st.cache_resource(ttl=600)
def get_db():
    """تأسيس الاتصال بقاعدة بيانات Google Sheets"""
    try: 
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception: 
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_data(sheet):
    """
    جلب البيانات مع نظام الكاش لمنع حظر خوادم جوجل.
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
        return False, "انقطاع في الاتصال."
    try:
        df = conn.read(worksheet=sheet, ttl=0)
        if df.empty:
            df_new = pd.DataFrame([data_dict])
        else:
            df_new = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
            
        conn.update(worksheet=sheet, data=df_new)
        st.cache_data.clear()
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
    """محرك الإصلاح الذاتي المؤسسي (Enterprise Auto-Heal)"""
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
                    df[c] = ""
                conn.update(worksheet=sh, data=df)
                report.append({"status": "success", "msg": f"تم إصلاح هيكل `{sh}` وحقن الأعمدة المفقودة."})
            else:
                report.append({"status": "success", "msg": f"هيكل `{sh}` سليم 100%."})
        except Exception:
            try:
                conn.update(worksheet=sh, data=pd.DataFrame(columns=cols))
                report.append({"status": "success", "msg": f"تم بناء قاعدة `{sh}` المفقودة من الصفر."})
            except Exception as e:
                report.append({"status": "error", "msg": f"فشل بناء `{sh}`. الخطأ: {str(e)}"})
                
    st.cache_data.clear()
    return report

# =====================================================================
# 5. DYNAMIC ROUTING ENGINE (Haversine)
# محرك الملاحة وحساب المسافات الجغرافية الدقيقة
# =====================================================================

def get_distance(lat1, lon1, lat2, lon2):
    """حساب المسافة الجغرافية بالكيلومتر"""
    R = 6371.0 
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def get_eta(origin):
    """تحليل سرعة الطريق بناءً على الموقع ومصفوفة الزحام"""
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
    
    if 7 <= hr <= 9: 
        mult = 1.5
    elif 13 <= hr <= 15: 
        mult = 1.6
    elif 17 <= hr <= 21: 
        mult = 1.8
    else: 
        mult = 1.1
        
    final_eta = int(base_mins * mult) + 5
    return final_eta, dist

# =====================================================================
# 6. DYNAMIC CLINICAL RECOVERY (الاستشفاء التفاعلي)
# =====================================================================

def get_recovery_protocol(mode, iron_target):
    """
    بروتوكول طبي يتغير بناءً على قرارك في النادي.
    """
    if mode == "ClassOnly":
        html_output = """
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
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>يُمنع الدخول للساونا أو البخار اليوم. الكارديو + الساونا يؤديان إلى جفاف شديد، هدم عضلي، وارتفاع هرمون التوتر (الكورتيزول).</p>
            </div>
        </div>
        """
        return html_output
        
    is_heavy = False
    current_day = get_makkah_time().strftime("%A")
    if current_day in ["Monday", "Thursday"]:
        is_heavy = True
    if "أرجل" in iron_target:
        is_heavy = True
        
    if is_heavy and mode in ["Full", "IronOnly"]:
        html_output = """
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (العلاج التبايني العنيف)</h3>
            <p style='color:#8B949E; text-align:right;'>مسارك اليوم <b>عنيف (تمارين مقاومة ثقيلة)</b>. يجب التخلص من حمض اللاكتيك المتراكم لحماية الألياف.</p>
            <div class='med-hot'>
                <h4 style='color:#F85149; margin:0;'>🔥 المرحلة 1: التوسيع (Vasodilation)</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>غرفة البخار:</b> 5 إلى 8 دقائق. (يوسع الأوعية ويضخ المغذيات للعضلة).</li>
                </ul>
            </div>
            <div class='med-cold'>
                <h4 style='color:#58A6FF; margin:0;'>🧊 المرحلة 2: الانقباض (Vasoconstriction)</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>الجاكوزي البارد:</b> 1-2 دقيقة مباشرة بعد البخار لعصر الدم الفاسد.</li>
                </ul>
            </div>
            <div class='med-danger'>
                <h4 style='color:#D29922; margin:0;'>⚠️ تحذير الخصوبة</h4>
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>الختام إلزامي بالماء البارد لحماية هرمون التستوستيرون من التلف الحراري.</p>
            </div>
        </div>
        """
        return html_output
    else:
        html_output = """
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
        """
        return html_output

# =====================================================================
# 7. COMMERCIAL BIOMECHANICS DATABASE (توسع تجاري للتمارين)
# =====================================================================
def get_bio_db():
    """
    قاعدة بيانات صلبة ومفصلة للتمارين.
    كل تمرين مستقل في أسطر خاصة به لمنع الدمج الخاطئ.
    """
    db = {
        "صدر": [
            {
                "n": "Incline Barbell Bench Press", 
                "r": "6-8", 
                "t": "دكة 30 درجة. انزل لملامسة أعلى الصدر.", 
                "b": "شهيق أسفل، زفير أعلى.", 
                "gp": "أعلى الصدر.", 
                "bp": "مفصل الكتف الداخلي."
            },
            {
                "n": "Flat Dumbbell Press", 
                "r": "8-10", 
                "t": "كوعك مائل للداخل 45 درجة لتقليل الضغط.", 
                "b": "شهيق أسفل، زفير أعلى.", 
                "gp": "عمق الصدر.", 
                "bp": "الرسغ أو الكوع."
            },
            {
                "n": "Decline Cable Flys", 
                "r": "12-15", 
                "t": "اسحب للأسفل باتجاه الحوض للقضاء على التثدي.", 
                "b": "زفير عند الضم في الأسفل.", 
                "gp": "أسفل الصدر.", 
                "bp": "الكتف الأمامي."
            },
            {
                "n": "Pec Deck Machine", 
                "r": "12-15", 
                "t": "ظهرك ملتصق. اعصر صدرك في المنتصف.", 
                "b": "زفير عند الضم القوي.", 
                "gp": "الخط الداخلي للصدر.", 
                "bp": "الكتف الخارجي."
            },
            {
                "n": "Chest Dips (Bodyweight)", 
                "r": "للفشل العضلي", 
                "t": "مل للأمام قليلاً. انزل للزاوية 90 وادفع.", 
                "b": "شهيق أسفل، زفير أعلى.", 
                "gp": "الصدر السفلي والترايسبس.", 
                "bp": "عظمة القص."
            }
        ],
        "ظهر": [
            {
                "n": "Deadlift", 
                "r": "3-5", 
                "t": "ظهر مستقيم 100%، ادفع الأرض بقدميك.", 
                "b": "شهيق عميق قبل الرفع، زفير أعلى.", 
                "gp": "أوتار الركبة والقطنية.", 
                "bp": "فقرات الظهر العلوية."
            },
            {
                "n": "Lat Pulldown Wide", 
                "r": "8-12", 
                "t": "اسحب الكيبل لأعلى صدرك مع شد الأكتاف للخلف.", 
                "b": "زفير عند السحب للأسفل.", 
                "gp": "المجنص العريض.", 
                "bp": "عضلة البايسبس."
            },
            {
                "n": "Seated Cable Row", 
                "r": "10-12", 
                "t": "اسحب لسرتك مع تثبيت الجذع وعدم التأرجح.", 
                "b": "زفير عند السحب للبطن.", 
                "gp": "منتصف الظهر وسماكته.", 
                "bp": "القطنية (من التأرجح القوي)."
            },
            {
                "n": "T-Bar Row", 
                "r": "8-10", 
                "t": "انحنِ 45 درجة واسحب للصدر السفلي.", 
                "b": "زفير في السحب بقوة.", 
                "gp": "العمق الداخلي للظهر.", 
                "bp": "ألم في الركبة."
            }
        ],
        "أرجل": [
            {
                "n": "Barbell Squat", 
                "r": "4-6", 
                "t": "انزل كجلوس الكرسي لزاوية 90 درجة على الأقل.", 
                "b": "شهيق قبل النزول لملء البطن، زفير أعلى.", 
                "gp": "الفخذ الأمامي والمؤخرة.", 
                "bp": "الركبة من الأمام أو الظهر."
            },
            {
                "n": "Leg Press", 
                "r": "10-12", 
                "t": "لا تقفل ركبتك بالكامل في الأعلى أبداً.", 
                "b": "زفير بالدفع للأعلى.", 
                "gp": "الفخذ كاملاً.", 
                "bp": "مفصل الركبة من الخلف."
            },
            {
                "n": "Bulgarian Split Squat", 
                "r": "10-12", 
                "t": "رجل للخلف على الدكة وانزل بشكل عمودي مستقيم.", 
                "b": "زفير بالصعود والدفع.", 
                "gp": "الأرداف والفخذ.", 
                "bp": "ألم الكاحل الخلفي."
            },
            {
                "n": "Romanian Deadlift", 
                "r": "8-10", 
                "t": "ادفع حوضك للخلف لأقصى شد ممكن.", 
                "b": "شهيق بالنزول البطيء.", 
                "gp": "الخلفيات والأوتار.", 
                "bp": "شد في القطنية."
            }
        ],
        "أكتاف": [
            {
                "n": "Overhead Press", 
                "r": "6-8", 
                "t": "ادفع البار فوق رأسك مباشرة وبثبات.", 
                "b": "زفير بالدفع للأعلى.", 
                "gp": "الكتف كاملاً.", 
                "bp": "أسفل الظهر."
            },
            {
                "n": "Lateral Raise", 
                "r": "12-15", 
                "t": "ارفع للجانب مع ثني الكوع قليلاً كالصب.", 
                "b": "زفير بالرفع السريع.", 
                "gp": "الكتف الجانبي الخارجي.", 
                "bp": "الترابيس العلوية."
            },
            {
                "n": "Face Pulls", 
                "r": "15-20", 
                "t": "اسحب الحبل لمستوى عينيك وافتح للجانبين.", 
                "b": "زفير بالسحب الصعب.", 
                "gp": "الكتف الخلفي.", 
                "bp": "تشنج الرقبة."
            }
        ],
        "باي": [
            {
                "n": "Barbell Bicep Curl", 
                "r": "8-10", 
                "t": "ثبت كوعك بجانبك وارفع للصدر.", 
                "b": "زفير بالرفع المتواصل.", 
                "gp": "بطن البايسبس.", 
                "bp": "شد الساعد."
            },
            {
                "n": "Hammer Curl", 
                "r": "10-12", 
                "t": "قبضة محايدة كمطرقة البناء.", 
                "b": "زفير بالرفع.", 
                "gp": "خارجي العضلة.", 
                "bp": "ألم الرسغ."
            }
        ],
        "تراي": [
            {
                "n": "Tricep Pushdown", 
                "r": "12-15", 
                "t": "ادفع وافتح الحبل بالأسفل لأقصى انقباض.", 
                "b": "زفير بالدفع.", 
                "gp": "خلف الذراع بالكامل.", 
                "bp": "مفصل الكوع."
            },
            {
                "n": "Skull Crushers", 
                "r": "8-10", 
                "t": "انزل بالبار خلف رأسك لتمديد العضلة.", 
                "b": "زفير بالدفع العنيف.", 
                "gp": "العمق الطويل.", 
                "bp": "ألم الكوع."
            }
        ],
        "بطن": [
            {
                "n": "Cable Crunches", 
                "r": "10-12", 
                "t": "انحن للأمام بعضلات بطنك حصراً.", 
                "b": "تفريغ هواء تام.", 
                "gp": "البطن العلوي.", 
                "bp": "ألم القطنية."
            },
            {
                "n": "Hanging Leg Raises", 
                "r": "12-15", 
                "t": "ارفع رجليك ولف الحوض للصدر.", 
                "b": "زفير بالرفع المستمر.", 
                "gp": "أسفل البطن.", 
                "bp": "شد الفخذ."
            }
        ],
        "جوانب": [
            {
                "n": "Woodchoppers", 
                "r": "12-15", 
                "t": "دوران جذع مقاوَم لأسفل.", 
                "b": "زفير قوي جداً.", 
                "gp": "الخواصر الجانبية.", 
                "bp": "الظهر المتوسط."
            }
        ],
        "تمرين حر": [
            {
                "n": "Custom Machine", 
                "r": "10-12", 
                "t": "تمرين جهاز مخصص.", 
                "b": "تنفس اعتيادي.", 
                "gp": "العضلة.", 
                "bp": "المفصل."
            }
        ]
    }
    return db

def get_ex_list(muscle):
    """جلب قائمة التمارين بشكل آمن"""
    db = get_bio_db()
    
    if not muscle or muscle == "راحة / غياب": 
        return ["➕ إدخال تمرين جديد (Custom)"]
        
    names = []
    for k, v in db.items():
        if k in muscle:
            for ex in v: 
                names.append(ex.get("n", "مخصص"))
                
    if not names: 
        return ["تمرين مخصص", "➕ إدخال تمرين جديد (Custom)"]
        
    names = list(set(names))
    names.sort()
    names.append("➕ إدخال تمرين جديد (Custom)")
    return names

def get_ex_info(name):
    """جلب تفاصيل التكنيك والألم"""
    db = get_bio_db()
    for grp in db.values():
        for ex in grp:
            if ex.get("n", "") == name: 
                return ex
                
    return {
        "n": name, 
        "r": "10-12", 
        "t": "حافظ على التكنيك السليم وتجنب التأرجح.", 
        "b": "تنفس منتظم مستمر.", 
        "gp": "بطن العضلة المستهدفة.", 
        "bp": "المفاصل والأوتار."
    }

def fetch_past_reps(ex_name):
    """جلب الأوزان السابقة لغرض التطور"""
    df = fetch_data("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past = df[df['Exercise'] == ex_name]
        if not past.empty:
            last_record = past.iloc[-1]
            return last_record.get('Date', 'N/A'), float(last_record.get('Weight', 0)), int(last_record.get('Reps', 10))
            
    return None, 0.0, 0

def smart_reps(ex_name, current_weight):
    """محرك الذكاء الاصطناعي لتقدير العدات (Progressive Overload)"""
    date, lw, lr = fetch_past_reps(ex_name)
    if date:
        if current_weight > lw: 
            return max(lr - 2, 6)
        elif current_weight < lw: 
            return lr + 2
        else: 
            return lr
            
    return 10

# =====================================================================
# 8. COMMERCIAL FOOD DATABASE
# =====================================================================
def get_food_db():
    """قاعدة البيانات الغذائية المفصلة"""
    database = {
        "إيدام دجاج بالبطاطس (صحن وسط)": {"p": 35, "c": 320},
        "إيدام دجاج + رز (150 جرام)": {"p": 40, "c": 580},
        "إيدام لحم بالخضار (بدون رز)": {"p": 45, "c": 450},
        "إيدام لحم + رز": {"p": 50, "c": 710},
        "كبسة دجاج (صدر صافي)": {"p": 45, "c": 650},
        "نصف حبة دجاج شواية (بدون جلد)": {"p": 45, "c": 420},
        "شاورما دجاج (صاروخ عادي)": {"p": 25, "c": 550},
        "تونا بالماء (علبة كاملة)": {"p": 26, "c": 120},
        "سكوب بروتين Whey (بالماء)": {"p": 25, "c": 120},
        "برجر لحم مشوي (مفرد)": {"p": 20, "c": 350},
        "وجبة البيك (مسحب 7 قطع بدون بطاطس)": {"p": 32, "c": 500},
        "3 بيضات مسلوقة كاملة": {"p": 18, "c": 210},
        "شوفان بالحليب الكامل": {"p": 13, "c": 310}
    }
    return database

# =====================================================================
# 9. DYNAMIC TIME ENGINE & WORKOUT CLASSES
# =====================================================================
CLASSES = {
    "موتيف 8": {"burn": 450, "iron": "صدر + تراي", "flow": "الصدر يحتاج تركيز عالي. ابدأ بالبنش برس."},
    "فت كومبات": {"burn": 650, "iron": "أرجل + بطن", "flow": "يوم حرق الدهون! سكوات ثقيل أولاً."},
    "كور اكستريم": {"burn": 350, "iron": "أكتاف + جوانب", "flow": "أكتاف عريضة = خصر أنحف بصرياً. ركز على Overhead Press."},
    "ستيب": {"burn": 450, "iron": "ظهر + باي", "flow": "شد الظهر يمنع التحدب. العب Deadlift و سحب."},
    "اكوا": {"burn": 350, "iron": "حديد شامل", "flow": "تمرين مركب لكل عضلة كبيرة."},
    "بامب فت": {"burn": 400, "iron": "صدر + أكتاف", "flow": "أوزان متوسطة وتكرارات عالية للـ Pump."},
    "بودي ماكس": {"burn": 600, "iron": "أرجل + ظهر", "flow": "أعنف يوم! يستهدف أكبر عضلتين لنسف الكرش."},
    "رادير": {"burn": 300, "iron": "ذراعين", "flow": "العب Supersets باي وتراي لاختصار الوقت."},
    "جي فت": {"burn": 400, "iron": "حديد قوة", "flow": "3-5 عدات بأقصى وزن. راحة 3 دقائق لتجنب إصابة الجهاز العصبي."},
    "فت اتاك": {"burn": 600, "iron": "أرجل + أكتاف", "flow": "تمارين مركبة لرفع النبض."},
    "موبيلتي": {"burn": 200, "iron": "تمرين حر", "flow": "إطالات عميقة للتعافي ومرونة المفاصل."},
    "لا يوجد": {"burn": 0, "iron": "تمرين حر متكامل", "flow": "أنت القائد اليوم. صمم روتينك."},
    "راحة / غياب": {"burn": 0, "iron": "راحة", "flow": "استشفاء سلبي. بناء العضلات يتم الآن."}
}

def get_sched(mode, origin):
    """محرك الجدولة الزمنية بالدقيقة لتفادي الهدم العضلي"""
    now = get_makkah_time()
    eta_m, dist = get_eta(origin)
    
    arr_obj = now + timedelta(minutes=eta_m)
    i_start_obj = arr_obj + timedelta(minutes=10)
    i_end_obj = i_start_obj + timedelta(minutes=75) # 75 mins max for Hypertrophy
    
    return now.strftime("%I:%M %p"), arr_obj.strftime("%I:%M %p"), i_start_obj.strftime("%I:%M %p"), i_end_obj.strftime("%I:%M %p"), arr_obj, dist, eta_m

# =====================================================================
# 10. MAIN APP LOGIC (The Selling Point SaaS UI)
# =====================================================================
def main():
    now = get_makkah_time()
    
    days_ar = {
        "Sunday":"الأحد", "Monday":"الاثنين", "Tuesday":"الثلاثاء", 
        "Wednesday":"الأربعاء", "Thursday":"الخميس", "Friday":"الجمعة", "Saturday":"السبت"
    }
    
    day_ar = days_ar[now.strftime("%A")]
    date_str = now.strftime("%Y-%m-%d")
    
    # --- SaaS Premium Dashboard Header ---
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #1A1C23, #0D1117); padding: 15px 30px; border-radius: 12px; border-bottom: 2px solid #E5B94C; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
        <div style='color: #8B949E; font-size: 14px;'>مكة المكرمة | {day_ar} {date_str} | {now.strftime('%I:%M %p')}</div>
        <div style='display: flex; gap: 20px; align-items: center;'>
            <span style='background: rgba(229, 185, 76, 0.1); padding: 5px 15px; border-radius: 20px; color: #E5B94C; font-weight: bold; font-size: 13px;'>👑 PRO PLAN ACTIVE</span>
            <span style='color: #E8ECEF; font-weight: bold;'>Titan Commercial System V43</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🚀 الميدان والملاحة", "🗓️ المخطط الأسبوعي", "🏋️ السجل الحيوي", "🏥 العيادة الطبية", "📸 عدسة الذكاء (Vision AI)", "🥗 مختبر الماكروز", "🛠️ لوحة الإدارة (SaaS)"])
    t_ops, t_setup, t_log, t_clinic, t_vision, t_fuel, t_sys = tabs

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS (Dynamic)
    # -----------------------------------------------------------------
    with t_ops:
        plan_df = fetch_data("Weekly_Plan")
        s_cls = "موتيف 8"
        
        if not plan_df.empty and 'Date' in plan_df.columns:
            try: 
                match_row = plan_df[plan_df['Date'] == date_str]
                if not match_row.empty:
                    s_cls = match_row.iloc[0].get('Class', 'موتيف 8')
            except Exception: 
                pass
        
        i_tgt = CLASSES.get(s_cls, {}).get("iron", "صدر + تراي")
        mode = st.session_state['attendance_mode']

        if day_ar == "الجمعة" and mode != "IronOnly":
            st.markdown("<div class='titan-card titan-card-center'><h1 style='color:#2EA043; margin:0;'>يوم راحة سلبي 🛑</h1><p style='color:#8B949E; margin-top:10px;'>بناء الأنسجة العضلية يتم الآن.</p></div>", unsafe_allow_html=True)
            if st.button("استثناء: الذهاب للحديد فقط"): 
                st.session_state['attendance_mode'] = "IronOnly"
                st.rerun()
                
        elif s_cls == "راحة / غياب" or mode == "Absent":
            st.markdown("<div class='titan-card'><h2 style='color:#F85149; text-align:center;'>مجدول כـ (راحة) ❌</h2><p style='color:#8B949E; text-align:center;'>تأجيل للتمرين. خفف الكربوهيدرات الليلة.</p></div>", unsafe_allow_html=True)
            if st.button("إلغاء الغياب والتوجه للنادي"): 
                st.session_state['attendance_mode'] = "Full"
                st.rerun()
                
        else:
            c1, c2 = st.columns([2, 1])
            with c2:
                st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 الملاحة الذكية</h3>", unsafe_allow_html=True)
                locs = ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"]
                loc = st.selectbox("الانطلاق:", locs, index=locs.index(st.session_state['selected_origin_loc']))
                st.session_state['selected_origin_loc'] = loc
                
                st.markdown("<hr><h3 style='margin-top:0;'>🕹️ التحكم</h3>", unsafe_allow_html=True)
                if st.button("✅ كلاس + حديد (Full)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "Full"
                    st.rerun()
                if st.button("🏋️ حديد فقط (Iron)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "IronOnly"
                    st.rerun()
                if st.button("🤸 كلاس فقط (Class)", use_container_width=True): 
                    st.session_state['attendance_mode'] = "ClassOnly"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            with c1:
                n_str, a_str, is_str, ie_str, a_obj, d_km, e_min = get_sched(mode, loc)
                c_bn = CLASSES.get(s_cls, {}).get("burn", 0)
                flw = CLASSES.get(s_cls, {}).get("flow", "لا يوجد.")
                
                note = ""
                if a_obj.hour < 18 and mode in ["Full", "ClassOnly"]:
                    note = "<div class='alert-box'>* الكلاس يبدأ 9:00 م. تمرينك مبكر. ستحتاج للعودة للكلاس لاحقاً، أو حول مسارك لحديد فقط.</div>"
                
                if mode == "Full":
                    html = f"""
                    <div class='titan-card'>
                        <h3 style='margin-top:0;'>🗺️ الخطة أ (طاقة قصوى)</h3>
                        <p><span class='data-label'>الحديد:</span> <b style='color:#E5B94C;'>{i_tgt}</b> | <span class='data-label'>الكلاس:</span> <b style='color:#E5B94C;'>{s_cls}</b></p>
                        <p style='color:#8B949E;'>الاستراتيجية: {flw}</p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b> | ⏱️ زحام: <b>{e_min} د</b></p>
                        <h5 style='margin-top:20px;'>الجدول التنفيذي</h5>
                        <p>🔥 {a_str} - {is_str} : إحماء</p>
                        <p>💪 {is_str} - {ie_str} : <b style='color:#F85149;'>صالة الحديد (75 دقيقة لمنع الهدم)</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>الكلاس (حرق ~{c_bn} kcal)</b></p>
                        {note}
                    </div>
                    """
                elif mode == "IronOnly":
                    html = f"""
                    <div class='titan-card' style='border-color: #58A6FF;'>
                        <h3 style='margin-top:0; color:#58A6FF;'>🏋️ مسار الحديد المكثف (الكلاس ملغي)</h3>
                        <p><span class='data-label'>مستهدف اليوم:</span> <b style='color:#E5B94C;'>{i_tgt}</b></p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <p>💪 {is_str} - {(a_obj + timedelta(minutes=90)).strftime('%I:%M %p')} : <b style='color:#F85149;'>حديد مفتوح (العب جولات أكثر)</b></p>
                    </div>
                    """
                elif mode == "ClassOnly":
                    html = f"""
                    <div class='titan-card' style='border-color: #E5B94C;'>
                        <h3 style='margin-top:0; color:#E5B94C;'>🤸 مسار الكارديو (الحديد ملغي)</h3>
                        <p><span class='data-label'>الكلاس:</span> <b style='color:#E5B94C;'>{s_cls}</b></p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>الكلاس (حرق ~{c_bn} kcal)</b></p>
                        {note}
                    </div>
                    """
                st.markdown(html, unsafe_allow_html=True)
            
            # عرض بروتوكول الاستشفاء
            st.markdown(get_recovery_protocol(mode, i_tgt), unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع (مزامنة سحابية)")
        
        plan_df = fetch_data("Weekly_Plan")
        c_pln = {r['Day']: r['Class'] for _, r in plan_df.iterrows()} if not plan_df.empty and 'Day' in plan_df.columns else {}
        
        wd_map = [(d, (makkah_now - timedelta(days=(makkah_now.weekday()+2)%7) + timedelta(days=i)).strftime("%Y-%m-%d")) for i, d in enumerate(["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"])]
        
        with st.form("wp_form"):
            ns = []
            cols = st.columns(3)
            opts = list(CLASSES.keys())
            
            for i, (d, dt) in enumerate(wd_map):
                idx = opts.index(c_pln.get(d, "موتيف 8")) if c_pln.get(d, "موتيف 8") in opts else 0
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E8ECEF; text-align:right;'>{d} <span style='font-size:11px; color:#8B949E;'>({dt})</span></h5>", unsafe_allow_html=True)
                    ch = st.selectbox("", opts, index=idx, key=f"d_{d}", label_visibility="collapsed")
                    ns.append({"Day": d, "Date": dt, "Class": ch, "Muscle": CLASSES.get(ch,{}).get("iron",""), "Status": "مجدول"})
                    
            if st.form_submit_button("✅ اعتماد المخطط في السحابة", use_container_width=True):
                s, m = overwrite_data("Weekly_Plan", pd.DataFrame(ns))
                if s: st.success(m)
                else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 3: BIOMECHANICS & LOGS
    # -----------------------------------------------------------------
    with t_log:
        st.markdown("### 🏋️ الذكاء الحركي وتسجيل الأوزان")
        t_mus = iron_target
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة</h4>", unsafe_allow_html=True)
            if st.button("90 ثانية (بناء)"): 
                pb = st.progress(0)
                for i in range(90):
                    time.sleep(1)
                    pb.progress((i+1)/90)
                st.success("انتهى وقت الراحة. ارجع للبار!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>عضلة اليوم: <span style='color:#E5B94C;'>{t_mus}</span></h4>", unsafe_allow_html=True)
            x_list = get_ex_list(t_mus)
            s_ex = st.selectbox("التمرين:", x_list)
            
            f_ex = st.text_input("اسم التمرين:") if "Custom" in s_ex else s_ex
            f_ex = f_ex if f_ex else "مخصص"
            
            info = get_ex_info(f_ex)
            
            st.markdown(f"""
            <div style='background:#161B22; padding:20px; border-radius:12px; margin-bottom:20px; border-right: 4px solid #E5B94C;'>
                <p><span class='bio-tech'>⚙️ الأداء:</span> {info.get('t', 'تكنيك صحيح.')}</p>
                <p><span class='bio-breath'>🫁 التنفس:</span> {info.get('b', 'تنفس مستمر.')}</p>
                <hr style='border-color:#30363D;'>
                <p><span class='bio-good'>✅ ألم جيد:</span> {info.get('gp', 'العضلة.')}</p>
                <p><span class='bio-bad'>❌ ألم إصابة:</span> {info.get('bp', 'المفصل.')}</p>
                <h5 style='color:#E5B94C; margin:0;'>النطاق: {info.get('r', '10-12')}</h5>
            </div>
            """, unsafe_allow_html=True)
            
            p_date, l_w, l_r = fetch_past_reps(f_ex)
            if p_date:
                st.markdown(f"<p style='color:#8B949E;'>سابقاً ({p_date}): <b>{l_w} KG</b> × {l_r}</p>", unsafe_allow_html=True)
            
            cw, cr = st.columns(2)
            iw = cw.number_input("الوزن (KG)", min_value=0.0, value=float(l_w), step=2.5)
            ir = cr.number_input("العدات (0 = حساب آلي)", min_value=0, value=0)
            
            if st.button("💾 توثيق الجلسة بالسحابة", use_container_width=True):
                fr = smart_reps(f_ex, iw) if ir == 0 else ir
                s, m = push_data("Workout_Logs", {"Date": date_str, "Muscle": t_mus, "Exercise": f_ex, "Weight": iw, "Reps": fr})
                if s: st.success(f"تم تسجيل {f_ex} بـ {fr} عدات.")
                else: st.error(m)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 4: CLINIC
    # -----------------------------------------------------------------
    with t_clinic:
        st.markdown("### 📸 أرشفة التقرير الطبي (InBody)")
        with st.form("ib_f"):
            c_i1, c_i2 = st.columns(2)
            i_dt = st.date_input("التاريخ")
            i_w = c_i1.number_input("الوزن (KG)", value=91.9)
            i_m = c_i2.number_input("العضل (KG)", value=40.0)
            i_f = c_i1.number_input("الدهون %", value=20.0)
            i_v = c_i2.number_input("الحشوية", value=14)
            if st.form_submit_button("حفظ التقرير"):
                s, m = push_data("InBody_Logs", {"Date": i_dt.strftime("%Y-%m-%d"), "Weight": i_w, "Muscle_Mass": i_m, "Fat_Percentage": i_f, "Visceral_Fat": i_v})
                if s: st.success("تم الحفظ.")
                else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 5: PREMIUM VISION AI (ميزة تجارية تباع للعملاء)
    # -----------------------------------------------------------------
    with t_vision:
        st.markdown("### 📸 عدسة تايتان للذكاء الاصطناعي (Premium Vision AI)")
        st.markdown("<p style='color:#8B949E; text-align:right;'>تقوم بقراءة صور الوجبات وتحليل الماكروز عبر محركات الذكاء الاصطناعي العميقة (محاكاة).</p>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='text-align:right;'><span style='background:rgba(229,185,76,0.1); color:#E5B94C; padding:5px 10px; border-radius:5px;'>المتبقي في باقتك: {st.session_state['ai_vision_scans_left']} صور</span></p>", unsafe_allow_html=True)
        
        if st.session_state['ai_vision_scans_left'] > 0:
            up_img = st.file_uploader("التقط أو ارفع صورة وجبتك للتحليل", type=["jpg", "png", "jpeg"])
            if up_img:
                st.image(up_img, use_container_width=True)
                if st.button("🔍 مسح ضوئي واستخراج الماكروز (Scan)", use_container_width=True):
                    with st.spinner("جاري الاتصال بخوادم Vision AI... تحليل الأنسجة والكميات..."):
                        time.sleep(2) 
                        
                        est_prot = 45
                        est_cals = 520
                        
                        st.session_state['daily_protein'] += est_prot
                        st.session_state['daily_cals'] += est_cals
                        st.session_state['ai_vision_scans_left'] -= 1
                        
                        st.markdown(f"""
                        <div class='success-box'>
                            <h4 style='margin:0; color:#2EA043;'>🤖 اكتمل التحليل بنجاح!</h4>
                            <p style='margin-top:5px; color:#E8ECEF;'><b>المكونات المكتشفة:</b> مصدر بروتين حيواني + كربوهيدرات معقدة.</p>
                            <p style='color:#E8ECEF;'><b>البروتين المقدر:</b> {est_prot}g | <b>السعرات المقدرة:</b> {est_cals} kcal</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("لقد استنفدت باقتك المخصصة من مسح الصور لهذا الشهر. قم بترقية اشتراكك.")

    # -----------------------------------------------------------------
    # TAB 6: NUTRITION CALCULATOR
    # -----------------------------------------------------------------
    with t_fuel:
        st.markdown("### 🥗 مختبر التغذية والماكروز")
        cf1, cf2 = st.columns([1, 1.2])
        f_db = get_food_db()
        
        with cf2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>أضف من قاعدة البيانات</h4>", unsafe_allow_html=True)
            sel_f = st.selectbox("الصنف:", list(f_db.keys()))
            q = st.number_input("حصص:", value=1.0)
            if st.button("➕ إضافة"):
                st.session_state['daily_protein'] += int(f_db[sel_f]["p"] * q)
                st.session_state['daily_cals'] += int(f_db[sel_f]["c"] * q)
                st.success("تم الإضافة.")
            
            st.write("إدخال يدوي:")
            cm1, cm2 = st.columns(2)
            mp = cm1.number_input("بروتين", min_value=0)
            mc = cm2.number_input("سعرات", min_value=0)
            if st.button("➕ إضافة يدوي"):
                st.session_state['daily_protein'] += mp
                st.session_state['daily_cals'] += mc
                st.success("تم.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with cf1:
            t_p, t_c = int(91.9 * 2.2), 1900
            st.markdown(f"""
            <div class='titan-card'>
                <h3 style='margin-top:0;'>📊 لوحة الوقود</h3>
                <p>البروتين: <b style='color:#F85149; font-size:24px;'>{st.session_state['daily_protein']} / {t_p} g</b></p>
                <p>السعرات: <b style='color:#E5B94C; font-size:24px;'>{st.session_state['daily_cals']} / {t_c}</b></p>
            </div>
            """, unsafe_allow_html=True)
            with st.form("h_f"):
                slp = st.number_input("نوم:", value=7.5)
                wtr = st.number_input("ماء:", value=3.5)
                if st.form_submit_button("💾 حفظ اليوم بالسحابة"):
                    s, m = push_data("Health_Log", {"Date": date_str, "Sleep": slp, "Water": wtr, "Protein": st.session_state['daily_protein'], "Calories": st.session_state['daily_cals']})
                    if s: 
                        st.success("تم الحفظ في قاعدة البيانات.")
                        st.session_state['daily_protein'] = 0
                        st.session_state['daily_cals'] = 0
                    else: 
                        st.error(m)

    # -----------------------------------------------------------------
    # TAB 7: SAAS DASHBOARD & AUTO-HEAL
    # -----------------------------------------------------------------
    with t_sys:
        st.markdown("### 🛠️ لوحة الإدارة المؤسسية (SaaS Administration)")
        st.info("مخصص لمشرفي النظام لإدارة حالة التطبيق وإصلاح قواعد البيانات.")
        
        c_saas1, c_saas2 = st.columns(2)
        with c_saas1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>محرك الإصلاح الذاتي (Omni-Heal)</h4>", unsafe_allow_html=True)
            if st.button("🔄 فحص وإصلاح قاعدة البيانات", use_container_width=True):
                with st.spinner("جاري المسح..."):
                    for r in auto_heal():
                        st.markdown(f"<div class='{'success-box' if r['status']=='success' else 'alert-box'}'>{r['msg']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_saas2:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>إدارة الذاكرة (Memory Management)</h4>", unsafe_allow_html=True)
            st.warning("يُستخدم إذا واجهت شاشة بيضاء أو تعليق.")
            if st.button("⚠️ إعادة ضبط المصنع (Clear Cache)", use_container_width=True):
                force_program_reset()
                st.success("تم التنظيف. حدث الصفحة.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("#### 📑 استخراج تقارير الأداء (PDF Export)")
        if st.button("📥 استخراج تقرير الأداء الشهري للعميل"):
            with st.spinner("جاري التجهيز..."):
                time.sleep(2)
                st.success("تم تجهيز التقرير! (ميزة تجارية سيتم تفعيلها لاحقاً).")

if __name__ == "__main__":
    main()
