# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import threading
i = 12

def wa():
    global i
    i += 1
    print(f'i ben trong thread: {i}')
    
threading.Thread(target=wa).start()
print(f'i ben ngoai: {i}')