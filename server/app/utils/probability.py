def score_to_probability(score: float, min_score = 160, max_score= 400):

    # interpolación lineal inversa (a mayor distancia, menor probabilidad)
    normalized = (score - min_score) / (max_score - min_score)
    probability = (1.0 - normalized) * 100.0
    if probability > 100:
        probability =  100
     
    elif probability < 0:
        probability =  0
    
    return probability
