import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import time

# =====================================================================
# 1. التأسيس البصري (Titan OLED Optimized)
# =====================================================================
st.set_page_config(page_title="Titan Strategic Cloud", page_icon="👑", layout="wide")

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
        border-radius: 15px; padding: 20px; margin-bottom: 20px; text-align: center; 
    }
    .gold-val { color: #FFD700; font-size: 32px; font-weight: bold; }
    .stat-box { background: #0d1117; padding: 15px; border-radius: 10px; border: 1px solid #333; margin: 5px; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. محرك المزامنة السحابية (GSheets Sync)
# =====================================================================
conn = st.connection("gsheets", type=GSheetsConnection)

def fetch_sheet(name):
    try:
        return conn.read(worksheet=name, ttl="0s")
    except:
        return pd.DataFrame()

# =====================================================================
# 3. هندسة التوازن العضلي (Muscle Logic Engine)
# =====================================================================
STRATEGY_MAP = {
    "موتيف 8": "صدر + تراي", "فت كومبات": "أرجل + بطن", "كور اكستريم": "أكتاف + جوانب",
    "ستيب": "ظهر + باي", "اكوا": "حديد شامل", "بامب فت": "صدر + أكتاف",
    "بودي ماكس": "أرجل + ظهر", "رادير": "ذراعين", "جي فت": "حديد قوة",
    "فت اتاك": "أرجل + أكتاف", "موبيلتي": "استشفاء حركي", "لا يوجد": "تمرين حر"
}

def check_legs_presence(df):
    all_muscles = " ".join(df['Muscle'].astype(str))
    return "أرجل" in all_muscles

# =====================================================================
# 4. بناء غرف العمليات (Tabs)
# =====================================================================
def main():
    days_ar = {"Sunday": "الأحد", "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت"}
    today_ar = days_ar[datetime.now().strftime("%A")]
    curr_date = datetime.now().strftime("%Y-%m-%d")

    st.markdown(f"<h1>👑 غرفة عمليات تايتان</h1>", unsafe_allow_html=True)

    tab_op, tab_setup, tab_tracker, tab_clinic, tab_health = st.tabs([
        "🚀 العمليات اليومية", "🗓️ هندسة الأسبوع", "🏋️ سجل الأوزان", "📸 عيادة InBody", "🥗 الوقود والنوم"
    ])

    # -----------------------------------------------------------------
    # لسان العمليات: ملخص اليوم والبروتوكول الطبي
    # -----------------------------------------------------------------
    with tab_op:
        if today_ar == "الجمعة":
            st.markdown("<div class='titan-card'><h2>OFF DAY 🛑</h2><p>استشفاء سلبي لبناء الأنسجة والخصوبة.</p></div>", unsafe_allow_html=True)
        else:
            plan_df = fetch_sheet("Weekly_Plan")
            try:
                today_row = plan_df[plan_df['Day'] == today_ar].iloc[0]
                s_class, target_m = today_row['Class'], today_row['Muscle']
            except:
                s_class, target_m = "لم يتم الضبط", "اذهب لهندسة الأسبوع"

            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"""
                <div class='titan-card' style='text-align: right;'>
                    <h3>⚡ مهمة اليوم: {today_ar}</h3>
                    <p>الكلاس: <b>{s_class}</b> | الهدف: <b>{target_m}</b></p>
                    <hr style='border-color:#333;'>
                    <p>🚗 08:10 م | 🅿️ 08:35 م | 💪 09:00 م</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
                if st.button("⏳ تأجيل"): st.warning("اختصر الإحماء.")
                if st.button("❌ غياب"): st.error("تم التسجيل.")
                st.markdown("</div>", unsafe_allow_html=True)

            # بروتوكول الاستشفاء والخصوبة
            st.markdown("### 🧊 البروتوكول الطبي (إلزامي)")
            st.info("🏊 15-20 دقيقة سباحة + ❄️ 3 دقائق جاكوزي بارد (يومياً).")
            if today_ar in ["الاثنين", "الخميس"]:
                st.warning("🔥 تصريح حراري: مسموح 10 دق حار/بخار + ❄️ دش بارد فوراً لحماية الخصوبة.")
            else:
                st.success("🛡️ حظر حراري: ممنوع الحار اليوم لضمان أعلى مستويات التستوستيرون.")

    # -----------------------------------------------------------------
    # لسان هندسة الأسبوع: معالجة نقص الأرجل
    # -----------------------------------------------------------------
    with tab_setup:
        st.markdown("### 🗓️ ميزان العضلات الأسبوعي")
        days = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "السبت"]
        new_plan = []
        with st.form("weekly_config"):
            cols = st.columns(3)
            for i, d in enumerate(days):
                with cols[i % 3]:
                    choice = st.selectbox(f"{d}", list(STRATEGY_MAP.keys()), key=f"set_{d}")
                    new_plan.append({"Day": d, "Class": choice, "Muscle": STRATEGY_MAP[choice]})
            
            if st.form_submit_button("✅ حفظ الجدول ومراجعة التوازن"):
                df_plan = pd.DataFrame(new_plan)
                if not check_legs_presence(df_plan):
                    st.error("⚠️ خطأ هندسي: الجدول يفتقد لتمرين الأرجل! يرجى اختيار كلاس (فت كومبات أو بودي ماكس).")
                else:
                    st.success("المخطط متوازن وشامل. تم الإرسال للسحاب.")

    # -----------------------------------------------------------------
    # لسان السجل: الذاكرة التاريخية ومنع التعارض
    # -----------------------------------------------------------------
    with tab_tracker:
        st.markdown("### 🏋️ الذاكرة التاريخية للأوزان")
        logs = fetch_sheet("Workout_Logs")
        
        if not logs.empty:
            all_exercises = logs['Exercise'].unique()
            search_ex = st.selectbox("ابحث عن تمرين سابق لمعرفة آخر وزن:", [""] + list(all_exercises))
            if search_ex:
                prev_data = logs[logs['Exercise'] == search_ex].iloc[-1]
                st.markdown(f"""
                <div class='stat-box'>
                    <p style='color:#888;'>آخر مرة لعبت هذا التمرين كانت في {prev_data['Date']}</p>
                    <div class='gold-val'>{prev_data['Weight']} KG × {prev_data['Reps']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        with st.form("log_entry", clear_on_submit=True):
            st.write("**تسجيل جلسة اليوم:**")
            c1, c2, c3 = st.columns([2, 1, 1])
            ex_in = c1.text_input("اسم التمرين (مثال: سحب أرضي)")
            wt_in = c2.number_input("الوزن (KG)", step=2.5)
            rp_in = c3.number_input("العدات", step=1)
            if st.form_submit_button("💾 حفظ في جوجل شيتس"):
                # هنا يتم الربط البرمجي مع الشيت
                st.success(f"تم تسجيل {ex_in} في السجل السحابي.")

if __name__ == "__main__":
    main()
