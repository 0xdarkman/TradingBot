import SECRETS
from selenium import webdriver
from time import sleep, time
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys as keys


class NordnetScraperSelenium():

	payload = {"username": SECRETS.NORDNET_username, "password": SECRETS.NORDNET_password}
	nordnet_login_url = "https://classic.nordnet.no/mux/login/startNO.html?clearEndpoint=0&intent=next"

	stock_list_turnover = "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=turnover&sortOrder=desc&page=1&exchangeCountry=NO&exchangeList=no%3Aose"
	stock_list_change = "https://www.nordnet.no/market/stocks?selectedTab=prices&sortField=diff_pct&sortOrder=desc&page=1&exchangeCountry=NO&exchangeList=no%3Aose"

	def __init__(self):
		chrome_options = Options()
		#chrome_options.add_argument("--headless")
		chrome_options.add_argument("--window-size=%s" % "1920,1080")

		prefs = {"profile.managed_default_content_settings.images": 2}
		chrome_options.add_experimental_option("prefs", prefs)

		self.driver = webdriver.Chrome(executable_path='C:/Windows/chromedriver.exe',
		                               chrome_options=chrome_options
		                              )

	def login(self):
		self.driver.get(self.nordnet_login_url)
		sleep(1)

		self.driver.find_element_by_xpath('//*[@id="authentication-login"]/section/section[2]/section/section/section/div[2]/div/button').click()

		username = self.driver.find_element_by_xpath('//*[@id="username"]')
		username.click()
		username.send_keys(self.payload['username'])

		password = self.driver.find_element_by_xpath('//*[@id="password"]')
		password.click()
		password.send_keys(self.payload['password'])

		login_btn = self.driver.find_element_by_xpath('//*[@id="authentication-login"]/section/section[2]/section/section/section/section/section/section/form/section[2]/div[1]/button')
		login_btn.click()

		sleep(1)

		self.driver.get(self.stock_list_turnover)

	def create_email(self):
		self.driver.get('https://temp-mail.org/en/')
		sleep(5)

		email_address = self.driver.find_element_by_xpath('//*[@id="mail"]')
		email_address.click()
		email_address.send_keys(keys.CONTROL + 'c')

		self.driver.execute_script("window.open('','_blank');")

	def canYouMakeItSelector(self):
		second_window = self.driver.window_handles[1]

		self.driver.switch_to.window(second_window)
		self.driver.get('https://canyoumakeit.redbull.com/')
		sleep(5)

		team_sel = self.driver.find_element_by_xpath('//*[@id="inpt-search-applications"]')
		team_sel.send_keys(keys.ARROW_DOWN * 3)
		team_sel.click()
		team_sel.send_keys('Overcharged')
		team_sel.send_keys(keys.ENTER)

		body = self.driver.find_element_by_tag_name('body')
		body.send_keys(keys.ARROW_DOWN * 10)
		sleep(1)

		try:
			team_icon = self.driver.find_element_by_xpath('//*[@id="drop-applications"]/div[2]/div[1]')
			team_icon.click()
		except Exception:
			exc = True
			while exc:
				try:
					play_btn = self.driver.find_element_by_xpath('//*[@id="drop-applications"]/div[2]/div[3]')
					play_btn.click()
					exc = False
				except Exception:
					sleep(1)

		vote_button = self.driver.find_element_by_xpath('//*[@id="form-submit-vote"]/div/button')
		try:
			vote_button.send_keys(keys.ARROW_DOWN * 3)
		except Exception:
			pass
		sleep(1)
		vote_button.click()

	def login_not(self):
		sleep(random.randint(1, 3))
		log_mail = self.driver.find_element_by_xpath('//*[@id="email"]')
		sleep(random.randint(1, 3))
		log_mail.click()
		sleep(random.randint(1, 4))

		write_mail = self.driver.find_element_by_xpath('//*[@id="email"]')
		sleep(random.randint(1, 4))
		write_mail.send_keys(keys.CONTROL + 'v')
		sleep(random.randint(1, 5))
		write_mail.send_keys(keys.ENTER)
		sleep(random.randint(1, 2))

		write_name = self.driver.find_element_by_xpath('//*[@id="firstName"]')
		write_name.click()
		write_name.send_keys(firstname)
		sleep(1)

		write_name2 = self.driver.find_element_by_xpath('//*[@id="lastName"]')
		write_name2.click()
		write_name2.send_keys(lastname)
		sleep(1)

		write_pass = self.driver.find_element_by_xpath('//*[@id="password"]')
		write_pass.click()
		write_pass.send_keys("qwerty123")
		sleep(1)

		make_acc = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/form/button')
		make_acc.click()

		sleep(2)

	def verAndVote(self):
		base_window = self.driver.window_handles[0]
		self.driver.switch_to.window(base_window)
		self.driver.get('https://temp-mail.org/en/')
		sleep(3)

		email = self.driver.find_element_by_xpath(
			'/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a/span[1]')
		email.click()

		verify = self.driver.find_element_by_xpath(
			'/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/a')
		verify.click()
		sleep(2)
		whird_window = self.driver.window_handles[2]
		self.driver.switch_to.window(whird_window)
		sleep(1)
		clicky = self.driver.find_element_by_xpath('//*[@id="form-submit-vote"]/div/button')
		clicky.click()

		self.driver.close()


start_time = time()

bot = NordnetScraperSelenium()
bot.login()

print("--- %s seconds ---" % (time() - start_time))