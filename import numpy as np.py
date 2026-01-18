import numpy as np
import math
import random

# ==========================================
# Part 1: SIM-MIMO System Environment
# ==========================================
class SIM_MIMO_System:
    def __init__(self, Nt, Nr, N_sim_elements, Layers=1):
        """
        Initializes the MIMO system with Stacked Intelligent Metasurfaces.
        
        Args:
            Nt (int): Number of Transmit Antennas
            Nr (int): Number of Receive Antennas
            N_sim_elements (int): Number of elements per SIM layer
            Layers (int): Number of stacked layers (default 1 for basic implementation)
        """
        self.Nt = Nt
        self.Nr = Nr
        self.N_elements = N_sim_elements
        self.Layers = Layers
        
        # Simulate a random Rayleigh fading channel for demonstration
        # H_base: Channel from Tx to SIM (Line of Sight or Scatter)
        # G_base: Channel from SIM to Rx
        # In a real scenario, this would be the cascaded channel matrix H
        self.H_base = (np.random.randn(N_sim_elements, Nt) + 1j * np.random.randn(N_sim_elements, Nt)) / np.sqrt(2)
        self.G_base = (np.random.randn(Nr, N_sim_elements) + 1j * np.random.randn(Nr, N_sim_elements)) / np.sqrt(2)
        
        self.SNR_dB = 20
        self.SNR_linear = 10**(self.SNR_dB / 10)

    def calculate_spectral_efficiency(self, phase_shifts):
        """
        Objective Function: Calculates Capacity based on phase shifts.
        
        Args:
            phase_shifts (np.array): Vector of phase angles [0, 2pi]
        
        Returns:
            float: Spectral Efficiency (Capacity) in bits/s/Hz
        """
        # Construct the SIM Phase Matrix (Phi)
        # Phi is a diagonal matrix where elements are e^(j * theta)
        phi_elements = np.exp(1j * phase_shifts)
        Phi = np.diag(phi_elements)
        
        # Effective Channel H_eff = G * Phi * H
        # This models the signal passing through the SIM layer
        H_eff = self.G_base @ Phi @ self.H_base
        
        # MIMO Capacity Formula: C = log2(det(I + SNR/Nt * H_eff * H_eff^H))
        #  (Generalized from MIMO capacity formulas)
        Identity = np.eye(self.Nr)
        H_conjugate = H_eff.conj().T
        
        # Determinant calculation for Capacity
        matrix_inner = Identity + (self.SNR_linear / self.Nt) * (H_eff @ H_conjugate)
        
        # Use abs(det) to handle numerical noise, though det should be real positive for Hermitian
        try:
            capacity = np.real(np.log2(np.linalg.det(matrix_inner)))
        except:
            capacity = 0 # Handle singular matrices
            
        return capacity

