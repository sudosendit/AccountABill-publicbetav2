import threading, os
import src.window as window
import src.shell as shell
import src.timer as timer


if __name__ in "__main__":
    # Sets dir working loc
    install_location = os.path.dirname(__file__); os.chdir(install_location)
    
    # window initialization
    engine = window.AAB_Instance(install_location)

    # Starts timer to check for timeslot match
    timer_thread = threading.Thread(target=timer.startTimer, args=(engine,))
    timer_thread.daemon = True
    timer_thread.start()

    # Starts shell to interact with AAB
    cmd_thread = threading.Thread(target=shell.spawnAABCommandLine, args=(engine,))
    cmd_thread.daemon = True
    cmd_thread.start()

    # Spawn and hides window.
    #engine.window.withdraw()
    engine.window.mainloop()
    
    #

