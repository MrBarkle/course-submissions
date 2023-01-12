import os
import tkinter as tk
from tkinter import Button, Label, Toplevel
from PIL import Image, ImageTk
import time
import json

'''
    Desktop Applications Organizer - Inventory Bags
    In the theme of The Lord of the Rings Online MMORPG

    :author:        Brandon Barkle <linkedin.com/in/brandonbarkle>
    :date:          1/11/2023

    :description:   This application uses a JSON file to read in applications to
                    store as slots within an inventory bag GUI. The root of this
                    GUI is a mock Windows 10 taskbar. Pressing 'i' while in
                    focus of the taskbar or an inventory bag will open or close
                    the remaining bags. As of now, populate the JSON file for
                    your own personal configuration. Be sure to update the
                    attribute 'contentList' which should contain integer values
                    1-15 depending on which slots you choose to fill. To close
                    the application, click the button located to the right end
                    of the taskbar. See README for more details.

'''


class Content:
    '''
    A Class to hold shared configuration data that can be passed to the taskbar
    object as well as bag objects upon creation.

    '''
    _shared_config_data = None

    def __init__(self):
        '''
        Initialize Content object.

        '''

        # Get JSON configuration data
        self._shared_config_data = self._load_config()

    def _load_config(self, file_path='config.json'):
        '''
        Load the JSON data found in the specified file path.

        :param file_path: The location of the JSON file to load from.
        :type  file_path: str

        :returns:    JSON file contents.
        :rtype:      list

        '''
        with open(file_path) as file:
            self._shared_config_data = json.load(file)
            return self._shared_config_data


class TaskBar(Content):
    '''
    A Class to create a TaskBar object from root. This Class inherits from the
    Content class with the Singleton design pattern in mind. The data stored in
    Content will be used within the TaskBar class to set variables.

    '''

    def __init__(self, root, geometry):
        '''
        Initialize TaskBar object.

        :param root: The root window.
        :type  root: tkinter.Tk

        :param geometry: The window geometry for the TaskBar object.
        :type  geometry: str

        '''
        Content.__init__(self)
        self.root = root
        self.geometry = geometry

        # Configure object
        self._configureObject()

        # Create window on top of root
        self.top = Label(root)

        # Add close button to taskbar
        self.close = Button(self.top, command=lambda: root.destroy(),
                            bg='#262626', activebackground='#262626', bd=0)

        # Create Bags
        self._createBags()

        # Add bag buttons to taskbar for each bag
        self.b1 = TaskbarBagButton(self.top, 1, self.bags[0].window)
        self.b2 = TaskbarBagButton(self.top, 2, self.bags[1].window)
        self.b3 = TaskbarBagButton(self.top, 3, self.bags[2].window)
        self.b4 = TaskbarBagButton(self.top, 4, self.bags[3].window)
        self.b5 = TaskbarBagButton(self.top, 5, self.bags[4].window)
        self.b6 = TaskbarBagButton(self.top, 6, self.bags[5].window)

        # Stylize the taskbar
        self._stylize()

    def _configureObject(self):
        '''
        Configure the TaskBar object for placement on the screen
        as well as setting attributes and key bindings.

        '''
        self.root.geometry(self.geometry)
        self.root.overrideredirect(True)
        self.root.attributes('-transparentcolor', 'red')
        self.root.bind('<Key>', self.keyPress)
        self.bags = list()

    def _stylize(self):
        '''
        Set the style of the TaskBar object.

        '''

        # Define and set taskbar image
        taskbar_image = Image.open(os.path.join('images', 'taskbar.png'))
        taskbar_set = ImageTk.PhotoImage(taskbar_image)

        # Define and set close taskbar button image
        close_image = Image.open(os.path.join('images', 'Close_taskbar.png'))
        close_set = ImageTk.PhotoImage(close_image)

        # Configure images
        self.top.config(image=taskbar_set)
        self.top.image = taskbar_set
        self.close.config(image=close_set)
        self.close.image = close_set

        # Pack items onto parent window
        self.top.pack(fill='both', expand=1)
        self.close.place(x=1912, y=-2)

    def _createBags(self):
        '''
        Create the Bag objects to be associated with each bag button on the
        TaskBar object. Use inherited contents of JSON file data to set 
        attributes of each bag.

        '''

        # Create bags
        bag_1 = Bag(1, self._shared_config_data[0][0]['bag_geometry'])
        self.bags.append(bag_1)
        bag_2 = Bag(2, self._shared_config_data[1][0]['bag_geometry'])
        self.bags.append(bag_2)
        bag_3 = Bag(3, self._shared_config_data[2][0]['bag_geometry'])
        self.bags.append(bag_3)
        bag_4 = Bag(4, self._shared_config_data[3][0]['bag_geometry'])
        self.bags.append(bag_4)
        bag_5 = Bag(5, self._shared_config_data[4][0]['bag_geometry'])
        self.bags.append(bag_5)
        bag_6 = Bag(6, self._shared_config_data[5][0]['bag_geometry'])
        self.bags.append(bag_6)

    def keyPress(self, event):
        '''
        Create a key press listener that updates the TaskBar object's bag
        buttons when the 'i' key is pressed.

        :param event: The key press event to listen for (i).
        :type  event: tkinter.Event

        '''

        # When 'i' is pressed
        if (event.char == 'i'):
            # If bags change to hidden, update taskbar
            if all([b.window.state() == 'normal' for b in self.bags]):
                self.b1.updateTaskbar(self.bags[0].window, False)
                self.b2.updateTaskbar(self.bags[1].window, False)
                self.b3.updateTaskbar(self.bags[2].window, False)
                self.b4.updateTaskbar(self.bags[3].window, False)
                self.b5.updateTaskbar(self.bags[4].window, False)
                self.b6.updateTaskbar(self.bags[5].window, False)
            # If bags change to visible, update taskbar
            else:
                self.b1.updateTaskbar(self.bags[0].window, True)
                self.b2.updateTaskbar(self.bags[1].window, True)
                self.b3.updateTaskbar(self.bags[2].window, True)
                self.b4.updateTaskbar(self.bags[3].window, True)
                self.b5.updateTaskbar(self.bags[4].window, True)
                self.b6.updateTaskbar(self.bags[5].window, True)


