from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import time

# All paths that will be used :
srchbx = "//input[@id='search']"
fltr = "//div[@id='filter-button']"
chnl = "//div[@id='label'][@title='Search for Channel']"
chnlrn = "//ytd-channel-renderer[1]"
vds = "//yt-tab-shape[@tab-title='Videos']"

pt1 = "//ytd-app/div[1]/ytd-page-manager/ytd-browse[2]//div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row["
pt2 = "]/div/ytd-rich-item-renderer["
pt3 = "]//h3/a"

file1 = "input.txt"
file2 = "output.txt"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

# Returns True if the date is within 2 weeks and false otherwise
def retDateYng(text):
  t = 'null'
  for x in range(len(text)) :
    l = text[x:(x+4)]
    if l == 'view' :
      t = text[x+4:]
      if t[0] == 's' :
        t = t[2:]
      else :
        t = t[1:]

  try : 
    int(t[1])
    n = t[0:2]
    t = t[2:].strip() 
  except :
    n = t[0:1]
    t = t[1:].strip()

  num = int(n)
  if (num == 2 and (t[0:4] == 'week')) or (num < 16 and (t[0:3] == 'day')) or (t[0:4] == 'hour') or (t[0:3] == 'min') :
    return(True)
  else :
    return(False)
  

# Adds the desired data to the ouput file so we can see our most recent vids from our fav youtubers
def addtofile(title, stats, link, file) :
  fl = open(file, 'a')
  fl.write('Video Title: ' + title + '\n')
  fl.write('Stats: ' + stats + '\n')
  fl.write(link + '\n\n')
  fl.close()


# After routing to the desired page we can grab the thumbnail title and date info and calls retDateYng() then addtofile() when ret is true
def grabvd() :
  i = 0
  yng = True
  while yng :
    j = 1
    i+=1
    while j < 5 :
      try :
        vid = driver.find_element(By.XPATH, (pt1 + str(i) + pt2 + str(j) + pt3))
        ttl = vid.get_attribute('title')
        arlb = vid.get_attribute('aria-label')
        txt = arlb.replace(ttl,'').strip()
        hrf = vid.get_attribute('href')

        yng = retDateYng(txt)
        if not yng :
          break

        addtofile(ttl, txt, hrf, file2) 
      except :
        break
      finally :
        j+=1


# Routes to youtube channel of the top user related to the user input and calls grabvd()
def srch(input) :
  driver.get("http://youtube.com")
  search = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, srchbx)))
  time.sleep(0.5)
  search.clear()
  search.send_keys(input)
  search.send_keys(Keys.ENTER)
  print("searching for " + input + ': ', end='')
  try :
    wait.until(EC.element_to_be_clickable((By.XPATH, fltr))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, chnl))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, chnlrn))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, vds))).click()
  finally :
    time.sleep(0.5)

  grabvd()
  print('done')
  

# grabs the input file filled with users inputed youtubers and calls srch() 
def checkList(fname) :
  f = open(fname, 'r')
  for x in f :
    srch(x.strip())
  f.close()

#Make sure output file is cleared
f = open(file2, 'w')
f.write('')
f.close()

#Run
checkList(file1)

print('finished program')
driver.quit()