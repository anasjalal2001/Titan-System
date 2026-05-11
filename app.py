import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Black & Gold - Honor Magic 6 Pro Optimized)
# =====================================================================
# إعداد الصفحة الرئيسية لتعمل بكفاءة على شاشات الهواتف الذكية مع منع التمدد العرضي المزعج
st.set_page_config(page_title="Titan Cloud V10 - Master Suite", page_icon="👑", layout="wide")

# هندسة الواجهة الأمامية (Frontend Engineering) باستخدام CSS مخصص
# تم تصميم الألوان لتقليل استهلاك بطارية الهاتف (OLED) وإبراز النصوص باللون الذهبي
st.markdown(
    """
    <style>
        /* الإعدادات الأساسية للخلفية والخطوط */
        .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        h1, h2, h3, h4, h5 { color: #D4AF37 !important; text-align: center; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
        
        /* تصميم الألسنة العلوية (Tabs) بشكل احترافي للجوال */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
        .stTabs [data-baseweb="tab"] { 
            border: 2px solid #D4AF37; background-color: #111111;
            border-radius: 8px; padding: 12px 18px; color: #D4AF37; font-size: 14px; font-weight: bold; transition: 0.3s;
        }
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000000 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
        
        /* البطاقات التفاعلية (Cards) التي تحتوي على المعلومات */
        .titan-card { 
            background: linear-gradient(145deg, #161B22, #0d1117); border: 1px solid rgba(212, 175, 55, 0.3); 
            border-radius: 16px; padding: 25px; margin-bottom: 22px; text-align: center; 
            box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: transform 0.2s;
        }
        .titan-card:hover { transform: translateY(-2px); border-color: rgba(212, 175, 55, 0.8); }
        
        /* النصوص والأرقام البارزة للمقاييس الحيوية */
        .gold-value { color: #FFD700; font-size: 38px; font-weight: 900; margin: 15px 0; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.2); }
        .sub-text { color: #8B949E; font-size: 14px; line-height: 1.6; }
        
        /* بروتوكولات الاستشفاء والطب (تنسيق لوني دقيق للتنبيهات النفسية) */
        .recovery-routine { background: linear-gradient(135deg, #001220, #001f3f); border-right: 6px solid #0074D9; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
        .fertility-safe { background: linear-gradient(135deg, #051409, #0a1910); border-right: 6px solid #2ECC40; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
        .fertility-warning { background: linear-gradient(135deg, #1a0505, #1a0808); border-right: 6px solid #FF4136; padding: 22px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
        
        /* صناديق التنبيهات الخاصة (رسائل النظام) */
        .alert-box { background: rgba(255, 65, 54, 0.1); border: 1px solid #FF4136; padding: 15px; border-radius: 8px; color: #FF4136; text-align: right; margin-bottom: 15px;}
        .success-box { background: rgba(46, 204, 64, 0.1); border: 1px solid #2ECC40; padding: 15px; border-radius: 8px; color: #2ECC40; text-align: right; margin-bottom: 15px;}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 2. الذاكرة المؤقتة (Session State Initialization) للتعافي من الانقطاعات
# =====================================================================
# هذا القسم بالغ الأهمية: يضمن عدم انهيار التطبيق أو فقدان البيانات
# إذا حدث انقطاع في خوادم Google Sheets. البيانات تُحفظ محلياً في ذاكرة التخزين المؤقت.
if 'offline_logs' not in st.session_state:
    st.session_state['offline_logs'] = []
if 'offline_weekly' not in st.session_state:
    st.session_state['offline_weekly'] = []
if 'offline_health' not in st.session_state:
    st.session_state['offline_health'] = []

# =====================================================================
# 3. محرك الاتصال السحابي (المدرع ضد الأخطاء المباشرة وغير المباشرة)
# =====================================================================
def get_db_connection():
    """محاولة الاتصال بالسحاب مع معالجة صامتة للأخطاء لمنع الانهيار"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception:
        return None

def fetch_sheet_safe(sheet_name):
    """جلب البيانات بأمان. إذا فشل الاتصال، يعيد التطبيق جدولاً فارغاً لكي تستمر الواجهة بالعمل"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = conn.read(worksheet=sheet_name, ttl="0s")
        # تنظيف البيانات من القيم الفارغة التي قد تسبب أخطاء غير متوقعة (NaN/Nulls)
        return df.dropna(how='all')
    except Exception:
        return pd.DataFrame()

def append_to_sheet_safe(sheet_name, new_data_dict):
    """إضافة سطر جديد بأمان. إذا فشل السحاب، يحفظ في الذاكرة المؤقتة لضمان عدم ضياع تعب المستخدم"""
    conn = get_db_connection()
    if not conn:
        # مسار الحفظ المحلي البديل (Offline Fallback Route)
        if sheet_name == "Workout_Logs": 
            st.session_state['offline_logs'].append(new_data_dict)
        elif sheet_name == "Health_Log": 
            st.session_state['offline_health'].append(new_data_dict)
        return False, "تم الحفظ في الذاكرة المؤقتة (فشل الاتصال السحابي)."
    
    try:
        # قراءة الشيت الحالي
        df = conn.read(worksheet=sheet_name, ttl="0s")
        new_row = pd.DataFrame([new_data_dict])
        
        # دمج البيانات
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
        # تحديث الشيت السحابي
        conn.update(worksheet=sheet_name, data=updated_df)
        return True, "تم الحفظ في قاعدة بيانات جوجل بنجاح."
    except Exception as e:
        return False, f"جوجل ترفض التعديل. تأكد من صلاحيات المحرر (Editor). الخطأ التفصيلي: {e}"

def overwrite_sheet_safe(sheet_name, df_new):
    """استبدال كامل للبيانات (يستخدم حصرياً للجدول الأسبوعي لأنه يتبدل كل أسبوع)"""
    conn = get_db_connection()
    if not conn:
        st.session_state['offline_weekly'] = df_new.to_dict('records')
        return False, "تم الحفظ في الذاكرة المحلية فقط للمخطط الأسبوعي."
    
    try:
        conn.update(worksheet=sheet_name, data=df_new)
        return True, "تم اعتماد المخطط الأسبوعي سحابياً بنجاح."
    except Exception as
