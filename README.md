# **pxlTextGenerator**  *v0.1.1 - Alpha*
## **Text to Handwriting Generator**
#### *Turn your written characters into an image based font*
#### *Export with custom page backgrounds to PNG*

## <br/>**Index**
* [Tool Information](#tool-information)
* [Starting Out](#starting-out)
* [Character Builder Tab](#character-builder-tab)
* [Page Output Tab](#page-output-tab)

--------------------------------------------------------------------------------------------
<p align='center'><img src='http://metal-asylum.net/python/pxlTextGenerator/show/intro.png' alt="pxlTextGenerator Overview" /></p>
<p align='center'><img src='http://metal-asylum.net/python/pxlTextGenerator/show/intro_pageOutput.png' alt="pxlTextGenerator Page Output" /></p>

--------------------------------------------------------------------------------------------

## <br/>**Tool Information**
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

#### Things to note-
  * For all sliders, you can click on the text next to the slider to manually enter in a value.
##### <p align="right">[^ Top](#index)</p>
##
## **Character Builder Tab**
#### TextBase Image Viewer
  * **`Set Project Folder`** - Sets and Attempts to load existing data
  * **`Reset Character Data`** - Resets all currently selected character data (The green color after sampling)
  * **`TextBase Image List`** - List of all your images, Hide/Show Toggle
  * **`Hide/Show TextBase List`** - Hide/Show visibility toggle for the TextBase Image List
  * **`Searching Threshold`** - Value of brightness that searching stops at.
    * *(Searching finds darker colors than the threshold value.)*
  * **`Sample Threshold by Color`** - Lets you select pixels to set the Searching Threshold
    * *(Set the threshold lower once it's set, its the exact value it found, you want darker)*
  * **`Modes`**-
    * **`Select Area`**
      * *Search for a character*
      * *No Brush Indicator*
    * **`Add Brush`**
      * *Add pixels to found area*
      * *Brush Indicator is a Green color*
    * **`Remove Brush`**
      * *Remove pixels to found area*
      * *Brush Indicator is a Purple color*
  * **`Add/Remove Brush Size`** - Size of Add/Remove Brushes
  * **`Edge Grow/Shrink`** - Contract or Expand your character's edge per pixel
    * *Negative (-1) to Contract*
    * *Positive (1) to Expand*
  * **`Set Working Area`** - To help speed up character searching, setting a Working Area will crop the image down
    * *Click it, then click and drag in the TextBase area to draw a blue working area outline*
  * **`Show Outline Only`** - Sometimes the character found might have grabbed some junk, this will outline the found character
  * **`Show Normal Display`** - When viewing the outline, this button will redraw the found area as it normally looks
#### Character Settings
  * **`Read Found Character Data`** - Load your character data.
    * Once you search for a character in the TextBase Viewer,
    * This button will gather all the data and build transparency information for you
    * You can then edit the character with the below options.
  * **`Crop, Found Area, Alpha Thumbnails`** - These thumbnails are for reference only, showing the found character data.
    * '`Alpha`' refers to the transparency of the final image.<br/>Like how you can see the checkerboard pattern behind the main Character image.
  * **`Top/Bottom`** - These side sliders add or remove bounding box's top or bottom
  * **`Left/Right Align`** - The left/right most edge of the character, for spacing characters correctly
  * **`Base Line`** - Where the character aligns vertically on the line, for TextBed and Page
  * **`PreMultiply Scale`** - The amount the character is multiplied before added to the line, for TextBed and Page
  * **`Alpha Fade Reach`** - Pixel distance from the edge to had a fade to transparent
  * **`Alpha Contrast`** - The % visibility of the Alpha Fade edge.
  * **`Degree Rotation`** - Rotate the character counter-clockwise or clockwise by Negative or Positive degrees, respectively.
  * **`Finish Character`** - Creates a new Character Entry in the side bar with all of your settings stored on the entry.
#### Side Bar
  * **`Current TextBase`** - Thumbnail of the current TextBase image
    * *Clicking it will `Reset Character Data` in the TextBase Viewer*
  * **`Filter`** - Display only specific characters here.
    * *Putting in 'A' will display only Capital Letter A's*
    * *Putting in 'AaB' will display only Capital Letters 'A' and 'B', along with Lowercase 'a'*
  * **`Character Entry List`** - Clicking the Character in the Entry List will load the settings into the Character Settings
    * *Existing un-Finish'ed character parameter details are lost*
#### TextBed
  * **`Load Text Image`** - Load a background image into the TextBed
    * *One is provided in the root of pxlTextGenerator*
  * **`Reload Text`** - Reload any changes made to characters or Text Field
  * **`Input Test Text`** - Characters to display in the TextBed Viewer
  * **`Pull Capital Letters`** - Loads all Capital letters into the Text Field
  * **`Pull Lower Letters`** - Loads all Lower Case letters into the Text Field
  * **`Pull Numbers`** - Loads all Numbers into the Text Field
  * **`Pull Non-Alphanumeric`** - Loads all non-letters and non-numbers into the Text Field
  * **`Missing Characters`** - Any non-existent characters will show up here from your `Input Text Text`
  * **`Auto Update`** - Any changes in Character Settings or Text Field will automatically show up when `On`.
  * **`Vertical Sliders`**  -
    * *First, Top of character reference bar*
    * *Second, Mid of character reference bar*
  * **`Character TextBed Display`** - Output of the Text Field as your Writing
##### <p align="right">[^ Top](#index)</p>
##
## **Page Output Tab**
#### Sidebar Options
  * **`Load Page Data File`** - Loads any previous Page Data written to disk
  * **`Load Page BG Image`** - Load a background image into the Page Output viewer
    * *One is provided in the root of pxlTextGenerator*
  * **`Input Page Text`** - The text you'd like to add to the page.
    * *You can add special characters by adding % before and after*
    * *For a Concerned Smiley Face,* **`%ocl%`**
    * *(All created special characters must be created by you)*
  * **`Page Indentation`**; Left, Top, Right, Bottom - Page margins 
    * *Indicated by red lines in the Page Output Viewer*
  * **`Font Scale`** - Global scale multiplier of characters as they are added into the page
  * **`Space Size`** - Size of a 'space' in pixels
  * **`Line Height`** - How spread apart each new line is in pixels
  * **`Line Indent`** - Indentation distance of wrapped lines of text
  * **`Random Seed`** - The random value used when picking each character.
    * *Lets say you have 4 'A' characters and type 'AAAA'*
    * *Random Seed 0.0 might give you A3,A2,A4,A1*
    * *Random Seed 3.1 might give you A1,A4,A1,A2*
  * **`Auto Update`** - Any changes will rebuild the page, when `On`
  * **`Update Output Text to Writing`** - Update the current page you are editing
  * **`Set to New Page Entry`** - Creates a new Page Group from your current settings
  * **`Output Directory`** - Directory to export your Page Images to
  * **`Write Page Data File`** - Write out the Page Data File ONLY; *projectName*/pageListKey.py
  * **`Export All Page Data & Images`** - Write out the Page Data File and all Page Images
#### Bottom Bar (After loading a Page BG Image)
  * **`Page Group List`** - List of all your current work
  * **`Per Group`** - Isolated group of pages built from one text input
    * **`Name of Group`** - This is the prefix name to your pages
      * *A Name of 'Info' will export the pages as 'Info_1', 'Info_2', etc...*
    * **`Edit Pages`** - Load and set all of the settings for that Page Group for Editing
    * **`Delete Pages`** - Deletes the ENTIRE Page Group
    * **`Thumbnail`** - Small little view of whats going on on the page

##### <p align="right">[^ Top](#index)</p>
______________________________

## Thanks for checking out pxlTextGenerator!

