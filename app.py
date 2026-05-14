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
    page_title="Titan Enterprise SaaS", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_makkah_time() -> datetime:
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# =====================================================================
# 2. ADVANCED FRONTEND ENGINEERING (CSS Architecture)
# =====================================================================

def inject_premium_css():
    """هندسة بصرية متطورة بدون مسافات تكسر التصميم"""
    css_code = "".join([
        "<style>",
        ".stApp { background-color: #030406; color: #E8ECEF; font-family: 'Inter', -apple-system, sans-serif; }",
        "h1, h2, h3, h4, h5, h6 { color: #E5B94C !important; text-align: right; font-weight: 900; letter-spacing: 0.5px; margin-bottom: 20px; text-transform: uppercase; }",
        ".stTabs [data-baseweb='tab-list'] { gap: 15px; justify-content: center; background: #0A0D14; padding: 20px; border-radius: 20px; border: 1px solid #1F2937; margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }",
        ".stTabs [data-baseweb='tab'] { background-color: #0D1117; border: 1px solid #30363D; border-radius: 12px; padding: 15px 30px; color: #8B949E; font-size: 16px; font-weight: 700; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }",
        ".stTabs [aria-selected='true'] { background-color: rgba(229, 185, 76, 0.15) !important; border-color: #E5B94C !important; color: #E5B94C !important; box-shadow: 0 0 25px rgba(229, 185, 76, 0.2); transform: scale(1.08) translateY(-2px); }",
        ".titan-card { background: linear-gradient(145deg, #0D1117, #080A0F); border: 1px solid #30363D; border-radius: 24px; padding: 35px; margin-bottom: 30px; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.7); transition: all 0.3s ease; }",
        ".titan-card:hover { border-color: #E5B94C; transform: translateY(-5px); box-shadow: 0 30px 60px rgba(0,0,0,0.9); }",
        ".titan-card-center { text-align: center; }",
        ".premium-value { color: #E5B94C; font-size: 42px; font-weight: 900; margin: 15px 0; font-family: 'Monaco', monospace; text-shadow: 0 0 15px rgba(229, 185, 76, 0.3); }",
        ".data-label { color: #8B949E; font-size: 15px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; }",
        ".med-hot { background: rgba(248, 81, 73, 0.08); border-right: 6px solid #F85149; padding: 25px; border-radius: 15px; margin-top: 20px; text-align: right; }",
        ".med-cold { background: rgba(88, 166, 255, 0.08); border-right: 6px solid #58A6FF; padding: 25px; border-radius: 15px; margin-top: 20px; text-align: right; }",
        ".med-neutral { background: rgba(46, 160, 67, 0.08); border-right: 6px solid #2EA043; padding: 25px; border-radius: 15px; margin-top: 20px; text-align: right; }",
        ".med-danger { background: rgba(210, 153, 34, 0.08); border-right: 6px solid #D29922; padding: 25px; border-radius: 15px; margin-top: 20px; text-align: right; }",
        ".alert-box { background: rgba(248, 81, 73, 0.15); border: 2px solid #F85149; padding: 25px; border-radius: 15px; color: #F85149; text-align: right; margin-bottom: 25px; font-weight: 800; box-shadow: 0 10px 20px rgba(248, 81, 73, 0.1); }",
        ".success-box { background: rgba(46, 160, 67, 0.15); border: 2px solid #2EA043; padding: 25px; border-radius: 15px; color: #2EA043; text-align: right; margin-bottom: 25px; font-weight: 800; }",
        ".stButton > button { background: linear-gradient(90deg, #E5B94C, #B8860B); color: #000; border-radius: 10px; border: none; font-weight: 900; padding: 12px 24px; transition: all 0.3s ease; width: 100%; }",
        ".stButton > button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(229, 185, 76, 0.4); }",
        "</style>"
    ])
    st.markdown(css_code, unsafe_allow_html=True)

inject_premium_css()

# =====================================================================
# 3. ENTERPRISE STATE MANAGEMENT
# =====================================================================
def init_titan_states():
    if 'attendance_mode' not in st.session_state: st.session_state['attendance_mode'] = "Full"
    if 'selected_origin_loc' not in st.session_state: st.session_state['selected_origin_loc'] = "المنزل (جدة - المروة)"
    if 'daily_protein' not in st.session_state: st.session_state['daily_protein'] = 0
    if 'daily_cals' not in st.session_state: st.session_state['daily_cals'] = 0
    if 'swim_cals_burned' not in st.session_state: st.session_state['swim_cals_burned'] = 0
    if 'ai_vision_scans_left' not in st.session_state: st.session_state['ai_vision_scans_left'] = 20
    if 'last_sync_timestamp' not in st.session_state: st.session_state['last_sync_timestamp'] = ""

