import math
import random
import matplotlib.pyplot as plt 

class Neural():
    def __init__(self, input_data, output_data, thetas) -> None:
        self.first_layer = NeuralLayer(input_data, output_data, thetas, 1)
        self.last_layer = self.first_layer
        while(self.last_layer.next_layer != None):
            self.last_layer = self.last_layer.next_layer

    def __forward_propagation(self):
        self.first_layer.forward_propagation()

    def __backward_propagation(self):
        self.last_layer.backward_propagation()

    def train(self, input_data, output_data):
        self.first_layer.data = input_data
        self.last_layer.true_data = output_data
        self.__forward_propagation()
        self.__backward_propagation()
    
    def get_output(self, input_data, output_data):
        """
        calculate the output data based on the trained theta value
        """
        self.first_layer.data = input_data
        self.last_layer.true_data = output_data
        self.__forward_propagation()
        return [input_data, output_data, self.last_layer.data]

class NeuralLayer():
    __LAMDA = 0.01
    __ALPHA = 0.5
    def __init__(self, data, output_data, theta, layer_pos, base_layer = None) -> None:
        self.next_layer = None
        self.back_layer = base_layer
        self.layer_pos = layer_pos
        self.delta = []
        self.accumulator = []
        self.data = data
        self.bias = 1
        self.true_data = None
        if layer_pos <= len(theta):
            self.theta = theta[layer_pos - 1]
            self.next_layer = NeuralLayer(self.__calculate_next_layer(), output_data, theta, layer_pos + 1, self)
        if layer_pos == len(theta):
            self.next_layer.true_data = output_data

    def forward_propagation(self):
        if self.next_layer != None:
            self.next_layer.data = self.__calculate_next_layer()
            self.next_layer.forward_propagation()

    def __calculate_next_layer(self):
        next_layer_data = [0] * len(self.theta)
        for i, theta in enumerate(self.theta):
            for j, data in enumerate([self.bias, *self.data]):
                next_layer_data[i] += data * theta[j]
        return [self.__sigmoid(data) for data in next_layer_data]
    
    def __sigmoid(self, data):
        return 1 / (1 + math.e ** -data)

    def backward_propagation(self):
        if self.true_data != None:
            self.delta = [d[0] - d[1] for d in zip(self.data, self.true_data)]
        else:
            self.__calc_delta()
            self.__calc_accumulator()
            self.__update_theta()
        if self.back_layer != None:
            self.back_layer.backward_propagation()

    def __calc_delta(self):
        error_theta = [0] * 10
        for i, ti in enumerate(self.theta):
            for j, tj in enumerate(ti):
                error_theta[j] += self.theta[i][j] * self.next_layer.delta[i]
        error_net = [d * (1 - d) for d in self.data]
        self.delta = [d[0] * d[1] for d in zip(error_net, error_theta)]

    def __calc_accumulator(self):
        delta = self.next_layer.delta
        a = self.data
        self.accumulator = [[0] * (len(a) + 1)] * len(delta)
        for i, di in enumerate(delta):
            for j, aj in enumerate([self.bias, *a]):
                self.accumulator[i][j] = di * aj
    
    def __update_theta(self):
        m = 1
        for i, ac_i in enumerate(self.accumulator):
            for j, ac_ij in enumerate(ac_i):
                if j != 0:
                    self.theta[i][j] -= self.__ALPHA * (ac_ij / m + self.__LAMDA * self.theta[i][j])
                else:
                    self.theta[i][j] -= self.__ALPHA * ac_ij / m
        
def generate_dots(n = 100):
    """
    generate dots based on a quadratic function curve, the dots under the curve is false
    """
    x1 = [random.random() for i in range(n)]
    x2 = [random.random() for i in range(n)]
    plt.plot(sorted(x1), [(2 * xi - 0.3) * (xi - 0.45) * (xi - 0.6) + 0.3 for xi in sorted(x1)])
    y = [(2 * x1[i] - 0.3) * (x1[i] - 0.45) * (x1[i] - 0.6) + 0.3 - x2[i] > 0 for i in range(n)]
    return [[[d[0], d[1]], [d[2]]] for d in list(zip(x1, x2, y))]

def plot(points):
    """
    the round is the calculated value, * is the true value
    """
    plt.plot([point[0][0] for point in points if point[1][0]],[point[0][1] for point in points if point[1][0]], 'ro' )
    plt.plot([point[0][0] for point in points if not point[1][0]],[point[0][1] for point in points if not point[1][0]], 'bo' )
    plt.plot([point[0][0] for point in points if point[2][0] > 0.5],[point[0][1] for point in points if point[2][0] > 0.5], 'r+' )
    plt.plot([point[0][0] for point in points if not point[2][0] > 0.5],[point[0][1] for point in points if not point[2][0] > 0.5], 'b+' )
    plt.show()

def main():
    # all theta start with random value
    theta1 = [[random.random()] * 3, [random.random()] * 3]
    # theta3 = [[random.random()] * 3, [random.random()] * 3]
    theta2 = [[random.random()] * 3]
    training_sets = generate_dots()
    nn = Neural(*training_sets[0], (theta1, theta2))
    for i in range(1000):
        nn.train(*random.choice(training_sets))

    # input new data, see if the neural network really work
    test_sets = generate_dots(100)
    data = []
    for point in test_sets:
        data.append(nn.get_output(*point))
    error_data = [d for d in data if d[1][0] != (d[2][0] > 0.5)]
    print('error points rate: %.2f' % (len(error_data) / len(data) * 100) + r'%')
    plot(data)

if __name__ == '__main__':
    main()