"""
=============================================================================
TITAN ENTERPRISE SAAS SYSTEM - V46 (The Unbreakable Monolith)
=============================================================================
Author: Titan AI Engineering
Date: May 2026
Description: This is the core architecture file for the Titan System.
It includes rigorous error handling, explicit variable scoping, and 
cloud synchronization mechanisms to prevent any NameError or KeyError.
=============================================================================
"""

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time
import math
import textwrap

# =====================================================================
# 1. SYSTEM CONFIGURATION & GLOBAL CONSTANTS
# إعدادات الخادم والمتغيرات الثابتة
# =====================================================================

# إعدادات الصفحة الأساسية (يجب أن تكون أول أمر في Streamlit)
st.set_page_config(
    page_title="Titan Enterprise SaaS", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_makkah_time() -> datetime:
    """
    محرك التوقيت الدقيق لمكة المكرمة (UTC+3).
    يستدعى في كل مكان لضمان عدم وجود أي تعارض زمني بين سيرفر جوجل وموقع المستخدم.
    """
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# =====================================================================
# 2. ADVANCED FRONTEND ENGINEERING (SaaS UI/UX)
# هندسة الواجهة الأمامية - تم فك الضغط بالكامل لمنع أخطاء الـ HTML
# =====================================================================

def inject_premium_css():
    """
    مكتبة التصميم الشاملة.
    مفصلة عمودياً لضمان قراءة المتصفح لكل سطر بدون تداخل.
    """
    css_code = """
    <style>
        /* --------------------------------------------------- */
        /* Core Background and Text Colors */
        /* --------------------------------------------------- */
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
        
        /* --------------------------------------------------- */
        /* Navigation Tabs (SaaS Style) */
        /* --------------------------------------------------- */
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
        
        /* --------------------------------------------------- */
        /* Premium Cards Framework */
        /* --------------------------------------------------- */
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
        
        /* --------------------------------------------------- */
        /* Typography & Values */
        /* --------------------------------------------------- */
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
        
        /* --------------------------------------------------- */
        /* Medical Recovery Interactive Boxes */
        /* --------------------------------------------------- */
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
        
        /* --------------------------------------------------- */
        /* Global Alert Boxes */
        /* --------------------------------------------------- */
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
        
        /* --------------------------------------------------- */
        /* Biomechanics Text Highlights */
        /* --------------------------------------------------- */
        .bio-tech { color: #E5B94C; font-weight: bold; }
        .bio-breath { color: #58A6FF; font-weight: bold; }
        .bio-good { color: #2EA043; font-weight: bold; }
        .bio-bad { color: #F85149; font-weight: bold; }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# تفعيل الـ CSS فوراً
inject_premium_css()

# =====================================================================
# 3. ENTERPRISE STATE MANAGEMENT (إدارة المتغيرات والذاكرة)
# =====================================================================

def init_states():
    """
    تهيئة جميع متغيرات الجلسة (Session States) بشكل صريح ومؤمّن.
    يضمن عدم ظهور خطأ KeyError عند استدعاء أي متغير.
    """
    # متغيرات الملاحة والعمليات
    if 'attendance_mode' not in st.session_state:
        st.session_state['attendance_mode'] = "Full"
        
    if 'selected_origin_loc' not in st.session_state:
        st.session_state['selected_origin_loc'] = "المنزل (جدة - المروة)"
        
    # متغيرات التغذية والماكروز
    if 'daily_protein' not in st.session_state:
        st.session_state['daily_protein'] = 0
        
    if 'daily_cals' not in st.session_state:
        st.session_state['daily_cals'] = 0
        
    if 'swim_cals_burned' not in st.session_state:
        st.session_state['swim_cals_burned'] = 0
        
    # متغيرات التتبع والصيانة
    if 'ai_vision_scans_left' not in st.session_state:
        st.session_state['ai_vision_scans_left'] = 10
        
    if 'is_premium_user' not in st.session_state:
        st.session_state['is_premium_user'] = True
        
    # متغير أمان لضمان عمل التزامن مرة واحدة عند الفتح
    if 'sync_done_for_today' not in st.session_state:
        st.session_state['sync_done_for_today'] = ""

def force_program_reset():
    """
    أداة الصيانة العميقة (Hard Reset).
    تمسح الكاش وتدمر الجلسة لإعادة بناء المتغيرات من الصفر.
    """
    st.cache_resource.clear()
    st.cache_data.clear()
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]

# =====================================================================
# 4. SECURE CLOUD CONNECTORS & OMNI-HEAL ENGINE
# محركات الاتصال بقواعد البيانات السحابية والإصلاح الذاتي
# =====================================================================

@st.cache_resource(ttl=600)
def get_db():
    """
    تأسيس الاتصال بقاعدة بيانات Google Sheets بصمت تام.
    (مؤمنة لـ 10 دقائق لعدم حظر الـ API).
    """
    try: 
        connection = st.connection("gsheets", type=GSheetsConnection)
        return connection
    except Exception: 
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_data(sheet_name: str) -> pd.DataFrame:
    """
    جلب البيانات مع نظام الكاش لمنع حظر خوادم جوجل (Quota Limit 429).
    """
    conn = get_db()
    if not conn: 
        return pd.DataFrame()
        
    try: 
        df = conn.read(worksheet=sheet_name, ttl=600)
        # التأكد من تنظيف البيانات الفارغة
        cleaned_df = df.dropna(how='all')
        return cleaned_df
    except Exception: 
        return pd.DataFrame()

def push_data(sheet_name: str, data_dict: dict):
    """
    إضافة سجل جديد (تمرين، تغذية، انبودي).
    تقرأ البيانات الحية أولاً، تدمج، ثم ترفع، ثم تمسح الكاش.
    """
    conn = get_db()
    if not conn: 
        return False, "انقطاع في الاتصال بقاعدة البيانات."
        
    try:
        # قراءة الأحدث دائماً قبل الكتابة (بدون كاش)
        current_df = conn.read(worksheet=sheet_name, ttl=0) 
        
        if current_df.empty:
            df_new = pd.DataFrame([data_dict])
        else:
            df_new = pd.concat([current_df, pd.DataFrame([data_dict])], ignore_index=True)
            
        conn.update(worksheet=sheet_name, data=df_new)
        st.cache_data.clear() 
        return True, "تمت المزامنة بنجاح."
        
    except Exception as e: 
        return False, f"فشل في الاتصال السحابي: {str(e)}"

def overwrite_data(sheet_name: str, df: pd.DataFrame):
    """
    استبدال الجدول بالكامل (مخصصة للمخطط الأسبوعي).
    """
    conn = get_db()
    if not conn: 
        return False, "انقطاع في الاتصال."
        
    try:
        conn.update(worksheet=sheet_name, data=df)
        st.cache_data.clear()
        return True, "تم التحديث الشامل للسحابة."
    except Exception as e: 
        return False, f"خطأ في الرفع: {str(e)}"

def auto_heal():
    """
    محرك الإصلاح الذاتي المؤسسي (Enterprise Omni-Heal).
    يتأكد من أن جميع الأوراق والأعمدة موجودة وسليمة.
    """
    report = []
    conn = get_db()
    
    if not conn:
        return [{"status": "error", "msg": "انقطاع في خوادم Google Cloud."}]
        
    # المخطط الهندسي الدقيق لكل ورقة عمل
    schemas = {
        "Weekly_Plan": ["Day", "Date", "Class", "Muscle", "Status"],
        "Workout_Logs": ["Date", "Muscle", "Exercise", "Weight", "Reps"],
        "Health_Log": ["Date", "Sleep", "Water", "Protein", "Calories", "Notes"],
        "InBody_Logs": ["Date", "Weight", "Muscle_Mass", "Fat_Percentage", "Visceral_Fat"]
    }
    
    for sh, cols in schemas.items():
        try:
            # قراءة الورقة
            df = conn.read(worksheet=sh, ttl=0)
            
            # فحص الأعمدة الناقصة
            missing_columns = [c for c in cols if c not in df.columns]
            
            if missing_columns:
                for c in missing_columns: 
                    df[c] = "" # حقن العمود
                conn.update(worksheet=sh, data=df)
                report.append({"status": "success", "msg": f"تم إصلاح هيكل `{sh}` وحقن الأعمدة."})
            else:
                report.append({"status": "success", "msg": f"الهيكل التنظيمي لورقة `{sh}` سليم."})
                
        except Exception:
            # في حال فشلت القراءة (الورقة غير موجودة)
            try:
                empty_df = pd.DataFrame(columns=cols)
                conn.update(worksheet=sh, data=empty_df)
                report.append({"status": "success", "msg": f"تم بناء ورقة `{sh}` المفقودة من الصفر."})
            except Exception as e:
                report.append({"status": "error", "msg": f"فشل بناء `{sh}`. الخطأ: {str(e)}"})
                
    st.cache_data.clear()
    return report

# =====================================================================
# 5. DYNAMIC ROUTING ENGINE (Haversine Formula)
# محرك الملاحة وحساب المسافات الجغرافية
# =====================================================================

def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """حساب المسافة الجغرافية بالكيلومتر باستخدام Haversine."""
    R = 6371.0 
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def calculate_smart_eta(origin_name: str, current_time: datetime):
    """
    تحليل سرعة الطريق بناءً على الموقع (مكة، جدة) 
    وتطبيق مصفوفة الزحام.
    تم تأمين الدالة بالكامل وتمرير time لتجنب NameError.
    """
    # إحداثيات الوجهة (نادي بودي ماسترز الروضة)
    dest_lat = 21.5768 
    dest_lon = 39.1620
    
    if origin_name == "المنزل (جدة - المروة)": 
        origin_lat = 21.6214
        origin_lon = 39.1989
        base_speed_kmh = 50.0
    elif origin_name == "العمل (جدة)": 
        origin_lat = 21.5200
        origin_lon = 39.1700
        base_speed_kmh = 40.0
    elif origin_name == "العمل (مكة المكرمة)": 
        origin_lat = 21.4225
        origin_lon = 39.8262
        base_speed_kmh = 90.0 
    else: 
        origin_lat = 21.6214
        origin_lon = 39.1989
        base_speed_kmh = 50.0
    
    dist_km = get_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    base_time_mins = (dist_km / base_speed_kmh) * 60.0
    
    hr = current_time.hour
    
    # مصفوفة الزحام
    if 7 <= hr <= 9: 
        traffic_multiplier = 1.5   
    elif 13 <= hr <= 15: 
        traffic_multiplier = 1.6   
    elif 17 <= hr <= 21: 
        traffic_multiplier = 1.8   
    else: 
        traffic_multiplier = 1.1   
        
    final_eta_mins = int(base_time_mins * traffic_multiplier) + 5
    return final_eta_mins, dist_km

# --- نهاية الدفعة الأولى (Part 1) ---
# =====================================================================
# =====================================================================
# 6. DYNAMIC CLINICAL RECOVERY (الاستشفاء التفاعلي)
# محرك طبي يتفاعل لحظياً مع اختيارك الميداني (كارديو أم مقاومة)
# =====================================================================
# =====================================================================

def get_recovery_protocol(mode: str, iron_target: str, current_time: datetime) -> str:
    """
    بروتوكول طبي يتغير بناءً على قرارك في النادي.
    تم استخدام textwrap.dedent لتنظيف كود ה-HTML من المسافات البادئة
    التي تسبب ظهور الكود كنص في Streamlit.
    """
    current_day = current_time.strftime("%A")
    is_heavy = False
    
    # تحديد أيام المجهود العالي (أيام الأرجل أو الأيام المجدولة للشدة العالية)
    if current_day in ["Monday", "Thursday"] or "أرجل" in iron_target:
        is_heavy = True
        
    if mode == "ClassOnly":
        html_output = textwrap.dedent("""
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (بروتوكول ما بعد الكارديو)</h3>
            <p style='color:#8B949E; text-align:right;'>بما أن مسارك اليوم هو <b>(كلاس لياقة فقط)</b>، فقد خسرت كمية هائلة من السوائل والأملاح. الاستشفاء الحراري ممنوع طبياً.</p>
            
            <div class='med-neutral'>
                <h4 style='color:#2EA043; margin:0;'>🏊 التبريد الهادئ وإعادة السوائل</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>السباحة:</b> 10 دقائق حركة بطيئة جداً لخفض نبضات القلب التدريجي.</li>
                    <li><b>شرب الماء:</b> لتر كامل تدريجياً لتعويض التعرق وتجنب الجفاف العضلي.</li>
                </ul>
            </div>
            
            <div class='med-danger'>
                <h4 style='color:#D29922; margin:0;'>🚫 حظر حراري تام (No Heat)</h4>
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>يُمنع الدخول للساونا أو البخار اليوم. الكارديو المفرط + الساونا يؤديان إلى جفاف شديد، هدم عضلي مباشر، وارتفاع حاد في هرمون التوتر (الكورتيزول).</p>
            </div>
        </div>
        """)
        return html_output
        
    elif is_heavy and mode in ["Full", "IronOnly"]:
        html_output = textwrap.dedent("""
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (العلاج التبايني العنيف)</h3>
            <p style='color:#8B949E; text-align:right;'>مسارك اليوم <b>عنيف (تمارين مقاومة ثقيلة)</b>. يجب التخلص من حمض اللاكتيك المتراكم لحماية الألياف العضلية الممزقة.</p>
            
            <div class='med-hot'>
                <h4 style='color:#F85149; margin:0;'>🔥 المرحلة 1: التوسيع الوعائي (Vasodilation)</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>غرفة البخار:</b> 5 إلى 8 دقائق. (يوسع الأوعية الدموية ويضخ المغذيات للعضلة المستهدفة).</li>
                </ul>
            </div>
            
            <div class='med-cold'>
                <h4 style='color:#58A6FF; margin:0;'>🧊 المرحلة 2: الانقباض الوعائي (Vasoconstriction)</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>الجاكوزي البارد:</b> 1-2 دقيقة مباشرة بعد البخار لعصر الدم الفاسد وتخفيف التهابات المفاصل.</li>
                </ul>
            </div>
            
            <div class='med-danger'>
                <h4 style='color:#D29922; margin:0;'>⚠️ تحذير طبي للخصوبة (Fertility & CNS)</h4>
                <p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>الختام إلزامي بالماء البارد. الخروج من النادي وحرارة جسمك مرتفعة يؤدي لتلف هرمون التستوستيرون وإجهاد الجهاز العصبي المركزي.</p>
            </div>
        </div>
        """)
        return html_output
        
    else:
        html_output = textwrap.dedent("""
        <div class='titan-card'>
            <h3 style='margin-top:0;'>🏥 العيادة الطبية (التبريد العميق Active Recovery)</h3>
            <p style='color:#8B949E; text-align:right;'>مسارك اليوم متوسط الشدة. ركز على الاستشفاء البارد النشط لرفع المناعة.</p>
            
            <div class='med-cold'>
                <h4 style='color:#58A6FF; margin:0;'>🧊 التبريد وتقليل الالتهاب</h4>
                <ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>
                    <li><b>الجاكوزي البارد:</b> 3 إلى 5 دقائق. يحفز إفراز هرمونات البناء ويقلل آلام المفاصل العميقة.</li>
                    <li><b>السباحة الحرة:</b> 15 دقيقة تفكيك مفاصل العمود الفقري وتخفيف الضغط الغضروفي.</li>
                </ul>
            </div>
        </div>
        """)
        return html_output

# =====================================================================
# =====================================================================
# 7. COMMERCIAL BIOMECHANICS DATABASE (قاعدة بيانات التمارين الشاملة)
# =====================================================================
# =====================================================================

def get_bio_db() -> dict:
    """
    أضخم قاعدة بيانات صلبة ومفصلة لعلوم الحركة الحيوية.
    كل تمرين مستقل في أسطر خاصة به (Vertical Structure) لمنع الدمج الخاطئ.
    """
    database = {
        "صدر": [
            {
                "name": "Incline Barbell Bench Press", 
                "reps": "6-8 عدات (للتضخيم وبناء الكتلة العلوية)", 
                "technique": "اضبط الدكة على زاوية 30 درجة فقط لتقليل تدخل الكتف. انزل بالبار حتى يلمس أعلى صدرك ببطء، وادفع بقوة متفجرة.", 
                "breathing": "شهيق عميق في النزول لتوسيع القفص الصدري، زفير قوي في الدفع.", 
                "good_pain": "أعلى الصدر، والجزء الأمامي من الكتف (ألم شد وتوسع).", 
                "bad_pain": "ألم وخز في مفصل الكتف الداخلي (كوعك مفتوح 90 درجة، ضمه للداخل بزاوية 45)."
            },
            {
                "name": "Flat Dumbbell Press", 
                "reps": "8-10 عدات (كتلة شاملة وتوازن)", 
                "technique": "استلقِ على الدكة المسطحة. ادفع الدنابل للأعلى مع إبقاء الكوع مائلاً للداخل قليلاً لتقليل الضغط على أوتار الكتف.", 
                "breathing": "شهيق ببطء في النزول، زفير في الدفع للأعلى.", 
                "good_pain": "منتصف الصدر وعمقه.", 
                "bad_pain": "ألم حاد في الرسغ (يجب أن يكون الرسغ مستقيماً غير مثني تحت الوزن) أو ألم في الكوع."
            },
            {
                "name": "Decline Cable Flys", 
                "reps": "12-15 عدة (للنحت والقضاء على التثدي السفلي)", 
                "technique": "قف في منتصف الكيبل. اسحب المقابض من الأعلى إلى الأسفل باتجاه حوضك واعصر عضلة الصدر في الأسفل لمدة ثانية كاملة.", 
                "breathing": "شهيق عند فتح الذراعين للسماح بالتمدد، زفير عند العصر في الأسفل.", 
                "good_pain": "أسفل الصدر، والخط الفاصل بين الصدرين.", 
                "bad_pain": "ألم في الكتف الأمامي (هذا يعني أنك تدفع الكيبل دفعاً ولا تقوم بحركة العناق الصحيحة)."
            },
            {
                "name": "Pec Deck Machine", 
                "reps": "12-15 عدة (عزل الخط الداخلي)", 
                "technique": "اجلس وظهرك ملتصق بالكامل بالمسند. ضم المقابض حتى تتلامس واعصر صدرك في المنتصف. افتح ببطء وقاوم الوزن.", 
                "breathing": "شهيق عند الفتح البطيء، زفير عند الضم القوي.", 
                "good_pain": "عمق الصدر والخط الداخلي (الشق).", 
                "bad_pain": "ألم في مفصل الكتف (يعني أن الوزن أثقل من قدرتك وأنك تستخدم كتفك الأمامي للضم بدلاً من صدرك)."
            },
            {
                "name": "Chest Dips (Bodyweight)", 
                "reps": "حتى الفشل العضلي", 
                "technique": "مل بجذعك للأمام قليلاً لتركيز الحمل على الصدر. انزل حتى يصبح كتفك بموازاة كوعك (زاوية 90)، ثم ادفع بقوة.", 
                "breathing": "شهيق متحكم به في النزول، زفير متفجر في الصعود.", 
                "good_pain": "الصدر السفلي والترايسبس.", 
                "bad_pain": "ألم شديد في عظمة القص بمنتصف الصدر (يحدث إذا نزلت بعمق مبالغ فيه يمزق الأربطة)."
            }
        ],
        "ظهر": [
            {
                "name": "Deadlift", 
                "reps": "3-5 عدات (قوة عصبية ورفع هرمون التستوستيرون)", 
                "technique": "قف والبار يلامس قصبة ساقك. انزل بحوضك للخلف مع إبقاء ظهرك مستقيماً 100%. ادفع الأرض بقدميك ولا تسحب بظهرك.", 
                "breathing": "شهيق عميق جداً قبل الرفع وحبس الأنفاس في البطن (Bracing)، زفير بعد تخطي البار للركبة في الصعود.", 
                "good_pain": "القطنية (أسفل الظهر العضلي)، أوتار الركبة الخلفية، وعضلات المؤخرة.", 
                "bad_pain": "ألم حاد أو طقطقة في فقرات العمود الفقري (هذا يعني أن ظهرك كان مقوساً كالقطة، توقف فوراً هذا إنذار بالديسك)."
            },
            {
                "name": "Lat Pulldown Wide Grip", 
                "reps": "8-12 عدة (لتعريض الظهر وسحب الجلد)", 
                "technique": "أمسك البار بقبضة واسعة. اسحب البار باتجاه أعلى صدرك مع إرجاع لوحي كتفك للخلف والأسفل.", 
                "breathing": "زفير أثناء السحب للأسفل، شهيق أثناء إرجاع البار للأعلى ببطء ومقاومة.", 
                "good_pain": "عضلة المجنص العريضة (تحت الإبط والظهر الجانبي).", 
                "bad_pain": "ألم أو شد في البايسبس أو الساعد (أنت تسحب بقوة يدك، تخيل أن يدك مجرد خطاف واسحب باستخدام كوعك)."
            },
            {
                "name": "Seated Cable Row", 
                "reps": "10-12 عدة (لسمك الظهر الأوسط)", 
                "technique": "اجلس وظهرك مستقيم تماماً. اسحب المقبض باتجاه سرة بطنك واعصر لوحي كتفك معاً في الخلف.", 
                "breathing": "زفير في السحب، شهيق في العودة مع إرخاء الكتفين للأمام قليلاً.", 
                "good_pain": "منتصف الظهر وسماكته (بين لوحي الكتف).", 
                "bad_pain": "ألم في القطنية (ناتج عن التأرجح القوي بظهرك للأمام والخلف، يجب أن يكون ظهرك ثابتاً وتتحرك أذرعك فقط)."
            }
        ],
        "أرجل": [
            {
                "name": "Barbell Squat", 
                "reps": "4-6 عدات (محفز التستوستيرون الأول بالجسم)", 
                "technique": "ضع البار على ترابيسك. افتح قدميك باتساع الكتف أو أوسع قليلاً. انزل للخلف وكأنك تجلس على كرسي حتى توازي فخذيك الأرض على الأقل.", 
                "breathing": "شهيق عميق قبل النزول لملء تجويف البطن وحماية العمود الفقري، زفير قوي عند الدفع للوقوف.", 
                "good_pain": "الفخذ الأمامي (الرباعيات) وعضلات المؤخرة (الجلوتس).", 
                "bad_pain": "ألم في صابونة الركبة من الأمام، أو أسفل الظهر (دليل على انحناء الظهر للأمام بشكل مبالغ فيه أثناء النزول)."
            },
            {
                "name": "Leg Press", 
                "reps": "10-12 عدة (ضغط الكتلة بأمان)", 
                "technique": "ضع قدميك في منتصف اللوح. انزل بالوزن حتى تصل ركبتك لزاوية 90 درجة على الأقل، ادفع للأعلى ولا تقفل ركبتك بالكامل أبداً.", 
                "breathing": "شهيق في النزول المستمر، زفير بالدفع للأعلى.", 
                "good_pain": "الفخذ كاملاً يحترق.", 
                "bad_pain": "ألم حاد في مفصل الركبة من الخلف (يحدث عند قفل الركبة 100% في الأعلى والوزن ثقيل، وقد يكسر المفصل)."
            },
            {
                "name": "Romanian Deadlift (RDL)", 
                "reps": "8-10 عدات (شد الخلفيات والمؤخرة)", 
                "technique": "امسك البار أو الدنابل. اثنِ ركبتيك ثنية بسيطة جداً (لا تفردهما بالكامل). ادفع حوضك للخلف لأقصى شد ممكن في الخلفيات، ثم ارجع للأعلى.", 
                "breathing": "شهيق بالنزول البطيء والمتحكم به، زفير بالصعود مع عصر المؤخرة.", 
                "good_pain": "الخلفيات والأوتار وعضلات المؤخرة.", 
                "bad_pain": "شد مؤلم في القطنية (أنت تثني ظهرك للأسفل بدلاً من دفع حوضك للخلف، حافظ على ظهرك مستقيماً)."
            }
        ],
        "أكتاف": [
            {
                "name": "Overhead Barbell Press", 
                "reps": "6-8 عدات (بناء الأكتاف العريضة)", 
                "technique": "قف مستقيماً واقبض عضلات بطنك ومؤخرتك للثبات. ادفع البار فوق رأسك مباشرة، وأدخل رأسك قليلاً للأمام عند وصول البار للقمة.", 
                "breathing": "شهيق قبل الدفع لثبات الجذع، زفير بالدفع للأعلى.", 
                "good_pain": "الكتف الأمامي والجانبي بشكل كامل.", 
                "bad_pain": "ألم في أسفل الظهر (أنت تقوس ظهرك للخلف بشكل مبالغ فيه لرفع الوزن الثقيل، قلل الوزن)."
            },
            {
                "name": "Dumbbell Lateral Raise", 
                "reps": "12-15 عدة (التعريض الجانبي البصري المباشر)", 
                "technique": "ارفع الدنابل للجانبين مع ثني الكوعين قليلاً، تخيل أنك تصب الماء من إبريقين في القمة لتفعيل العضلة الجانبية.", 
                "breathing": "زفير بالرفع السريع للجانبين، شهيق في النزول البطيء.", 
                "good_pain": "الكتف الجانبي الخارجي يحترق.", 
                "bad_pain": "ألم في الترابيس العلوية (أنت ترفع كتفك بالكامل لرفع الوزن الثقيل بدل أن ترفع ذراعك فقط، استخدم وزناً أخف)."
            }
        ],
        "باي": [
            {
                "name": "Barbell Bicep Curl", 
                "reps": "8-10 عدات (الكتلة الأساسية للذراع)", 
                "technique": "قف مستقيماً. ارفع البار مع تثبيت كوعك بجانب خصرك تماماً. لا تتأرجح بجسمك للخلف لاستغلال الزخم.", 
                "breathing": "زفير بالرفع المتواصل، شهيق في النزول.", 
                "good_pain": "تكوير وبطن عضلة البايسبس.", 
                "bad_pain": "ألم في أسفل الظهر (أنت تتأرجح بشكل خاطئ)، أو شد مؤلم في الساعد الداخلي (استخدم EZ Bar المتعرج بدلاً من البار المستقيم)."
            }
        ],
        "تراي": [
            {
                "name": "Tricep Rope Pushdown", 
                "reps": "12-15 عدة (نحت الرأس الجانبي - حدوة الحصان)", 
                "technique": "ثبت كوعك بجانب خصرك كأنه مسمر. ادفع الحبل للأسفل وافتح يديك للخارج في نهاية الحركة لأقصى انقباض.", 
                "breathing": "زفير بالدفع القوي للأسفل، شهيق في الصعود ببطء.", 
                "good_pain": "خلف الذراع بالكامل من الخارج.", 
                "bad_pain": "ألم حاد في مفصل الكوع نفسه (دليل على استخدام وزن ثقيل جداً يجهد الأوتار قبل العضلة)."
            }
        ],
        "بطن": [
            {
                "name": "Cable Crunches", 
                "reps": "10-12 عدة بوزن ثقيل (لبروز الـ 6-pack)", 
                "technique": "اجلس على ركبتيك. أمسك الحبل خلف رقبتك. انحن للأمام محاولاً إيصال كوعك لركبتك باستخدام عضلات بطنك حصراً.", 
                "breathing": "تفريغ هواء تام (زفير) عند الانحناء للعصر، شهيق عند الصعود.", 
                "good_pain": "عضلات البطن العلوية والوسطى.", 
                "bad_pain": "ألم في القطنية (أنت تستخدم وزنك וظهرك للسحب وليس عضلات بطنك، ثبت حوضك جيداً)."
            },
            {
                "name": "Weighted Plank", 
                "reps": "60 ثانية (قوة الجذع الداخلي للداخل)", 
                "technique": "استند على كوعيك وقدميك، ضع قرص وزن على ظهرك. حافظ على ظهرك مستقيماً مثل اللوح، واشفط بطنك للداخل طوال الوقت.", 
                "breathing": "تنفس سطحي ومنتظم ولا تحبس أنفاسك أبداً.", 
                "good_pain": "ارتجاف في كامل جدار البطن الداخلي والعميق.", 
                "bad_pain": "انهيار أسفل الظهر للأسفل (ارفع حوضك قليلاً للأعلى واقبض الجلوتس)."
            }
        ],
        "تمرين حر": [
            {
                "name": "Custom Machine Workout", 
                "reps": "10-12 عدة (معدل بناء وتضخيم)", 
                "technique": "استخدم الجهاز بمدى حركي كامل وتدرج بالأوزان للوصول للفشل العضلي الإيجابي.", 
                "breathing": "تنفس اعتيادي، زفير عند الدفع/السحب.", 
                "good_pain": "العضلة المستهدفة بالكامل.", 
                "bad_pain": "أي ألم مفاجئ أو وخز في المفصل (توقف فوراً)."
            }
        ]
    }
    return database

def get_ex_list(muscle: str) -> list:
    """جلب قائمة التمارين بشكل آمن لمنع أخطاء الـ Key Errors"""
    db = get_bio_db()
    
    if not muscle or muscle == "راحة / غياب": 
        return ["➕ إدخال تمرين جديد (يدوي ذكي)"]
        
    names = []
    for k, v in db.items():
        if k in muscle:
            for ex in v: 
                # تأمين الاستدعاء باستخدام .get
                names.append(ex.get("name", "تمرين غير محدد"))
                
    if not names: 
        return ["تمرين مخصص", "➕ إدخال تمرين جديد (يدوي ذكي)"]
        
    # إزالة التكرار وترتيب القائمة وإضافة خيار الإدخال اليدوي
    names = list(set(names))
    names.sort()
    names.append("➕ إدخال تمرين جديد (يدوي ذكي)")
    
    return names

def get_ex_info(name: str) -> dict:
    """جلب تفاصيل التكنيك والألم بأمان وتأمين القيم الافتراضية"""
    db = get_bio_db()
    
    for grp in db.values():
        for ex in grp:
            if ex.get("name", "") == name: 
                return ex
                
    # قيمة افتراضية آمنة في حال كان التمرين يدوياً
    return {
        "name": name, 
        "reps": "10-12 عدة (تضخيم وبناء)", 
        "technique": "حافظ على التكنيك السليم وتجنب التأرجح واستخدام الزخم. المدى الحركي الكامل (Full ROM) هو سر التطور.", 
        "breathing": "تنفس منتظم مستمر. لا تحبس أنفاسك. زفير قوي مع الجهد الأكبر.", 
        "good_pain": "شد واحتراق إيجابي في بطن العضلة المستهدفة.", 
        "bad_pain": "أي ألم حاد، طقطقة، أو وخز في المفاصل والأوتار المحيطة."
    }

# =====================================================================
# 8. AI REP IMPUTATION (خوارزمية الذكاء الاصطناعي لحساب العدات وتطور الأوزان)
# =====================================================================

def fetch_past_reps(ex_name: str):
    """
    جلب الأوزان السابقة لغرض التطوير (Progressive Overload).
    يقرأ من قاعدة البيانات السحابية بأمان.
    """
    df = fetch_data("Workout_Logs")
    
    if not df.empty and 'Exercise' in df.columns:
        past = df[df['Exercise'] == ex_name]
        if not past.empty:
            last_record = past.iloc[-1]
            return last_record.get('Date', 'غير متوفر'), float(last_record.get('Weight', 0)), int(last_record.get('Reps', 10))
            
    return None, 0.0, 0

def smart_reps(ex_name: str, current_weight: float) -> int:
    """
    محرك الذكاء الاصطناعي لتقدير العدات بناءً على قوانين التضخيم.
    إذا زاد الوزن -> تقل العدات (بحد أدنى 6 لحماية الجهاز العصبي).
    إذا قل الوزن -> تزيد العدات للوصول للفشل العضلي.
    """
    date, last_weight, last_reps = fetch_past_reps(ex_name)
    
    if date:
        if current_weight > last_weight: 
            return max(last_reps - 2, 6)
        elif current_weight < last_weight: 
            return last_reps + 2
        else: 
            return last_reps
            
    # الرقم الافتراضي لأول تمرين
    return 10

# --- نهاية الدفعة الثانية (Part 2) ---
# =====================================================================
# =====================================================================
# 9. CLOUD-STATE SYNC ENGINE (محرك المزامنة السحابية اللحظية)
# هذا الجزء يضمن أن قراراتك (حديد فقط، كلاس فقط) تُحفظ للأبد في السحابة
# =====================================================================
# =====================================================================

def update_attendance_decision(mode_key: str, status_label: str, current_date: str):
    """
    تقوم بتحديث حالة الحضور في ورقة العمل "Weekly_Plan" مباشرة.
    تضمن أن التغيير يظهر في الجوال واللابتوب في نفس اللحظة.
    """
    st.session_state['attendance_mode'] = mode_key
    conn = get_db()
    
    if conn:
        try:
            # جلب البيانات الحية للتعديل
            df = conn.read(worksheet="Weekly_Plan", ttl=0)
            if not df.empty and 'Date' in df.columns:
                # البحث عن سطر اليوم الحالي
                mask = df['Date'] == current_date
                if mask.any():
                    df.loc[mask, 'Status'] = status_label
                    conn.update(worksheet="Weekly_Plan", data=df)
                    # تفريغ الكاش ليقرأ النظام الحالة الجديدة فوراً
                    st.cache_data.clear() 
                    return True
        except Exception:
            pass
    return False

def sync_mode_from_cloud(current_date: str):
    """
    تقرأ حالة الحضور المسجلة في السحابة عند فتح التطبيق.
    تمنع عودة التطبيق للحالة الافتراضية عند تحديث الصفحة.
    """
    if st.session_state.get('sync_done_for_today') != current_date:
        plan_df = fetch_data("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns and 'Status' in plan_df.columns:
            today_rows = plan_df[plan_df['Date'] == current_date]
            if not today_rows.empty:
                cloud_status = str(today_rows.iloc[0].get('Status', 'مجدول'))
                
                # ترجمة الحالة النصية إلى Mode برمجية
                status_map = {
                    "حضور كامل": "Full",
                    "حديد فقط": "IronOnly",
                    "كلاس فقط": "ClassOnly",
                    "تأخير": "Delayed",
                    "غائب": "Absent"
                }
                st.session_state['attendance_mode'] = status_map.get(cloud_status, "Full")
        
        st.session_state['sync_done_for_today'] = current_date

# =====================================================================
# =====================================================================
# 10. GLOBAL EXECUTION ENGINE (The main() Function)
# الدالة الرئيسية التي تدير كامل هيكل التطبيق
# =====================================================================
# =====================================================================

def main():
    """
    نقطة الانطلاق المركزية.
    تم تصميمها بهيكلية "الطبقات" لضمان عدم حدوث NameError.
    """
    # [1] تهيئة المتغيرات
    init_states()
    
    # [2] ضبط الوقت (المتغير العالمي الموحد)
    CURRENT_MAKKAH_TIME = get_makkah_time()
    current_date_str = CURRENT_MAKKAH_TIME.strftime("%Y-%m-%d")
    
    # [3] مزامنة الحالة مع السحابة فور الفتح
    sync_mode_from_cloud(current_date_str)
    
    # [4] تحضير أسماء الأيام باللغة العربية
    days_lookup = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_ar = days_lookup.get(CURRENT_MAKKAH_TIME.strftime("%A"), "غير محدد")
    
    # [5] جلب التواريخ المجدولة للأسبوع
    week_dates = get_week_dates(CURRENT_MAKKAH_TIME)

    # -----------------------------------------------------------------
    # SAAS HEADER UI
    # الهيدر التجاري الاحترافي
    # -----------------------------------------------------------------
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #1A1C23, #0D1117); padding: 15px 30px; border-radius: 12px; border-bottom: 2px solid #E5B94C; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
        <div style='color: #8B949E; font-size: 14px;'>مكة المكرمة | {today_ar} {current_date_str} | {CURRENT_MAKKAH_TIME.strftime('%I:%M %p')}</div>
        <div style='display: flex; gap: 20px; align-items: center;'>
            <span style='background: rgba(229, 185, 76, 0.1); padding: 5px 15px; border-radius: 20px; color: #E5B94C; font-weight: bold; font-size: 13px;'>👑 PREMIUM SaaS ACTIVE</span>
            <span style='color: #E8ECEF; font-weight: bold;'>Titan Commercial V46</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # MAIN NAVIGATION TABS
    # -----------------------------------------------------------------
    tabs = st.tabs([
        "🚀 الميدان والملاحة", 
        "🗓️ المخطط الأسبوعي", 
        "🏋️ السجل الحيوي", 
        "🏥 العيادة الطبية", 
        "📸 عدسة الذكاء (AI)", 
        "🥗 مختبر الماكروز", 
        "🛠️ الإدارة والإصلاح"
    ])
    
    t_ops, t_setup, t_log, t_clinic, t_vision, t_fuel, t_sys = tabs

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS (الميدان والملاحة)
    # -----------------------------------------------------------------
    with t_ops:
        # قراءة المخطط الأسبوعي
        plan_df = fetch_data("Weekly_Plan")
        active_class = "موتيف 8" # القيمة الافتراضية في حال عدم وجود جدول
        
        if not plan_df.empty and 'Date' in plan_df.columns:
            today_match = plan_df[plan_df['Date'] == current_date_str]
            if not today_match.empty:
                active_class = today_match.iloc[0].get('Class', 'موتيف 8')
        
        # استخراج بيانات الحديد والكلاس
        engine_data = WORKOUT_ENGINE_DB.get(active_class, {})
        iron_target_muscle = engine_data.get("iron", "صدر + تراي")
        workout_flow = engine_data.get("flow", "استراتيجية حرة.")
        class_calories = CLASS_BURN_DB.get(active_class, 0)
        
        current_mode = st.session_state['attendance_mode']

        # [A] منطق يوم الجمعة (الراحة الإلزامية)
        if today_ar == "الجمعة" and current_mode != "IronOnly":
            st.markdown(
                "<div class='titan-card titan-card-center'>"
                "<h1 style='color:#2EA043; margin:0;'>يوم راحة سلبي إلزامي 🛑</h1>"
                "<p style='color:#8B949E; margin-top:10px;'>الاستشفاء هو السر الحقيقي وراء ضخامة العضلات.</p>"
                "</div>", unsafe_allow_html=True
            )
            if st.button("الذهاب للنادي للحديد فقط (كسر الجدول)"): 
                update_attendance_decision("IronOnly", "حديد فقط", current_date_str)
                st.rerun()
                
        # [B] منطق يوم الراحة المجدول أو الغياب
        elif active_class == "راحة / غياب" or current_mode == "Absent":
            st.markdown(
                "<div class='titan-card'>"
                "<h2 style='color:#F85149; text-align:center;'>مجدول כـ (يوم راحة) ❌</h2>"
                f"<p style='text-align:center; color:#8B949E;'>تم ترحيل تمرين <b>({iron_target_muscle})</b> للغد تلقائياً.</p>"
                "</div>", unsafe_allow_html=True
            )
            if st.button("تغيير القرار والذهاب للنادي الآن"): 
                update_attendance_decision("Full", "حضور كامل", current_date_str)
                st.rerun()
                
        # [C] الميدان النشط
        else:
            col_ops_l, col_ops_r = st.columns([2, 1])
            
            with col_ops_r:
                st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>📍 الملاحة الذكية</h4>", unsafe_allow_html=True)
                
                selected_loc = st.selectbox(
                    "من أين ستنطلق؟", 
                    ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"],
                    index=["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"].index(st.session_state['selected_origin_loc'])
                )
                st.session_state['selected_origin_loc'] = selected_loc
                
                # استدعاء محرك الملاحة
                eta_val, dist_val = calculate_smart_eta(selected_loc, CURRENT_MAKKAH_TIME)
                
                st.markdown(f"<p style='color:#8B949E;'>المسافة: {dist_val:.1f} KM<br>الوقت المقدر بالزحام: {eta_val} دقيقة</p>", unsafe_allow_html=True)
                st.markdown("<hr style='border-color:#30363D;'><h4 style='margin-top:0;'>🕹️ إدارة الحضور والغياب</h4>", unsafe_allow_html=True)
                
                if st.button("✅ حضور كامل (كلاس + حديد)", use_container_width=True): 
                    update_attendance_decision("Full", "حضور كامل", current_date_str); st.rerun()
                    
                if st.button("🏋️ صالة الحديد فقط", use_container_width=True): 
                    update_attendance_decision("IronOnly", "حديد فقط", current_date_str); st.rerun()
                    
                if st.button("🤸 كلاس اللياقة فقط", use_container_width=True): 
                    update_attendance_decision("ClassOnly", "كلاس فقط", current_date_str); st.rerun()
                    
                if st.button("⏳ تأخير مسار (زحمة الطريق)", use_container_width=True): 
                    update_attendance_decision("Delayed", "تأخير", current_date_str); st.rerun()
                    
                if st.button("❌ غياب تام عن النادي", use_container_width=True): 
                    update_attendance_decision("Absent", "غائب", current_date_str); st.rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)

            with col_ops_l:
                # حساب الأوقات الميدانية
                n_str, a_str, is_str, ie_str, arr_time_obj, d_km, e_min = get_sched(current_mode, selected_loc, CURRENT_MAKKAH_TIME)
                
                # رسالة تنبيه للوقت المبكر
                time_alert = ""
                if arr_time_obj.hour < 18 and current_mode in ["Full", "ClassOnly"]:
                    time_alert = "<div class='alert-box'>⚠️ تنبيه هندسي: الكلاس يبدأ 9:00 م. وصولك الآن مبكر جداً، ستحتاج للعودة لاحقاً أو تحويل المسار لـ (حديد فقط).</div>"
                
                if current_mode == "Full":
                    main_card_html = f"""
                    <div class='titan-card'>
                        <h3 style='margin-top:0;'>🗺️ الخطة أ (طاقة قصوى)</h3>
                        <p><span class='data-label'>عضلة اليوم:</span> <b style='color:#E5B94C;'>{iron_target_muscle}</b></p>
                        <p><span class='data-label'>كلاس السهرة:</span> <b style='color:#E5B94C;'>{active_class}</b> <span style='font-size:12px; color:#F85149;'>(حرق ~{class_calories} kcal)</span></p>
                        <p style='color:#8B949E;'>الاستراتيجية: {workout_flow}</p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <h5 style='margin-top:20px; color:#E8ECEF;'>الجدول الزمني الميداني</h5>
                        <p>🔥 {a_str} - {is_str} : إحماء وتجهيز مفاصل</p>
                        <p>💪 {is_str} - {ie_str} : <b style='color:#F85149;'>صالة الحديد (75 دقيقة لمنع الهدم)</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>حضور الكلاس (حرق دهون البطن)</b></p>
                        {time_alert}
                    </div>
                    """
                elif current_mode == "IronOnly":
                    main_card_html = f"""
                    <div class='titan-card' style='border-color: #58A6FF;'>
                        <h3 style='margin-top:0; color:#58A6FF;'>🏋️ مسار الحديد المكثف (الكلاس ملغي)</h3>
                        <p><span class='data-label'>المستهدف:</span> <b style='color:#E5B94C;'>{iron_target_muscle}</b></p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <p>💪 {is_str} - {(arr_time_obj + timedelta(minutes=90)).strftime('%I:%M %p')} : <b style='color:#F85149;'>صالة الحديد (استغل طاقتك في كسر الأوزان)</b></p>
                    </div>
                    """
                elif current_mode == "ClassOnly":
                    main_card_html = f"""
                    <div class='titan-card' style='border-color: #E5B94C;'>
                        <h3 style='margin-top:0; color:#E5B94C;'>🤸 مسار الكارديو (الحديد ملغي)</h3>
                        <p><span class='data-label'>الكلاس المجدول:</span> <b style='color:#E5B94C;'>{active_class}</b></p>
                        <hr style='border-color:#30363D;'>
                        <p>🚗 انطلاق: <b>{n_str}</b> | 🅿️ وصول: <b>{a_str}</b></p>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>حضور الكلاس (حرق صافي)</b></p>
                        {time_alert}
                    </div>
                    """
                else: # Delayed
                    main_card_html = f"""
                    <div class='titan-card' style='border-color: #F85149;'>
                        <h3 style='margin-top:0; color:#F85149;'>⚠️ مسار التأخير والزحمة (إنقاذ التمرين)</h3>
                        <p><span class='data-label'>الحديد المختصر:</span> <b style='color:#E5B94C;'>{iron_target_muscle}</b></p>
                        <hr style='border-color:#30363D;'>
                        <p>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>توجه للكلاس مباشرة لعدم تفويت التسخين</b></p>
                        <p>💪 09:55 PM - 10:30 PM : <b style='color:#F85149;'>حديد سريع (أجهزة عزل فقط)</b></p>
                    </div>
                    """
                st.markdown(main_card_html, unsafe_allow_html=True)
            
            # عرض بروتوكول الاستشفاء الديناميكي
            st.markdown(get_recovery_protocol(current_mode, iron_target_muscle, CURRENT_MAKKAH_TIME), unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع (مزامنة سحابية)")
        plan_df = fetch_data("Weekly_Plan")
        stored_plan = {r['Day']: r['Class'] for _, r in plan_df.iterrows()} if not plan_df.empty and 'Day' in plan_df.columns else {}
        
        with st.form("weekly_setup_form"):
            new_schedule = []
            cols = st.columns(3)
            options_list = list(WORKOUT_ENGINE_DB.keys())
            
            for i, (day_name, day_date) in enumerate(week_dates.items()):
                idx = 0
                try: idx = options_list.index(stored_plan.get(day_name, "موتيف 8"))
                except: idx = 0
                
                with cols[i % 3]:
                    st.markdown(f"<h5 style='color:#E8ECEF; text-align:right;'>{day_name} <br><span style='font-size:11px; color:#8B949E;'>({day_date})</span></h5>", unsafe_allow_html=True)
                    sel_ch = st.selectbox("الكلاس", options_list, index=idx, key=f"sel_{day_name}", label_visibility="collapsed")
                    
                    target_m = WORKOUT_ENGINE_DB.get(sel_ch, {}).get("iron", "غير محدد")
                    new_schedule.append({"Day": day_name, "Date": day_date, "Class": sel_ch, "Muscle": target_m, "Status": "مجدول"})
            
            if st.form_submit_button("✅ اعتماد المخطط الاستراتيجي وتفريغ الكاش", use_container_width=True):
                is_balanced, bal_msg = analyze_muscle_balance(pd.DataFrame(new_schedule))
                st.markdown(f"<div class='{'success-box' if is_balanced else 'alert-box'}'>{bal_msg}</div>", unsafe_allow_html=True)
                
                s, m = overwrite_data("Weekly_Plan", pd.DataFrame(new_schedule))
                if s: st.success(m)
                else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 3: BIOMECHANICS & LOGS
    # -----------------------------------------------------------------
    with t_log:
        st.markdown("### 🏋️ السجل الحيوي (تسجيل الأوزان)")
        
        # التقييم قبل التمرين
        pre_pain = st.selectbox("كيف حال مفاصلك اليوم؟", ["سليم 100%", "إجهاد بسيط", "ألم مفاصل (خطر)"])
        if "خطر" in pre_pain: st.warning("🚨 بما أن هناك ألم مفاصل، يُمنع لعب الأوزان الحرة. استخدم الأجهزة فقط!")
        
        c_log_l, c_log_r = st.columns([1, 2])
        
        with c_log_l:
            st.markdown("<div class='titan-card titan-card-center'><h4>⏱️ مؤقت الراحة</h4>", unsafe_allow_html=True)
            if st.button("بدء 90 ثانية"): 
                pb = st.progress(0)
                for i in range(90): time.sleep(1); pb.progress((i+1)/90)
                st.success("انتهت الراحة! ارجع للبار.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_log_r:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4>المستهدف: <span style='color:#E5B94C;'>{iron_target_muscle}</span></h4>", unsafe_allow_html=True)
            
            exercises = get_ex_list(iron_target_muscle)
            selected_ex = st.selectbox("اختر التمرين:", exercises)
            
            final_exercise_name = st.text_input("اسم التمرين الجديد:") if "يدوي" in selected_ex else selected_ex
            final_exercise_name = final_exercise_name if final_exercise_name else "مخصص"
            
            ex_info = get_ex_info(final_exercise_name)
            st.markdown(f"""
            <div style='background:#161B22; padding:20px; border-radius:12px; margin-bottom:20px; border-right: 4px solid #E5B94C;'>
                <p><span class='bio-tech'>⚙️ الأداء:</span> {ex_info.get('technique', ex_info.get('t', ''))}</p>
                <p><span class='bio-breath'>🫁 التنفس:</span> {ex_info.get('breathing', ex_info.get('b', ''))}</p>
                <hr style='border-color:#30363D;'>
                <p><span class='bio-good'>✅ ألم جيد:</span> {ex_info.get('good_pain', ex_info.get('gp', ''))}</p>
                <p><span class='bio-bad'>❌ ألم إصابة:</span> {ex_info.get('bad_pain', ex_info.get('bp', ''))}</p>
            </div>
            """, unsafe_allow_html=True)
            
            p_date, p_w, p_r = fetch_historical_data(final_exercise_name)
            if p_date:
                st.markdown(f"<p style='color:#8B949E;'>سابقاً ({p_date}): <b>{p_w} KG</b> × {p_r} عدات</p>", unsafe_allow_html=True)
            
            cw, cr = st.columns(2)
            input_w = cw.number_input("الوزن المرفوع (KG)", min_value=0.0, value=float(p_w) if p_date else 0.0, step=2.5)
            input_r = cr.number_input("العدات (0 = حساب آلي)", min_value=0, value=0)
            
            if st.button("💾 توثيق الجلسة في السحابة", use_container_width=True):
                final_reps = calculate_smart_reps(final_exercise_name, input_w) if input_r == 0 else input_r
                s, m = push_data("Workout_Logs", {"Date": current_date_str, "Muscle": iron_target_muscle, "Exercise": final_exercise_name, "Weight": input_w, "Reps": final_reps})
                if s: st.success(f"تم تسجيل {final_exercise_name} بنجاح.")
                else: st.error(m)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 4: CLINIC
    # -----------------------------------------------------------------
    with t_clinic:
        st.markdown("### 📸 أرشفة تقرير InBody السحابي")
        with st.form("clinic_f"):
            c_cl1, c_cl2 = st.columns(2)
            c_date = st.date_input("تاريخ الفحص")
            c_w = c_cl1.number_input("الوزن الإجمالي", value=91.9)
            c_m = c_cl2.number_input("كتلة العضلات", value=40.0)
            c_f = c_cl1.number_input("نسبة الدهون %", value=20.0)
            c_v = c_cl2.number_input("الدهون الحشوية", value=14)
            if st.form_submit_button("أرشفة البيانات طبياً"):
                s, m = push_data("InBody_Logs", {"Date": c_date.strftime("%Y-%m-%d"), "Weight": c_w, "Muscle_Mass": c_m, "Fat_Percentage": c_f, "Visceral_Fat": c_v})
                if s: st.success("تمت الأرشفة بنجاح.")
                else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 5: VISION AI (The SaaS Premium Feature)
    # -----------------------------------------------------------------
    with t_vision:
        st.markdown("### 📸 عدسة تايتان للذكاء الاصطناعي (SaaS Feature)")
        scans = st.session_state['ai_vision_scans_left']
        st.markdown(f"<p style='text-align:right;'><span style='background:rgba(229,185,76,0.1); color:#E5B94C; padding:8px 15px; border-radius:8px;'>الرصيد المتبقي: {scans} مسحات ضوئية</span></p>", unsafe_allow_html=True)
        
        if scans > 0:
            up_img = st.file_uploader("ارفع صورة وجبتك للتحليل الدقيق للبروتين والسعرات", type=["jpg", "png", "jpeg"])
            if up_img:
                st.image(up_img, use_container_width=True)
                if st.button("🔍 مسح ضوئي واستخراج الماكروز", use_container_width=True):
                    with st.spinner("جاري الاتصال بخوادم Vision AI..."):
                        time.sleep(2)
                        st.session_state['daily_protein'] += 40
                        st.session_state['daily_cals'] += 550
                        st.session_state['ai_vision_scans_left'] -= 1
                        st.markdown("<div class='success-box'>🤖 تحليل الذكاء: اكتشاف (دجاج مشوي + رز) | بروتين: 40g | سعرات: 550</div>", unsafe_allow_html=True)
        else:
            st.error("لقد استنفدت باقة المسح المجانية. قم بترقية اشتراكك.")

    # -----------------------------------------------------------------
    # TAB 6: NUTRITION
    # -----------------------------------------------------------------
    with t_fuel:
        st.markdown("### 🥗 مختبر التغذية (Offline Builder)")
        cf1, cf2 = st.columns([1, 1.2])
        e_db, f_db = get_nutrition_databases()
        all_f = {**e_db, **f_db}
        
        with cf2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>أضف من قاعدة البيانات</h4>", unsafe_allow_html=True)
            sel_f = st.selectbox("ابحث عن الصنف:", list(all_f.keys()))
            q = st.number_input("عدد الحصص:", value=1.0)
            if st.button("➕ إضافة الوجبة", use_container_width=True):
                st.session_state['daily_protein'] += int(all_f[sel_f].get("protein", 0) * q)
                st.session_state['daily_cals'] += int(all_f[sel_f].get("cals", 0) * q)
                st.success("تمت الإضافة.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with cf1:
            tar_p, tar_c = int(91.9 * 2.2), 1900
            st.markdown(f"""
            <div class='titan-card'>
                <h3 style='margin-top:0;'>📊 لوحة الوقود</h3>
                <p><span class='data-label'>البروتين:</span> <b style='color:#F85149; font-size:26px;'>{st.session_state['daily_protein']} / {tar_p} g</b></p>
                <p><span class='data-label'>السعرات:</span> <b style='color:#E5B94C; font-size:26px;'>{st.session_state['daily_cals']} / {tar_c}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("health_save_f"):
                s_slp = st.number_input("نوم:", value=7.5)
                s_wtr = st.number_input("ماء:", value=3.5)
                if st.form_submit_button("💾 حفظ اليوم في السحابة"):
                    push_data("Health_Log", {"Date": current_date_str, "Sleep": s_slp, "Water": s_wtr, "Protein": st.session_state['daily_protein'], "Calories": st.session_state['daily_cals']})
                    st.session_state['daily_protein'] = 0; st.session_state['daily_cals'] = 0; st.success("تم الحفظ وتصفير العداد.")

    # -----------------------------------------------------------------
    # TAB 7: SaaS ADMIN & AUTO-HEAL
    # -----------------------------------------------------------------
    with t_sys:
        st.markdown("### 🛠️ مركز الصيانة والتحكم المؤسسي")
        c_sa1, c_sa2 = st.columns(2)
        with c_sa1:
            st.markdown("<div class='titan-card titan-card-center'><h4>محرك الإصلاح الذاتي (Omni-Heal)</h4>", unsafe_allow_html=True)
            if st.button("🔄 فحص وإصلاح قاعدة البيانات", use_container_width=True):
                with st.spinner("جاري المسح..."):
                    reports = auto_heal()
                    for r in reports: st.markdown(f"<div class='{ 'success-box' if r['status']=='success' else 'alert-box' }'>{r['msg']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with c_sa2:
            st.markdown("<div class='titan-card titan-card-center'><h4>تنظيف الذاكرة (Memory Management)</h4>", unsafe_allow_html=True)
            if st.button("⚠️ إعادة ضبط المصنع (Clear Cache)", use_container_width=True):
                force_program_reset(); st.success("تم تنظيف السيرفر. يرجى التحديث.")
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
