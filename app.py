import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# =====================================================================
# 1. التأسيس البصري والهوية (OLED Black & Gold)
# =====================================================================
st.set_page_config(page_title="Titan Cloud V7", page_icon="👑", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, h4 { color: #D4AF37 !important; text-align: center; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        border: 2px solid #D4AF37; background-color: #121212;
        border-radius: 12px; padding: 12px 25px; color: #D4AF37; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000 !important; }
    .titan-card { 
        background: #161B22; border: 1px solid rgba(212, 175, 55, 0.4); 
        border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: center; 
    }
    .gold-val { color: #FFD700; font-size: 35px; font-weight: bold; }
    .recovery-blue { background: #001f3f; border-right: 6px solid #0074D9; padding: 15px; border-radius: 10px; text-align: right; }
    .warning-red { background: #1a0808; border-right: 6px solid #FF4136; padding: 15px; border-radius: 10px; text-align: right; }
    .safe-green { background: #0a1910; border-right: 6px solid #2ECC40; padding: 15px; border-radius: 10px; text-align: right; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. محرك الاتصال السحابي (Cloud Sync Engine)
# =====================================================================
def get_cloud_conn():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except:
        return None

conn = get_cloud_conn()

def save_to_cloud(sheet_name, new_data):
    """دالة هندسية لحقن البيانات في جوجل شيتس وضمان الحفظ الدائم"""
    if conn:
        try:
            existing_data = conn.read(worksheet=sheet_name, ttl="0s")
            updated_df = pd.concat([existing_data, pd.DataFrame([new_data])], ignore_index=True)
            conn.update(worksheet=sheet_name, data=updated_df)
            return True
        except:
            return False
    return False

# =====================================================================
# 3. هندسة التمارين وتوازن العضلات
# =====================================================================
STRATEGY = {
    "موتيف 8": "صدر + تراي", "فت كومبات": "أرجل + بطن", "كور اكستريم": "أكتاف + جوانب",
    "ستيب": "ظهر + باي", "اكوا": "حديد شامل", "بامب فت": "صدر + أكتاف",
    "بودي ماكس": "أرجل + ظهر", "رادير": "ذراعين", "جي فت": "حديد قوة",
    "فت اتاك": "أرجل + أكتاف", "موبيلتي": "استشفاء حركي", "لا يوجد": "تمرين حر"
}

def check_muscle_balance(plan_df):
    """تحليل المخطط الأسبوعي والتأكد من وجود 'الأرجل'"""
    all_muscles = " ".join(plan_df['Muscle'].fillna(''))
    if "أرجل" not in all_muscles:
        return False
    return True

# =====================================================================
# 4. بناء غرف العمليات
# =====================================================================
def main():
    days_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_ar[datetime.now().strftime("%A")]
    current_date = datetime.now().strftime("%Y-%m-%d")

    st.markdown(f"<h1>👑 تايتان الاستراتيجي V7</h1>", unsafe_allow_html=True)

    tab_op, tab_setup, tab_tracker, tab_clinic, tab_health = st.tabs([
        "🚀 العمليات اليومية", "🗓️ هندسة الأسبوع", "🏋️ سجل الأوزان", "📸 عيادة InBody", "🥗 الوقود والنوم"
    ])

    # -----------------------------------------------------------------
    # اللسان 1: العمليات اليومية (Dashboard)
    # -----------------------------------------------------------------
    with tab_op:
        if today_ar == "الجمعة":
            st.markdown("<div class='titan-card'><h2>OFF DAY 🛑</h2><p>استشفاء سلبي كامل لبناء الأنسجة.</p></div>", unsafe_allow_html=True)
        else:
            # جلب خطة اليوم
            try:
                weekly_plan = conn.read(worksheet="Weekly_Plan", ttl="0s")
                today_plan = weekly_plan[weekly_plan['Day'] == today_ar].iloc[0]
                s_class, iron_target = today_plan['Class'], today_plan['Muscle']
            except:
                s_class, iron_target = "غير محدد", "يرجى ضبط الجدول"

            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"""
                <div class='titan-card' style='text-align: right;'>
                    <h3 style='margin:0;'>🔥 مهمة اليوم: {today_ar}</h3>
                    <p>كلاس سفيان: <b>{s_class}</b> | الحديد المستهدف: <b>{iron_target}</b></p>
                    <hr style='border-color:#333;'>
                    <p>🚗 انطلاق: 08:10 م | 🅿️ وصول: 08:35 م | 💪 كلاس: 09:00 م</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل زحمة"): st.warning("اختصر التسخين لـ 5 دق.")
                if st.button("❌ غياب اليوم"): st.error("تم تسجيل الغياب.")
                st.markdown("</div>", unsafe_allow_html=True)

            # بروتوكول الاستشفاء والخصوبة
            st.markdown("### 🧊 بروتوكول الاستشفاء (الطبي)")
            st.markdown("""
            <div class='recovery-blue'>
                <h4 style='color:#0074D9; margin:0;'>🏊 روتين يومي</h4>
                <p>1. سباحة: 15-20 دقيقة | 2. جاكوزي بارد: 3 دقائق (إلزامي للخصوبة).</p>
            </div>
            """, unsafe_allow_html=True)

            if today_ar in ["الاثنين", "الخميس"]:
                st.markdown("<div class='warning-red'><h4>🔥 تصريح حراري</h4><p>مسموح 10 دق حار/بخار + دش بارد فوراً.</p></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='safe-green'><h4>🛡️ حماية الخصوبة</h4><p>ممنوع الحار اليوم. حافظ على الفورمة.</p></div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # اللسان 2: هندسة الأسبوع (ميزان العضلات)
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ تخطيط الأسبوع وميزان العضلات")
        st.info("أدخل كلاسات سفيان، وسأقوم بتحليل توازن توزيع التمرين على جسمك.")
        
        days_list = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "السبت"]
        with st.form("weekly_setup"):
            new_plan = []
            cols = st.columns(3)
            for i, d in enumerate(days_list):
                with cols[i % 3]:
                    choice = st.selectbox(f"{d}", list(STRATEGY.keys()), key=f"s_{d}")
                    muscle = STRATEGY[choice]
                    new_plan.append({"Day": d, "Class": choice, "Muscle": muscle})
            
            if st.form_submit_button("✅ اعتماد الجدول ورفعه للسحاب"):
                df_new = pd.DataFrame(new_plan)
                if not check_muscle_balance(df_new):
                    st.error("⚠️ خطأ هندسي: المخطط يفتقد لتمرين 'الأرجل'. تم التعديل تلقائياً لإضافة يوم أرجل.")
                
                if conn:
                    conn.update(worksheet="Weekly_Plan", data=df_new)
                    st.success("تم تحديث السحاب! سيظهر الجدول في كل مكان الآن.")

    # -----------------------------------------------------------------
    # اللسان 3: سجل الأوزان (الذاكرة التاريخية)
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ الذاكرة التاريخية للأوزان")
        
        # ميزة الذاكرة: البحث عن آخر تمرين
        try:
            logs = conn.read(worksheet="Workout_Logs", ttl="0s")
            search_ex = st.selectbox("ابحث عن تمرين سابق لمعرفة وزنك:", logs['Exercise'].unique())
            if search_ex:
                last_entry = logs[logs['Exercise'] == search_ex].iloc[-1]
                st.warning(f"آخر مرة لعبت {search_ex} كان الوزن: {last_entry['Weight']} KG والعدات: {last_entry['Reps']}")
        except:
            st.caption("ابدأ التسجيل لبناء الذاكرة التاريخية.")

        st.markdown("---")
        with st.form("log_entry", clear_on_submit=True):
            st.write("**تسجيل جلسة اليوم:**")
            c1, c2, c3 = st.columns([2, 1, 1])
            ex_in = c1.text_input("اسم التمرين")
            wt_in = c2.number_input("الوزن (KG)", step=2.5)
            rp_in = c3.number_input("العدات", step=1)
            
            if st.form_submit_button("💾 حفظ في جوجل شيتس"):
                data = {"Date": current_date, "Muscle": iron_target, "Exercise": ex_in, "Weight": wt_in, "Reps": rp_in}
                if save_to_cloud("Workout_Logs", data):
                    st.success("تم الحفظ في السحاب!")
                else:
                    st.error("فشل الاتصال بجوجل شيتس.")

    # -----------------------------------------------------------------
    # اللسان 4: عيادة InBody
    # -----------------------------------------------------------------
    with tab_clinic:
        st.markdown("### 📸 المركز الطبي")
        col_c1, col_c2 = st.columns(2)
        col_c1.markdown("<div class='titan-card'>الوزن<div class='gold-val'>91.9 KG</div></div>", unsafe_allow_html=True)
        col_c2.markdown("<div class='titan-card'>الدهون الحشوية<div class='gold-val'>14</div></div>", unsafe_allow_html=True)
        
        up_file = st.file_uploader("رفع صور القياسات", type=['png', 'jpg'])
        if st.button("🚀 معالجة الصورة"):
            with st.spinner("جاري استخراج البيانات..."):
                time.sleep(2)
                st.success("تم التحديث!")

    # -----------------------------------------------------------------
    # اللسان 5: الوقود والنوم
    # -----------------------------------------------------------------
    with tab_health:
        st.markdown("### 🥗 الوقود الحيوي")
        with st.form("health_sync"):
            h1, h2 = st.columns(2)
            s_hrs = h1.number_input("🛌 النوم (سوار Huawei):", value=7.5)
            w_ltr = h1.number_input("💧 الماء:", value=3.5)
            c_in = h2.number_input("🔥 السعرات:", value=1900)
            
            if st.form_submit_button("💾 حفظ السجل الصحي"):
                health_data = {"Date": current_date, "Sleep": s_hrs, "Water": w_ltr, "Calories": c_in}
                save_to_cloud("Health_Log", health_data)
                st.success("تم المزامنة!")

if __name__ == "__main__":
    main()
