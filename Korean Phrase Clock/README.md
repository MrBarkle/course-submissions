# ![Korean Icon](/images/icon.png) [Korean Phrase Clock](#title)

#### Created By: [Brandon Barkle](https://www.linkedin.com/in/brandonbarkle)

## Project Description:

For this project I have created two Python files: [clock.py](/clock.py) and [koreanNumbers.py](/koreanNumbers.py). Together they are used to create a simple clock that displays the current local time in the Korean language as it would be written out fully for the purpose of speaking. What does this mean? Rather than displaying the time as 2:30 AM for instance, in Korean you could read the time as "오전 두 시 반" instead. This clock makes use of a simple Tkinter interface to actively display the time in the format described.

I created this project to help myself, and hopefully others, learn the Korean number system, date format, and time format. With it, I think it's possible to learn all of these things!

I first created this project back in 2018 and decided to update it with a growing understanding of Python programming as I work towards building my portfolio. I have included an [original.txt](/original.txt) file to show what the original code version looked like (In case you'd like to see how I've improved over the years).

![Korean Clock Example Image](/images/example.png)
In the image above, the first label on the clock (shown in blue) gives the current date written out in Korean in the form of: "Today, year, month, day, day of the week, is." Translated to English this reads something like: "Today is, day of the week, month, day, year."

Underneath of the blue bar on white is a question that reads, "몇 시예요?" or "What time is it?"

Further down in large black text is an actively changing time label displayed for the purpose of reading aloud. For example: "오후 네시 사분" displays the time of 4:04 PM, the time that I was writing this README file!

A short language lesson and explanation of the display formatting:

- For all times before the half hour mark, the display reads in the format: "Time of day, hour, minutes."
- For those times after the half hour mark, they read as: "Time of day, minutes before next hour."
  - Example: Rather than saying that it's "3:45" you could say it's "15 minutes to/before 4:00."
- Those times falling directly on the hour are displayed as "Time of day, hour, o'clock."
- Those times falling at the exact half hour point are written in a shorthand form using the word '반' to indicate 30 minutes rather than writing out the full word for the number 30 followed by the word for minutes.

The final label at the bottom of the clock indicates the seconds counter.

## About The '[clock.py](/clock.py)' File:

When run from the terminal this file creates the clock object using a Tkinter interface, pulls from the local time for labels, and formats a datetime object to be properly displayed in Korean. It contains the following functions:

- ### `get_time_in_korean(dt)`:

  This function takes a datetime object in as input and extracts the time portion of it. It then converts that time to an equivalent string written in Korean using a local dictionary for hours and a call to my [koreanNumbers.py](/koreanNumbers.py) file for the minutes. **In Korean, there are two number systems. These consist of Native Korean numbers and Sino-Korean numbers. Hours use the Native Korean system where as minutes use the Sino-Korean system**. The time is formatted as described above and is returned as a string to be used later on as a label on the clock.

- ### `get_date_in_korean(dt)`:

  This function also takes a datetime object but instead extracts the date portion of it. It converts the day of the week using a local dictionary and converts the year, month, and day using the same [koreanNumbers.py](/koreanNumbers.py) call from earlier.

- ### `display(curr=" ")`:

  This function gets the current local time as a datetime object and makes use of the above functions, recursively updating the clock display as needed.

The remainder of the file then creates and configures the look and feel of the clock interface when run from the terminal.

If imported, assuming you are within the same working directory, these functions can be used to make conversions from another file as shown in the following example:

![Code Sample Describing How to Use clock.py as Import](/images/code_sample_2.png)

When this code is run, it results in the following output:

![Output of Previously Described Code Sample](/images/output.png)

## About The '[koreanNumbers.py](/koreanNumbers.py)' File:

This file takes a number between 0 and 9999 and converts it to the Sino-Korean spoken equivalent of that number. A class object is created for each new number. Additionally, if desired the koreanNumbers.py file can be called in the terminal with an added number argument. As long as this number is within the specified range, the Korean translation will be printed to the terminal if supported (Shown Below).

![Terminal Call Example](/images/terminal.png)

This file includes the following class:

- ### `class KoreanNumber()`:

  This class sets a number in the constructor based on the value that was passed to it. Within this class is a `_convert_to_sino( )` function that contains the nested functions for `_get_units_place(num)`, `_get_tens_place(num)`, `_get_hundreds_place(num)`, and `_get_thousands_place(num)`.

- ### `_convert_to_sino()`:

  This internal function makes use of a dictionary to define the key components of a Sino-Korean number with definitions for numbers 0 - 10, 100, and 1000. These values are all that is needed to construct any number from 0 to 9999. Depending on the length of the number being converted, a call to one of the following internal functions is made and a string representation of that number in Korean is returned.

