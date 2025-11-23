import math


def calculate_P_work_joint_2more(r=0.93, lambda_val=0.001, penalty=0.07, max_impacts=20):
    """
    система работает и произошло >=2 ударов одновременно
    """
    P_work = 0
    for m in range(2, max_impacts + 1):
        r_new = max(0.01, r - m * penalty)
        P_m = (lambda_val ** m) * math.exp(-lambda_val) / math.factorial(m)
        P_for_different_modules = sum(math.comb(6, i) * (r_new ** i) * ((1 - r_new) ** (6 - i))
                                      for i in range(4, 7))
        P_work += P_m * P_for_different_modules
    return P_work


def calculate_P_work_conditional_2more(r=0.93, lambda_val=0.001, penalty=0.07, max_impacts=20):
    """
    система работает при условии, что произошло ≥2 ударов
    P(раб | m≥2) = P(раб и m≥2) / P(m≥2)
    """
    P_work_joint = 0
    P_2more = 0
    for m in range(2, max_impacts + 1):
        r_new = max(0.01, r - m * penalty)
        P_m = (lambda_val ** m) * math.exp(-lambda_val) / math.factorial(m)
        P_work_given_m = sum(math.comb(6, i) * (r_new ** i) * ((1 - r_new) ** (6 - i))
                             for i in range(4, 7))
        P_work_joint += P_m * P_work_given_m
        P_2more += P_m
    return P_work_joint / P_2more if P_2more > 0 else 0


def calculate_total_P_work(r=0.93, lambda_val=0.001, penalty=0.07, max_impacts=20):
    """
    Расчёт общей P(раб) - полной вероятности работы системы
    """
    total_P_work = 0
    for m in range(0, max_impacts + 1):
        r_new = max(0.01, r - m * penalty)
        P_m = (lambda_val ** m) * math.exp(-lambda_val) / math.factorial(m)
        P_work_given_m = sum(math.comb(6, i) * (r_new ** i) * ((1 - r_new) ** (6 - i))
                             for i in range(4, 7))
        total_P_work += P_m * P_work_given_m
    return total_P_work


def calculate_P_S_work_P_S_notwork(r, lambda_val, penalty=0.07):
    """
    Расчёт P(S|раб) и P(S|не раб) на основе состояния системы
    """
    P_work_scenarios = []
    P_fail_scenarios = []
    total_P = sum((lambda_val ** m) * math.exp(-lambda_val) / math.factorial(m) for m in range(0, 5))
    for m in range(0, 5):
        p_module = max(0.01, r - m * penalty)
        P_m = (lambda_val ** m) * math.exp(-lambda_val) / math.factorial(m)
        P_m_normalized = P_m / total_P
        module_states_probs = [math.comb(6, i) * (p_module ** i) * ((1 - p_module) ** (6 - i))
                               for i in range(7)]
        P_work = sum(module_states_probs[4:])
        P_fail = sum(module_states_probs[:4])
        signal_prob_if_work = 0
        signal_prob_if_fail = 0
        for i in range(7):
            prob_state = module_states_probs[i]
            faulty_modules = 6 - i
            signal_prob = min(0.95, 0.05 + 0.15 * faulty_modules)
            if i >= 4:
                if P_work > 0:
                    signal_prob_if_work += (prob_state / P_work) * signal_prob
            else:
                if P_fail > 0:
                    signal_prob_if_fail += (prob_state / P_fail) * signal_prob
        P_work_scenarios.append(P_m_normalized * signal_prob_if_work)
        P_fail_scenarios.append(P_m_normalized * signal_prob_if_fail)
    P_S_work = sum(P_work_scenarios)
    P_S_notwork = sum(P_fail_scenarios)
    return P_S_work, P_S_notwork


r = 0.93
lambda_val = 0.001
penalty = 0.07
max_impacts = 20
P_work = calculate_total_P_work(r, lambda_val, penalty, max_impacts)
P_work_2more = calculate_P_work_conditional_2more(r, lambda_val, penalty, max_impacts)
P_S_work, P_S_notwork = calculate_P_S_work_P_S_notwork(r, lambda_val, penalty)
print(f"P(S|раб) = {P_S_work:.3f}")
print(f"P(S|не раб) = {P_S_notwork:.3f}")
print(f"P(раб|≥2 ударов) = {P_work_2more:.3f}")
