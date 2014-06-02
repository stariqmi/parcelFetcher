from selenium import webdriver

url = "https://www.biz.indygov.org/treasurer/property/propSearch.aspx"
driver = webdriver.PhantomJS()

list_file = open("list.txt")
addresses = list_file.readlines()

results_file = open("parcels.tsv","w")
results_file.write("Parcel#\tAddress\n")

for addr in addresses:
	# Extract Street Number and Name
	split_addr = addr.split()
	street_num = split_addr[0]
	street_name = " ".join(split_addr[1:])

	# Start navigating to search
	driver.get(url)
	driver.find_element_by_xpath('//*[@id="rdoSearchAddr"]').click()
	driver.find_element_by_xpath('//*[@id="ctl00_cphMain1_btnStart"]').click()
		
	# Debug:
	print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
	print "Searching ..."
	print "Street Number: {0}\nStreet Name: {1}".format(street_num, street_name)

	driver.save_screenshot("search.png")

	# Fill form with above information
	driver.find_element_by_xpath('//*[@id="ctl00_cphMain1_txtStreetNo"]').send_keys(street_num)
	driver.find_element_by_xpath('//*[@id="ctl00_cphMain1_txtStreetName"]').send_keys(street_name)
	driver.save_screenshot("filled_form.png")

	# Execute Search
	driver.find_element_by_xpath('//*[@id="ctl00_cphMain1_btnSearch"]').click()
	driver.save_screenshot("results.png")

	# Extract Parcel Number if results found:
	rows = driver.find_elements_by_class_name("parcelRow")
	if len(rows) > 0:
		tds = rows[0].find_elements_by_tag_name("td")
		parcel_num = tds[3].text.strip()
		print "Parcel # {0} found for Address: {1}".format(parcel_num,addr)
		results_file.write(parcel_num + "\t" + addr + "\n")
	else:
		print "No results found for Address: {0}".format(addr)
		