Markov chains lab
=================

The learning goals of this lab are:

- to learn how to use Markov chains to model a system,
- to learn how to simulate a Markov chain with SimPy.

1 - Discrete-time Markov chain - Tennis
-----------------------------------------

In this exercise, we will model a tennis game as a discrete-time Markov chain. The states of the Markov chain will represent the score of the game, and the transitions between states will represent the possible outcomes of each point played.

Assume that the players have a fixed 'strength' such that player A wins a point with probability *p* and loses with probability *1-p*.

We want to explore the probability of winning a game as a function of the probability *p* of winning a point.


### 1.1 Transition matrix

Assume the following model:

- There are two players, A and B.
- The points are counted as: 0 - 15 - 30 - 40.
- We apply a simplified scoring: the first player to reach 40 wins the game. There are no deuces or advantages.
- The states of the Markov chain will represent the score of the game, i.e., the pairs (Points A, Points B).
- The constant *p* is the probability that player A wins a point. Player B wins with probability *1-p*.

The transition matrix of this model has too many states to create it manually.

You have to complete the code in the existing file `./models/tennis.py` to implement this model.

#### Todo

- [ ] Complete the function `def transition_matrix(p)` that fills the transition matrix for the tennis Markov chain and returns it as a Numpy array.
      The parameter `p` is the probability that player A wins a point.
- [ ] Answer the questions in file `Questions-tennis.md`.


### 1.2 - Limiting distributions

The Markov chain is not recurrent and therefore does not have a unique stationary distribution. 
It does have limiting distributions. Of course, they are not unique, but depend on the initial state.
Since a tennis game always starts with the score (0, 0), we can compute the limiting distribution from this initial state.

#### Todo

- [ ] Complete the function `def limiting_distributions(P, n)` that computes the limiting distributions of the transition matrix P, for n steps.
- [ ] Answer the questions in file `Questions-tennis.md`.


### 1.3 - Winning probabilities

The winning probability of player A can be computed from the limiting distributions and the correct initial state.

#### Todo

- [ ] Complete the function `def winning_probability(p)` that computes the winning probability of player A.
- [ ] After completing all functions, run the `main()` function in `tennis_solution.py` to plot the winning probabilities for different values of `p`.
- [ ] Answer the questions in file `Questions-tennis.md`.


### 1.4 - Checklist for the tennis model

- [ ] You've answered all questions in the `Questions-tennis.md` file.
- [ ] You have a file `./models/tennis.py` with the following code:
  - [ ] the function `def transition_matrix(p)` that returns the transition matrix for the tennis Markov chain.
  - [ ] a function `def limiting_distribution(P, n)` that computes the limiting distribution of the transition matrix P, for n steps.
  - [ ] a function `def winning_probability(p)` that computes the winning probability of player A.
  - [ ] the `main()` function runs without errors and generates the plot of winning probabilities.
- [ ] You have a file `tennis_win_probability.png` with the plot of the winning probabilities.



2 - Continuous-time Markov chain - Computer worm infection
----------------------------------------------------------

In this exercise we will simulate a worm infection of a server farm using Markov chains.

Suppose that we have a server farm with 1'000 servers. Each server can be in one of three states:

- **Susceptible**: the server is susceptible to infection.
- **Infected**: the server is currently infected.
- **Recovered**: the server has been recovered and is not susceptible to infection anymore.

The transitions between these states can be modeled as a continuous-time Markov chain. A susceptible server can become infected with rate `infection_rate`. An infected server can heal and become recovered with rate `recovery_rate`.

This model is difficult to implement directly. The states are all possible triples `(susceptible, infected, recovered)` with the number of servers in each state. These are far too many states to model.

### 2.1 Gillespie algorithm

The Gillespie algorithm is a simulation algorithm that allows us to easily simulate this model. Instead of simulating all states and their transitions in contiuous time, it proceeds in three steps:

1. Compute the time until the next event.
2. Determine which of the possible events has happened and update the state accordingly.
3. Repeat

##### Compute the time until the next event

A susceptible server can become infected with rate *infection_rate*. If we have *n* susceptible servers, we can define an *infection_propensity* as *n * infection_rate*.

An infected server can heal and become recovered with rate *recovery_rate*. If we have *m* infected servers, the *recovery_propensity* equals *m * recovery_rate*.

In a continuous-time Markov chain, the time until the next transition has an exponential distribution. Since there are several different events that may occur with different rates, the next event occurs at a rate that is the some of the individual rates. 

We can thus simply generate the time *tau* until the next event like this:

```python
import numpy as np
infection_propensity = num_susceptible * infection_rate
recovery_propensity = num_infected * recovery_rate
total_propensity = infection_propensity + recovery_propensity
tau = np.random.exponential(1 / total_propensity)
```

##### Determine the next event

After waiting for time *tau*, we need to determine which event of the possible events has occurred. We have two types of events: a new infection or a server becomes immune. They occur with probabilities proportional to their propensities. We can use Numpy to choose the event like this:

```python
event = np.random.choice(["infection", "recovery"], p=[infection_propensity/total_propensity, recovery_propensity/total_propensity])
```

Once the type of event is determined, we can update the state accordingly:

```
if event == "infection":
    # Update the state for a new infection
    num_infected += 1
    num_susceptible -= 1
elif event == "recovery":
    # Update the state for a server becoming recovered
    num_infected -= 1
    num_recovered += 1
```

##### Repeat

We repeat these steps in a loop until the end of the simulation.

### 2.2 - SIR model

To implement the Gillespie algorithm for the SIR model, complete the code in the file `./models/sir.py`.

This model is called *SIR model* for Susceptible - Infected - Recovered. The SIR model is used to describe the behavior of epidemics. In fact, it has been used to model the propagation of the Corona virus in 2020.

However, this model is not realistic for computers: computers do not have an immune system and do not heal by themselves. They have to be patched by the system administrators.

#### Todo

- [ ] Implement the Gillespie algorithm in the `./models/sir.py` file.
- [ ] Run the simulation to generate the plot for the SIR model.
- [ ] Answer the questions in file `Questions-worm.md`, section 2.2.

### 2.3 - Realistic computer worm model

Let's implement a more realistic model for computer worms.


- We will assume that the system adminstrators can patch infected or vulnerable servers with a *fixed* rate, such as 5 servers per unit of time.
- They will first patch infected servers, if there are any.
- If there are no infected servers, they will patch susceptible servers.
- If there aren't any infected or susceptible servers, we can stop the simulation, since no new events will happen.

#### Todo

- [ ] Copy the file `./models/sir.py` to `./models/worm.py`. Only edit this new file.
- [ ] Change the name of the plot to `worm_infection_simulation.png`.
- [ ] Change the `recovery_propensity` to make it fixed, independent of the number of infected servers.
- [ ] If the next event is `recovery` first try repairing an infected server if there are any. If not, repair a susceptible server. If there aren't any servers left to repair, stop the simulation.
- [ ] Run the simulation with `infection_rate = 0.1` and `recovery_rate = 5.0`.
- [ ] Answer the questions in the file `Questions-worm.md`.


### 2.4 - Checklist for the worm model

- [ ] You've answered all questions in the `Questions-worm.md` file.
- [ ] You have a file `./models/sir.py`. It runs without errors and generates the plot `sir_infection_simulation.png`.
- [ ] You have a file `./models/worm.py`. It runs without errors and generates the plot `worm_infection_simulation.png`.
