from selenium import webdriver
from time import sleep
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# import Image
# import pytesseract

# print(pytesseract.image_to_string(Image.open('cropped_maindraw.png')))
# print(pytesseract.image_to_string(Image.open('cropped_stackpot.png')))
# print(pytesseract.image_to_string(Image.open('cropped_survey.png')))

def crop_image(image, long=False):
    from shutil import copyfile
    copyfile(image, "working_image.png")
    image1 = Image.open("working_image.png")
    #crop the image using the attributes defined (l, t, r, b)
    if long:
        image1 = image1.crop((445,210,700,2080))
    else:
        image1 = image1.crop((445,210,700,280))
    image1.save("cropped_" + image)

print('starting')
driver = webdriver.PhantomJS()
driver.implicitly_wait(30)
driver.set_window_size(1120, 550)

driver.get("https://freepostcodelottery.com/")
driver.find_element_by_class_name("cancel-btn").click()
sleep(10)
driver.find_element_by_id("confirm-email").send_keys("spencer.jago.register@gmail.com")
driver.find_element_by_id("confirm-ticket").send_keys("PL3 4PW")
driver.find_element_by_class_name("btn-loader").click()
sleep(10)
try:
    driver.find_element_by_class_name("dismiss").click()
except:
    pass
print('taking login screen shot')
sleep(10)
driver.save_screenshot('maindraw.png')
driver.find_element_by_link_text('Check Survey draw').click()
print('taking survey screen shot')
sleep(60)
try:
    driver.find_element_by_link_text('No thanks, show me the winning postcode').click()
except:
    pass
finally:
    driver.save_screenshot('survey.png')
    driver.find_element_by_link_text('Check Video draw').click()
sleep(20)

container = driver.find_element_by_class_name("vjs-tech")
button = driver.find_element_by_class_name("vjs-big-play-button")
ActionChains(driver).move_to_element(container).click(button).perform()
# Hover = ActionChains(driver).move_to_element(add).click("vjs-big-play-button")
# Hover.click().perform()
# driver.find_element_by_class_name("vjs-tech").click()
print('taking video screen shot')
sleep(40)
driver.save_screenshot('video.png')
driver.find_element_by_link_text('Check the Stackpot').click()
print('taking stackpot screen shot')
try:
    driver.find_element_by_class_name("dismiss").click()
except:
    pass
driver.save_screenshot('stackpot.png')
driver.find_element_by_link_text('Check Bonus Draw').click()
try:
    driver.find_element_by_class_name("dismiss").click()
except:
    pass
sleep(40)
driver.save_screenshot('bonus.png')
driver.get("https://freepostcodelottery.com/sponsored/")
sleep(10)
elems = driver.find_elements_by_link_text('Get your entry for today')
elems[0].click()
sleep(60)
driver.save_screenshot('groupon.png')
driver.execute_script("window.history.go(-1)")
elems = driver.find_elements_by_link_text('Get your entry for today')
elems[1].click()
sleep(60)
driver.save_screenshot('quidco.png')

driver.quit()

crop_image('maindraw.png')
crop_image('survey.png')
crop_image('video.png')
crop_image('stackpot.png', True)

print('sending email')
fromaddr = "spencer.jago.main@gmail.com"
toaddr = "spencer.jago@gmail.com"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "POSTCODE LOTTERY"
 
body = "Todays winners\n"
 
msg.attach(MIMEText(body, 'plain'))
 
filename1 = "cropped_maindraw.png"
attachment1 = open("/Users/Spencer/Code/pcl/cropped_maindraw.png", "rb")
filename2 = "cropped_survey.png"
attachment2 = open("/Users/Spencer/Code/pcl/cropped_survey.png", "rb")
# filename3 = "video.png"
# attachment3 = open("/Users/Spencer/Code/pcl/cropped_video.png", "rb")
filename4 = "cropped_stackpot.png"
attachment4 = open("/Users/Spencer/Code/pcl/cropped_stackpot.png", "rb")
 
part1 = MIMEBase('application', 'octet-stream')
part2 = MIMEBase('application', 'octet-stream')
# part3 = MIMEBase('application', 'octet-stream')
part4 = MIMEBase('application', 'octet-stream')
part1.set_payload((attachment1).read())
part2.set_payload((attachment2).read())
# part3.set_payload((attachment3).read())
part4.set_payload((attachment4).read())
encoders.encode_base64(part1)
encoders.encode_base64(part2)
# encoders.encode_base64(part3)
encoders.encode_base64(part4)
part1.add_header('Content-Disposition', "attachment; filename= %s" % filename1)
part2.add_header('Content-Disposition', "attachment; filename= %s" % filename2)
# part3.add_header('Content-Disposition', "attachment; filename= %s" % filename3)
part4.add_header('Content-Disposition', "attachment; filename= %s" % filename4)
 
msg.attach(part1)
msg.attach(part2)
# msg.attach(part3)
msg.attach(part4)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "6%alKLDRs9@Sds0H")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()