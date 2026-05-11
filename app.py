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
    page_title="Titan V28 - Medical & Biomechanical Masterpiece", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_makkah_time():
    """
    محرك التوقيت الدقيق لمكة المكرمة (UTC+3).
    هذا المحرك يضمن أن النظام يعمل بتوقيت السعودية بغض النظر عن موقع سيرفر Streamlit.
    """
    utc_time = datetime.utcnow()
    makkah_time = utc_time + timedelta(hours=3)
    return makkah_time

# =====================================================================
# 2. ADVANCED FRONTEND ENGINEERING (CSS)
# =====================================================================
def inject_custom_css():
    """
    مكتبة التصميم الشاملة.
    تم بناء فئات CSS مخصصة لكل قسم (الاستشفاء الطبي، الملاحة، السجل)
    لضمان واجهة احترافية لا تقل جودة عن التطبيقات المدفوعة.
    """
    css_code = """
    <style>
        /* الإعدادات الأساسية والخلفية */
        .stApp { 
            background-color: #050505; 
            color: #F0F0F0; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        }
        
        h1, h2, h3, h4, h5 { 
            color: #D4AF37 !important; 
            text-align: center; 
            font-weight: 900; 
            letter-spacing: 1px; 
            margin-bottom: 15px;
        }
        
        /* تصميم الألسنة (Tabs) لتعمل كأزرار تحكم علوية */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 8px; 
            justify-content: center; 
            margin-bottom: 30px; 
            flex-wrap: wrap; 
        }
        
        .stTabs [data-baseweb="tab"] { 
            border: 2px solid #D4AF37; 
            background-color: #0A0A0A; 
            border-radius: 12px; 
            padding: 12px 18px; 
            color: #D4AF37; 
            font-size: 15px; 
            font-weight: bold; 
            transition: all 0.3s ease; 
        }
        
        .stTabs [aria-selected="true"] { 
            background-color: #D4AF37 !important; 
            color: #000000 !important; 
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); 
            transform: scale(1.05); 
        }
        
        /* البطاقات الاحترافية (Cards) */
        .titan-card { 
            background: linear-gradient(145deg, #11151A, #080A0F); 
            border: 1px solid rgba(212, 175, 55, 0.2); 
            border-radius: 20px; 
            padding: 30px; 
            margin-bottom: 25px; 
            text-align: right; 
            box-shadow: 0 15px 25px rgba(0,0,0,0.8); 
        }
        
        .titan-card-center { 
            text-align: center; 
        }
        
        /* الأرقام الحيوية */
        .gold-value { 
            color: #FFD700; 
            font-size: 40px; 
            font-weight: 900; 
            margin: 15px 0; 
            text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.3); 
        }
        
        /* بروتوكولات الاستشفاء الطبي (Medical Recovery Colors) */
        .medical-hot { 
            background: rgba(255, 65, 54, 0.05); 
            border-right: 6px solid #FF4136; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 15px; 
            text-align: right; 
        }
        
        .medical-cold { 
            background: rgba(0, 116, 217, 0.05); 
            border-right: 6px solid #0074D9; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 15px; 
            text-align: right; 
        }
        
        .medical-swim { 
            background: rgba(46, 204, 64, 0.05); 
            border-right: 6px solid #2ECC40; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 15px; 
            text-align: right; 
        }
        
        .medical-warning { 
            background: rgba(255, 133, 27, 0.05); 
            border-right: 6px solid #FF851B; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 15px; 
            text-align: right; 
        }
        
        /* صناديق التنبيه العامة */
        .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 10px; color: #FF4136; text-align: right; margin-bottom: 15px; font-weight: bold;}
        .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 10px; color: #2ECC40; text-align: right; margin-bottom: 15px; font-weight: bold;}
        
        /* تفاصيل التمارين (Biomechanics) */
        .bio-good { color: #2ECC40; font-weight: bold; }
        .bio-bad { color: #FF4136; font-weight: bold; }
        .bio-breath { color: #0074D9; font-weight: bold; }
        .bio-tech { color: #FFD700; font-weight: bold; }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

inject_custom_css()

# =====================================================================
# 3. ROBUST SESSION STATE MANAGEMENT
# =====================================================================
def initialize_session_states():
    """تهيئة المتغيرات لضمان عدم ضياع البيانات أثناء التصفح"""
    states = [
        'attendance_mode', 'selected_origin_loc', 
        'daily_protein', 'daily_cals', 'swim_cals_burned'
    ]
    
    if 'attendance_mode' not in st.session_state: st.session_state['attendance_mode'] = "Full"
    if 'selected_origin_loc' not in st.session_state: st.session_state['selected_origin_loc'] = "المنزل (جدة - المروة)"
    if 'daily_protein' not in st.session_state: st.session_state['daily_protein'] = 0
    if 'daily_cals' not in st.session_state: st.session_state['daily_cals'] = 0
    if 'swim_cals_burned' not in st.session_state: st.session_state['swim_cals_burned'] = 0

initialize_session_states()

# =====================================================================
# 4. CLOUD DATABASE CONNECTORS (Google Sheets)
# =====================================================================
@st.cache_resource(ttl="10m")
def get_db_connection():
    """اتصال صامت ومأمن بالسحابة"""
    try: 
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception: 
        return None

def fetch_sheet_safe(sheet_name):
    """جلب بيانات آمن يمنع انهيار التطبيق"""
    conn = get_db_connection()
    if conn is None: return pd.DataFrame()
    try: 
        return conn.read(worksheet=sheet_name, ttl="0s").dropna(how='all')
    except Exception: 
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """إضافة سجلات جديدة (تمارين، صحة، انبودي)"""
    conn = get_db_connection()
    if not conn: return False, "لا يوجد اتصال بالإنترنت، لم يتم الحفظ."
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        updated_df = pd.DataFrame([new_data_dict]) if df.empty else pd.concat([df, pd.DataFrame([new_data_dict])], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم التوثيق في قاعدة البيانات بنجاح."
    except Exception as e: 
        return False, f"خطأ في الصلاحيات أو الاتصال: {str(e)}"

def overwrite_sheet_safe(sheet_name, df_new):
    """تحديث شامل لجدول الأسبوع"""
    conn = get_db_connection()
    if not conn: return False, "فشل الاتصال."
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط بنجاح."
    except Exception as e: 
        return False, f"فشل الرفع: {str(e)}"

# =====================================================================
# 5. INTERNAL ROUTING ENGINE (بديل جوجل ماب المدفوع)
# =====================================================================
def haversine_distance(lat1, lon1, lat2, lon2):
    """معادلة رياضية لحساب المسافة الجغرافية بالكيلومتر"""
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_smart_eta(origin_name):
    """حساب وقت الوصول بناءً على المسافة وزحام خط الحرمين/جدة"""
    dest_lat, dest_lon = 21.5768, 39.1620 # بودي ماسترز الروضة
    
    if origin_name == "المنزل (جدة - المروة)":
        origin_lat, origin_lon, base_speed = 21.6214, 39.1989, 50
    elif origin_name == "العمل (جدة)":
        origin_lat, origin_lon, base_speed = 21.5200, 39.1700, 40
    elif origin_name == "العمل (مكة المكرمة)":
        origin_lat, origin_lon, base_speed = 21.4225, 39.8262, 90 # خط سريع
    else:
        origin_lat, origin_lon, base_speed = 21.6214, 39.1989, 50

    distance_km = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    base_time_mins = (distance_km / base_speed) * 60
    
    hour = get_makkah_time().hour
    # مصفوفة الزحام
    if 7 <= hour <= 9: multiplier = 1.5
    elif 13 <= hour <= 15: multiplier = 1.6
    elif 17 <= hour <= 21: multiplier = 1.8
    else: multiplier = 1.1
        
    final_eta_mins = int(base_time_mins * multiplier) + 5 # 5 دقائق مواقف
    return final_eta_mins, distance_km

# =====================================================================
# 6. MEDICAL & CLINICAL RECOVERY DATABASE (قاعدة الاستشفاء الطبي)
# =====================================================================
def get_medical_recovery_protocol(is_high_intensity):
    """
    بروتوكول طبي مفصل للاستشفاء.
    يعالج مشكلة (المسبح، الساونا، البخار، الجاكوزي الحار والبارد) بشكل علمي.
    """
    html = "<div class='titan-card'><h3 style='margin-top:0;'>🏥 العيادة الطبية الرياضية (بروتوكولات الاستشفاء)</h3>"
    
    if is_high_intensity:
        html += """
        <p style='color:#888; text-align:right;'>بما أن المجهود كان عالياً (تمارين أرجل أو كلاس عنيف)، الألياف العضلية ممزقة وحمض اللاكتيك متراكم. سنطبق (العلاج التبايني).</p>
        
        <div class='medical-hot'>
            <h4 style='color:#FF4136; margin:0;'>🔥 المرحلة 1: التوسيع الوعائي (Vasodilation)</h4>
            <p style='margin-top:5px; font-size:15px;'>الهدف: ضخ الدم المحمل بالغذاء للعضلات الممزقة.</p>
            <ul>
                <li><b>غرفة البخار (Steam Room):</b> من 5 إلى 8 دقائق. (أفضل من الساونا الجافة اليوم لترطيب الشعب الهوائية بعد الكارديو).</li>
                <li><b>أو الجاكوزي الحار:</b> 5 دقائق متواصلة.</li>
            </ul>
        </div>
        
        <div class='medical-cold'>
            <h4 style='color:#0074D9; margin:0;'>🧊 المرحلة 2: الانقباض الوعائي (Vasoconstriction)</h4>
            <p style='margin-top:5px; font-size:15px;'>الهدف: عصر الدم الفاسد وحمض اللاكتيك خارج العضلة وتقليل الالتهاب.</p>
            <ul>
                <li><b>الجاكوزي البارد:</b> انزل مباشرة من الحار إلى البارد لمدة دقيقة إلى دقيقتين فقط.</li>
            </ul>
        </div>
        
        <div class='medical-warning'>
            <h4 style='color:#FF851B; margin:0;'>⚠️ تكرار وتحذير طبي (Fertility & CNS)</h4>
            <p style='margin-top:5px; font-size:15px;'>كرر الانتقال بين الحار والبارد <b>3 مرات متتالية</b>. <br><br><b>قاعدة طبية صارمة:</b> يجب أن تكون الدورة الأخيرة هي (الماء البارد). الخروج وجسمك حار يرفع حرارة الخصيتين ويدمر التستوستيرون ويجهد الجهاز العصبي (CNS) مما يمنعك من النوم العميق.</p>
        </div>
        """
    else:
        html += """
        <p style='color:#888; text-align:right;'>المجهود كان متوسطاً (علوي أو حديد فقط). لا نحتاج لإجهاد القلب بالحرارة العالية، سنركز على الاستشفاء النشط.</p>
        
        <div class='medical-swim'>
            <h4 style='color:#2ECC40; margin:0;'>🏊 المرحلة 1: الاستشفاء النشط (Active Recovery)</h4>
            <p style='margin-top:5px; font-size:15px;'>الهدف: تحريك المفاصل بدون ضغط أو أوزان (Zero Impact).</p>
            <ul>
                <li><b>السباحة الهادئة:</b> 15 إلى 20 دقيقة سباحة حرة مستمرة. هذا يفكك تيبس فقرات الظهر والأكتاف.</li>
            </ul>
        </div>
        
        <div class='medical-cold'>
            <h4 style='color:#0074D9; margin:0;'>🧊 المرحلة 2: التبريد العميق (Cold Exposure)</h4>
            <p style='margin-top:5px; font-size:15px;'>الهدف: رفع مستويات التستوستيرون وتقوية المناعة.</p>
            <ul>
                <li><b>الجاكوزي البارد:</b> 3 إلى 5 دقائق متواصلة. التركيز على التنفس العميق أثناء الغطس.</li>
            </ul>
        </div>
        
        <div class='medical-warning'>
            <h4 style='color:#FF851B; margin:0;'>🚫 حظر حراري (No Heat Protocol)</h4>
            <p style='margin-top:5px; font-size:15px;'><b>يُمنع منعاً باتاً</b> الدخول للساونا، البخار، أو الجاكوزي الحار اليوم. الحرارة المتكررة تسبب جفافاً خفياً (Dehydration) يمنع حرق دهون الكرش في اليوم التالي.</p>
        </div>
        """
        
    html += "</div>"
    return html

# =====================================================================
# 7. BIOMECHANICS & EXERCISE DATABASE (التفصيل الطبي للتمارين)
# =====================================================================
def get_biomechanics_db():
    """
    قاعدة بيانات عملاقة تفصل كل تمرين:
    - طريقة الأداء (Technique)
    - التنفس (Breathing)
    - الألم الجيد والسيء (DOMS tracking)
    """
    db = {
        "صدر": [
            {
                "name": "Incline Barbell Bench Press", 
                "reps": "6-8 عدات (للتضخيم وبناء الكتلة)",
                "technique": "اضبط الدكة على زاوية 30 درجة فقط. انزل بالبار حتى يلمس أعلى صدرك ببطء، وادفع بقوة.",
                "breathing": "خذ شهيق عميق وأنت تنزل بالبار، وازفر الهواء بقوة وأنت تدفع للأعلى.",
                "good_pain": "أعلى الصدر، والجزء الأمامي من الكتف.",
                "bad_pain": "ألم وخز في مفصل الكتف الداخلي (هذا يعني أن كوعك مفتوح 90 درجة، يجب ضمه للداخل زاوية 45)."
            },
            {
                "name": "Decline Cable Flys", 
                "reps": "12-15 عدة (للنحت والتشريح)",
                "technique": "قف في منتصف الكيبل. اسحب المقابض من الأعلى إلى الأسفل باتجاه حوضك واعصر عضلة الصدر في الأسفل لمدة ثانية.",
                "breathing": "شهيق عند فتح الذراعين، زفير عند العصر في الأسفل.",
                "good_pain": "أسفل الصدر، والخط الفاصل بين الصدرين.",
                "bad_pain": "ألم في الكتف الأمامي (هذا يعني أنك تدفع الكيبل دفعاً ولا تقوم بحركة 'العناق')."
            },
            {
                "name": "Dips - Chest Focus", 
                "reps": "حتى الفشل العضلي",
                "technique": "مل بجذعك للأمام قليلاً وانزل حتى يصبح كتفك بموازاة كوعك، ثم ادفع.",
                "breathing": "شهيق في النزول، زفير في الصعود.",
                "good_pain": "الصدر السفلي والترايسبس.",
                "bad_pain": "ألم شديد في عظمة القص (منتصف الصدر)، هذا يحدث إذا نزلت بعمق مبالغ فيه ووزنك ثقيل."
            }
        ],
        "ظهر": [
            {
                "name": "Deadlift", 
                "reps": "3-5 عدات (قوة عصبية)",
                "technique": "قف والبار يلامس قصبة ساقك. انزل بحوضك للخلف مع إبقاء ظهرك مستقيماً 100%. ادفع الأرض بقدميك لترفع البار.",
                "breathing": "خذ نفساً عميقاً جداً واحبسه في بطنك قبل الرفع (Bracing)، ازفر بعد أن تتجاوز الركبة في الصعود.",
                "good_pain": "القطنية (أسفل الظهر العضلي)، أوتار الركبة، والمؤخرة.",
                "bad_pain": "ألم حاد أو 'طقطقة' في فقرات العمود الفقري (هذا يعني أن ظهرك كان مقوساً كالقطة، توقف فوراً)."
            },
            {
                "name": "Lat Pulldown - Wide Grip", 
                "reps": "8-12 عدة (لتعريض الظهر)",
                "technique": "أمسك البار بقبضة واسعة. اسحب البار باتجاه أعلى صدرك مع إرجاع لوحي كتفك للخلف.",
                "breathing": "زفير أثناء السحب للأسفل، شهيق أثناء إرجاع البار للأعلى ببطء.",
                "good_pain": "عضلة المجنص (تحت الإبط والظهر الجانبي).",
                "bad_pain": "ألم أو شد في البايسبس أو الساعد (هذا يعني أنك تسحب بيدك، تخيل أن يدك مجرد 'خطاف' واسحب بكوعك)."
            }
        ],
        "أرجل": [
            {
                "name": "Barbell Squat", 
                "reps": "4-6 عدات (تحفيز هرموني شامل)",
                "technique": "ضع البار على ترابيسك. افتح قدميك باتساع الكتف. انزل للخلف وكأنك تجلس على كرسي حتى توازي فخذيك الأرض.",
                "breathing": "شهيق عميق قبل النزول (Bracing)، زفير قوي عند الدفع للوقوف.",
                "good_pain": "الفخذ الأمامي (الرباعيات) وعضلات المؤخرة (الجلوتس).",
                "bad_pain": "ألم في صابونة الركبة من الأمام، أو أسفل الظهر (دليل على انحناء الظهر للأمام أثناء النزول)."
            },
            {
                "name": "Bulgarian Split Squat", 
                "reps": "10-12 عدة لكل رجل (لنحت الأرجل)",
                "technique": "ضع قدمك الخلفية على دكة. انزل بحوضك للأسفل وليس للأمام. حافظ على استقامة الجذع.",
                "breathing": "شهيق في النزول، زفير في الصعود.",
                "good_pain": "المؤخرة، الفخذ الأمامي للرجل الأمامية.",
                "bad_pain": "ألم في كاحل الرجل الخلفية (موقع القدم خاطئ)."
            }
        ],
        "أكتاف": [
            {
                "name": "Overhead Barbell Press", 
                "reps": "6-8 عدات",
                "technique": "ادفع البار للأعلى فوق رأسك مباشرة، وأدخل رأسك قليلاً للأمام عند وصول البار للقمة.",
                "breathing": "شهيق قبل الدفع، زفير في الأعلى.",
                "good_pain": "الكتف الأمامي والجانبي.",
                "bad_pain": "ألم في أسفل الظهر (أنت تقوس ظهرك للخلف بشكل مبالغ فيه لرفع الوزن)."
            }
        ],
        "باي": [
            {
                "name": "Barbell Bicep Curl", 
                "reps": "8-10 عدات",
                "technique": "قف مستقيماً. ارفع البار مع تثبيت كوعك بجانب خصرك. لا تتأرجح.",
                "breathing": "زفير عند الرفع، شهيق عند النزول ببطء.",
                "good_pain": "بطن عضلة البايسبس.",
                "bad_pain": "ألم في أسفل الظهر (أنت تتأرجح)، ألم في الساعد الداخلي (القبضة غير مريحة لك، استخدم EZ Bar)."
            }
        ],
        "تراي": [
            {
                "name": "Tricep Rope Pushdown", 
                "reps": "12-15 عدة",
                "technique": "ثبت كوعك بجانب خصرك. ادفع الحبل للأسفل وافتح يديك للخارج في نهاية الحركة.",
                "breathing": "زفير عند الدفع للأسفل، شهيق عند الصعود.",
                "good_pain": "خلف الذراع (الرأس الجانبي).",
                "bad_pain": "ألم في مفصل الكوع نفسه."
            }
        ],
        "بطن": [
            {
                "name": "Cable Crunches", 
                "reps": "10-12 عدة (بوزن ثقيل)",
                "technique": "اجلس على ركبتيك. أمسك الحبل خلف رقبتك. انحنِ للأمام محاولاً إيصال كوعك لركبتك باستخدام عضلات بطنك فقط.",
                "breathing": "زفير قوي وتفريغ الهواء بالكامل عند الانحناء للعصر، شهيق عند الصعود.",
                "good_pain": "عضلات البطن العلوية والوسطى (الـ 6-pack).",
                "bad_pain": "ألم في القطنية (أنت تستخدم ظهرك للسحب وليس بطنك)."
            }
        ]
    }
    
    # قائمة افتراضية لتفادي الأخطاء
    default_ex = {
        "name": "تمرين مخصص", "reps": "10-12", "technique": "حافظ على التكنيك السليم وتدرج في الوزن.",
        "breathing": "زفير عند المجهود (الدفع/السحب)، شهيق في العودة.", "good_pain": "بطن العضلة", "bad_pain": "المفاصل والأربطة"
    }
    
    # تعبئة باقي العضلات تفادياً للأخطاء البرمجية
    for m in ["جوانب", "تمرين حر"]:
        db[m] = [default_ex]
        
    return db

def get_exercise_list(muscle):
    """إرجاع القائمة للعضلة المطلوبة"""
    db = get_biomechanics_db()
    if not muscle or muscle == "راحة / غياب": return ["➕ إدخال تمرين جديد (يدوي ذكي)"]
    names = []
    for k, v in db.items():
        if k in muscle: names.extend([ex["name"] for ex in v])
    if not names: return ["تمرين مخصص", "➕ إدخال تمرين جديد (يدوي ذكي)"]
    
    names = list(set(names))
    names.sort()
    names.append("➕ إدخال تمرين جديد (يدوي ذكي)")
    return names

def get_exercise_info(ex_name):
    """جلب التفاصيل الحيوية للتمرين"""
    db = get_biomechanics_db()
    for group in db.values():
        for ex in group:
            if ex["name"] == ex_name:
                return ex
    return {
        "name": ex_name, "reps": "10-12 عدة", "technique": "أداء حركي كامل المدى (Full ROM).",
        "breathing": "شهيق في النزول، زفير في الدفع.", "good_pain": "العضلة المستهدفة.", "bad_pain": "المفصل."
    }

def calculate_smart_reps(exercise_name, current_weight):
    """محرك كسر الأوزان (Progressive Overload)"""
    df = fetch_sheet_safe("Workout_Logs")
    if not df.empty and 'Exercise' in df.columns:
        past = df[df['Exercise'] == exercise_name]
        if not past.empty:
            lw, lr = float(past.iloc[-1]['Weight']), int(past.iloc[-1]['Reps'])
            if current_weight > lw: return max(lr - 2, 6)
            elif current_weight < lw: return lr + 2
            else: return lr
    return 10

# =====================================================================
# 8. NUTRITION & MACROS ENGINE (حاسبة الأكل السعودي بدون API)
# =====================================================================
FOOD_DATABASE = {
    # بروتينات صافية
    "صدر دجاج مشوي (100 جرام)": {"prot": 31, "cals": 165},
    "تونا بالماء (علبة كاملة)": {"prot": 26, "cals": 120},
    "سكوب بروتين (Whey)": {"prot": 25, "cals": 120},
    "بيض مسلوق (حبة كاملة)": {"prot": 6, "cals": 70},
    "بياض بيض (حبة واحدة)": {"prot": 4, "cals": 17},
    "شريحة لحم عجل (100 جرام)": {"prot": 26, "cals": 250},
    
    # كربوهيدرات
    "أرز أبيض مطبوخ (100 جرام / 5 ملاعق)": {"prot": 3, "cals": 130},
    "شوفان (50 جرام جاف)": {"prot": 7, "cals": 190},
    "بطاطس مشوية (حبة متوسطة)": {"prot": 4, "cals": 160},
    "خبز أسمر (رغيف واحد)": {"prot": 4, "cals": 80},
    
    # وجبات ومطاعم
    "نصف حبة شواية (بدون جلد)": {"prot": 45, "cals": 420},
    "شاورما دجاج (صاروخ عادي)": {"prot": 25, "cals": 550},
    "إيدام دجاج بالبطاطس (صحن وسط)": {"prot": 30, "cals": 350},
    "كبسة دجاج (ربع دجاجة + رز)": {"prot": 35, "cals": 650},
    "برجر لحم مشوي (مفرد)": {"prot": 20, "cals": 400},
    
    # ألبان ومكملات
    "حليب بروتين عالي (ندى/المراعي)": {"prot": 27, "cals": 150},
    "زبادي يوناني سادة": {"prot": 15, "cals": 100},
    
    # أخرى
    "موز (حبة متوسطة)": {"prot": 1, "cals": 105},
    "زبدة فول سوداني (ملعقة طعام)": {"prot": 4, "cals": 95}
}

# =====================================================================
# 9. WEEKLY STRATEGY ENGINE
# =====================================================================
CLASS_BURN = {"موتيف 8": 450, "فت كومبات": 650, "كور اكستريم": 350, "ستيب": 450, "اكوا": 350, "بامب فت": 400, "بودي ماكس": 600, "رادير": 300, "جي فت": 400, "فت اتاك": 600, "موبيلتي": 200, "لا يوجد": 0, "راحة / غياب": 0}
W_ENG = {
    "موتيف 8": {"iron": "صدر + تراي", "flow": "الصدر يحتاج تركيز عالي. ابدأ بالبنش برس."},
    "فت كومبات": {"iron": "أرجل + بطن", "flow": "يوم حرق الدهون العظيم! سكوات ثقيل أولاً."},
    "كور اكستريم": {"iron": "أكتاف + جوانب", "flow": "أكتاف عريضة = خصر أنحف بصرياً."},
    "ستيب": {"iron": "ظهر + باي", "flow": "شد الظهر يمنع التحدب. ركز على السحب."},
    "اكوا": {"iron": "حديد شامل (Full Body)", "flow": "تمرين مركب واحد لكل عضلة كبيرة."},
    "بامب فت": {"iron": "صدر + أكتاف", "flow": "أوزان متوسطة وتكرارات عالية للـ Pump."},
    "بودي ماكس": {"iron": "أرجل + ظهر", "flow": "أعنف يوم! يستهدف أكبر عضلتين لنسف الكرش."},
    "رادير": {"iron": "ذراعين (باي وتراي)", "flow": "Supersets باي مع تراي لزيادة الحرق."},
    "جي فت": {"iron": "حديد قوة (Heavy Lift)", "flow": "3 إلى 5 عدات بأقصى وزن حر."},
    "فت اتاك": {"iron": "أرجل + أكتاف", "flow": "تمارين مركبة سريعة لرفع نبض القلب."},
    "موبيلتي": {"iron": "تمرين حر", "flow": "استهدف عضلة متأخرة أو قم بإطالات عميقة."},
    "لا يوجد": {"iron": "تمرين حر متكامل", "flow": "أنت القائد اليوم."},
    "راحة / غياب": {"iron": "راحة", "flow": "استشفاء وبناء أنسجة."}
}

# =====================================================================
# 10. DIAGNOSTIC SWEEPER
# =====================================================================
def run_diagnostics():
    """يفحص اتصال جوجل شيتس ووجود الأوراق"""
    report = []
    conn = get_db_connection()
    if not conn:
        report.append({"status": "error", "msg": "🔴 انقطاع الاتصال بالسحابة. تحقق من الـ Secrets."})
        return report
    report.append({"status": "success", "msg": "🟢 الاتصال بالسحابة فعال."})
    for s in ["Weekly_Plan", "Workout_Logs", "Health_Log", "InBody_Logs"]:
        try:
            conn.read(worksheet=s, ttl="0s")
            report.append({"status": "success", "msg": f"🟢 ورقة `{s}` متصلة بنجاح."})
        except Exception as e:
            report.append({"status": "error", "msg": f"🔴 ورقة `{s}` غير موجودة. قم بإنشائها في الإكسل."})
    return report

# =====================================================================
# 11. MAIN COMMANDER DASHBOARD
# =====================================================================
def main():
    makkah_now = get_makkah_time()
    days_map = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_map[makkah_now.strftime("%A")]
    current_date = makkah_now.strftime("%Y-%m-%d")
    
    idx_day = (makkah_now.weekday() + 2) % 7 
    sat_date = makkah_now - timedelta(days=idx_day)
    week_dates = {d: (sat_date + timedelta(days=i)).strftime("%Y-%m-%d") for i, d in enumerate(["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"])}

    st.markdown("<h1>👑 محرك تايتان V28 (Medical & Biomechanical Masterpiece)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#888;'>مكة المكرمة | {today_ar} ({current_date}) | الساعة: {makkah_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    t_ops, t_setup, t_log, t_clinic, t_fuel, t_sys = st.tabs(["🚀 الملاحة والميدان", "🗓️ هندسة الأسبوع", "🏋️ علم الحركة الحيوية", "🏥 العيادة والاستشفاء", "🥗 حاسبة الماكروز", "🛠️ الصيانة"])

    # -----------------------------------------------------------------
    # TAB 1: OPERATIONS & NAVIGATION
    # -----------------------------------------------------------------
    with t_ops:
        plan_df = fetch_sheet_safe("Weekly_Plan")
        s_class, iron_target = "موتيف 8", "صدر + تراي" # Default
        if not plan_df.empty and 'Date' in plan_df.columns:
            try:
                r = plan_df[plan_df['Date'] == current_date].iloc[0]
                s_class, iron_target = r['Class'], r['Muscle']
            except: pass

        if today_ar == "الجمعة" or s_class == "راحة / غياب" or st.session_state['attendance_mode'] == "Absent":
            st.markdown("<div class='titan-card titan-card-center' style='border: 2px solid #FF4136;'><h1 style='color:#FF4136; margin:0;'>يوم راحة سلبي 🛑</h1><p>العضلات تنمو الآن. الكربوهيدرات العالية ممنوعة الليلة.</p></div>", unsafe_allow_html=True)
            if st.button("🔄 التراجع والذهاب للنادي"): st.session_state['attendance_mode'] = "Full"; st.rerun()
        else:
            c1, c2 = st.columns([2, 1])
            with c2:
                st.markdown("<div class='titan-card titan-card-center'><h3 style='margin-top:0;'>📍 الملاحة الداخلية</h3>", unsafe_allow_html=True)
                loc = st.selectbox("الانطلاق من:", ["المنزل (جدة - المروة)", "العمل (جدة)", "العمل (مكة المكرمة)"])
                eta_mins, dist = calculate_smart_eta(loc)
                st.markdown(f"<p style='color:#D4AF37;'>مسافة: {dist:.1f} KM | زحام: {eta_mins} دقيقة</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)
                if st.button("✅ كلاس + حديد", use_container_width=True): st.session_state['attendance_mode'] = "Full"; st.rerun()
                if st.button("🏋️ حديد فقط", use_container_width=True): st.session_state['attendance_mode'] = "IronOnly"; st.rerun()
                if st.button("❌ تسجيل غياب", use_container_width=True): st.session_state['attendance_mode'] = "Absent"; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            with c1:
                arr_obj = makkah_now + timedelta(minutes=eta_mins)
                arr_str = arr_obj.strftime("%I:%M %p")
                iron_start = (arr_obj + timedelta(minutes=10)).strftime("%I:%M %p")
                
                st.markdown(f"""
                <div class='titan-card'>
                    <h3 style='margin-top:0;'>🗺️ الميدان (حضور: {st.session_state['attendance_mode']})</h3>
                    <p>الحديد: <b style='color:#FFD700;'>{iron_target}</b> | الكلاس: <b style='color:#FFD700;'>{s_class}</b></p>
                    <hr>
                    <p>🚗 الانطلاق: <b style='color:#D4AF37;'>{makkah_now.strftime("%I:%M %p")}</b> | 🅿️ الوصول: <b style='color:#D4AF37;'>{arr_str}</b></p>
                    <p>🔥 {arr_str} - {iron_start} : إحماء</p>
                    <p>💪 {iron_start} - 09:00 PM : <b style='color:#FF4136;'>صالة الحديد</b></p>
                    <p>🤸 09:00 PM - 09:50 PM : <b style='color:#D4AF37;'>الكلاس (حرق ~{CLASS_BURN.get(s_class, 0)} kcal)</b></p>
                    <p>🧊 10:00 PM : <b style='color:#2ECC40;'>التوجه للعيادة والاستشفاء</b></p>
                </div>
                """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 2: WEEKLY PLAN
    # -----------------------------------------------------------------
    with t_setup:
        st.markdown("### 🗓️ هندسة الأسبوع")
        with st.form("w_plan"):
            ns = []
            cols = st.columns(3)
            opts = list(W_ENG.keys())
            for i, d in enumerate(["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]):
                with cols[i % 3]:
                    c = st.selectbox(f"{d} ({week_dates.get(d,'')})", opts, key=f"c_{d}")
                    ns.append({"Day": d, "Date": week_dates.get(d,""), "Class": c, "Muscle": W_ENG[c]['iron'], "Status": "مجدول"})
            if st.form_submit_button("✅ اعتماد السحابة", use_container_width=True):
                s, m = overwrite_sheet_safe("Weekly_Plan", pd.DataFrame(ns))
                if s: st.success(m)
                else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 3: BIOMECHANICS & LOGS
    # -----------------------------------------------------------------
    with t_log:
        st.markdown("### 🏋️ علم الحركة الحيوية (Biomechanics) وتسجيل الأوزان")
        t_muscle = iron_target
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("<div class='titan-card titan-card-center'><h4 style='margin:0;'>⏱️ مؤقت الراحة</h4>", unsafe_allow_html=True)
            if st.button("90 ثانية (بناء)"): 
                pb = st.progress(0)
                for i in range(90): time.sleep(1); pb.progress((i+1)/90)
                st.success("انتهت الراحة!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"<div class='titan-card' style='text-align:right;'><h4 style='margin-top:0;'>العضلة: <span style='color:#FFD700;'>{t_muscle}</span></h4>", unsafe_allow_html=True)
            ex_list = get_exercise_list(t_muscle)
            s_ex = st.selectbox("اختر التمرين:", ex_list)
            f_ex = st.text_input("اسم التمرين اليدوي:") if "يدوي" in s_ex else s_ex
            f_ex = f_ex if f_ex else "تمرين مخصص"
            
            info = get_exercise_info(f_ex)
            st.markdown(f"""
            <div style='background:#111; padding:15px; border-radius:10px; margin-bottom:15px;'>
                <p><span class='bio-tech'>⚙️ الأداء (Technique):</span> {info['technique']}</p>
                <p><span class='bio-breath'>🫁 التنفس (Breathing):</span> {info['breathing']}</p>
                <p><span class='bio-good'>✅ الألم الجيد:</span> {info['good_pain']}</p>
                <p><span class='bio-bad'>❌ الألم الخطر:</span> {info['bad_pain']}</p>
                <p style='color:#FFD700;'><b>النطاق العلمي: {info['reps']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            df_logs = fetch_sheet_safe("Workout_Logs")
            if not df_logs.empty and 'Exercise' in df_logs.columns and f_ex in df_logs['Exercise'].values:
                last_w = df_logs[df_logs['Exercise'] == f_ex].iloc[-1]['Weight']
                st.write(f"الوزن السابق: {last_w} KG")
            else: last_w = 0.0
            
            cw, cr = st.columns(2)
            w = cw.number_input("الوزن (KG)", value=float(last_w), step=2.5)
            r = cr.number_input("العدات (0 = حساب آلي)", value=0)
            
            if st.button("💾 توثيق الجلسة"):
                f_r = calculate_smart_reps(f_ex, w) if r == 0 else r
                s, m = append_to_sheet_safe("Workout_Logs", {"Date": current_date, "Muscle": t_muscle, "Exercise": f_ex, "Weight": w, "Reps": f_r})
                if s: st.success(f"تم تسجيل {f_ex} بـ {f_r} عدات.")
                else: st.error(m)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # TAB 4: CLINICAL RECOVERY
    # -----------------------------------------------------------------
    with t_clinic:
        st.markdown("### 🏥 العيادة الطبية والاستشفاء (Medical Recovery)")
        is_heavy = today_ar in ["الاثنين", "الخميس"] or "أرجل" in iron_target
        st.markdown(get_medical_recovery_protocol(is_heavy), unsafe_allow_html=True)
        
        st.markdown("#### 🏊 حاسبة الاستشفاء النشط (المسبح)")
        with st.form("swim_form"):
            s_mins = st.number_input("كم دقيقة سبحت اليوم؟", min_value=0, value=15, step=5)
            if st.form_submit_button("حساب السعرات وإضافتها"):
                c_burn = int(s_mins * 8.5) # 8.5 سعرة بالدقيقة للسباحة لوزن 92 كيلو
                st.session_state['swim_cals_burned'] = c_burn
                st.success(f"تم حرق {c_burn} سعرة حرارية من السباحة. (سيتم تسجيلها في التقرير الصحي)")
        
        st.markdown("#### 📸 رفع بيانات InBody")
        with st.form("ib_form"):
            c1, c2 = st.columns(2)
            i_w = c1.number_input("الوزن الإجمالي", value=91.9)
            i_m = c2.number_input("العضلات", value=40.0)
            i_f = c1.number_input("نسبة الدهون %", value=20.0)
            i_v = c2.number_input("الدهون الحشوية", value=14)
            if st.form_submit_button("أرشفة"):
                s, m = append_to_sheet_safe("InBody_Logs", {"Date": current_date, "Weight": i_w, "Muscle_Mass": i_m, "Fat_Percentage": i_f, "Visceral_Fat": i_v})
                if s: st.success("تم الحفظ.")
                else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 5: NUTRITION CALCULATOR (Offline Macro Builder)
    # -----------------------------------------------------------------
    with t_fuel:
        st.markdown("### 🥗 حاسبة الماكروز العميقة (بدون الحاجة لاشتراكات مدفوعة)")
        st.info("قم ببناء وجباتك بالجرام عبر إضافة المكونات وسيتم الحساب تلقائياً.")
        
        c_f1, c_f2 = st.columns(2)
        with c_f2:
            st.markdown("<div class='titan-card' style='text-align:right;'><h4>أضف مكونات طعامك</h4>", unsafe_allow_html=True)
            food_items = list(FOOD_DATABASE.keys())
            sel_food = st.selectbox("اختر الصنف:", food_items)
            qty = st.number_input("الكمية (عدد الحصص المذكورة أعلاه):", min_value=1, value=1)
            
            if st.button("➕ إضافة للعداد اليومي", use_container_width=True):
                st.session_state['daily_protein'] += (FOOD_DATABASE[sel_food]["prot"] * qty)
                st.session_state['daily_cals'] += (FOOD_DATABASE[sel_food]["cals"] * qty)
                st.success(f"تم إضافة {qty} حصة من {sel_food}.")
                
            st.markdown("<hr>", unsafe_allow_html=True)
            st.write("أو إدخال حر سريع:")
            m_p = st.number_input("بروتين", min_value=0)
            m_c = st.number_input("سعرات", min_value=0)
            if st.button("إضافة اليدوي"):
                st.session_state['daily_protein'] += m_p
                st.session_state['daily_cals'] += m_c
                st.success("تمت الإضافة.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_f1:
            tar_prot = int(91.9 * 2.2)
            tar_cals = 1900
            
            st.markdown(f"""
            <div class='titan-card'>
                <h3 style='margin-top:0;'>📊 لوحة الماكروز اليومية</h3>
                <p>البروتين: <b style='color:#FF4136; font-size:30px;'>{st.session_state['daily_protein']} / {tar_prot} g</b></p>
                <p>السعرات المستهلكة: <b style='color:#D4AF37; font-size:30px;'>{st.session_state['daily_cals']} / {tar_cals}</b></p>
                <p>حرق السباحة الإضافي: <b style='color:#2ECC40; font-size:20px;'>- {st.session_state['swim_cals_burned']} kcal</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("health_form"):
                slp = st.number_input("ساعات النوم:", value=7.5, step=0.5)
                wtr = st.number_input("الماء (لتر):", value=3.5, step=0.5)
                if st.form_submit_button("💾 حفظ اليوم في السحابة", use_container_width=True):
                    net_cals = st.session_state['daily_cals'] - st.session_state['swim_cals_burned']
                    s, m = append_to_sheet_safe("Health_Log", {"Date": current_date, "Sleep": slp, "Water": wtr, "Protein": st.session_state['daily_protein'], "Calories": net_cals})
                    if s: 
                        st.success("تم الحفظ بنجاح وتصفير العداد لغدٍ.")
                        st.session_state['daily_protein'] = 0; st.session_state['daily_cals'] = 0; st.session_state['swim_cals_burned'] = 0
                    else: st.error(m)

    # -----------------------------------------------------------------
    # TAB 6: SYSTEM DIAGNOSTICS
    # -----------------------------------------------------------------
    with t_sys:
        st.markdown("### 🛠️ مركز الصيانة والتشخيص")
        if st.button("فحص الرادار الشامل", use_container_width=True):
            for r in run_diagnostics():
                c_box = 'success-box' if r['status'] == 'success' else 'alert-box' if r['status'] == 'error' else 'info-box'
                st.markdown(f"<div class='{c_box}'>{r['msg']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
