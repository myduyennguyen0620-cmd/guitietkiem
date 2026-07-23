import streamlit as st
import pandas as pd
import plotly.graph_objects as go 

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
.nhan-dinh {
    font-size: 15px;
    line-height: 1.6;
    color: #333;
    padding-top: 10px;
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
    LSN_chuoi = st.text_input("Lãi suất một năm (%, tối đa 2 số thập phân) :red[*] :", value="", placeholder="VD: 6.5").replace(",", ".")
with col2:
    SN_chuoi = st.text_input("Thời gian gửi tiền (năm, tối đa 1 số thập phân) :red[*] :", value="", placeholder="VD: 5").replace(",", ".")

C_chuoi, PV_chuoi, LP_chuoi, FV_chuoi = "", "", "", ""

if Chon == 1:
    col3, col4, col5 = st.columns(3)
    with col3:
        C_chuoi = st.text_input("Tiền gửi mỗi tháng (triệu đồng, tối đa 2 số thập phân) :red[*] :", value="", placeholder="VD: 5").replace(",", ".")
    with col4:
        PV_chuoi = st.text_input("Vốn sẵn có (triệu đồng, tối đa 2 số thập phân):", value="", placeholder="VD: 50").replace(",", ".")
    with col5:
        LP_chuoi = st.text_input("Lạm phát dự kiến (%, tối đa 2 số thập phân):", value="", placeholder="VD: 4.2").replace(",", ".")
        
elif Chon == 2:
    FV_chuoi = st.text_input("Tổng mục tiêu muốn có (triệu đồng, tối đa 2 số thập phân) :red[*] :", value="", placeholder="VD: 500").replace(",", ".")

# --- 3. NÚT THỰC THI & XỬ LÝ LOGIC ---
if st.button("🚀 Bắt Đầu Tính Toán", use_container_width=True, type="primary"):
    st.balloons()
    
    if LSN_chuoi == "" or SN_chuoi == "":
        st.error("LỖI: Cần nhập đầy đủ Lãi suất và Thời gian")
        st.stop()
        
    if "." in LSN_chuoi and len(LSN_chuoi.split(".")[1]) > 2:
        st.error("LỖI: Lãi suất chỉ nhập tối đa 2 số thập phân")
        st.stop()
    LSN = float(LSN_chuoi)

    if "." in SN_chuoi and len(SN_chuoi.split(".")[1]) > 1:
        st.error("LỖI: Thời gian gửi tiền chỉ nhập tối đa 1 số thập phân")
        st.stop()
    SN = float(SN_chuoi)

    r = (LSN / 100) / 12
    n = int(SN * 12)

    danh_sach_nam = []
    danh_sach_goc = []
    danh_sach_lai = []
    danh_sach_tien = []

    if Chon == 1:
        if C_chuoi == "":
            st.error("LỖI: Cần nhập số tiền gửi mỗi tháng")
            st.stop()
        if "." in C_chuoi and len(C_chuoi.split(".")[1]) > 2:
            st.error("LỖI: Số tiền gửi mỗi tháng chỉ nhập tối đa 2 số thập phân")
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
            
    elif Chon == 2:
        if FV_chuoi == "":
            st.error("LỖI: Cần nhập số tiền mục tiêu mong muốn")
            st.stop()
        if "." in FV_chuoi and len(FV_chuoi.split(".")[1]) > 2:
            st.error("LỖI: Tổng mục tiêu muốn có chỉ nhập tối đa 2 số thập phân")
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

    # --- 4. RENDER GIAO DIỆN PHÂN TÍCH ---
    if len(danh_sach_nam) > 0:
        
        # ---> ĐÃ SỬA: Gom dòng hướng dẫn rê chuột gộp chung vào tiêu đề để không sinh ra ô rỗng <---
        st.markdown("""
        ### 📈 ĐỒ THỊ TĂNG TRƯỞNG TÀI SẢN
        *(💡 Hướng dẫn: Rê chuột (trên PC) hoặc Chạm (trên Điện thoại) vào từng cột để xem chi tiết)*
        """)
        
        fig1 = go.Figure(data=[
            go.Bar(name='Tổng vốn', x=danh_sach_nam, y=danh_sach_goc, marker_color='#4CAF50',
                   hovertemplate='<b>%{x}</b><br>Tổng vốn: %{y:,.2f} Tr<extra></extra>'),
            go.Bar(name='Tiền lãi', x=danh_sach_nam, y=danh_sach_lai, marker_color='#FF9800',
                   hovertemplate='<b>%{x}</b><br>Tiền lãi: %{y:,.2f} Tr<extra></extra>')
        ])
        
        fig1.update_layout(
            barmode='stack',
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(title='Triệu đồng', gridcolor='rgba(200, 200, 200, 0.2)')
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # --- HÀNG 2: CHIA CỘT (BIỂU ĐỒ TRÒN & NHẬN ĐỊNH) ---
        col_pie, col_text = st.columns([1, 1.2]) 
        
        nam_hien_thi = int(SN) if SN == int(SN) else SN
        ty_le_lai = (TienLai / FV) * 100
        ty_le_goc = 100 - ty_le_lai

        if SN < 5:
            loi_khuyen = "Trong ngắn hạn, thách thức lớn nhất là vượt qua <b>'Thiên kiến hiện tại' (Present Bias)</b> – tâm lý thích chi tiêu ngay lập tức. Hãy giữ vững kỷ luật!"
        elif SN <= 10:
            loi_khuyen = "Dòng tiền đang tích lũy tốt. Hãy kiên định, đừng để những biến động nhỏ làm bạn chệch hướng mục tiêu trung hạn."
        else:
            loi_khuyen = "Thời gian là đòn bẩy vĩ đại nhất! Kỷ luật xuyên suốt sẽ giúp bạn chiến thắng mọi biến động của thị trường."
            
        if ty_le_lai >= 50:
            nhan_xet_lai = "Tiền lãi đã vượt mốc 50% tổng tài sản! Đây chính là đỉnh cao của việc 'để tiền đẻ ra tiền'."
        else:
            nhan_xet_lai = "Dòng tiền của bạn đang hoạt động sinh lời rất ổn định và an toàn."

        with col_pie:
            st.markdown(f"### 🥧 CƠ CẤU TÀI SẢN\n*(Tỷ lệ % sau {nam_hien_thi} năm)*")
            
            fig2 = go.Figure(data=[go.Pie(
                labels=['Tổng vốn', 'Tiền lãi'],
                values=[TongGoc, TienLai],
                marker=dict(colors=['#4CAF50', '#FF9800']),
                textinfo='label+percent',
                textposition='inside',
                textfont=dict(size=13, color='white', family="Arial Black"),
                hovertemplate='%{label}: %{value:,.2f} Tr<extra></extra>'
            )])
            
            # ---> Tinh chỉnh height=300 và margin để vừa khít tuyệt đối với hộp text <---
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(t=20, b=20, l=0, r=0),
                height=300 
            )
            st.plotly_chart(fig2, use_container_width=True)
            
        with col_text:
            # ---> ĐÃ SỬA: Gộp chung Tiêu đề và Nội dung vào 1 lệnh st.markdown duy nhất để tạo thành 1 khối hộp đồng nhất <---
            if Chon == 1:
                st.markdown(f"""
                ### 💡 NHẬN ĐỊNH TÀI CHÍNH
                <div class='nhan-dinh'>
                    <b>1. Tổng kết thành quả:</b> Sau {nam_hien_thi} năm, bạn sẽ tích lũy được <b>{FV:,.2f} Triệu đồng</b>.<br><br>
                    <b>2. Hiệu suất đầu tư:</b> Tiền lãi sinh ra chiếm <b>{ty_le_lai:.1f}%</b>. {nhan_xet_lai}<br><br>
                    <b>3. Lời khuyên hành vi:</b> {loi_khuyen}
                </div>
                """, unsafe_allow_html=True)
            elif Chon == 2:
                st.markdown(f"""
                ### 💡 NHẬN ĐỊNH TÀI CHÍNH
                <div class='nhan-dinh'>
                    <b>1. Tính khả thi:</b> Để đạt mục tiêu <b>{FV:,.2f} Triệu đồng</b>, kỷ luật gửi <b>{C:,.2f} Tr/tháng</b> là chìa khóa then chốt.<br><br>
                    <b>2. Đòn bẩy tài chính:</b> Bạn thực chất chỉ bỏ ra <b>{ty_le_goc:.1f}%</b> công sức (tiền gốc). {nhan_xet_lai}<br><br>
                    <b>3. Lời khuyên hành vi:</b> {loi_khuyen}
                </div>
                """, unsafe_allow_html=True)

        # --- HÀNG 3: BẢNG DÒNG TIỀN ---
        st.markdown("### 📋 BẢNG CHI TIẾT DÒNG TIỀN")
        
        df = pd.DataFrame({
            "Thời gian": danh_sach_nam,
            "Tổng vốn (Triệu đồng)": [round(x, 2) for x in danh_sach_goc],
            "Tiền lãi (Triệu đồng)": [round(x, 2) for x in danh_sach_lai],
            "Tổng tài sản (Triệu đồng)": [round(x, 2) for x in danh_sach_tien]
        })
        
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(
            label="📥 Tải Báo Cáo Xuống (Mở bằng Excel)",
            data=csv,
            file_name="Bao_Cao_Tiet_Kiem.csv",
            mime="text/csv",
            type="primary"
        )
