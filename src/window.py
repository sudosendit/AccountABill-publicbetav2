from tkinter import Tk, ttk
from tkinter import *
import src.frames as frames
import src.timer as timer
import src.csvHandler as csvHandler
import configparser, os


class AAB_Instance:
    # Function to initialize all required functions on starting call in main.py
    def __init__(self, install_location):
        
        self.install_location = install_location
        
        self.window = Tk()
    
        self.configureWindow()

        self.loadFrames()

        self.createDropMenu()

        self.loadConfiguration()

        self.windowData()

        self.frameLabels()

        self.drawFrames()
    
    # Function to configure properties of the window
    def configureWindow(self):
        
        # changes init var to Tk window instance
        self.window.attributes('-topmost', True)
        self.window.title('Account-A-Bill')
        self.window.protocol('WM_DELETE_WINDOW', self.manualWindowClose)
        self.window.geometry(f'500x220+{self.window.winfo_screenwidth()-520}+{self.window.winfo_screenheight()-320}')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    # function to initialize a drop down menu for the window
    def createDropMenu(self):
        menu_bar = Menu()
        self.window.config(menu=menu_bar)

        # First section - Dev Tools
        drop_section_1 = Menu(menu_bar, tearoff=False)
        drop_section_1.add_command(label='Geometry Editor', command=self.geometryEditor)

        # Second section - commands
        drop_section_2 = Menu(menu_bar, tearoff=False)
        drop_section_2.add_command(label='Update Timeslot', command=self.updateManualTimeslotList)
        drop_section_2.add_command(label='Find daily totals', command=lambda: self.changeFrame(self.frame_7))

        menu_bar.add_cascade(label='Commands', menu=drop_section_2)
        #menu_bar.add_cascade(label='Development tools', menu=drop_section_1)  >> Add this back for DEV TOOL access

    # Function to initialize all the the frame vars used
    def loadFrames(self):
        screen_size_x = self.window.winfo_screenwidth()    # 1920
        screen_size_y = self.window.winfo_screenheight()   # 1080

        default_geometry_offset = f'{screen_size_x-520}+{screen_size_y-320}'

        self.current_frame = None
        
        # frame indexs; [0] = frame_var,                    [1] = frame_name,   [2] = frame_geometry, [3] = frame number
        self.frame_1 = (ttk.Frame(self.window, padding=15), 'Idle Frame',          f'500x200+{default_geometry_offset}',             1)
        self.frame_2 = (ttk.Frame(self.window, padding=15), 'Add New Timeslot Frame',          f'500x200+{default_geometry_offset}',             2)
        self.frame_3 = (ttk.Frame(self.window, padding=15), 'Confirmation Frame',          f'500x200+{default_geometry_offset}',             3)
        self.frame_4 = (ttk.Frame(self.window, padding=15), 'Missing Timeslot Frame',          f'500x200+{default_geometry_offset}',             4)
        self.frame_5 = (ttk.Frame(self.window, padding=15), 'Update Timeslot Frame',          f'500x220+{default_geometry_offset}',             5)
        self.frame_6 = (ttk.Frame(self.window, padding=15), 'Find Totals Frame',          f'600x350+{screen_size_x-620}+{screen_size_y-470}',             6)
        self.frame_7 = (ttk.Frame(self.window, padding=15), 'FT Enter Date Frame',          f'500x200+{default_geometry_offset}',             7)

        self.frameList = [
        self.frame_1, 
        self.frame_2,
        self.frame_3,
        self.frame_4,
        self.frame_5,
        self.frame_6,
        self.frame_7
        ]

    # Function to initialize global data vars
    def windowData(self):
        #globals
        self.hours_worked = 0
        self.onbreak_string_value = 'On Break'
        self.default_string_value = '-- Select --'
        self.the_date = timer.time.strftime('%d-%m-%Y')
        self.current_time = timer.currentTime()             # Will return string of the current machine time
        self.rounded_time = timer.currentTimeSlot()         # Will return string of current time rounded down to 15 min slot
        self.next_timeslot = None                           # Will return string of current time rounded up to 15 min slot 
        
        self.billed_timeslots = []                          # Will return list of all dict rows in daily_data the have values
        self.unbilled_timeslots = []                        # Will return list of all dict rows in daily_data the do not have values
        self.missing_timeslots = []                         # Will return list of all dict rows from daily_data inbetween start and end timeslots.
        self.target_timeslot = None     
        self.starting_time = None
        self.finishing_time = None
        self.timeslot_string = None


        # Daily data is pulling from template it need to pull from daily timesheet
        self.csv_file = csvHandler.checkForTimesheet(self)
        self.daily_data = csvHandler.read(self.csv_file)

        # Frame 2 - Submit Timeslot
        self.billing_selection_1 = StringVar(self.window)
        self.billing_selection_2 = StringVar(self.window)
        self.billing_note = StringVar(self.window)

        # Frame 4
        self.missing_timeslot_update_selection = StringVar(self.window)

        # Frame 5
        self.manual_timeslot_update_selection = StringVar(self.window)

        # Frame 7 
        self.find_totals_day_selection = StringVar(self.window)
        self.find_totals_month_selection = StringVar(self.window)
        self.find_totals_year_selection = StringVar(self.window)

    # Function to initialize all temporary or changing label and buttons
    def frameLabels(self):
        # Frame 1 - Idle Frame
        self.frame_1_current_time_label = ttk.Label(
            self.frame_1[0], 
            text=f'{self.current_time}', 
            font=('Helvetica', 10, 'bold')
        )

        self.frame_1_next_timeslot_label = ttk.Label(
            self.frame_1[0], 
            text=f'{timer.nextTimeSlot(self.rounded_time)}', 
            font=('Helvetica', 10, 'bold')
        )

        self.frame_1_missing_timeslots_label = ttk.Label(
            self.frame_1[0], 
            text=f'Loading...', 
            font=('Helvetica', 10, 'bold')
        )

        self.frame_1_start_time_label = ttk.Label(
            self.frame_1[0], 
            text=f'Loading...', 
            font=('Helvetica', 10, 'bold')
        )

        self.frame_1_finish_time_label = ttk.Label(
            self.frame_1[0], 
            text=f'Loading...', 
            font=('Helvetica', 10, 'bold')
        )

        self.frame_1_update_timeslot_button = ttk.Button(
            self.frame_1[0],
            text='Update Missing Timeslots',
            command=self.updateMissingTimeslotList)
        
        
        self.frame_1_hours_billed_label = ttk.Label(
            self.frame_1[0],
            text='Loading...',
            font=('Helvetica', 10, 'bold')
        )

        self.frame_1_hours_remaining_label = ttk.Label(
            self.frame_1[0],
            text='Loading...',
            font=('Helvetica', 10, 'bold')
        )

        # Frame 2 - Add Timeslot Frame
        self.frame_2_target_timeslot_label = ttk.Label(
            self.frame_2[0], 
            text=f'{self.rounded_time} - {timer.nextTimeSlot(self.rounded_time)}', 
            font=('Helvetica', 10, 'bold')
        )

        # Frame 4 - Missing Timeslot Frame
        self.frame_4_missing_timeslot_optmenu = ttk.OptionMenu(
            self.frame_4[0],
            self.missing_timeslot_update_selection,
            self.default_string_value,
        )

        # Frame 5 - Update Timeslot Frame
        self.frame_5_update_timeslot_optmenu = ttk.OptionMenu(
            self.frame_5[0],
            self.manual_timeslot_update_selection,
            self.default_string_value
        )

        self.frame_5_current_billing_one_label = ttk.Label(
            self.frame_5[0],
            text='',
            borderwidth=2,
            relief='solid'
        )

        self.frame_5_current_billing_two_label = ttk.Label(
            self.frame_5[0],
            text='',
            borderwidth=2,
            relief='solid'
        )


        # Frame 6 - Find Totals frame
        # Creats billing_one label in list
        self.frame_6_title_label = ttk.Label(
            self.frame_6[0],
            text=''
        )

        self.frame_6_biller_one_totals_labels = []
        for biller in self.config_biller_one_list:
            new_label = ttk.Label(
                self.frame_6[0],
                text=f'{biller}',
                font=('Helvetica', 10, 'bold')
                )
            self.frame_6_biller_one_totals_labels.append(new_label)
        
        # Creates billing_two labels in list
        self.frame_6_biller_two_totals_labels = []
        for biller in self.config_biller_two_list:
            new_label = ttk.Label(
                self.frame_6[0],
                text=f'{biller}',
                font=('Helvetica', 10, 'bold')
                )
            self.frame_6_biller_two_totals_labels.append(new_label)
        
        self.frame_6_hours_billed_label = ttk.Label(
            self.frame_6[0], 
            text='',
            font=('Helvetica', 10, 'bold'))
        
        self.frame_6_start_time_label = ttk.Label(
            self.frame_6[0], 
            text='',
            font=('Helvetica', 10, 'bold'))

        self.frame_6_finish_time_label = ttk.Label(
            self.frame_6[0], 
            text='',
            font=('Helvetica', 10, 'bold'))

        self.frame_6_break_start_label = ttk.Label(
            self.frame_6[0], 
            text='',
            font=('Helvetica', 10, 'bold'))
        
        self.frame_6_break_finish_label = ttk.Label(
            self.frame_6[0], 
            text='',
            font=('Helvetica', 10, 'bold'))
        
        # Frame 7
        self.frame_7_day_label = ttk.Entry(
            self.frame_7[0],
            textvariable=self.find_totals_day_selection
        )

        self.frame_7_month_label = ttk.Entry(
            self.frame_7[0],
            textvariable=self.find_totals_month_selection
        )

        self.frame_7_year_label = ttk.Entry(
            self.frame_7[0],
            textvariable=self.find_totals_year_selection
        )

    # Function to initialize configuration vars from config.ini
    def loadConfiguration(self):
        # Create local path to csv and function ensure it exists 

        # Complete load from config
        config = configparser.ConfigParser()
        config.read(self.install_location+"\\config.ini")

        self.config_biller_one_list = []
        self.config_biller_two_list = []
        self.config_working_hours = config.getint('settings', 'working_hours')
        self.config_break_minutes = config.getint('settings', 'break_minutes')

        biller_one_import = (config.get('settings', 'biller_one_list')).split(',')
        biller_two_import = (config.get('settings', 'biller_two_list')).split(',')


        for entry in biller_one_import:
            self.config_biller_one_list.append(entry.strip())

        for entry in biller_two_import:
            self.config_biller_two_list.append(entry.strip())

    # Function to initialize all tkinter frame gridding
    def drawFrames(self):
        frames.drawAll(self)
        self.current_frame = self.frame_1
        self.frame_1[0].grid(row=0, column=0, sticky='nsew')

    # Function available to call to change frame of app
    def changeFrame(self, next_frame):
        #self.frame_1_current_time_label
        for frame in self.frameList:
            if next_frame[0] != frame[0]:
                frame[0].grid_forget()
        
        next_frame[0].grid(row=0, column=0, sticky='nsew')
        self.current_frame = next_frame
        #self.window.title(f'Account-A-Bill')
        self.window.geometry(next_frame[2])

    # Function available to call to change frame of app from a different thread e.g. imports from shell or timer
    def changeFrameFromThread(self, next_frame):
        self.window.after(0, self.changeFrame, next_frame)
        self.window.deiconify()

    # Function called to update global lists - included in timer
    def updateTimeslotLists(self):
        def clearIndexing():
            for row in self.daily_data:
                del row['_row_index']

        # Resets all lists
        self.billed_timeslots = []      
        self.unbilled_timeslots = []    
        self.missing_timeslots = []
        self.onbreak_timeslots = []     

        # Builds list for billed_time, sets starting and finishing times + add rows numbers to daily_data
        index_key = '_row_index'
        row_index = 0
        for row in self.daily_data:
        
            if len(row['_billing_one']) > 0 and row['_billing_one'] != self.onbreak_string_value:
                self.billed_timeslots.append(row)
                # remove lunch timeslots
            
            elif len(row['_billing_one']) <= 0:
                self.unbilled_timeslots.append(row)

            if row['_billing_one'] == self.onbreak_string_value:
                self.onbreak_timeslots.append(row)
                
            row[index_key] = row_index
            row_index += 1

        try:
            self.starting_time = self.billed_timeslots[0]['_time']
            self.finishing_time = timer.findFinishingTime(self)
            
        except IndexError:
            clearIndexing()
            return
        
        for row in self.daily_data:
            if row['_time'] == self.finishing_time:
                finishing_time_row_index = row[index_key]
        
            if row['_time'] == self.rounded_time:
                current_time_index = row[index_key] + 1

        starting_time_row_index = self.billed_timeslots[0][index_key]

        for unbilled_row in self.unbilled_timeslots:
            # Probs need to add date check. Past totals will misinterperet the current_time_index check
            if unbilled_row[index_key] > starting_time_row_index and (unbilled_row[index_key] < finishing_time_row_index and unbilled_row[index_key] < current_time_index):
                self.missing_timeslots.append(unbilled_row)

        # Clear _row_index for saving data
        clearIndexing()

    # Function called to update most labels in frameLabels()
    def updateFrameDataAndLabels(self):
        # Update windowData values
        self.current_time = timer.currentTime()
        self.rounded_time = timer.currentTimeSlot()
        self.next_timeslot = timer.nextTimeSlot(self.rounded_time)
        
        self.timeslot_string = f'{self.rounded_time} - {self.next_timeslot}'
        # udpdateTimeslotLists() to update windowData billed_timeslots, unbilled_timeslots and missing_timeslots
        self.updateTimeslotLists()
        self.hours_worked = len(self.billed_timeslots)*15/60
        ### Update frame labels >> Probs need to put in updateFrameLabels()
        #frame1
        self.frame_1_current_time_label.config(text=f'{self.current_time}')
        self.frame_1_next_timeslot_label.config(text=f'{self.next_timeslot}')
        if len(self.billed_timeslots) > 0: 
            self.frame_1_start_time_label.config(text=f'{self.billed_timeslots[0]['_time']}')
            self.frame_1_finish_time_label.config(text=f'{timer.findFinishingTime(self)}')
            self.frame_1_hours_remaining_label.config(text=f'{timer.findRemainingHours(self)} /hr\'s')
        else:
            self.frame_1_start_time_label.config(text='Awaiting Entry')
            self.frame_1_finish_time_label.config(text='Awaiting Entry')
            self.frame_1_hours_remaining_label.config(text=f'{self.config_working_hours} /hr\'s')

        self.frame_1_missing_timeslots_label.config(text=f'{len(self.missing_timeslots)}')
        if len(self.missing_timeslots) > 0:
            self.frame_1_update_timeslot_button.grid(**self.frame_1_update_timeslot_button.grid_info_backup)
        elif len(self.missing_timeslots) <= 0:
            self.frame_1_update_timeslot_button.grid_forget()
        self.frame_1_hours_billed_label.config(text=f'{self.hours_worked} /hr\'s')

        # Add check for remaining hours with checkRemainingHours()
        
    # Function called to write entire daily_data to new csv
    def submitTimeslot(self):
        if (self.billing_selection_1.get() == self.default_string_value) or (self.billing_selection_2.get() == self.default_string_value):
            print('console: You need to add biller values.')
            return
    
        # Attempts to write with if line
        if csvHandler.write(self, self.target_timeslot) is True:
            self.changeFrame(self.frame_3)

        # Updates list immediately after submission
        self.updateFrameDataAndLabels()

    # Function called to update the Missing Timeslot Frame before changing to it
    def updateMissingTimeslotList(self):

        self.frame_4_missing_timeslot_optmenu['menu'].delete(0, 'end') 

        # Update missing slot list
        for timeslot in self.missing_timeslots:
            self.frame_4_missing_timeslot_optmenu['menu'].add_command(
                label=f'{timeslot['_time']}-{timer.nextTimeSlot(timeslot['_time'])}: ',
                command=lambda value=timeslot['_time']:  self.missing_timeslot_update_selection.set(value)
            )

        self.changeFrame(self.frame_4)

    # Function called to update the Update Timeslot Frame before changing to it
    def updateManualTimeslotList(self):
        def showCurrentSelections(target_timeslot):
            self.frame_5_current_billing_one_label.grid(**self.frame_5_current_billing_one_label.grid_info_backup)
            self.frame_5_current_billing_two_label.grid(**self.frame_5_current_billing_two_label.grid_info_backup)
            for timeslot in self.daily_data:
                if target_timeslot == timeslot:
                    self.frame_5_current_billing_one_label.config(text=f'{timeslot['_billing_one']}')
                    self.frame_5_current_billing_two_label.config(text=f'{timeslot['_billing_two']}')
            

        self.frame_5_update_timeslot_optmenu['menu'].delete(0, 'end') 
        
        # Update missing slot list
        for timeslot in self.daily_data:
            self.frame_5_update_timeslot_optmenu['menu'].add_command(
                label=f'{timeslot['_time']}-{timer.nextTimeSlot(timeslot['_time'])}: {timeslot['_billing_one']}/{timeslot['_billing_two']}',
                command=lambda value=timeslot:  (self.manual_timeslot_update_selection.set(value['_time']),
                showCurrentSelections(value))
            )

        self.changeFrame(self.frame_5)
    
    # function called to update the Find Totals Frame before changing to it
    def updateBillingTotals(self, timeslot_data, file_date):
        self.frame_6_title_label.config(text=f'Billing totals summary for   {file_date}')
        enum_count = 0
        biller_count = 0
        for biller in self.config_biller_one_list:
            for timeslot in timeslot_data:    # note: can change self.daily_data with specific timesheet
                if biller == timeslot['_billing_one']:
                    biller_count += 1

            # Labels sort in list are basicall getting assign only in order. If order chnages could cause issue.
            self.frame_6_biller_one_totals_labels[enum_count].config(text=f'{(biller_count * 15) / 60} /hr\'s')
            enum_count += 1
            biller_count = 0

        enum_count = 0
        for biller in self.config_biller_two_list:
            for timeslot in timeslot_data:    # note: can change self.daily_data with specific timesheet
                if biller == timeslot['_billing_two']:
                    biller_count += 1

            # Labels sort in list are basicall getting assign only in order. If order chnages could cause issue.
            self.frame_6_biller_two_totals_labels[enum_count].config(text=f'{(biller_count * 15) / 60} /hr\'s')
            enum_count += 1
            biller_count = 0
        
        # Rebuild some lists for custom date selection
        onbreak_slots = []
        billed_slots = []
        for timeslot in timeslot_data:
            if len(timeslot['_billing_one']) > 0 and timeslot['_billing_one'] != self.onbreak_string_value:
                billed_slots.append(timeslot)
            if timeslot['_billing_one'] == self.onbreak_string_value:
                onbreak_slots.append(timeslot)
            
        if len(onbreak_slots) > 0:
            self.frame_6_break_start_label.config(text=f'{onbreak_slots[0]['_time']}')
            self.frame_6_break_finish_label.config(text=f'{timer.nextTimeSlot(onbreak_slots[-1]['_time'])}')
        else:
            self.frame_6_break_start_label.config(text=f'None')
            self.frame_6_break_finish_label.config(text=f'None')

        self.frame_6_hours_billed_label.config(text=f'{(len(billed_slots) * 15) / 60} /hr\'s')
        self.frame_6_start_time_label.config(text=f'{billed_slots[0]['_time']}')

        self.frame_6_finish_time_label.config(text=f'{billed_slots[-1]['_time']}')
        
        self.changeFrame(self.frame_6)

    # Function called to set the correct  timeslot_data for updateBillingTotals()
    def setDateOfBillingTotals(self):
        target_day = self.find_totals_day_selection.get().strip()
        target_month = self.find_totals_month_selection.get().strip()
        target_year = self.find_totals_year_selection.get().strip()

        if int(target_day) > 32 or int(target_day) <= 0:
            print('\nconsole: You need to enter a day between 1 - 31.')
            return
        
        if len(target_month) == 1: 
            target_month = '0' + target_month
            self.find_totals_month_selection.set(target_month)
        
        if int(target_month) > 13 or int(target_month) <= 0:
            print('\nconsole: You need to enter a month between 1 - 12.\nEnter...')
            return
        
        if len(target_year) > 4 or len(target_year) < 4:
            print('\nconsole: 4 digits are required for the year e.g. 2000.\nEnter...')
            return
        

        for selection in [target_day, target_month, target_year]:
            if len(selection) <= 0:
                print('\nconsole: Please enter all fields.\nEnter...')
                return
            
        file_date = f'{target_day}-{target_month}-{target_year}'
        target_directory = self.install_location + '\\timesheets' + f'\\{target_year}' + f'\\{target_month}-{target_year}\\'

        try:
            for file in os.listdir(target_directory):
                if file_date in file: 
                    target_csv = target_directory + file

        except FileNotFoundError:
            print(f'\nconsole: Unable to find folder for  "{target_month}-{target_year}".')
            return

        try:
            target_csv
        except UnboundLocalError:
            print(f'\nconsole: Unable to find timesheet for {file_date}.\nEnter...')
            return
        
        self.updateBillingTotals(csvHandler.read(target_csv), file_date)        

    # Function called to set the correct missing timeslot time to update for the submitTimeslot()
    def setMissingSlotAsTarget(self):
        if self.missing_timeslot_update_selection.get() == self.default_string_value:
            print('console: Please make a selection.')
            return

        self.target_timeslot = self.missing_timeslot_update_selection.get()
        self.missing_timeslot_update_selection.set(self.default_string_value)
        self.frame_2_target_timeslot_label.config(text=f'{self.target_timeslot}-{timer.nextTimeSlot(self.target_timeslot)}')
        self.frame_1_update_timeslot_button.grid_forget()
        self.changeFrame(self.frame_2)

    # Function called to set the correct targeted timeslot to update for the submitTimeslot()
    def setManualSlotAsTarget(self):
        if self.manual_timeslot_update_selection.get() == self.default_string_value:
            print('console: Please make a selection.')
            return

        self.target_timeslot = self.manual_timeslot_update_selection.get()
        self.manual_timeslot_update_selection.set(self.default_string_value)
        self.frame_2_target_timeslot_label.config(text=f'{self.target_timeslot}-{timer.nextTimeSlot(self.target_timeslot)}')
        self.frame_5_current_billing_one_label.grid_forget()
        self.frame_5_current_billing_two_label.grid_forget()
        self.changeFrame(self.frame_2)
    
    def checkRemainingHours(self):

        if timer.findRemainingHours(self) <= 0:
            print('give user option to stop billing')

    def manualWindowClose(self):
        self.changeFrame(self.frame_1)
        self.window.withdraw()

    # Utility function to call for shutdown
    def shutDown(self):
        self.window.destroy()


    # Development assistance functions
    def geometryEditor(self):

        def updateWindow():
                if len(changeWidthVar.get()) <= 0 or len(changeHeightVar.get()) <= 0:
                    print('\nError', 'Please fill in both fields.')
                    return
                try: 
                    self.window.geometry(f'{changeWidthVar.get()}x{changeHeightVar.get()}')
                except TclError as e:
                    print('\nError', f'{e}')
                    return

        geoChangeWindow = Tk()
        changeHeightVar = StringVar(geoChangeWindow)
        changeWidthVar = StringVar(geoChangeWindow)
        geoChangeWindow.geometry(f'400x200')
        geoChangeWindow.protocol('WM_DELETE_WINDOW', geoChangeWindow.destroy)
        geoChangeFrame = ttk.Frame(geoChangeWindow, padding=15)
        geoChangeWindow.title(f'Geometry Modifier')
        geoChangeWindow.attributes('-topmost', True)
        ttk.Label(geoChangeFrame, text=f'Update the geometry of the current frame.').grid(row=0, column=0, sticky='nsew')
        ttk.Label(geoChangeFrame, text=f'Width:').grid(row=1, column=0, sticky='nsew')
        ttk.Entry(geoChangeFrame, textvariable=changeWidthVar).grid(row=1, column=1)
        ttk.Label(geoChangeFrame, text=f'Height:').grid(row=2, column=0, sticky='nsew')
        ttk.Entry(geoChangeFrame, textvariable=changeHeightVar).grid(row=2, column=1)
        ttk.Button(geoChangeFrame, text='Change', command=updateWindow).grid(row=3, column=0, sticky='ns')
        ttk.Button(geoChangeFrame, text='Close', command=geoChangeWindow.destroy).grid(row=4, column=0, sticky='ns')
        geoChangeFrame.grid(row=0, column=0, sticky='nsew')
        geoChangeWindow.mainloop()

