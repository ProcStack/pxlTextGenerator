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
<br/>With the tool open, click *`Set Project Folder`*, and select your folder.
<br/>The tool will then create three folders,
*    `pxl_textBases_origImages` - Your scans/photos will be moved to this directory
*    `pxl_textCharacterOutput` - Your exported Characters will be stored here as PNG files
*    `pxl_pageBuilderOutput` - Your exported Pages will be stored here as PNG files

If all went well, the tool should load up the first image it finds from `pxl_textBases_origImages,`
<br/>With a list of all your files on the top of the window
##### <p align="right">[^ Top](#index)</p>
##
## **Character Builder Tab**
#### TextBase Image Viewer
    Set Project Folder
    Reset Character Data
    Hide/Show TextBase List
    Searching Threshold
    Sample Threshold by Color
    Modes-
    _Select Area
    _Add Brush
    _Remove Brush
    Add/Remove Brush Size
    Edge Grow/Shrink
#### Character Settings
    Top/Bottoma
    Left Align
    Right Align
    Base Line
    PreMultiply Scale
    Alpha Fade Reach
    Alpha Contrast
    Degree Rotation
    Finish Character
#### Side Bar
    Current TextBase
    Filter
    Character Entry List
#### TextBed
    Load Text Image
    Reload Text
    Auto Update
    Text Field
    Random Seed
    Pull Capital Letters
    Pull Lower Letters
    Pull Numbers
    Pull Non-Alphanumeric
    Vertical Sliders 
    Charicter Test Display
##### <p align="right">[^ Top](#index)</p>
##
## **Page Output Tab**
#### Sidebar Options
    Load Page BG Image
    Font Scale
    Space Size
    Line Height
    Line Indent
    Random Seed
    Page Indentation; Left, Top, Right, Bottom
    Auto Update
    Update Output Text to Writing
    Set to New Page Entry
    Load Page Data File
    Output Directory
    Write Page Data File
    Export All Page Data & Images
#### Bottom Bar (After loading a Page BG Image)
    Page Group List
    Per Group
        Name of Group
        Edit Pages
        Delete Pages
        Thumbnail
    
##### <p align="right">[^ Top](#index)</p>
______________________________

## Thanks for checking out pxlTextGenerator!