class TaskbarBagButton:
    '''
    A Class to handle the create of bag buttons on the TaskBar object as well
    as the updating of said buttons upon opening and closing of their associated
    Bag objects.

    '''

    def __init__(self, parent, number, bag):
        '''
        Initialize the TaskbarButton objects.

        :param parent: The TaskBar root Label.
        :type  parent: tkinter.Label

        :param number: The associated bag number.
        :type  number: int

        :param bag: The Bag object's window.
        :type  bag: tkinter.Toplevel

        '''
        self.parent = parent
        self.number = number
        self.bag = bag

        # Initialize taskbar bag button
        self.button = Button(self.parent, bg='#262626',
                             activebackground='#262626', bd=0)
        self.button_open_set = None  # Initialize opened bag button image
        self.button_set = None  # Initialize closed bag button image

        # Stylize bag button
        self._stylize()

    def _stylize(self):
        '''
        Set the style of the TaskbarBagButton objects.

        '''

        # Define closed button image
        button_image = Image.open(os.path.join('images',
                                               f'taskbag{self.number}.png'))
        self.button_set = ImageTk.PhotoImage(button_image)

        # Define opened button image
        button_open_image = Image.open(
            os.path.join('images', f'taskbag{self.number}op.png'))
        self.button_open_set = ImageTk.PhotoImage(button_open_image)

        # Configure button image and set function
        self.button.config(image=self.button_set, command=lambda:
                           self._toggleBag(self.bag))
        self.button.image = self.button_set

        # Pack button
        if self.number == 6:
            self.button.place(x=50, y=8)
        elif self.number == 5:
            self.button.place(x=100, y=4)
        elif self.number == 4:
            self.button.place(x=150, y=8)
        elif self.number == 3:
            self.button.place(x=200, y=4)
        elif self.number == 2:
            self.button.place(x=250, y=8)
        elif self.number == 1:
            self.button.place(x=300, y=4)

    def _toggleBag(self, window):
        '''
        Toggle tha Bag object's window state to opened or closed

        :param window: The Bag object's window.
        :type  window: tkinter.Toplevel

        '''

        # Update taskbar to closed bag state
        if window.state() == 'normal':
            self.updateTaskbar(window, False)
        # Update taskbar to opened bag state
        else:
            self.updateTaskbar(window, True)

    def updateTaskbar(self, window, boolean):
        '''
        Update the TaskBar object's buttons to display the image for both opened
        and close bags depending on the Bag object's window state.

        :param window: The Bag object's window.
        :type  window: tkinter.Toplevel

        :param boolean: Indication of whether or not the window is open.
        :type  boolean:  Boolean 

        '''

        # Get the window name
        name = str(window)

        # Show closed bag images
        if not boolean:
            match name:
                case ('.!toplevel' | '.!toplevel2' | '.!toplevel3' |
                      '.!toplevel4' | '.!toplevel5' | '.!toplevel6'):
                    self.button.config(image=self.button_set)
                    self.button.image = self.button_set
            window.withdraw()
        # Show opened bag images
        else:
            match name:
                case ('.!toplevel' | '.!toplevel2' | '.!toplevel3' |
                      '.!toplevel4' | '.!toplevel5' | '.!toplevel6'):
                    self.button.config(image=self.button_open_set)
                    self.button.image = self.button_open_set
            window.update(), window.deiconify()


