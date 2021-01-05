import random
import math
import matplotlib.pyplot as plt 

points = []
n = 100
theta0 = 5
theta1 = 1
theta2 = 0.5
alpha = 0.001
a = random.random()
b = random.randrange(1,10)
def generate_dots():
    global points,n,a,b
    print('raw thetas a = {}, b = {}'.format(a, b))
    for i in range(1, n):
        x = random.randrange(0,100)
        y = random.randrange(0,100)
        t = (x, y, y > a * x + b)
        points.append(t)

generate_dots()
print(points[0])
def partial_derivative(i):
    global points, theta0, theta1, theta2
    p = 0
    for point in points:
        if i == 0:
            t = 1
        else:
            t = point[i - 1]
        p += (1 / (1 - math.e ** -(theta0 + theta1 * point[0] + theta2 * point[1])) - point[2])*t
    return p

# lmd is the parameter to minimize the thetas' value for regulization
def calc_theta(lmd = 0):
    global theta0, theta1, theta2
    for i in range(100):
        temp0 = theta0 - alpha * partial_derivative(0)
        temp1 = theta1 * (1 - lmd * alpha / len(points)) - alpha * partial_derivative(1)
        temp2 = theta2 * (1 - lmd * alpha / len(points)) - alpha * partial_derivative(2)
        theta2 = temp2
        theta1 = temp1
        theta0 = temp0
    

calc_theta(1)
plt.plot([p[0] for p in points if p[2]], [p[1] for p in points if p[2]], 'ro')
plt.plot([p[0] for p in points if not p[2]], [p[1] for p in points if not p[2]], 'b*')
plt.plot([p for p in range(1, 100)], [a * p + b for p in range(1, 100)], 'r')
plt.plot([p for p in range(1, 100)], [-(theta0 + theta1 * p) / theta2 for p in range(1, 100)], 'b')
plt.show()