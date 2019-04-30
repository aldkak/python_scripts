# create as many threads as you want
#handling Exception in threads
#stop threads
#get a return value from  thread based  on it's index

import threading
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,*args, **kwargs):
        super(StoppableThread, self).__init__(*args,**kwargs)
        self._stop_event = threading.Event()
        self.shutdown_flag = threading.Event()


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Thread_Exception(Exception):
    pass




def handling_Exception_in_thread(shared_object, *args, **kwargs):
    try:
        shared_object['target'](*args, **kwargs)
    except Exception as err:
        shared_object['errors'] = err
    except KeyboardInterrupt as krr:
        shared_object['errors'] = krr




def create_threads(target,parameters,return_flag=False):
    """
    parameters must be a dict {threads index type int start with 0:(threads args,) type tuple,..}
    threads args must be inside  tuple with a , at the end
    to get a return value you must add two parameter to your function dict and index
    index=thread index , and dict return value of a thread index

    def your_func(*args,response=None,index=None):
        response[index]=...
        return response
    """
    if not isinstance(parameters,dict):
        return 'parameters must be a dict {threads index:threads args,..}'
    try:
        shared_obj = {'errors':'', 'target': target}
        threads=[None]*len(parameters)
        if return_flag:
            response={}
            for index,args in parameters.items():
                threads[index] = StoppableThread(target =handling_Exception_in_thread,args=(shared_obj,*args,response,index))
                threads[index].start()
        else:
            for index,args in parameters.items():
                threads[index] = StoppableThread(target =handling_Exception_in_thread,args=(shared_obj,args))
                threads[index].start()

        for thread in threads:
            thread.join()


        if shared_obj['errors']:
            for thread in threads:
                thread.stop()
            raise Thread_Exception(shared_obj['errors'])
        if return_flag:
            return response
    except KeyboardInterrupt as e:
        for thread in threads:
                thread.stop()
        shared_obj['errors'] = e
        raise Thread_Exception(shared_obj['errors'])
