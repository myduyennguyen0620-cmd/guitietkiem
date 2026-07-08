import streamlit as st
import matplotlib.pyplot as plt

# --- 1. CẤU HÌNH GIAO DIỆN TRANG WEB ---
st.set_page_config(page_title="Kế Hoạch Tiết Kiệm", page_icon="💰", layout="centered")

st.title("💰 Ứng Dụng Tính Toán Tiền Gửi Tiết Kiệm")
st.markdown("Giải pháp tài chính minh bạch, trực quan dựa trên sức mạnh của Lãi Kép.")
st.markdown("---")

# --- 2. MENU LỰA CHỌN TÍNH NĂNG ---
chon_chuoi = st.radio(
    "📌 Lựa chọn bài toán của bạn:",
    ["1: Tính số tiền có được trong tương lai", "2: Tính số tiền cần gửi mỗi tháng"]
)
Chon = 1 if "1:" in chon_chuoi else 2

st.markdown("### 📝 Nhập Thông Số Kế Hoạch")

# Dùng st.columns để chia thành 2 cột cho đẹp mắt
col1, col2 = st.columns(2)
with col1:
    LSN_chuoi = st.text_input("Nhập lãi suất 1 năm (%, tối đa 2 số thập phân):", value="6.5").replace(",", ".")
with col2:
    SN_chuoi = st.text_input("Nhập thời gian gửi (năm, tối đa 1 số thập phân):", value="5").replace(",", ".")

# Các biến lưu tạm cho phần giao diện mở rộng
C_chuoi, PV_chuoi, LP_chuoi, FV_chuoi = "", "", "", ""

if Chon == 1:
    col3, col4, col5 = st.columns(3)
    with col3:
        C_chuoi = st.text_input("Tiền gửi mỗi tháng (triệu VNĐ):", value="5").replace(",", ".")
    with col4:
        PV_chuoi = st.text_input("Vốn sẵn có (ENTER để trống = 0):", value="").replace(",", ".")
    with col5:
        LP_chuoi = st.text_input("Lạm phát dự kiến % (ENTER để trống = 0):", value="4.2").replace(",", ".")
elif Chon == 2:
    FV_chuoi = st.text_input("Nhập tổng mục tiêu muốn có (triệu VNĐ):", value="500").replace(",", ".")

