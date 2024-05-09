#!/usr/bin/env python

import os, sys, string, argparse

class Stack():

    #def __repr__(self):
    #    return "Contents = " + str(self.show())
    #def __get__(self):
    #    print("get called")

    def len(self):
        return len(self._store)

    def __init__(self):
        self._store = []
        self.push(0)        # Create floor

    def push(self, item):
        try:
            self._store.append(item)
        except Exception as xxx:
            print ("Exc on push",  xxx)

    def pop(self):
        xlen = len(self._store)
        if xlen == 0:
            raise ValueError("Stack empty")
            return None

        item = self._store.pop(xlen - 1)
        return item

    def last(self):
        xlen = len(self._store)
        if xlen == 0: return None
        item = self._store[xlen - 1]
        return item

    def first(self):
        xlen = len(self._store)
        if xlen == 0: return None
        item = self._store[0]
        return item

    # This changed to no destructive get of current value
    def get(self):
        xlen = len(self._store)
        if xlen == 0: return None
        item = self._store[xlen-1]
        return item

    def stacklen(self):
        return len(self._store)

    def dump(self):
        cnt = 0; xlen = len(self._store)
        arr = []
        while cnt < xlen:
            arr.append(self._store[cnt]);
            cnt += 1
        return arr

    def show(self):
        cnt = len(self._store) - 1
        arr = []
        while cnt >= 0:
            arr.append(self._store[cnt])
            cnt -= 1
        return arr

# Start of program:

if __name__ == '__main__':

    stack = Stack()

    #print(stack)
    #print(dir(stack))

    stack.push(1)
    stack.push(3)
    print("dump", stack.dump())
    print("show", stack.show())
    print("len =",  stack.len())

    val = stack.get()
    print("get val:", val, "len =",  stack.len())

    val = stack.pop()
    print("val:", val, "len =",  stack.len())
    val = stack.pop()
    print("val:", val, "len =",  stack.len())

    try:
        val = stack.pop()
    except:
        print("stack", sys.exc_info())

    print("val:", val, "len =",  stack.len())
    print("show", stack.show())

    # EOF
