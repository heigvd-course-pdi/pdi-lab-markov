"""Simulate a computer worm infection (SIR model) using the Gillespie algorithm"""

import numpy as np
import simpy
from matplotlib import pyplot as plt

class ServerFarm:
    num_servers = 1000
    num_susceptible = num_servers
    num_infected = 0
    num_recovered = 0
    trace_susceptible = []
    trace_infected = []
    trace_recovered = []

    def run(self, env, infection_rate, recovery_rate):
        while True:
            # Compute the time until the next event:
            infection_propensity = xxx ### COMPLETE HERE
            recovery_propensity = xxx ### COMPLETE HERE
            total_propensity = xxx ### COMPLETE HERE

            if total_propensity == 0: break  # No more events can occur
            tau = np.random.exponential(1/total_propensity) if total_propensity > 0 else float('inf')

            # Wait until the next event
            yield env.timeout(tau)

            # Determine the type of event (infection or recovery)
            event = xxx ### COMPLETE HERE
            if event == 'infection':
                xxx ### COMPLETE HERE
            elif event == 'recovery':
                xxx ### COMPLETE HERE


    def trace(self, env, interval):
        while True:
            yield env.timeout(interval)
            self.trace_susceptible.append(self.num_susceptible)
            self.trace_infected.append(self.num_infected)
            self.trace_recovered.append(self.num_recovered)


def main():
    env = simpy.Environment()
    server_farm = ServerFarm()
    env.process(server_farm.run(env, infection_rate=0.1, recovery_rate=0.1))
    env.process(server_farm.trace(env, interval=1))
    env.run(until=200)

    # Plot results
    plt.plot(server_farm.trace_susceptible, label='Susceptible')
    plt.plot(server_farm.trace_infected, label='Infected')
    plt.plot(server_farm.trace_recovered, label='Recovered')
    plt.xlabel('Time')
    plt.ylabel('Number of Servers')
    plt.legend()
    plt.savefig('sir_infection_simulation.png')

if __name__ == "__main__":
    main()
