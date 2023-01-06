from datetime import datetime
import tkinter as tk
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
import koreanNumbers as kn
import os


def get_time_in_korean(dt):
    '''
    Takes a datetime.datetime object and returns the current time written out 
    phonetically in Korean. 

    Normally one might say the time as: 두 시 오분.
    This function returns the exact characters needed to read each number aloud.

    @type       dt: datetime.datetime
    @params:    dt: the current date and time

    @rtype:     string
    @return:    the current time written out phonetically in Korean 
    '''
    h = dt.hour  # 1-24
    m = dt.minute  # 1-59

    # Use these Native-Korean numbers 1-12 for hours, where 12's key is 0
    hours = {0: '열두', 1: '한', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯',
             7: '일곱', 8: '여덟', 9: '아홉', 10: '열', 11: '열한', }

    # Specify time of day AM (오전) / PM (오후)
    if (h % 24) < 12:
        timeofday = "오전"
    else:
        timeofday = "오후"

    # Convert hour 'h' variable to a number between 0 - 11 for proper key lookup
    h = (h % 12)

    # O' Clock sharp
    if m == 0:
        # It's [hours] o' clock
        return f"{timeofday} {hours[h]}시 정각"

    # Before 30 minute mark
    elif m < 30:
        # 십오 분 전 [hours]시 = It's quarter to [hours]
        # It's [minutes] minutes past [hours]
        return f"{timeofday} {hours[h]}시 {kn.KoreanNumber(m)}분"

    # After 30 minute mark
    elif m > 30:
        if h == 11:
            # It's [minutes] minutes before (to) [hour]
            return f"{timeofday} {kn.KoreanNumber(60 - m)}분 전 {hours[0]}시"
        else:
            # It's [minutes] minutes before (to) [hour]
            return f"{timeofday} {kn.KoreanNumber(60 - m)}분 전 {hours[h + 1]}시"

    # Exactly half past
    else:
        return f"{timeofday}{hours[h]} 시 반"


def get_date_in_korean(dt):
    '''
    Takes a datetime.datetime object and returns the current date written out 
    phonetically in Korean. 

    Normally one might say the date as: 오늘은 2023년 1월 5일 목요일이에요.
    This function returns the exact characters needed to read each number aloud.

    @type       date: datetime.datetime
    @params:    date: the current date and time

    @rtype:     string
    @return:    the current date written out phonetically in Korean in the form
                of the sentence above
    '''
    weekday = dt.weekday()
    month = dt.month
    day = dt.day
    year = dt.year

    # Monday(0) - Sunday(6) in Korean
    days = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일',
            5: '토요일', 6: '일요일'}

    # Today is [weekday] [month] [day] [year].
    return f"오늘은 {kn.KoreanNumber(year)}년 {kn.KoreanNumber(month)}월 {kn.KoreanNumber(day)}일 {days[weekday]}이에요."


def display(curr=''):
    '''
    Takes a datetime.datetime object and updates the display configuration
    labels to match the current time including hours, minutes, and seconds as 
    well as the date including year, month, day of the week, and day

    @type       curr: str or datetime.datetime
    @params:    curr: the current datetime.now() or an empty str
    '''

    # Get current local datetime
    now = datetime.now()

    # Get time and date as str in Korean
    time = get_time_in_korean(now)
    date = get_date_in_korean(now)

    # If the time str has changes, update it
    if now != curr:
        curr = now
        # Update minutes and hours
        clock_frame.config(text=time)
        # Update seconds
        seconds_frame.config(text=f"{kn.KoreanNumber(now.second)}초")
        # Update date
        date_frame.config(text=date)

    # Calls itself every 200 milliseconds to update
    clock_frame.after(200, display)


if __name__ == '__main__':

    # Create root object
    root = tk.Tk()

    # Set title
    root.title("Korean Phrase Clock")

    icon = Image.open(os.path.join('images', 'icon.png'))
    photo = ImageTk.PhotoImage(icon)
    root.wm_iconphoto(False, photo)

    # Center on screen
    root.geometry("1500x300+210+210")

    # Set attributes for buttons and labels
    red_bar = Label(root, bg='#C8102E')

    # Labels
    date_frame = Label(root, font=('Gulim', 20), bg='#002F6C', fg='white')
    question_frame = Label(root, font=('Gulim', 20),
                           bg='#F8F8F8', fg='black')
    clock_frame = Label(root, font=('Gulim', 100), bg='#F8F8F8', fg='black')
    seconds_frame = Label(root, font=('Gulim', 20), bg='#DCDCDC', fg='black')

    # As 'What time is it?' in Korean
    question_frame.config(text='몇 시예요?')

    # Pack the buttons and lables
    red_bar.pack(fill='both', expand=1)
    date_frame.pack(fill='both', expand=1)
    question_frame.pack(fill='both', expand=1)
    clock_frame.pack(fill='both', expand=1)
    seconds_frame.pack(fill='both', expand=1)

    # Run
    display()
    root.mainloop()
