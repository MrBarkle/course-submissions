# ![Lotro Ring Icon](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/ring.png) Desktop Applications Organizer - Inventory Bags

#### Created By: [Brandon Barkle](https://www.linkedin.com/in/brandonbarkle)

## Project Description:

This project uses Python's Tkinter toolkit and object-oriented programming to to create a desktop application organizer in the theme of inventory bags found in the MMORPG [The Lord of the Rings Online](https://www.lotro.com/home) (Lotro). I created this project back in 2018 after my retirement from Lotro as an homage to the 10 years I spent as part of a vast community of gamers exploring middle-earth. 

Rather than placing icons for files and executables within the desktop environment, this project keeps these items hidden until the `'i'` key is pressed, at which point 6 bags with 90 available inventory slots appear containing any items placed within. From inside of a bag the user can hover over an item to reveal a tooltip description of the associated file or program and then click on the accompanying icon to run it.

The project file is saved as a .pyw rather than a .py so that it can mimic an executable without the addition of a terminal window or third-party applications. In this way, the terminal window is suppressed and hidden from view. When in focus, it takes on the following appearance:

![Project application in action](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/example.png)

Figure 1: Above is an example of the project program in action on my desktop.

![Inventory bags as seen in the game Lotro](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/screenshot.jpg)

Figure 2: Here is what inventory bags looked like as part of the Lotro UI.

Instead of having in game items, I have mimiced the look and feel of inventory bags to be used with computer applications instead.

Additionally this is meant to be run with two screens as a second mock Windows 10 taskbar has been created as the root window for the project. The mock taskbar then sits on the base of the second screen and holds 6 icons representing each bag. The `'i'` key press is only listened for when this taskbar or a bag is in top focus.

![The taskbar GUI for this project](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/example2.png)

Figure 3: This is what the completed taskbar looks like with all bags closed. 

![Screenshot of Lotro taskbar bags](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/images/screenshot2.jpg)

Figure 4: And again but in game. 

I wanted there to be a blend between Windows 10 and the ingame version itself.

## About the '[config.json](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/config.json)' File:

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
        
In the `.json` file, the user will have to fill out each "slot" with information related to the executable they want to add to the specified slot. Two things to note here: 
1. If a new bag is being filled out, make sure to set `"hasContent":true` from the default false.
2. If a new slot is being added, make sure to add the slot number to the `"contentList":[1, 2, 3, ...]` list.

Bag Geometries within the `.json` file should not be changed, however, if comfortable, experimenting with the slot `geometry` lists may help with positioning issues of images. 

## About the '[bags.pyw](https://github.com/brandonbarkle/portfolio/blob/main/Desktop%20Application%20Organizer/bags.pyw)' File:

When run, this file builds a fake Windows 10 taskbar window GUI (defaulted to the bottom of a second screen). This taskbar contains 7 buttons, 6 for bags located on the left-hand side, and 1 for an end program button located on the far right side. Additionally 6 bags are loaded up and configured to the user's specifications which can be found within the accompanied `.json` file located within the same directory. 

- ### `class Content()`:
  This class is used to hold shared configuration data from the `.json` file that can be passed to the TaskBar class object as well as Bag class objects upon creation.   It contains the following internal method: `_load_config()` and has no class level parameters.

  - ### `_load_config(file_path)`:
    This method loads the config.json file and returns a list representing the json data.
 
- ### `class TaskBar(Content)`:
  This class is used to create the root window of the project GUI as the taskbar. This Class inherits from the Content class with the Singleton design pattern in mind. The data stored in Content will be used within the TaskBar class to set variables. It takes in the parameters `root` and `geometry` to represent the root window and geometry of the taskbar window respectively. This class contains the following internal methods `_configureObject()`, `_stylize()`, `_createBags()` and a regular method called `keyPress()` that will be called from another class later on. 
  
    - ### `_configureObject()`:
      This method is responsible for configuring the TaskBar object for placement on the screen as well as setting attributes and key bindings.
      
    - ### `_stylize()`:
      This method sets the style of the TaskBar object. 
    
    - ### `_createBags()`:
      This method creates 6 Bag objects to be associated with each bag button located on the TaskBar object. Attributes are set with inherited data from the Contents   class. 
    
    - ### `keyPress(event)`:
      This method is called as a result of key press on either the taskbar or a bag. If the key pressed is `'i'`, the taskbar icons will change image accordingly. 
      
