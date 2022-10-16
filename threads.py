# threads.py
# Contains all the thread classes


# Imports
from __future__ import annotations

from datetime import datetime
from threading import Thread
from time import sleep
from typing import Any

from PIL.PngImagePlugin import PngImageFile
from PIL.PyAccess import PyAccess

import image
from global_methods import all_equal, all_same_type, isntinstance
from ip import IP, ComplexIPrange, IPrange
from ping import ping


# Definitions   
class ThreadWrap(Thread):
    """A wrapper for a thread to manage it better"""

    # Variables
    thrd = Thread
    is_end = False


    # Init
    def __init__(self, name: str = None) -> None:
        if name != None:
            super().__init__(target=self.main, name=name)
        else:
            super().__init__(target=self.main)


    def end(self) -> None:
        """End the thread"""

        self.is_end = True


    # Dummy main method
    def main(self) -> None:
        """
        Define the code to be executed.
        This must be defined in the child class or an exception will be raised

        For a loop put a is_end break statement
        
        Usage:
        >>> class ChildThread(ThreadWrap):
        ...     def main(self):
        ...         # Some code
        
        For a loop:
        ...         while True:
        ...             # Some code
        ...             if self.is_end:
        ...                 break
        """

        raise NotImplementedError("This method should never be called. Define it in child class instead.")


class PingThread(ThreadWrap):
    """Creates a thread that will ping ip addresses"""

    # Variables
    check_range = IPrange # The range of ips to check
    results = []          # The results of the pings
    total_pinged = 0      # The total amount of ips pinged this thread
    is_finished = False   # If the thread finished its range of IPs


    # Methods
    def __init__(self, ip_range: IPrange | ComplexIPrange, name_num: int) -> None:
        # Check if ip range is in fact, an ip range
        if isntinstance(ip_range, (IPrange, ComplexIPrange)):
            raise TypeError(f"ip range must be of type IPrange or ComplexIPrange, not {ip_range.__class__.__name__}")
        
        super().__init__(f"PingThread-{name_num}")
        self.check_range = ip_range
    

    # Thread methods
    def join(self) -> tuple[list[tuple[IP, bool]], IPrange]:
        super().join()
        checked_range = IPrange(self.check_range[0], self.end_ip, no_stop_sub_1=True)
        return self.results, checked_range
    
    
    # Function to be executed
    def main(self) -> None:        
        # Ping loop
        results = []
        for ip in self.check_range:
            # Ping ip and append result
            results.append((ip, bool(ping(ip))))
            self.total_pinged += 1
            
            # Break when thread end
            if self.is_end:
                self.end_ip = ip
                break
        
        self.is_finished = True
        self.results = results


class LoadThread(ThreadWrap):
    """Creates a thread that loads images"""

    # Variables
    imgs = []
    pix_maps = []
    loaded_num = 0

    # Init
    def __init__(self, imgs: list[PngImageFile], name_num: int) -> None:
        super().__init__(f"LoadThread-{name_num}")
        self.imgs = imgs
    

    # Thread methods
    def join(self) -> list[PyAccess]:
        super().join()
        return self.pix_maps


    # Function to be executed
    def main(self) -> None:
        pix_maps = []
        for img in self.imgs:
            pix_maps.append(img.load())
            self.loaded_num += 1

            if self.is_end:
                break
        
        self.pix_maps = pix_maps
        

class ResultsThread(ThreadWrap):
    """Creates a thread that saves results to an image reference"""

    # Variables
    results = []
    img_refs = []


    # Init
    def __init__(self, results: list[tuple[IP, bool]], img_refs: list[PyAccess], name_num: int) -> None:
        super().__init__(f"ResultsThread-{name_num}")
        self.results = results
        self.img_refs = img_refs
    

    # Function to be executed
    def main(self) -> None:
        for result in self.results:
            image.write_pix(self.img_refs, result)

            if self.is_end:
                break


class SaveThread(ThreadWrap):
    """Creates a thread that saves pixel maps to their designated images"""

    # Variables
    imgs_n_out_nums = []
    saved_num = 0


    # Init
    def __init__(self, imgs_n_out_nums: list[tuple[PngImageFile, int]], name_num: int) -> None:
        super().__init__(f"SaveThread-{name_num}")
        self.imgs_n_out_nums = imgs_n_out_nums
    

    # Function to be executed
    def main(self) -> None:
        for img, out_num in self.imgs_n_out_nums:
            image.save(img, out_num)
            self.saved_num += 1

            if self.is_end:
                break


