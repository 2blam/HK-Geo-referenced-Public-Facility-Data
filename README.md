#Background

This project is to develop a script to download the Hong Kong Geo-referenced Public Facility Data [1] automatically. At the time of writing this document, there are total 79 csv data such as Cycling Sites, Hoilday Camps and Performing Venus. 

##About the download process

When the user clicks the download data button, a popup window will then be shown and the user is required to 

	1. select the "Unit" (where you come from such as Student, Government and Individual),
	2. select the "Purpose", and 
	3. refer the captcha image and key in the corresponding validation code.

If everything is correct, after pressing the Accept button, the data file can then be downloaded.

#Solution

It is a time consuming task to download all the data manually. At the beginning, I supposed the file can be download easily by just simply refer to the URL such as _action=downloadFile&filename=csv/AIDED_PRS.csv&authCode=RSQY2D&unit=opt9&purpose=opt10. However, it does not work as the authCode cannot be reused after downloaded a data file. 

I adopted Selenium [2] to automate the download process and [3] as a reference to dsign the function to decode the captcha. In short, I used the Python script to 

	1. capture the screen with captcha image*,
	2. preprocessing the captcha image, i.e. it just contain the characters (black and white image) and then, 
	3. send to PyTesser which is Optical Character Recognition (OCR) module for Python^

<sup>*</sup> the captcha image cannot be downloaded by referring the <img> tag src attribute. I used the script to take the screenshot and crop the captcha image for further process.

<sup>^</sup> there is some known problem in OCR, e.g. J was wrongly recognized as ]

#Convert the coordinates to WGS84
QGIS[6] can help to convert the coordinates from Hong Kong 1980 Grid System to WGS84. Also, it can help to save it as JSON file. Here is the details:

	1. Layer > Add Delimited Text Layer
	2. Select the csv file, then press OK button
	3. Select Hong Kong 1980 Grid System
	4. In Layer panel, right click the layer, select Save As
	5. Choose the output path
	6. In CRS entry, click Browse button, select WGS84
	7. Press OK button

I used macro [7] to process all the data files.

#Post-processing scripts for csv files
A number of python scripts (inside scripts folder) were created for
- check the encoding of all public facility data csv files (Note: all the csv files are encoded in UTF-16-LE)
- check the common and unique column names among all csv files
- combine all the csv file into a signl excel / csv file
- for each public facility, check which constituency area it belongs to and add new property CACODE to store the corresponding information

Note: there is an error in LIBRARY_LCSD_20131213.csv. Please check README.txt in csv_files_err_fixed.zip

For more details, please check the program comments.


#Alternative solution to download the data file
[This section can be omitted if you are not interested]

To download the data file, it is necessary to 

	1. get an updated captcha image, 
	2. update the authCode in the href attribute manually, and then
	3. click the link to download the data. 

The alternative way to download the file is using Notepad++ and the macro. I did not test the following approach. But write it down for future reference. 

Preparation

	1. Use Notepad++ to edit the link (with correct filename and authCode). Note that the link, which shows in Notepad++ editor, is clickable, i.e. double click the link will download the file immediately
	2. Use Chrome (or any browser) to [1]
	3. Click Map Tools > Data Download 
	4. Click Data Icon (any file is fine) to show a pop up with captcha image. Hold such screen and don't need to fill in anything (to keep the session)

Bot control: 

	1. refresh the captcha image [BOT] 
	2. move the cursor after the keyword authCode= (use find function) [BOT] 
	3. manually key in the captcha data [MANUAL]
	4. double click the link [BOT]
	5. delete the visited link [BOT] 
	6. Go Back to 1. and REPEAT 79 times

# How to run
<pre>python getAllPubFacilityData.py</pre>

# Requirements
- pytesser [4] - extract the zip files to the directory with getAllPubFacilityData.py
- selenium  [2]
- chrome web driver [5] - put the exe file to the directory with getAllPubFacilityData.py 

# Tested Platform
- Windows 7

# Future Work
- <strike>convert the coordinate system from Hong Kong 1980 Grid System (EPSG:2326) to WGS84 EPSG:4326</strike> <strong>DONE</strong>
- check if there is any script/command in QGIS to convert the coordinate system and export to JSON

# Reference
1. http://www1.map.gov.hk/gih3/view/index.jsp
2. http://docs.seleniumhq.org/
3. http://www.debasish.in/2012/01/bypass-captcha-using-python-and.html?m=1
4. http://code.google.com/p/pytesser
5. https://code.google.com/p/selenium/wiki/ChromeDriver
6. http://www.qgis.org/en/site/
7. http://www.jitbit.com/macro-recorder/