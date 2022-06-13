def grading(score):
    i = 0
    j = 1.525
    for i in range(0, 100):
        if i < score:
            i = i + 1
            j = j + 0.025
    return round(j, 3)

