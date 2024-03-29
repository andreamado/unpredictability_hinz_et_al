from common import *
from fitness_effects import *

################################################################################
##  Types of epistasis
UNDEFINED_EPISTASIS = 0
MAGNITUDE_EPISTASIS = 1
SIGN_EPISTASIS      = 2

def identify_epistasis_type(fe1, fe2):
    if np.isnan(fe1) or np.isnan(fe2):
        return UNDEFINED_EPISTASIS
    else:
        # if both fitness effects are greater or both are smaller than one the
        # epistasis is magnitude, otherwise is sign
        return MAGNITUDE_EPISTASIS if np.sign(fe1 - 1) == np.sign(fe2 - 1) else SIGN_EPISTASIS


epistasis_totals = np.zeros((n_envs, n_mutations, 3), dtype=float)
epistasis_partials = np.zeros((n_envs, n_mutations, n_backgrounds*(n_backgrounds-1)//2, 3), dtype=float)

for env in range(n_envs):
    idx_b = 0
    for b1 in range(n_backgrounds):
        for b2 in range(n_backgrounds):
            if b2 > b1:
                for i in range(n_mutations):
                    tp = identify_epistasis_type(fitness_effects[env, b1, i], fitness_effects[env, b2, i])
                    if tp is not UNDEFINED_EPISTASIS:
                        epistasis_partials[env, i, idx_b, tp] = np.abs(np.log(fitness_effects[env, b1, i]) - np.log(fitness_effects[env, b2, i]))
                        epistasis_totals[env, i, tp] += np.abs(np.log(fitness_effects[env, b1, i]) - np.log(fitness_effects[env, b2, i]))
                idx_b += 1

magnitude_epistasis = epistasis_totals[:, :, MAGNITUDE_EPISTASIS].sum(axis=1)
sign_epistasis      = epistasis_totals[:, :, SIGN_EPISTASIS].sum(axis=1)
total_epistasis     = magnitude_epistasis + sign_epistasis


if True:
    fig, ax = plt.subplots(1, 2, figsize=(14,6))

    cax = ax[0]
    cax.set_ylabel(r'Epistasis types (totals)', fontsize=12)

    m = cax.bar(range(n_envs), magnitude_epistasis, color=COLORS_BAR[1])
    s = cax.bar(range(n_envs), sign_epistasis,      color=COLORS_BAR[0], bottom=magnitude_epistasis)

    bottom, top = cax.get_ylim()
    cax.set_ylim(bottom=-0.05*(top-bottom), top=top)

    left_shift = 0.05
    box = cax.get_position()
    cax.set_position([box.x0-left_shift, box.y0, box.width, box.height * 1.05])

    cax.set_xticks(range(n_envs))
    cax.set_xticklabels(environments)


    cax = ax[1]
    cax.set_ylabel(r'Epistasis types (weighted fractions)', fontsize=12)

    m = cax.bar(range(n_envs), magnitude_epistasis/total_epistasis, color=COLORS_BAR[1])
    s = cax.bar(range(n_envs), sign_epistasis/total_epistasis,      color=COLORS_BAR[0], bottom=magnitude_epistasis/total_epistasis)

    bottom, top = cax.get_ylim()
    cax.set_ylim(bottom=-0.05*(top-bottom), top=top)

    box = cax.get_position()
    cax.set_position([box.x0-left_shift, box.y0, box.width, box.height * 1.05])

    cax.set_xticks(range(n_envs))
    cax.set_xticklabels(environments)

    leg = cax.legend(handles=[s, m], labels=['sign', 'magnitude'],title='Epistasis type', bbox_to_anchor=(1.05, 0.5), loc='center left', frameon=False)
    plt.setp(leg.get_title(), fontsize=12)
    leg._legend_box.align = 'left'

    plt.savefig(f'figs/fig_S4AB.pdf')
    plt.savefig(f'figs/fig_S4AB.png', dpi=1200)
    plt.close('all')

    print('Figures:')
    print('\tfigs/fig_S4AB.pdf')
    print('\tfigs/fig_S4AB.png')


if True:
    fig, ax = plt.subplots(2, 2, figsize=(14,12))

    for env in range(n_envs):
        d_magnitude = epistasis_partials[env, :, :, MAGNITUDE_EPISTASIS].flatten()
        d_sign = epistasis_partials[env, :, :, SIGN_EPISTASIS].flatten()

        d_magnitude = d_magnitude[d_magnitude>0.]
        d_sign = d_sign[d_sign>0.]

        cax = ax[env//2, env%2]

        if env > 1:
            cax.set_xlabel('Epistasis', fontsize=12)
        if env%2 == 0:
            cax.set_ylabel('Distribution', fontsize=12)

        mu_magnitude  = np.mean(d_magnitude)
        std_magnitude = np.std(d_magnitude)

        mu_sign  = np.mean(d_sign)
        std_sign = np.std(d_sign)

        left_shift = 0.05
        box = cax.get_position()
        cax.set_position([box.x0-left_shift, box.y0, box.width, box.height * 1.05])

        cax.set_xlim([0,1])
        cax.set_ylim([0,8])

        bins = np.arange(0, 1, 0.1)
        cax.set_title(environments[env])
        x, _, m = cax.hist([d_sign, d_magnitude], color=[COLORS_BAR[0], COLORS_BAR[1]], density=True, bins=bins, rwidth=0.95)

        if env == 3:
            leg = cax.legend(handles=m, labels=['sign', 'magnitude'],title='Epistasis type', bbox_to_anchor=(1.05, 0.5), loc='center left', frameon=False)
            plt.setp(leg.get_title(), fontsize=12)
            leg._legend_box.align = 'left'

    plt.savefig(f'figs/fig_S4C.pdf')
    plt.savefig(f'figs/fig_S4C.png', dpi=1200)
    plt.close('all')

    print('Figures:')
    print('\tfigs/fig_S4C.pdf')
    print('\tfigs/fig_S4C.png')