def titan_factory_reset():
    st.cache_resource.clear()
    st.cache_data.clear()
    for k in list(st.session_state.keys()): del st.session_state[k]

# =====================================================================
# 4. SECURE CLOUD CONNECTORS & OMNI-HEAL
# =====================================================================
@st.cache_resource(ttl=900)
def connect_to_cloud_storage():
    try: return st.connection("gsheets", type=GSheetsConnection)
    except Exception: return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_enterprise_data(worksheet_name: str) -> pd.DataFrame:
    conn = connect_to_cloud_storage()
    if not conn: return pd.DataFrame()
    try: return conn.read(worksheet=worksheet_name, ttl=600).dropna(how='all')
    except Exception: return pd.DataFrame()

def secure_push_data(worksheet_name: str, payload_dict: dict):
    conn = connect_to_cloud_storage()
    if not conn: return False, "OFFLINE_MODE"
    try:
        live_df = conn.read(worksheet=worksheet_name, ttl=0) 
        new_df = pd.DataFrame([payload_dict]) if live_df.empty else pd.concat([live_df, pd.DataFrame([payload_dict])], ignore_index=True)
        conn.update(worksheet=worksheet_name, data=new_df)
        st.cache_data.clear() 
        return True, "SYNC_SUCCESS"
    except Exception as e: return False, str(e)

def master_overwrite(worksheet_name: str, master_df: pd.DataFrame):
    conn = connect_to_cloud_storage()
    if not conn: return False, "CONN_FAIL"
    try:
        conn.update(worksheet=worksheet_name, data=master_df)
        st.cache_data.clear()
        return True, "MASTER_SYNC_OK"
    except Exception as e: return False, str(e)

def run_omni_heal_diagnostics():
    diagnostic_report = []
    conn = connect_to_cloud_storage()
    if not conn: return [{"status": "error", "msg": "انقطاع في خادم جوجل المركزي."}]
        
    enterprise_schemas = {
        "Weekly_Plan": ["Day", "Date", "Class", "Muscle", "Status"],
        "Workout_Logs": ["Date", "Muscle", "Exercise", "Weight", "Reps"],
        "Health_Log": ["Date", "Sleep", "Water", "Protein", "Calories", "Notes"],
        "InBody_Logs": ["Date", "Weight", "Muscle_Mass", "Fat_Percentage", "Visceral_Fat"],
        "SaaS_Settings": ["Config_Key", "Config_Value"]
    }
    
    for sheet, required_cols in enterprise_schemas.items():
        try:
            df = conn.read(worksheet=sheet, ttl=0)
            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                for c in missing: df[c] = ""
                conn.update(worksheet=sheet, data=df)
                diagnostic_report.append({"status": "success", "msg": f"تم ترميم الأعمدة المفقودة في `{sheet}`."})
            else:
                diagnostic_report.append({"status": "success", "msg": f"الورقة `{sheet}` سليمة بنيوياً."})
        except Exception:
            try:
                conn.update(worksheet=sheet, data=pd.DataFrame(columns=required_cols))
                diagnostic_report.append({"status": "success", "msg": f"تم بناء قاعدة `{sheet}` مفقودة."})
            except Exception as e:
                diagnostic_report.append({"status": "error", "msg": f"فشل بناء `{sheet}`. الخطأ: {str(e)}"})
    st.cache_data.clear()
    return diagnostic_report

# =====================================================================
# 5. DYNAMIC ROUTING ENGINE (Haversine Formula)
# =====================================================================
def get_geographic_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R_earth = 6371.0 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a_val = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R_earth * (2 * math.atan2(math.sqrt(a_val), math.sqrt(1 - a_val)))

def calculate_smart_eta(origin_name: str, current_time: datetime):
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
# =====================================================================
def get_recovery_protocol(mode: str, iron_target: str, current_time: datetime) -> str:
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
# =====================================================================
def get_biomechanics_database() -> dict:
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
    return enterprise_db

def get_exercise_options(muscle_group: str) -> list:
    master_db = get_biomechanics_database()
    if not muscle_group or muscle_group == "راحة / غياب": return ["➕ إدخال تمرين جديد (يدوي ذكي)"]
    exercise_names = [ex.get("name", "تمرين غير مصنف") for key, lst in master_db.items() if key in muscle_group for ex in lst]
    if not exercise_names: return ["تمرين مخصص", "➕ إدخال تمرين جديد (يدوي ذكي)"]
    exercise_names = list(set(exercise_names)); exercise_names.sort(); exercise_names.append("➕ إدخال تمرين جديد (يدوي ذكي)")
    return exercise_names

