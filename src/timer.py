import time

def currentTimeSlot():
    def roundDownTimeSlot(x, base=15):
            return base * (x // base)
    
    exact_hour = int(time.strftime("%H"))
    exact_minutes = int(time.strftime("%M"))
    rounded_minutes = roundDownTimeSlot(exact_minutes)
    if rounded_minutes == 0:
        if exact_minutes < 15:
            rounded_hour = exact_hour
        else:
            rounded_hour = (exact_hour - 1) % 24
    else:
        rounded_hour = exact_hour

    return f"{rounded_hour:02}:{rounded_minutes:02}"

def nextTimeSlot(start_time):
    # Get the current time slot start
    start_str = start_time
    hour, minute = map(int, start_str.split(":"))

    # Add 15 minutes
    minute += 15
    if minute >= 60:
        minute -= 60
        hour = (hour + 1) % 24  # Wrap around to 0 after 23

    return f"{hour:02}:{minute:02}"

def currentTime():
    return time.strftime("%H:%M")

def findFinishingTime(engine):

    start_time = engine.billed_timeslots[0]['_time']
    working_hours = engine.config_working_hours
    # Split the start time into hours and minutes
    hours, minutes = map(int, start_time.split(':'))
    
    # Add the whole working hours to the hours part
    end_hours = hours + int(working_hours)
    
    # Check whether on break slots exceed config var
    if (len(engine.onbreak_timeslots)*15) > engine.config_break_minutes:
        break_time = len(engine.onbreak_timeslots)*15
    else:
        break_time = engine.config_break_minutes

    # Add the fractional part (minutes) from the working_hours + Adds break time
    end_minutes = minutes + int((working_hours % 1) * 60)      + (break_time)
    
    # If minutes exceed 60, carry over to the hours
    if end_minutes >= 60:
        end_minutes -= 60
        end_hours += 1
    
    # Handle the case when hours exceed 24 (24-hour format)
    if end_hours >= 24:
        end_hours -= 24
    
    # Return the new time in HH:MM format
    return f"{end_hours:02}:{end_minutes:02}"

def findRemainingHours(engine):
    return engine.config_working_hours - engine.hours_worked

# Threaded loop
def startTimer(engine):
        while True:
            time.sleep(5)
            
            # Runs update on most global class data vars and Labels in frames - also calls updateTimeslotLists()
            engine.updateFrameDataAndLabels()

            # Check that current time = rounded time to timeslot and that isn't currently submitting a TS on frame 2
            if engine.current_time == engine.rounded_time and engine.current_frame[3] != 2:
                # Checks to ensure current timeslot has not been submitted
                for row in engine.daily_data:
                    if engine.rounded_time == row['_time']: 
                        if len(row['_billing_one']) > 0:
                            pass
                        else:
                            # Sumbits timeslot
                            try:
                                engine.target_timeslot = engine.rounded_time
                                engine.frame_2_target_timeslot_label.config(text=f'{engine.target_timeslot}-{nextTimeSlot(engine.target_timeslot)}')
                                engine.window.after(0, engine.changeFrameFromThread, engine.frame_2)
                
                            except Exception as e:
                                print(e)
                

           
                    

            

                
                
    
    
        