class Bag(Content):
    '''
    A Class to create a Bag object. This Class inherits from the
    Content class with the Singleton design pattern in mind. The data stored in
    Content will be used within the Bag class to set variables.

    '''

    def __init__(self, number, geometry):
        '''
        Initialize the Bag object. 

        :param number: The bag's number (1-6).
        :type  number: int

        :param geometry: The Bag object's window geometry.
        :type  geometry: str

        '''
        Content.__init__(self)
        self.number = number
        self.geometry = geometry

        # Create bag widget instance
        self.window = Toplevel()
        self.top = Label(self.window, bg='red')

        # Configure object
        self._configureObject()

        # Stylize the bag window
        self._stylize()

        # Load slot data for this bag
        self._loadSlots()

    def _loadSlots(self):
        '''
        Load slot data from inherited JSON file contents if it exists for each
        slot to be created for this Bag object.

        '''

        # Check if bag being created has content to load
        if self._shared_config_data[self.number - 1][0]['hasContent']:
            # For slots that have content in them
            for slot in self._shared_config_data[self.number - 1][0]['contentList']:
                # Get geometry of slot
                x, y = self._shared_config_data[self.number -
                                                1][slot]['geometry']
                title = self._shared_config_data[self.number -
                                                 1][slot]['title']
                desc = self._shared_config_data[self.number -
                                                1][slot]['description']
                image = self._shared_config_data[self.number -
                                                 1][slot]['image']
                path = self._shared_config_data[self.number -
                                                1][slot]['target_path']
                # Create the slot
                CreateSlot(self.window, slot, x, y, title, desc, image, path)

    def _configureObject(self):
        '''
        Configure the Bag object for placement on the screen
        as well as setting attributes and key bindings.

        '''

        # Configure bag window
        self.window.geometry(self.geometry)
        self.window.overrideredirect(True)
        self.window.attributes('-transparentcolor', 'red')
        self.window.bind('<Key>', lambda event: task_bar.keyPress(event))
        self.window.withdraw()

        # Make bag draggable
        self.top.bind('<ButtonPress-1>', self._startMove)
        self.top.bind('<ButtonRelease-1>', self._stopMove)
        self.top.bind('<B1-Motion>', self._onMotion)
        self.window.overrideredirect(True)

    def _onMotion(self, event):
        '''
        Define what to do when the Bag object is in motion.

        :param event: The window in motion event.
        :type  event: tkinter.Event

        '''
        x = (event.x_root - self.x - self.top.winfo_rootx() +
             self.top.winfo_rootx())
        y = (event.y_root - self.y - self.top.winfo_rooty() +
             self.top.winfo_rooty())
        self.window.geometry(f'+{x}+{y}')

    def _startMove(self, event):
        '''
        Define what to do when the Bag object starts to move.

        :param event: Event for when the window starts to move.
        :type event: tkinter.Event

        '''
        self.x = event.x
        self.y = event.y

    def _stopMove(self, e):
        '''
        Define what to do when the Bag object stops moving.

        :param e: A caught placeholder event, this isn't used.
        :type  e: tkinter.Event

        '''
        self.x = None
        self.y = None

    def _stylize(self):
        '''
        Set the style of the Bag object
        '''

        # Add close button to bag being created
        if self.number == 1:
            # Create close button when bag 1 is being created
            close = Button(self.top, command=lambda: task_bar.b1.updateTaskbar(
                self.window, False), bg='grey6', activebackground='grey6', bd=0)
        elif self.number == 2:
            # Create close button when bag 2 is being created
            close = Button(self.top, command=lambda: task_bar.b2.updateTaskbar(
                self.window, False), bg='grey6', activebackground='grey6', bd=0)
        elif self.number == 3:
            # Create close button when bag 3 is being created
            close = Button(self.top, command=lambda: task_bar.b3.updateTaskbar(
                self.window, False), bg='grey6', activebackground='grey6', bd=0)
        elif self.number == 4:
            # Create close button when bag 4 is being created
            close = Button(self.top, command=lambda: task_bar.b4.updateTaskbar(
                self.window, False), bg='grey6', activebackground='grey6', bd=0)
        elif self.number == 5:
            # Create close button when bag 5 is being created
            close = Button(self.top, command=lambda: task_bar.b5.updateTaskbar(
                self.window, False), bg='grey6', activebackground='grey6', bd=0)
        elif self.number == 6:
            # Create close button when bag 6 is being created
            close = Button(self.top, command=lambda: task_bar.b6.updateTaskbar(
                self.window, False), bg='grey6', activebackground='grey6', bd=0)

        # Define images
        top_image = Image.open(os.path.join('images',
                                            f'Bag{self.number}.png'))
        top_set = ImageTk.PhotoImage(top_image)
        x_image = Image.open(os.path.join('images',
                                          f'Close_bag.png'))
        x_set = ImageTk.PhotoImage(x_image)

        # Configure images
        self.top.config(image=top_set)
        self.top.image = top_set
        close.config(image=x_set)
        close.image = x_set

        # Pack images
        self.top.pack(fill='both', expand=1)
        close.place(x=170, y=20)


