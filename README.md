# Nghiên cứu & Cài đặt Thuật toán Bầy Ong Nhân Tạo (ABC) và Biến thể AEABC

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Đồ án môn học tập trung nghiên cứu về thuật toán tối ưu hóa bầy đàn **Artificial Bee Colony (ABC)** và biến thể cải tiến **Adaptive Exploration ABC (AEABC)**. Dự án bao gồm lý thuyết, mã nguồn cài đặt và ứng dụng thực tế trên bài toán kỹ thuật.

## 📋 Giới thiệu

Thuật toán Bầy ong nhân tạo (ABC) là một kỹ thuật tối ưu hóa lấy cảm hứng từ hành vi tìm kiếm thức ăn thông minh của đàn ong mật. Tuy nhiên, thuật toán gốc thường gặp vấn đề về tốc độ hội tụ chậm. Dự án này triển khai biến thể **AEABC (Adaptive Exploration ABC)** để khắc phục nhược điểm đó thông qua cơ chế điều chỉnh xác suất tìm kiếm dựa trên khoảng cách.

Mục tiêu chính:
1. Hiểu và cài đặt thuật toán ABC gốc.
2. Cài đặt biến thể AEABC với cơ chế thăm dò thích ứng.
3. So sánh hiệu năng và ứng dụng vào bài toán thiết kế Dầm hàn (Welded Beam Design).

## 📂 Cấu trúc Thư mục

| Tên File | Mô tả |
| :--- | :--- |
| `ABC.py` | Mã nguồn thuật toán ABC gốc (Basic implementation). |
| `AEABC.py` | Mã nguồn thuật toán cải tiến AEABC (Adaptive Exploration logic). |
| `demo_aeabc_welded_beam.py` | Demo áp dụng AEABC giải bài toán Thiết kế Dầm hàn (có ràng buộc). |
| `Nhóm_106_Báo_cáo...pdf` | Báo cáo chi tiết dạng PDF (Lý thuyết, Công thức, Kết quả thực nghiệm). |
| `README.md` | Tài liệu hướng dẫn sử dụng dự án. |

## 🚀 Cài đặt và Hướng dẫn chạy

1. Yêu cầu hệ thống
Dự án sử dụng Python 3. Các thư viện cần thiết:
* `numpy`

Để cài đặt thư viện:
```bash
pip install numpy
````

2\. Chạy thuật toán

Bạn có thể chạy trực tiếp các file Python từ terminal:

- Chạy thuật toán ABC cơ bản:

```bash
python ABC.py
```

- Chạy thuật toán cải tiến AEABC:

```bash
python AEABC.py
```

- Chạy Demo bài toán Dầm hàn (Welded Beam):

```bash
python demo_aeabc_welded_beam.py
```

## 📊 So sánh ABC vs AEABC

Dự án đã thực hiện so sánh trên các hàm Benchmark (Sphere, Rosenbrock...) và bài toán thực tế.

  * ABC: Đơn giản, dễ cài đặt nhưng hội tụ chậm ở các không gian tìm kiếm lớn.
  * AEABC: Sử dụng cơ chế xác suất $P_d = e^{-1/d}$ để cân bằng giữa *Thăm dò (Exploration)* và *Khai thác (Exploitation)*, giúp tránh cực trị địa phương và hội tụ nhanh hơn đáng kể.

*(Chi tiết xem trong file báo cáo PDF)*

👥 Nhóm thực hiện: Nhóm 106 - Kĩ thuật truyền thông (HUST)
  * **Nguyễn Khắc Trí** - 20225769
  * **Nguyễn Thiện Nam** - 20235790

## 📚 Tài liệu tham khảo

1.  *Karaboga, D. (2005). An idea based on honey bee swarm for numerical optimization.*
2.  *Najwan, Z., et al. (2024). Adaptive Exploration Artificial Bee Colony for Mathematical Optimization. MDPI.*