- ### `class TaskbarBagButton()`:
  This class handles the creation of bag buttons on the TaskBar object as well as being responsible for the updating of said buttons upon opening and closing of their associated Bag objects. It takes the parameters `parent` representing the Label object created from root, `number` for the bag number, and `bag` which is the actual Bag object's window. This class contains the following internal methods `_stylize()`, `_toggleBag()`, and a regular method called `updateTaskbar()` that will be called from another class later on. 
  
    - ### `_stylize()`:
      This method sets the style of the TaskbarBagButton objects.
      
    - ### `_toggleBag(window)`:
      This method calls updateTaskbar on a window to toggle it's appearance on or off. 
    
    - ### `updateTaskbar()`:
      This method swaps the image of the TaskbarBagButtons to represent either an open or closed bag in the same fashion as inventory bags in Lotro. A white ring around a bag icon means that the bag is currently open. 
      
- ### `class Bag(Content)`:
  The Bag class is used to create an instance of a Bag object. This class inherits from the Content class with the Singleton design pattern in mind. The data stored in Content will be used within the Bag class to set variables. This class has the parameters `number` and `geometry` to represent the bag's number (1-6) and the geometry of the Bag object's window respectively. 
  
    - ### `_loadSlots()`:
      Load slot checks the data passed over from Content to determine if there are any slots within the bag that have been previously defined by the user. If there is data to pull from, this method will loop over only those with content and extract and set the required information to pass along. 
    
    - ### `_configureObject()`:
      This method is responsible for configuring the Bag object for placement on the screen as well as setting attributes, key bindings, and motion binds.
    
    - ### `_onMotion(event)`:
      This method defines what to do when the Bag object is in motion.
    
    - ### `_startMove(event)`:
      This method defines what to do when the Bag object starts moving.
    
    - ### `_stopMove(e)`:
      This method defines what to do when the Bag object stops moving.
    
    - ### `_stylize()`:
      This method sets the style of the overall Bag object depending on its number and binds it to the updateTaskbar method for further changes.
  
- ### `class CreateSlot()`:
  The CreateSlot class is used to handle the creation of a slot within a Bag object. It takes the parameters, `parent_bag` for the baf in which the slot is being created, `slot_number` which is a value between 1 and 15, `x` and `y` for the slot's location within its parent Bag, and finally `title`, `desc`, `image` and `path` to define and describe the file or program being placed within the slot. It contains the following methods: `_stylize()`, and `_openFile()`.

    - ### `_stylize()`:
      This method sets the slot's style attributes and creates and instance of a `ToolTip()` class object. 
    
    - ### `_openFile(path)`:
      This method is used to open a file given its path. If the file is not found, the error is handled and a message is printed behind the scenes to the terminal window. 
  
- ### `class Tooltip()`:
  Finally, there is the ToolTip class. This class handles the creation of tooltips associated with filled slots in each Bag object. It contains the parameters `parent_slot` for the slot that it is associated with, `image` for the image to be placed on the tooltip, `desc` for the description input into the `.json` file by the user for this specific slot contents, and `title` for the name of the program or file. It contains the internal methods `_configureObject()`, `_onEnter()`, `_onLeave()`, and `_stylize()`.
  
    - ### `_configureObject()`:
      This method is responsible for configuring the Tooltip object for placement on the screen as well as setting attributes.
    
    - ### `_onEnter(e)`:
      This method create the tooltip window with a `time.sleep(0.5)` setting to mimic the halted appearance of a tooltip just like in Lotro.
    
    - ### `_onLeave(e)`:
      This method is responsible for destroying the tooltip window. 
    
    - ### `_stylize()`:
      This method sets the style of the tooltip.
  
