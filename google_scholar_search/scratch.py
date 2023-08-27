import time


def run_job(status, poll_interval=2):
    """TODO"""
    status = "running"
    while True:
        time.sleep(poll_interval)
        if status 
        status = "finished"

    return status


# Poll endpoint 101 times
state = input("Enter state: ")
state = run_job(state)


print(state)