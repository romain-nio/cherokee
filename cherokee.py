from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json


driver = webdriver.Firefox()

def payment_process() :
    time.sleep(10)

    driver.find_element_by_xpath("//button[contains(.,'Payer')]").click()
    time.sleep(10)
    # fill credit card
    driver.find_element_by_id('cardnumber').send_keys("439438509348985093534")
    driver.find_element_by_id('cardexpirationdate').send_keys("03/10")
    driver.find_element_by_id('cardcvv').send_keys("511")
    driver.find_element_by_id('cardholder').send_keys("ROMAIN NIO")
    driver.find_element_by_id("cb-agree-to-terms").click()

def load_configuration(filename) :
    filename = 'configuration/%s.json' % filename
    with open(filename) as data_file:    
        return json.load(data_file)


def generate_based_url():
    print (user_config)
    url = common_config['landing_page']\
    +user_config['departure_date']+'-'+user_config['departure_min_time']+'/'\
    +user_config['return_date']+'-'+user_config['return_min_time']

    return url

def authentification() :
    # visit login page
    driver.get(common_config['signin_page'])

    time.sleep(2)

    # enter credentials
    log_box = driver.find_element_by_xpath("//input[@placeholder='Adresse email']")
    log_box.send_keys(account['login'])
    pass_box = driver.find_element_by_xpath("//input[@placeholder='Mot de passe']")
    pass_box.send_keys(account['password'])

    # validate
    driver.find_element_by_xpath("//button[contains(.,'Connexion')]").click()
    time.sleep(7)

def find_trip() :
    # generate URL of the trip
    trip_url = generate_based_url()

    driver.get(trip_url)
    time.sleep(7)
    driver.find_element_by_xpath("//button[contains(.,'Rechercher')]").click()
    time.sleep(7)
    driver.find_element_by_xpath("//button[contains(.,'Choisir')]").click()
    time.sleep(7)
    driver.find_element_by_xpath("//button[contains(.,'Ajouter au panier')]").click()

def main():
    

    print(account)
    # force language to #FR
    driver.get(common_config['root_url'])

    # visit login page and enter user credentials
    authentification()

    # find trip according to user preferences
    find_trip()

    payment_process()

# GLOBAL variables : read configurations
user_config = load_configuration("user-preferences")

account = load_configuration("account")

common_config = load_configuration("common")


if __name__ == "__main__":  
    main()