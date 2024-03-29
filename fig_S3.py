from common import *
from fitness_effects import *

fig, ax = plt.subplots(4, 2, figsize=(10, 10))

idx = 0
for i in range(n_mutations):
    cax = ax[idx//2, idx%2]

    fe = fitness_effects[:, :, i]
    fe_errors = fitness_effects_errors[:, :, i]

    cax.set_title(mutations[i])

    cax.set_xticks(range(n_backgrounds))
    cax.set_yticks(range(n_envs))

    cax.set_xticklabels(backgrounds)
    cax.set_yticklabels(environments)
    plt.setp(cax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

    img = cax.imshow(fe, origin='upper', aspect='equal', vmin=0.35, vmax=1.4)

    print_values_all(fe, fe_errors, cax, value=True, test=1.)

    idx += 1

ax[3,1].set_aspect(aspect=6, anchor=(0.025,0))
fig.colorbar(img, cax=ax[3,1])

plt.tight_layout()

plt.savefig(f'figs/fig_S3.pdf')
plt.savefig(f'figs/fig_S3.png', dpi=1200)

print('Figures:')
print('\tfigs/fig_S3.pdf')
print('\tfigs/fig_S3.png')