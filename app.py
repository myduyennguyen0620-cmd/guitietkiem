import sys
import matplotlib.pyplot as plt

print("--- TÍNH TOÁN TIỀN GỬI TIẾT KIỆM ---")
print("1: Tính số tiền có được trong tương lai")
print("2: Tính số tiền cần gửi mỗi tháng")
Chon = float(input("Nhập lựa chọn (1 hoặc 2): "))

if Chon == 1 or Chon == 2:
    
    # 1. NHẬP LÃI SUẤT
    LSN_chuoi = input("Nhập lãi suất 1 năm (%, tối đa 2 số thập phân): ").replace(",", ".")
    if "." in LSN_chuoi and len(LSN_chuoi.split(".")[1]) > 2:
        sys.exit("LỖI: Lãi suất chỉ nhập tối đa 2 số thập phân")
    LSN = float(LSN_chuoi)

    # 2. NHẬP THỜI GIAN
    SN_chuoi = input("Nhập thời gian gửi (năm, tối đa 1 số thập phân): ").replace(",", ".")
    if "." in SN_chuoi and len(SN_chuoi.split(".")[1]) > 1:
        sys.exit("LỖI: Thời gian gửi chỉ nhập tối đa 1 số thập phân")
    SN = float(SN_chuoi)

    r = (LSN / 100) / 12
    n = int(SN * 12)
    
    # TẠO LIST ĐỂ LƯU DỮ LIỆU VẼ BIỂU ĐỒ
    danh_sach_nam = []
    danh_sach_tien = []
    
    # 3. TÍNH TOÁN
    if Chon == 1:
        C_chuoi = input("Nhập số tiền gửi mỗi tháng (triệu đồng, tối đa 2 số thập phân): ").replace(",", ".")
        if "." in C_chuoi and len(C_chuoi.split(".")[1]) > 2:
            sys.exit("LỖI: Số tiền gửi chỉ nhập tối đa 2 số thập phân")
        C = float(C_chuoi)

        PV_chuoi = input("Bạn có sẵn vốn không? (triệu đồng, tối đa 2 số thập phân, bấm ENTER để bỏ qua): ").replace(",", ".")
        if PV_chuoi != "":
            if "." in PV_chuoi and len(PV_chuoi.split(".")[1]) > 2:
                sys.exit("LỖI: Vốn sẵn có chỉ nhập tối đa 2 số thập phân")
            PV = float(PV_chuoi)
        else:
            PV = 0.0

        LP_chuoi = input("Nhập lạm phát (%, tối đa 2 số thập phân, bấm ENTER để bỏ qua): ").replace(",", ".")
        if LP_chuoi != "":
            if "." in LP_chuoi and len(LP_chuoi.split(".")[1]) > 2:
                sys.exit("LỖI: Lạm phát chỉ nhập tối đa 2 số thập phân")
            LP = float(LP_chuoi)
        else:
            LP = 0.0

        FV = (PV * ((1 + r)**n)) + (C * (((1 + r)**n - 1) / r))
        TongGoc = PV + (C * n)
        TienLai = FV - TongGoc
        Suc_mua_thuc_te = FV / ((1 + (LP/100))**SN)
        
        print(f"\n--- KẾT QUẢ TỔNG KẾT ---")
        print(f"Tổng tiền vốn đã gửi : {TongGoc:,.2f} triệu đồng")
        print(f"Tiền lãi sinh ra     : {TienLai:,.2f} triệu đồng")
        print(f"Tổng tài sản tương lai: {FV:,.2f} triệu đồng")
        if LP > 0:
            print(f"Sức mua thực tế (sau lạm phát {LP}%): {Suc_mua_thuc_te:,.2f} triệu đồng")
        
        print("\n--- LỊCH TRÌNH TÍCH LŨY ---")
        so_nam_tron = int(SN)
        for nam in range(1, so_nam_tron + 1):
            so_thang = nam * 12
            tien_co_duoc = (PV * ((1 + r)**so_thang)) + (C * (((1 + r)**so_thang - 1) / r))
            print(f"Hết năm thứ {nam}: Bạn có {tien_co_duoc:,.2f} triệu đồng")
            
            danh_sach_nam.append(f"Năm {nam}")
            danh_sach_tien.append(tien_co_duoc)
            
        if n > so_nam_tron * 12:
            print(f"Hết tháng thứ {n} (Tức {SN} năm): Bạn có {FV:,.2f} triệu đồng")
            danh_sach_nam.append(f"{SN} Năm")
            danh_sach_tien.append(FV)
        
    elif Chon == 2:
        FV_chuoi = input("Nhập tổng số tiền mục tiêu muốn có (triệu đồng, tối đa 2 số thập phân): ").replace(",", ".")
        if "." in FV_chuoi and len(FV_chuoi.split(".")[1]) > 2:
            sys.exit("LỖI: Số tiền mục tiêu chỉ nhập tối đa 2 số thập phân")
        FV = float(FV_chuoi)

        C = FV * (r / ((1 + r)**n - 1))
        TongGoc = C * n
        TienLai = FV - TongGoc
        
        print(f"\n--- KẾT QUẢ TỔNG KẾT ---")
        print(f"Mỗi tháng cần gửi    : {C:,.2f} triệu đồng")
        print(f"Tổng tiền vốn bỏ ra  : {TongGoc:,.2f} triệu đồng")
        print(f"Tiền lãi sinh ra     : {TienLai:,.2f} triệu đồng")
        
        print("\n--- LỊCH TRÌNH TÍCH LŨY ---")
        so_nam_tron = int(SN)
        for nam in range(1, so_nam_tron + 1):
            so_thang = nam * 12
            tien_co_duoc = C * (((1 + r)**so_thang - 1) / r)
            print(f"Hết năm thứ {nam}: Bạn có {tien_co_duoc:,.2f} triệu đồng")
            
            danh_sach_nam.append(f"Năm {nam}")
            danh_sach_tien.append(tien_co_duoc)
            
        if n > so_nam_tron * 12:
            print(f"Hết tháng thứ {n} (Tức {SN} năm): Bạn có {FV:,.2f} triệu đồng")
            danh_sach_nam.append(f"{SN} Năm")
            danh_sach_tien.append(FV)

    # BIỂU ĐỒ TRỰC QUAN
    if len(danh_sach_nam) > 0:
        plt.figure(figsize=(10, 5))
        bars = plt.bar(danh_sach_nam, danh_sach_tien, color='#4CAF50', edgecolor='black')
        
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + (max(danh_sach_tien)*0.01), 
                     f'{yval:,.1f}', ha='center', va='bottom', fontsize=9)
            
        plt.title('BIỂU ĐỒ TĂNG TRƯỞNG TÀI SẢN THEO NĂM', fontsize=14, fontweight='bold')
        plt.xlabel('Thời gian', fontsize=11)
        plt.ylabel('Triệu đồng', fontsize=11)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

else:
    sys.exit("LỖI: Bạn phải nhập số 1 hoặc 2.")
