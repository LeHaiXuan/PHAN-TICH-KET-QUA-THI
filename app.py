import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from io import BytesIO

st.set_page_config(page_title="Phân tích điểm thi THPT", layout="wide")
st.title("📊 Ứng dụng Phân tích Điểm thi THPT")
st.caption("THPT Lê Quý Đôn - Long Bình Tân")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is None:
        return pd.read_csv("data/samples/sample_scores.csv")
    else:
        try:
            if uploaded_file.name.lower().endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif uploaded_file.name.lower().endswith('.xlsx'):
                return pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                st.error("Định dạng không hỗ trợ. Vui lòng dùng CSV/XLSX.")
                return None
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")
            return None

uploaded = st.file_uploader("📤 Tải lên dữ liệu CSV/XLSX (tuân theo cấu trúc cột)", type=["csv","xlsx"]) 

df = load_data(uploaded)
if df is None:
    st.stop()

# Sidebar filters
st.sidebar.header("Bộ lọc")
classes = sorted(df['Lop'].dropna().unique())
subjects = sorted(df['Mon'].dropna().unique())
departments = sorted(df['ToChuyenMon'].dropna().unique())
exams = sorted(df['KyThi'].dropna().unique())

sel_classes = st.sidebar.multiselect("Lớp", classes, default=classes)
sel_subjects = st.sidebar.multiselect("Môn", subjects, default=subjects)
sel_departments = st.sidebar.multiselect("Tổ chuyên môn", departments, default=departments)
sel_exams = st.sidebar.multiselect("Kỳ thi", exams, default=exams)

filtered = df[df['Lop'].isin(sel_classes) & df['Mon'].isin(sel_subjects) & df['ToChuyenMon'].isin(sel_departments) & df['KyThi'].isin(sel_exams)]

st.subheader("Tổng quan")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Số bài", len(filtered))
with col2:
    st.metric("Điểm trung bình", round(filtered['Diem'].mean(),2))
with col3:
    st.metric("Trung vị", round(filtered['Diem'].median(),2))
with col4:
    st.metric("Độ lệch chuẩn", round(filtered['Diem'].std(),2))

st.divider()

st.subheader("Phân phối điểm theo môn")
fig, ax = plt.subplots(figsize=(10,4))
sns.boxplot(data=filtered, x='Mon', y='Diem', ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
st.pyplot(fig)

st.subheader("Trung bình theo tổ chuyên môn")
agg_dept = filtered.groupby('ToChuyenMon')['Diem'].agg(['count','mean','median','std']).reset_index()
st.dataframe(agg_dept, use_container_width=True)

st.divider()

st.subheader("🔁 So sánh giữa hai kỳ thi")
left, right = st.columns(2)
with left:
    exam_a = st.selectbox("Kỳ thi A", exams, index=0)
with right:
    exam_b = st.selectbox("Kỳ thi B", exams, index=min(1, len(exams)-1))

comp_df = df[df['KyThi'].isin([exam_a, exam_b])]
comp_subject = comp_df.groupby(['KyThi','Mon'])['Diem'].mean().reset_index()
pivot = comp_subject.pivot(index='Mon', columns='KyThi', values='Diem')
pivot['Chênh lệch (B - A)'] = pivot.get(exam_b, np.nan) - pivot.get(exam_a, np.nan)
st.dataframe(pivot.round(2).sort_values('Chênh lệch (B - A)', ascending=False), use_container_width=True)

fig2, ax2 = plt.subplots(figsize=(10,4))
(pivot[[exam_a, exam_b]].round(2)).plot(kind='bar', ax=ax2)
ax2.set_ylabel('Điểm TB')
ax2.set_title(f"So sánh điểm TB theo môn: {exam_a} vs {exam_b}")
ax2.legend(loc='best')
st.pyplot(fig2)

st.divider()

st.subheader("🖨️ Xuất báo cáo PDF")
report_title = st.text_input("Tiêu đề báo cáo", value=f"Báo cáo phân tích điểm – {datetime.now().strftime('%Y-%m-%d')}")
btn = st.button("Tạo PDF")

if btn:
    buf = BytesIO()
    with PdfPages(buf) as pdf:
        # Page 1: Summary metrics
        figp1, axp1 = plt.subplots(figsize=(8.27, 11.69)) # A4 portrait in inches
        axp1.axis('off')
        text = (
            f"{report_title}\n\n"+
            f"Số bài: {len(filtered)}\n"+
            f"Điểm TB: {filtered['Diem'].mean():.2f}\n"+
            f"Trung vị: {filtered['Diem'].median():.2f}\n"+
            f"Độ lệch chuẩn: {filtered['Diem'].std():.2f}\n\n"+
            f"Bộ lọc: Lớp={', '.join(sel_classes)}; Môn={', '.join(sel_subjects)}; Tổ={', '.join(sel_departments)}; Kỳ thi={', '.join(sel_exams)}"
        )
        axp1.text(0.05, 0.95, text, va='top', fontsize=12)
        pdf.savefig(figp1)
        plt.close(figp1)

        # Page 2: Boxplot
        figp2, axp2 = plt.subplots(figsize=(8.27, 11.69))
        sns.boxplot(data=filtered, x='Mon', y='Diem', ax=axp2)
        axp2.set_xticklabels(axp2.get_xticklabels(), rotation=30, ha='right')
        axp2.set_title('Phân phối điểm theo môn')
        pdf.savefig(figp2)
        plt.close(figp2)

        # Page 3: Department stats table
        figp3, axp3 = plt.subplots(figsize=(8.27, 11.69))
        axp3.axis('off')
        tbl = agg_dept.round(2)
        table = axp3.table(cellText=tbl.values, colLabels=tbl.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        axp3.set_title('Thống kê theo tổ chuyên môn')
        pdf.savefig(figp3)
        plt.close(figp3)

        # Page 4: Exam comparison chart
        figp4, axp4 = plt.subplots(figsize=(8.27, 11.69))
        (pivot[[exam_a, exam_b]].round(2)).plot(kind='bar', ax=axp4)
        axp4.set_ylabel('Điểm TB')
        axp4.set_title(f"So sánh điểm TB theo môn: {exam_a} vs {exam_b}")
        axp4.legend(loc='best')
        pdf.savefig(figp4)
        plt.close(figp4)

    buf.seek(0)
    st.download_button(label="Tải báo cáo PDF", data=buf, file_name="bao_cao_phan_tich_diem.pdf", mime="application/pdf")

st.divider()

st.markdown("""
**Ghi chú:**
- Thay dữ liệu bằng file thật của trường để có kết quả chính xác.
- Nếu muốn thêm chỉ số (tỉ lệ >=5, >=8; phân loại giỏi/khá/trung bình/yếu) tôi có thể mở rộng nhanh.
- Có thể bổ sung thống kê theo từng **lớp** và **giáo viên bộ môn** nếu dữ liệu có cột tương ứng.
""")
