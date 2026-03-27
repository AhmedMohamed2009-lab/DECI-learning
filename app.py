import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO

# إعدادات الصفحة (فاخرة)
st.set_page_config(page_title="Play For Fun", page_icon="⚽", layout="centered")

# اللوجو
st.markdown("""
    <h1 style='text-align: center; color: #00ff00; font-size: 3rem;'>
        ⚽ Play For Fun ⚽
    </h1>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #ffffff;'>نظام الحضور والغياب</h2>", unsafe_allow_html=True)

# البيانات
players = [
    {"name": "محمد محمود", "whatsapp": "+201012634012"},
    {"name": "أحمد طلبه", "whatsapp": "+201224826752"},
    {"name": "يوسف محمود", "whatsapp": "+201111408361"}
]

# تخزين الحضور (session)
if 'attendance' not in st.session_state:
    st.session_state.attendance = {}

# الصفحة الرئيسية
if st.button("🚀 ابدأ تمرين جديد", type="primary", use_container_width=True):
    st.session_state.attendance = {}
    st.rerun()

st.markdown("### اللاعبين:")

for player in players:
    name = player["name"]
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.markdown(f"<h3 style='color: white;'>{name}</h3>", unsafe_allow_html=True)
    
    with col2:
        if st.button("✅ حضر", key=f"h_{name}", use_container_width=True, type="secondary"):
            st.session_state.attendance[name] = "حضر"
            st.rerun()
    
    with col3:
        if st.button("❌ غاب", key=f"g_{name}", use_container_width=True, type="secondary"):
            st.session_state.attendance[name] = "غاب"
            st.rerun()

    # عرض الحالة الحالية
    status = st.session_state.attendance.get(name, "لم يحدد بعد")
    if status == "حضر":
        st.success(f"✅ {name} - حضر")
    elif status == "غاب":
        st.error(f"❌ {name} - غاب")

# زرار إنهاء التمرين
if len(st.session_state.attendance) == len(players):
    if st.button("💾 إنهاء التمرين وحفظ", type="primary", use_container_width=True):
        
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # إنشاء DataFrame للـ Excel
        data = []
        for name in [p["name"] for p in players]:
            status = st.session_state.attendance.get(name, "غير محدد")
            data.append({"التاريخ": date_str, "اللاعب": name, "الحالة": status})
        
        df = pd.DataFrame(data)
        
        # عرض التقرير
        st.success("✅ تم حفظ التمرين بنجاح!")
        st.subheader("تقرير التمرين")
        st.dataframe(df, use_container_width=True)
        
        # تحميل ملف Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='الحضور')
        
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 تحميل ملف Excel (مين حضر ومين غاب)",
            data=excel_data,
            file_name=f"حضور_PlayForFun_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
        
        # رسائل الواتساب (wa.me)
        st.subheader("📱 إرسال رسائل واتساب")
        for p in players:
            name = p["name"]
            if st.session_state.attendance.get(name) == "حضر":
                phone = p["whatsapp"].replace("+", "")
                message = f"✅ حضر التمرين\n\nاللاعب: {name}\nالأكاديمية: Play For Fun\nالتاريخ: {date_str}\nشكراً لثقتكم 💪"
                wa_link = f"https://wa.me/{phone}?text={message.replace(' ', '%20')}"
                
                st.markdown(f"**{name}** → [اضغط هنا لإرسال الرسالة على واتساب]({wa_link})")

else:
    st.info("يرجى تحديد حالة كل اللاعبين أولاً")
