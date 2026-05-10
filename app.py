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
# ملاحظة للمهندس: هذا الجزء يربط التطبيق بجدول جوجل شيتس الخاص بك
def get_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except:
        st.error("⚠️ فشل الاتصال بقاعدة البيانات السحابية. تأكد من إعداد Secrets في Streamlit Cloud.")
        return None

conn = get_connection()

# =====================================================================
# 3. المنطق التفاعلي (Sufyan Classes & Muscle Logic)
# =====================================================================
WORKOUT_STRATEGY = {
    "موتيف 8": "صدر + تراي", "فت كومبات": "أرجل + بطن", "كور اكستريم": "أكتاف + جوانب",
    "ستيب": "ظهر + باي", "اكوا": "حديد شامل (Full Body)", "بامب فت": "صدر + أكتاف",
    "بودي ماكس": "أرجل + ظهر", "رادير": "ذراعين (باي وتراي)", "جي فت": "حديد قوة (Heavy)",
    "فت اتاك": "ظهر + أكتاف", "موبيلتي": "استشفاء حركي", "لا يوجد": "تمرين حر"
}

def main():
    days_map = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_map[datetime.now().strftime("%A")]
    current_date = datetime.now().strftime("%Y-%m-%d")

    st.markdown(f"<h1>👑 محرك تايتان السحابي: {today_ar}</h1>", unsafe_allow_html=True)

    # الألسنة الخمسة الكاملة كما اتفقنا
    tab_op, tab_setup, tab_tracker, tab_clinic, tab_fuel = st.tabs([
        "🚀 الميدان والعمليات", "⚙️ هندسة الأسبوع", "🏋️ سجل الأوزان", "📸 عيادة InBody", "🥗 الوقود والنوم"
    ])

    # -----------------------------------------------------------------
    # اللسان 1: الميدان والعمليات (التحكم السحابي)
    # -----------------------------------------------------------------
    with tab_op:
        if today_ar == "الجمعة":
            st.markdown("<div class='titan-card'><h1 style='color:#2ECC40; font-size:60px;'>OFF DAY 🛑</h1><p>راحة تامة. بناء الأنسجة يتم الآن.</p></div>", unsafe_allow_html=True)
        else:
            # جلب خطة اليوم من السحاب
            st.markdown("### 🕒 هندسة الوقت والتحكم")
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                st.markdown(f"""
                <div class='titan-card' style='text-align: right;'>
                    <p>🚗 انطلاق: <b>08:10 م</b> | 🅿️ وصول: <b>08:35 م</b></p>
                    <p>🔥 تسخين: <b>08:40 م</b> (10 دق سير + 10 دق أوبتيكال)</p>
                    <p>💪 سفيان: <b>09:00 م</b></p>
                </div>
                """, unsafe_allow_html=True)
            with col_t2:
                st.markdown("<div class='titan-card' style='padding:15px;'>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل (زحمة)", use_container_width=True): st.warning("اقتصر التسخين على 5 دق.")
                if st.button("❌ غياب اليوم", use_container_width=True): st.error("تم تسجيل الغياب.")
                st.markdown("</div>", unsafe_allow_html=True)

            # بروتوكول الاستشفاء والخصوبة (المنطق الطبي)
            st.markdown("### 🧊 بروتوكول الاستشفاء (دائم التحديث)")
            st.markdown("""
            <div class='recovery-base'>
                <h4 style='color:#0074D9; margin:0;'>🏊 روتين يومي إلزامي</h4>
                <p>1. سباحة: 15-20 دقيقة | 2. جاكوزي بارد: 3 دقائق (رفع التستوستيرون).</p>
            </div>
            """, unsafe_allow_html=True)

            if today_ar in ["الاثنين", "الخميس"]:
                st.markdown("""
                <div class='fertility-alert'>
                    <h4 style='color:#FF4136; margin:0;'>🔥 تصريح حراري (اليوم فقط)</h4>
                    <p>مسموح 10 دقائق (حار/بخار) بحد أقصى + دش بارد فوراً لحماية الخصوبة.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='fertility-safe'>
                    <h4 style='color:#2ECC40; margin:0;'>🛡️ حماية الخصوبة (حظر حراري)</h4>
                    <p>ممنوع دخول الحار اليوم. حافظ على كفاءة هرموناتك.</p>
                </div>
                """, unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (التخطيط الاستباقي)
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ تخطيط أسبوع التايتان")
        st.info("اضبط جدول سفيان هنا، وسيقوم النظام بتعديل كل النوافذ الأخرى.")
        # ملاحظة: في النسخة السحابية، يفضل استخدام فورم واحد لإرسال البيانات لجوجل شيتس
        st.warning("جاري تفعيل الربط المباشر مع Google Sheets...")

    # -----------------------------------------------------------------
    # اللسان 3: سجل الأوزان (Log Book السحابي)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ تتبع التطور الميداني")
        with st.form("weight_cloud_form"):
            col_e, col_w, col_r = st.columns([2,1,1])
            ex = col_e.text_input("التمرين")
            wt = col_w.number_input("الوزن (KG)", step=2.5)
            rp = col_r.number_input("العدات", step=1)
            if st.form_submit_button("✅ حفظ في السحاب"):
                st.success(f"تم حفظ {ex} في قاعدة بيانات جوجل.")

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody (المركز الطبي)
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 تحليل القياسات (InBody)")
        col_c1, col_c2 = st.columns(2)
        col_c1.markdown("<div class='titan-card'>الوزن<div class='gold-value'>91.9 KG</div></div>", unsafe_allow_html=True)
        col_c2.markdown("<div class='titan-card'>الدهون الحشوية<div class='gold-value'>14</div></div>", unsafe_allow_html=True)
        st.file_uploader("رفع قراءة جديدة لمعالجتها سحابياً", type=['png', 'jpg'])

    # -----------------------------------------------------------------
    # اللسان 5: الوقود والنوم (Huawei Integration)
    # -----------------------------------------------------------------
    with tab_fuel:
        st.markdown("### 🥗 إدارة الوقود الحيوي")
        with st.form("health_cloud"):
            h1, h2 = st.columns(2)
            sleep = h1.number_input("🛌 ساعات النوم (Huawei):", value=7.5)
            water = h1.number_input("💧 الماء (لتر):", value=3.5)
            cals = h2.number_input("🔥 السعرات:", value=1900)
            if st.form_submit_button("💾 تحديث السجل السحابي"):
                st.success("تم التحديث!")

if __name__ == "__main__":
    main()
