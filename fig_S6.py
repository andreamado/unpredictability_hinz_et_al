from common import *
from fitness_effects import *

fig, ax = plt.subplots(3, 2, figsize=(10, 10))

idx = 0
for env1 in range(n_envs):
    for env2 in range(n_envs):
        if env1 > env2:
            cax = ax[idx//2, idx%2]
            for i in range(n_mutations):
                fe1 = flatten_and_clean_nans(fitness_effects[env1, :, i])
                fe2 = flatten_and_clean_nans(fitness_effects[env2, :, i])

                cax.plot(fe1, fe2, '.', label=f'{mutations[i]}', color=COLORS[i])
                linear_fit(fe1, fe2, COLORS[i], ax=cax)

            cax.set_aspect('equal')

            cax.set_xlim([0.35, 1.4])
            cax.set_ylim([0.35, 1.4])

            cax.set_xticks(np.arange(0.25, 1.45, 0.25))
            cax.set_yticks(np.arange(0.25, 1.45, 0.25))

            cax.set_xlabel(f'{environments[env1]}', fontsize=12)
            cax.set_ylabel(f'{environments[env2]}', fontsize=12)

            idx += 1

plt.legend(title='Mutation', frameon=False, bbox_to_anchor=(1.05, 0.5), loc='center left')

plt.tight_layout()

plt.savefig(f'figs/fig_S6.pdf')
plt.savefig(f'figs/fig_S6.png', dpi=1200)
plt.close('all')

print('Figures:')
print('\tfigs/fig_S6.pdf')
print('\tfigs/fig_S6.png')
