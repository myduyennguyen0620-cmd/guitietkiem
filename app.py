import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd # Đã thêm thư viện pandas để làm bảng số liệu và xuất Excel

# --- 1. CẤU HÌNH GIAO DIỆN TRANG WEB ---
st.set_page_config(page_title="Kế Hoạch Tiết Kiệm", page_icon="💰", layout="centered")

# --- CHÈN HÌNH NỀN & HIỆU ỨNG KÍNH MỜ (GLASSMORPHISM) ---
page_bg_img = """
<style>
.stMarkdown:has(style) {
    display: none !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

div[data-baseweb="input"] > div {
    background-color: rgba(255, 255, 255, 0.4) !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.stMarkdown, .stText, .stMetric, .stDataFrame {
    background-color: rgba(255, 255, 255, 0.3) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 8px 15px rgba(0,0,0,0.05);
}

[data-testid="stMetricValue"] {
    color: #1f77b4 !important;
    font-weight: bold;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# ---------------------------------------------------------
st.title("💰 Ứng Dụng Tính Toán Tiền Gửi Tiết Kiệm")

# --- 2. MENU LỰA CHỌN TÍNH NĂNG ---
chon_chuoi = st.radio(
    "📌 Lựa chọn bài toán của bạn:",
    ["1: Tính số tiền có được trong tương lai", "2: Tính số tiền cần gửi mỗi tháng"]
)
Chon = 1 if "1:" in chon_chuoi else 2

st.markdown("### 📝 Nhập Thông Số Kế Hoạch")

col1, col2 = st.columns(2)
with col1:
    LSN_chuoi = st.text_input("Lãi suất một năm (%, tối đa 2 số thập phân) :red[*] :", value="6.5").replace(",", ".")
with col2:
    SN_chuoi = st.text_input("Thời gian gửi tiền (năm, tối đa 1 số thập phân) :red[*] :", value="5").replace(",", ".")

C_chuoi, PV_chuoi, LP_chuoi, FV_chuoi = "", "", "", ""

if Chon == 1:
    col3, col4, col5 = st.columns(3)
    with col3:
        C_chuoi = st.text_input("Tiền gửi mỗi tháng (triệu đồng) :red[*] :", value="5").replace(",", ".")
    with col4:
        PV_chuoi = st.text_input("Vốn sẵn có (triệu đồng):", value="").replace(",", ".")
    with col5:
        LP_chuoi = st.text_input("Lạm phát dự kiến (%):", value="4.2").replace(",", ".")
        
elif Chon == 2:
    FV_chuoi = st.text_input("Tổng mục tiêu muốn có (triệu đồng) :red[*] :", value="500").replace(",", ".")

# --- 3. NÚT THỰC THI & XỬ LÝ LOGIC ---
if st.button("🚀 Bắt Đầu Tính Toán", use_container_width=True, type="primary"):
    st.snow()
    
    if LSN_chuoi == "" or SN_chuoi == "":
        st.error("LỖI: Cần nhập đầy đủ Lãi suất và Thời gian")
        st.stop()
        
    LSN = float(LSN_chuoi)
    SN = float(SN_chuoi)

    r = (LSN / 100) / 12
    n = int(SN * 12)

    # Khởi tạo giỏ đựng số liệu chuyên sâu hơn
    danh_sach_nam = []
    danh_sach_goc = []
    danh_sach_lai = []
    danh_sach_tien = []

    # --- TÍNH TOÁN OPTION 1 ---
    if Chon == 1:
        if C_chuoi == "":
            st.error("LỖI: Cần nhập số tiền gửi mỗi tháng")
            st.stop()
        C = float(C_chuoi)
        PV = float(PV_chuoi) if PV_chuoi != "" else 0.0
        LP = float(LP_chuoi) if LP_chuoi != "" else 0.0

        FV = (PV * ((1 + r)**n)) + (C * (((1 + r)**n - 1) / r))
        TongGoc = PV + (C * n)
        TienLai = FV - TongGoc
        Suc_mua_thuc_te = FV / ((1 + (LP/100))**SN)
        
        st.subheader("📊 BÁO CÁO KẾT QUẢ")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Tổng vốn đã gửi", value=f"{TongGoc:,.2f} Tr")
        m2.metric(label="Tiền lãi sinh ra", value=f"{TienLai:,.2f} Tr")
        m3.metric(label="Tổng tài sản tương lai", value=f"{FV:,.2f} Tr")
        
        if LP > 0:
            st.info(f"💡 **Sức mua thực tế** (sau khi khấu trừ {LP}% lạm phát/năm): **{Suc_mua_thuc_te:,.2f} triệu đồng**")

        so_nam_tron = int(SN)
        for nam in range(1, so_nam_tron + 1):
            so_thang = nam * 12
            tong_goc_ht = PV + (C * so_thang)
            tien_co_duoc = (PV * ((1 + r)**so_thang)) + (C * (((1 + r)**so_thang - 1) / r))
            tien_lai_ht = tien_co_duoc - tong_goc_ht
            
            danh_sach_nam.append(f"Năm {nam}")
            danh_sach_goc.append(tong_goc_ht)
            danh_sach_lai.append(tien_lai_ht)
            danh_sach_tien.append(tien_co_duoc)

        if n > so_nam_tron * 12:
            danh_sach_nam.append(f"{SN} Năm")
            danh_sach_goc.append(TongGoc)
            danh_sach_lai.append(TienLai)
            danh_sach_tien.append(FV)
            
    # --- TÍNH TOÁN OPTION 2 ---
    elif Chon == 2:
        if FV_chuoi == "":
            st.error("LỖI: Vui lòng nhập số tiền mục tiêu mong muốn!")
            st.stop()
        FV = float(FV_chuoi)

        C = FV * (r / ((1 + r)**n - 1))
        TongGoc = C * n
        TienLai = FV - TongGoc
        
        st.subheader("📊 BÁO CÁO KẾT QUẢ")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Mỗi tháng cần gửi", value=f"{C:,.2f} Tr")
        m2.metric(label="Tổng vốn bỏ ra", value=f"{TongGoc:,.2f} Tr")
        m3.metric(label="Tiền lãi sinh ra", value=f"{TienLai:,.2f} Tr")

        so_nam_tron = int(SN)
        for nam in range(1, so_nam_tron + 1):
            so_thang = nam * 12
            tong_goc_ht = C * so_thang
            tien_co_duoc = C * (((1 + r)**so_thang - 1) / r)
            tien_lai_ht = tien_co_duoc - tong_goc_ht
            
            danh_sach_nam.append(f"Năm {nam}")
            danh_sach_goc.append(tong_goc_ht)
            danh_sach_lai.append(tien_lai_ht)
            danh_sach_tien.append(tien_co_duoc)
            
        if n > so_nam_tron * 12:
            danh_sach_nam.append(f"{SN} Năm")
            danh_sach_goc.append(TongGoc)
            danh_sach_lai.append(TienLai)
            danh_sach_tien.append(FV)

    # --- 4. RENDER GIAO DIỆN PHÂN TÍCH (ĐỒ THỊ & BẢNG) ---
    if len(danh_sach_nam) > 0:
        
        # Chia cột để vẽ 2 biểu đồ cạnh nhau
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            st.markdown("### 📈 ĐỒ THỊ TĂNG TRƯỞNG TÀI SẢN (CỘT CHỒNG)")
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            
            # Vẽ cột gốc và lãi chồng lên nhau
            ax1.bar(danh_sach_nam, danh_sach_goc, label='Tổng vốn', color='#4CAF50', alpha=0.85)
            ax1.bar(danh_sach_nam, danh_sach_lai, bottom=danh_sach_goc, label='Tiền lãi', color='#FF9800', alpha=0.85)
            
            # Làm đẹp
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.set_ylabel('Triệu đồng', fontsize=11, color='#666666')
            ax1.grid(axis='y', linestyle='--', alpha=0.4)
            ax1.legend()
            st.pyplot(fig1)
            
        with col_chart2:
            st.markdown("### 🥧 CƠ CẤU TÀI SẢN")
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            
            # Vẽ biểu đồ tròn cho năm cuối cùng
            labels = ['Tổng vốn', 'Tiền lãi']
            sizes = [TongGoc, TienLai]
            colors = ['#4CAF50', '#FF9800']
            explode = (0, 0.05) # Làm nổi bật phần lãi
            
            ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
            ax2.axis('equal') 
            st.pyplot(fig2)

        # Bảng dữ liệu chi tiết và nút tải Excel
        st.markdown("### 📋 BẢNG CHI TIẾT DÒNG TIỀN")
        
        # Gom số liệu vào Pandas DataFrame
        df = pd.DataFrame({
            "Thời gian": danh_sach_nam,
            "Tổng vốn (Tr)": [round(x, 2) for x in danh_sach_goc],
            "Tiền lãi (Tr)": [round(x, 2) for x in danh_sach_lai],
            "Tổng tài sản (Tr)": [round(x, 2) for x in danh_sach_tien]
        })
        
        # Hiển thị bảng
        st.dataframe(df, use_container_width=True)
        
        # Nút xuất ra file CSV (Excel)
        csv = df.to_csv(index=False).encode('utf-8-sig') # Dùng utf-8-sig để Excel đọc không bị lỗi font tiếng Việt
        st.download_button(
            label="📥 Tải Báo Cáo Xuống (Mở bằng Excel)",
            data=csv,
            file_name="Bao_Cao_Tiet_Kiem.csv",
            mime="text/csv",
            type="primary"
        )