class CreateSlot:
    '''
    A Class to handle the slot creation within each Bag object

    '''

    def __init__(self, parent_bag, slot_number, x, y, title, desc, image, path):
        '''
        Initialize a slot.

        :param parent_bag: The Bag this slot is associated with.
        :type  parent_bag: tkinter.Toplevel

        :param slot_number: The number for this slot (1-15).
        :type  slot_number: int

        :param x: The geometry x coordinate.
        :type  x: int

        :param y: The geometry y coordinate.
        :type  y: int

        :param title: The app to slot's title.
        :type  title: str

        :param desc: The app to slot's description.
        :type  desc: str

        :param image: The app to slot's image file name.
        :type  image: str

        :param path: The full path location to the app.
        :type  path: str

        '''
        self.parent_bag = parent_bag
        self.slot_number = slot_number
        self.x = x
        self.y = y
        self.title = title
        self.desc = desc
        self.image = image
        self.path = path

        # Create slot button
        self.slot = Button(self.parent_bag,
                           command=lambda: self._openFile(path),
                           bg='grey6', activebackground='grey6', bd=0,
                           height=29, width=29)

        # Stylize the slot button
        self._stylize()

    def _stylize(self):
        '''
        Set the style of the defined slots within a Bag object.

        '''

        # Define a slot image
        slot_image = Image.open(
            os.path.join('program icons', f'{self.image}'))
        slot_set = ImageTk.PhotoImage(slot_image)

        # Set slot image
        self.slot.config(image=slot_set)
        self.slot.image = slot_set

        # Pack slot image using placement variables
        self.slot.place(x=self.x, y=self.y)

        # Add tooltip
        self.tooltip = ToolTip(self.slot, slot_set,
                               desc=self.desc,
                               title=self.title)

    def _openFile(self, path):
        '''
        Open a file.

        :param path: A file path to open.
        :type  path: str

        '''
        try:
            # Open item at path
            os.startfile(path)

        # Upon error, print a message, but don't kill the program
        except FileNotFoundError as e:
            print(e)


