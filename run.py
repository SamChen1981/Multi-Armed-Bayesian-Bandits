import numpy as np
import matplotlib.pyplot as plt

from bandit import *
from agents import *

def run(env, agents):
    rewards = []
    rewards_max = []
    
    _, _, d, _ = env.reset()
    for a in agents:
        a.reset()
    while not d:
        draw = True
        rewards_ = []
        for agent in agents:
            a = agent.action()
            _, r, d, _ = env.step(a, draw)
            draw = False
            agent.update(a, r)
            rewards_.append(r)
        rewards.append(rewards_)

    return np.array(rewards).T
def runs(num_runs, env, agents):
    rewards = []
    for i in range(num_runs):
        if (i+1)%100==0:
            print('\rrun', i, 'of', num_runs, end='')
        rewards.append(run(env, agents))

    rewards = np.array(rewards)
    rewards = np.mean(rewards, 0)
    return rewards


k = 2
max_steps = 500
num_episodes = 500
env = KBandit(k, max_steps=max_steps)

agents = [OptimalAgent(env), RandomAgent(k), FreqUCB(k)]
agents_names = ['Optimal', 'Random', 'FreqUCB']

rewards = runs(num_episodes, env, agents)


### VISUALIZE
plt.figure()
for i in range(len(agents)):
    plt.plot(rewards[i], label=agents_names[i])
    plt.title("Mean over " + str(num_episodes) + ' episodes')
plt.legend()
plt.draw()


plt.figure()
for i in range(len(agents)-1):
    plt.plot(np.cumsum(rewards[0] - rewards[i+1]), label=agents_names[i+1]+' regret')

plt.legend()
plt.show()
