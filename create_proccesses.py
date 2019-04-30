#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:06:43 2019
function will create as much proccess as you pass through param with one condition
proccess must be less than number of cpu
@author: msaif
"""
import multiprocessing as mp
num_workers= mp.cpu_count()

def distribute_processes_over_cpu(target,param):
    """
    finction'sparameters:
    target : the function the you want to call at the same time
    param: a pair of index,values where index(int)=0-~number of cpu_count
    and values are the targeted function parameters
    for exampel  param={0:*args0,1:*args1}
    0,1 are the process index
    *args0,*args1 are the parmaters in an iterable object(tuple for example)
    """
    if not isinstance(param,dict):
        return 'parameters must be a dict of index and (*args)'
    if len(param)>num_workers:
        return "You only have {} CPU".format(num_workers)
    processes=[None]*len(param)
    for index,args in param.items():
        processes[index]=mp.Process(target=target,args=(*args,))
        process.start()
    for process in processes:
        process.join()
