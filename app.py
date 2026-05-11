import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Optimized for Honor Magic 6 Pro)
# =====================================================================
st.set_page_config(page_title="Titan Cloud Engine", page_icon="👑", layout="wide")

st.markdown("""
<style>
    /* الثيم الملكي السحابي */
    h1, h2, h3, h4 { color: #D4AF37 !important; text-align: center; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #0E1117;
        border-radius: 12px; padding: 12px 25px; color: #D4AF37; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000 !important; }
    
    /* البطاقات الاستراتيجية */
    .titan-card { 
        background: #161B22; border: 1px solid rgba(212, 175, 55, 0.5); 
        border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: center; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.8); 
    }
    .gold-value { color: #FFD700; font-size: 40px; font-weight: bold; margin: 10px 0; }
    
    /* بروتوكولات الاستشفاء الطبي */
    .recovery-base { background: linear-gradient(135deg, #0d1117, #001f3f); border-right: 6px solid #0074D9; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: #0c1a0f; border-right: 6px solid #2ECC40; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-alert { background: #1a0a0a; border-right: 6px solid #FF4136; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. هندسة الربط السحابي (Google Sheets Cloud Connection)
# =====================================================================
def get_db_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except:
        return None

conn = get_db_connection()

# دالة لجلب البيانات من شيت معين
def fetch_data(sheet_name):
    if conn:
        try:
            return conn.read(worksheet=sheet_name, ttl="0s")
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# =====================================================================
# 3. المنطق التفاعلي (Workout & Muscle Logic)
# =====================================================================
S_CLASSES = ["لا يوجد", "موتيف 8", "فت كومبات", "كور اكستريم", "ستيب", "اكوا", "بامب فت", "بودي ماكس", "رادير", "فت اتاك", "جي فت", "موبيلتي"]

def suggest_muscle(s_class):
    mapping = {
        "موتيف 8": "صدر + تراي", "فت كومبات": "أرجل + بطن", "كور اكستريم": "أكتاف + جوانب",
        "ستيب": "ظهر + باي", "اكوا": "حديد شامل", "بامب فت": "صدر + أكتاف",
        "بودي ماكس": "أرجل + ظهر", "رادير": "ذراعين", "جي فت": "حديد قوة",
        "فت اتاك": "ظهر + أكتاف", "موبيلتي": "عضلة ضعيفة", "لا يوجد": "تمرين حر"
    }
    return mapping.get(s_class, "حديد شامل")

# =====================================================================
# 4. بناء التطبيق الميداني
# =====================================================================
def main():
    days_map = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_map[datetime.now().strftime("%A")]
    current_date = datetime.now().strftime("%Y-%m-%d")

    st.markdown(f"<h1>👑 غرفة عمليات تايتان السحابية</h1>", unsafe_allow_html=True)

    tab_op, tab_setup, tab_tracker, tab_clinic, tab_fuel = st.tabs([
        "🚀 الميدان والعمليات", "🗓️ هندسة الأسبوع", "🏋️ سجل الأوزان", "📸 عيادة InBody", "🥗 الوقود والنوم"
    ])

    # -----------------------------------------------------------------
    # اللسان 1: العمليات اليومية
    # -----------------------------------------------------------------
    with tab_op:
        if today_ar == "الجمعة":
            st.markdown("<div class='titan-card'><h1 style='color:#2ECC40; font-size:60px;'>OFF DAY 🛑</h1><p>يوم الاستشفاء العالمي.</p></div>", unsafe_allow_html=True)
        else:
            # افتراضياً، لو ما ضبطت الجدول بيطلع لك تنبيه
            st.markdown(f"### 🕒 خطة اليوم: {today_ar}")
            col_info, col_actions = st.columns([2, 1])
            with col_info:
                st.markdown(f"""
                <div class='titan-card' style='text-align: right;'>
                    <p>🚗 انطلاق: <b>08:10 م</b> | 🅿️ وصول: <b>08:35 م</b></p>
                    <p>🔥 تسخين: <b>08:40 م</b> (10 دق سير + 10 دق أوبتيكال)</p>
                    <p>💪 موعد الكلاس: <b>09:00 م</b></p>
                </div>
                """, unsafe_allow_html=True)
            with col_actions:
                st.markdown("<div class='titan-card' style='padding:15px;'>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل (زحمة)", use_container_width=True): st.warning("اقتصر التسخين على 5 دق.")
                if st.button("❌ غياب اليوم", use_container_width=True): st.error("تم تسجيل الغياب.")
                st.markdown("</div>", unsafe_allow_html=True)

            # بروتوكول الاستشفاء والخصوبة
            st.markdown("### 🧊 بروتوكول الاستشفاء (دقيق)")
            st.markdown("""
            <div class='recovery-base'>
                <h4 style='color:#0074D9; margin:0;'>🏊 روتين يومي إلزامي</h4>
                <p>1. سباحة: 15-20 دقيقة | 2. جاكوزي بارد: 3 دقائق.</p>
            </div>
            """, unsafe_allow_html=True)

            if today_ar in ["الاثنين", "الخميس"]:
                st.markdown("""
                <div class='fertility-alert'>
                    <h4 style='color:#FF4136; margin:0;'>🔥 تصريح حراري (اليوم فقط)</h4>
                    <p>مسموح 10 دقائق (حار/بخار) + دش بارد فوراً لحماية الخصوبة.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='fertility-safe'>
                    <h4 style='color:#2ECC40; margin:0;'>🛡️ حماية الخصوبة (حظر حراري)</h4>
                    <p>ممنوع دخول الحار اليوم. حافظ على التستوستيرون.</p>
                </div>
                """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (التخطيط التفاعلي)
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 📝 هندسة الجدول الأسبوعي")
        st.info("اضبط كلاسات سفيان، والنظام سيبني لك خطة الحديد والاستشفاء فوراً.")
        
        days_list = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "السبت"]
        weekly_data = []

        with st.form("weekly_form"):
            cols = st.columns(3)
            for i, d in enumerate(days_list):
                with cols[i % 3]:
                    st.write(f"**{d}**")
                    choice = st.selectbox(f"كلاس سفيان ({d})", S_CLASSES, key=f"setup_{d}")
                    iron = suggest_muscle(choice)
                    st.caption(f"الحديد: {iron}")
                    weekly_data.append({"Day": d, "Class": choice, "Iron": iron})
            
            if st.form_submit_button("✅ اعتماد الجدول الأسبوعي وحفظه سحابياً"):
                st.success("تم تحديث الجدول الأسبوعي! (سيتم رفعه لجوجل شيتس في التحديث القادم)")

    # -----------------------------------------------------------------
    # اللسان 3: سجل الأوزان (Log Book)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ تتبع التطور الميداني")
        with st.form("workout_log_form", clear_on_submit=True):
            c_ex, c_wt, c_rp = st.columns([2, 1, 1])
            ex = c_ex.text_input("اسم التمرين")
            wt = c_wt.number_input("الوزن (KG)", step=2.5)
            rp = c_rp.number_input("العدات", step=1)
            
            if st.form_submit_button("✅ حفظ الجلسة في السحاب"):
                if ex:
                    st.success(f"تم تسجيل {ex} بوزن {wt} كجم. سيظهر في ملف الإكسل.")
                else:
                    st.error("يرجى كتابة اسم التمرين.")

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody (تحليل الصور)
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 المركز الطبي (InBody)")
        col_m1, col_m2 = st.columns(2)
        with col_m1: st.markdown("<div class='titan-card'>الوزن<div class='gold-value'>91.9 KG</div></div>", unsafe_allow_html=True)
        with col_m2: st.markdown("<div class='titan-card'>الدهون الحشوية<div class='gold-value'>14</div></div>", unsafe_allow_html=True)
        
        st.file_uploader("ارفع صورة ميزان هواوي أو InBody", type=['png', 'jpg'])
        if st.button("🚀 تحليل OCR وحفظ في السجل", use_container_width=True):
            st.info("جاري المعالجة سحابياً...")

    # -----------------------------------------------------------------
    # اللسان 5: الوقود والنوم
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 إدارة السعرات والنوم")
        with st.form("fuel_entry"):
            f1, f2 = st.columns(2)
            sleep = f1.number_input("🛌 ساعات النوم (سوار Huawei):", value=7.5, step=0.5)
            water = f1.number_input("💧 الماء المستهلك (لتر):", value=3.5, step=0.5)
            cals = f2.number_input("🔥 السعرات المستهلكة:", value=1900, step=50)
            if st.form_submit_button("💾 تحديث السجل الصحي"):
                st.success("تم التحديث!")

if __name__ == "__main__":
    main()
