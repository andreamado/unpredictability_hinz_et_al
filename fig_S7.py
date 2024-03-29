from common import *
from fitness_effects import *

correlation_coefficients = np.zeros((n_mutations, n_envs, n_envs))
env_pairs = []

for env1 in range(n_envs):
    for env2 in range(n_envs):
        if env1 > env2:
            for i in range(n_mutations):
                n_effects = 0
                samples = np.zeros(n_samples)
                for s in range(n_samples):
                    fe1 = flatten_and_clean_nans(fitness_effects[env1, :, i] + np.random.normal(np.zeros(fitness_effects[env1, :, i].shape), fitness_effects_errors[env1, :, i]))
                    fe2 = flatten_and_clean_nans(fitness_effects[env2, :, i] + np.random.normal(np.zeros(fitness_effects[env2, :, i].shape), fitness_effects_errors[env2, :, i]))

                    samples[s] = pearson_correlation_coefficient(fe1, fe2)
                    n_effects = len(fe1)

                correlation_coefficient = (np.around(np.mean(samples), 4), np.around(np.std(samples) / np.sqrt(n_effects), 4))
                correlation_coefficients[i, env2, env1] = correlation_coefficient[0]
                correlation_coefficients[i, env1, env2] = correlation_coefficient[1]

            env_pairs.append((environments[env1], environments[env2]))

tril = np.tril_indices(n_envs, k=-1)

fig, ax = plt.subplots(4, 2, figsize=(10, 12.5))
idx = 0

for i in range(n_mutations):
    correlation_coefs = np.copy(correlation_coefficients[i, :, :])
    correlation_coefs[tril] = np.nan
    np.fill_diagonal(correlation_coefs, np.nan)

    correlation_coefs_err = np.copy(correlation_coefficients[i, :, :])
    for k in range(n_envs):
        for j in range(n_envs):
            if j > k:
                correlation_coefs_err[k, j] = correlation_coefs_err[j, k]

    # remove the empty lines and rows
    correlation_coefs = np.delete(correlation_coefs, 0, 1)
    correlation_coefs = np.delete(correlation_coefs, 3, 0)

    correlation_coefs_err = np.delete(correlation_coefs_err, 0, 1)
    correlation_coefs_err = np.delete(correlation_coefs_err, 3, 0)

    cmap = mpl.colors.Colormap(plt.rcParams['image.cmap'])
    cmap.set_bad((0.8, 0.8, 0.8, 1))

    cax = ax[idx//2, idx%2]
    img = cax.imshow(correlation_coefs, origin='upper', aspect='equal', vmin=-1, vmax=1)

    cax.set_title(mutations[i])

    cax.set_xticks(range(n_envs-1))
    cax.set_yticks(range(n_envs-1))

    cax.set_xticklabels(environments[1:])
    cax.set_yticklabels(environments[:-1])

    print_values(correlation_coefs, correlation_coefs_err, cax)

    idx += 1

ax[3,1].set_aspect(aspect=6, anchor=(0.27,0))
fig.colorbar(img, cax=ax[3,1])

plt.tight_layout()

plt.savefig(f'figs/fig_S7.pdf')
plt.savefig(f'figs/fig_S7.png', dpi=1200)
plt.clf()

print('Figures:')
print('\tfigs/fig_S7.pdf')
print('\tfigs/fig_S7.png')
