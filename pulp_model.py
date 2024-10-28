from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Sample parameters
time_horizon = 24  # 24 time periods
charge_cost = [10 + i % 3 for i in range(time_horizon)]  # Example time-varying cost
discharge_revenue = [15 - i % 2 for i in range(time_horizon)]
max_charge = 10
max_discharge = 10
battery_capacity = 50

# Initialize the problem
model = LpProblem("Battery_Optimization", LpMaximize)

# Define decision variables
charge = LpVariable.dicts("charge", range(time_horizon), lowBound=0, upBound=max_charge)
discharge = LpVariable.dicts("discharge", range(time_horizon), lowBound=0, upBound=max_discharge)
SoC = LpVariable.dicts("SoC", range(time_horizon + 1), lowBound=0, upBound=battery_capacity)

# Objective function
model += lpSum(discharge_revenue[t] * discharge[t] - charge_cost[t] * charge[t] for t in range(time_horizon))

# Constraints
for t in range(time_horizon):
    model += SoC[t + 1] == SoC[t] + charge[t] - discharge[t], f"Energy_Balance_{t}"
    model += SoC[t] >= 0, f"SoC_Lower_Bound_{t}"
    model += SoC[t] <= battery_capacity, f"SoC_Upper_Bound_{t}"

# Initial SoC
model += SoC[0] == 0

# Solve the problem
model.solve()

# Results
print("Status:", model.status)
print("Objective Value:", model.objective.value())
for t in range(time_horizon):
    print(f"Period {t}: Charge={charge[t].value()}, Discharge={discharge[t].value()}, SoC={SoC[t].value()}")
