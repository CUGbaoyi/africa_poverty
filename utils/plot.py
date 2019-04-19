import matplotlib.pyplot as plt
import numpy as np


def heatmap(mat, xlabels, ylabels, title=None, format_spec='{:.1f}'):
    '''Creates a heatmap plot of the given matrix.

    Args
    - mat: np.array, shape [m, n]
    - xlabels: list of str, length n
    - ylabels: list of str, length m
    - title: str, optional
    - format_spec: str, format specification
    '''
    m, n = mat.shape
    assert len(xlabels) == n
    assert len(ylabels) == m

    fig, ax = plt.subplots(1, 1, figsize=[n*0.7 + 0.5, m*0.7])
    im = ax.imshow(mat, cmap='viridis')
    fig.colorbar(im, ax=ax)

    # show all ticks
    ax.set_xticks(range(n))
    ax.set_yticks(range(m))

    # label them with the respective list entries
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)

    # rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right',
             rotation_mode='anchor')

    # loop over data dimensions and create text annotations
    for i in range(m):
        for j in range(n):
            ax.text(j, i, format_spec.format(mat[i, j]),
                    ha='center', va='center', color='w')

    if title is not None:
        ax.set_title(title)
    fig.tight_layout()
    plt.show()


def symmetric_heatmap(mat, labels, title=None, format_spec='{:.1f}',
                      figsize=None):
    '''Creates a symmetric heatmap plot of the given matrix.

    Args
    - mat: np.array, shape [n, n]
    - labels: list of str, length n
    - title: str, optional
    - format_spec: str, format specification
    - figsize: list [width, height]
        - if None, defaults to [n*0.7 + 0.5, n*0.7]
    '''
    heatmap(
        mat=mat,
        xlabels=labels,
        ylabels=labels,
        title=title,
        format_spec=format_spec,
        figsize=figsize)


def boxplot_df(df, y, by, figsize, ylabel, title, colors):
    '''Creates a box-and-whisker plot from a DataFrame.

    Args
    - df: pd.DataFrame, contains columns from `y` and `by`
    - y: str, name of a column in `df` for the y-axis
    - by: str or list of str, names of columns in `df` to group by
    - figsize: list [width, height], in inches
    - ylabel: str
    - title: str
    - colors: list of matplotlib colors, one per group after grouping by `by`
    '''
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    bplot = df.boxplot(y, by=by, ax=ax, grid=False, patch_artist=True,
                            return_type='dict', widths=0.8)
    for i, patch in enumerate(bplot[y]['boxes']):
        patch.set_facecolor(colors[i])
    ax.grid(True, axis='y')
    plt.setp(ax.get_xticklabels(), rotation=60, ha='right',
             rotation_mode='anchor')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.suptitle('')
    fig.tight_layout()
    plt.show()


def plot_image_by_band(img, band_order, nrows, title, rgb=None, colorbar=False):
    '''
    Args
    - img: np.array, shape [H, W, C], type float, normalized
    - band_order: list of str, names of the bands in order
    - nrows: int, desired number of rows in the created figure
    - title: str, or None
    - rgb: one of [None, 'merge', 'add']
        - None: do not create a separate RGB image
        - 'merge': plot the RGB bands as a merged image
        - 'add': plot all bands, but also add a merged RGB image
    - colorbar: bool, whether to show colorbar
    '''
    nbands = img.shape[2]
    rgb_to_naxs = {
        None: nbands,
        'merge': nbands - 2,
        'add': nbands + 1
    }
    nplots = rgb_to_naxs[rgb]
    ncols = int(np.ceil(nplots / float(nrows)))
    fig_w = min(15, 3*ncols)
    fig_h = min(15, 3*nrows)
    fig, axs = plt.subplots(nrows, ncols, sharex=True, sharey=True,
                            figsize=[fig_w, fig_h], constrained_layout=True)
    if title is not None:
        fig.suptitle(title, y=1.03)

    # scale image to [0,1]: 0 = -3 std, 0.5 = mean, 1 = +3 std
    scaled_img = np.clip(img / 6.0 + 0.5, a_min=0, a_max=1)
    bands = {band_name: scaled_img[:, :, b] for b, band_name in enumerate(band_order)}

    plots = []
    plot_titles = []
    if rgb is not None:
        r, g, b = bands['RED'], bands['GREEN'], bands['BLUE']
        rgb_img = np.stack([r,g,b], axis=2)
        plots.append(rgb_img)
        plot_titles.append('RGB')

    if rgb == 'merge':
        for band_name in band_order:
            if band_name not in ['RED', 'GREEN', 'BLUE']:
                plots.append(bands[band_name])
                plot_titles.append(band_name)
    else:
        plots += [bands[band_name] for band_name in band_order]
        plot_titles += band_order

    for b in range(len(plots)):
        if len(axs.shape) == 1:
            ax = axs[b]
        else:
            ax = axs[b // ncols, b % ncols]
        # set origin='lower' to match lat/lon direction
        im = ax.imshow(plots[b], origin='lower', cmap='viridis', vmin=0, vmax=1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(plot_titles[b])

    if colorbar:
        fig.colorbar(im, orientation='vertical', ax=axs)
    plt.show()