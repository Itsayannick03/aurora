from time import sleep
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

def step1():
    print("1")
    sleep(1)
def step2():
    print("2")
    sleep(2)
def step3():
    print("3")
    sleep(3)

steps = [
    "Checking system compatibility",
    "Checking dependencies",
    "Installing aurora.service",
    "Installing aurora.timer",
    "Reloading systemd daemon",
    "Enabling aurora.timer",
]

with Progress(
   
) as progress:

    task = progress.add_task("Step 1: printing 1", total=3)
    
    progress.advance(task)
    step1()
    
    
    progress.advance(task)
    step2()
    
    
    progress.advance(task)
    step3()
    

print(":: Installation complete")