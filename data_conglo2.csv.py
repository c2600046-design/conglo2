import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Đường dẫn file dữ liệu
file_path = "caidoivam.xlsx"

# 2. Đọc dữ liệu từ file Excel
df = pd.read_excel(file_path, sheet_name=0)

# 3. Làm sạch cấu trúc dữ liệu ban đầu
# Loại bỏ các cột Unnamed không chứa dữ liệu quan trọng
df_clean = df.iloc[:, :4].copy()
df_clean.columns = ["ngay", "gio", "muc_nuoc", "loai_thuy_trieu"]

# 4. Chuyển đổi và hợp nhất cột ngày & giờ thành định dạng datetime
df_clean["timestamp"] = pd.to_datetime(
    df_clean["ngay"].astype(str) + " " + df_clean["gio"].astype(str)
)

# Sắp xếp dữ liệu theo mốc thời gian tăng dần
df_clean = df_clean.sort_values(by="timestamp").reset_index(drop=True)

# 5. Kiểm tra và xử lý dữ liệu khuyết thiếu / dữ liệu trùng
print("=== THÔNG TIN DỮ LIỆU SAU KHI LÀM SẠCH ===")
print(f"Tổng số bản ghi: {len(df_clean)}")
print(f"Số lượng ô trống:\n{df_clean.isnull().sum()}\n")

# 6. Trích xuất các đặc trưng thời gian 
df_clean["thang"] = df_clean["timestamp"].dt.month
df_clean["ngay_trong_thang"] = df_clean["timestamp"].dt.day
df_clean["gio_trong_ngay"] = df_clean["timestamp"].dt.hour
df_clean["thu"] = df_clean["timestamp"].dt.dayofweek  # 0: Thứ 2, 6: Chủ nhật

# 7. Thống kê mô tả dữ liệu thủy văn / tĩnh không
print("=== THỐNG KÊ MÔ TẢ MỰC NƯỚC / TĨNH KHÔNG ===")
print(df_clean["muc_nuoc"].describe())

# 8. Xuất dữ liệu đã xử lý ra file CSV chuẩn
output_file = "caidoivam_cleaned.csv"
df_clean.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"\n[Thành công] Đã lưu dữ liệu đã tiền xử lý vào file: {output_file}")

# 9. Trực quan hóa dữ liệu cơ bản 
plt.figure(figsize=(12, 5))
plt.plot(
    df_clean["timestamp"],
    df_clean["muc_nuoc"],
    marker="o",
    linestyle="-",
    color="b",
    label="Khoảng cách mực nước - mép cống (m)",
)
plt.title(
    "Chuỗi thời gian mực nước / Tĩnh không tại Cống Lộ II (Cái Đôi Vàm - Cà Mau)"
)
plt.xlabel("Thời gian")
plt.ylabel("Khoảng cách (m)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("muc_nuoc_caidoivam_chart.png", dpi=300)
plt.show()