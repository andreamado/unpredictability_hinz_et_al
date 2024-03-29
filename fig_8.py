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
    for env in range(n_envs):
        plt.plot(distances.flatten(), difference_in_fitness_effects[env].flatten(), '.', color=COLORS_ENV[env], label=f'{environments[env]}', markersize=1.5)
        linear_fit(flatten_and_clean_nans(distances), flatten_and_clean_nans(difference_in_fitness_effects[env]), COLORS_ENV[env], alpha=0.05)

    plt.xlim([0, 0.05])
    plt.ylim([-0.05, 0.85])

    plt.yticks(np.arange(0., 0.85, 0.2))

    plt.xlabel('phylogenetic distance', fontsize=12)
    plt.ylabel('difference in fitness effects', fontsize=12)

    ax = plt.gca()

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height*0.1, box.width * 0.75, box.height * 1])

    leg = plt.legend(title='Environment', bbox_to_anchor=(1.05, 0.5), loc='center left', frameon=False, markerscale=5/1.5)
    leg._legend_box.align = 'left'
    plt.setp(leg.get_title(), fontsize=12)

    error_data = np.loadtxt('generated_data/difference_in_fitness_effects_philogenetic_distance_correlation.dat', usecols=(1,3))
    for env in range(n_envs):
        plt.text(0.1, 0.9-env*0.05, f'R = {error_data[env, 0]:.3f}, p {format_p_value(error_data[env, 1])}', color=COLORS_ENV[env], transform=ax.transAxes)

    print('Figures:')
    plt.savefig('figs/fig_8B.pdf')
    print('\tfigs/fig_8B.pdf')
    plt.savefig('figs/fig_8B.png', dpi=1200)
    print('\tfigs/fig_8B.png')
    
    plt.close('all')


################################################################################
# Correlation of difference in fitness effects with difference in background fitness
#
################################################################################
f_background = np.zeros((n_envs, n_backgrounds, n_mutations))
for env in range(n_envs):
    for i in range(n_backgrounds):
        for j in range(n_mutations):
            if np.isnan(fitness_effects[env, i, j]):
                f_background[env, i, j] = np.nan
            else:
                f_background[env, i, j] = background_fitness[env, i]

f_background_errors = np.zeros((n_envs, n_backgrounds, n_mutations))
for env in range(n_envs):
    for i in range(n_backgrounds):
        for j in range(n_mutations):
            if np.isnan(fitness_effects[env, i, j]):
                f_background_errors[env, i, j] = np.nan
            else:
                f_background_errors[env, i, j] = background_fitness_errors[env, i]

if replot:
    difference_in_background_fitness = np.zeros((n_envs, n_backgrounds, n_backgrounds, n_mutations))
    for env in range(n_envs):
        for b1 in range(n_backgrounds):
            for b2 in range(n_backgrounds):
                for j in range(n_mutations):
                    if b1 == b2:
                        difference_in_background_fitness[env, b1, b2, j] = np.nan
                    else:
                        difference_in_background_fitness[env, b1, b2, j] = np.abs(f_background[env, b1, j] - f_background[env, b2, j])

    for env in range(n_envs):
        plt.plot(difference_in_background_fitness[env].flatten(), difference_in_fitness_effects[env].flatten(), '.', color=COLORS_ENV[env], label=f'{environments[env]}', markersize=1.5)
        linear_fit(flatten_and_clean_nans(difference_in_background_fitness[env]), flatten_and_clean_nans(difference_in_fitness_effects[env]), COLORS_ENV[env], alpha=0.05)


    plt.xlim([0, 1.4])
    plt.ylim([-0.05, 0.85])

    plt.xticks(np.arange(0., 1.4, 0.25))
    plt.yticks(np.arange(0., 0.85, 0.2))

    plt.xlabel('difference in background fitness', fontsize=12)
    plt.ylabel('difference in fitness effects', fontsize=12)

    ax = plt.gca()

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height*0.1, box.width * 0.75, box.height * 1])

    leg = plt.legend(title='Environment', bbox_to_anchor=(1.05, 0.5), loc='center left', frameon=False, markerscale=5/1.5)
    leg._legend_box.align = 'left'
    plt.setp(leg.get_title(), fontsize=12)

    error_data = np.loadtxt('generated_data/difference_in_fitness_effects_difference_in_background_fitness_correlation.dat', usecols=(1,3))
    for env in range(n_envs):
        plt.text(0.1, 0.9-env*0.05, f'R = {error_data[env, 0]:.3f}, p {format_p_value(error_data[env, 1])}', color=COLORS_ENV[env], transform=ax.transAxes)

    print('Figures:')
    plt.savefig('figs/fig_8A.pdf')
    print('\tfigs/fig_8A.pdf')
    plt.savefig('figs/fig_8A.png', dpi=1200)
    print('\tfigs/fig_8A.png')

    plt.close('all')


if recalculate:
    r_samples = np.zeros((n_samples, n_envs))
    for s in range(n_samples):
        f_background_s = f_background + np.random.normal(np.zeros(fitness_effects.shape), f_background_errors)
        difference_in_background_fitness = np.zeros((n_envs, n_backgrounds, n_backgrounds, n_mutations))
        for env in range(n_envs):
            for b1 in range(n_backgrounds):
                for b2 in range(n_backgrounds):
                    for j in range(n_mutations):
                        if b1 == b2:
                            difference_in_background_fitness[env, b1, b2, j] = np.nan
                        else:
                            difference_in_background_fitness[env, b1, b2, j] = np.abs(f_background_s[env, b1, j] - f_background_s[env, b2, j])


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
            r_samples[s, env] = pearson_correlation_coefficient(difference_in_background_fitness[env], difference_in_fitness_effects[env])

    with open('generated_data/difference_in_fitness_effects_difference_in_background_fitness_correlation.dat', 'w') as f:
        f.write('#environment\tcorrelation\tcorrelation_std\tpvalue\n')
        for env in range(n_envs):
            pvalue = p_value(np.mean(r_samples[:, env]), 0., np.std(r_samples[:, env]))
            f.write(f'{environments[env]}\t{np.mean(r_samples[:, env])}\t{np.std(r_samples[:, env])}\t{pvalue}\n')

    print('Data:')
    print('\tgenerated_data/difference_in_fitness_effects_difference_in_background_fitness_correlation.dat')
