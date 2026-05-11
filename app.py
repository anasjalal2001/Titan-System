import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Black & Gold)
# =====================================================================
st.set_page_config(page_title="Titan Cloud V9", page_icon="👑", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, h4 { color: #D4AF37 !important; text-align: center; font-weight: bold; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; margin-bottom: 20px;}
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #121212;
        border-radius: 10px; padding: 10px 20px; color: #D4AF37; font-size: 15px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000 !important; }
    .titan-card { 
        background: #1A1C23; border: 1px solid rgba(212, 175, 55, 0.5); 
        border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: center; 
    }
    .gold-value { color: #FFD700; font-size: 38px; font-weight: bold; margin: 15px 0; }
    .daily-recovery { background: linear-gradient(145deg, #001f3f, #000000); border-right: 6px solid #0074D9; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-safe { background: #0a1910; border-right: 6px solid #2ECC40; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
    .fertility-warning { background: #1a0808; border-right: 6px solid #FF4136; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: right; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. محرك الاتصال السحابي الحقيقي (Google Sheets Engine)
# =====================================================================
def get_db_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        st.error(f"⚠️ خطأ في تهيئة الاتصال السحابي: {e}")
        return None

def append_to_sheet(worksheet_name, new_data_dict):
    """دالة تقوم بجلب البيانات، إضافة السطر الجديد، ورفعها مرة أخرى لجوجل"""
    conn = get_db_connection()
    if not conn: return False
    
    try:
        # قراءة البيانات الحالية
        df = conn.read(worksheet=worksheet_name, ttl="0s")
        # تحويل البيانات الجديدة إلى DataFrame
        new_row = pd.DataFrame([new_data_dict])
        # دمج البيانات
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
        # رفع البيانات المحدثة
        conn.update(worksheet=worksheet_name, data=updated_df)
        return True
    except Exception as e:
        # لو جوجل رفض التعديل بيطلع لك هذا الخطأ المباشر
        st.error(f"❌ جوجل شيتس يرفض الكتابة! هل أضفت Service Account في الـ Secrets؟ التفاصيل: {e}")
        return False

# =====================================================================
# 3. هندسة التمارين وتوازن العضلات
# =====================================================================
WORKOUT_ENGINE = {
    "موتيف 8": "صدر + تراي", "فت كومبات": "أرجل + بطن", "كور اكستريم": "أكتاف + جوانب",
    "ستيب": "ظهر + باي", "اكوا": "حديد شامل (Full Body)", "بامب فت": "صدر + أكتاف",
    "بودي ماكس": "أرجل + ظهر", "رادير": "ذراعين (باي وتراي)", "جي فت": "حديد قوة (Heavy Lift)",
    "فت اتاك": "أرجل + أكتاف", "موبيلتي": "تمرين حر (العضلة الضعيفة)", "لا يوجد": "تمرين حر متكامل"
}

# =====================================================================
# 4. واجهة التطبيق الرئيسية (Main App)
# =====================================================================
def main():
    days_map = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_map[datetime.now().strftime("%A")]
    current_date = datetime.now().strftime("%Y-%m-%d")

    st.markdown(f"<h1>👑 غرفة عمليات تايتان: {today_ar}</h1>", unsafe_allow_html=True)

    tab_ops, tab_setup, tab_tracker, tab_clinic, tab_fuel = st.tabs([
        "🚀 العمليات המيدانية", "🗓️ هندسة الأسبوع", "🏋️ سجل التطور", "📸 عيادة InBody", "🥗 الوقود والنوم"
    ])

    # -----------------------------------------------------------------
    # اللسان 1: العمليات الميدانية والجاكوزي
    # -----------------------------------------------------------------
    with tab_ops:
        if today_ar == "الجمعة":
            st.markdown("""
            <div class='titan-card' style='border: 2px solid #2ECC40;'>
                <h1 style='color: #2ECC40; font-size: 65px; margin:0;'>OFF DAY 🛑</h1>
                <p style='font-size: 22px;'>يوم الراحة المقدس. استشفاء سلبي لبناء الأنسجة العضلية.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            col_t1, col_t2 = st.columns([1.5, 1])
            with col_t1:
                st.markdown("""
                <div class='titan-card' style='text-align: right; padding: 20px;'>
                    <h3 style='margin-top:0;'>⏰ التوقيت الميداني (بودي ماسترز)</h3>
                    <hr style='border-color: #333;'>
                    <h4>🚗 الانطلاق من جدة: <span style='color:#D4AF37;'>08:10 م</span></h4>
                    <h4>🅿️ الوصول للمواقف: <span style='color:#D4AF37;'>08:35 م</span></h4>
                    <h4>🔥 التسخين: <span style='color:#D4AF37;'>08:40 م</span> <small>(10 دق سير + 10 دق أوبتيكال)</small></h4>
                    <h4>💪 دخول الكلاس: <span style='color:#D4AF37;'>09:00 م</span></h4>
                </div>
                """, unsafe_allow_html=True)
            with col_t2:
                st.markdown("<div class='titan-card' style='padding: 20px;'><h3 style='margin-top:0;'>أزرار التحكم</h3>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل (زحمة)", use_container_width=True): st.warning("اقطع الأوبتيكال فوراً، واكتفِ بـ 5 دقائق سير.")
                st.write("") 
                if st.button("❌ غياب اليوم", use_container_width=True): st.error("تم تسجيل الغياب. قلل الكربوهيدرات في العشاء.")
                st.markdown("</div>", unsafe_allow_html=True)

            # بروتوكول الاستشفاء والخصوبة (عاد كما طلبت)
            st.markdown("### 🧊 بروتوكول الاستشفاء الطبي")
            
            st.markdown("""
            <div class='daily-recovery'>
                <h4 style='color:#0074D9; margin-top:0;'>🏊 الأساس اليومي (إلزامي بعد التمرين)</h4>
                <p style='font-size: 18px; margin:0;'>
                1. <b>سباحة هادئة:</b> 15 - 20 دقيقة لفكفكة العضلات.<br>
                2. <b>الجاكوزي البارد:</b> 3 دقائق كاملة (إلزامي لتقليل الالتهاب ورفع التستوستيرون).</p>
            </div>
            """, unsafe_allow_html=True)

            if today_ar in ["الاثنين", "الخميس"]:
                st.markdown("""
                <div class='fertility-warning'>
                    <h4 style='color:#FF4136; margin-top:0;'>🔥 تصريح حراري مؤقت (يفتح اليوم فقط)</h4>
                    <p style='font-size: 17px; margin:0;'>
                    يُسمح لك اليوم بدخول <b>(الجاكوزي الحار، الساونا، أو البخار)</b>.<br>
                    <b style='color:#FFD700;'>شرط طبي إلزامي:</b> الحد الأقصى <b>10 دقائق فقط</b>، ويتبعها دش بارد جداً فور الخروج لحماية الخصوبة.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='fertility-safe'>
                    <h4 style='color:#2ECC40; margin-top:0;'>🛡️ حظر حراري (لحماية الخصوبة)</h4>
                    <p style='font-size: 17px; margin:0;'>
                    <b>ممنوع منعاً باتاً</b> دخول الجاكوزي الحار أو الساونا أو البخار هذا اليوم.<br>
                    اكتفِ بالسباحة والجاكوزي البارد فقط لضمان أعلى مستويات الهرمونات.</p>
                </div>
                """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (التأكد من الأرجل)
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ بناء خطة الأسبوع وتوازن العضلات")
        st.info("قم باختيار كلاسات سفيان، وسيقوم النظام بالتأكد من شمولية التمارين (وخاصة الأرجل).")
        
        days_list = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "السبت"]
        with st.form("weekly_plan_form"):
            new_schedule = []
            cols = st.columns(3)
            for i, d in enumerate(days_list):
                with cols[i % 3]:
                    st.write(f"**{d}**")
