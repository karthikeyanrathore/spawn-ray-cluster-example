# ray-cluster-example


## experiments - monte carlo simulation

run simulation with ray cluster in a distributed way
```
docker-compuse up
REMOTE=1 ./monte_carlo.py 
```

run simulation in serialized way
```
./monte_carlo.py 
```

### task-1

```
NUM_TASK = 1_0
NUM_SAMPLES_PER_TASK = 10_000_000
TOTAL_NUM_SAMPLES = NUM_TASK * NUM_SAMPLES_PER_TASK
```

- with ray distributed parallelization (1 cluster = 1 head + 1 worker) it takes 15 seconds. 
- without any parallelization (serialized) it takes 48 sec to compute pi value.

### task-2

```
NUM_TASK = 10
NUM_SAMPLES_PER_TASK = 20_000_000
TOTAL_NUM_SAMPLES = NUM_TASK * NUM_SAMPLES_PER_TASK
```

- with ray it takes (1 cluster = 1 head + 2 worker) -  34.221394062042236secs 
- with ray it takes (1 cluster = 1 head + 1 worker) - 29.369746923446655secs
- serialized way it takes - 101.6926052570343secs