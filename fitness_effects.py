from common import *

test = False

# import fitness effects of mutations
_present = np.zeros((n_envs, n_backgrounds, n_mutations), dtype=int)
fitness_effects = np.zeros((n_envs, n_backgrounds, n_mutations), dtype=float)
fitness_effects_errors = np.zeros((n_envs, n_backgrounds, n_mutations), dtype=float)

# Load data
_data = np.loadtxt('data/data.dat')
for line in _data:
    env = int(line[0])

    i = int(line[1])
    j = int(line[2]) - 1
    f = line[5]

    # ignore the backgrounds
    if j >= 0:
        _present[env, i, j] += 1
        fitness_effects[env, i, j] += f
        fitness_effects_errors[env, i, j] += f**2


# Calculate the mean fitness effects and corresponding standard deviations,
# filling any missing values with np.nan
for env in range(n_envs):
    for i in range(n_backgrounds):
        for j in range(n_mutations):
            N = _present[env, i, j]
            if N == 0:
                fitness_effects[env, i, j] = np.nan
                fitness_effects_errors[env, i, j] = np.nan
            else:
                fitness_effects[env, i, j] /= N
                x2 = fitness_effects_errors[env, i, j] / N
                fitness_effects_errors[env, i, j] = np.sqrt((x2 - fitness_effects[env, i, j]**2) / (N-1))


# import background fitness
_present = np.zeros((n_envs, n_backgrounds), dtype=int)
background_fitness = np.zeros((n_envs, n_backgrounds))
background_fitness_errors = np.zeros((n_envs, n_backgrounds))


# Load data
_data = np.loadtxt('data/ancestors.dat')

for line in _data:
    env = int(line[0])
    i = int(line[1])

    f = line[4]
    if not np.isnan(f):
        _present[env, i] += 1
        background_fitness[env, i] += f
        background_fitness_errors[env, i] += f**2

# Calculate the mean background fitnesses and corresponding standard deviations,
# filling any missing values with np.nan
for env in range(n_envs):
    for i in range(n_backgrounds):
        N = _present[env, i]
        if N == 0:
            background_fitness[env, i] = np.nan
            background_fitness_errors[env, i] = np.nan
        else:
            background_fitness[env, i] /= N
            x2 = background_fitness_errors[env, i] / N
            background_fitness_errors[env, i] = np.sqrt((x2 - background_fitness[env, i]**2) / (N-1))


# import philogenetic distances
philogenetic_distances = np.loadtxt('data/distance_matrix.txt', usecols=np.arange(1,13))
order = []
names = []
with open('data/distance_matrix.txt') as f:
    for line in f:
        background = line.split()[0]
        names.append(background)
        order.append(backgrounds.index(background))


# reordering the distances matrix to match the order of the data
swap_matrix = np.zeros((n_backgrounds, n_backgrounds))
for l in range(n_backgrounds):
    swap_matrix[l, order[l]] = 1

philogenetic_distances = swap_matrix.dot(philogenetic_distances.dot(swap_matrix.T))
np.fill_diagonal(philogenetic_distances, np.nan)
