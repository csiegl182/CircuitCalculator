import numpy as np
from matplotlib.patches import Polygon
from matplotlib.axes import Axes

def get_aspect(ax: Axes) -> float:
    figW, figH = ax.get_figure().get_size_inches()
    _, _, w, h = ax.get_position().bounds
    disp_ratio = (figH * h) / (figW * w)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    data_ratio = (ylim[1]-ylim[0]) / (xlim[1]-xlim[0])
    return disp_ratio / data_ratio

def arrow_head(ax: Axes, xy0, height, width, angle, color='black', **kwargs):
    def A(phi: float) -> np.matrix:
        xy_ratio = get_aspect(ax)
        return np.matrix([[np.cos(phi), -np.sin(phi)*xy_ratio], [np.sin(phi)/xy_ratio, np.cos(phi)]])
    def triangular_shape(abs_height: float, abs_width: float) -> np.matrix:
        return np.matrix([np.array([-abs_height, 0, -abs_height]),
                          np.array([abs_width/2, 0, -abs_width/2])])
    def offset(x: float, y: float) -> np.matrix:
        return np.matrix([[x], [y]])
    def create_patch(polygon, color, **kwargs):
        if 'linewidth' in kwargs.keys():
            kwargs.pop('linewidth')
        return Polygon(polygon.T, color=color, linewidth=0, zorder=100, **kwargs)
    triangular = A(angle)*triangular_shape(width, height)+offset(xy0[0], xy0[1])
    patch = create_patch(triangular, color, **kwargs)
    ax.add_patch(patch)

def arrow(ax: Axes, xy0, xy1, height, width, tail=False, color='black', **kwargs) -> None:
    dx = xy1[0]-xy0[0]
    dy = xy1[1]-xy0[1]
    alpha_r = np.arctan2(dy*get_aspect(ax), dx)
    alpha = np.arctan2(dy, dx)
    arrow_head(
        ax=ax,
        xy0=xy1,
        height=height,
        width=width,
        angle=alpha_r,
        color=color,
        **kwargs)
    if tail:
        arrow_head(
            ax=ax,
            xy0=xy0,
            height=height,
            width=width,
            angle=alpha-np.pi,
            color=color,
            **kwargs)
    if get_aspect(ax) > 1:
        aspect = get_aspect(ax)
    else:
        aspect = 1
    if tail:
        xy0[0]+=height*np.cos(alpha)/aspect
        xy0[1]+=height*np.sin(alpha)/aspect
    xy1[0]-=height*np.cos(alpha)/aspect
    xy1[1]-=height*np.sin(alpha)/aspect
    ax.plot([xy0[0], xy1[0]], [xy0[1], xy1[1]], color=color, **kwargs)

def complex_pointer(ax: Axes, z0, z1, width=0.05, height=0.05, **kwargs) -> None:
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    delta_x, delta_y = xlim[1]-xlim[0], ylim[1]-ylim[0]
    max_stretch = max(delta_x, delta_y)
    width *= max_stretch
    height *= max_stretch
    if z0 != z1:
        arrow(ax, [np.real(z0), np.imag(z0)], [np.real(z1), np.imag(z1)], width, height, **kwargs)
