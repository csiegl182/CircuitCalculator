
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from functools import partial
from CircuitCalculator.Display.ScientificFloat import scientific_float
from CircuitCalculator.Network.EquivalentSources import NortenEquivalentSource, TheveninEquivalentSource

def plot_equivalent_source_diagram(x0: float, y0: float, xlabel: str, ylabel: str, m2: float = 0, title: str = '', x0label: str = '', y0label: str = '') -> tuple[Figure, Axes]:
    fig, ax = plt.subplots()
    ax.plot([0, x0], [y0, 0], linewidth=2)
    ax.grid(visible=True)
    ax.set_xlim(left=0, right=ax.get_xticks()[-1])
    ax.set_ylim(bottom=0, top=ax.get_yticks()[-1])
    ax.set_xlabel(f'${xlabel} \\rightarrow$')
    ax.set_ylabel(f'${ylabel} \\rightarrow$')
    ax.set_title(title)
    
    xticks = ax.get_xticks()
    xticks = np.sort(np.append(xticks, x0))
    ax.set_xticks(xticks)
    
    yticks = ax.get_yticks()
    yticks = np.sort(np.append(yticks, y0))
    ax.set_yticks(yticks)

    axes_text = partial(ax.text, rotation_mode='anchor', ha='left', va='center', backgroundcolor='white')
    axes_text(
        x=x0,
        s=x0label,
        y=1/2*np.diff(ax.get_yticks()[:2])[0],
        rotation='vertical'
    )
    axes_text(
        x=1/2*np.diff(ax.get_xticks()[:2])[0],
        y=y0,
        s=y0label
    )

    if m2 > 0:
        xmax = ax.get_xlim()[-1]
        ax.plot([0, xmax], [0, m2*xmax], color='red')
        x_load = y0/(y0/x0+m2)
        y_load = m2*x_load
        ax.plot(x_load, y_load, marker='o', color='red')

    fig.show()
    return fig, ax

def plot_thevenin_source(source: TheveninEquivalentSource, xlabel: str = 'I', ylabel: str = 'U', title: str = 'Thevenin Equivalent Source', R_load: float = 0) -> tuple[Figure, Axes]:
    UL = np.real(source.U)
    Ri = np.real(source.Z)
    IK = UL/Ri
    sf = partial(scientific_float, exp_prefixes={3: 'k', -3: 'm', -6: 'u'})
    fig, ax = plot_equivalent_source_diagram(
        x0=IK,
        y0=UL,
        xlabel=xlabel,
        ylabel=ylabel,
        m2=R_load,
        title=title,
        x0label='$I_\\mathrm{K}='+sf(IK)+'\\mathrm{A}$',
        y0label='$U_\\mathrm{L}='+sf(UL)+'\\mathrm{V}$'
    )
    fig.show()
    return fig, ax

def plot_norten_source(source: NortenEquivalentSource, xlabel: str = 'U', ylabel: str = 'I', title: str = 'Norten Equivalent Source', R_load: float = 0) -> tuple[Figure, Axes]:
    IK = np.real(source.I)
    Ri = 1/np.real(source.Y)
    UL = Ri*IK
    sf = partial(scientific_float, exp_prefixes={3: 'k', -3: 'm', -6: 'u'})
    fig, ax = plot_equivalent_source_diagram(
        x0=UL,
        y0=IK,
        xlabel=xlabel,
        ylabel=ylabel,
        m2=1/R_load,
        title=title,
        x0label='$U_\\mathrm{L}='+sf(UL)+'\\mathrm{V}$',
        y0label='$I_\\mathrm{K}='+sf(IK)+'\\mathrm{A}$'
    )
    fig.show()
    return fig, ax