class StatsThread(ThreadWrap):
    """Creates a thread that prints the current stats"""

    # Variables
    thrds = []


    # Init
    def __init__(self, thrds: ThreadsList[PingThread] | ThreadsList[LoadThread] | ThreadsList[SaveThread]) -> None:
        if not all_same_type(thrds):
            raise TypeError("Threads must all be same type")
        
        super().__init__(f"StatsThread-{thrds[0].__class__.__name__}")
        self.thrds = thrds
        self.thrd_cls = thrds[0].__class__
    
    
    # Function to be executed
    def main(self) -> None:
        if self.thrd_cls == PingThread:
            # Ping stats

            # Set starting time
            start = datetime.now()
            start = start.replace(microsecond=0)

            finished = False

            # Stats loop
            while not self.is_end:
                # Get stats values
                total = sum(thrd.total_pinged for thrd in self.thrds)

                # Get elapsed time
                now = datetime.now()
                now = now.replace(microsecond=0)
                time_elapsed = now - start

                # Print these values
                print(f"Pinged {total} ips in {time_elapsed}; ", end='')
                if finished:
                    print("A thread has finished!; ", end='')
                try:
                    print(f"{int(total // time_elapsed.total_seconds())} ips/sec; ", end='')
                except ZeroDivisionError:
                    print("0 ips/sec; ", end='')
                try:
                    print(f"{int(total // (time_elapsed.total_seconds() / 60))} ips/min; ", end='')
                except ZeroDivisionError:
                    print("0 ips/min; ", end='')
                try:
                    print(f"{int(total // (time_elapsed.total_seconds() / 3600))} ips/hour; ", end='\r')
                except ZeroDivisionError:
                    print("0 ips/hour; ", end='\r')

                # Delay
                sleep(0.2)
            
        elif self.thrd_cls == LoadThread:
            # Loading stats

            # Set starting time
            start = datetime.now()
            start = start.replace(microsecond=0)

            # Stats loop
            while not self.is_end:
                # Get stats values
                total = sum(thrd.loaded_num for thrd in self.thrds)

                # Get elapsed time
                now = datetime.now()
                now = now.replace(microsecond=0)
                time_elapsed = now - start

                # Print these values
                print(f"Loaded {total}/64 images; {time_elapsed} elapsed", end='\r')

                # Delay
                sleep(0.2)
            
            # Get elapsed time
            now = datetime.now()
            now = now.replace(microsecond=0)
            time_elapsed = now - start

            # Print these values
            print(f"Loaded 64/64 images; {time_elapsed} elapsed")
        
        elif self.thrd_cls == SaveThread:
            # Loading stats

            # Set starting time
            start = datetime.now()
            start = start.replace(microsecond=0)

            # Stats loop
            while not self.is_end:
                # Get stats values
                total = sum(thrd.saved_num for thrd in self.thrds)

                # Get elapsed time
                now = datetime.now()
                now = now.replace(microsecond=0)
                time_elapsed = now - start

                # Print these values
                print(f"Saved {total}/64 images; {time_elapsed} elapsed", end='\r')

                # Delay
                sleep(0.2)
            
            # Get elapsed time
            now = datetime.now()
            now = now.replace(microsecond=0)
            time_elapsed = now - start

            # Print these values
            print(f"Saved 64/64 images; {time_elapsed} elapsed")


class ThreadsList(list):
    """Special immutable list of threads that can act on itself easily"""

    # List methods
    def __init__(self, thrds: list[Thread] | list[ThreadWrap]):
        # Make sure every thrd is a thread
        for thrd in thrds:
            if isntinstance(thrd, Thread):
                raise TypeError(f"Only threads can be added to threads list, not {thrd.__class__.__name__}")

        # All types must be the same
        if not all_same_type(thrds):
            raise TypeError(f"Threads must all be the same type")
        
        # The thread class
        self.thrd_cls = thrds[0].__class__

        # Initialize list
        super().__init__(thrds)
    

    # Thread methods
    def start(self) -> None:
        """Start threads"""

        thrd: Thread | ThreadWrap

        for thrd in super().__iter__():
            thrd.start()
    

    def end(self) -> None:
        """End threads"""

        thrd: Thread | ThreadWrap

        # End threads if they have end attribute
        if hasattr(self.thrd_cls, "end"):
            for thrd in super().__iter__():
                thrd.end()
        
        else:
            raise AttributeError("Thread does not have end attribute")
    
    def join(self) -> list[Any]:
        """Join threads"""
        
        return [thrd.join() for thrd in super().__iter__()]