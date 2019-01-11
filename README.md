# **pxlTextGenerator**  *v0.0.9 - Alpha*
## **Text to Handwriting Generator**

## **Index**
[Tool Information](#tool-information)
<br/>[Starting Out](#starting-out)
<br/>[Character Builder Tab](#character-builder-tab)
<br/>[Page Output Tab](#page-output-tab)

## **Tool Information**
This tool is designed to allow users to **gather hand written characters**,
<br/>**(*Or I guess, any connected mass*)**
<br/>In photos and **export** them to an **image library** and **database**.
<br/>***- Written with* `Python 2.7` *and* `PyQt 4`**
<br/>
<br/>A database is built so later iterations of this tool can take the exported
<br/>characters and use them to convert typed text into an image that is seemingly hand written.
<br/>
<br/>Currently, You can save out hand written characters into individual PNG files with options
<br/>to modify the alpha fall off from the dynamically built mask of the ink.
<br/>
<br/>Since I have an intended purpose for this tool, it is expecting lighter paper and dark ink.
<br/>Being that, the color threshold will tell the script to select only neighboring pixels of color
<br/>darker than the set color threshold of brightness.
<br/>
<br/>There have been some logic written up on converting this system to an OCR reader
<br/>But that is a long time from now.
<br/>
<br/>It is slow right now, but hoping to expand this out toward OpenGL or C++ in the future.
<br/>Python and PyQt was just the easy route to start with.
<br/>
### - **Kevin Edzenga** <br/>
##### <p align="right">[^ Top](#index)</p>
##
## **Starting Out**
The tool is expecting a folder in its root with images ( jpg, jpeg, png, bmp )
<br/>These photos should be scans/photos you took of your handwriting/letters/characters
<br/>
<br/>With the tool open, click 'Set Project Folder', and select your folder.
<br>![Set Your Project Folder](http://metal-asylum.net/python/pxlTextGenerator/show/readMe_setProjectFolder.jpg)
<br/>The tool will then create three folders,
<br/>   pxl_textBases_origImages - Your scans/photos will be moved to this directory
<br/>   pxl_textCharacterOutput - Your exported Characters will be stored here as PNG files
<br/>   pxl_pageBuilderOutput - Your exported Pages will be stored here as PNG files
<br>![Folder Structure](http://metal-asylum.net/python/pxlTextGenerator/show/readMe_folderStructure.jpg)
<br/>
<br/>If all went well, the tool should load up the first image it finds from `pxl_textBases_origImages`,
<br/>With a list of all your files on the top of the window
##### <p align="right">[^ Top](#index)</p>
##
## **Character Builder Tab**
#### TextBase Image Viewer
<br/>    Set Project Folder
<br/>    Reset Character Data
<br/>    Hide/Show TextBase List
<br/>    Searching Threshold
<br/>    Sample Threshold by Color
<br/>    Modes-
<br/>    _Select Area
<br/>    _Add Brush
<br/>    _Remove Brush
<br/>    Add/Remove Brush Size
<br/>    Edge Grow/Shrink
#### Character Settings
<br/>    Top/Bottom
<br/>    Left Align
<br/>    Right Align
<br/>    Base Line
<br/>    PreMultiply Scale
<br/>    Alpha Fade Reach
<br/>    Alpha Contrast
<br/>    Degree Rotation
<br/>    Finish Character
#### Side Bar
<br/>    Current TextBase
<br/>    Filter
<br/>    Character Entry List
#### TextBed
<br/>    Load Text Image
<br/>    Reload Text
<br/>    Auto Update
<br/>    Text Field
<br/>    Random Seed
<br/>    Pull Capital Letters
<br/>    Pull Lower Letters
<br/>    Pull Numbers
<br/>    Pull Non-Alphanumeric
<br/>    Vertical Sliders 
<br/>    Charicter Test Display
##### <p align="right">[^ Top](#index)</p>
##
## **Page Output Tab**
#### Sidebar Options
<br/>    Load Page BG Image
<br/>    Font Scale
<br/>    Space Size
<br/>    Line Height
<br/>    Line Indent
<br/>    Random Seed
<br/>    Page Indentation; Left, Top, Right, Bottom
<br/>    Auto Update
<br/>    Update Output Text to Writing
<br/>    Set to New Page Entry
<br/>    Load Page Data File
<br/>    Output Directory
<br/>    Write Page Data File
<br/>    Export All Page Data & Images
#### Bottom Bar (After loading a Page BG Image)
<br/>    Page Group List
<br/>    Per Group
<br/>        Name of Group
<br/>        Edit Pages
<br/>        Delete Pages
<br/>        Thumbnail
<br/>    
##### <p align="right">[^ Top](#index)</p>
______________________________

## Thanks for checking out pxlTextGenerator!

