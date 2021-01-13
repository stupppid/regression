import random
import matplotlib.pyplot as plt 

points = []
k = 3
n = 100
r = 7
u = [0] * k
c = [0] * n
tu = [0] * k
def generate_dots(k, n, r):
    global points
    for i in range(0, k):
        tu[i] = [random.randint(r, 100 - r), random.randint(r, 100 - r)]
    for i in range(0, n):
        tmp = random.choice(tu)
        x = tmp[0] + random.random() * 2 * r - r
        y = tmp[1] + random.random() * 2 * r - r
        # x = random.randint(0,100)
        # y = random.randint(0,100)
        points.append([x,y])

def calc_distance(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def k_means():
    """
    when the dataset already have some clear boundary, initial the centroid by hand first. or else one centroid would be with no data.
    """
    global points, u, k, n, c, r
    for i in range(0, 100):
        d = [[0] * k for i in range(0, n)]
        for i in range(0, k):
            # u[i] = [random.randint(r, 100 - r), random.randint(r, 100 - r)]
            u[i] = [tu[i][0] + random.randint(-10,10), tu[i][1] + random.randint(-10,10)]
        for i in range(0, n):
            tmp = 1000000
            for j in range(0, k):
                d[i][j] = calc_distance(points[i], u[j])
                if tmp > d[i][j]:
                    tmp = d[i][j]
                    c[i] = j
        sum = [[0,0] for i in range(0, k)]
        num = [0] * k
        for i in range(0, n):
            sum[c[i]] = [points[i][0] + sum[c[i]][0], points[i][1] + sum[c[i]][1]]
            num[c[i]] = num[c[i]] + 1
        u = [[sum[i][0] / num[i], sum[i][1] / num[i]] for i in range(0, k)]
        plt.cla()
        plot_figure()
        plt.pause(0.1)
        

def plot_figure():
    color = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    for i in range(0, k):
        plt.plot([point[0] for idx, point in enumerate(points) if c[idx] == i], [point[1] for idx, point in enumerate(points) if c[idx] == i], color[i] + 'o')
        plt.plot([point[0] for point in u], [point[1] for point in u], color[i] + 'x')
    plt.show()

def main():
    plt.ion()
    generate_dots(k, n, r)
    k_means()
    plt.ioff()
    plt.show()

main()