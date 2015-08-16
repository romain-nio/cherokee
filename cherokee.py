from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import json

driver = webdriver.Firefox()
driver.implicitly_wait(10) # seconds

class train:
    
    def __init__(self, departure_time, arrival_time, price):
        self.button_id = departure_time
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        #compute duration
        t1 = datetime.time(int(departure_time[0:2]),int(departure_time[3:5]))
        t2 = datetime.time(int(arrival_time[0:2]),int(arrival_time[3:5]))
        dummydate = datetime.date(1990,8,9)
        duration = datetime.datetime.combine(dummydate,t2) - datetime.datetime.combine(dummydate,t1)
        self.duration_sec = duration
        self.price = price
        
    def displaytrain(self):
        print('Departure: {}, arrival: {}, duration: {}, price {}'.format(self.departure_time,\
                                                                         self.arrival_time,\
                                                                         self.duration_sec,\
                                                                         self.price))
def load_configuration(filename) :
    filename = 'configuration/%s.json' % filename
    with open(filename) as data_file:    
        return json.load(data_file)

        
def generate_based_url(base_url, departure, arrival,
                       departure_date, departure_min_time,
                       return_date, return_min_time):
    url = base_url+departure+'/'+arrival+'/'+departure_date\
    +'-'+departure_min_time+'/'+return_date+'-'+return_min_time
    return url



def authentification(signin_page, login, password) :
    # visit login page
    driver.get(signin_page)

    # enter credentials
    log_box = driver.find_element_by_xpath("//input[@placeholder='Adresse email']")
    log_box.send_keys(login)
    pass_box = driver.find_element_by_xpath("//input[@placeholder='Mot de passe']")
    pass_box.send_keys(password)

    # validate
    driver.find_element_by_xpath("//button[contains(.,'Se connecter')]").click()
    
def search_trip(trip_url) :
    # Search for the user trip
    driver.get(trip_url)
    driver.find_element_by_xpath("//button[contains(.,'Rechercher')]").click()
    
    schedule=driver.find_elements_by_xpath("//span[@class='time']")
    secondclass_price=driver.find_elements_by_xpath("//div[@class='ember-view third' or @class='ember-view third best-price']")

    train_list = []
    try: #what if no price for a train ?
        for i in range(len(schedule)):
            dep_time, arr_time = schedule[i].text.split('➔')
            second_price = secondclass_price[i].text
            train_list.append(train(dep_time.strip(), arr_time.strip(), second_price))
    except:
        pass
        
    return train_list
        
def choose_train(train_list):
    #still to do
    random = 0
    return train_list[random]

def add_to_cart(train):
    departure = train.departure_time
    driver.find_element_by_xpath("//span[contains(.,'"+departure+"')]").click()
    driver.find_element_by_xpath("//button[contains(.,'Choisir')]").click()
    driver.find_element_by_xpath("//button[contains(.,'Ajouter au panier')]").click()


def buy_ticket(cardholder, expirationdate, cardnumber, cardcvv):
    driver.find_element_by_xpath("//button[contains(.,'Payer')]").click()
    # fill credit card
    driver.find_element_by_id('cardnumber').send_keys(cardnumber)
    driver.find_element_by_id('cardexpirationdate').send_keys(expirationdate)
    driver.find_element_by_id('cardcvv').send_keys(cardcvv)
    driver.find_element_by_id('cardholder').send_keys(cardholder)
    driver.find_element_by_id("cb-agree-to-terms").click()
    driver.find_element_by_xpath("//button[contains(.,'Payer')]").click()

def main():
    # GLOBAL variables : read configurations
    user_config = load_configuration("user-preferences")
    account = load_configuration("account")
    common_config = load_configuration("common")

    root_url = common_config['root_url']
    login = account['login']
    password = account['password']
    signin_page = common_config['signin_page']

    base_url = common_config['landing_page']
    departure = user_config['departure']
    arrival = user_config['arrival']
    departure_date = user_config['departure_date']
    departure_min_time = user_config['departure_min_time']
    return_date = user_config['return_date']
    return_min_time = user_config['return_min_time']
    trip_url = generate_based_url(base_url, departure, arrival, departure_date,
                                 departure_min_time, return_date, return_min_time)



    # force language to #FR
    driver.get(root_url)
    # visit login page and enter user credentials
    authentification(signin_page,login,password)
    # search for a trip according to user preferences
    trains=search_trip(trip_url)
    train = choose_train(trains)
    add_to_cart(train)
    buy_ticket('lili', ' 01/19', '143256743342345', '123')
    
if __name__=='__main__':
    main()