- `_get_units_place(num)`:
  This nested internal function takes the value located within the final digit of a number and returns its string equivalent.

- `_get_tens_place(num)`:
  This nested internal function handles the return of string values for numbers corresponding to the 10s place digit.

- `_get_hundreds_place(num)`:
  This nested internal function handles the return of string values for numbers corresponding to the 100s place digit, trickling down into the 10s or final digit places if necessary and making calls to each's corresponding function.

- `_get_thousands_place(num)`:
  This nested internal function handles the return of string values for numbers corresponding to the 1000s place digit, trickling down into the 100s, 10s, or final digit places if necessary and making calls to each's corresponding function.

## Technologies Used and Challenges Faced:

With the addition of match:case to Python 3.10+ I wanted to try out this feature for myself. I've only recently started exploring other languages in depth and was pleased to see that upon updating my current version of Python, I could also make use of this capability. I decided to add a match:case in [koreanNumbers.py](/koreanNumbers.py) as a substitute for multiple if/ifelse statements. (Shown Below)

![Example Code Image](/images/code_sample_1.png)

I hadn't had much experience working with datetime objects and wanted to gain some exposure to this area of Python as well. In my latest version of this project, I make use of datetime objects instead of using the 'time' import with slicing.

I also wanted to explore object-oriented programming more which is why I opted to create the KoreanNumbers class rather than regular function definitions.

I've made use of the '`os`' import to properly create a path that can be used on both Windows and Mac; something I have learned to use recently as a best practice for compatibility.

My original code for this project made the mistake of repeating and hardcoding. I think I have now made a valid attempt at remedying this. Rather than creating a dictionary in multiple locations for numbers between 0 and 60 for minutes, and 1-12 for hours, I have created the [koreanNumbers.py](/koreanNumbers.py) class to handle all number building needs. Conveniently, this can also be used for year numbers, month numbers, day numbers, and seconds. My previous version of the Korean Phrase Clock would break every year. I would then be forced to go in and add a new year to my code's dictionaries if I wanted to keep using it. This was not ideal. My new implementation has solved this issue. As an added bonus anyone that has the file can import it for use in their projects or call it from the terminal!

I have decided to make use of f'strings rather than '`+`' string concatenation when building my string returns as I believe this to be a more efficient method of joining strings together in Python.

I have noticed that some terminal windows are not configured by default to display UTF-8 characters including those from the Korean language. This would be an issue if someone was attempting to call the [koreanNumbers.py](/koreanNumbers.py) file from the terminal with an additional number argument. I believe the fix is related to how the user sets up their terminal environment rather than a coding issue.

One final comment, I have made a few little fun uses of the '`%`' operator throughout my code which was something I knew was possible in the past but is much cleaner than how I would have previously solved a problem back in 2018. Cool, math!

## How To Run:

First make sure you are using [Python](https://www.python.org/downloads/) version 3.10 or later otherwise the code wil break when attempting to perform a match:case operation.

Next make sure you have both PIL and Tkinter installed. If you do not have these installed, you will need to do so via pip. This should look something like:

- `python3 -m pip install --upgrade pip`
- `python3 -m pip install Pillow`
- `python3 -m pip install tk`

Finally, download the accompanying files and images folder. Then, in the terminal navigate to the project file and type either `python clock.py` (python3 for Mac) to get the clock up and running. Or to try out the stand alone number converter type: `python koreanNumbers.py number` where number is any whole number value between 1 and 9999 (including 0). If you are in the same working directory, you can also `import clock` or `import koreanNumbers` to utilize each in a new file as described above.

## Final Comments:

While I've been studying the Korean language through various sources for the past few years now, I'm still no expert. If you notice any errors in my work in this regard, please feel free to contact me and let me know what changes I can include to better represent the time using the Korean language.

I had a lot of fun re-making this project and updating it to reflect my current understanding of the Python programming language. Thanks for visiting my portfolio and I hope you get some enjoyment out of this project too!

## Credits:

Line's containing: `len("%i" % i)` in [koreanNumbers.py](/koreanNumbers.py) taken from suggestion in [this](https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer) thread:

Singling out specific digits described [here](https://stackoverflow.com/questions/32752750/how-to-find-the-numbers-in-the-thousands-hundreds-tens-and-ones-place-in-pyth)

Interested in learning more about Korean? I have used [Talk to Me in Korean](https://talktomeinkorean.com/) as one of my primary resources for learning the language!