class ToolTip:
    '''
    A Class to handle the creation of tooltips associated with filled slots in
    each Bag object.

    '''

    def __init__(self, parent_slot, image, desc, title):
        '''
        Initialize the ToolTip object.

        :param parent_slot: The slot associated with this ToolTip object.
        :type  parent_slot: tkinter.Button

        :param image: The file name of the image to place on the ToolTip object.
        :type  image: str

        :param desc: A description of the app to place on the Tooltip.
        :type  desc: str

        :param title: The title of the app to place on the ToolTip.
        :type  title: str

        '''
        self.parent_slot = parent_slot
        self.image = image
        self.desc = desc
        self.title = title

        # Set action result
        self.parent_slot.bind('<Enter>', self._onEnter)
        self.parent_slot.bind('<Leave>', self._onLeave)

    def _configureObject(self):
        '''
        Configure the ToolTip object for placement on the screen
        as well as setting attributes.

        '''

        # Configure tooltip location and attributes
        loc_x, loc_y = self.parent_slot.winfo_pointerxy()
        self.tooltip.attributes('-topmost', True)
        if (loc_x - 150) > 0:
            self.tooltip.geometry(f'+{loc_x - 155}+{loc_y + 20}')
        else:
            self.tooltip.geometry(f'+{loc_x + 15}+{loc_y + 20}')
        self.tooltip.overrideredirect(True)
        self.tooltip.attributes('-alpha', 0.8)

    def _onEnter(self, e):
        '''
        Create the tooltip window.

        :param e: A caught placeholder event, this isn't used.
        :type  e: tkinter.Event

        '''

        # Create tooltip widget instance
        self.tooltip = Toplevel()

        # Set delay before tooltip displays
        time.sleep(0.5)

        # Create a tooltip
        self._configureObject()

        # Style the tooltip
        self._stylize()

    def _onLeave(self, e):
        '''
        Destroy the tooltip window.

        :param e: A caught placeholder event, this isn't used.
        :type  e: tkinter.Event

        '''
        # Destroy tooltip if not hovering over button
        self.tooltip.destroy()

    def _stylize(self):
        '''
        Set the style of the ToolTip object.

        '''

        # Add labels to tooltip
        background = Label(self.tooltip, bg='#050c12', bd=2, relief='ridge')
        background.pack(fill='both', expand=1)

        header = Label(background, text=self.title, font=('Trajan Pro', 11),
                       wraplength=150, justify='left', bg='#050c12',
                       fg='#c8c9a9')
        tooltip_image = Label(background, image=self.image, bg='#050c12')
        description = Label(background, text=self.desc, font=('Calibri', 11),
                            wraplength=150, justify='left', bg='#050c12',
                            fg='#c8c9a9')

        # Place labels
        tooltip_image.grid(row=0, column=0, stick='w')
        header.grid(row=0, column=1, stick='w', padx=5)
        description.grid(row=1, columnspan=2, stick='w')


if __name__ == '__main__':

    # Create underlying widget for taskbar
    root = tk.Tk()

    # Create taskbar using root
    task_bar = TaskBar(root, '1920x40+1920+1040')

    # Run mainloop
    root.mainloop()
