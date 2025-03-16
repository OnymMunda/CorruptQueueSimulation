import numpy as np
from numpy import random as nr

class CorruptQueue:
    def __init__(self, lambda_, mu, sigma):
        self.single_queue = []
        self.lambda_ = lambda_
        self.mu = mu
        self.sigma = sigma
        self.current_time = 0
        self.wait_times = []
        self.system_times = []
        self.client_id = 0

    def arrival(self):
        return nr.poisson(self.lambda_)

    def service_time(self):
        return nr.normal(self.mu, self.sigma)

    def lineup(self):
        arrivals = self.arrival()
        for _ in range(arrivals):
            self.client_id += 1
            self.single_queue.append((f"Client {self.client_id}", self.current_time))

        if arrivals > 0:
            print(f"{arrivals} new clients arrived")

    def serve(self):
        if self.single_queue:
            client, arrival_time = self.single_queue.pop(0)
            service_time = self.service_time()
            wait_time = self.current_time - arrival_time
            self.current_time += service_time

            self.wait_times.append(wait_time)
            self.system_times.append(wait_time + service_time)

            print(f"Serving {client} | Wait: {wait_time:.2f} min | Total: {wait_time + service_time:.2f} min")
        else:
                print("No clients to serve")

    def run_simulation(self, iterations):
        total_clients_served = 0
        for _ in range(iterations):
            self.lineup()
            while self.single_queue:
                self.serve()
                total_clients_served += 1

        avg_wait = np.mean(self.wait_times) if self.wait_times else 0
        avg_system_time = np.mean(self.system_times) if self.system_times else 0

        print(f"Total Clients Served in {iterations} minutes: {total_clients_served}")
        print(f"Average Wait Time: {avg_wait:.2f} min")
        print(f"Average Total Time: {avg_system_time:.2f} min")
        return avg_wait, avg_system_time, total_clients_served

class CQSimulation:
    def __init__(self):
        self.run()

    def run(self):
        iterations = int(input("Simulations (mins): "))
        lambda_ = float(input("λ arrivals/min: "))
        mu = float(input(" μ Mean service time: "))
        sigma = float(input("σ Stddev of service time: "))

        corrupt_queue = CorruptQueue(lambda_, mu, sigma)
        corrupt_queue.run_simulation(iterations)

if __name__ == "__main__":
    TEST_MODE = False

    if TEST_MODE:
        print("Test mode: 2, 3, 1")
        queue = CorruptQueue(lambda_=2, mu=3, sigma=1)
        queue.run_simulation(100)
    else:
        CQSimulation()