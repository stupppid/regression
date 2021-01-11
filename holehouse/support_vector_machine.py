from math import isnan
import random
import matplotlib.pyplot as plt 

"""
are there any codes wrong?
"""

points = []
alpha = []
b = 0
raw_a = 0.6
raw_b = 20
def generate_dots(n):
    global points,alpha
    a = raw_a
    b = raw_b
    for i in range(1, n):
        x = random.randrange(0,100)
        y = random.randrange(0,100)
        if y > a * x + b + 5 or y < a * x + b - 5:
            if y > a * x + b: 
                t = (x, y, 1)
            else:
                t = (x, y, -1)
            points.append(t)
    alpha = [1 / len(points)] * len(points)

def kernal(i,j):
    global points
    return points[i][0] * points[j][0] + points[i][1] * points[j][1]

def fun(i):
    global points, alpha
    sum = 0
    for j in range(0, len(points)):
        sum += kernal(i,j) * points[j][2] * alpha[j]
    return sum

def ei(i):
    global points
    return fun(i) - points[i][2]

def calc_alpha(i, j):
    global b, alpha, points
    new_alphaj = alpha[j] + points[j][2] * (ei(i) - ei(j)) / (kernal(1,1) + kernal(1,2) - 2*kernal(1,2))
    constant = alpha[i] * alpha[i] + alpha[j] * alpha[j]
    u = 0
    v = 0
    if points[i][2] * points[j][2] == -1:
        u = max(0, alpha[j] - alpha[i])
        v = min(constant, constant + alpha[j] - alpha[i])
    else:
        u = max(0, alpha[j] + alpha[i] - constant)
        v = min(constant, alpha[j] + alpha[i])
    if new_alphaj > v:
        new_alphaj = v
    if new_alphaj < u:
        new_alphaj = u
    new_alphai = alpha[i] + points[i][2] * points[j][2] * (alpha[j] - new_alphaj)
    alpha[j] = new_alphaj
    alpha[i] = new_alphai
    b = (points[i][2] - fun(i) + points[j][2] - fun(j)) / 2

def loop():
    global b, alpha, points
    l = len(alpha)
    w = 0
    last_w = sum([i for i in alpha]) - 0.5 * sum([points[i][2] * points[j][2] * alpha[i] * alpha[j] * kernal(i,j) for i in range(0,l) for j in range(0,l)])
    gap = 1
    n = 0
    while gap > 0.001 and n < 1000:
        for i in range(0, len(alpha) - 1):
            calc_alpha(i,i + 1)
        # for i in range(0, len(alpha) - 1):
        #     for j in range(0, len(alpha) - 1):
        #         if i != j:
        #             calc_alpha(i,j)
        w = sum([i for i in alpha]) - 0.5 * sum([points[i][2] * points[j][2] * alpha[i] * alpha[j] * kernal(i,j) for i in range(0,l) for j in range(0,l)])
        gap = (w - last_w) / last_w
        if abs(w) > 1e+7 or isnan(w) or abs(b) > 1e+7:
            print('error! b: {}, w: {}'.format(b, w))
            break
        print("value: {}, last value: {}".format(w, last_w))
        last_w = w
        n = n + 1

def main():
    generate_dots(1000)
    loop()
    w1 = 0
    w2 = 0
    for i in range(0, len(alpha)):
        w1 += points[i][0] * points[i][2] * alpha[i]
        w2 += points[i][1] * points[i][2] * alpha[i]
    plt.plot([p[0] for p in points if 1 == p[2]], [p[1] for p in points if 1 == p[2]], 'ro')
    plt.plot([p[0] for p in points if 1 != p[2]], [p[1] for p in points if 1 != p[2]], 'b*')
    plt.plot([p for p in range(1, 100)], [raw_a * p + raw_b for p in range(1, 100)], 'r')
    plt.plot([p for p in range(1, 100)], [-(b + w1 * p) / w2 for p in range(1, 100)], 'b')
    plt.show()
    print('a: {}, b: {}\nraw_a: {}, raw_b: {}'.format(-w1/w2, -b / w2, raw_a, raw_b))

if __name__ == '__main__':
    main()

