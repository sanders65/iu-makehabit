# Make it a Habit

**An easy-to-use app designed to help you track 
your daily and weekly tasks, empowering you
to establish and maintain good habits in your life.**

I created this portfolio project as part of the 
*"Object Oriented and Functional Programming"* course at IU Academy.

***
## What is it?

With „Make it a Habit“ you can effectively track habits 
that you want to improve upon regularly. 
It works in an easy-to-use and simply-to-manage interface. 

### Key Features:
- **Create multiple habits:** Each habit can be
assigned a periodicity: daily or weekly. 
- **Check off habits:** When you complete a habit, check it off. 
Completing a habit within its defined periodicity will "raise  
your streak", reflecting your success in building positive habits.
- **Track your progress:**  If a habit isn't checked off within its
periodicity, you **„break the streak“**, your streak will reset.
- **Analyze your habits:**: Gain insights into your progress 
by viewing e.g. all your habits or your longest streak. 
- **Delete habits:**: Easily remove habits you no longer wish to track.

***
## Installation
To run the app, first install all required dependencies:

```pip install -r requirements.txt```

***
## Usage 
Once you have downloaded all necessary files and 
installed the requirements, start the program with the
following command in your terminal:
```python main.py```

Upon starting, you'll be asked whether you want to load example habit data. 
Choose **"n"** for "No" to enter your own habits. 
You can then add, check off, edit or analyze your habits. 
When you're finished, exit the program by selecting "Exit" in the main menu.

If you prefer to explore predefined data, select **"y"** for "Yes". 
For more details on this testing routine, see "Tests" section below.

***
## Tests
To run the tests, ensure you have pytest installed, 
then execute:
```pytest .```

**Predefined example habits and tracking data** are available in the CLI. 
Start the program using ```python main.py```  
When prompted, select **"y"** for "Yes" to load the example data and continue 
using the app with the predefined habits.

**Important Note:**
After loading the example habits and tracking data, 
if you exit the program, you must delete the example.db 
file from your directory before restarting the program 
to load the example data again. If you do not delete this 
file, the program will insert the example data into 
example.db again, leading to duplicate entries, 
which we want to avoid.

***
## Acknowledgment
As a beginner in programming, I initially doubted my ability 
to complete a project of this scale.  
However, in the end I finally made it work (at least I think so). 
Cheers to that! 