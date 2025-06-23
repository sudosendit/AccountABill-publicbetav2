from tkinter import ttk
from tkinter import *
import time

def drawAll(engine):

    def rowbreak(frame, row, column):
        ttk.Label(frame).grid(row=row, column=column)
    
    def drawFrame1(frame):
        for col in range(5):
            frame.grid_columnconfigure(col, weight=4)
        
        ttk.Label(frame, text='Waiting for next billing slot...').grid(row=0, column=0, sticky='w')
        rowbreak(frame, row=1, column=0)
        ttk.Label(frame, text=f'Current time: ', borderwidth=2, relief='solid').grid(row=2, column=0, sticky='nsew')
        engine.frame_1_current_time_label.grid(row=2, column=1, sticky='nsew')
        ttk.Label(frame, text='Next billing slot: ', borderwidth=2, relief='solid').grid(row=3, column=0, sticky='nsew')
        engine.frame_1_next_timeslot_label.grid(row=3, column=1, sticky='nsew')
        ttk.Label(frame, text='Billed Hour\'s: ', borderwidth=2, relief='solid').grid(row=4, column=0, sticky='nsew')
        engine.frame_1_hours_billed_label.grid(row=4, column=1, sticky='nsew')
        ttk.Label(frame, text='Remaining Hour\'s: ', borderwidth=2, relief='solid').grid(row=5, column=0, sticky='nsew')
        engine.frame_1_hours_remaining_label.grid(row=5, column=1, sticky='nsew')
        rowbreak(frame, row=6, column=0)
        # DEV: Next frame button for testing
        #ttk.Button(frame, text='Next Frame', command=lambda: engine.changeFrame(engine.frame_2)).grid(row=7, column=0, sticky='n')

        ttk.Label(frame).grid(row=2,column=2, sticky='nsew') # column break

        ttk.Label(frame, text=f'Start Time: ', borderwidth=2, relief='solid').grid(row=2, column=3, sticky='nsew')
        engine.frame_1_start_time_label.grid(row=2, column=4, sticky='w')
        ttk.Label(frame, text='Finish Time: ', borderwidth=2, relief='solid').grid(row=3, column=3, sticky='nsew')
        engine.frame_1_finish_time_label.grid(row=3, column=4, sticky='nsew')
        ttk.Label(frame, text='Missed Timeslots:', borderwidth=2, relief='solid').grid(row=5, column=3, sticky='nsew')
        engine.frame_1_missing_timeslots_label.grid(row=5, column=4, sticky='w')
        
        engine.frame_1_update_timeslot_button.grid_info_backup = {'row': 7, 'column': 3, 'sticky': 'nsew'}

    
    def drawFrame2(frame):

        ttk.Label(frame, text='Please submit billing for the following timeslot:').grid(row=0, column=0)
        engine.frame_2_target_timeslot_label.grid(row=0, column=1, sticky='n')
        rowbreak(frame, row=1, column=0)
        ttk.OptionMenu(frame, engine.billing_selection_1, engine.default_string_value, *engine.config_biller_one_list).grid(row=2, column=0)
        ttk.OptionMenu(frame, engine.billing_selection_2, engine.default_string_value, *engine.config_biller_two_list).grid(row=2, column=1)
        rowbreak(frame, row=3, column=0)
        ttk.Label(frame, text='Notes: ').grid(row=4, column=0)
        ttk.Entry(frame, textvariable=engine.billing_note).grid(row=4, column=1)
        rowbreak(frame, row=5, column=0)
        ttk.Button(frame, text='Cancel', command=lambda: engine.changeFrame(engine.frame_1)).grid(row=6, column=0)
        ttk.Button(frame, text='Submit', command=engine.submitTimeslot).grid(row=6, column=1)

    def drawFrame3(frame):
        
        rowbreak(frame, row=0, column=0)
        ttk.Label(frame, text='Timeslot successfully submitted!', font=(('Helvetica', 9, 'bold'))).grid(row=1, column=0, sticky='w')
        rowbreak(frame, row=2, column=0)
        ttk.Button(frame, text='Ok', command=lambda: engine.changeFrame(engine.frame_1)).grid(row=3, column=0)

    def drawFrame4(frame):
        ttk.Label(frame, text='Please select missed timeslot to update:').grid(row=0, column=0)
        engine.frame_4_missing_timeslot_optmenu.grid(row=1, column=0)
        rowbreak(frame, row=2, column=0)
        ttk.Button(frame, text='Update Selected Timeslot', command=engine.setMissingSlotAsTarget).grid(row=2,column=0)
        ttk.Button(frame, text='Cancel', command=lambda: engine.changeFrame(engine.frame_1)).grid(row=3,column=0)


    def drawFrame5(frame):
        for col in range(3):
            frame.grid_columnconfigure(col, weight=4)
        ttk.Label(frame, text='Please select a previous timeslot to update:').grid(row=0, column=0)
        engine.frame_5_update_timeslot_optmenu.grid(row=1, column=0)
        rowbreak(frame, row=2, column=0)
        ttk.Label(frame, text='Current billing: ').grid(row=3, column=0)
        engine.frame_5_current_billing_one_label.grid_info_backup = {'row': 4, 'column': 0, 'sticky': 'nsew'}
        engine.frame_5_current_billing_two_label.grid_info_backup = {'row': 5, 'column': 0, 'sticky': 'nsew'}
        rowbreak(frame, row=6, column=0)
        ttk.Button(frame, text='Update Selected Timeslot', command=engine.setManualSlotAsTarget).grid(row=7, column=0)
        ttk.Button(frame, text='Cancel', command=lambda: engine.changeFrame(engine.frame_1)).grid(row=8, column=0)

    def drawFrame6(frame):
        for col in range(4):
            frame.grid_columnconfigure(col, weight=4)

        engine.frame_6_title_label.grid(row=0, column=0)
        rowbreak(frame, row=1, column=0)
        row_index = 2
        for biller in engine.config_biller_one_list: 
            ttk.Label(frame, text=f'{biller}: ', borderwidth=2, relief='solid').grid(row=row_index, column=0, sticky='nsew')
            row_index += 1

        row_index = 2
        for label in engine.frame_6_biller_one_totals_labels:
            label.grid(row=row_index, column=1)
            row_index += 1

        row_index = 2
        for biller in engine.config_biller_two_list:
            ttk.Label(frame, text=f'{biller}: ', borderwidth=2, relief='solid').grid(row=row_index, column=2, sticky='nsew')
            row_index += 1
        
        row_index = 2
        for label in engine.frame_6_biller_two_totals_labels:
            label.grid(row=row_index, column=3)
            row_index += 1
        
        rowbreak(frame, row=row_index, column=0)
        ttk.Label(frame, text='Break Start Time: ', borderwidth=2, relief='solid').grid(row=row_index+1, column=0, sticky='nsew')
        engine.frame_6_break_start_label.grid(row=row_index+1, column=1)
        ttk.Label(frame, text='Break Finish Time: ', borderwidth=2, relief='solid').grid(row=row_index+1, column=2,  sticky='nsew')
        engine.frame_6_break_finish_label.grid(row=row_index+1, column=3)

        ttk.Label(frame, text='Start Time: ', borderwidth=2, relief='solid').grid(row=row_index+2, column=0, sticky='nsew')
        engine.frame_6_start_time_label.grid(row=row_index+2, column=1)
        ttk.Label(frame,text='Finishing Time: ', borderwidth=2, relief='solid').grid(row=row_index+2, column=2, sticky='nsew')
        engine.frame_6_finish_time_label.grid(row=row_index+2, column=3)
        
        rowbreak(frame, row=row_index+3, column=0)
        ttk.Label(frame, text='Total Hours Billed: ', borderwidth=2, relief='solid').grid(row=row_index+4, column=0, sticky='nsew')
        engine.frame_6_hours_billed_label.grid(row=row_index+4, column=1)
        rowbreak(frame, row=row_index+5, column=0) 
        ttk.Button(frame, text='Ok', command=lambda: engine.changeFrame(engine.frame_1)).grid(row=row_index+6, column=0)
        ttk.Button(frame, text='Enter New Date', command=lambda: engine.changeFrame(engine.frame_7)).grid(row=row_index+6, column=3)

    def drawFrame7(frame):
        def setAsToday():
            engine.find_totals_day_selection.set(f'{time.strftime("%d")}')
            engine.find_totals_month_selection.set(f'{time.strftime("%m")}')
            engine.find_totals_year_selection.set(f'{time.strftime("%Y")}')

        ttk.Label(frame, text='Please enter a date:').grid(row=0, column=0)
        rowbreak(frame, row=1, column=0)
        ttk.Label(frame, text='Enter Day:').grid(row=2, column=0)
        ttk.Label(frame, text='Enter Month:').grid(row=2, column=1)
        ttk.Label(frame, text='Enter Year:').grid(row=2, column=2)
        engine.frame_7_day_label.grid(row=3, column=0)
        engine.frame_7_month_label.grid(row=3, column=1)
        engine.frame_7_year_label.grid(row=3, column=2)
        ttk.Button(frame, text='Set as today', command=setAsToday).grid(row=3, column=3)
        rowbreak(frame, row=4, column=0)
        ttk.Button(frame, text='Ok', command=engine.setDateOfBillingTotals).grid(row=5, column=1)
        ttk.Button(frame, text='Cancel', command=lambda: engine.changeFrame(engine.frame_1)).grid(row=5, column=0)



    drawFrame1(engine.frame_1[0])
    drawFrame2(engine.frame_2[0])
    drawFrame3(engine.frame_3[0])
    drawFrame4(engine.frame_4[0])
    drawFrame5(engine.frame_5[0])
    drawFrame6(engine.frame_6[0])
    drawFrame7(engine.frame_7[0])