import csv, os, shutil
# Dev testing imports \/


install_location = os.path.dirname(__file__); os.chdir(install_location)

ffile = install_location + '\\timesheet.csv'

def read(csv_file):
    read_list = []
    row_count = 0
    with open(csv_file, newline='') as cfile:
        reader = csv.DictReader(cfile)
        for row in reader:

            ## Adding extra error catch for adding 0 to time before 10am in timesheet csv
            if '_time' in row:
                if len(row['_time']) <= 4:
                    row['_time'] = '0' + row['_time']
            else:
                pass
            ##

            row_count += 1
            #row["_row_no"] = row_count      >> DEV row count line
            read_list.append(row)

        return read_list

def write(engine, timeslot):

    new_rows = []
    # 
    for row in engine.daily_data:

         ## Adding extra error catch for adding 0 to time before 10am in timesheet csv
        if '_time' in row:
            if len(row['_time']) <= 4:
                row['_time'] = '0' + row['_time']
        else:
            pass
        
        if timeslot == row['_time']:
            
            row['_billing_one'] = engine.billing_selection_1.get()
            row['_billing_two'] = engine.billing_selection_2.get()
            row['_notes'] = engine.billing_note.get()
    
        new_rows.append(row)

    fieldnames = ['_time', '_billing_one', '_billing_two', '_notes']

    with open(engine.csv_file, 'w', newline='') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
        return True

def checkForTimesheet(engine):
    csv_filename = f'AAB_Minutes_{engine.the_date}.csv'
    csv_path_dirname = f'{engine.install_location}\\timesheets\\{engine.the_date.split('-')[2]}\\{engine.the_date.split('-')[1]}-{engine.the_date.split('-')[2]}\\'

    if os.path.exists(csv_path_dirname):
        pass
    else:
        os.makedirs(csv_path_dirname)
        print('\nconsole: Could not find monthly directory, so it was automatically created.')

    try:
        with open(csv_path_dirname+csv_filename):
            print(f'\nconsole: Loaded existing timesheet for {engine.the_date}\n')
            pass
    except FileNotFoundError:
        shutil.copy(f'{engine.install_location}\\assets\\timesheet.csv', f'{csv_path_dirname}{csv_filename}')
        print('\nconsole: New daily timesheet created.\n')
    return f'{csv_path_dirname}{csv_filename}'



            








def write_old(csv_file, current_time, billing_slot_one, billing_slot_two, note_data): #, the_time_value, new_biller1_value, new_biller2_value, new_notes_value
    rows = []
    executed = False    # for testing
    # Read existing rows
    with open(csv_file, newline='') as cfile:
        reader = csv.DictReader(cfile)
        for row in reader:
            
            ## Adding extra error catch for adding 0 to time before 10am in timesheet csv
            if '_time' in row:
                if len(row['_time']) <= 4:
                    row['_time'] = '0' + row['_time']
            else:
                pass
            ##
            
            if current_time == row['_time']:
                row['_billing_one'] = billing_slot_one
                row['_billing_two'] = billing_slot_two
                row['_notes'] = note_data
                executed = True # for testing
            
            rows.append(row)

        print(reader)