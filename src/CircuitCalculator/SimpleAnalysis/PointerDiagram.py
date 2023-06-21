from .layout import pointer_diagram_plot
from ..Circuit import solution as solutions
from dataclasses import dataclass
from .plot_elements import complex_pointer
import functools

def plot_voltage_pointer(id: str, origin:str='', pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),  **kwargs):
    @pointer_diagram_plot(ax_lim=pd_lim, xlabel='Re{V}→', ylabel='Im{V}→')
    def plot_pointer(fig, ax, solution:solutions.CircuitSolution=solutions.NoSolution()):
        kwargs.update({'label':f'V({id})'})
        z0 = 0 if origin == '' else complex(solution.get_voltage(origin))
        z1 = complex(solution.get_voltage(id))
        complex_pointer(ax, z0, z0+z1, **kwargs)
        return fig, ax
    return plot_pointer

def plot_current_pointer(id:str, origin:str='', pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),  **kwargs):
    @pointer_diagram_plot(ax_lim=pd_lim, xlabel='Re{I}→', ylabel='Im{I}→')
    def plot_pointer(fig, ax, solution:solutions.CircuitSolution=solutions.NoSolution()):
        kwargs.update({'label':f'I({id})'})
        z0 = 0 if origin == '' else complex(solution.get_current(origin))
        z1 = complex(solution.get_current(id))
        complex_pointer(ax, z0, z0+z1, **kwargs)
        return fig, ax
    return plot_pointer

def plot_power_pointer(id:str, origin:str='', pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),  **kwargs):
    @pointer_diagram_plot(ax_lim=pd_lim, xlabel='P→', ylabel='Q→')
    def plot_pointer(fig, ax, solution:solutions.CircuitSolution=solutions.NoSolution()):
        kwargs.update({'label':f'S({id})'})
        z0 = 0 if origin == '' else complex(solution.get_power(origin))
        z1 = complex(solution.get_power(id))
        complex_pointer(ax, z0, z0+z1, **kwargs)
        return fig, ax
    return plot_pointer

def pointer_diagram_analysis(circuit, w, fig_fcn, *args):
    solution = solutions.ComplexSolution(circuit=circuit, w=w)
    new_args = tuple(functools.partial(a, solution=solution) for a in args)
    return fig_fcn(*new_args)