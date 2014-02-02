from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as BY
import os
import time


from PIL import Image
import ImageEnhance
from urllib import urlretrieve
import pytesser
import re
 
# getAuthCode - get the captcha image, extract the characters
#				convert the image to black and white
#				feed to OCR for character recognition
def getAuthCode(fn):
	#read the file
	im = Image.open(fn)

	# change the image size
	nx, ny = im.size
	width = int(nx*7)
	height = int(ny*7)
	im2 = im.resize((width, height), Image.BICUBIC)

	#if the pixel value is close less than RGB value (90, 136, 100)
	# convert it to black pixel (0, 0, 0), 
	# otherwise, white pixel (255, 255, 255)
	pix = im2.load()
	for x in range(width):
		for y in range(height):			
				(r, g, b) = pix[x, y]
				if (r < 90 and g < 136 and b < 100 ):							
					pix[x, y] = (0, 0, 0)
				else:				
					pix[x, y] = (255, 255, 255)

	#save the image 
	im2.save("bw.bmp")				

	# OCR
	pattern = re.compile(r'[\s\n]+')
	result= pytesser.image_file_to_string('bw.bmp').strip().upper()
	result= pattern.sub('', result).upper()
	#print result	
	return result

#saveCaptchaImage - capture the screen shot, crop the captcha region
#					save it with respect to output file name (ofn)
def saveCaptchaImage(driver, ofn, box):
	driver.save_screenshot('screen.png')	
	im = Image.open("screen.png")
	#crop the screen with respect to box coordinates
	area = im.crop(box)
	area.save(ofn)


if __name__ == "__main__":
	#call chrome driver
	chromedriver = "./chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	
	driver.get("http://www1.map.gov.hk/gih3/view/index.jsp")

	time.sleep( 5 ) #wait everthing ready
	

	#change to English page
	wait = WebDriverWait(driver, 10) #wait until the button is clickable
	element = wait.until(EC.element_to_be_clickable((BY.ID,'chglang1')))
	element = driver.find_elements_by_id("chglang1")
	print element[0].text
	element[0].click()
	time.sleep( 5 ) #wait everthing ready
	
	# click map tool tab
	wait = WebDriverWait(driver, 10) #wait until the button is clickable
	element = wait.until(EC.element_to_be_clickable((BY.ID,'tab_theLeft2_label')))
	element = driver.find_elements_by_id("tab_theLeft2_label") 
	mapToolTab = element[0]
	mapToolTab.click()

	# click download button
	wait = WebDriverWait(driver, 10)
	element = wait.until(EC.element_to_be_clickable((BY.ID,'menuBtn_psi')))
	element = driver.find_elements_by_id("menuBtn_psi")
	downloadBtn = element[0]
	downloadBtn.click()

	btnNumber = 10 #the Accept button named as yui-gen10-button
				   # the number will be incremented by 2 in next download page
				   #For example, in next download page, the Accept button is with id yui-gen12-button
	
	first = True #check if it is the first time to download the file
				 # it needs to change the box dimension
				 # if it is first time, box dimension: (309, 529, 408, 559)
				 # else, box dimension: (309, 509, 408, 536)

	captchaImageFileName = "captcha.png"

	for page in range(4): # 4 pages	  
		#get the download page
		wait = WebDriverWait(driver, 10) #wait until the button is clickable
		downloadDataElements = wait.until(EC.element_to_be_clickable((BY.XPATH,'//img[@alt="Download Data"]')))
		downloadDataElements = driver.find_elements_by_xpath('//img[@alt="Download Data"]/parent::a')
		
		# for each page, check the total number of download items
		numOfItems = int(len(downloadDataElements))
		#print "numOfItems" + str(numOfItems)
		
		for idx in range(numOfItems):	
			#click to download the item
			item = downloadDataElements[idx]
			item.click()

			# select option - Unit:			
			wait = WebDriverWait(driver, 10) #wait until the button is clickable
			element = wait.until(EC.element_to_be_clickable((BY.NAME,'unit')))
			select_box = Select(driver.find_element_by_name("unit"))
			select_box.select_by_visible_text("Others")

			# select option - Purpose:
			select_box = Select(driver.find_element_by_name("purpose"))
			select_box.select_by_visible_text("Others")

			
			# get the authRsult path		
			img = driver.find_element_by_xpath('//img[@id="authRslt"]')
			src = img.get_attribute('src')
			# if it is incorrect
			while src.split("/")[-1] == "cross.gif" or src.split("/")[-1] == "space.bmp":
				#refresh the captcha
				refreshBtn = driver.find_element_by_xpath('//img[@id="reloadAuthImg"]')
				refreshBtn.click()
				time.sleep(1)
				if first == True:
					saveCaptchaImage(driver, captchaImageFileName, box=(309, 529, 408, 559))	
				else:				
					saveCaptchaImage(driver, captchaImageFileName, box=(309, 509, 408, 536))	

				#authImg = driver.find_element_by_id("authImg")
				#src = authImg.get_attribute('src')
				
				# get the image source, crop the captcha, and save it
				authCode = getAuthCode(captchaImageFileName)

				# locate the authCode text field
				item = driver.find_elements_by_id('authCode')
				authCodeField = item[0]
				authCodeField.clear()
				# send the OCRed authCode
				authCodeField.send_keys(authCode)
				
				time.sleep(1)	
				#get the authRslt path again to check if it is correct
				img = driver.find_element_by_xpath('//img[@id="authRslt"]')
				src = img.get_attribute('src')
				#print src
				time.sleep(1)

			#click Accept button
			item = driver.find_elements_by_id('yui-gen' + str(btnNumber) + '-button')
			btnNumber = btnNumber + 2
			acceptBtn = item[0]
			acceptBtn.click()
			first = False
			time.sleep(3) # need to wait longer otherwise, the item cannot be clicked
			

		#click next button
		nextBtn = driver.find_element_by_xpath('//a[@alt="Next Page"]')
		time.sleep(2)
		nextBtn.click()
		time.sleep(2)


	driver.quit()