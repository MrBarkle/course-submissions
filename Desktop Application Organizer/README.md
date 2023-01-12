# ![Lotro Ring Icon](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/ring.png) Desktop Applications Organizer - Inventory Bags

#### Created By: [Brandon Barkle](https://www.linkedin.com/in/brandonbarkle)

## Project Description:

This project uses Python's Tkinter toolkit and object-oriented programming to to create a desktop application organizer in the theme of inventory bags found in the MMORPG [The Lord of the Rings Online](https://www.lotro.com/home) (Lotro). I created this project back in 2018 after my retirement from Lotro as an homage to the 10 years I spent as part of a vast community of gamers exploring middle-earth. 

Rather than placing icons for files and executables within the desktop environment, this project keeps these items hidden until the `'i'` key is pressed, at which point 6 bags with 90 available inventory slots appear containing any items placed within. From inside of a bag the user can hover over an item to reveal a tooltip description of the associated file or program and then click on the accompanying icon to run it.

The project file is saved as a .pyw rather than a .py so that it can mimic an executable without the addition of a terminal window or additional third-party applications. In this way, the terminal window is suppressed and hidden from view. When in focus, it takes on the following appearance:

![Project application in action](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/example.png)

Figure 1: Here is an example of the project program in action on my desktop.

![Inventory bags as seen in the game Lotro](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/screenshot.jpg)

Figure 2: Here is what inventory bags looked like as part of the Lotro UI.

Instead of having in game items, I have mimicked the look and feel of inventory bags to be used with computer applications instead.

Additionally this is meant to be run with two screens as a second mock Windows 10 taskbar has been created as the root window for the project. The mock taskbar then sits on the base of the second screen and holds 6 icons representing each bag. The `'i'` key press is only listened for when this taskbar or a bag is in top focus.

## About the 'config.json' File:

This file contains all of the information related to filling the bag slots with applications or files. The structure is as follows: 

        {
            "hasContent":true,
            "contentList":[LIST OF NUMBERS FOR EACH BAG THAT HAS ACTIVE SLOTS],
            "bag_geometry": "197x165+2200+50" 
        },
        
        {
            "bag_number": 1,
            "slot_number": 1,
            "geometry": [9, 46],
            "target_path": "PATH TO AN EXECUTABLE",
            "image": "IMAGE TO REPRESENT EXECUTABLE (32x32 PNG/JPG)",
            "title": "A TITLE",
            "description": "A DESCRIPTION"
        },
        
In the .json file, the user will have to fill out each "slot" with information related to the executable they want to add to the specified slot. Two things to note here: 
1. If a new bag is being filled out, make sure to set `"hasContent":true"` from the default false.
2. If a new slot is being added, make sure to add the slot number to the `"contentList":[1, 2, 3, ...]` list.

Bag Geometries within the .json file should not be changed, however, if comfortable, experimenting with the slot geometry lists may help with positioning issues of images. 

## About the 'bags.pyw' File:

When run, this file builds a fake Windows 10 taskbar window GUI (defaulted to the bottom of a second screen). This taskbar contains 7 buttons, 6 for bags located on the left-hand side, and 1 for an end program button located on the far right side. Additionally 6 bags are loaded up and configured to the user's specifications which can be found within the accompanied `.json` file located within the same directory. 

- ### `class Content()`:
  This class is used to hold shared configuration data from the .json file that can be passed to the TaskbBar class object as well as Bag class objects upon creation.   It contains the following internal method: `_load_config()` and has no class level parameters.

  - ### `_load_config()`:
    This method loads the config.json file and returns a list representing the json data.
 
- ### `class TaskBar(Content)`:
  This class is used to create the root window of the project GUI as the taskbar. This Class inherits from the Content class with the Singleton design pattern in mind. The data stored in Content will be used within the TaskBar class to set variables. It takes in the parameters `root` and `geometry` to represent the root window and geometry of the taskbar window respectively. This class contains the following internal methods `_configureObject()`, `_stylize()`, `_createBags()` and a regular method called `keyPress()` that will be called from another class later on. 
  
    - ### `_configureObject()`:
      This method is responsible for configuring the TaskBar object for placement on the screen as well as setting attributes and key bindings.
      
    - ### `_stylize()`:
      This method sets the style of the TaskBar object. 
    
    - ### `_createBags()`:
      This method creates 6 Bag objects to be associated with each bag button located on the TaskBar object. Attributes are set with inherited data from the Contents   class. 
    
    - ### `keyPress()`:
      This method is called as a result of key press on either the taskbar or a bag. If the key pressed is `'i'`, the taskbar icons will change image accordingly. 
      
 - ### `TaskbarBagButton()`:
   TODO: In the process of filling the rest of this out. Presently it is 3:00AM! 
    - ### `_stylize()`:
    - ### `_toggleBag()`:
    - ### `updateTaskbar()`:
      
 - ### `Bag(Content)`:
    - ### `_loadSlots()`:
    - ### `_configureObject()`:
    - ### `_onMotion()`:
    - ### `_startMove()`:
    - ### `_stopMove()`:
    - ### `_stylize()`:
  
 - ### `CreateSlot()`:
    - ### `_stylize()`:
    - ### `_openFile()`:
  
 - ### `Tooltip()`:
    - ### `_configureObject()`:
    - ### `_onEnter()`:
    - ### `_onLEave()`:
    - ### `_stylize()`:
  
## Technologies Used and Challenges Faced:

## How To Run:

## Future Changes and Updates:
  
## Final Comments:
  
## Credits:

## Youtube Video Link:

Here is a video link of the project working on my old computer.

https://youtu.be/ElN2RZxqpjw
