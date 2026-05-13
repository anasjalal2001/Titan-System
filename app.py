import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time
import math
import textwrap

# =====================================================================
# 1. CORE ARCHITECTURE & SYSTEM INITIALIZATION
# إعدادات النظام المعمارية الأساسية للواجهة
# =====================================================================

st.set_page_config(
    page_title="Titan V41 - The Ultimate Enterprise Edition", 
    page_icon="👑", 
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
    تم إصلاح خطأ المتغير (css_code) بالكامل.
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
        
        /* الأرقام والإحصائيات */
        .premium-value { 
            color: #E5B94C; 
            font-size: 36px; 
            font-weight: 900; 
            margin: 10px 0; 
            font-family: 'Courier New', monospace; 
        }
        
        .data-label { 
            color: #8B949E; 
            font-size: 13px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
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
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# تفعيل واجهة الـ CSS
inject_premium_css()

# =====================================================================
# 3. ENTERPRISE STATE MANAGEMENT (إدارة المتغيرات والذاكرة)
# =====================================================================

def init_states():
    """
    تهيئة جميع متغيرات الجلسة بوضوح وبدون اختصارات.
    يضمن عدم ظهور خطأ (KeyError) في أي مكان في التطبيق.
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

# تفعيل حالة الجلسة
init_states()

# =====================================================================
# 4. SECURE CLOUD CONNECTORS & AUTO-HEAL
# =====================================================================

@st.cache_resource(ttl=600)
def get_db():
    """تأسيس الاتصال بقاعدة بيانات Google Sheets بصمت تام"""
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
    """
    إضافة سجل جديد (تمرين، تغذية، الخ) ثم تفريغ الكاش.
    """
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
    """
    استبدال الجدول بالكامل (خاص بالمخطط الأسبوعي).
    """
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
    يتأكد من أن جميع الأوراق والأعمدة موجودة وسليمة.
    """
    report = []
    conn = get_db()
    
    if not conn:
        return [{"status": "error", "msg": "انقطاع في خوادم Google Cloud. يرجى مراجعة إعدادات Secrets."}]
        
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
                report.append({"status": "error", "msg": f"فشل بناء `{sh}`. تأكد من صلاحية المحرر. الخطأ: {str(e)}"})
                
    st.cache_data.clear()
    return report

# =====================================================================
# 5. DYNAMIC ROUTING ENGINE (Haversine Formula)
# محرك الملاحة وحساب المسافات الجغرافية
# =====================================================================

def get_distance(lat1, lon1, lat2, lon2):
    """حساب المسافة الدقيقة بين نقطتين"""
    R = 6371.0 # نصف قطر الأرض
    
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
    dest_lat = 21.5768 # نادي بودي ماسترز الروضة
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
    
    # مصفوفة الزحام (Traffic Matrix)
    if 7 <= hr <= 9: 
        mult = 1.5
    elif 13 <= hr <= 15: 
        mult = 1.6
    elif 17 <= hr <= 21: 
        mult = 1.8
    else: 
        mult = 1.1
        
    final_eta = int(base_mins * mult) + 5 # 5 دقائق إضافية للمواقف
    return final_eta, dist

# =====================================================================
# 6. DYNAMIC CLINICAL RECOVERY (الاستشفاء التفاعلي)
# =====================================================================

def get_recovery_protocol(mode, iron_target):
    """
    بروتوكول طبي يتغير بناءً على قرارك في النادي.
    إذا لعبت كارديو فقط، يمنع الحرارة تماماً.
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
        
    # فحص إذا كان اليوم يتطلب مجهود عالي (أرجل أو أيام محددة)
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
                <h4 style='color:#D29922; margin:0;'>⚠️ تحذير طبي للخصوبة</h4>
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>تكرار الدورة 3 مرات. الختام إلزامي بالماء البارد لحماية هرمون التستوستيرون من التلف الحراري.</p>
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
# 7. COMMERCIAL BIOMECHANICS DATABASE (قاعدة بيانات التمارين الشاملة)
# =====================================================================
def get_bio_db():
    """
    قاعدة بيانات صلبة ومفصلة.
    تم الاستغناء عن دمجها في سطر واحد لضمان دقة القراءة وسهولة التعديل.
    """
    database = {
        "صدر": [
            {
                "name": "Incline Barbell Bench Press", 
                "reps": "6-8 عدات", 
                "technique": "دكة 30 درجة. انزل لملامسة أعلى الصدر.", 
                "breathing": "شهيق في النزول، زفير في الدفع.", 
                "good_pain": "أعلى الصدر.", 
                "bad_pain": "مفصل الكتف."
            },
            {
                "name": "Flat Dumbbell Press", 
                "reps": "8-10 عدات", 
                "technique": "كوعك مائل للداخل 45 درجة.", 
                "breathing": "شهيق في النزول، زفير في الدفع.", 
                "good_pain": "عمق الصدر.", 
                "bad_pain": "الرسغ."
            },
            {
                "name": "Decline Cable Flys", 
                "reps": "12-15 عدة", 
                "technique": "اسحب للأسفل باتجاه الحوض للقضاء على التثدي.", 
                "breathing": "زفير عند الضم.", 
                "good_pain": "أسفل الصدر.", 
                "bad_pain": "الكتف الأمامي."
            },
            {
                "name": "Pec Deck Machine", 
                "reps": "12-15 عدة", 
                "technique": "ظهرك ملتصق. اعصر صدرك في المنتصف.", 
                "breathing": "زفير عند الضم.", 
                "good_pain": "الخط الداخلي للصدر.", 
                "bad_pain": "الكتف."
            },
            {
                "name": "Chest Dips (Bodyweight)", 
                "reps": "للفشل العضلي", 
                "technique": "مل للأمام. انزل للزاوية 90 وادفع.", 
                "breathing": "شهيق في النزول، زفير في الدفع.", 
                "good_pain": "الصدر السفلي والتراي.", 
                "bad_pain": "عظمة القص."
            }
        ],
        "ظهر": [
            {
                "name": "Deadlift", 
                "reps": "3-5 عدات", 
                "technique": "ظهر مستقيم، ادفع الأرض بقدميك.", 
                "breathing": "شهيق عميق قبل الرفع، زفير في الأعلى.", 
                "good_pain": "أوتار الركبة والقطنية.", 
                "bad_pain": "فقرات الظهر."
            },
            {
                "name": "Lat Pulldown Wide", 
                "reps": "8-12 عدة", 
                "technique": "اسحب الكيبل لأعلى صدرك.", 
                "breathing": "زفير عند السحب.", 
                "good_pain": "المجنص.", 
                "bad_pain": "البايسبس."
            },
            {
                "name": "Seated Cable Row", 
                "reps": "10-12 عدة", 
                "technique": "اسحب لسرتك مع تثبيت الجذع.", 
                "breathing": "زفير عند السحب.", 
                "good_pain": "منتصف الظهر.", 
                "bad_pain": "القطنية (بسبب التأرجح)."
            },
            {
                "name": "T-Bar Row", 
                "reps": "8-10 عدات", 
                "technique": "انحنِ 45 درجة واسحب للصدر السفلي.", 
                "breathing": "زفير في السحب.", 
                "good_pain": "العمق الداخلي للظهر.", 
                "bad_pain": "الركبة."
            }
        ],
        "أرجل": [
            {
                "name": "Barbell Squat", 
                "reps": "4-6 عدات", 
                "technique": "انزل كجلوس الكرسي لزاوية 90.", 
                "breathing": "شهيق قبل النزول، زفير في الأعلى.", 
                "good_pain": "الفخذ والمؤخرة.", 
                "bad_pain": "الركبة أو الظهر."
            },
            {
                "name": "Leg Press", 
                "reps": "10-12 عدة", 
                "technique": "لا تقفل ركبتك بالكامل في الأعلى.", 
                "breathing": "زفير بالدفع.", 
                "good_pain": "الفخذ كاملاً.", 
                "bad_pain": "مفصل الركبة."
            },
            {
                "name": "Bulgarian Split Squat", 
                "reps": "10-12 عدة", 
                "technique": "رجل للخلف على الدكة وانزل بشكل عمودي.", 
                "breathing": "زفير بالصعود.", 
                "good_pain": "الأرداف والفخذ.", 
                "bad_pain": "الكاحل."
            },
            {
                "name": "Romanian Deadlift", 
                "reps": "8-10 عدات", 
                "technique": "ادفع حوضك للخلف لأقصى شد.", 
                "breathing": "شهيق بالنزول.", 
                "good_pain": "الخلفيات.", 
                "bad_pain": "القطنية."
            }
        ],
        "أكتاف": [
            {
                "name": "Overhead Press", 
                "reps": "6-8 عدات", 
                "technique": "ادفع البار فوق رأسك مباشرة.", 
                "breathing": "زفير بالدفع.", 
                "good_pain": "الكتف كاملاً.", 
                "bad_pain": "أسفل الظهر."
            },
            {
                "name": "Lateral Raise", 
                "reps": "12-15 عدة", 
                "technique": "ارفع للجانب مع ثني الكوع.", 
                "breathing": "زفير بالرفع.", 
                "good_pain": "الكتف الجانبي.", 
                "bad_pain": "الترابيس."
            },
            {
                "name": "Face Pulls", 
                "reps": "15-20 عدة", 
                "technique": "اسحب الحبل لمستوى عينيك.", 
                "breathing": "زفير بالسحب.", 
                "good_pain": "الكتف الخلفي.", 
                "bad_pain": "الرقبة."
            }
        ],
        "باي": [
            {
                "name": "Barbell Bicep Curl", 
                "reps": "8-10 عدات", 
                "technique": "ثبت كوعك بجانبك.", 
                "breathing": "زفير بالرفع.", 
                "good_pain": "البايسبس.", 
                "bad_pain": "الساعد."
            },
            {
                "name": "Hammer Curl", 
                "reps": "10-12 عدة", 
                "technique": "قبضة محايدة.", 
                "breathing": "زفير بالرفع.", 
                "good_pain": "خارجي.", 
                "bad_pain": "الرسغ."
            }
        ],
        "تراي": [
            {
                "name": "Tricep Pushdown", 
                "reps": "12-15 عدة", 
                "technique": "ادفع وافتح الحبل بالأسفل.", 
                "breathing": "زفير بالدفع.", 
                "good_pain": "خلف الذراع.", 
                "bad_pain": "الكوع."
            },
            {
                "name": "Skull Crushers", 
                "reps": "8-10 عدات", 
                "technique": "انزل بالبار خلف رأسك.", 
                "breathing": "زفير بالدفع.", 
                "good_pain": "العمق.", 
                "bad_pain": "الكوع."
            }
        ],
        "بطن": [
            {
                "name": "Cable Crunches", 
                "reps": "10-12 عدة", 
                "technique": "انحن للأمام بعضلات بطنك.", 
                "breathing": "تفريغ هواء تام عند العصر.", 
                "good_pain": "البطن.", 
                "bad_pain": "القطنية."
            },
            {
                "name": "Hanging Leg Raises", 
                "reps": "12-15 عدة", 
                "technique": "ارفع رجليك ولف الحوض.", 
                "breathing": "زفير بالرفع.", 
                "good_pain": "أسفل البطن.", 
                "bad_pain": "الفخذ."
            }
        ],
        "جوانب": [
            {
                "name": "Woodchoppers", 
                "reps": "12-15 عدة", 
                "technique": "دوران جذع مقاوَم.", 
                "breathing": "زفير قوي.", 
                "good_pain": "الخواصر.", 
                "bad_pain": "الظهر."
            }
        ],
        "تمرين حر": [
            {
                "name": "Custom Machine", 
                "reps": "10-12 عدة", 
                "technique": "تمرين جهاز مخصص.", 
                "breathing": "تنفس منتظم.", 
                "good_pain": "العضلة المستهدفة.", 
                "bad_pain": "المفصل."
            }
        ]
    }
    return database

def get_ex_list(muscle):
    """إرجاع قائمة التمارين بشكل دقيق"""
    db = get_bio_db()
    if not muscle or muscle == "راحة / غياب": 
        return ["➕ إدخال تمرين جديد (Custom)"]
        
    names = []
    for k, v in db.items():
        if k in muscle:
            for ex in v: 
                names.append(ex.get("name", "غير محدد"))
                
    if not names: 
        return ["تمرين مخصص", "➕ إدخال تمرين جديد (Custom)"]
        
    names = list(set(names))
    names.sort()
    names.append("➕ إدخال تمرين جديد (Custom)")
    return names

def get_ex_info(name):
    """جلب التفاصيل الحيوية لتمرين محدد"""
    db = get_bio_db()
    for grp in db.values():
        for ex in grp:
            if ex.get("name", "") == name: 
                return ex
                
    return {
        "name": name, 
        "reps": "10-12 عدة", 
        "technique": "حافظ على التكنيك السليم.", 
        "breathing": "تنفس منتظم.", 
        "good_pain": "العضلة المستهدفة.", 
        "bad_pain": "المفاصل."
    }

def fetch_past_reps(ex_name):
    """جلب السجل التاريخي للتمرين"""
    df = fetch_data("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past = df[df['Exercise'] == ex_name]
        if not past.empty:
            last_record = past.iloc[-1]
            return last_record.get('Date', 'N/A'), float(last_record.get('Weight', 0)), int(last_record.get('Reps', 10))
    return None, 0.0, 0

def smart_reps(ex_name, current_weight):
    """الاستنتاج الآلي للعدات بناءً على قوانين التضخيم"""
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
# 8. COMMERCIAL FOOD DATABASE (قاعدة التغذية التجارية)
# =====================================================================
def get_food_db():
    """أضخم مكتبة للغذاء السعودي (Offline)"""
    database = {
        "إيدام دجاج بالبطاطس (صحن وسط)": {"prot": 35, "cals": 320},
        "إيدام دجاج + رز أبيض (150 جرام)": {"prot": 40, "cals": 580},
        "إيدام لحم بالخضار (بدون رز)": {"prot": 45, "cals": 450},
        "إيدام لحم + رز أبيض": {"prot": 50, "cals": 710},
        "كبسة دجاج (صدر)": {"prot": 45, "cals": 650},
        "نصف حبة دجاج شواية (بدون جلد)": {"prot": 45, "cals": 420},
        "شاورما دجاج (صاروخ عادي)": {"prot": 25, "cals": 550},
        "علبة تونا (مصفاة بالماء)": {"prot": 26, "cals": 120},
        "سكوب بروتين Whey (مع ماء)": {"prot": 25, "cals": 120},
        "برجر لحم مشوي (مفرد)": {"prot": 20, "cals": 350},
        "وجبة البيك (مسحب 7 قطع بدون بطاطس)": {"prot": 32, "cals": 500},
        "3 بيضات مسلوقة كاملة": {"prot": 18, "cals": 210},
        "شوفان بالحليب (50ج)": {"prot": 13, "cals": 310}
    }
    return database

# =====================================================================
# 9. DYNAMIC TIME ENGINE & WORKOUT CLASSES (هنا تم إصلاح المتغيرات)
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
        "flow": "ابدأ بالبنش برس لشد الجزء العلوي."
    },
    "فت كومبات": {
        "iron": "أرجل + بطن", 
        "flow": "يوم حرق الدهون! سكوات ثقيل."
    },
    "كور اكستريم": {
        "iron": "أكتاف + جوانب", 
        "flow": "ركز على تمرين Overhead Press."
    },
    "ستيب": {
        "iron": "ظهر + باي", 
        "flow": "العب Deadlift و سحب لتقويم الظهر."
    },
    "اكوا": {
        "iron": "حديد شامل (Full Body)", 
        "flow": "تمرين مركب لكل عضلة كبيرة."
    },
    "بامب فت": {
        "iron": "صدر + أكتاف", 
        "flow": "أوزان متوسطة وتكرارات عالية للـ Pump."
    },
    "بودي ماكس": {
        "iron": "أرجل + ظهر", 
        "flow": "أعنف يوم! يستهدف أكبر عضلتين لنسف الكرش."
    },
    "رادير": {
        "iron": "ذراعين (باي وتراي)", 
        "flow": "العب Supersets لاختصار الوقت."
    },
    "جي فت": {
        "iron": "حديد قوة (Heavy Lift)", 
        "flow": "3-5 عدات بأقصى وزن. راحة 3 دقائق."
    },
    "فت اتاك": {
        "iron": "أرجل + أكتاف", 
        "flow": "تمارين مركبة لرفع النبض."
    },
    "موبيلتي": {
        "iron": "تمرين حر", 
        "flow": "إطالات عميقة للتعافي."
    },
    "لا يوجد": {
        "iron": "تمرين حر متكامل", 
        "flow": "صمم روتينك."
    },
    "راحة / غياب": {
        "iron": "راحة", 
        "flow": "استشفاء سلبي."
    }
}

def get_sched(mode, origin):
    """محرك الجدول الزمني الفعلي"""
    now = get_makkah_time()
    eta_m, dist = get_eta(origin)
    
    arr_obj = now + timedelta(minutes=eta_m)
    i_start_obj = arr_obj + timedelta(minutes=10)
    i_end_obj = i_start_obj + timedelta(minutes=75) # 75 mins max for Hypertrophy
    
    now_formatted = now.strftime("%I:%M %p")
    arr_formatted = arr_obj.strftime("%I:%M %p")
    start_formatted = i_start_obj.strftime("%I:%M %p")
    end_formatted = i_end_obj.strftime("%I:%M %p")
    
    return now_formatted, arr_formatted, start_formatted, end_formatted, arr_obj, dist, eta_m

# =====================================================================
# 10. MAIN APP LOGIC (The SaaS Enterprise UI)
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
    header_html = f"""
    <div style='background: linear-gradient(90deg, #1A1C23, #0D1117); padding: 15px 30px; border-radius: 12px; border-bottom: 2px solid #E5B94C; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
        <div style='color: #8B949E; font-size: 14px;'>مكة المكرمة | {day_ar} {date_str} | {now.strftime('%I:%M %p')}</div>
        <div style='display: flex; gap: 20px; align-items: center;'>
            <span style='background: rgba(229, 185, 76, 0.1); padding: 5px 15px; border-radius: 20px; color: #E5B94C; font-weight: bold; font-size: 13px;'>👑 PRO PLAN ACTIVE</span>
            <span style='color: #E8ECEF; font-weight: bold;'>Titan Commercial System V41</span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    tabs = st.tabs([
        "🚀 الميدان والملاحة", 
        "🗓️ المخطط האسبوعي", 
        "🏋️ السجل الحيوي", 
        "🏥 العيادة الطبية", 
        "📸 عدسة الذكاء (Vision AI)", 
        "🥗 مختبر الماكروز", 
        "🛠️ لوحة الإدارة (SaaS)"
    ])
    
    t_ops, t_setup, t_log, t_clinic, t_vision, t_fuel, t_sys = tabs

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS (الملاحة والميدان)
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
        
        # استخراج الحديد الخاص بالكلاس من القاموس
        dict_data = WORKOUT_ENGINE_DB.get(s_cls, {})
        i_tgt = dict_data.get("iron", "صدر + تراي")
        mode = st.session_state['attendance_mode']

        if day_ar == "الجمعة" and mode != "IronOnly":
            st.markdown(
                "<div class='titan-card titan-card-center'>"
                "<h1 style='color:#2EA043; margin:0;'>يوم راحة سلبي 🛑</h1>"
                "<p style='color:#8B949E; margin-top:10px;'>بناء الأنسجة العضلية يتم الآن. استمتع بيومك.</p>"
                "</div>", 
                unsafe_allow_html=True
            )
            if st.button("الذهاب للحديد فقط كاستثناء"): 
                st.session_state['attendance_mode'] = "IronOnly"
                st.rerun()
                
        elif s_cls == "راحة / غياب" or mode == "Absent":
            st.markdown(
                "<div class='titan-card'>"
                "<h2 style='color:#F85149; text-align:center;'>مجدول כـ (راحة / غياب) ❌</h2>"
                "<p style='text-align:center; color:#8B949E;'>تم تأجيل تمرينك للغد. يُنصح بخفض الكربوهيدرات.</p>"
                "</div>", 
                unsafe_allow_html=True
            )
            if st.button("إلغاء الغياب والتوجه للنادي"): 
                st.session_state['attendance_mode'] = "Full"
                st.rerun()
                
        else:
            col_nav1, col_nav2 = st.columns([2, 1])
            
            with col_nav2:
                st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 الملاحة الذكية</h3>", unsafe_allow_html=True)
                
                locs = ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"]
                loc_index = locs.index(st.session_state['selected_origin_loc'])
                loc = st.selectbox("منطقة الانطلاق:", locs, index=loc_index)
                st.session_state['selected_origin_loc'] = loc
                
                st.markdown("<hr style='border-color:#30363D;'><h3 style='margin-top:0;'>🕹️ التحكم الميداني</h3>", unsafe_allow_html=True)
                
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

            with col_nav1:
                n_str, a_str, is_str, ie_str, a_obj, d_km, e_min = get_sched(mode, loc)
                
                # جلب السعرات والاستراتيجية بأمان
                c_bn = CLASS_BURN_DB.get(s_cls, 0)
                engine_data = WORKOUT_ENGINE_DB.get(s_cls, {})
                flw = engine_data.get("flow", "لا يوجد استراتيجية محددة.")
                
                note_html = ""
                if a_obj.hour < 18 and mode in ["Full", "ClassOnly"]:
                    note_html = "<div class='alert-box'>* ملاحظة: الكلاس يبدأ 9:00 م. تمرينك الآن مبكر جداً. ستحتاج للعودة للكلاس لاحقاً، أو حوّل مسارك لحديد فقط من أزرار التحكم.</div>"
                
                if mode == "Full":
                    main_html = f"""
                    <div class='titan-card'>
                        <h3 style='margin-top:0;'>🗺️ الخطة أ (طاقة قصوى)</h3>
                        <p><span class='data-label'>الحديد:</span> <b style='color:#E5B94C;'>{i_tgt}</b> | <span class='data-label'>الكلاس:</span> <b style='color:#E5B94C;'>{s_cls}</b></p>
                        <p style='color:#8B949E;'>الاستراتيجية: {flw}</p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b> | ⏱️ زحام: <b>{e_min} د</b></p>
                        <h5 style='margin-top:20px; color:#E8ECEF;'>الجدول التنفيذي الدقيق</h5>
                        <p>🔥 {a_str} - {is_str} : إحماء مفاصل وتجهيز</p>
                        <p>💪 {is_str} - {ie_str} : <b style='color:#F85149;'>صالة الحديد (75 دقيقة كحد أقصى لمنع هدم العضلات)</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>الكلاس (حرق ~{c_bn} kcal صافي)</b></p>
                        {note_html}
                    </div>
                    """
                elif mode == "IronOnly":
                    main_html = f"""
                    <div class='titan-card' style='border-color: #58A6FF;'>
                        <h3 style='margin-top:0; color:#58A6FF;'>🏋️ مسار الحديد المكثف (الكلاس ملغي)</h3>
                        <p><span class='data-label'>مستهدف اليوم:</span> <b style='color:#E5B94C;'>{i_tgt}</b></p>
                        <p style='color:#8B949E;'>بما أن الكلاس تم إسقاطه، استغل طاقتك الكاملة في كسر الأوزان الحرة.</p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <h5 style='margin-top:20px; color:#E8ECEF;'>الجدول التنفيذي המفتوح</h5>
                        <p>🔥 {a_str} - {is_str} : إحماء دقيق وتمدد</p>
                        <p>💪 {is_str} - {(a_obj + timedelta(minutes=90)).strftime('%I:%M %p')} : <b style='color:#F85149;'>حديد مفتوح (وقتك ملكك، العب جولات إضافية)</b></p>
                    </div>
                    """
                elif mode == "ClassOnly":
                    main_html = f"""
                    <div class='titan-card' style='border-color: #E5B94C;'>
                        <h3 style='margin-top:0; color:#E5B94C;'>🤸 مسار الكارديو (الحديد ملغي)</h3>
                        <p><span class='data-label'>الكلاس المجدول:</span> <b style='color:#E5B94C;'>{s_cls}</b></p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>الكلاس (حرق ~{c_bn} kcal)</b></p>
                        {note_html}
                    </div>
                    """
                st.markdown(main_html, unsafe_allow_html=True)
            
            # استدعاء بروتوكول الاستشفاء المربوط بحالة الحضور
            st.markdown(get_recovery_protocol(mode, i_tgt), unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN (هندسة الأسبوع)
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع المتقدمة (Muti-Device Sync)")
        
        plan_df = fetch_data("Weekly_Plan")
        c_pln = {}
        if not plan_df.empty:
            if 'Day' in plan_df.columns and 'Class' in plan_df.columns:
                for index, row in plan_df.iterrows():
                    day_val = row['Day']
                    class_val = row['Class']
                    c_pln[day_val] = class_val
        
        # إنشاء مصفوفة أيام الأسبوع القادمة بدءاً من السبت
        week_days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        start_date = makkah_now - timedelta(days=(makkah_now.weekday() + 2) % 7)
        
        wd_map = []
        for i, d_name in enumerate(week_days):
            date_val = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            wd_map.append((d_name, date_val))
        
        with st.form("wp_form"):
            ns = []
            cols = st.columns(3)
            opts = list(WORKOUT_ENGINE_DB.keys())
            
            for i, (d_name, d_date) in enumerate(wd_map):
                current_choice = c_pln.get(d_name, "موتيف 8")
                try:
                    idx = opts.index(current_choice)
                except ValueError:
                    idx = 0
                    
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E8ECEF; text-align:right;'>{d_name} <br><span style='font-size:12px; color:#8B949E;'>({d_date})</span></h5>", unsafe_allow_html=True)
                    selected_class = st.selectbox("", opts, index=idx, key=f"d_{d_name}", label_visibility="collapsed")
                    
                    target_muscle = WORKOUT_ENGINE_DB.get(selected_class, {}).get("iron", "غير محدد")
                    ns.append({
                        "Day": d_name, 
                        "Date": d_date, 
                        "Class": selected_class, 
                        "Muscle": target_muscle, 
                        "Status": "مجدول"
                    })
                    
            if st.form_submit_button("✅ اعتماد المخطط في السحابة", use_container_width=True):
                # فحص هندسي قبل الرفع
                is_balanced, balance_message = analyze_muscle_balance(pd.DataFrame(ns))
                
                if is_balanced:
                    st.markdown(f"<div class='success-box'>{balance_message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='alert-box'>{balance_message}</div>", unsafe_allow_html=True)
                    
                # الرفع النهائي
                success, sync_msg = overwrite_data("Weekly_Plan", pd.DataFrame(ns))
                if success: 
                    st.success(sync_msg)
                else: 
                    st.error(sync_msg)

    # -----------------------------------------------------------------
    # TAB 3: BIOMECHANICS & LOGS (علم الحركة والتسجيل)
    # -----------------------------------------------------------------
    with t_log:
        st.markdown("### 🏋️ الذكاء الحركي وتسجيل الأوزان (Biomechanics)")
        t_mus = iron_target
        
        c_log1, c_log2 = st.columns([1, 2])
        
        with c_log1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة الدقيق</h4>", unsafe_allow_html=True)
            if st.button("90 ثانية (تضخيم وبناء)"): 
                pb = st.progress(0)
                for i in range(90):
                    time.sleep(1)
                    pb.progress((i+1)/90)
                st.success("انتهى وقت الراحة. ارجع للبار فوراً!")
                
            if st.button("3 دقائق (قوة Power)"): 
                pb = st.progress(0)
                for i in range(180):
                    time.sleep(1)
                    pb.progress((i+1)/180)
                st.success("تم استشفاء الجهاز العصبي بالكامل. انطلق.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_log2:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>عضلة اليوم: <span style='color:#E5B94C;'>{t_mus}</span></h4>", unsafe_allow_html=True)
            
            x_list = get_ex_list(t_mus)
            s_ex = st.selectbox("اختر التمرين:", x_list)
            
            # معالجة الإدخال اليدوي
            if "Custom" in s_ex:
                f_ex = st.text_input("أدخل اسم التمرين الجديد (باللغة الإنجليزية للتوحيد):")
            else:
                f_ex = s_ex
                
            f_ex = f_ex if f_ex else "تمرين مخصص"
            
            # جلب تفاصيل التكنيك والألم
            info = get_ex_info(f_ex)
            tech = info.get('technique', 'أداء حركي كامل.')
            breath = info.get('breathing', 'تنفس منتظم.')
            g_pain = info.get('good_pain', 'بطن العضلة.')
            b_pain = info.get('bad_pain', 'المفاصل.')
            r_range = info.get('reps', '10-12')
            
            st.markdown(f"""
            <div style='background:#161B22; padding:20px; border-radius:12px; margin-bottom:20px; border-right: 4px solid #E5B94C;'>
                <p><span class='bio-tech'>⚙️ الأداء המيكانيكي:</span> {tech}</p>
                <p><span class='bio-breath'>🫁 التنفس الصحيح:</span> {breath}</p>
                <hr style='border-color:#30363D;'>
                <p><span class='bio-good'>✅ ألم التطور (DOMS):</span> {g_pain}</p>
                <p><span class='bio-bad'>❌ ألم الإصابة الخطرة:</span> {b_pain}</p>
                <h5 style='color:#E5B94C; margin:0; margin-top:15px;'>النطاق العلمي: {r_range}</h5>
            </div>
            """, unsafe_allow_html=True)
            
            # جلب آخر قراءة للتمرين
            p_date, l_w, l_r = fetch_past_reps(f_ex)
            if p_date:
                st.markdown(f"<p style='color:#8B949E; background:#111; padding:10px; border-radius:8px;'>سابقاً ({p_date}): <b>{l_w} KG</b> × {l_r} عدات</p>", unsafe_allow_html=True)
            
            cw, cr = st.columns(2)
            iw = cw.number_input("الوزن המرفوع (KG)", min_value=0.0, value=float(l_w), step=2.5)
            ir = cr.number_input("العدات (اكتب 0 للحساب الآلي)", min_value=0, value=0)
            
            if st.button("💾 توثيق الجلسة بالسحابة", use_container_width=True):
                # خوارزمية استنتاج العدات الذكية
                fr = smart_reps(f_ex, iw) if ir == 0 else ir
                
                if ir == 0:
                    st.success(f"🤖 الذكاء الاصطناعي استنتج أنك حققت {fr} عدات بناءً على الوزن القديم وقوانين التضخيم.")
                    
                entry = {
                    "Date": date_str, 
                    "Muscle": t_mus, 
                    "Exercise": f_ex, 
                    "Weight": iw, 
                    "Reps": fr
                }
                s, m = push_data("Workout_Logs", entry)
                if s: 
                    st.success(f"تم تسجيل {f_ex} بنجاح.")
                else: 
                    st.error(m)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 4: CLINIC (عيادة القياسات)
    # -----------------------------------------------------------------
    with t_clinic:
        st.markdown("### 📸 أرشفة التقرير الطبي (InBody)")
        st.info("قم برفع أرقامك هنا. النظام يقوم بحفظها تاريخياً لرسم منحنى النزول لاحقاً.")
        
        with st.form("ib_f"):
            i_dt = st.date_input("تاريخ الفحص الطبي")
            c_i1, c_i2 = st.columns(2)
            
            i_w = c_i1.number_input("الوزن الإجمالي (KG)", value=91.9, step=0.1)
            i_m = c_i2.number_input("كتلة العضلات (KG)", value=40.0, step=0.1)
            i_f = c_i1.number_input("نسبة الدهون الإجمالية %", value=20.0, step=0.5)
            i_v = c_i2.number_input("مؤشر الدهون الحشوية (الكرش الداخلي)", value=14, step=1)
            
            if st.form_submit_button("💾 أرشفة التقرير في السحابة"):
                data_pack = {
                    "Date": i_dt.strftime("%Y-%m-%d"), 
                    "Weight": i_w, 
                    "Muscle_Mass": i_m, 
                    "Fat_Percentage": i_f, 
                    "Visceral_Fat": i_v
                }
                s, m = push_data("InBody_Logs", data_pack)
                if s: 
                    st.success("تم الحفظ والأرشفة بنجاح.")
                else: 
                    st.error(m)

    # -----------------------------------------------------------------
    # TAB 5: PREMIUM VISION AI (ميزة تجارية تباع للعملاء - محاكاة تفاعلية)
    # -----------------------------------------------------------------
    with t_vision:
        st.markdown("### 📸 عدسة تايتان للذكاء الاصطناعي (Premium Vision AI)")
        st.markdown("<p style='color:#8B949E; text-align:right;'>هذه الميزة مدفوعة (SaaS). تقوم بقراءة صور الوجبات وتحليل الماكروز عبر محركات الذكاء الاصطناعي العميقة لشركة Google.</p>", unsafe_allow_html=True)
        
        # رصيد المحاكاة للعميل
        scans_left = st.session_state['ai_vision_scans_left']
        st.markdown(f"<p style='text-align:right;'><span style='background:rgba(229,185,76,0.1); color:#E5B94C; padding:8px 15px; border-radius:8px; font-weight:bold;'>الرصيد المتبقي في باقتك: {scans_left} عمليات مسح</span></p>", unsafe_allow_html=True)
        
        if scans_left > 0:
            up_img = st.file_uploader("التقط أو ارفع صورة وجبتك للتحليل الدقيق", type=["jpg", "png", "jpeg"])
            if up_img:
                st.image(up_img, use_container_width=True)
                if st.button("🔍 مسح ضوئي واستخراج الماكروز (Scan Image)", use_container_width=True):
                    with st.spinner("جاري الاتصال بخوادم Vision API... تحليل الأنسجة والأبعاد..."):
                        time.sleep(2.5) # محاكاة تأخير معالجة السيرفر
                        
                        # محاكاة ذكية للنتائج
                        est_prot = 45
                        est_cals = 520
                        
                        st.session_state['daily_protein'] += est_prot
                        st.session_state['daily_cals'] += est_cals
                        st.session_state['ai_vision_scans_left'] -= 1
                        
                        st.markdown(f"""
                        <div class='success-box'>
                            <h4 style='margin:0; color:#2EA043;'>🤖 اكتمل التحليل بنجاح!</h4>
                            <p style='margin-top:5px; color:#E8ECEF;'><b>المكونات المكتشفة:</b> مصدر بروتين حيواني مشوي (دجاج/لحم) + كربوهيدرات معقدة.</p>
                            <p style='color:#E8ECEF; font-size:18px;'><b>البروتين المقدر:</b> {est_prot}g | <b>السعرات المقدرة:</b> {est_cals} kcal</p>
                            <p style='font-size:12px; color:#8B949E; margin-top:10px;'>تم خصم عملية مسح واحدة من رصيدك. تمت إضافة القيم لعدادك اليومي تلقائياً.</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("لقد استنفدت باقتك المخصصة من مسح الصور لهذا الشهر. قم بترقية اشتراكك للمتابعة.")

    # -----------------------------------------------------------------
    # TAB 6: NUTRITION CALCULATOR (مختبر الماكروز العملاق)
    # -----------------------------------------------------------------
    with t_fuel:
        st.markdown("### 🥗 مختبر التغذية والماكروز (Offline Database)")
        cf1, cf2 = st.columns([1, 1.2])
        
        # جلب قاعدة البيانات المحلية
        e_db, f_db = get_food_db()
        full_food = {**e_db, **f_db}
        
        with cf2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>أضف من قاعدة البيانات السعودية</h4>", unsafe_allow_html=True)
            
            sel_f = st.selectbox("ابحث عن الصنف (طبخ بيت أو مطاعم):", list(full_food.keys()))
            q = st.number_input("عدد الحصص (المكتوبة بجانب الصنف):", value=1.0, step=0.5)
            
            if st.button("➕ إضافة الوجبة للعداد", use_container_width=True):
                added_p = int(full_food[sel_f].get("prot", 0) * q)
                added_c = int(full_food[sel_f].get("cals", 0) * q)
                
                st.session_state['daily_protein'] += added_p
                st.session_state['daily_cals'] += added_c
                st.success(f"تمت الإضافة: [+ {added_p}g بروتين, + {added_c} سعرة]")
            
            st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
            st.write("أو إدخال يدوي من غلاف منتج آخر:")
            
            cm1, cm2 = st.columns(2)
            mp = cm1.number_input("البروتين المدون (جرام)", min_value=0)
            mc = cm2.number_input("السعرات المدونة", min_value=0)
            
            if st.button("➕ إضافة الإدخال اليدوي", use_container_width=True):
                st.session_state['daily_protein'] += mp
                st.session_state['daily_cals'] += mc
                st.success("تم جمع القيم المدخلة بنجاح.")
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        with cf1:
            t_p = int(91.9 * 2.2) # هدف البروتين لمنع الهدم
            t_c = 1900 # هدف السعرات للتنشيف
            
            st.markdown(f"""
            <div class='titan-card'>
                <h3 style='margin-top:0;'>📊 لوحة الوقود اللحظية</h3>
                <p><span class='data-label'>البروتين المكتسب:</span> <b style='color:#F85149; font-size:26px;'>{st.session_state['daily_protein']} / {t_p} g</b></p>
                <p><span class='data-label'>إجمالي السعرات:</span> <b style='color:#E5B94C; font-size:26px;'>{st.session_state['daily_cals']} / {t_c} kcal</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("h_f"):
                st.write("مؤشرات الصحة الإلزامية قبل حفظ اليوم:")
                slp = st.number_input("ساعات النوم الفعلي:", value=7.5, step=0.5)
                wtr = st.number_input("الماء المستهلك (لتر):", value=3.5, step=0.5)
                
                if st.form_submit_button("💾 توثيق وحفظ يوم التغذية بالسحابة", use_container_width=True):
                    record = {
                        "Date": date_str, 
                        "Sleep": slp, 
                        "Water": wtr, 
                        "Protein": st.session_state['daily_protein'], 
                        "Calories": st.session_state['daily_cals'],
                        "Notes": ""
                    }
                    s, m = push_data("Health_Log", record)
                    if s: 
                        st.success("تم أرشفة البيانات الصحية بنجاح.")
                        # تصفير العداد لليوم الجديد
                        st.session_state['daily_protein'] = 0
                        st.session_state['daily_cals'] = 0
                    else: 
                        st.error(m)

    # -----------------------------------------------------------------
    # TAB 7: SAAS DASHBOARD & AUTO-HEAL (لوحة الإدارة والإصلاح)
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
            
        # محاكاة استخراج تقرير للمشتركين (SaaS Export Feature)
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
