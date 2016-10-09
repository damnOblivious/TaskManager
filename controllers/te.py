#!/usr/bin/python
dict = {}
a=1
b=3
dict[str(a)+str(b)]="testing"
dict['one'] = "This is one"
dict[2]= "This is two"
print dict['one'] 
print dict['13']
print dict.keys() 
print dict.values()
if dict.get(str(a)+str(b)):
    print 'yes'
else:
    print 'no'
