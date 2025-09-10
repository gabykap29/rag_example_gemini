def score_to_probability(score: float, min_score = 160, max_score= 500):
    norm = ( max_score - score) / (max_score / min_score)
    
    probability = max(0, min(1, norm)) * 100
    return probability
    