import numpy as np
import random
import math

# --- CẤU HÌNH BÀI TOÁN DẦM HÀN (WELDED BEAM DESIGN) ---
# Biến số: x1(h), x2(l), x3(t), x4(b)
# Phạm vi biến:
LB = [0.1, 0.1, 0.1, 0.1]   # Lower Bound
UB = [2.0, 10.0, 10.0, 2.0] # Upper Bound
PROBLEM_SIZE = 4

# Các hằng số vật lý
P = 6000.0
L = 14.0
E = 30e6
G = 12e6
TauMax = 13600.0
SigmaMax = 30000.0
DeltaMax = 0.25

def welded_beam_cost(x):
    h, l, t, b = x[0], x[1], x[2], x[3]
    # Hàm mục tiêu: Chi phí chế tạo
    cost = 1.10471 * (h**2) * l + 0.04811 * t * b * (14.0 + l)
    return cost

def check_constraints(x):
    h, l, t, b = x[0], x[1], x[2], x[3]
    
    # Tính toán các thông số chịu lực
    tau_prime = P / (math.sqrt(2) * h * l)
    M = P * (L + l / 2)
    R = math.sqrt((l**2) / 4 + ((h + t) / 2)**2)
    J = 2 * (math.sqrt(2) * h * l * ((l**2) / 4 + ((h + t) / 2)**2))
    tau_double_prime = (M * R) / J
    tau = math.sqrt(tau_prime**2 + 2 * tau_prime * tau_double_prime * (l / (2 * R)) + tau_double_prime**2)
    sigma = (6 * P * L) / (b * (t**2))
    delta = (4 * P * (L**3)) / (E * (t**3) * b)
    Pc = (4.013 * E * math.sqrt((t**2 * b**6) / 36) / (L**2)) * (1 - (t / (2 * L)) * math.sqrt(E / (4 * G)))

    # Các ràng buộc (g(x) <= 0)
    g1 = tau - TauMax
    g2 = sigma - SigmaMax
    g3 = h - b
    g4 = delta - DeltaMax
    g5 = P - Pc
    g6 = 0.125 - h
    g7 = 1.10471 * h**2 * l + 0.04811 * t * b * (14.0 + l) - 5.0 # Ràng buộc chi phí biên (ví dụ)

    # Tính tổng mức độ vi phạm (Penalty)
    violations = [max(0, g) for g in [g1, g2, g3, g4, g5, g6, g7]]
    return sum(violations)

def fitness_function(x):
    cost = welded_beam_cost(x)
    penalty = check_constraints(x)
    # Nếu vi phạm ràng buộc, cộng thêm một giá trị phạt cực lớn
    return cost + 100000 * penalty

# --- THUẬT TOÁN AEABC ---
def run_aeabc():
    # Tham số thuật toán
    NP = 50           # Số lượng ong (Population Size)
    MAX_ITER = 200    # Số vòng lặp
    LIMIT = 100       # Giới hạn bỏ nguồn thức ăn
    
    # Khởi tạo quần thể
    foods = np.zeros((NP, PROBLEM_SIZE))
    for i in range(NP):
        for j in range(PROBLEM_SIZE):
            foods[i][j] = LB[j] + random.random() * (UB[j] - LB[j])
            
    f = np.array([fitness_function(ind) for ind in foods])
    trial = np.zeros(NP)
    
    best_ind = np.copy(foods[0])
    best_val = f[0]

    for it in range(MAX_ITER):
        
        # --- Giai đoạn Ong Thợ (Employed Bees) ---
        for i in range(NP):
            # AEABC Logic: Chọn k và tính khoảng cách
            k = i
            while k == i: k = random.randint(0, NP-1)
            
            dist = np.linalg.norm(foods[i] - foods[k])
            Pd = math.exp(-1.0/dist) if dist > 0 else 0
            
            # Chỉ tìm kiếm nếu thỏa mãn điều kiện AEABC
            if random.random() > Pd:
                j = random.randint(0, PROBLEM_SIZE-1)
                phi = random.uniform(-1, 1)
                
                # Tạo giải pháp mới
                v = np.copy(foods[i])
                v[j] = foods[i][j] + phi * (foods[i][j] - foods[k][j])
                
                # Giới hạn biên
                v[j] = max(LB[j], min(UB[j], v[j]))
                
                score = fitness_function(v)
                
                if score < f[i]:
                    foods[i] = v
                    f[i] = score
                    trial[i] = 0
                else:
                    trial[i] += 1
            else:
                pass # Bỏ qua tìm kiếm (Exploration state)

        # --- Tính xác suất ---
        mean_f = np.mean(f)
        if mean_f == 0: mean_f = 0.0001
        fitness_ratio = 1.0 / (1.0 + f)
        prob = fitness_ratio / np.sum(fitness_ratio)
        
        # --- Giai đoạn Ong Quan Sát (Onlooker Bees) ---
        t = 0
        m = 0
        while m < NP:
            if random.random() < prob[t]:
                m += 1
                i = t # Ong quan sát chọn nguồn thức ăn t
                
                # AEABC Logic lặp lại
                k = i
                while k == i: k = random.randint(0, NP-1)
                dist = np.linalg.norm(foods[i] - foods[k])
                Pd = math.exp(-1.0/dist) if dist > 0 else 0
                
                if random.random() > Pd:
                    j = random.randint(0, PROBLEM_SIZE-1)
                    phi = random.uniform(-1, 1)
                    v = np.copy(foods[i])
                    v[j] = foods[i][j] + phi * (foods[i][j] - foods[k][j])
                    v[j] = max(LB[j], min(UB[j], v[j]))
                    
                    score = fitness_function(v)
                    if score < f[i]:
                        foods[i] = v
                        f[i] = score
                        trial[i] = 0
                    else:
                        trial[i] += 1
            t += 1
            if t >= NP: t = 0

        # --- Giai đoạn Ong Trinh Sát (Scout Bees) ---
        max_trial_idx = np.argmax(trial)
        if trial[max_trial_idx] > LIMIT:
            for j in range(PROBLEM_SIZE):
                foods[max_trial_idx][j] = LB[j] + random.random() * (UB[j] - LB[j])
            f[max_trial_idx] = fitness_function(foods[max_trial_idx])
            trial[max_trial_idx] = 0

        # Cập nhật kết quả tốt nhất
        min_f = np.min(f)
        if min_f < best_val:
            best_val = min_f
            best_ind = foods[np.argmin(f)]
            
        print(f"Iter {it+1}: Cost = {best_val:.4f}")

    print("\n--- KẾT QUẢ TỐI ƯU (DẦM HÀN) ---")
    print(f"Chi phí thấp nhất: {best_val:.4f}")
    print(f"Thông số tối ưu [h, l, t, b]: {best_ind}")
    print(f"Kiểm tra vi phạm ràng buộc: {check_constraints(best_ind)}")

if __name__ == "__main__":
    run_aeabc()
