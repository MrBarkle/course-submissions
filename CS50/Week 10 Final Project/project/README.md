# Lab Note: Electronic Laboratory Notebook

### CS50x Final Project 2021

#### Video Demo: <https://youtu.be/XiaEnIbXxRg>

#### What Was My Motivation For Creating This Project?

The motivation behind this final project was to create something that relates closely to my own personal interests. I have a background in Cheminformatics as well as an interest in scientific research and thought that creating an electronic laboratory notebook or (ELN) could be useful.

#### Why Build This Project?

This ELN was created as my final project for [CS50x](https://cs50.harvard.edu/x/2021/). The goal was to create my own piece of software that would draw upon the lessons covered in CS50x's course material; beyond that, the nature of this project was entirely up to me. The only other criteria given were to create a project that was of interest to me, would solve a problem, impact the community, or change the world. I opted to try creating something of interest that would also stand a chance at outliving the course itself.

#### What Problem Does it Solve?

With this project I wanted to try bringing the outdated carbon copy paper lab notebook to the digital sphere. You rarely seem to see other ELN's in use. With this project I was hoping to come up with a way to make an easy to use and good looking ELN that also had features that would draw the interest of its users. Although still in its early stages, I believe that this project is well on its way to becoming that new lab software tool.

#### What Did I learn?

Before creating this project, I had covered lectures in CS50x on C programming, Python, HTML/CSS/JS, and SQL. Most of these topics were refreshers on information covered while pursuing my undergraduate program however, there were also bits of new material as well as clearer explanation of the old. I was able to apply much of this information to create this software project and tie everything I had learned together. For instance, both Jinja and Flask were new to me but they were the glue needed to connect my front end HTML/CSS/JS to the back end Python and Sqlite that operate behind the scenes and makes the entire project work.

Throughout the entire project creation I continued to list different ideas on design and functionality that I wanted to include. Most of the final results are things that I had to learn along the way as I was creating the project. After much googling and looking back at course material, I was able to produce this end result.

#### What Makes This Project Stand Out?

I think this project stands out because it takes the concept of an old paper carbon copy lab notebook and puts it into the future by using current technologies. This project specifically allows the user to create not only new experiments within their lab notebook but also to create multiple notebooks organized within the same place. In addition to that, it comes with various tools that might be needed while typing up a research paper or lab experiment. This adds a level of convenience to the user experience; instead of shifting between the internet and lab notebook / text editor, many of the tools needed are all within the same software.

#### Description:

LabNote is a web application that allows the user to document experiments in an electronic laboratory notebook online utilizing a user account and databases rather than a traditional carbon copy paper notebook. After creating an account a user may start a new notebook which will hold all of their future experiments. A notebook displays in the form of a tab that one might see separating pages. This tab design was made to mimic a conventional notebook. Once created, a table of contents appears on the tab page and represents all pertinent information regarding the notebook itself as well as user profile and experiment data contained within. Once an experiment is created it will appear in the table that displays below the table of contents and can be accessed at any time. Simultaneously, the experiment editor will open and a user can begin documentation. (Don't forget to save! The auto save feature is still being worked on!). Within the experiment editor are various tools such as a periodic table and quick access guide of atomic data that can be swiftly copied for use within the document.

This project uses many different techniques to bring everything together. For simply design and ease of project creation, I decided to use Bootstrap 5.0 for a majority of its components. Prior to CS50x, I had not known of Bootstrap. It has made things much easier, and now with 5.0, I was able to use vanilla JS throughout the entire project without needing to import bulky JQuery alternatives. Additionally, I used Python's Flask web framework/Jinja web templates to send and receive data between front and back end. It also allowed for dynamic page creation and to move data between page submissions. Sqlite was used for the database which accompanied this process and HTML/CSS/JS were also used for any additional design / functions.

#### Challenges faced, Future Plans, and Known Bugs

From the time I started brainstorming this project all the way to the submission point, I kept a continuously growing list of features I wanted to include with LabNote. Some of these I either got stuck on or was unsure how to implement them, and others proved too time consuming for what they were actually worth. The following is a list of those challenges I faced along the way and any future plans I might have for LabNote.

- Creating an input mask for the phone form field within the 'Create Account' modal. The only way I could find to do this was to use JQuery or a preexisting bulky import that wasn't worth the resources used.
- If an email already exists, the page redirects with an alert, however, due to this redirect (which is required to check for duplicate emails behind the scenes after submission) the users is then required to retype all of their form fields when trying to create a new account again.
- I attempted to make the notebook tabs on the home page vertical moving down the side of the page like what you might see in a real notebook. This worked however the text on each tab appeared too pixelated for my liking.
- There is no mobile version for this web app at this time. And resizing is picky. I would like to implement this in the future and alter aspects of the design to be more web friendly.
- When too many notebook tabs are created, I would like them to collapse / hide themselves. Either this or I will simply limit the number of notebooks a user can create per account. This second option would conserve resources as well.
- Presently when deleting a notebook, the experiments that go with that notebook are deleted manually via python behind the scenes. I do believe if I re-design my sqlite tables, I can automate this cascading deletion.
- Find a way to auto save any table of contents, experiment content, or header changes while following best practices.
- Potentially put a dropdown of experiments on each notebook's tab that way the user doesn’t need to click the tab to see what is contained within each notebook
- Which ever sort method is being used should be saved for page refresh within the database and indicated on the sort button or within its dropdown
- The insert image feature on the experiment editor toolbar is not yet functional
- I had initially tried to create the impression of a new page being started each time the user made it to the bottom of the existing active page however I was unsuccessful in that on reaching the bottom, it was difficult to determine if (with random formatting) I had reached the end of the current page. Deleting a page worked perfectly as did creating a new page via the toolbar button. In the end I opted for the page to grow as the user continued to type.
- I would like to improve the experiment editor’s toolbar so that depending on the location of the cursor, the toolbar updates its active formatting and style icons. If the highlighted text is bold the toolbar should indicate that. If its centered that should be known as well.
- Strike through, superscript, and subscript should work as toggles rather than their current compounding effect they have on themselves.
- Paste button is restricted in nearly all browsers so I removed the ability to copy / paste via a button. Instead the traditional Ctrl+C and Ctrl+V work.
- I had found some really cool periodic table examples online that allowed the user to click a 'Halogen' button for example and the table would block out all but those belonging to that sub category of elements.  I would like to do this with LabNote's periodic table as well.
- The ability to save the document as a PDF was always in my initial design as this would act as the "carbon copy" for the digital version of a laboratory notebook. I ran out of time on this one, and had initially tried to split into pages to better accommodate a PDF's format.
- Another feature I wanted to have since the start was the ability to look up chemical structures and place them within the experiment document as images. Time was a factor here however I am not quite sure where to begin yet.
- When creating a table in the experiment editor, clicking within the table reveals some options to add / delete rows and columns. This toolbar should follow the table / cursor as long as it is within the table. Right now it is a little off due to removing the new page capabilities. It also does not disappear when it should and cannot distinguish between multiple tables yet.
- The select field in the create account modal displays upward rather than down when the screen size and position are a certain way. I’d prefer to force this downward at all times since it looks better.
- I'd like to give the user the option to select multiple experiments to delete at once using check boxes.
- The insert glassware button is not yet implemented. When documenting an experiment in a conventional lab notebook it is common to show which glassware and apparatuses are used. This feature would allow the user to do that digitally as well. I ran out of time on this one.
- Font color change options, weight, and highlight should come standard with this toolbar as well. Time was an issue here but these should be simple to include down the line.
- Add checkmarks or other indicators in the toolbar to know which format / styles are active
- I ran out of time on designing a profile page. It should display the user's information and have an option to delete their account and all associated data. I may place this README on the about section and the contact page doesn't need anything unless I actually deploy this web application after the course completes
- To really set this notebook apart from a paper notebook I’d like to find a way to include something like Jupyter notebooks in the experiment editor. With this the user would be able to display complex calculations and graphs as well as code if they desired. This would add way more functionality to the overall experiment documentation process. I am unsure where to begin with this one.
- When writing up an example experiment for the video, I had to copy paste the degree's symbol from a search engine rather than having it on hand. A list of symbols will be included with the editor in the future.
- Other general scientific quick reference information will be accessible from the toolbar in the future as well. Ran out of time and hadn't thought of this until too late.
- One final feature I’d like to include, which I found how to implement online, is the ability to drag and drop and image into the document. This is also how I would set up the glassware list to work but any image the user wants would also be convenient.
- Considering adding footer to login and main index.html home page that contains links to 'About Us' and 'Contact' pages so they are available other than while logged out on the welcome page.
- Changing the color of a notebook immediately changes the appearance however there are some issues with certain pieces acting properly prior to saving.
- Getting a constant error "FileNotFoundError: [Errno 2] No such file or directory: '/tmp/tmpk4j71npp/1c8f5435fa4e764c48aa652bc150a439'" behind the scenes. I don't believe this was always happening but it doesnt seem to hurt anything that I can tell. I think it has something to do with using the filesystem over cookies in application.py?


#### How to use:

When visiting the LabNote web application, the first thing the user sees is a short loading screen that leads to the welcome page. Here they will find a short description of the application along with links to an 'About Us' page, 'Contacts' and two different links which lead to the login page. From the login page, the user can either log into their account if they have an existing one with LabNote, or they may create a new account by clicking the corresponding button. After inputting some personal information to create a new account the user will be automatically logged in and redirected to the main **Home Page**. Any personal information is used to be displayed on notebook or experiment pages like with conventional lab notebooks. If it is the user's first time visiting this page, determined by not having created a notebook or experiment yet, an alert will appear pointing out the location of the 'Create Notebook' button and the 'New Experiment' button. Once a notebook has been created, the user has the option to change the color of each notebook tab by double clicking anywhere on the table of contents header. This also allows the user to edit certain notebook specific information. Be sure to click the save button on the upper left hand side of the **Edit Mode** table of contents for changes to take place. Within this **Edit Mode** the user also has the option to delete the notebook permanently and individual experiments once they have been created. Other features on this page include a 'Sort' button that will list the table of experiments according to the listed criteria. The last active notebook tab will always display first when visiting this page. That means that whichever notebook last received table of contents changes or started a new experiment will be the first to show. When the user clicks on the 'New Experiment' button, they are prompted with a few inputs for experiment specifics. Once filled out they may continue on to the **Experiment Editor** page. At this time, the new experiment is added to the notebooks table and the user is redirected. The editor page is like any other simple text editor but also includes buttons on the toolbar for a periodic table and quick reference guide for atomic data. The user will also notice that above the beginning of their document is another header type display. This includes all of the information pertaining to the experiment which was just input by the user along with the notebook that it is associated with and other profile information that may be important such as user name. Again just as with the table of contents of a notebook tab on the home page, the header of an experiment may be edited by double clicking on it. Changes made here should also be saved by clicking the 'Save' icon within the header. This differs from the other save icon located on the main toolbar in that it saves both the header and the experiment page content. (The toolbar save will not save header changes.) Now all that is left for the user to do is to begin documenting their experimental work. They will then be able to update and access it at any time by logging in a navigating to the corresponding notebook and experiment name location.

#### Credits:

Flask basic usage as well as underlying apology.html, layout.html, helpers.py, and application.py structure [from CS50x pset9 and others](https://cs50.harvard.edu/x/2021/psets/9/finance/).

Overall design and components mostly from [bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

Login page design based on [GitHub's](https://github.com/) login page.

Many icons either from bootstrap or [fontawesome](https://fontawesome.com/v5.15/icons?d=gallery&p=2) This includes Logo microscope icon.

List of states in account creation modal found [here](https://www.freeformatter.com/usa-state-list-html-select.html).

Loading screen adapted from [this post](https://ihatetomatoes.net/create-custom-preloading-screen/).

Video background by Pressmaster from [Pexels](https://www.pexels.com/video/people-working-on-liquids-inside-a-laboratory-3195367/).

Periodic Table adapted from [Kevin Marks's Code](https://codepen.io/kevinmarks/pen/qjqXxG).

Periodic Table also takes from [Mike Golus's example](https://codepen.io/mikegolus/pen/OwrPgB).

Verify password JS example from [w3schools tutorial](//https://www.w3schools.com/howto/howto_js_password_validation.asp).

ContentEditable div's and experiment.html's toolbar functions adapted from [Mozilla's Web Guide](//developer.mozilla.org/en-US/docs/Web/Guide/HTML/Editable_content)

Simple rich text editor [example](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Editable_content)

Other editor examples used for [inspiration](https://alloyeditor.com)

Paste HTML at caret position [example](https://jsfiddle.net/Xeoncross/4tUDk)

Keeping track of caret position within experiment document modified from [Konstantin Münster's JS](https://javascript.plainenglish.io/how-to-find-the-caret-inside-a-contenteditable-element-955a5ad9bf81).

Other caret related [sources](https://javascript.plainenglish.io/how-to-find-the-caret-inside-a-contenteditable-element-955a5ad9bf81)

How to set cursor position [discussion](https://stackoverflow.com/questions/6249095/how-to-set-caretcursor-position-in-contenteditable0element-div)

Table creation button functionality adapted from this [Stackoverflow thread](https://stackoverflow.com/questions/14643617/create-table-using-javascript)

Save contentEditable content by moving to hidden form field from this other [Stackoverflow thread](https://stackoverflow.com/questions/6247702/using-html5-how-do-i-use-contenteditable-fields-in-a-form-submission)

404 Error page image found [here](https://www.animaljamarchives.com/science-party)

Header icon from [Favicon](https://favicon.io/emoji-favicons/microscope)

Experiment page link creation adapted from this [example](https://stackoverflow.com/questions/23811132/adding-a-target-blank-with-execcommand-createlink)











