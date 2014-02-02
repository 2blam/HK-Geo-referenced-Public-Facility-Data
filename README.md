#Background

This project is to develop an automatic way to download the Hong Kong Geo-referenced Public Facility Data [1]. At the time of writing this document, there are total 79 csv data such as Cycling Sites, Hoilday Camps and Performing Venus. 

##About the download process

When the user clicks the download data button, a popup window will then be shown and the user is required to 

	1. select the "Unit" (where you come from such as Student, Government and Individual),
	2. select the "Purpose", and 
	3. input the validation code.

The user needs to refer the captcha image and key in the corresponding validation. If everything is correct, after pressing the Accept button, the data file can then be downloaded.

#Solution

It is a time consuming task to download all the data manually. At the beginning, I supposed the file can be download easily by just simply refer to the URL such as _action=downloadFile&filename=csv/AIDED_PRS.csv&authCode=RSQY2D&unit=opt9&purpose=opt10. However, it does not work as the authCode cannot be reused after downloaded a data file. 

I adopted Selenium [2] to automate the download process and sed [3] as a reference to dsign the function to decode the captcha. In short, I used the Python script to 

	1. capture the screen with captcha image*,
	2. preprocessing the captcha image, i.e. it just contain the characters (black and white image) and then, 
	3. feed to send to PyTesser which is Optical Character Recognition (OCR) module for Python^

<sup>*</sup> the captcha image cannot be downloaded by referring the <img> tag src attribute. I used the script to take the screenshot and crop the captcha image for further process.

<sup>^</sup> there is some known problem in OCR, e.g. J was wrongly recognized as ]

#Alternative solution 
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
- pytesser
- selenium 
- chrome web driver

# Tested Platform
- Windows 7

# Future Work
- convert the coordinate system from Hong Kong 1980 Grid System (EPSG:2326) to WGS84 EPSG:4326

# Reference
1. http://www1.map.gov.hk/gih3/view/index.jsp
2. http://docs.seleniumhq.org/
3. http://www.debasish.in/2012/01/bypass-captcha-using-python-and.html?m=1
4. http://code.google.com/p/pytesser
