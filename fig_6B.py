import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

nbins = 30

app = ''

environments = ['LB', 'M9-Glucose', 'Urine', 'Colon']
n_envs = len(environments)

colors = mpl.rcParams['axes.prop_cycle'].by_key()['color']

mpl.rcParams['axes.linewidth'] = 0.1
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.labelsize'] = 8.
mpl.rcParams['xtick.labelsize'] = 8.


fig, axs = plt.subplots(nrows=2, ncols=3,
                        figsize = mpl.figure.figaspect(2.5/3.5),
                        gridspec_kw = dict( wspace=0.2, hspace=0.2,
                                            left=0.13, right=0.95, top=0.95, bottom=0.1,
                                    )
                        )

maxima = [12064, 2181]

model = np.load('model_fit_data/model_1000000_model_samples_50bins.dat.npy')

for k, maximum in enumerate(maxima):
    #### Plot mean ############################################
    data = np.load(f'model_fit_data/mean_gaussian.dat.npy')

    axs[k, 0].set_xlim([-0.2, 0])

    model_statistics, model_range = model[['mean', f'range_mean']][maximum]
    axs[k, 0].fill_between(np.linspace(model_range[0], model_range[1], len(model_statistics)), model_statistics, color='lightgray')

    for i, env in enumerate(environments):
        axs[k, 0].axvline(np.mean(data.T[i]), color=colors[i])
        axs[k, 0].axvline(np.mean(data.T[i])+np.std(data.T[i]), color=colors[i], linestyle='--', linewidth=0.5)
        axs[k, 0].axvline(np.mean(data.T[i])-np.std(data.T[i]), color=colors[i], linestyle='--', linewidth=0.5)
    axs[k, 0].set_ylim(bottom=0)

    #### Plot variance ########################################
    data = np.load(f'model_fit_data/variance_gaussian.dat.npy')

    axs[k, 1].set_xlim([0, 0.075])
    model_statistics, model_range = model[['variance', f'range_variance']][maximum]
    axs[k, 1].fill_between(np.linspace(model_range[0], model_range[1], len(model_statistics)), model_statistics, color='lightgray')

    for i, env in enumerate(environments):
        axs[k, 1].axvline(np.mean(data.T[i]), color=colors[i])
        axs[k, 1].axvline(np.mean(data.T[i])+np.std(data.T[i]), color=colors[i], linestyle='--', linewidth=0.5)
        axs[k, 1].axvline(np.mean(data.T[i])-np.std(data.T[i]), color=colors[i], linestyle='--', linewidth=0.5)
    axs[k, 1].set_ylim(bottom=0)

    #### Plot gamma ###########################################
    data = np.load(f'model_fit_data/gamma_gaussian.dat.npy')

    axs[k, 2].set_xlim([0, 1])
    model_statistics, model_range = model[['gamma', f'range_gamma']][maximum]
    axs[k, 2].fill_between(np.linspace(model_range[0], model_range[1], len(model_statistics)), model_statistics, color='lightgray')

    for i, env in enumerate(environments):
        axs[k, 2].axvline(np.mean(data.T[i]), color=colors[i])
        axs[k, 2].axvline(np.mean(data.T[i])+np.std(data.T[i]), color=colors[i], linestyle='--', linewidth=0.5)
        axs[k, 2].axvline(np.mean(data.T[i])-np.std(data.T[i]), color=colors[i], linestyle='--', linewidth=0.5)
    axs[k, 2].set_ylim(bottom=0)

axs[0, 0].set_ylabel('Best fit to variance\n($\\sigma_a=0.180$, $\\sigma_b=0.008$)', size=8)
axs[1, 0].set_ylabel('Best fit to gamma\n($\\sigma_a=0.032$, $\\sigma_b=0.074$)', size=8)

axs[1, 0].set_xlabel(r'Mean of fitness effects', size=8)
axs[1, 1].set_xlabel(r'Variance of fitness effects', size=8)
axs[1, 2].set_xlabel(r'Epistasis, gamma', size=8)

fig.text(0.01, 0.5, r'Probability density', va='center', size=10, rotation='vertical')
fig.text(0.05, 0.935,  r'B', va='center', size=10, weight='bold')

plt.savefig(f'figs/fig_6B.pdf')
plt.savefig(f'figs/fig_6B.png', dpi=1200)

print('Figures:')
print('\tfigs/fig_6B.pdf')
print('\tfigs/fig_6B.png')
