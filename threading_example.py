import time
import multiprocessing
import concurrent.futures


def do_something():
    print("sleep")
    time.sleep(1)
    print("done")


# synchronously
start = time.perf_counter()
do_something()
do_something()
do_something()
finish = time.perf_counter()
print(f'Finished in {round(finish - start, 2)} second(s)')

# asynchronously - multi processing
start = time.perf_counter()
p1 = multiprocessing.Process(target=do_something)
p2 = multiprocessing.Process(target=do_something)
# start the processes
p1.start()
p2.start()
# wait for processes to finish
p1.join()
p2.join()
finish = time.perf_counter()
print(f'Finished in {round(finish - start, 3)} second(s)')


# asynchronously - multi processing
start = time.perf_counter()
processes = []
for _ in range(10):
    p = multiprocessing.Process(target=do_something)
    p.start()
    processes.append(p)
for process in processes:
    process.join()
finish = time.perf_counter()
print(f'Finished in {round(finish - start, 3)} second(s)')


def do_something_arg(seconds):
    print(f"sleep {seconds}")
    time.sleep(seconds)
    print("done")
    return f"done{seconds}"


# asynchronously - multi processing
start = time.perf_counter()
processes = []
for _ in range(10):
    p = multiprocessing.Process(target=do_something_arg, args=[1.5])
    p.start()
    processes.append(p)

for process in processes:
    process.join()
finish = time.perf_counter()
print(f'Finished in {round(finish - start, 3)} second(s)')

# asynchronously - multi processing
start = time.perf_counter()
with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = executor.map(do_something_arg, secs)
    # results = [executor.submit(do_something_arg, sec) for sec in secs]
    for f in concurrent.futures.as_completed(results):
        print(f.result())
finish = time.perf_counter()
print(f'Finished in {round(finish - start, 3)} second(s)')


