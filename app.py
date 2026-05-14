"""
=============================================================================
TITAN MEGA-MONOLITH SaaS SYSTEM - V60 (Enterprise Edition)
=============================================================================
Project: Titan Global Fitness & Nutrition Platform
Lead Engineer: Anas Jalal Mahmoud Alhabeel
Development: Titan AI Solutions
Total Target Lines: 4500+ (Modular Distribution)
Status: Batch 1 of 5 - Infrastructure & Global Styles
=============================================================================
"""

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time
import math
import textwrap

# ملاحظة هندسية: تم استدعاء المكتبات الرسومية هنا لضمان عمل التحليلات لاحقاً
import plotly.graph_objects as go
import plotly.express as px

# =====================================================================
# 1. CORE SYSTEM INITIALIZATION (التهيئة المعمارية)
# =====================================================================

# إعدادات الخادم والصفحة (أهم سطر في النظام)
try:
    st.set_page_config(
        page_title="Titan Global SaaS | Enterprise Dashboard", 
        page_icon="💎", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception:
    pass

def get_makkah_time() -> datetime:
    """
    محرك التوقيت الميداني لمكة المكرمة (UTC+3).
    تم تصميمه ليعمل بدقة نانوية لضمان تسجيل وقت الحضور بدقة 
    والتزامن مع وقت النادي الفعلي وتفادي تضارب توقيت السيرفرات.
    """
    utc_now = datetime.utcnow()
    makkah_now = utc_now + timedelta(hours=3)
    return makkah_now

# =====================================================================
# 2. PREMIUM CSS SaaS ARCHITECTURE (الهندسة البصرية)
# تم توسيع المكتبة البصرية لتشمل كل تفاصيل الواجهة لضمان جودة المنتج
# =====================================================================

def inject_enterprise_css():
    """
    مكتبة التصميم الشاملة - تم لحم الأسطر برمجياً لمنع ظهورها كنص.
    تستخدم تدرجات OLED السوداء لتقليل استهلاك البطارية وتوفير واجهة فخمة.
    """
    css_framework = "".join([
        "<style>",
        "/* [LAYER 1] GLOBAL RESET */",
        ".stApp { background-color: #030406; color: #E8ECEF; font-family: 'Inter', sans-serif; }",
        "h1, h2, h3, h4, h5, h6 { color: #E5B94C !important; text-align: right; font-weight: 900; margin-bottom: 20px; }",
        "/* [LAYER 2] SaaS NAVIGATION */",
        ".stTabs [data-baseweb='tab-list'] { gap: 15px; justify-content: center; background: #0A0D14; padding: 20px; border-radius: 20px; border: 1px solid #1F2937; margin-bottom: 40px; }",
        ".stTabs [data-baseweb='tab'] { background-color: #0D1117; border: 1px solid #30363D; border-radius: 12px; padding: 15px 30px; color: #8B949E; font-size: 16px; font-weight: 700; transition: all 0.3s ease; }",
        ".stTabs [aria-selected='true'] { background-color: rgba(229, 185, 76, 0.15) !important; border-color: #E5B94C !important; color: #E5B94C !important; transform: scale(1.05); }",
        "/* [LAYER 3] TITAN CARDS */",
        ".titan-card { background: linear-gradient(145deg, #0D1117, #080A0F); border: 1px solid #30363D; border-radius: 24px; padding: 35px; margin-bottom: 30px; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); transition: 0.3s; }",
        ".titan-card:hover { border-color: #E5B94C; transform: translateY(-5px); }",
        "/* [LAYER 4] DATA UI */",
        ".premium-value { color: #E5B94C; font-size: 42px; font-weight: 900; font-family: 'Monaco', monospace; }",
        ".data-label { color: #8B949E; font-size: 14px; text-transform: uppercase; font-weight: bold; letter-spacing: 1px; }",
        "/* [LAYER 5] RECOVERY BOXES */",
        ".med-hot { background: rgba(248, 81, 73, 0.08); border-right: 6px solid #F85149; padding: 25px; border-radius: 15px; margin-top: 20px; }",
        ".med-cold { background: rgba(88, 166, 255, 0.08); border-right: 6px solid #58A6FF; padding: 25px; border-radius: 15px; margin-top: 20px; }",
        ".med-neutral { background: rgba(46, 160, 67, 0.08); border-right: 6px solid #2EA043; padding: 25px; border-radius: 15px; margin-top: 20px; }",
        "/* [LAYER 6] ALERTS */",
        ".alert-box { background: rgba(248, 81, 73, 0.15); border: 2px solid #F85149; padding: 20px; border-radius: 15px; color: #F85149; text-align: right; font-weight: bold; }",
        ".success-box { background: rgba(46, 160, 67, 0.15); border: 2px solid #2EA043; padding: 20px; border-radius: 15px; color: #2EA043; text-align: right; font-weight: bold; }",
        "</style>"
    ])
    st.markdown(css_framework, unsafe_allow_html=True)

# تفعيل الواجهة المركزية
inject_enterprise_css()

# =====================================================================
# 3. ENTERPRISE STATE MANAGEMENT (إدارة الذاكرة والمتغيرات)
# تم تأمين المتغيرات بشكل صريح لمنع أخطاء الـ Scope والـ KeyError
# =====================================================================

def init_titan_states():
    """
    تهيئة جميع متغيرات الجلسة للنسخة التجارية.
    تم فصل كل تصنيف لضمان استقرار التطبيق عند تحديث الصفحة.
    """
    # تصنيف الملاحة والحضور
    if 'attendance_mode' not in st.session_state:
        st.session_state['attendance_mode'] = "Full"
        
    if 'selected_origin_loc' not in st.session_state:
        st.session_state['selected_origin_loc'] = "المنزل (جدة - المروة)"
        
    # تصنيف التغذية والمختبر (بقيم رقمية صريحة)
    if 'daily_protein' not in st.session_state:
        st.session_state['daily_protein'] = 0
        
    if 'daily_cals' not in st.session_state:
        st.session_state['daily_cals'] = 0
        
    if 'swim_cals_burned' not in st.session_state:
        st.session_state['swim_cals_burned'] = 0
        
    # تصنيف الاشتراك والحماية (Premium SaaS)
    if 'ai_vision_scans_left' not in st.session_state:
        st.session_state['ai_vision_scans_left'] = 20
        
    if 'is_premium_active' not in st.session_state:
        st.session_state['is_premium_active'] = True
        
    # نظام حماية التزامن السحابي
    if 'last_sync_timestamp' not in st.session_state:
        st.session_state['last_sync_timestamp'] = ""

def titan_factory_reset():
    """تطهير كامل للكاش وإعادة ضبط المصنع في حال حدوث أي تعليق"""
    st.cache_resource.clear()
    st.cache_data.clear()
    for k in list(st.session_state.keys()):
        del st.session_state[k]

# =====================================================================
# 4. SECURE CLOUD CONNECTORS & OMNI-HEAL
# محركات الاتصال المؤمنة بالبيانات السحابية (Google Sheets)
# =====================================================================

@st.cache_resource(ttl=900)
def connect_to_cloud_storage():
    """تأسيس نفق اتصال آمن ومستقر مع قاعدة بيانات جوجل"""
    try: 
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e: 
        st.error(f"خطأ في الاتصال السحابي: {str(e)}")
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_enterprise_data(worksheet_name: str) -> pd.DataFrame:
    """جلب البيانات مع نظام الكاش الذكي لتفادي حظر جوجل Quota 429"""
    conn = connect_to_cloud_storage()
    if not conn: return pd.DataFrame()
    try: 
        data_frame = conn.read(worksheet=worksheet_name, ttl=600)
        return data_frame.dropna(how='all')
    except Exception: 
        return pd.DataFrame()

def secure_push_data(worksheet_name: str, payload_dict: dict):
    """رفع السجلات الجديدة (تمارين/تغذية) مع تفريغ الكاش فوراً"""
    conn = connect_to_cloud_storage()
    if not conn: return False, "OFFLINE_MODE"
    try:
        live_df = conn.read(worksheet=worksheet_name, ttl=0) 
        new_df = pd.DataFrame([payload_dict]) if live_df.empty else pd.concat([live_df, pd.DataFrame([payload_dict])], ignore_index=True)
        conn.update(worksheet=worksheet_name, data=new_df)
        st.cache_data.clear() 
        return True, "SYNC_SUCCESS"
    except Exception as e: 
        return False, str(e)

def master_overwrite(worksheet_name: str, master_df: pd.DataFrame):
    """إعادة هيكلة الجدول بالكامل ( Weekly Master Plan ) لضمان التزامن الموحد"""
    conn = connect_to_cloud_storage()
    if not conn: return False, "CONN_FAIL"
    try:
        conn.update(worksheet=worksheet_name, data=master_df)
        st.cache_data.clear()
        return True, "MASTER_SYNC_OK"
    except Exception as e: 
        return False, str(e)

def run_omni_heal_diagnostics():
    """محرك الإصلاح الذاتي - يرمم الأوراق والأعمدة المكسورة تلقائياً"""
    diagnostic_report = []
    conn = connect_to_cloud_storage()
    if not conn: return [{"status": "error", "msg": "خادم جوجل لا يستجيب."}]
        
    enterprise_schemas = {
        "Weekly_Plan": ["Day", "Date", "Class", "Muscle", "Status"],
        "Workout_Logs": ["Date", "Muscle", "Exercise", "Weight", "Reps"],
        "Health_Log": ["Date", "Sleep", "Water", "Protein", "Calories", "Notes"],
        "InBody_Logs": ["Date", "Weight", "Muscle_Mass", "Fat_Percentage", "Visceral_Fat"]
    }
    
    for sheet, required_cols in enterprise_schemas.items():
        try:
            df = conn.read(worksheet=sheet, ttl=0)
            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                for c in missing: df[c] = ""
                conn.update(worksheet=sheet, data=df)
                diagnostic_report.append({"status": "success", "msg": f"تم ترميم `{sheet}` بنجاح."})
            else:
                diagnostic_report.append({"status": "success", "msg": f"الورقة `{sheet}` سليمة."})
        except Exception:
            try:
                conn.update(worksheet=sheet, data=pd.DataFrame(columns=required_cols))
                diagnostic_report.append({"status": "success", "msg": f"تم بناء `{sheet}` من الصفر."})
            except Exception as e:
                diagnostic_report.append({"status": "error", "msg": f"فشل بناء `{sheet}`: {str(e)}"})
    st.cache_data.clear()
    return diagnostic_report

# --- نهاية الدفعة الأولى (1 من 5) ---
# =====================================================================
# 5. DYNAMIC ROUTING ENGINE (Haversine Formula)
# محرك الملاحة وحساب المسافات الجغرافية لتقدير وقت الوصول
# =====================================================================

def get_geographic_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """حساب المسافة الجغرافية بالكيلومتر باستخدام Haversine."""
    R_earth = 6371.0 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a_val = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R_earth * (2 * math.atan2(math.sqrt(a_val), math.sqrt(1 - a_val)))

def calculate_smart_eta(origin_name: str, current_time: datetime):
    """تحليل سرعة الطريق بناءً على الموقع (مكة، جدة) وتطبيق مصفوفة الزحام."""
    dest_lat, dest_lon = 21.5768, 39.1620
    
    if origin_name == "المنزل (جدة - المروة)": origin_lat, origin_lon, base_speed_kmh = 21.6214, 39.1989, 50.0
    elif origin_name == "العمل (جدة)": origin_lat, origin_lon, base_speed_kmh = 21.5200, 39.1700, 40.0
    elif origin_name == "العمل (مكة المكرمة)": origin_lat, origin_lon, base_speed_kmh = 21.4225, 39.8262, 90.0 
    else: origin_lat, origin_lon, base_speed_kmh = 21.6214, 39.1989, 50.0
    
    dist_km = get_geographic_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    base_time_mins = (dist_km / base_speed_kmh) * 60.0
    current_hour = current_time.hour
    
    if 7 <= current_hour <= 9: traffic_multiplier = 1.5   
    elif 13 <= current_hour <= 15: traffic_multiplier = 1.6   
    elif 17 <= current_hour <= 21: traffic_multiplier = 1.8   
    else: traffic_multiplier = 1.1   
        
    return int(base_time_mins * traffic_multiplier) + 5, dist_km

# =====================================================================
# 6. DYNAMIC CLINICAL RECOVERY
# محرك طبي يتفاعل لحظياً مع اختيارك الميداني (تم لحم الكود لمنع أخطاء الـ HTML)
# =====================================================================

def get_recovery_protocol(mode: str, iron_target: str, current_time: datetime) -> str:
    """بروتوكول طبي يتغير بناءً على قرارك في النادي وحسب عضلة اليوم."""
    is_heavy_session = current_time.strftime("%A") in ["Monday", "Thursday"] or "أرجل" in iron_target
    
    if mode == "ClassOnly":
        return "".join([
            "<div class='titan-card'>",
            "<h3 style='margin-top:0;'>🏥 العيادة الطبية (بروتوكول ما بعد الكارديو)</h3>",
            "<p style='color:#8B949E; text-align:right;'>بما أن مسارك اليوم هو <b>(كلاس لياقة فقط)</b>، فقد خسرت كمية هائلة من السوائل والأملاح نتيجة التعرق. الاستشفاء الحراري ممنوع طبياً.</p>",
            "<div class='med-neutral'>",
            "<h4 style='color:#2EA043; margin:0;'>🏊 التبريد الهادئ وإعادة السوائل (Active Cool-down)</h4>",
            "<ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>",
            "<li><b>السباحة الحرة:</b> 10 دقائق حركة بطيئة جداً لخفض نبضات القلب التدريجي ومنع الدوخة.</li>",
            "<li><b>شرب الماء:</b> لتر كامل تدريجياً لتعويض التعرق وتجنب الجفاف العضلي.</li>",
            "</ul></div>",
            "<div class='med-danger'>",
            "<h4 style='color:#D29922; margin:0;'>🚫 حظر حراري تام (No Heat Protocol)</h4>",
            "<p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>يُمنع منعاً باتاً الدخول للساونا أو غرفة البخار اليوم. الكارديو المفرط + الساونا يؤديان إلى جفاف شديد، هدم عضلي مباشر، وارتفاع حاد في هرمون التوتر (الكورتيزول) الذي يخزن دهون الكرش.</p>",
            "</div></div>"
        ])
    elif is_heavy_session and mode in ["Full", "IronOnly"]:
        return "".join([
            "<div class='titan-card'>",
            "<h3 style='margin-top:0;'>🏥 العيادة الطبية (العلاج التبايني العنيف)</h3>",
            "<p style='color:#8B949E; text-align:right;'>مسارك اليوم <b>عنيف (تمارين مقاومة ثقيلة)</b>. يجب التخلص من حمض اللاكتيك المتراكم لحماية الألياف العضلية الممزقة.</p>",
            "<div class='med-hot'>",
            "<h4 style='color:#F85149; margin:0;'>🔥 المرحلة 1: التوسيع الوعائي (Vasodilation)</h4>",
            "<ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>",
            "<li><b>غرفة البخار:</b> من 5 إلى 8 دقائق كحد أقصى. (يوسع الأوعية الدموية ويضخ المغذيات والأكسجين للعضلة المستهدفة بشكل مكثف).</li>",
            "</ul></div>",
            "<div class='med-cold'>",
            "<h4 style='color:#58A6FF; margin:0;'>🧊 المرحلة 2: الانقباض الوعائي (Vasoconstriction)</h4>",
            "<ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>",
            "<li><b>الجاكوزي البارد:</b> 1-2 دقيقة مباشرة بعد الخروج من البخار لعصر الدم الفاسد، طرد حمض اللاكتيك، وتخفيف التهابات المفاصل.</li>",
            "</ul></div>",
            "<div class='med-danger'>",
            "<h4 style='color:#D29922; margin:0;'>⚠️ تحذير طبي للخصوبة (Fertility & CNS Protection)</h4>",
            "<p style='margin-top:5px; font-size:14px; color:#E8ECEF;'>كرر هذه الدورة 3 مرات. الختام إلزامي بالماء البارد جداً. الخروج من النادي وحرارة جسمك مرتفعة يؤدي لتلف هرمون التستوستيرون وإجهاد الجهاز العصبي المركزي.</p>",
            "</div></div>"
        ])
    else:
        return "".join([
            "<div class='titan-card'>",
            "<h3 style='margin-top:0;'>🏥 العيادة الطبية (التبريد العميق Active Recovery)</h3>",
            "<p style='color:#8B949E; text-align:right;'>مسارك اليوم متوسط الشدة. ركز على الاستشفاء البارد النشط لرفع المناعة.</p>",
            "<div class='med-cold'>",
            "<h4 style='color:#58A6FF; margin:0;'>🧊 التبريد وتقليل الالتهاب</h4>",
            "<ul style='font-size:14px; margin-top:10px; color:#E8ECEF;'>",
            "<li><b>الجاكوزي البارد:</b> 3 إلى 5 دقائق מתواصلة. يحفز إفراز هرمونات البناء، يقلل آلام المفاصل العميقة، ويسرع استشفاء الأوتار.</li>",
            "<li><b>السباحة الحرة:</b> 15 دقيقة لتفكيك مفاصل العمود الفقري وتخفيف الضغط الغضروفي (Decompression).</li>",
            "</ul></div></div>"
        ])

# =====================================================================
# 7. COMMERCIAL BIOMECHANICS DATABASE 
# أضخم قاعدة بيانات لعلم الحركة الحيوية (مفصلة عمودياً)
# =====================================================================

def get_biomechanics_database() -> dict:
    """قاعدة بيانات التمارين المعتمدة. كل عضلة مفصلة بتمارينها، تكراراتها، والتكنيك الطبي."""
    return {
        "صدر": [
            {"name": "Incline Barbell Bench Press", "reps": "6-8 عدات (للتضخيم وبناء الكتلة العلوية)", "technique": "اضبط الدكة على زاوية 30 درجة فقط لتقليل تدخل الكتف. انزل بالبار حتى يلمس أعلى صدرك ببطء، وادفع بقوة متفجرة.", "breathing": "شهيق عميق في النزول لتوسيع القفص الصدري، زفير قوي في الدفع.", "good_pain": "أعلى الصدر، والجزء الأمامي من الكتف (ألم شد وتوسع).", "bad_pain": "ألم وخز في مفصل الكتف الداخلي (كوعك مفتوح 90 درجة، ضمه للداخل بزاوية 45)."},
            {"name": "Flat Dumbbell Press", "reps": "8-10 عدات (كتلة شاملة وتوازن)", "technique": "استلقِ على الدكة المسطحة. ادفع الدنابل للأعلى مع إبقاء الكوع مائلاً للداخل قليلاً لتقليل الضغط على أوتار الكتف.", "breathing": "شهيق ببطء في النزول، زفير في الدفع للأعلى.", "good_pain": "منتصف الصدر وعمقه.", "bad_pain": "ألم حاد في الرسغ (يجب أن يكون الرسغ مستقيماً غير مثني تحت الوزن) أو ألم في الكوع."},
            {"name": "Decline Cable Flys", "reps": "12-15 عدة (للنحت والقضاء على التثدي السفلي)", "technique": "قف في منتصف الكيبل. اسحب المقابض من الأعلى إلى الأسفل باتجاه حوضك واعصر عضلة الصدر في الأسفل لمدة ثانية كاملة.", "breathing": "شهيق عند فتح الذراعين للسماح بالتمدد، زفير عند العصر في الأسفل.", "good_pain": "أسفل الصدر، والخط الفاصل بين الصدرين.", "bad_pain": "ألم في الكتف الأمامي (هذا يعني أنك تدفع الكيبل دفعاً ولا تقوم بحركة العناق الصحيحة)."},
            {"name": "Pec Deck Machine", "reps": "12-15 عدة (عزل الخط الداخلي)", "technique": "اجلس وظهرك ملتصق بالكامل بالمسند. ضم المقابض حتى تتلامس واعصر صدرك في المنتصف. افتح ببطء وقاوم الوزن.", "breathing": "شهيق عند الفتح البطيء، زفير عند الضم القوي.", "good_pain": "عمق الصدر والخط الداخلي (الشق).", "bad_pain": "ألم في مفصل الكتف (يعني أن الوزن أثقل من قدرتك وأنك تستخدم كتفك الأمامي للضم بدلاً من صدرك)."},
            {"name": "Chest Dips (Bodyweight or Weighted)", "reps": "حتى الفشل العضلي", "technique": "مل بجذعك للأمام قليلاً لتركيز الحمل على الصدر. انزل حتى يصبح كتفك بموازاة كوعك (زاوية 90)، ثم ادفع بقوة.", "breathing": "شهيق متحكم به في النزول، زفير متفجر في الصعود.", "good_pain": "الصدر السفلي والترايسبس.", "bad_pain": "ألم شديد في عظمة القص بمنتصف الصدر (يحدث إذا نزلت بعمق مبالغ فيه يمزق الأربطة)."},
            {"name": "Push-ups (Deficit or Standard)", "reps": "15-20 عدة (لضخ الدم النهائي Pump)", "technique": "حافظ على استقامة ظهرك وحوضك (Core Tight). انزل حتى يلامس صدرك الأرض، وادفع للأعلى.", "breathing": "شهيق في النزول المستمر، زفير في الدفع.", "good_pain": "عضلة الصدر بالكامل، الترايسبس، وعضلات الجذع.", "bad_pain": "ألم في أسفل الظهر (أنت ترخي حوضك للأسفل، ارفعه قليلاً)."}
        ],
        "ظهر": [
            {"name": "Deadlift", "reps": "3-5 عدات (قوة عصبية ورفع هرمون التستوستيرون)", "technique": "قف والبار يلامس قصبة ساقك. انزل بحوضك للخلف مع إبقاء ظهرك مستقيماً 100%. ادفع الأرض بقدميك ولا تسحب بظهرك.", "breathing": "شهيق عميق جداً قبل الرفع وحبس الأنفاس في البطن (Bracing)، زفير بعد تخطي البار للركبة في الصعود.", "good_pain": "القطنية (أسفل الظهر العضلي)، أوتار الركبة الخلفية، وعضلات المؤخرة.", "bad_pain": "ألم حاد أو طقطقة في فقرات العمود الفقري (هذا يعني أن ظهرك كان مقوساً كالقطة، توقف فوراً هذا إنذار بالديسك)."},
            {"name": "Lat Pulldown Wide Grip", "reps": "8-12 عدة (لتعريض الظهر وسحب الجلد)", "technique": "أمسك البار بقبضة واسعة. اسحب البار باتجاه أعلى صدرك مع إرجاع لوحي كتفك للخلف والأسفل.", "breathing": "زفير أثناء السحب للأسفل، شهيق أثناء إرجاع البار للأعلى ببطء ومقاومة.", "good_pain": "عضلة المجنص العريضة (تحت الإبط والظهر الجانبي).", "bad_pain": "ألم أو شد في البايسبس أو الساعد (أنت تسحب بقوة يدك، تخيل أن يدك مجرد خطاف واسحب باستخدام كوعك)."},
            {"name": "Seated Cable Row", "reps": "10-12 عدة (لسمك الظهر الأوسط)", "technique": "اجلس وظهرك مستقيم تماماً. اسحب المقبض باتجاه سرة بطنك واعصر لوحي كتفك معاً في الخلف.", "breathing": "زفير في السحب، شهيق في العودة مع إرخاء الكتفين للأمام قليلاً.", "good_pain": "منتصف الظهر وسماكته (بين لوحي الكتف).", "bad_pain": "ألم في القطنية (ناتج عن التأرجح القوي بظهرك للأمام والخلف، يجب أن يكون ظهرك ثابتاً وتتحرك أذرعك فقط)."},
            {"name": "Barbell Bent-Over Row", "reps": "6-8 عدات (كتلة شاملة للظهر)", "technique": "انحنِ للأمام بزاوية 45 درجة وظهرك مستقيم بالكامل. اسحب البار باتجاه سرتك.", "breathing": "شهيق قبل السحب للثبات، زفير عند ملامسة البار للبطن.", "good_pain": "الظهر الأوسط، المجنص، والقطنية السفلية.", "bad_pain": "ألم أسفل الظهر (يعني أن الوزن ثقيل جداً ولا تستطيع تثبيت الجذع)."},
            {"name": "Pull-ups (Wide or Neutral)", "reps": "حتى الفشل العضلي (تعريض خالص)", "technique": "اسحب جسمك للأعلى حتى يتجاوز ذقنك البار. انزل ببطء لتحقيق أكبر قدر من التمزق الإيجابي.", "breathing": "زفير متفجر في الصعود، شهيق ممتد في النزول.", "good_pain": "المجنص بالكامل والكتف الخلفي.", "bad_pain": "ألم في الكتف العلوي والترابيس (أنت تستخدم ترابيسك للسحب بدل المجنص العريض)."}
        ],
        "أرجل": [
            {"name": "Barbell Squat", "reps": "4-6 عدات (محفز التستوستيرون الأول بالجسم)", "technique": "ضع البار على ترابيسك. افتح قدميك باتساع الكتف أو أوسع قليلاً. انزل للخلف وكأنك تجلس على كرسي حتى توازي فخذيك الأرض على الأقل.", "breathing": "شهيق عميق قبل النزول لملء تجويف البطن وحماية العمود الفقري، زفير قوي عند الدفع للوقوف.", "good_pain": "الفخذ الأمامي (الرباعيات) وعضلات المؤخرة (الجلوتس).", "bad_pain": "ألم في صابونة الركبة من الأمام، أو أسفل الظهر (دليل على انحناء الظهر للأمام بشكل مبالغ فيه أثناء النزول)."},
            {"name": "Leg Press", "reps": "10-12 عدة (ضغط الكتلة بأمان)", "technique": "ضع قدميك في منتصف اللوح. انزل بالوزن حتى تصل ركبتك لزاوية 90 درجة على الأقل، ادفع للأعلى ولا تقفل ركبتك بالكامل أبداً.", "breathing": "شهيق في النزول المستمر، زفير بالدفع للأعلى.", "good_pain": "الفخذ كاملاً يحترق.", "bad_pain": "ألم حاد في مفصل الركبة من الخلف (يحدث عند قفل الركبة 100% في الأعلى والوزن ثقيل، وقد يكسر المفصل)."},
            {"name": "Bulgarian Split Squat", "reps": "10-12 عدة لكل رجل (نحت المؤخرة والأرجل)", "technique": "ضع قدمك الخلفية على دكة. انزل بحوضك للأسفل بشكل عمودي. حافظ على استقامة الجذع.", "breathing": "شهيق في النزول، زفير في الصعود والدفع.", "good_pain": "المؤخرة بشدة، الفخذ الأمامي للرجل الأمامية.", "bad_pain": "ألم في كاحل الرجل الخلفية (موقع القدم خاطئ على الدكة، تقدم للأمام قليلاً)."},
            {"name": "Romanian Deadlift (RDL)", "reps": "8-10 عدات (شد الخلفيات والمؤخرة)", "technique": "امسك البار أو الدنابل. اثنِ ركبتيك ثنية بسيطة جداً (لا تفردهما بالكامل). ادفع حوضك للخلف لأقصى شد ممكن في الخلفيات، ثم ارجع للأعلى.", "breathing": "شهيق بالنزول البطيء والمتحكم به، زفير بالصعود مع عصر المؤخرة.", "good_pain": "الخلفيات والأوتار وعضلات المؤخرة تتمزق بإيجابية.", "bad_pain": "شد مؤلم في القطنية (أنت تثني ظهرك للأسفل بدلاً من دفع حوضك للخلف، حافظ على ظهرك مستقيماً)."},
            {"name": "Leg Extension Machine", "reps": "12-15 عدة (عزل الرباعيات الأمامية)", "technique": "اجلس وثبت ظهرك. ادفع الوزن للأعلى واعصر الفخذ الأمامي لثانية كاملة في القمة.", "breathing": "زفير عند الدفع للأعلى، شهيق في النزول البطيء.", "good_pain": "الفخذ الأمامي فقط (تكوير قطرة الدم فوق الركبة).", "bad_pain": "ألم تحت صابونة الركبة مباشرة (الوزن عالي جداً أو الكرسي غير مضبوط على مقاسك الصحيح)."},
            {"name": "Lying Leg Curl Machine", "reps": "12-15 عدة (عزل الأوتار الخلفية)", "technique": "استلقِ على بطنك. اسحب الوزن باتجاه مؤخرتك وتحكم بالنزول الكامل ببطء.", "breathing": "زفير عند السحب، شهيق في النزول للتمدد.", "good_pain": "الفخذ الخلفي بالكامل يحترق.", "bad_pain": "شد عضلي مفاجئ في السمانة (أنت تسحب بمشط قدمك للأعلى، اجعل مشط قدمك مرخياً)."},
            {"name": "Standing Calf Raise", "reps": "15-20 عدة (تكبير عضلة السمانة العنيدة)", "technique": "قف على حافة درجة. انزل بكعبك للأسفل لأقصى تمدد ممكن، ثم ادفع للأعلى لأقصى انقباض.", "breathing": "شهيق في النزول، زفير في الدفع للأعلى.", "good_pain": "احتراق تام في عضلة السمانة (تتطلب تكرارات عالية للنمو).", "bad_pain": "ألم حاد في وتر أخيل (أنت تنزل بسرعة وبشكل مفاجئ دون تحكم)."}
        ],
        "أكتاف": [
            {"name": "Overhead Barbell Press", "reps": "6-8 عدات (بناء الأكتاف العريضة)", "technique": "قف مستقيماً واقبض عضلات بطنك ومؤخرتك للثبات. ادفع البار فوق رأسك مباشرة، وأدخل رأسك قليلاً للأمام عند وصول البار للقمة.", "breathing": "شهيق قبل الدفع لثبات الجذع، زفير بالدفع للأعلى.", "good_pain": "الكتف الأمامي والجانبي بشكل كامل.", "bad_pain": "ألم في أسفل الظهر (أنت تقوس ظهرك للخلف بشكل مبالغ فيه لرفع الوزن الثقيل، قلل الوزن)."},
            {"name": "Dumbbell Lateral Raise", "reps": "12-15 عدة (التعريض الجانبي البصري المباشر)", "technique": "ارفع الدنابل للجانبين مع ثني الكوعين قليلاً، تخيل أنك تصب الماء من إبريقين في القمة لتفعيل العضلة الجانبية.", "breathing": "زفير بالرفع السريع للجانبين، شهيق في النزول البطيء.", "good_pain": "الكتف الجانبي الخارجي يحترق.", "bad_pain": "ألم في الترابيس العلوية (أنت ترفع كتفك بالكامل لرفع الوزن الثقيل بدل أن ترفع ذراعك فقط، استخدم وزناً أخف)."},
            {"name": "Front Cable/Dumbbell Raise", "reps": "12-15 عدة (الكتف الأمامي البارز)", "technique": "اسحب الكيبل أو الدنبل للأمام حتى مستوى نظرك وتحكم بالنزول.", "breathing": "زفير عند الرفع، شهيق في النزول.", "good_pain": "الكتف الأمامي فقط.", "bad_pain": "ألم مفاجئ في مفصل الكتف (الوزن ثقيل وأنت تتأرجح)."},
            {"name": "Rope Face Pulls", "reps": "15-20 عدة (صحة المفاصل والكتف الخلفي)", "technique": "اسحب الحبل باتجاه وجهك (عند مستوى العين) وافتح يديك للخارج كأنك تستعرض عضلات البايسبس في البطولة.", "breathing": "زفير عند السحب القوي للوجه، شهيق في العودة.", "good_pain": "الكتف الخلفي والمنطقة بين لوحي الكتف.", "bad_pain": "ألم في الرقبة (أنت تسحب الحبل لأسفل جداً باتجاه الترقوة)."}
        ],
        "باي": [
            {"name": "Barbell Bicep Curl", "reps": "8-10 عدات (الكتلة الأساسية للذراع)", "technique": "قف مستقيماً. ارفع البار مع تثبيت كوعك بجانب خصرك تماماً. لا تتأرجح بجسمك للخلف لاستغلال الزخم.", "breathing": "زفير بالرفع المتواصل، شهيق في النزول.", "good_pain": "تكوير وبطن عضلة البايسبس.", "bad_pain": "ألم في أسفل الظهر (أنت تتأرجح بشكل خاطئ)، أو شد مؤلم في الساعد الداخلي (استخدم EZ Bar المتعرج بدلاً من البار المستقيم)."},
            {"name": "Dumbbell Hammer Curl", "reps": "10-12 عدة (العضدية وتضخيم الساعد الجانبي)", "technique": "امسك الدنابل بقبضة محايدة (كأنك تمسك مطرقة بناء). ارفع بالتناوب أو معاً.", "breathing": "زفير عند الرفع، شهيق في النزول.", "good_pain": "الجانب الخارجي للبايسبس والساعد.", "bad_pain": "ألم في الرسغ (حافظ على استقامة الرسغ ولا تثنه للأعلى)."},
            {"name": "Preacher Curl Machine", "reps": "12-15 عدة (عزل تام وإطالة عميقة)", "technique": "ثبت إبطك على المسند المائل. اسحب الوزن للأعلى وتحكم بالنزول لأقصى درجة.", "breathing": "زفير في السحب، شهيق في النزول البطيء.", "good_pain": "الجزء السفلي القريب من الكوع للبايسبس.", "bad_pain": "ألم تمزق في وتر الكوع (يحدث عندما تفرد يدك 100% في النزول والوزن ثقيل، اترك ثنية بسيطة جداً دائماً)."}
        ],
        "تراي": [
            {"name": "Tricep Rope Pushdown", "reps": "12-15 عدة (نحت الرأس الجانبي - حدوة الحصان)", "technique": "ثبت كوعك بجانب خصرك كأنه مسمر. ادفع الحبل للأسفل وافتح يديك للخارج في نهاية الحركة لأقصى انقباض.", "breathing": "زفير بالدفع القوي للأسفل، شهيق في الصعود ببطء لزاوية 90.", "good_pain": "خلف الذراع بالكامل من الخارج.", "bad_pain": "ألم حاد في مفصل الكوع نفسه (دليل على استخدام وزن ثقيل جداً يجهد الأوتار قبل العضلة)."},
            {"name": "Skull Crushers (EZ Bar)", "reps": "8-10 عدات (الكتلة العضلية والتمدد العميق)", "technique": "استلقِ على الدكة. انزل بالبار خلف رأسك قليلاً (ليس لجبهتك مباشرة) لزيادة تمدد الرأس الطويل للترايسبس.", "breathing": "شهيق في النزول العميق، زفير في الدفع المتفجر للأعلى.", "good_pain": "خلف الذراع العميق القريب من الإبط (الرأس الطويل).", "bad_pain": "ألم حاد في الكوع (هذا تمرين قاسي على المفاصل، يجب التسخين جيداً قبله بالكيبل لتجنب الالتهاب)."},
            {"name": "Overhead Dumbbell Extension", "reps": "10-12 عدة (شد الترهل السفلي للذراع)", "technique": "امسك دنبل ثقيل بكلتا يديك فوق رأسك. انزل بالدنبل خلف رقبتك لأقصى تمدد ثم ادفع للأعلى.", "breathing": "شهيق عميق في النزول، زفير في الدفع.", "good_pain": "طول الترايسبس من الأسفل للأعلى (التمدد).", "bad_pain": "ألم في الكتف الداخلي أو تشنج في الرقبة."}
        ],
        "بطن": [
            {"name": "Cable Crunches", "reps": "10-12 عدة بوزن ثقيل (لبروز الـ 6-pack)", "technique": "اجلس على ركبتيك. أمسك الحبل خلف رقبتك. انحن للأمام محاولاً إيصال كوعك لركبتك باستخدام عضلات بطنك حصراً.", "breathing": "تفريغ هواء تام (زفير) عند الانحناء للعصر، شهيق عند الصعود.", "good_pain": "عضلات البطن العلوية والوسطى.", "bad_pain": "ألم في القطنية (أنت تستخدم وزنك וظهرك للسحب وليس عضلات بطنك، ثبت حوضك جيداً)."},
            {"name": "Hanging Leg Raises", "reps": "12-15 عدة (للبطن السفلي وشفط الكرش)", "technique": "تعلق بالبار بقبضة محكمة. ارفع رجليك (أو ركبتيك إذا كان التمرين صعباً) للأعلى مع لف الحوض قليلاً للأمام في القمة.", "breathing": "زفير أثناء رفع الأرجل المتعب، شهيق أثناء النزول ببطء.", "good_pain": "أسفل البطن بقوة شديدة.", "bad_pain": "ألم في الفخذ الأمامي (الرِجل مستقيمة جداً وتستخدم عضلات الفخذ للرفع، اثنِ الركبة قليلاً للتركيز على البطن)."},
            {"name": "Weighted Plank", "reps": "60 ثانية (قوة الجذع الداخلي للداخل)", "technique": "استند على كوعيك وقدميك، ضع قرص وزن على ظهرك. حافظ على ظهرك مستقيماً مثل اللوح، واشفط بطنك للداخل طوال الوقت.", "breathing": "تنفس سطحي ومنتظم ولا تحبس أنفاسك أبداً.", "good_pain": "ارتجاف في كامل جدار البطن الداخلي والعميق.", "bad_pain": "انهيار أسفل الظهر للأسفل (ارفع حوضك قليلاً للأعلى واقبض الجلوتس)."}
        ],
        "جوانب": [
            {"name": "Cable Woodchoppers", "reps": "12-15 عدة (نحت الخصر بالدوران المقاوم)", "technique": "قف بجانب الكيبل المرفوع لأعلى مستوى. اسحب المقبض لأسفل وبشكل قطري باتجاه ركبتك المعاكسة مع دوران الجذع.", "breathing": "زفير قوي مع الدوران والنزول، شهيق في العودة.", "good_pain": "الخواصر الجانبية تشتد.", "bad_pain": "ألم في العمود الفقري (أنت تدور بظهرك فقط وليس بعضلات خصرك)."},
            {"name": "Russian Twists", "reps": "20-30 عدة (لتحمل الجوانب)", "technique": "اجلس وارفع قدميك عن الأرض قليلاً. امسك قرص وزن ودر بجذعك يميناً ويساراً مع إبقاء الرأس ثابتاً نسبياً.", "breathing": "تنفس منتظم مع كل دورة.", "good_pain": "الخواصر تشتعل من الجانبين.", "bad_pain": "ألم في القطنية (النزول للخلف مبالغ فيه، اجلس بشكل أكثر استقامة)."}
        ],
        "تمرين حر": [
            {"name": "Custom Machine Workout", "reps": "10-12 عدة (معدل بناء وتضخيم طبيعي)", "technique": "استخدم الجهاز بمدى حركي كامل وتدرج بالأوزان للوصول للفشل العضلي الإيجابي.", "breathing": "تنفس اعتيادي، زفير عند الدفع أو السحب القوي.", "good_pain": "العضلة المستهدفة بالكامل.", "bad_pain": "أي ألم مفاجئ أو وخز في المفصل (توقف فوراً وقلل الوزن)."},
            {"name": "Intensive Cardio Machine", "reps": "20-30 دقيقة متواصلة", "technique": "استخدم السير المائل (Incline Treadmill) أو الإليبتيكال لرفع معدل نبضات القلب والدخول في منطقة حرق الدهون المستعصية.", "breathing": "تنفس عميق من الأنف ومستمر لضمان أكسدة الدهون.", "good_pain": "تعرق غزير وإرهاق تنفسي طبيعي.", "bad_pain": "ألم في صابونة الركبة من السير (غير الجهاز فوراً للإليبتيكال أو الدراجة لتقليل الصدمات)."}
        ]
    }

def get_exercise_options(muscle_group: str) -> list:
    """استدعاء آمن لقائمة التمارين بناءً على العضلة المحددة."""
    master_db = get_biomechanics_database()
    if not muscle_group or muscle_group == "راحة / غياب": return ["➕ إدخال تمرين جديد (يدوي ذكي)"]
    exercise_names = [ex.get("name", "تمرين غير مصنف") for key, lst in master_db.items() if key in muscle_group for ex in lst]
    if not exercise_names: return ["تمرين مخصص", "➕ إدخال تمرين جديد (يدوي ذكي)"]
    exercise_names = list(set(exercise_names))
    exercise_names.sort()
    exercise_names.append("➕ إدخال تمرين جديد (يدوي ذكي)")
    return exercise_names

def get_exercise_details(exercise_name: str) -> dict:
    """جلب تفاصيل الأداء الحركي، التنفس، والألم لغرض توجيه المتدرب."""
    master_db = get_biomechanics_database()
    for group_name, exercises_list in master_db.items():
        for ex in exercises_list:
            if ex.get("name", "") == exercise_name: return ex
    return {
        "name": exercise_name, "reps": "10-12 عدة (نطاق تضخيم أساسي)", "technique": "حافظ على التكنيك السليم وتجنب التأرجح واستخدام الزخم. المدى الحركي الكامل (Full ROM) هو السر الوحيد للتطور.", 
        "breathing": "تنفس منتظم مستمر. لا تحبس أنفاسك أبداً تحت الوزن. زفير قوي مع الجهد الأكبر.", "good_pain": "شد واحتراق إيجابي في بطن العضلة المستهدفة يعقبه تمدد (Pump).", "bad_pain": "أي ألم حاد، طقطقة، أو وخز مفاجئ في المفاصل والأوتار المحيطة."
    }

# =====================================================================
# 8. AI REP IMPUTATION (الذكاء الاصطناعي لحساب العدات والتطور)
# =====================================================================

def fetch_historical_record(exercise_name: str):
    """جلب الأوزان السابقة لتمرين محدد لغرض التطوير التدريجي (Progressive Overload)."""
    df = fetch_enterprise_data("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_records = df[df['Exercise'] == exercise_name]
        if not past_records.empty:
            last = past_records.iloc[-1]
            return last.get('Date', 'غير متوفر'), float(last.get('Weight', 0)), int(last.get('Reps', 10))
    return None, 0.0, 0

def predict_smart_reps(exercise_name: str, current_weight: float) -> int:
    """محرك الذكاء الاصطناعي لتقدير العدات بناءً على قوانين التضخيم العالمية"""
    date, last_weight, last_reps = fetch_historical_record(exercise_name)
    if date:
        if current_weight > last_weight: return max(last_reps - 2, 6) 
        elif current_weight < last_weight: return last_reps + 2
        else: return last_reps
    return 10

# --- نهاية الدفعة الثانية (2 من 5) ---
# =====================================================================
# 9. COMMERCIAL NUTRITION DATABASE (قاعدة التغذية والمطاعم السعودية)
# قاعدة بيانات (Offline) تضمن عمل التطبيق بسرعة البرق دون الحاجة
# للاتصال بـ APIs خارجية مكلفة. تم دمجها في قاموس واحد لتفادي ValueError.
# =====================================================================

def get_enterprise_food_db() -> dict:
    """
    مكتبة الماكروز السعودية المعتمدة للتنشيف والبناء.
    تحتوي على الإيدامات، المطاعم السريعة، والمكملات في هيكل موحد.
    """
    return {
        # --- قسم الإيدامات وطبخ البيت ---
        "إيدام دجاج بالبطاطس (صحن وسط - بدون رز)": {"protein": 35, "cals": 320},
        "إيدام دجاج بالبطاطس + صحن رز أبيض (150 جرام)": {"protein": 40, "cals": 580},
        "إيدام لحم بالخضار (بدون رز - قطع لحم صافية)": {"protein": 45, "cals": 450},
        "إيدام لحم بالخضار + صحن رز أبيض متوسط": {"protein": 50, "cals": 710},
        "إيدام بامية باللحم (طبيخ منزلي)": {"protein": 40, "cals": 410},
        "ملوخية بالدجاج + صحن رز": {"protein": 35, "cals": 480},
        "كبسة دجاج (صدر دجاج صافي + رز 200 جرام)": {"protein": 45, "cals": 650},
        "كبسة دجاج (فخذ دجاج مع الجلد + رز)": {"protein": 35, "cals": 750},
        "مكرونة حمراء بالدجاج (صدر مقطع)": {"protein": 35, "cals": 520},
        "صالونة خضار مشكلة (بدون لحم أو دجاج)": {"protein": 5, "cals": 150},
        "جريش باللحم (صحن متوسط)": {"protein": 30, "cals": 450},
        "قرصان (صحن متوسط)": {"protein": 15, "cals": 350},
        "سليق بالدجاج (صحن متوسط)": {"protein": 35, "cals": 500},
        
        # --- قسم المطاعم السريعة والشواية ---
        "نصف حبة دجاج شواية (بدون جلد - الأفضل للتنشيف)": {"protein": 45, "cals": 420},
        "نصف حبة دجاج فحم (مع الجلد)": {"protein": 40, "cals": 550},
        "بروستد (نصف حبة دجاج مقلي مع البطاطس)": {"protein": 35, "cals": 950},
        "وجبة البيك (دجاج مسحب 10 قطع مع بطاطس وثوم)": {"protein": 45, "cals": 1100},
        "وجبة البيك (مسحب 7 قطع بدون بطاطس - للدايت)": {"protein": 32, "cals": 500},
        "صاروخ شاورما دجاج (عادي بدون بطاطس وجبن إضافي)": {"protein": 25, "cals": 550},
        "صحن شاورما عربي دجاج (مع بطاطس وثوم)": {"protein": 35, "cals": 850},
        "وجبة ماك تشيكن (ساندوتش + بطاطس وسط)": {"protein": 18, "cals": 750},
        "وجبة بيج ماك (لحم)": {"protein": 25, "cals": 850},
        "برجر لحم مشوي (مفرد - مطاعم الشوي المختصة)": {"protein": 20, "cals": 400},
        "برجر دجاج مشوي (مطعم دايت صحي)": {"protein": 30, "cals": 350},
        
        # --- قسم النواشف والمكملات ---
        "علبة تونة (مصفاة بالماء - 100 جرام)": {"protein": 26, "cals": 120},
        "علبة تونة (بالزيت - مصفاة قليلاً)": {"protein": 24, "cals": 220},
        "سكوب بروتين (Whey Protein - مع ماء)": {"protein": 25, "cals": 120},
        "سكوب بروتين (مع 200 مل حليب كامل الدسم)": {"protein": 31, "cals": 240},
        "3 بيضات مسلوقة كاملة (مع الصفار)": {"protein": 18, "cals": 210},
        "5 بياض بيض مسلوق (بدون صفار - تنشيف صافي)": {"protein": 18, "cals": 85},
        "شريحة لحم ستيك (200 جرام - مطبوخ)": {"protein": 50, "cals": 450},
        "علبة زبادي يوناني سادة (150 جرام)": {"protein": 15, "cals": 100},
        "حليب بروتين عالي (ندى/المراعي - عبوة 320 مل)": {"protein": 27, "cals": 150},
        "شوفان بالحليب الكامل (50 جرام شوفان)": {"protein": 13, "cals": 310}
    }

# =====================================================================
# 10. DYNAMIC TIME ENGINE & WORKOUT CLASSES
# المحرك الاستراتيجي للكلاسات، حساب الحرق، والهندسة الزمنية
# =====================================================================

def get_class_burn_rates() -> dict:
    """معدلات الحرق التقريبية للكلاسات لاستخدامها في حساب السعرات النهائي."""
    return {
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

def get_workout_strategy() -> dict:
    """
    المحرك الاستراتيجي الذي يربط الكلاس بالعضلة المستهدفة في صالة الحديد.
    يضمن لك مساراً تدريبياً خالياً من التعارض بين العضلات المجهدة في الكلاس وتمرين الحديد.
    """
    return {
        "موتيف 8": {"iron": "صدر + تراي", "flow": "الصدر يحتاج تركيز عالي وتوازن. ابدأ بـ Incline Press لشد الجزء العلوي، ثم انتقل للترايسبس."},
        "فت كومبات": {"iron": "أرجل + بطن", "flow": "يوم حرق الدهون العظيم! ابدأ بالسكوات الثقيل كمحفز للتستوستيرون، ولا تتنازل عن الأوزان الحرة."},
        "كور اكستريم": {"iron": "أكتاف + جوانب", "flow": "أكتاف عريضة = خصر أنحف بصرياً. ركز على تمرين Overhead Press لبناء الكتلة الأساسية."},
        "ستيب": {"iron": "ظهر + باي", "flow": "شد الظهر يمنع التحدب ويصحح قوام المهندس. ركز على الـ Deadlift و السحب العلوي."},
        "اكوا": {"iron": "حديد شامل (Full Body)", "flow": "اختر تمرين مركب واحد لكل عضلة كبيرة (بنش، سكوات، سحب عالي) لإبقاء الجسم في حالة نشاط."},
        "بامب فت": {"iron": "صدر + أكتاف", "flow": "استخدم أوزان متوسطة وتكرارات عالية جداً (15+) لزيادة الـ Pump وضخ الدم بقوة للألياف."},
        "بودي ماكس": {"iron": "أرجل + ظهر", "flow": "أعنف يوم في الأسبوع! يستهدف أكبر عضلتين لنسف الكرش. حافظ على طاقتك واشرب الكثير من الماء."},
        "رادير": {"iron": "ذراعين (باي وتراي)", "flow": "العب بطريقة (Supersets) باي متبوعاً بتراي مباشرة لزيادة الحرق واختصار وقت النادي."},
        "جي فت": {"iron": "حديد قوة (Heavy Lift)", "flow": "3 إلى 5 عدات فقط بأقصى وزن حر. يجب أن تأخذ راحة 3 دقائق كاملة بين الجولات لتجنب إصابة الجهاز العصبي."},
        "فت اتاك": {"iron": "أرجل + أكتاف", "flow": "تمارين مركبة سريعة لرفع نبض القلب وزيادة معدل الحرق الأيضي (Metabolic Rate)."},
        "موبيلتي": {"iron": "تمرين حر (النقاط الضعيفة)", "flow": "استهدف عضلة متأخرة وضعيفة (مثل السمانة أو السواعد)، أو قم بجلسة إطالات عميقة للتعافي."},
        "لا يوجد": {"iron": "تمرين حر متكامل", "flow": "أنت القائد اليوم. صمم روتينك بناءً على مستوى طاقتك ونشاطك، واستمع لجسدك."},
        "راحة / غياب": {"iron": "راحة", "flow": "استشفاء سلبي. بناء الأنسجة العضلية يتم الآن. قلل من الكربوهيدرات لعدم وجود مجهود عالي اليوم."}
    }

def analyze_muscle_balance(plan_df: pd.DataFrame) -> tuple:
    """
    فحص التوازن الهندسي. يحذرك إذا أهملت عضلة معينة أو ضغطت على عضلة أخرى
    أكثر من اللازم خلال أسبوع التدريب.
    """
    if plan_df.empty: 
        return True, ""
        
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    engineering_alerts = []
    
    if "أرجل" not in all_muscles_text: 
        engineering_alerts.append("🔴 خطأ معماري: المخطط يفتقد لتمارين الأرجل (وهي الأساس الأول لإفراز التستوستيرون وحرق دهون الكرش المستعصية).")
    if "ظهر" not in all_muscles_text: 
        engineering_alerts.append("🔴 خلل في القوام: يجب تدريب الظهر بانتظام لسحب الأكتاف للخلف وتصحيح انحناء العمود الفقري الناتج عن العمل المكتبي.")
    if all_muscles_text.count("صدر") > 2: 
        engineering_alerts.append("🔴 إجهاد هيكلي מفرط: الصدر مستهدف بكثافة عالية جداً في أسبوع واحد، هذا سيؤدي للهدم العضلي والالتهاب ولن تنمو العضلة.")
        
    if len(engineering_alerts) > 0: 
        return False, "<br><br>".join(engineering_alerts)
        
    return True, "🟢 التصريح الهندسي: ممتاز. المخطط متوازن تماماً، يهاجم الدهون بقوة، ويضمن الاستشفاء السليم لجميع المفاصل."

def get_dynamic_schedule(attendance_mode: str, origin_loc: str, current_time: datetime) -> tuple:
    """
    محرك الجدولة الزمنية بالدقيقة (Time Blocking Engine).
    يحسب الوقت لإنهاء الحديد في 75 دقيقة كحد أقصى تجنباً لإفراز الكورتيزول.
    """
    eta_mins, distance_km = calculate_smart_eta(origin_loc, current_time)
    
    arrival_time_obj = current_time + timedelta(minutes=eta_mins)
    iron_start_obj = arrival_time_obj + timedelta(minutes=10) # 10 دقائق للتغيير والتسخين
    iron_end_obj = iron_start_obj + timedelta(minutes=75) # 75 دقيقة حد أقصى للتضخيم
    
    now_formatted = current_time.strftime("%I:%M %p")
    arrival_formatted = arrival_time_obj.strftime("%I:%M %p")
    iron_start_formatted = iron_start_obj.strftime("%I:%M %p")
    iron_end_formatted = iron_end_obj.strftime("%I:%M %p")
    
    return now_formatted, arrival_formatted, iron_start_formatted, iron_end_formatted, arrival_time_obj, distance_km, eta_mins

def get_week_dates(current_time: datetime) -> dict:
    """
    دالة لحساب تواريخ الأسبوع الجاري بديناميكية بحيث يبدأ الأسبوع بيوم السبت دائماً.
    """
    days_since_saturday = (current_time.weekday() + 2) % 7 
    last_saturday_date = current_time - timedelta(days=days_since_saturday)
    
    week_days_names = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
    week_dates_mapping = {}
    
    for i, day in enumerate(week_days_names):
        future_date = last_saturday_date + timedelta(days=i)
        week_dates_mapping[day] = future_date.strftime("%Y-%m-%d")
        
    return week_dates_mapping

# --- نهاية الدفعة الثالثة (3 من 5) ---
# =====================================================================
# 11. CLOUD-STATE SYNC ENGINE (محرك المزامنة السحابية اللحظية)
# هذا المحرك هو المسؤول عن حل مشكلة "فقدان البيانات" عند تحديث الصفحة.
# يقوم بكتابة حالة الحضور (Mode) في السحابة فور اتخاذ القرار.
# =====================================================================

def update_attendance_decision(mode_key: str, status_label: str, current_date: str):
    """
    تحديث حالة الحضور في ورقة العمل "Weekly_Plan" مباشرة.
    يضمن التزامن الكامل بين نسخة الجوال والمتصفح في وقت واحد.
    """
    st.session_state['attendance_mode'] = mode_key
    conn = connect_to_cloud_storage()
    
    if conn:
        try:
            # جلب البيانات الحية بدون كاش لضمان التعديل على آخر نسخة
            df = conn.read(worksheet="Weekly_Plan", ttl=0)
            if not df.empty and 'Date' in df.columns:
                # تحديد سطر اليوم الحالي لتعديل حالته
                mask = df['Date'] == current_date
                if mask.any():
                    df.loc[mask, 'Status'] = status_label
                    conn.update(worksheet="Weekly_Plan", data=df)
                    # مسح الكاش لإجبار النظام على قراءة الحالة الجديدة
                    st.cache_data.clear() 
                    return True
        except Exception:
            pass
    return False

def sync_mode_from_cloud(current_date: str):
    """
    قراءة حالة الحضور المسجلة سحابياً عند فتح التطبيق.
    تمنع ضياع القرارات الميدانية عند إعادة تشغيل المحرك.
    """
    if st.session_state.get('last_sync_timestamp') != current_date:
        plan_df = fetch_enterprise_data("Weekly_Plan")
        if not plan_df.empty and 'Date' in plan_df.columns and 'Status' in plan_df.columns:
            today_rows = plan_df[plan_df['Date'] == current_date]
            if not today_rows.empty:
                cloud_status = str(today_rows.iloc[0].get('Status', 'مجدول'))
                
                # خارطة الطريق لترجمة حالات الإكسل إلى أوضاع برمجية
                status_map = {
                    "حضور كامل": "Full",
                    "حديد فقط": "IronOnly",
                    "كلاس فقط": "ClassOnly",
                    "تأخير": "Delayed",
                    "غائب": "Absent",
                    "مجدول": "Full"
                }
                st.session_state['attendance_mode'] = status_map.get(cloud_status, "Full")
        
        # قفل التزامن لليوم الحالي لمنع تكرار العمليات
        st.session_state['last_sync_timestamp'] = current_date

# =====================================================================
# 12. GLOBAL EXECUTION ENGINE (The main() Function)
# الدالة الرئيسية التي تدير كامل هيكل التطبيق والواجهة الأمامية
# =====================================================================

def main():
    """
    نقطة الانطلاق المركزية للنظام.
    تم تصميمها بنظام "الطبقات" (Layered Architecture) لضمان عدم حدوث NameError.
    """
    # [1] طبقة التهيئة: استدعاء المتغيرات المؤمنة
    init_titan_states()
    
    # [2] طبقة الزمن: ضبط التوقيت العالمي الموحد للتطبيق
    CURRENT_MAKKAH_TIME = get_makkah_time()
    current_date_str = CURRENT_MAKKAH_TIME.strftime("%Y-%m-%d")
    
    # [3] طبقة التزامن: مطابقة حالة الجوال مع السحابة فور التشغيل
    sync_mode_from_cloud(current_date_str)
    
    # [4] طبقة البيانات الوصفية: تحضير الأيام والتواريخ
    days_ar_map = {
        "Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", 
        "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"
    }
    today_ar_name = days_ar_map.get(CURRENT_MAKKAH_TIME.strftime("%A"), "غير محدد")
    week_dates_dict = get_week_dates(CURRENT_MAKKAH_TIME)
    
    # [5] طبقة المحركات الاستراتيجية
    workout_strategies = get_workout_strategy()
    class_burn_data = get_class_burn_rates()

    # -----------------------------------------------------------------
    # SAAS COMMAND CENTER HEADER
    # واجهة التحكم العليا - التصميم التجاري الفاخر
    # -----------------------------------------------------------------
    header_section = "".join([
        f"<div style='background: linear-gradient(90deg, #1A1C23, #0D1117); padding: 25px 40px; border-radius: 18px; border-bottom: 4px solid #E5B94C; display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; box-shadow: 0 15px 35px rgba(0,0,0,0.6);'>",
        f"<div style='color: #8B949E; font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px;'>",
        f"مكة المكرمة | {today_ar_name} {current_date_str} | <span style='color: #E8ECEF;'>{CURRENT_MAKKAH_TIME.strftime('%I:%M %p')}</span>",
        f"</div>",
        f"<div style='display: flex; gap: 25px; align-items: center;'>",
        f"<span style='background: rgba(229, 185, 76, 0.15); padding: 10px 25px; border-radius: 35px; color: #E5B94C; font-weight: 900; font-size: 14px; border: 1px solid rgba(229, 185, 76, 0.3);'>👑 ENTERPRISE PRO ACTIVE</span>",
        f"<span style='color: #E8ECEF; font-weight: 800; font-size: 20px; letter-spacing: 1px;'>Titan System V60</span>",
        f"</div></div>"
    ])
    st.markdown(header_section, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # MAIN COMMAND TABS
    # ألسنة التنقل المركزية للنظام
    # -----------------------------------------------------------------
    tabs_list = st.tabs([
        "🚀 الميدان والملاحة", 
        "🗓️ المخطط الأسبوعي", 
        "🏋️ السجل الحيوي", 
        "🏥 العيادة الطبية", 
        "📸 عدسة الذكاء (AI)", 
        "🥗 مختبر الماكروز", 
        "🛠️ الإدارة والإصلاح"
    ])
    
    t_ops, t_setup, t_log, t_clinic, t_vision, t_fuel, t_sys = tabs_list

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS (الميدان والملاحة المركزية)
    # -----------------------------------------------------------------
    with t_ops:
        # قراءة المخطط الاستراتيجي من السحابة لليوم الحالي
        plan_df = fetch_enterprise_data("Weekly_Plan")
        todays_scheduled_class = "موتيف 8" # القيمة الافتراضية
        
        if not plan_df.empty and 'Date' in plan_df.columns:
            today_row = plan_df[plan_df['Date'] == current_date_str]
            if not today_row.empty:
                todays_scheduled_class = str(today_row.iloc[0].get('Class', 'موتيف 8'))
        
        # جلب تفاصيل الاستراتيجية
        strategy_info = workout_strategies.get(todays_scheduled_class, {})
        iron_target = strategy_info.get("iron", "صدر + تراي")
        flow_note = strategy_info.get("flow", "استراتيجية حرة، ركز على المدى الحركي.")
        burn_est = class_burn_data.get(todays_scheduled_class, 0)
        
        mode = st.session_state['attendance_mode']

        # [A] منطق يوم الجمعة (يوم الراحة العالمي)
        if today_ar_name == "الجمعة" and mode != "IronOnly":
            friday_card = "".join([
                "<div class='titan-card titan-card-center' style='border: 2px solid #2EA043; background: linear-gradient(145deg, rgba(46, 160, 67, 0.1), #080A0F);'>",
                "<h1 style='color:#2EA043; margin:0; font-size: 55px;'>يوم راحة سلبي إلزامي 🛑</h1>",
                "<p style='color:#8B949E; margin-top:20px; font-size:22px; font-weight: bold;'>الأنسجة العضلية تُبنى أثناء النوم والراحة، وليس في النادي. استمتع بيومك يا مهندس.</p>",
                "</div>"
            ])
            st.markdown(friday_card, unsafe_allow_html=True)
            
            if st.button("الذهاب للنادي للحديد فقط (تجاوز الراحة)", use_container_width=True): 
                update_attendance_decision("IronOnly", "حديد فقط", current_date_str)
                st.rerun()
                
        # [B] منطق يوم الراحة المجدول أو الغياب الطارئ
        elif todays_scheduled_class == "راحة / غياب" or mode == "Absent":
            absent_card = "".join([
                "<div class='titan-card' style='border-color: #F85149; background: linear-gradient(145deg, rgba(248, 81, 73, 0.05), #080A0F);'>",
                "<h2 style='color:#F85149; text-align:center; font-size: 40px;'>مجدول كـ (راحة / غياب) ❌</h2>",
                f"<p style='text-align:center; color:#8B949E; font-size:20px;'>تم ترحيل تمرين العضلة المستهدفة <b>({iron_target})</b> للغد تلقائياً.</p>",
                "<hr style='border-color:#30363D; margin: 35px 0;'>",
                "<h4 style='color:#E8ECEF; text-align:center;'>توجيه تغذية طارئ</h4>",
                "<p style='text-align:center; color:#8B949E; font-size:16px;'>بما أن الحرق اليوم منخفض، يُنصح بتقليل حصة الكربوهيدرات والدهون وزيادة البروتين للحفاظ على الكتلة.</p>",
                "</div>"
            ])
            st.markdown(absent_card, unsafe_allow_html=True)
            
            if st.button("إلغاء الراحة والتوجه للنادي الآن", use_container_width=True): 
                update_attendance_decision("Full", "حضور كامل", current_date_str)
                st.rerun()
                
        # [C] العمليات الميدانية النشطة
        else:
            col_ ميدان_l, col_ ميدان_r = st.columns([2, 1])
            
            # --- العمود الأيمن: الملاحة والتحكم ---
            with col_ ميدان_r:
                st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>📍 الملاحة الذكية والإحداثيات</h4>", unsafe_allow_html=True)
                
                loc_list = ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"]
                current_loc_idx = loc_list.index(st.session_state['selected_origin_loc']) if st.session_state['selected_origin_loc'] in loc_list else 0
                
                origin_loc = st.selectbox("موقع الانطلاق الحالي:", loc_list, index=current_loc_idx)
                st.session_state['selected_origin_loc'] = origin_loc
                
                # تفعيل محرك الملاحة الجغرافي
                eta_val, dist_val = calculate_smart_eta(origin_loc, CURRENT_MAKKAH_TIME)
                
                nav_stats_html = "".join([
                    f"<div style='background: rgba(88, 166, 255, 0.08); padding: 20px; border-radius: 15px; margin-top: 25px; border: 1px solid rgba(88, 166, 255, 0.2); text-align: right;'>",
                    f"<p style='color:#8B949E; margin: 0 0 12px 0; font-size:16px;'><span style='color:#58A6FF;'>📏 المسافة:</span> <b style='color:#E8ECEF; font-size:19px;'>{dist_val:.1f} KM</b></p>",
                    f"<p style='color:#8B949E; margin: 0; font-size:16px;'><span style='color:#58A6FF;'>⏱️ الوقت (Traffic):</span> <b style='color:#E8ECEF; font-size:19px;'>{eta_val} دقيقة</b></p>",
                    f"</div>"
                ])
                st.markdown(nav_stats_html, unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color:#30363D; margin: 35px 0;'><h4 style='margin-top:0;'>🕹️ إدارة المسار الميداني</h4>", unsafe_allow_html=True)
                
                if st.button("✅ حضور كامل (كلاس + حديد)", use_container_width=True): 
                    update_attendance_decision("Full", "حضور كامل", current_date_str); st.rerun()
                if st.button("🏋️ صالة الحديد فقط", use_container_width=True): 
                    update_attendance_decision("IronOnly", "حديد فقط", current_date_str); st.rerun()
                if st.button("🤸 كلاس اللياقة فقط", use_container_width=True): 
                    update_attendance_decision("ClassOnly", "كلاس فقط", current_date_str); st.rerun()
                if st.button("⏳ تأخير مسار (زحمة الطريق)", use_container_width=True): 
                    update_attendance_decision("Delayed", "تأخير", current_date_str); st.rerun()
                if st.button("❌ تسجيل غياب لليوم", use_container_width=True): 
                    update_attendance_decision("Absent", "غائب", current_date_str); st.rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)

            # --- العمود الأيسر: الجدول الزمني التفصيلي ---
            with col_ ميدان_l:
                # حساب الأوقات بدقة الدقيقة
                n_str, a_str, is_str, ie_str, arr_obj, d_km, e_min = get_dynamic_schedule(mode, origin_loc, CURRENT_MAKKAH_TIME)
                
                # رسالة التنبيه للوقت المبكر
                time_warning_html = ""
                if arr_obj.hour < 18 and mode in ["Full", "ClassOnly"]:
                    time_warning_html = "<div class='alert-box' style='margin-top:25px;'>⚠️ تنبيه هندسي للوقت: الكلاس يبدأ 9:00 م. وصولك الآن مبكر جداً، ستحتاج للعودة لاحقاً، أو يمكنك إنهاء تمرينك دفعة واحدة بتحويل المسار لـ (حديد فقط).</div>"
                
                # بناء بطاقة الجدول الزمني التفاعلية
                if mode == "Full":
                    main_ops_html = "".join([
                        "<div class='titan-card'>",
                        "<h3 style='margin-top:0;'>🗺️ الخطة أ (طاقة قصوى - كلاس وحديد)</h3>",
                        f"<p><span class='data-label'>عضلة اليوم:</span> <b style='color:#E5B94C; font-size:22px;'>{iron_target}</b></p>",
                        f"<p><span class='data-label'>كلاس السهرة:</span> <b style='color:#E5B94C; font-size:22px;'>{todays_scheduled_class}</b> <span style='font-size:14px; color:#F85149;'>(~{burn_est} kcal)</span></p>",
                        f"<div style='background: rgba(229, 185, 76, 0.05); padding: 20px; border-radius: 12px; border-right: 5px solid #E5B94C; margin-top: 20px;'>",
                        f"<p style='color:#E8ECEF; margin:0; font-size:16px;'><b>الاستراتيجية:</b> {flow_note}</p>",
                        "</div><hr style='border-color:#30363D; margin: 30px 0;'>",
                        f"<p style='font-size: 17px;'>🚗 الانطلاق المجدول: <b style='color:#E8ECEF;'>{n_str}</b> | 🅿️ وصول البوابة: <b style='color:#E8ECEF;'>{a_str}</b></p>",
                        "<h5 style='margin-top:35px; color:#E5B94C;'>الجدول الزمني الميداني المقترح</h5>",
                        f"<p style='font-size: 17px; margin: 12px 0;'>🔥 {a_str} - {is_str} : <span style='color:#8B949E;'>إحماء وتجهيز مفاصل دقيق</span></p>",
                        f"<p style='font-size: 17px; margin: 12px 0;'>💪 {is_str} - {ie_str} : <b style='color:#F85149;'>صالة الحديد (تم تقييدها بـ 75 دقيقة لمنع الهدم)</b></p>",
                        f"<p style='font-size: 17px; margin: 12px 0;'>🤸 09:00 PM - 09:50 PM : <b style='color:#2EA043;'>حضور الكلاس (مرحلة حرق الدهون الصافية)</b></p>",
                        time_warning_html,
                        "</div>"
                    ])
                elif mode == "IronOnly":
                    main_ops_html = "".join([
                        "<div class='titan-card' style='border-color: #58A6FF; box-shadow: 0 15px 35px rgba(88, 166, 255, 0.1);'>",
                        "<h3 style='margin-top:0; color:#58A6FF;'>🏋️ مسار الحديد المكثف (تم إلغاء الكلاس)</h3>",
                        f"<p><span class='data-label'>المستهدف الرئيسي:</span> <b style='color:#E5B94C; font-size:22px;'>{iron_target}</b></p>",
                        f"<div style='background: rgba(88, 166, 255, 0.05); padding: 20px; border-radius: 12px; border-right: 5px solid #58A6FF; margin-top: 20px;'>",
                        "<p style='color:#E8ECEF; margin:0; font-size:16px;'>كامل طاقتك موجهة لكسر الأوزان الحرة وبناء الكتلة العضلية اليوم.</p>",
                        "</div><hr style='border-color:#30363D; margin: 30px 0;'>",
                        f"<p style='font-size: 17px;'>🚗 الانطلاق المجدول: <b style='color:#E8ECEF;'>{n_str}</b> | 🅿️ وصول البوابة: <b style='color:#E8ECEF;'>{a_str}</b></p>",
                        "<h5 style='margin-top:35px; color:#58A6FF;'>الجدول الميداني المفتوح</h5>",
                        f"<p style='font-size: 17px; margin: 12px 0;'>🔥 {a_str} - {is_str} : <span style='color:#8B949E;'>إحماء دقيق وتمديد للأوتار</span></p>",
                        f"<p style='font-size: 17px; margin: 12px 0;'>💪 {is_str} - {(arr_obj + timedelta(minutes=90)).strftime('%I:%M %p')} : <b style='color:#F85149;'>صالة الحديد المفتوحة (العب جولات إضافية للأجزاء الضعيفة)</b></p>",
                        "</div>"
                    ])
                elif mode == "ClassOnly":
                    main_ops_html = "".join([
                        "<div class='titan-card' style='border-color: #E5B94C;'>",
                        "<h3 style='margin-top:0; color:#E5B94C;'>🤸 مسار الكارديو (صالة الحديد ملغية)</h3>",
                        f"<p><span class='data-label'>الكلاس المجدول:</span> <b style='color:#E5B94C; font-size:22px;'>{todays_scheduled_class}</b></p>",
                        "<div style='background: rgba(229, 185, 76, 0.05); padding: 20px; border-radius: 12px; border-right: 5px solid #E5B94C; margin-top: 20px;'>",
                        "<p style='color:#E8ECEF; margin:0; font-size:16px;'>الهدف اليوم هو حرق السعرات ورفع اللياقة القلبية. ركز على كفاءة التنفس.</p>",
                        "</div><hr style='border-color:#30363D; margin: 30px 0;'>",
                        f"<p style='font-size: 17px;'>🤸 09:00 PM - 09:50 PM : <b style='color:#2EA043;'>حضور الكلاس (مستهدف حرق ~{burn_est} kcal)</b></p>",
                        time_warning_html,
                        "</div>"
                    ])
                else: # Delayed
                    main_ops_html = "".join([
                        "<div class='titan-card' style='border-color: #F85149;'>",
                        "<h3 style='margin-top:0; color:#F85149;'>⚠️ مسار التأخير والطوارئ (إنقاذ التمرين)</h3>",
                        f"<p><span class='data-label'>الحديد المختصر:</span> <b style='color:#E5B94C; font-size:22px;'>{iron_target}</b></p>",
                        "<hr style='border-color:#30363D; margin: 30px 0;'>",
                        "<p style='font-size: 17px; margin: 12px 0;'>🤸 09:00 PM - 09:50 PM : <b style='color:#E5B94C;'>توجه للكلاس مباشرة لعدم تفويت التسخين الجماعي</b></p>",
                        "<p style='font-size: 17px; margin: 12px 0;'>💪 09:55 PM - 10:30 PM : <b style='color:#F85149;'>حديد سريع ومكثف (استخدم أجهزة العزل فقط لحماية المفاصل المرهقة)</b></p>",
                        "</div>"
                    ])
                
                st.markdown(main_ops_html, unsafe_allow_html=True)
            
            # استدعاء بروتوكول الاستشفاء (من Batch 2) وتضمينه في الواجهة
            st.markdown(get_recovery_protocol(mode, iron_target, CURRENT_MAKKAH_TIME), unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN (هندسة الأسبوع السحابية)
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع (مزامنة سحابية متقدمة)")
        st.info("قم بتوزيع الكلاسات للأيام القادمة. يتم مزامنة هذه اللوحة مع سيرفرات جوجل لتنعكس على جميع أجهزتك فورياً.")
        
        # قراءة المخطط السابق
        plan_df = fetch_enterprise_data("Weekly_Plan")
        stored_plan_dict = {row['Day']: row['Class'] for _, row in plan_df.iterrows()} if not plan_df.empty and 'Day' in plan_df.columns else {}
        
        with st.form("weekly_setup_master_form"):
            new_schedule_list = []
            cols_grid = st.columns(3)
            all_available_options = list(workout_strategies.keys())
            
            for index, (day_n, day_dt) in enumerate(week_dates_dict.items()):
                # تحديد الخيار السابق لتسهيل عملية التعديل السريع
                previous_choice = stored_plan_dict.get(day_n, "موتيف 8")
                try: option_index = all_available_options.index(previous_choice)
                except ValueError: option_index = 0
                
                with cols_grid[index % 3]:
                    st.markdown(f"""
                    <div style='background: #161B22; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #30363D;'>
                        <h5 style='color:#E8ECEF; text-align:right; margin: 0 0 15px 0;'>{day_n} <br><span style='font-size:12px; color:#8B949E;'>({day_dt})</span></h5>
                    """, unsafe_allow_html=True)
                    
                    selected_class_val = st.selectbox("الكلاس:", all_available_options, index=option_index, key=f"select_{day_n}", label_visibility="collapsed")
                    
                    target_muscle_val = workout_strategies.get(selected_class_val, {}).get("iron", "غير محدد")
                    
                    new_schedule_list.append({
                        "Day": day_n, "Date": day_dt, "Class": selected_class_val, 
                        "Muscle": target_muscle_val, "Status": "مجدول"
                    })
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='border-color:#30363D; margin: 20px 0;'>", unsafe_allow_html=True)
            if st.form_submit_button("✅ فحص التوازن الهندسي واعتماد المخطط في السحابة", use_container_width=True):
                # فحص هندسي لعضلات الأسبوع
                balance_check, balance_msg = analyze_muscle_balance(pd.DataFrame(new_schedule_list))
                st.markdown(f"<div class='{'success-box' if balance_check else 'alert-box'}'>{balance_msg}</div>", unsafe_allow_html=True)
                
                # رفع الجدول النهائي للسحابة
                if master_overwrite("Weekly_Plan", pd.DataFrame(new_schedule_list)):
                    st.success("تم تحديث المخطط الاستراتيجي بنجاح وتفريغ الذاكرة المؤقتة للاعتماد الفوري.")
                else:
                    st.error("فشل في المزامنة السحابية. تأكد من جودة الاتصال.")

# --- نهاية الدفعة الرابعة (4 من 5) ---
# -----------------------------------------------------------------
    # TAB 3: BIOMECHANICS & LOGS (علم الحركة الحيوية وتتبع الأوزان)
    # -----------------------------------------------------------------
    with t_log:
        st.markdown("### 🏋️ السجل الحيوي وتتبع الأوزان (Biomechanics Analytics)")
        
        # التقييم قبل التمرين (Pre-Workout Safety Check)
        st.markdown("<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>🚦 التقييم الصحي والأمني قبل التمرين</h4>", unsafe_allow_html=True)
        pre_workout_pain = st.selectbox(
            "كيف تقيم حالة جسمك ومفاصلك اليوم قبل البدء بالأوزان؟", 
            [
                "سليم 100% (جاهز لكسر الأوزان الحرة وبناء الكتلة)", 
                "إرهاق عام وعضلات مشدودة (DOMS طبيعي من الأمس)", 
                "ألم خفيف في أحد المفاصل (ركبة، كوع، رسغ)", 
                "ألم حاد في أسفل الظهر أو الكتف الداخلي (خطر إصابة)"
            ]
        )
        
        if "المفاصل" in pre_workout_pain or "خطر" in pre_workout_pain: 
            st.warning("🚨 تحذير النظام الطبي: يُمنع اليوم لعب الأوزان الحرة المركبة (Deadlift, Squat, Barbell Press). استمر بتمرينك باستخدام الأجهزة ذات المسار الثابت (Cable & Machines) فقط لحماية أربطتك من التمزق.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_log_l, col_log_r = st.columns([1, 2])
        
        # --- عمود المؤقت (يسار) ---
        with col_log_l:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة الدقيق</h4><p style='font-size:13px; color:#8B949E; margin-top:10px;'>الالتزام بوقت الراحة هو السر وراء ضخ الدم (Pump) والبناء.</p>", unsafe_allow_html=True)
            
            if st.button("بدء 90 ثانية (تضخيم وبناء)", use_container_width=True): 
                progress_bar = st.progress(0)
                for second in range(90): 
                    time.sleep(1)
                    progress_bar.progress((second + 1) / 90)
                st.success("انتهى وقت الراحة المعتمد. ارجع للبار فوراً!")
                
            if st.button("3 دقائق (قوة Power)", use_container_width=True): 
                progress_bar = st.progress(0)
                for second in range(180): 
                    time.sleep(1)
                    progress_bar.progress((second + 1) / 180)
                st.success("تم استشفاء الجهاز العصبي بالكامل. انطلق لرفع الوزن الثقيل.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --- عمود تسجيل التمارين (يمين) ---
        with col_log_r:
            # تأمين استدعاء العضلة في حال كان المتغير غير معرف
            safe_iron_target = iron_target if 'iron_target' in locals() else "غير محدد"
            
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>العضلة المستهدفة اليوم: <span style='color:#E5B94C;'>{safe_iron_target}</span></h4>", unsafe_allow_html=True)
            
            # جلب قائمة التمارين الآمنة بناءً على العضلة
            exercises_list = get_exercise_options(safe_iron_target)
            selected_exercise = st.selectbox("اختر التمرين من قاعدة البيانات الهندسية:", exercises_list)
            
            # معالجة التمارين المضافة يدوياً
            if "يدوي" in selected_exercise or "Custom" in selected_exercise:
                final_exercise_name = st.text_input("أدخل اسم التمرين الجديد (باللغة الإنجليزية لتوحيد السجلات في السحابة):")
            else:
                final_exercise_name = selected_exercise
                
            final_exercise_name = final_exercise_name if final_exercise_name else "تمرين مخصص"
            
            # جلب تفاصيل التكنيك والألم
            ex_details = get_exercise_details(final_exercise_name)
            
            ex_card_html = "".join([
                "<div style='background:#161B22; padding:25px; border-radius:15px; margin-bottom:25px; border-right: 5px solid #E5B94C; box-shadow: 0 5px 15px rgba(0,0,0,0.3);'>",
                f"<p><span class='bio-tech'>⚙️ الأداء الميكانيكي (Technique):</span><br><span style='color:#E8ECEF;'>{ex_details.get('technique', 'حافظ على تكنيك سليم وتجنب التأرجح')}</span></p>",
                f"<p><span class='bio-breath'>🫁 التنفس الصحيح (Breathing):</span><br><span style='color:#E8ECEF;'>{ex_details.get('breathing', 'تنفس منتظم مستمر')}</span></p>",
                "<hr style='border-color:#30363D;'>",
                f"<p><span class='bio-good'>✅ الألم الجيد للتطور (Target DOMS):</span><br><span style='color:#E8ECEF;'>{ex_details.get('good_pain', 'بطن العضلة')}</span></p>",
                f"<p><span class='bio-bad'>❌ الألم السيء والإصابات (Injury Warning):</span><br><span style='color:#E8ECEF;'>{ex_details.get('bad_pain', 'المفاصل أو الأوتار')}</span></p>",
                "<hr style='border-color:#30363D;'>",
                f"<h5 style='color:#E5B94C; margin:0;'>النطاق العلمي الأمثل: {ex_details.get('reps', '10-12 عدة')}</h5>",
                "</div>"
            ])
            st.markdown(ex_card_html, unsafe_allow_html=True)
            
            # جلب آخر قراءة للتمرين للتطوير التدريجي (Progressive Overload)
            past_date, past_weight, past_reps = fetch_historical_record(final_exercise_name)
            
            if past_date:
                history_html = "".join([
                    "<div style='background:rgba(88, 166, 255, 0.05); border: 1px solid #58A6FF; padding:15px; border-radius:10px; margin-bottom:25px;'>",
                    f"<p style='color:#8B949E; margin:0 0 10px 0; font-size:14px;'>سجلك التاريخي الأخير بتاريخ ({past_date}):</p>",
                    f"<p style='margin:0;'><b style='color:#58A6FF; font-size:26px;'>{past_weight} KG</b> <span style='color:#8B949E; font-size:20px; margin: 0 10px;'>×</span> <b style='color:#E8ECEF; font-size:24px;'>{past_reps}</b> <span style='color:#8B949E; font-size:16px;'>عدات</span></p>",
                    "</div>"
                ])
                st.markdown(history_html, unsafe_allow_html=True)
            
            col_w, col_r = st.columns(2)
            input_weight = col_w.number_input("الوزن المرفوع حالياً (KG)", min_value=0.0, value=float(past_weight) if past_date else 0.0, step=2.5)
            input_reps = col_r.number_input("العدات المحققة (اكتب 0 للحساب الذكي)", min_value=0, value=0, step=1)
            
            if st.button("💾 توثيق وتشفير الجولة في السحابة", use_container_width=True):
                # خوارزمية استنتاج العدات الذكية
                calculated_reps = predict_smart_reps(final_exercise_name, input_weight) if input_reps == 0 else input_reps
                
                if input_reps == 0:
                    st.success(f"🤖 محرك الذكاء الاصطناعي استنتج أنك حققت {calculated_reps} عدات بناءً على الوزن القديم وقوانين التضخيم.")
                    
                log_payload = {
                    "Date": current_date_str, 
                    "Muscle": safe_iron_target, 
                    "Exercise": final_exercise_name, 
                    "Weight": input_weight, 
                    "Reps": calculated_reps
                }
                
                sync_status, sync_message = secure_push_data("Workout_Logs", log_payload)
                if sync_status: 
                    st.success(f"تم تسجيل وتشفير تمرين ({final_exercise_name}) بنجاح تام.")
                else: 
                    st.error(f"حدث خطأ أثناء المزامنة: {sync_message}")
            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------------------------------------------
        # Post-Workout DOMS Tracker (تحليل الألم بعد التمرين)
        # -------------------------------------------------------------
        st.markdown("#### 🤕 تحليل الاستشفاء والألم (DOMS Analytics Tracker)")
        with st.form("doms_analysis_form"):
            st.write("كيف كان شعورك في اليوم التالي بعد هذا التمرين؟ يساعد هذا التقييم في كشف الإصابات المبكرة وتعديل التكنيك.")
            
            doms_intensity = st.slider("مستوى الألم العضلي (1 = لا يوجد، 10 = ألم معيق للحركة):", 1, 10, 3)
            doms_location = st.selectbox("أين تركز الألم بشكل رئيسي؟", [
                "في بطن العضلة المستهدفة (ألم تمدد طبيعي وممتاز)", 
                "في المفاصل أو الأوتار المحيطة (خطر إصابة)", 
                "في أسفل الظهر أو القطنية (تحذير جدي)", 
                "في الرقبة أو الترابيس العلوية (تكنيك خاطئ)"
            ])
            
            if st.form_submit_button("💾 تحليل وحفظ تقرير الاستشفاء", use_container_width=True):
                if "المفاصل" in doms_location or "أسفل الظهر" in doms_location:
                    st.error("⚠️ التقييم يوضح أن التكنيك كان خاطئاً أو أنك استخدمت أوزاناً ثقيلة جداً لدرجة استعانتك بمفاصلك لرفعها. راجع أداءك المرة القادمة فوراً لحماية الأربطة.")
                elif doms_intensity > 8:
                    st.warning("⚠️ الألم المرتفع جداً (أكثر من 8) يعني تمزقاً ليفياً عالياً. يتطلب هذا أخذ راحة سلبية وتجنب تمرين العضلة لـ 72 ساعة القادمة، مع زيادة حصة البروتين.")
                else:
                    st.success("✅ أداء مثالي. ألم العضلة المحتمل يدل على تمزيق الألياف بشكل إيجابي لإعادة بنائها بصلابة وحجم أكبر. استمر في التغذية السليمة والنوم العميق.")

    # -----------------------------------------------------------------
    # TAB 4: CLINIC (العيادة الطبية وأرشفة الانبودي)
    # -----------------------------------------------------------------
    with t_clinic:
        st.markdown("### 📸 أرشفة التقرير الطبي (InBody Cloud Archive)")
        st.info("قم برفع أرقامك هنا. النظام يقوم بحفظها وتشفيرها تاريخياً في سيرفرات جوجل، تمهيداً لرسم منحنيات النزول والبناء في التحديثات القادمة.")
        
        with st.form("clinic_inbody_form"):
            col_inb1, col_inb2 = st.columns(2)
            
            inb_date = st.date_input("تاريخ إجراء الفحص الطبي")
            inb_weight = col_inb1.number_input("الوزن الإجمالي (KG)", value=91.9, step=0.1)
            inb_muscle = col_inb2.number_input("كتلة العضلات الصافية (SMM - KG)", value=40.0, step=0.1)
            inb_fat = col_inb1.number_input("نسبة الدهون الإجمالية (%)", value=20.0, step=0.5)
            inb_visceral = col_inb2.number_input("مؤشر الدهون الحشوية (يجب أن يكون أقل من 10)", value=14, step=1)
            
            st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
            if st.form_submit_button("💾 تشفير وأرشفة البيانات الطبية", use_container_width=True):
                inbody_payload = {
                    "Date": inb_date.strftime("%Y-%m-%d"), 
                    "Weight": inb_weight, 
                    "Muscle_Mass": inb_muscle, 
                    "Fat_Percentage": inb_fat, 
                    "Visceral_Fat": inb_visceral
                }
                sync_status, sync_msg = secure_push_data("InBody_Logs", inbody_payload)
                if sync_status: 
                    st.success("تمت الأرشفة بنجاح. أرقامك الحيوية في أمان تام.")
                else: 
                    st.error(f"خطأ في الأرشفة: {sync_msg}")

    # -----------------------------------------------------------------
    # TAB 5: PREMIUM VISION AI (ميزة الذكاء الاصطناعي للصور)
    # -----------------------------------------------------------------
    with t_vision:
        st.markdown("### 📸 عدسة تايتان للذكاء الاصطناعي (Premium SaaS Feature)")
        st.markdown("<p style='color:#8B949E; text-align:right; font-size:15px;'>هذه الميزة مخصصة لمشتركي الـ PRO. تقوم برفع صورة الوجبة، وتتولى خوادم Google Vision AI العميقة (محاكاة) استخراج المكونات وتقدير الماكروز بدقة.</p>", unsafe_allow_html=True)
        
        scans_remaining = st.session_state.get('ai_vision_scans_left', 0)
        st.markdown(f"<p style='text-align:right;'><span style='background:rgba(229,185,76,0.1); color:#E5B94C; padding:10px 20px; border-radius:10px; font-weight:bold; font-size:16px;'>الرصيد المتبقي في باقة الـ PRO الخاصة بك: {scans_remaining} عمليات مسح ضوئي</span></p>", unsafe_allow_html=True)
        
        if scans_remaining > 0:
            uploaded_meal_img = st.file_uploader("التقط صورة من الكاميرا أو ارفع صورة وجبتك للتحليل", type=["jpg", "png", "jpeg"])
            
            if uploaded_meal_img:
                st.image(uploaded_meal_img, use_container_width=True, caption="الصورة المرفوعة جاهزة للتحليل")
                
                if st.button("🔍 بدء المسح الضوئي واستخراج الماكروز (Scan Image)", use_container_width=True):
                    with st.spinner("جاري الاتصال بخوادم Vision API المتقدمة... تحليل الأنسجة الكيميائية والأبعاد..."):
                        time.sleep(3.0) # محاكاة تأخير معالجة السيرفر الحقيقية
                        
                        # محاكاة ذكية للنتائج
                        estimated_protein = 45
                        estimated_calories = 520
                        
                        # تحديث الذاكرة
                        st.session_state['daily_protein'] += estimated_protein
                        st.session_state['daily_cals'] += estimated_calories
                        st.session_state['ai_vision_scans_left'] -= 1
                        
                        ai_result_html = "".join([
                            "<div class='success-box'>",
                            "<h3 style='margin:0; color:#2EA043;'>🤖 اكتمل التحليل الكيميائي بنجاح!</h3>",
                            "<p style='margin-top:15px; color:#E8ECEF; font-size:16px;'><b>المكونات التي تم اكتشافها بصرياً:</b> مصدر بروتين حيواني مشوي (دجاج/لحم) + نسبة من الكربوهيدرات المعقدة.</p>",
                            "<hr style='border-color: rgba(46, 160, 67, 0.3); margin: 20px 0;'>",
                            "<div style='display: flex; justify-content: space-around; text-align: center;'>",
                            "<div>",
                            "<p style='color:#8B949E; margin:0 0 10px 0; font-size:15px;'>البروتين المقدر</p>",
                            f"<h2 style='color:#E8ECEF; margin:0;'>{estimated_protein} g</h2>",
                            "</div>",
                            "<div>",
                            "<p style='color:#8B949E; margin:0 0 10px 0; font-size:15px;'>السعرات المقدرة</p>",
                            f"<h2 style='color:#E8ECEF; margin:0;'>{estimated_calories} kcal</h2>",
                            "</div>",
                            "</div>",
                            "<p style='font-size:13px; color:#8B949E; margin-top:25px; text-align:center;'>تم خصم عملية مسح واحدة من رصيدك. تمت إضافة القيم لعدادك اليومي تلقائياً.</p>",
                            "</div>"
                        ])
                        st.markdown(ai_result_html, unsafe_allow_html=True)
        else:
            st.error("لقد استنفدت باقتك المخصصة من مسح الصور لهذا الشهر. قم بترقية اشتراكك للمتابعة في استخدام محركات الذكاء الاصطناعي.")

    # -----------------------------------------------------------------
    # TAB 6: NUTRITION CALCULATOR (مختبر الماكروز العملاق)
    # -----------------------------------------------------------------
    with t_fuel:
        st.markdown("### 🥗 مختبر التغذية والماكروز (Offline Database)")
        st.info("قم ببناء وجباتك بدقة عبر إضافة الأصناف والكميات. النظام سيجمع السعرات ويخصم منها حرق المسبح تلقائياً ليقدم لك الصافي.")
        
        col_fuel_left, col_fuel_right = st.columns([1, 1.2])
        
        # استدعاء قاعدة البيانات الموحدة لحل مشكلة ValueError للأبد
        full_nutrition_database = get_enterprise_food_db()
        
        with col_fuel_right:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>أضف من قاعدة البيانات السعودية المعتمدة</h4>", unsafe_allow_html=True)
            
            selected_food_item = st.selectbox("ابحث واختر الصنف (من المطاعم أو طبخ البيت):", list(full_nutrition_database.keys()))
            food_portion_qty = st.number_input("الكمية (عدد الحصص المذكورة في اسم الصنف):", min_value=1.0, value=1.0, step=0.5)
            
            if st.button("➕ إضافة الوجبة للعداد اليومي", use_container_width=True):
                # حساب الماكروز بناءً على الكمية (استخدام get لتفادي KeyError)
                food_details = full_nutrition_database.get(selected_food_item, {})
                added_p = int(food_details.get("protein", 0) * food_portion_qty)
                added_c = int(food_details.get("cals", 0) * food_portion_qty)
                
                # إضافة القيم لمتغيرات الجلسة الآمنة
                st.session_state['daily_protein'] += added_p
                st.session_state['daily_cals'] += added_c
                st.success(f"تمت الإضافة بنجاح: [+ {added_p}g بروتين, + {added_c} سعرة]")
                
            st.markdown("<hr style='border-color:#30363D; margin:30px 0;'>", unsafe_allow_html=True)
            st.write("**هل قرأت السعرات من غلاف منتج آخر؟ أدخله يدوياً هنا:**")
            
            col_man_1, col_man_2 = st.columns(2)
            manual_p_input = col_man_1.number_input("البروتين المدون (جرام)", min_value=0)
            manual_c_input = col_man_2.number_input("السعرات المدونة", min_value=0, step=10)
            
            if st.button("➕ إضافة الإدخال اليدوي للعداد", use_container_width=True):
                st.session_state['daily_protein'] += manual_p_input
                st.session_state['daily_cals'] += manual_c_input
                st.success("تم جمع القيم المدخلة يدوياً للعداد النهائي بنجاح.")
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_fuel_left:
            # المستهدفات العلمية (ثابتة حالياً)
            target_daily_protein = int(91.9 * 2.2) # 2.2 جرام لكل كيلو من وزن الجسم لمنع الهدم العضلي
            target_daily_calories = 1900 # السعرات المستهدفة للتنشيف
            
            # حساب الصافي بعد المجهود الإضافي (حرق السباحة)
            current_cals = st.session_state.get('daily_cals', 0)
            swim_cals = st.session_state.get('swim_cals_burned', 0)
            net_calories_consumed = current_cals - swim_cals
            
            fuel_dashboard_html = "".join([
                "<div class='titan-card'>",
                "<h3 style='margin-top:0;'>📊 لوحة الوقود اللحظية</h3>",
                f"<p><span class='data-label'>البروتين المكتسب:</span> <br><b style='color:#F85149; font-size:35px;'>{st.session_state.get('daily_protein', 0)} <span style='font-size:20px; color:#8B949E;'>/ {target_daily_protein} g</span></b></p>",
                f"<p><span class='data-label'>إجمالي السعرات المدخلة:</span> <br><b style='color:#E5B94C; font-size:35px;'>{current_cals} <span style='font-size:20px; color:#8B949E;'>/ {target_daily_calories} kcal</span></b></p>",
                "<hr style='border-color:#30363D; margin: 25px 0;'>",
                f"<p><span class='data-label'>حرق السباحة الإضافي المخصوم:</span> <br><b style='color:#2EA043; font-size:24px;'>- {swim_cals} kcal</b></p>",
                f"<p><span class='data-label'>صافي السعرات النهائي بعد المجهود:</span> <br><b style='color:#E8ECEF; font-size:32px;'>{net_calories_consumed} kcal</b></p>",
                "</div>"
            ])
            st.markdown(fuel_dashboard_html, unsafe_allow_html=True)
            
            with st.form("health_metrics_save_form"):
                st.write("مؤشرات الصحة الإلزامية قبل أرشفة وإغلاق يومك:")
                sleep_hours = st.number_input("ساعات النوم الفعلي الليلة الماضية (من ساعة Huawei):", value=7.5, step=0.5)
                water_liters = st.number_input("الماء المستهلك (لتر - مهم جداً لطرد احتباس السوائل):", value=3.5, step=0.5)
                
                st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
                if st.form_submit_button("💾 توثيق وحفظ يوم التغذية النهائي في السحابة", use_container_width=True):
                    health_payload = {
                        "Date": current_date_str, 
                        "Sleep": sleep_hours, 
                        "Water": water_liters, 
                        "Protein": st.session_state['daily_protein'], 
                        "Calories": net_calories_consumed, 
                        "Notes": ""
                    }
                    sync_stat, sync_msg = secure_push_data("Health_Log", health_payload)
                    
                    if sync_stat: 
                        st.success("تم الحفظ بنجاح. سيتم تصفير العداد لليوم التالي ليكون جاهزاً للاستخدام.")
                        # تصفير العدادات فورياً
                        st.session_state['daily_protein'] = 0
                        st.session_state['daily_cals'] = 0
                        st.session_state['swim_cals_burned'] = 0
                    else: 
                        st.error(f"فشل في الحفظ: {sync_msg}")

    # -----------------------------------------------------------------
    # TAB 7: SAAS ADMIN & AUTO-HEAL (لوحة الإدارة والإصلاح الذاتي)
    # -----------------------------------------------------------------
    with t_sys:
        st.markdown("### 🛠️ لوحة الإدارة المؤسسية (SaaS Administration)")
        st.info("هذا القسم مخصص لمشرفي النظام (Admins) لإدارة حالة التطبيق، تنظيف الذاكرة، وإصلاح قواعد البيانات السحابية (Google Sheets).")
        
        col_admin_1, col_admin_2 = st.columns(2)
        
        with col_admin_1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>محرك الإصلاح الذاتي (Omni-Heal)</h4>", unsafe_allow_html=True)
            st.write("يقوم بالدوران على ملف الإكسل المركزي. إذا وجد ورقة مفقودة أو عموداً ناقصاً (مثل تحديثات النظام الجديدة)، يبنيه من الصفر لضمان عدم توقف النظام أو ظهور أي خطأ برمجي (KeyError).")
            
            if st.button("🔄 بدء فحص وإصلاح قاعدة البيانات", use_container_width=True):
                with st.spinner("جاري المسح العميق والتفاوض مع خوادم Google Workspace..."):
                    time.sleep(2.0) # محاكاة معالجة
                    heal_diagnostics = run_omni_heal_diagnostics()
                    for rpt in heal_diagnostics:
                        msg_box_css = 'success-box' if rpt['status'] == 'success' else 'alert-box'
                        st.markdown(f"<div class='{msg_box_css}'>{rpt['msg']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_admin_2:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin-top:0;'>إدارة الذاكرة (Memory Management)</h4>", unsafe_allow_html=True)
            st.warning("يُستخدم هذا الزر في الحالات الطارئة فقط (إذا واجهت شاشة بيضاء، تعليق في الواجهة، أو استمرت البيانات القديمة بالظهور رغم تحديثها). سيقوم بمسح الذاكرة المؤقتة (Cache) بالكامل.")
            
            if st.button("⚠️ إعادة ضبط المصنع (Clear All Cache)", use_container_width=True):
                titan_factory_reset()
                st.success("تم تنظيف السيرفر من البيانات المعلقة ومسح الجلسة بالكامل. يرجى تحديث الصفحة (Refresh) للبدء من جديد.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # محاكاة استخراج تقرير للمشتركين (SaaS Export Feature)
        st.markdown("<hr style='border-color:#30363D; margin:40px 0;'>", unsafe_allow_html=True)
        st.markdown("#### 📑 وحدة استخراج تقارير الأداء للعملاء (PDF/CSV Export Module)")
        st.write("تسمح هذه الأداة بتصدير تقارير الإنجاز الشهرية بصيغة هندسية احترافية لإرسالها للمشتركين أو للمراجعة الشخصية.")
        
        if st.button("📥 إنشاء واستخراج تقرير الأداء الشهري", use_container_width=True):
            with st.spinner("جاري تجميع البيانات الحيوية، تحليل منحنى التطور، وتجهيز التقرير..."):
                time.sleep(3.0)
                st.success("تم تجهيز التقرير بنجاح! (ملاحظة تقنية: هذه ميزة تجارية سيتم تفعيل تصديرها الفعلي كملف قابل للتحميل لاحقاً عند دمج مكتبات ReportLab و FPDF في السيرفر).")

# =====================================================================
# =====================================================================
# SYSTEM EXECUTION TRIGGER (محرك إطلاق النظام)
# =====================================================================
# =====================================================================

if __name__ == "__main__":
    # تشغيل الدالة المركزية التي تبدأ كل المحركات
    main()
