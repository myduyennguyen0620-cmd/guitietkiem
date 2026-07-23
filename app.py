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
/* Tuỳ chỉnh font cho phần nhận định */
.nhan-dinh {
    font-size: 16px;
    line-height: 1.6;
    color: #333;
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
        
        # --- HÀNG 1: ĐỒ THỊ CỘT FULL MÀN HÌNH ---
        st.markdown("### 📈 ĐỒ THỊ TĂNG TRƯỞNG TÀI SẢN")
        
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
        # Bật full width cho cột
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True) # Tạo khoảng trắng cho dễ nhìn
        
        # --- HÀNG 2: CHIA CỘT (BIỂU ĐỒ TRÒN & NHẬN ĐỊNH TÀI CHÍNH) ---
        col_pie, col_text = st.columns([1, 1.2]) # Bên text nhỉnh hơn một chút cho rộng rãi
        
        nam_hien_thi = int(SN) if SN == int(SN) else SN
        ty_le_lai = (TienLai / FV) * 100
        ty_le_goc = 100 - ty_le_lai

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
            
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig2, use_container_width=True)
            
        with col_text:
            st.markdown("### 💡 NHẬN ĐỊNH TÀI CHÍNH")
            
            # Khung text nhận định thông minh thay đổi theo Option
            if Chon == 1:
                st.markdown(f"""
                <div class='nhan-dinh'>
                    <b>1. Tổng kết thành quả:</b> Sau {nam_hien_thi} năm kiên trì, bạn sẽ sở hữu tổng tài sản là <b>{FV:,.2f} Triệu đồng</b>.<br><br>
                    <b>2. Sức mạnh Lãi kép:</b> Tiền lãi sinh ra chiếm tới <b>{ty_le_lai:.1f}%</b> trong cơ cấu tài sản. Dòng tiền của bạn đang hoạt động sinh lời cực kỳ hiệu quả.<br><br>
                    <b>3. Động lực tâm lý:</b> Việc duy trì thói quen tiết kiệm đều đặn sẽ giúp bạn kiểm soát tốt các định kiến hành vi và cám dỗ chi tiêu ngắn hạn.
                </div>
                """, unsafe_allow_html=True)
            elif Chon == 2:
                st.markdown(f"""
                <div class='nhan-dinh'>
                    <b>1. Tính khả thi của mục tiêu:</b> Để đạt được <b>{FV:,.2f} Triệu đồng</b>, việc chia nhỏ kế hoạch và kỷ luật gửi <b>{C:,.2f} Tr/tháng</b> sẽ giúp giảm bớt áp lực tài chính đáng kể.<br><br>
                    <b>2. Đòn bẩy thời gian:</b> Nhờ vào sức mạnh của lãi kép, bạn thực chất chỉ phải bỏ ra <b>{ty_le_goc:.1f}%</b> công sức (tiền gốc), phần còn lại là sự gia tăng tự nhiên của dòng tiền.<br><br>
                    <b>3. Lời khuyên hành vi:</b> Bắt đầu càng sớm, số tiền phải trích lập hàng tháng sẽ càng nhẹ. Sự kỷ luật chính là chìa khóa quyết định thành công!
                </div>
                """, unsafe_allow_html=True)
                
            st.success("Tóm lại: Thời gian và sự kỷ luật là hai đòn bẩy lớn nhất trong đầu tư và tích lũy!")

        st.markdown("---")
        
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
