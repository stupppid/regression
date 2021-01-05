import random
import matplotlib.pyplot as plt

true_theta0 = random.random()
true_theta1 = random.random()
points = []
x = []
y = []
n = 100
def generate_dots(n):
    global points
    for i in range(1, n):
        p = random.randint(0,100)
        x.append(p)
        y.append(true_theta0 + true_theta1 * p + (random.random() - 0.5) * 5)
    points = list(zip(x, y))

generate_dots(n)

theta0 = 1
theta1 = 1
alpha = 0.0001

def cost_func_derivative0():
    p = 0
    for point in points:
        p += (theta0 + theta1 * point[0] - point[1]) * 2
    return p / len(points)

def cost_func_derivative1():
    p = 0
    for point in points:
        p += (theta0 + theta1 * point[0] - point[1]) * 2 * point[0]
    return p / len(points)

# lmd is the parameter to minimize the thetas' value for regulization
def calc_theta(lmd = 0):
    global theta0, theta1
    for i in range(1, 1000):
        print(cost_func_derivative0())
        temp0 = theta0 - alpha * cost_func_derivative0()
        temp1 = theta1 * (1 - lmd * alpha / len(points)) - alpha * cost_func_derivative1()
        theta0 = temp0
        theta1 = temp1
    print(theta0, theta1, true_theta0, true_theta1)
    t = [theta0 + theta1 * i for i in x]
    plt.plot(x, y, 'ro')
    plt.plot(x, t)
    plt.show()

calc_theta(1)