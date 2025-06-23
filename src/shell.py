import os, time

def spawnAABCommandLine(engine):
    print("AAB Start Success - Type 'exit' to stop this program.")
    while True:
        user_input = input('command >> ').strip()
        if user_input.lower() in ['help', '?', 'h']:
            print(cmd_help)

        elif user_input.lower() in ['exit', 'quit']:
            input_confirm = input('console: Are you sure you want to quit (y/n) >> ')
            if input_confirm.lower() in ['yes', 'y']:
                print('\nconsole: Program is shutting down...')
                time.sleep(1)
                print('console: Shutdown success.\n')
                engine.shutDown()
                quit()

            else:
                print('Type "yes" after exit command to shutdown program.')
                pass

        elif user_input.lower() in ['cls', 'clear']:
            os.system('cls')
            print("AAB Start Success - Type 'exit' to stop this program.")

        elif user_input.lower() in ['update']:
            engine.changeFrameFromThread(engine.frame_5)

        elif user_input.lower() in ['totals', 'find']:
            engine.changeFrameFromThread(engine.frame_7)

        
        elif user_input.lower() in ['show', 'open']:
            engine.changeFrameFromThread(engine.frame_1)

        elif user_input.lower() in ['hide']:
            engine.window.withdraw()


        else: 
            print('Please type "help" for options.')

cmd_help = """\n--- Help Menu ---
'open' / 'show' - To open window.
'update'        - To update a timeslot.
'totals'        - To calculate todays daily totals.
'find'          - To find daily totals for another date.
'h' / 'help'    - for Help.
'clear' / 'cls' - to clear data in Terminal.
'exit' / 'quit' - to Exit the program.  
------------------\n"""