from selenium import webdriver
from time import sleep as sl
from selenium.webdriver.chrome.options import Options

class crawler:
  def __init__(self):
    chrome_options=Options()
    # 無頭模式，防止Heroku執行webdriver時崩潰的情況
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    self.__driver=webdriver.Chrome(chrome_options=chrome_options)
    self.__information="""
      dcard Linebot v1
    """
  # __information回傳的資訊
  @property
  def information(self):
    return self.__information
  def get_forumList(self):
    forumList=[]
    with open("forum.csv","r",encoding="utf-8") as f:
      for line in f.readlines():
        if line=="\n":
          continue
        forumList.append(line)
    return forumList
  def __close(self):
    sl(0.5)
    self.__driver.close()
  def crawl_specific_form(self,name):
    forumList=self.get_forumList()
    for i in forumList:
      if i.split(",")[0] in name:
        link=i.split(",")[1]
        break
    else:
      self.__close()
      return "汪汪!"
    self.__driver.get(link)
    sl(0.5)
    r_list=self.__driver.find_elements_by_xpath(' //*[@id="__next"]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div')
    xStr=""
    for article in r_list:
      try:
        title=article.find_element_by_xpath('./article/h2/a/span').text
        href=article.find_element_by_xpath('./article/h2/a').get_attribute('href')
        motion=article.find_element_by_xpath('./article/div[3]/div[1]/div/div[2]').text
        response=article.find_element_by_xpath('./article/div[3]/div[2]/div/span').text
        xStr +="\n".join([title,href,motion,response])
      except Exception as e:
        pass
    self.__close()
    return xStr