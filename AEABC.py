Python 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import random
import numpy as np
import math

# --- Thiết lập tham số ---
num_employed_bees = 50
num_onlooker_bees = 50
max_iterations = 100
limit = 50
problem_size = 5

# --- Hàm mục tiêu (Sphere) ---
def fitness_function(x):
    return np.sum(x**2)

# --- Khởi tạo ---
food_sources = np.random.rand(num_employed_bees, problem_size) * 100
fitness_values = np.array([fitness_function(food) for food in food_sources])
no_improvement_counters = np.zeros(num_employed_bees)

# --- Vòng lặp chính ---
for iteration in range(max_iterations):
    
    # === GIAI ĐOẠN 1: ONG THỢ (EMPLOYED BEES) VỚI AEABC ===
    for i in range(num_employed_bees):
        # 1. Chọn đối tác ngẫu nhiên k (khác i)
        k = i
        while k == i:
            k = random.randint(0, num_employed_bees - 1)
            
        # 2. Tính khoảng cách Euclidean
        distance = np.linalg.norm(food_sources[i] - food_sources[k])
        
        # 3. Tính xác suất Pd (Tránh chia cho 0)
        if distance == 0:
            Pd = 0
        else:
            Pd = math.exp(-1.0 / distance)
            
        # 4. Cơ chế AEABC: Chỉ tìm kiếm nếu r > Pd
        # (Khoảng cách xa -> Pd ~ 1 -> Ít tìm kiếm -> Thăm dò)
        # (Khoảng cách gần -> Pd ~ 0 -> Tìm kiếm nhiều -> Khai thác)
        if random.random() > Pd:
            # --- Code ABC Gốc ---
            dimension = random.randint(0, problem_size - 1)
            mutant = np.copy(food_sources[i])
            mutant[dimension] += (random.random() - 0.5) * 2 * (food_sources[i][dimension] - food_sources[k][dimension])
            
            # Giới hạn biên (nếu cần, ở đây bỏ qua để đơn giản)
            
            mutant_fitness = fitness_function(mutant)
            
            if mutant_fitness < fitness_values[i]:
                food_sources[i] = mutant
                fitness_values[i] = mutant_fitness
                no_improvement_counters[i] = 0
            else:
                no_improvement_counters[i] += 1
        else:
            # Nếu không thỏa mãn điều kiện AEABC, giữ nguyên và không tăng bộ đếm lỗi
            pass

    # === TÍNH XÁC SUẤT CHỌN LỌC (Cho Ong quan sát) ===
    total_fitness = np.sum(fitness_values)
    if total_fitness == 0:
        probabilities = np.ones(num_employed_bees) / num_employed_bees
    else:
        # Nghịch đảo fitness vì bài toán cực tiểu hóa
        inv_fitness = 1.0 / (1.0 + fitness_values)
        probabilities = inv_fitness / np.sum(inv_fitness)

    # === GIAI ĐOẠN 2: ONG QUAN SÁT (ONLOOKER BEES) VỚI AEABC ===
    for j in range(num_onlooker_bees):
        # Chọn nguồn thức ăn theo Roulette Wheel
        i = np.random.choice(num_employed_bees, p=probabilities)
        
        # Lặp lại logic AEABC cho Ong quan sát
        k = i
        while k == i:
            k = random.randint(0, num_employed_bees - 1)
            
        distance = np.linalg.norm(food_sources[i] - food_sources[k])
        
        if distance == 0: Pd = 0
        else: Pd = math.exp(-1.0 / distance)
            
        if random.random() > Pd:
            dimension = random.randint(0, problem_size - 1)
            mutant = np.copy(food_sources[i])
            mutant[dimension] += (random.random() - 0.5) * 2 * (food_sources[i][dimension] - food_sources[k][dimension])
            
            mutant_fitness = fitness_function(mutant)
            
            if mutant_fitness < fitness_values[i]:
                food_sources[i] = mutant
                fitness_values[i] = mutant_fitness
                no_improvement_counters[i] = 0
            else:
                no_improvement_counters[i] += 1

    # === GIAI ĐOẠN 3: ONG TRINH SÁT (SCOUT BEES) ===
    for k in range(num_employed_bees):
        if no_improvement_counters[k] > limit:
            food_sources[k] = np.random.rand(problem_size) * 100
            fitness_values[k] = fitness_function(food_sources[k])
            no_improvement_counters[k] = 0

    best_fitness = np.min(fitness_values)
    print(f"Vòng {iteration}: Best Cost = {best_fitness}")

# --- Kết quả ---
print(f"Tối ưu toàn cục: {np.min(fitness_values)}")