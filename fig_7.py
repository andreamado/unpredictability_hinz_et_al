from common import *
from fitness_effects import *

correlation_coefficients = np.zeros((n_mutations, n_envs, n_envs))
env_pairs = []
env_pair_idx = []

# Load all data
for env1 in range(n_envs):
    for env2 in range(n_envs):
        if env1 > env2:
            fig, ax = plt.subplots(1,1)

            for i in range(n_mutations):
                fe1 = flatten_and_clean_nans(fitness_effects[env1, :, i])
                fe2 = flatten_and_clean_nans(fitness_effects[env2, :, i])

                fe1_err = flatten_and_clean_nans(fitness_effects_errors[env1, :, i])
                fe2_err = flatten_and_clean_nans(fitness_effects_errors[env2, :, i])

                samples = np.zeros(100)
                for k in range(len(samples)):
                    e1 = np.random.normal(np.zeros(len(fe1)), fe1_err)
                    e2 = np.random.normal(np.zeros(len(fe2)), fe2_err)
                    samples[k] = pearson_correlation_coefficient(fe1 + e1, fe2 + e2)

                correlation_coefficient = (np.around(np.mean(samples), 4), np.around(np.std(samples), 4))
                correlation_coefficients[i, env1, env2] = correlation_coefficient[0]
                correlation_coefficients[i, env2, env1] = correlation_coefficient[1]

            env_pairs.append((environments[env1], environments[env2]))
            env_pair_idx.append((env1, env2))

env_pair_names = [f'{a[0]}_{a[1]}' for a in env_pairs]


if True:
    fig, ax = plt.subplots(1, 2, figsize=(14,6))

    ax0, ax1 = ax

    ax0.set_ylabel(r'Correlation of fitness effects', fontsize=12)
    ax0.set_xticks(np.arange(n_env_pairs))
    ax1.set_xticks(np.arange(n_env_pairs))
    ax0.set_xticklabels([f'{a[0]} x {a[1]}' for a in env_pairs])
    ax1.set_xticklabels([f'{a[0]} x {a[1]}' for a in env_pairs])

    ax0.set_ylim([-0.8, 1.1])
    ax1.set_ylim([-0.8, 1.1])

    for i in range(n_mutations):
        coefs     = np.zeros(n_env_pairs)
        coefs_std = np.zeros(n_env_pairs)

        for pair, (e1, e2) in enumerate(env_pair_idx):
            coefs[pair]     = correlation_coefficients[i, e1, e2]
            coefs_std[pair] = correlation_coefficients[i, e2, e1]

        ax1.errorbar(range(n_env_pairs), coefs, coefs_std, fmt='o', label=mutations[i], color=COLORS[i])
        ax1.hlines(coefs.mean(), 0, n_env_pairs-1, linestyles='dashed', color=COLORS[i])

    if True:
        coefs     = np.zeros(n_env_pairs)
        coefs_std = np.zeros(n_env_pairs)

        for pair, (e1, e2) in enumerate(env_pair_idx):
            coefs[pair]     = np.mean(correlation_coefficients[:, e1, e2])
            coefs_std[pair] = np.std(correlation_coefficients[:, e1, e2])

        ax0.errorbar(range(n_env_pairs), coefs, coefs_std, fmt='o', color=COLORS[-1])
        ax0.hlines(coefs.mean(), 0, n_env_pairs-1, linestyles='dashed', color=COLORS[-1])


    plt.setp(ax0.get_xticklabels(), rotation=30, ha='right', rotation_mode='anchor')
    plt.setp(ax1.get_xticklabels(), rotation=30, ha='right', rotation_mode='anchor')

    left_shift = 0.05
    box = ax0.get_position()
    ax0.set_position([box.x0-left_shift, box.y0+0.05, box.width, box.height * 1.0])

    box = ax1.get_position()
    ax1.set_position([box.x0-left_shift, box.y0+0.05, box.width, box.height * 1.0])


    leg = plt.legend(title='Mutation', bbox_to_anchor=(1.05, 0.5), loc='center left', frameon=False)
    leg._legend_box.align = 'left'
    plt.setp(leg.get_title(), fontsize=12)

    plt.savefig(f'figs/fig_7.pdf')
    plt.savefig(f'figs/fig_7.png', dpi=1200)
    print('Figures:')
    print('\tfigs/fig_7.pdf')
    print('\tfigs/fig_7.png')
    
    plt.close('all')


with open('generated_data/fitness_effects_correlation_across_environments.dat', 'w') as f:
    f.write('#env1\tenv2')
    for mutation in mutations:
        f.write(f'\t{mutation}\tstd')
    f.write('\n')

    for pair, (e1, e2) in enumerate(env_pair_idx):
        f.write(f'{environments[e1]}\t{environments[e2]}')
        for i in range(n_mutations):
            f.write(f'\t{correlation_coefficients[i, e1, e2]}\t{correlation_coefficients[i, e2, e1]}')
        f.write('\n')

print('Data:')
print('\tgenerated_data/fitness_effects_correlation_across_environments.dat')