## Technologies Used and Challenges Faced:

The core of this project was created using the Tkinter toolkit in Python. It handles the overall GUI for the project in conjunction with specially crafted image files to look and function just like Lotro's inventory bags. This was my first time using JSON but I think it worked will for my purposes here. As described above, this file is used to pass predefined information from the user to the project. 

I recall initially having challenges when writing this for the first time back in 2018 in that I knew what I wanted the project to look like and mostly how I wanted it to function, but I had no prior experience creating something this intricate with Tkinter. The original result was can be seen in the `original.txt` file was a mess of google search results and lesser python knowledge. This leads me to my most recent challenge which was untangling the mess of my past self to create a more streamlined design. While its im sure by no means perfect and I am still learning more about design patterns and principles, It is now much clearer to read and understand and the code has been reduced from  1170 lines to only 692. I consider this to be a huge win. 

Another big issue I had faced when first starting this project was determining how I wanted to access the files. With my then limited understanding I opted for simply hard-coding in my own configuration. The second time around I wanted to make this project accessible to others so I eventually used JSON to pass in information from the user. 

## Future Changes and Updates:

In future updates to this project I would like to find a way to allow the user to either drag a program file directly onto a bag window from the desktop or for them to click an empty slot in order to add a program to it. This would be more convenient. Rather than having to pre-fill out the `.json` file, it could be updated mid run. I know how to make a save method for JSON but am not yet sure how I want to implement this feature. Either way, this would make it more similar to the actual inventory bags of Lotro. In related fashion, I think removing a program from a slot should be as simple as dragging it out of the bag onto the desktop and receiving a prompt to delete or not. Next, slot contents should be able to be dragged within the bag to a new slot and the `.json` file should update to its new geometric location. If a file already exists in that spot and was not previously in the bag, it will get placed next to that slot, if available. If dragging a slot icon over another slot icon, they should swap. I think that the location of a bag should be saved after it stops moving so when the program is run again, you start off where you left them, not in the default position. In addition to this I could also easily add a way to reset to defaults. 

It might be cool to see what other inventory bags look like in other games and create swappable skins. I'd have to see what the look and feel of each of these is like as well. 

Also in terms of appearance, not everyone uses Windows 10. Added taskbar images could also increase the appearance's scope for say Mac or Linux. 

## How To Run:

First make sure you are using [Python](https://www.python.org/downloads/) version 3.10 or later otherwise the code will break when attempting to perform a match:case operation.

Next make sure you have both PIL and Tkinter installed. If you do not have these installed, you will need to do so via pip. This should look something like:

- `python3 -m pip install --upgrade pip`
- `python3 -m pip install Pillow`
- `python3 -m pip install tk`

Finally, download the accompanying files and images folder. Then, in the terminal navigate to the project file and type either `python bags.pyw` (python3 for Mac) to get the project up and running.

I recommend placing the bags.pyw file within your `Start Up` folder (if using Windows) or similar. This way, as long as you have python installed, the project GUI will appear in its designated location on the screen each time you start your computer. 

A Note on this. You may need to play around with the `TaskBar()` object's geometry within the Python file to get it located in a spot that you like. The stands for each bag's location located in the `.json` file as `'bag_geometry'`. The default setting is for the taskbar to be placed on my second 23 inch 1920x1080 screen. 

## Final Comments:

I really enjoyed making this project and hope you enjoy using it equally as much. For me it brings the nostalgia of playing Lotro to the tasks of my everyday life!  
  
## Credits:

All images adapted from my own screenshots taken while playing [The Lord of the Rings Online](https://www.lotro.com/home). 

## Youtube Video Link:

Here is a video link of the project working on my old computer.

https://youtu.be/ElN2RZxqpjw