# --- 3. NÚT THỰC THI & XỬ LÝ LOGIC ---
if st.button("🚀 Bắt Đầu Tính Toán", use_container_width=True, type="primary"):
    
    # KHI BẤM NÚT, HỆ THỐNG SẼ CHẠY BỘ LỌC BẮT LỖI
    if LSN_chuoi == "" or SN_chuoi == "":
        st.error("LỖI: Vui lòng nhập đầy đủ Lãi suất và Thời gian!")
        st.stop() # Lệnh này thay thế cho sys.exit() trong Streamlit
        
    if "." in LSN_chuoi and len(LSN_chuoi.split(".")[1]) > 2:
        st.error("LỖI: Lãi suất chỉ nhập tối đa 2 số thập phân")
        st.stop()
    LSN = float(LSN_chuoi)

    if "." in SN_chuoi and len(SN_chuoi.split(".")[1]) > 1:
        st.error("LỖI: Thời gian gửi chỉ nhập tối đa 1 số thập phân")
        st.stop()
    SN = float(SN_chuoi)

    # Đổi đơn vị
    r = (LSN / 100) / 12
    n = int(SN * 12)

    # Tạo giỏ đựng số liệu vẽ đồ thị
    danh_sach_nam = []
    danh_sach_tien = []

    # --- TÍNH TOÁN OPTION 1 ---
    if Chon == 1:
        if C_chuoi == "":
            st.error("LỖI: Vui lòng nhập số tiền gửi mỗi tháng!")
            st.stop()
        if "." in C_chuoi and len(C_chuoi.split(".")[1]) > 2:
            st.error("LỖI: Số tiền gửi chỉ nhập tối đa 2 số thập phân")
            st.stop()
        C = float(C_chuoi)

        if PV_chuoi != "":
            if "." in PV_chuoi and len(PV_chuoi.split(".")[1]) > 2:
                st.error("LỖI: Vốn sẵn có chỉ nhập tối đa 2 số thập phân")
                st.stop()
            PV = float(PV_chuoi)
        else:
            PV = 0.0

        if LP_chuoi != "":
            if "." in LP_chuoi and len(LP_chuoi.split(".")[1]) > 2:
                st.error("LỖI: Lạm phát chỉ nhập tối đa 2 số thập phân")
                st.stop()
            LP = float(LP_chuoi)
        else:
            LP = 0.0

        FV = (PV * ((1 + r)**n)) + (C * (((1 + r)**n - 1) / r))
        TongGoc = PV + (C * n)
        TienLai = FV - TongGoc
        Suc_mua_thuc_te = FV / ((1 + (LP/100))**SN)
        
        st.markdown("---")
        st.subheader("📊 BÁO CÁO KẾT QUẢ")
        
        # Dùng st.metric để tạo các khối thông số cực kỳ xịn xò
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Tổng vốn đã gửi", value=f"{TongGoc:,.2f} Tr")
        m2.metric(label="Tiền lãi sinh ra", value=f"{TienLai:,.2f} Tr")
        m3.metric(label="Tổng tài sản tương lai", value=f"{FV:,.2f} Tr")
        
        if LP > 0:
            st.info(f"💡 **Sức mua thực tế** (sau khi khấu trừ {LP}% lạm phát/năm): **{Suc_mua_thuc_te:,.2f} triệu đồng**")

        # Quét chu kỳ tích lũy
        so_nam_tron = int(SN)
        for nam in range(1, so_nam_tron + 1):
            so_thang = nam * 12
            tien_co_duoc = (PV * ((1 + r)**so_thang)) + (C * (((1 + r)**so_thang - 1) / r))
            danh_sach_nam.append(f"Năm {nam}")
            danh_sach_tien.append(tien_co_duoc)

        if n > so_nam_tron * 12:
            danh_sach_nam.append(f"{SN} Năm")
            danh_sach_tien.append(FV)
            
    # --- TÍNH TOÁN OPTION 2 ---
    elif Chon == 2:
        if FV_chuoi == "":
            st.error("LỖI: Vui lòng nhập số tiền mục tiêu mong muốn!")
            st.stop()
        if "." in FV_chuoi and len(FV_chuoi.split(".")[1]) > 2:
            st.error("LỖI: Số tiền mục tiêu chỉ nhập tối đa 2 số thập phân")
            st.stop()
        FV = float(FV_chuoi)

        C = FV * (r / ((1 + r)**n - 1))
        TongGoc = C * n
        TienLai = FV - TongGoc
        
        st.markdown("---")
        st.subheader("📊 BÁO CÁO KẾT QUẢ")
        
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Mỗi tháng cần gửi", value=f"{C:,.2f} Tr")
        m2.metric(label="Tổng vốn bỏ ra", value=f"{TongGoc:,.2f} Tr")
        m3.metric(label="Tiền lãi sinh ra", value=f"{TienLai:,.2f} Tr")

        # Quét chu kỳ tích lũy
        so_nam_tron = int(SN)
        for nam in range(1, so_nam_tron + 1):
            so_thang = nam * 12
            tien_co_duoc = C * (((1 + r)**so_thang - 1) / r)
            danh_sach_nam.append(f"Năm {nam}")
            danh_sach_tien.append(tien_co_duoc)
            
        if n > so_nam_tron * 12:
            danh_sach_nam.append(f"{SN} Năm")
            danh_sach_tien.append(FV)

    # --- 4. RENDER BIỂU ĐỒ LÊN WEB ---
    if len(danh_sach_nam) > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📈 LỊCH TRÌNH TĂNG TRƯỞNG TÀI SẢN")
        
        # Khởi tạo khung vẽ matplotlib
        fig, ax = plt.subplots(figsize=(10, 4.5))
        bars = ax.bar(danh_sach_nam, danh_sach_tien, color='#4CAF50', edgecolor='none', width=0.6, alpha=0.9)
        
        # Hiển thị số liệu trên đầu cột
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + (max(danh_sach_tien)*0.02), 
                     f'{yval:,.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')
            
        # Làm đẹp đồ thị
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel('Triệu đồng', fontsize=11, color='#666666')
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        plt.tight_layout()
        
        # Xuất biểu đồ ra Streamlit
        st.pyplot(fig)