# ==========================================
# Part 2: Artificial Bee Colony (ABC) Algorithm
# ==========================================
class ArtificialBeeColony:
    def __init__(self, objective_function, D, bounds, SN=20, MCN=100, limit=50):
        """
        ABC Algorithm Implementation[cite: 160, 341].
        
        Args:
            objective_function (func): Function to maximize
            D (int): Dimension of the problem (Number of variables)
            bounds (tuple): (lower_bound, upper_bound) for variables
            SN (int): Number of Food Sources (Population Size) [cite: 167]
            MCN (int): Maximum Cycle Number (Iterations) [cite: 169]
            limit (int): Trials before abandonment [cite: 188]
        """
        self.func = objective_function
        self.D = D
        self.lb, self.ub = bounds
        self.SN = SN
        self.MCN = MCN
        self.limit = limit
        
        # Initialization
        self.foods = np.random.uniform(self.lb, self.ub, (SN, D))
        self.fitness = np.zeros(SN)
        self.trial_counters = np.zeros(SN)
        self.best_solution = None
        self.best_fitness = -np.inf
        self.fitness_history = []

    def calculate_fitness(self):
        """Evaluate all food sources."""
        for i in range(self.SN):
            val = self.func(self.foods[i])
            self.fitness[i] = val
            
            # Update Global Best
            if val > self.best_fitness:
                self.best_fitness = val
                self.best_solution = self.foods[i].copy()

    def employed_bees_phase(self):
        """
        Employed bees search neighborhood: v_ij = x_ij + phi * (x_ij - x_kj) 
        """
        for i in range(self.SN):
            # Select random partner k distinct from i
            k = list(range(self.SN))
            k.remove(i)
            k = random.choice(k)
            
            # Select random parameter j
            j = random.randint(0, self.D - 1)
            
            # Generate new candidate solution
            phi = random.uniform(-1, 1)
            new_solution = self.foods[i].copy()
            new_solution[j] = self.foods[i][j] + phi * (self.foods[i][j] - self.foods[k][j])
            
            # Boundary control
            new_solution[j] = np.clip(new_solution[j], self.lb, self.ub)
            
            # Greedy Selection [cite: 192]
            new_fitness = self.func(new_solution)
            
            if new_fitness > self.fitness[i]:
                self.foods[i] = new_solution
                self.fitness[i] = new_fitness
                self.trial_counters[i] = 0
            else:
                self.trial_counters[i] += 1

    def onlooker_bees_phase(self):
        """
        Onlooker bees select sources based on probability (Roulette Wheel)[cite: 177, 349].
        """
        # Avoid division by zero/negative in probability calculation (for maximization)
        # Shift fitness to be positive if necessary
        fit_calc = self.fitness - np.min(self.fitness) + 1e-6 
        probabilities = fit_calc / np.sum(fit_calc)
        
        for i in range(self.SN):
            # Select food source i based on probability
            selected_index = np.random.choice(range(self.SN), p=probabilities)
            
            # Perform search (same equation as employed bee)
            k = list(range(self.SN))
            k.remove(selected_index)
            k = random.choice(k)
            j = random.randint(0, self.D - 1)
            phi = random.uniform(-1, 1)
            
            new_solution = self.foods[selected_index].copy()
            new_solution[j] = self.foods[selected_index][j] + phi * (self.foods[selected_index][j] - self.foods[k][j])
            new_solution[j] = np.clip(new_solution[j], self.lb, self.ub)
            
            new_fitness = self.func(new_solution)
            
            if new_fitness > self.fitness[selected_index]:
                self.foods[selected_index] = new_solution
                self.fitness[selected_index] = new_fitness
                self.trial_counters[selected_index] = 0
            else:
                self.trial_counters[selected_index] += 1

    def scout_bees_phase(self):
        """
        Reset food sources that have exceeded the trial limit[cite: 185, 330].
        """
        for i in range(self.SN):
            if self.trial_counters[i] > self.limit:
                # Re-initialize randomly [cite: 190]
                self.foods[i] = np.random.uniform(self.lb, self.ub, self.D)
                self.fitness[i] = self.func(self.foods[i])
                self.trial_counters[i] = 0

    def optimize(self):
        """Main Optimization Loop"""
        # Initial evaluation
        self.calculate_fitness()
        
        print(f"Starting ABC Optimization for SIM-MIMO...")
        print(f"Initial Best Capacity: {self.best_fitness:.4f} bits/s/Hz")
        
        for cycle in range(self.MCN):
            self.employed_bees_phase()
            self.onlooker_bees_phase()
            self.scout_bees_phase()
            
            # Update global best
            current_best = np.max(self.fitness)
            if current_best > self.best_fitness:
                self.best_fitness = current_best
                self.best_solution = self.foods[np.argmax(self.fitness)].copy()
            
            self.fitness_history.append(self.best_fitness)
            
            if cycle % 10 == 0:
                print(f"Iteration {cycle}/{self.MCN} - Best Capacity: {self.best_fitness:.4f} bits/s/Hz")
                
        return self.best_solution, self.best_fitness, self.fitness_history

# ==========================================
# Part 3: Running the Simulation
# ==========================================

if __name__ == "__main__":
    # 1. Setup SIM-MIMO Environment
    # Define problem dimensions
    Nt = 4              # Transmit Antennas
    Nr = 4              # Receive Antennas
    N_elements = 16     # Number of SIM elements (Optimization Variables)
    
    sim_env = SIM_MIMO_System(Nt, Nr, N_elements)
    
    # 2. Configure ABC Algorithm
    # Search space: Phase shifts between 0 and 2*pi
    bounds = (0, 2 * math.pi) 
    
    abc = ArtificialBeeColony(
        objective_function=sim_env.calculate_spectral_efficiency,
        D=N_elements,       # Dimension = number of phase shifts to optimize
        bounds=bounds,
        SN=30,              # Population size (Food Sources)
        MCN=100,            # Max Cycles
        limit=20            # Abandonment limit
    )
    
    # 3. Execute Optimization
    best_phases, max_capacity, history = abc.optimize()
    
    print("\noptimization Complete.")
    print(f"Optimized Capacity: {max_capacity:.5f} bits/s/Hz")
    print("Optimized Phase Shifts (First 5):", best_phases[:5])