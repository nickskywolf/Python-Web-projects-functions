import multiprocessing
import time

def find_factors(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def factorize(number):
    # Синхронна версія
    def synchronous_factorize(numbers):
        results = []
        for n in numbers:
            factors = find_factors(n)
            results.append(factors)
        return results

    # Покращена версія з використанням багатьох ядер
    def parallel_factorize(numbers):
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        results = pool.map(find_factors, numbers)
        pool.close()
        pool.join()
        return results

    start_time = time.time()
    results_sync = synchronous_factorize(number)
    end_time = time.time()
    print(f'Synchronous execution time: {end_time - start_time:.2f} seconds')

    start_time = time.time()
    results_parallel = parallel_factorize(number)
    end_time = time.time()
    print(f'Parallel execution time: {end_time - start_time:.2f} seconds')

    return results_sync, results_parallel

if __name__ == '__main__':
    numbers = [128, 255, 99999, 10651060]

    results_sync, results_parallel = factorize(numbers)

    # Перевірка результатів
    a, b, c, d = results_sync
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]



