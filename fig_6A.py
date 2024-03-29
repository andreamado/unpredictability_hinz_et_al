import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

data_labels = ['Mean', 'Variance', 'Gamma']
environments = ['_LB', '_M9-Glucose', '_Urine', '_Colon', '']
colormaps = ['Blues', 'Greens', 'Oranges']

# '_gaussian' or '_bootstrap'
app_data = '_gaussian'

mpl.rcParams['axes.linewidth'] = 0.1
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.labelsize'] = 8.
mpl.rcParams['xtick.labelsize'] = 8.


fig, axs = plt.subplots(nrows=5, ncols=4,
                        sharex=True, sharey=True,
                        figsize = mpl.figure.figaspect(5.5/4.5),
                        gridspec_kw = dict( wspace=0.05, hspace=0.05,
                                            left=0.20, right=0.95, top=0.95, bottom=0.15
                                    ),
                        subplot_kw  = dict( aspect='equal',
                                            xticks=[0.1, 0.2],
                                            yticks=[0, 0.1, 0.2],
                                            xlim=[0,0.24],
                                            ylim=[0,0.24]
                                    )
                        )


axs[0,0].set_ylabel('')

environment = ''
app = f'_1000000_model_samples_50bins{app_data}{environment}'

sa = np.load(f'model_fit_data/likelihood_sigmaa{app}.dat.npy')
sb = np.load(f'model_fit_data/likelihood_sigmab{app}.dat.npy')

delta = sb[1] - sb[0]
sa_size = int((sa.max() - sa.min())/delta) + 1
sb_size = int(len(sa)/sa_size)

new_shape = (sa_size, sb_size)

sa = sa.reshape(new_shape)
sb = sb.reshape(new_shape)

axs[0, 3].set_title('All', size=9)
axs[4, 0].set_ylabel('All', size=9)

fig.text(0.55, 0.02, r'$\sigma_a$ (standard deviation of additive component)', ha='center', size=10)
fig.text(0.01, 0.5, r'$\sigma_b$ (standard deviation of epistatic component)', va='center', size=10, rotation='vertical')

xx = np.arange(0,0.25,0.01)

for i, environment in enumerate(environments):
    app = f'_1000000_model_samples_50bins{app_data}{environment}'

    total_likelihood = np.zeros(new_shape)

    if len(environment):
        m = np.load('model_fit_data/mean_gaussian.dat.npy')
        m2 = np.mean(m)**2
        vm = (np.mean(m[:, i]) - np.mean(m))**2
        vv = np.mean(np.load('model_fit_data/variance_gaussian.dat.npy')[:, i])
        gg = np.mean(np.load('model_fit_data/gamma_gaussian.dat.npy')[:, i])

    for j, label in enumerate(data_labels):
        if i == 0:
            axs[0, j].set_title(label, size=9)

        if j == 0 and i < 4:
            axs[i, 0].set_ylabel(environment[1:], size=9)

        data = np.load(f'model_fit_data/likelihood_{label}{app}.dat.npy')

        with np.errstate(divide='ignore'):
            z = np.log(data).reshape(new_shape)
        z = z - z.max()

        argmax = np.argmax(z)

        total_likelihood += z

        p = axs[i, j].contourf(sa, sb, z, levels=np.arange(-100, 1, 20), cmap=colormaps[j])
        axs[i, 3].contour(sa, sb, z, levels=np.arange(-100, 1, 20), cmap=colormaps[j], linewidths=0.5)

        # plot the colorbars
        if i == 0 and j < 3:
            pos = axs[4, j].get_position()
            cax = plt.axes([pos.x0, 0.085, pos.width, 0.03])

            cb = fig.colorbar(p, cax=cax, orientation='horizontal')
            cb.set_ticks([-80, -40, 0])
            cb.ax.tick_params(labelsize=6)

    if len(environment):
        sa_estimate = np.sqrt(abs(gg*vv - (1-gg)*m2))
        sb_estimate = np.sqrt(abs((1-gg)*(m2+vv)/2))
        axs[i, 3].plot(sa_estimate, sb_estimate, color='red', marker='o', markersize=2)

    argmax = np.argmax(total_likelihood)

fig.text(0.05, 0.935, r'A', va='center', size=10, weight='bold')

plt.savefig('figs/fig_6A.pdf')
plt.savefig('figs/fig_6A.png', dpi=1200)

print('Figures:')
print('\tfigs/fig_6A.pdf')
print('\tfigs/fig_6A.png')