def get_exercise_details(exercise_name: str) -> dict:
    master_db = get_biomechanics_database()
    for group_name, exercises_list in master_db.items():
        for ex in exercises_list:
            if ex.get("name", "") == exercise_name: return ex
    return {
        "name": exercise_name, "reps": "10-12 عدة (نطاق تضخيم أساسي)", "technique": "حافظ على التكنيك السليم وتجنب التأرجح واستخدام الزخم. المدى الحركي الكامل (Full ROM) هو السر الوحيد للتطور.", 
        "breathing": "تنفس منتظم مستمر. لا تحبس أنفاسك أبداً تحت الوزن. زفير قوي مع الجهد الأكبر.", "good_pain": "شد واحتراق إيجابي في بطن العضلة المستهدفة يعقبه تمدد (Pump).", "bad_pain": "أي ألم حاد، طقطقة، أو وخز مفاجئ في المفاصل والأوتار المحيطة."
    }

# =====================================================================
# 8. AI REP IMPUTATION 
# =====================================================================
def fetch_historical_record(exercise_name: str):
    df = fetch_enterprise_data("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past_records = df[df['Exercise'] == exercise_name]
        if not past_records.empty:
            last = past_records.iloc[-1]
            return last.get('Date', 'غير متوفر'), float(last.get('Weight', 0)), int(last.get('Reps', 10))
    return None, 0.0, 0

def predict_smart_reps(exercise_name: str, current_weight: float) -> int:
    date, last_weight, last_reps = fetch_historical_record(exercise_name)
    if date:
        if current_weight > last_weight: return max(last_reps - 2, 6) 
        elif current_weight < last_weight: return last_reps + 2
        else: return last_reps
    return 10

# =====================================================================
# 9. COMMERCIAL NUTRITION DATABASE (Offline Fast-Access)
# =====================================================================
def get_enterprise_food_db() -> dict:
    return {
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
# =====================================================================
def get_class_burn_rates() -> dict:
    return {"موتيف 8": 450, "فت كومبات": 650, "كور اكستريم": 350, "ستيب": 450, "اكوا": 350, "بامب فت": 400, "بودي ماكس": 600, "رادير": 300, "جي فت": 400, "فت اتاك": 600, "موبيلتي": 200, "لا يوجد": 0, "راحة / غياب": 0}

def get_workout_strategy() -> dict:
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
    if plan_df.empty: return True, ""
    all_muscles_text = " ".join(plan_df['Muscle'].astype(str))
    engineering_alerts = []
    if "أرجل" not in all_muscles_text: engineering_alerts.append("🔴 خطأ معماري: المخطط يفتقد لتمارين الأرجل (وهي الأساس الأول لإفراز التستوستيرون وحرق دهون الكرش المستعصية).")
    if "ظهر" not in all_muscles_text: engineering_alerts.append("🔴 خلل في القوام: يجب تدريب الظهر بانتظام لسحب الأكتاف للخلف وتصحيح انحناء العمود الفقري الناتج عن العمل المكتبي.")
    if all_muscles_text.count("صدر") > 2: engineering_alerts.append("🔴 إجهاد هيكلي מفرط: الصدر مستهدف بكثافة عالية جداً في أسبوع واحد، هذا سيؤدي للهدم العضلي والالتهاب ولن تنمو العضلة.")
    if len(engineering_alerts) > 0: return False, "<br><br>".join(engineering_alerts)
    return True, "🟢 التصريح الهندسي: ممتاز. المخطط متوازن تماماً، يهاجم الدهون بقوة، ويضمن الاستشفاء السليم لجميع المفاصل."

def get_dynamic_schedule(attendance_mode: str, origin_loc: str, current_time: datetime) -> tuple:
    eta_mins, distance_km = calculate_smart_eta(origin_loc, current_time)
    arrival_time_obj = current_time + timedelta(minutes=eta_mins)
    iron_start_obj = arrival_time_obj + timedelta(minutes=10)
    iron_end_obj = iron_start_obj + timedelta(minutes=75)
    return current_time.strftime("%I:%M %p"), arrival_time_obj.strftime("%I:%M %p"), iron_start_obj.strftime("%I:%M %p"), iron_end_obj.strftime("%I:%M %p"), arrival_time_obj, distance_km, eta_mins

def get_week_dates(current_time: datetime) -> dict:
    days_since_saturday = (current_time.weekday() + 2) % 7 
    last_saturday_date = current_time - timedelta(days=days_since_saturday)
    return {day: (last_saturday_date + timedelta(days=i)).strftime("%Y-%m-%d") for i, day in enumerate(["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"])}

# --- نهاية الدفعة الثانية ---
