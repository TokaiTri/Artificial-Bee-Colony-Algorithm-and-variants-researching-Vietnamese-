import random
import numpy as np

# --- Thiết lập các tham số ---
num_employed_bees = 50      # Số lượng ong thợ (Employed Bees)
num_onlooker_bees = 50      # Số lượng ong quan sát/ong chờ (Onlooker Bees)
max_iterations = 100        # Số vòng lặp tối đa
limit = 50                  # Giới hạn số lần không cải thiện trước khi bỏ nguồn thức ăn
problem_size = 5           # Kích thước bài toán (số chiều của biến số)

# --- Định nghĩa hàm thích nghi (Fitness Function) ---
def fitness_function(x):
    return np.sum(x**2)     # Bài toán tối ưu hóa hàm cầu (Sphere function)

# --- Khởi tạo quần thể ban đầu ---
food_sources = np.random.rand(num_employed_bees, problem_size) * 100
fitness_values = np.array([fitness_function(food) for food in food_sources])
no_improvement_counters = np.zeros(num_employed_bees) # Bộ đếm số lần không cải thiện

# --- Vòng lặp chính ---
for iteration in range(max_iterations):
    # --- Giai đoạn Ong thợ (Employed bees) ---
    for i in range(num_employed_bees):
        # Chọn ngẫu nhiên một chiều (biến) để thay đổi
        dimension = random.randint(0, problem_size - 1)

        # Tạo ra một giải pháp ứng viên mới (đột biến/biến thể)
        mutant = np.copy(food_sources[i])
        mutant[dimension] += (random.random() - 0.5) * 2  # Sửa đổi chiều được chọn một cách ngẫu nhiên

        # Đánh giá độ thích nghi của giải pháp mới
        mutant_fitness = fitness_function(mutant)

        # Lựa chọn tham lam (Greedy selection) giữa giải pháp hiện tại và giải pháp mới
        if mutant_fitness < fitness_values[i]:
            food_sources[i] = mutant
            fitness_values[i] = mutant_fitness
            no_improvement_counters[i] = 0
        else:
            no_improvement_counters[i] += 1

    # --- Tính toán xác suất dựa trên giá trị thích nghi ---
    total_fitness = np.sum(fitness_values)
    if total_fitness == 0:
        probabilities = np.ones(num_employed_bees) / num_employed_bees
    else:
        # Công thức tính xác suất (nghịch đảo vì đây là bài toán tìm cực tiểu)
        probabilities = (1.0 / (1.0 + fitness_values)) / np.sum(1.0 / (1.0 + fitness_values))

    # --- Giai đoạn Ong quan sát (Onlooker bees) ---
    for j in range(num_onlooker_bees):
        # Chọn nguồn thức ăn dựa trên vòng quay roulette (xác suất)
        selected_food_source = np.random.choice(num_employed_bees, p=probabilities)

        # Chọn ngẫu nhiên một chiều để thay đổi
        dimension = random.randint(0, problem_size - 1)

        # Tạo ra một giải pháp ứng viên mới
        mutant = np.copy(food_sources[selected_food_source])
        mutant[dimension] += (random.random() - 0.5) * 2  # Sửa đổi chiều được chọn một cách ngẫu nhiên

        # Đánh giá độ thích nghi của giải pháp mới
        mutant_fitness = fitness_function(mutant)

        # Lựa chọn tham lam giữa giải pháp được chọn và giải pháp mới
        if mutant_fitness < fitness_values[selected_food_source]:
            food_sources[selected_food_source] = mutant
            fitness_values[selected_food_source] = mutant_fitness
            no_improvement_counters[selected_food_source] = 0
        else:
            no_improvement_counters[selected_food_source] += 1

    # --- Giai đoạn Ong trinh sát (Scout bees) ---
    for k in range(num_employed_bees):
        # Nếu một nguồn thức ăn không cải thiện quá số lần giới hạn (limit)
        if no_improvement_counters[k] > limit:
            # Thay thế bằng một nguồn thức ăn ngẫu nhiên mới
            food_sources[k] = np.random.rand(problem_size) * 100
            fitness_values[k] = fitness_function(food_sources[k])
            no_improvement_counters[k] = 0

    # Hiển thị giải pháp tốt nhất trong mỗi vòng lặp
    best_fitness = np.min(fitness_values)
    print(f"Vòng lặp {iteration}, Độ thích nghi tốt nhất: {best_fitness}")

# --- Tìm giải pháp tốt nhất tổng thể ---
overall_best_fitness = np.min(fitness_values)
overall_best_index = np.argmin(fitness_values)
overall_best_solution = food_sources[overall_best_index]

print("--- Kết quả tối ưu hóa ---")
print(f"Độ thích nghi tốt nhất: {overall_best_fitness}")

print(f"Giải pháp tốt nhất: {overall_best_solution}")
