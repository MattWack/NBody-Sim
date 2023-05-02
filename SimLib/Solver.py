# -*- coding: utf-8 -*-
"""
The Solver base class and its children
This set of classes implements various differential equation solving 
algorithms.  They are intended for use with the classes derived from Physics.
"""

class Solver():
    """Differential equation solver base class.
    
    Attributes
    ----------
    physics : Physics 
        A reference to a physics class for access to a differential equation
    
    """
    
    def __init__(self,physics=None):
        self.physics = physics
                        
    def advance(self,f,x,dx):
        ''' Advance a differential equation one step
        
        This advance implementation in the Solver base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Solver should define their own versions of 
        advance following the same interface.
        
        Parameters
        ----------
        x : float
            The independent variable

        f : float
            The dependent variable(s)
                        
        dx : float
            The distance to advance the independent variable. 
            (ie. the stepsize)
            
        Returns
        -------
        xnext : float
            The value of the independent variable at the next step

        fnext : float
            The value of the dependent variable at the next step            
        '''
        print("Solver.advance is a stub!  This line should never be executed")
        return          # Do nothing, simply return.
                

class Euler(Solver):
    """Euler's technique for differential equation solving    
    """
            
    def advance(self, x, f, dx, diff_eq):
        """
        Advances a given function to it's next value given it's diff_eq and time step.

        Parameters
        ----------
        x : flaot
            The independant variable.
        f : float
            The current value of the function.
        dx : float
            The time step.
        diff_eq : method
            The diff_eq to pass in current x and f.

        Returns
        -------
        dnext : flaot
            The independant variable value at next function value.
        fnext : float
            The advanced function value.

        """
        
        
        dnext = x + dx
        fnext = f + diff_eq(x,f)*dx
        return dnext, fnext


class RK2(Solver):
    """RK2 technique for differential equation solving    
    """
    
    def advance(self, x, f, dx, diff_eq):
        """
        Advances a given function to it's next value given its diff_eq and time step.

        Parameters
        ----------
        x : flaot
            The independant variable.
        f : float
            The current value of the function.
        dx : float
            The time step.
        diff_eq : method
            The diff_eq to pass in current x and f.

        Returns
        -------
        dnext : flaot
            The independant variable value at next function value.
        fnext : float
            The advanced function value.

        """
        k1 = diff_eq(x,f)
        k2 = diff_eq(x + 1/2*dx, f + 1/2*k1*dx)
        fnext = f + k2 * dx 
        return x + dx, fnext

class RK4(Solver):
    """RK4 technique for differential equation solving    
    """
    def advance(self, x, f, dx, diff_eq):
        """
        Advances a given function to it's next value given its diff_eq and time step.

        Parameters
        ----------
        x : flaot
            The independant variable.
        f : float
            The current value of the function.
        dx : float
            The time step.
        diff_eq : method
            The diff_eq to pass in current x and f.

        Returns
        -------
        dnext : flaot
            The independant variable value at next function value.
        fnext : float
            The advanced function value.

        """
        k1 = diff_eq(x,f)
        k2 = diff_eq(x + dx/2, f + dx*k1/2)
        k3 = diff_eq(x + dx/2, f + dx*k2/2)
        k4 = diff_eq(x + dx, f + dx*k3)
        fnext = f + dx*(1/6*k1+1/3*k2+1/3*k3+1/6*k4)

        return x + dx, fnext