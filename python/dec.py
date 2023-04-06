def ann(f):
    def wrapper():
        print("About to run")
        f()
        print("Done with the function")

    return wrapper

@ann
def hello():
    print("Help")

hello()

