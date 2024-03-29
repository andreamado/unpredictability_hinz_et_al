from common import *
from fitness_effects import *

################################################################################
# Correlation of fitness effects with background distances
#
################################################################################
distances = np.zeros((n_backgrounds, n_backgrounds, n_mutations))
for back1 in range(n_backgrounds):
    for back2 in range(n_backgrounds):
        for i in range(n_mutations):
            if back1 == back2 or np.isnan(fitness_effects[0, back1, i]) or np.isnan(fitness_effects[0, back2, i]):
                distances[back1, back2, i] = np.nan
            else:
                distances[back1, back2, i] = philogenetic_distances[back1, back2]

if recalculate:
    r_samples = np.zeros((n_samples, n_envs))
    for s in range(n_samples):
        f_effects = fitness_effects + np.random.normal(np.zeros(fitness_effects.shape), fitness_effects_errors)

        difference_in_fitness_effects = np.zeros((n_envs, n_backgrounds, n_backgrounds, n_mutations))
        for env in range(n_envs):
            for back1 in range(n_backgrounds):
                for back2 in range(n_backgrounds):
                    for i in range(n_mutations):
                        if back1 == back2:
                            difference_in_fitness_effects[env, back1, back2, i] = np.nan
                        else:
                            difference_in_fitness_effects[env, back1, back2, i] = np.abs(f_effects[env, back1, i] - f_effects[env, back2, i])

        for env in range(n_envs):
            r_samples[s, env] = pearson_correlation_coefficient(distances, difference_in_fitness_effects[env])

    with open('generated_data/difference_in_fitness_effects_philogenetic_distance_correlation.dat', 'w') as f:
        f.write('#environment\tcorrelation\tcorrelation_std\tpvalue\n')
        for env in range(n_envs):
            pvalue = p_value(np.mean(r_samples[:, env]), 0., np.std(r_samples[:, env]))
            f.write(f'{environments[env]}\t{np.mean(r_samples[:, env])}\t{np.std(r_samples[:, env])}\t{pvalue}\n')

    print('Data:')
    print('\tgenerated_data/difference_in_fitness_effects_philogenetic_distance_correlation.dat')



f_effects = fitness_effects

difference_in_fitness_effects = np.zeros((n_envs, n_backgrounds, n_backgrounds, n_mutations))
for env in range(n_envs):
    for back1 in range(n_backgrounds):
        for back2 in range(n_backgrounds):
            for i in range(n_mutations):
                if back1 == back2:
                    difference_in_fitness_effects[env, back1, back2, i] = np.nan
                else:
                    difference_in_fitness_effects[env, back1, back2, i] = np.abs(f_effects[env, back1, i] - f_effects[env, back2, i])


if replot:
    fig, ax = plt.subplots(2, 2, figsize=(10, 10/3*2))

    idx = 0
    for env in range(n_envs):
        cax = ax[idx//2, idx%2]

        for i in range(n_mutations):
            fe, fb = flatten_and_clean_nans(difference_in_fitness_effects[env, :, :, i], distances[:, :, i])

            cax.plot(fb, fe, '.', label=f'{mutations[i]}', color=COLORS[i])
            linear_fit(fb, fe, COLORS[i], ax=cax, alpha=0.05)

        cax.set_xlim([0.0, 0.05])
        cax.set_ylim([-0.05, 0.85])

        cax.set_xticks(np.arange(0, 0.055, 0.01))
        cax.set_yticks(np.arange(0., 0.85, 0.2))

        cax.set_title(f'{environments[env]}', fontsize=12)
        cax.set_xlabel(f'philogenetic distance', fontsize=12)
        cax.set_ylabel(f'difference in fitness effects', fontsize=12)

        idx += 1

    plt.legend(title='Mutation', frameon=False, bbox_to_anchor=(1.05, 0.5), loc='center left')

    plt.tight_layout()

    print('Figures:')
    plt.savefig('figs/fig_S10.pdf')
    print('\tfigs/fig_S10.pdf')
    plt.savefig('figs/fig_S10.png', dpi=1200)
    print('\tfigs/fig_S10.png')

    plt.close('all')
