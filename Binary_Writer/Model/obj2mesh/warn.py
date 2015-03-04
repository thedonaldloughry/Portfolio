warned={}

def warn_reset():
    global warned
    warned={}
    
def warn(msg):
    if msg not in warned:
        print("Warning:",msg)
        warned[msg]=1
    
