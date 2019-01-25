# **pxlTextGenerator**  *v0.2.0 - Beta*
## **Text to Handwriting Generator**
#### *Turn your written characters into an image based font*
#### *Export with custom page backgrounds to PNG*

## <br/>**Index**
* [Welcome & Tool Information](#welcome-message--tool-information)
* [Starting Out](#starting-out)
* [Character Builder Tab](#character-builder-tab)
* [Page Output Tab](#page-output-tab)

--------------------------------------------------------------------------------------------
<p align='center'><img src='http://metal-asylum.net/python/pxlTextGenerator/show/intro_characterBuilder_V020.png' alt="pxlTextGenerator Overview" /></p>
<p align='center'><img src='http://metal-asylum.net/python/pxlTextGenerator/show/intro_pageOutput_V020.png' alt="pxlTextGenerator Page Output" /></p>

--------------------------------------------------------------------------------------------

## <br/>**Welcome Message \& Tool Information**
This tool is designed to allow users to **gather hand written characters**,
<br/>**(*Or I guess, any connected mass*)**
<br/>In photos/scans/images and **export** them to an **image library** and **database**.
<br/>***- Written with* `Python 2.7` *and* `PyQt 4`**
<br/>
<br/>A Character Database is built and can be used to convert typed text into seemingly hand written images.
<br/>You can save those pages to a Page Database or export them as PNG files!
<br/>*(The Character and Page Database Files let you jump back in where you left off, allowing you to edit all the settings.)*
<br/>
<br/>Since I have an intended purpose for this tool, it currently looks for darker objects.
<br/>Like having ink that is darker than the paper it's on.
<br/>This is done by looking out pixel by pixel to see if it's under a user-settable brightness threshold.
<br/>
<br/>In the future, I'd like to add OCR (Optical Character Recognition) functionality.
<br/>Since it supports having as many character variations as you'd like, they could be used as training material for the OCR.
<br/>But that will be some time from now...  We all have lives to manage and things that distract us.
<br/>
<br/>It's slow right now, optimizations are being worked on,
<br/>But I'm hoping to expand out toward OpenGL / C++ in the future.
<br/>*(Especially for the OCR support)*
<br/>Python and PyQt was just the easy route to start with.
<br/>
<br/> **\*\* Since this is still in Beta, some aspects are in flux \*\***
<br/> The only major changes I forsee is GUI layout and adding new features.
<br/> If you find any bugs or have any suggestions, feel free to contact me at--
<br/> [Kevin@Metal-Asylum.Net](mailto:Kevin@Metal-Asylum.Net)
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
  * For sliders, you can click on the text next to the slider to manually enter in a value.
    * Only vertical sliders and the Left/Right Align sliders on the `Character Entry Editor` *(Right side)* don't have this feature yet.
  * After you select your character and run `Read Found Character Data` the `Final Output` thumbnail will have 3 red lines on it.  You can click near those red lines and drag to adjust the values without fudging around with the sliders.
  * If you are working on editing a Character Entry, type the character out in the TextBed on the bottom to see your changes in real time. (Vertical/Left/Right Alignment and Scaling mostly)
  * Hotkeys --
    * **`P`** - Load a Project Folder
    * **`T`** - Sample Threshold Color; toggle
    * **`S`** - Select Mode
    * **`A`** - Set to Add Brush
    * **`R`** - Set to Remove Brush
    * **`W`** - Set Working Area; toggle
    * **`C`** - Crop to Work Area; toggle
    * **`O`** - Show Outline Only; toggle
##### <p align="right">[^ Top](#index)</p>
##
## **Character Builder Tab**
#### TextBase Image Viewer
  * **`Set Project Folder`** - `P` hotkey - Sets and Attempts to load existing data
  * **`Reset Character Data`** - Resets all currently selected character data (The green color after sampling)
  * **`TextBase Image List`** - List of all your images, Hide/Show Toggle
  * **`Hide/Show TextBase List`** - Hide/Show visibility toggle for the TextBase Image List
  * **`Searching Threshold`** - Value of brightness that searching stops at.
    * *(Searching finds darker colors than the threshold value.)*
  * **`Sample Threshold by Color`** - `T` hotkey - Lets you select pixels to set the Searching Threshold
    * *(Set the threshold lower once it's set, its the exact value it found, you want darker)*
    
![pxlTextGenerator Page Output](http://metal-asylum.net/python/pxlTextGenerator/show/TextBaseOptions_brushes_all.png)
  * **`Modes`**- \[When *Active* image\]
    * **`Select Area`** - `S` hotkey -<br/> ![Select Character Mode Option](http://metal-asylum.net/python/pxlTextGenerator/show/TextBaseOptions_brushes_sel.png)
      * *Search for a character*
      * *No Brush Indicator*
    * **`Add Brush`** - `A` hotkey -<br/> ![Add Brush Option](http://metal-asylum.net/python/pxlTextGenerator/show/TextBaseOptions_brushes_add.png)
      * *Add pixels to found area*
      * *Brush Indicator is a Green color*
    * **`Remove Brush`** - `R` hotkey -<br/> ![Remove Brush Option](http://metal-asylum.net/python/pxlTextGenerator/show/TextBaseOptions_brushes_rem.png)
      * *Remove pixels to found area*
      * *Brush Indicator is a Purple color*
  * **`Add/Remove Brush Size`** - Size of Add/Remove Brushes
  * **`Edge Grow/Shrink`** - Contract or Expand your character's edge per pixel
    * *Negative (-1) to Contract*
    * *Positive (1) to Expand*
  * **`Set Working Area`** / **`Remove Work Area`** - `W` hotkey - Isolate an area of your TextBase Image to help speed up performance and make tools/brushes easier to use.
    * *Click it, the button's text will switch to **`Remove Work Area`** and turn blue, then click and drag in the TextBase area to draw a blue working area outline.*
    * *Clicking again will remove the current work area you have set.*
  * **`Crop To Work Area`** / **`Exit Work Area Crop`** - `C` hotkey - To help speed up things further, you can view the Work Area by itself for faster feed back for `Select`/`Add`/`Remove` Brushes.
    * *Click it to isolate your Work Area, the button's text will change to `Exit Work Area Crop` and turn blue.*
    * *Clicking it again will bring back the whole image you are working on.*
  * **`Exit Work Area on Reset`** - Auto Exit Work Area Crop
    * When `Off`, if you **`Reset Character Data`**, it will keep the TextBase Viewer in Crop mode.
    * When `On`, it will exit Crop mode when you **`Reset Character Data`**.
  * **`Show Outline Only`** / **`Exit Outline Only`** - `O` hotkey - Sometimes the character found might have grabbed some junk, this will outline the found character
    *  Clicking again will redraw the found area as it normally looks
#### Character Settings
  * **`Read Found Character Data`** - Load your character data.
    * Once you search for a character in the TextBase Viewer,
    * This button will gather all the data and build transparency information for you
    * You can then edit the character with the below options.
  * **`Crop, Found Area, Alpha Thumbnails`** - After running `Read Found Character Data` thumbnails are generated to show aspects of the found character data.
    * '`Alpha`' refers to the transparency of the final image.<br/>Like how you can see the checkerboard pattern behind the main Character image.
    * *Currently These thumbnails are for reference only.*
  * **`Character Final Output Image`** - This is what your final character looks like.
    * *The checkered background is just to help with seeing the transparency in the character. Its removed when you click `Finishe Character`
    * There are 3 red lines; 2 vertical and 1 horizontal
      * *The left vertical line is the desired spacing on the left side of the character to it's neighbor.*
      * *The right vertical line is the same as the left, but spacing on the right side of the character from its neighbor.*
      * *The horizontal line is the base of the character.  Where the character will line up vertically on a line of text.*
    * **(*If you click near a red line and drag, it will move the line for you.  No need to use the sliders.*)**
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
  * **`Font Kerning`** - Global kerning size in pixels, the distance between characters in the page
  * **`Space Size`** - Size of a 'space' in pixels
  * **`Line Height`** - How spread apart each new line is in pixels
  * **`Line Indent`** - Indentation distance of wrapped lines of text
  * **`Random Seed`** - The random value used when picking each character.
    * *Lets say you have 4 'A' characters and type 'AAAA'*
    * *Random Seed 0.0 might give you A3,A2,A4,A1*
    * *Random Seed 3.1 might give you A1,A4,A1,A2*
  * **`Auto Update`** - Any changes will rebuild the page, when `On`
  * **`Update Output Text to Writing`** - Update the current page you are editing
  * **`New Empty Page Entry`** - Creates a new empty Page Group, resetting you values
    * *Any unsaved changes to the current page you are working on will be lost*
  * **`Set as New Page Entry`** - Creates a new Page Group from your current settings
  * **`Output Directory`** - Directory to export your Page Images to
  * **`Write Page Data File`** - Write out the Page Data File ONLY; *projectName*/pageListKey.py
  * **`Export All Page Data & Images`** - Write out the Page Data File and all Page Images
  * Implimented scipting system for modifying your `Input Page Text`-
<p align='center'><img src='http://metal-asylum.net/python/pxlTextGenerator/show/pageOutput_fontTagSample.png' alt="pxlTextGenerator Page Output" /></p>
#### Special Characters-
  * **`%charName%`** to output the character you desire
    * eg- **`%str%`** for a star symbol instead of just a multiply symbol
  * Custom special characters not implimented yet,
    * Thats a little outside my current needs for this tool.
  * Current supported special characters-
    * **`ocl`**,**`ocr`**,**`oll`**,**`olr`**,**`osl`**,**`osr`**,**`oal`**,**`oar`**,**`str`**
  * They can be set to what ever you'd like though
    * Just because it's called **`str`** doesn't mean it needs to be a star.
### Font Modifying Tags-
  * **`%###%`** to scale text; **`%50%`** is 50 percent scale, **`%100%`** to get back to normal
	  
  * **`%align:position%`** - the positions can be **`left`**, **`center`**, or **`right`**
    * %align:center%`** to align your text center then **`%align%`** to reset to left alignment.
    * Affects whole line until set again or reset with **`%align%`**
  * **`%a:position%`** - Set alignment for current line only
    * Any return or `\n` will reset the alignment to `left`
		
  * **`%offset:#,#%`** - Offset characters in X,Y by pixels
    * Relative offset for all following text.
    * If you put only one number, it will offset only in Y
      * **`%offset:10%`** - Will offset the following text [0,10]
    * Affects whole lines until set again or reset with **`%offset%`** or **`%o%`**
  * **`%o:#,#%`** - To set offset for the next character only
    * It will reset to 0,0 offset after the next character.
		
  * **`%rotate:degrees%`** - Rotate characters in degrees for all following text.
	  
  * **`%spaceSize:pixels%`** - Line space size ixels is relative offset.
    * %spaceSize:-10% - If space size is 50, it will be 40
    * Affects whole lines until set again or reset with **`%spaceSize%`** or **`%ss%`**
  * **`%ss:pixels%`** - Set spaceSize for current line only
    * Any return or `\n` will reset the spaceSize to current setting
		
  * **`%kern:pixels%`** - Line character kerning in relative pixels offset.
    * **`%kern:-10%`** - If kerning is 0, it will be -10
    * Affects whole lines until set again or reset with **`%kern%`** or **`%k%`**
  * **`%k:pixels%`** - Set kerning for next character only
    * It will reset to a 0 pixel kerning offset after the next character.
		
  * **`%lineHeight:pixels%`** - pixels is relative offset
    * **`%lineHeight:-20%`** - If line height is 70, it will be 50
    * **`%lineHeight%`** to clear offset.
    * Affects whole lines until set again or reset with **`%lineHeight%`** or **`%lh%`**
  * **`%lh:pixels%`** - Set lineHeight pixels for current line only
    * Any return or `\n` will reset the lineHeight to current setting
	  
  * **`%seed:#%`** - Set the seed random for following characters.
    * **`%seed:12.4%`** to set a random value of 12.4
    * **`%seed%`** to reset to your set seed
    * This is good for changing a lot of characters in a word or line.
  * **`%s%`** or **`%s:#%`** - To set a random or specific seed for the next character only
    * If a specific character is a repeat of a near by variation-
      * `will` and both 'l's are the same 'l'-
      * `wil%s%l` changes the second 'l' to a different variation
		  
  * **`%opacity:percent%`** - Percentage is 0-100
    * **`%opacity:50%`** - The characters following will be at 50% opacity.
    * Affects whole lines until set again or reset with **`%opacity%`** or **`%op%`**
  * **`%op:percent%`** - To set opacity for the next character only
    * It will reset to 100% opacity after the next character.
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
