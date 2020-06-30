import multiprocessing as mp
nprocs = 21

def func(x):
    print(x)
    return x**2

with mp.Pool( nprocs ) as p:
    result = p.map( func, range(0,10) )


print(mp.cpu_count())

#print(result)