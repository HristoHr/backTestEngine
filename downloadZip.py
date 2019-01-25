from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://subscene.com/english/How-I-Met-Your-Mother-Seventh-Season/subtitle-482407.aspx')
browser.execute_script('WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("s$lc$bcr$downloadLink", "", true, "", "/english/How-I-Met-Your-Mother-Seventh-Season/subtitle-482407-dlpath-90698/zip.zipx", false, true))')
# btns = driver.find_elements_by_tag_name("a")
# for btn in btns:
#     btn.click()