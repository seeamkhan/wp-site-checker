#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import Conf_Reader
import os, time
import requests


def wp_checker():
    site_name = 'Rethinkhealth'
    admin_login = False
    site_is_up = False
    wp_site_status = False
    wp_checker_log = ''
    message = []
    start_time = str(datetime.now())
    message.append("Site tested at %s" %start_time)
    # message.append('%s site is checking, please wait...' %site_name)
    print '%s site is checking, please wait...' %site_name
    wp_url = "http://rth.dev.lin.panth.com"

    # Site is UP checking
    status = "Unknown"
    try:
        req = requests.get(wp_url)
        status = req.status_code, req.reason
        site_status = str(status)
        if site_status == "(200, 'OK')":
            wp_site_status = True
            message.append("Rethinkhealth site status: %s" % site_status)
            print "Rethinkhealth site status: %s" % site_status
        else:
            message.append("Rethinkhealth Site status: %s" % site_status)
            print "Rethinkhealth site status: %s" % site_status
    except requests.exceptions.ConnectionError as e:
        message.append("%s site is not responding." % site_name)
        print "%s site is not responding." % site_name

    if wp_site_status is True:
        driver = webdriver.PhantomJS()
        # driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(wp_url)

        # Site elements
        page = "//div[@id='page']"
        site_logo = ".//div[@class='branding']"
        navbar = ".//*[@class='navbar']"


        """Check site elements was loaded properly."""

        # Check site page element loaded properly.
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, page)))
            site_is_up = True
        except:
            # site_is_up = False
            message.append("Error! %s site did not load." % site_name)
            print "Error! %s site did not load." % site_name

        # Check site logo loaded properly.
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, site_logo)))
            site_is_up = True
            message.append("%s site logo loaded." % site_name)
            print "%s site logo loaded." % site_name
        except:
            # site_is_up = False
            message.append("Error! %s site logo did not load." % site_name)
            print "Error! %s site logo did not load." % site_name

        # Check site navbar loaded properly.
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, navbar)))
            site_is_up = True
            message.append("%s site navigation bar loaded properly." % site_name)
            print "%s site navigation bar loaded properly." % site_name
        except:
            # site_is_up = False
            message.append("Error! %s site navigation bar did not load." % site_name)
            print "Error! %s site navigation bar did not load." % site_name

        if site_is_up is True:
            site_is_up_message = 'Verified Rethinkhealth site is up and running.'
            message.append(site_is_up_message)
            print site_is_up_message

            # Admin login test
            driver.get("http://rth.dev.lin.panth.com/wp-admin")
            login_email_field = 'user_login'
            login_pass_field = 'user_pass'
            login_button = 'wp-submit'
            wp_admin_bar = "wpadminbar"

            # Get username and password from the credential file
            credentials_file = os.path.join(os.path.dirname(__file__), 'login.credentials')
            username = Conf_Reader.get_value(credentials_file, 'LOGIN_USER')
            password = Conf_Reader.get_value(credentials_file, 'LOGIN_PASSWORD')
            print username
            print password


            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, login_email_field)))
            except:
                message.append('Error! Username or Email field does not load.')
                print 'Error! Username or Email field does not load.'

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, login_pass_field)))
            except:
                message.append('Error! Password field does not load.')
                print 'Error! Password field does not load.'

            driver.find_element_by_id(login_email_field).clear()
            driver.find_element_by_id(login_email_field).send_keys(username)
            driver.find_element_by_id(login_pass_field).clear()
            driver.find_element_by_id(login_pass_field).send_keys(password)
            driver.find_element_by_id(login_button).click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, wp_admin_bar)))
                admin_login = True
                message.append('Successfully logged in as Admin.')
                print 'Successfully logged in as Admin.'
            except:
                message.append('Login as Admin failed.')
                print 'Login as Admin failed.'
            if admin_login is True:
                # WP Version check
                # Page elements
                dashboard = "//h1[contains(text(), 'Dashboard')]"
                wp_version_id = "wp-version"

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, dashboard)))
                except:
                    message.append('Error! %s admin dashboard did not load.' % site_name)
                    print 'Error! %s admin dashboard did not load.' % site_name

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, wp_version_id)))
                    wp_version = driver.find_element_by_id(wp_version_id).text
                    wp_version_message = "Rethinkhealth Current WordPress Version is: " + wp_version + "."
                    if wp_version == "":
                        driver.find_element_by_xpath(".//*[@id='dashboard_right_now']/button[@type='button']").click()
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, wp_version_id)))
                        wp_version = driver.find_element_by_id(wp_version_id).text
                        wp_version_message = "Rethinkhealth Current WordPress Version is: " + wp_version + "."
                    message.append(wp_version_message)
                    print wp_version_message
                    # print "Rethinkhealth Current WordPress Version is: " + wp_version + "."
                except:
                    message.append('Error! Rethinkhealth WordPress version message did not found.')
                    print 'Error! Rethinkhealth WordPress version message did not found.'
            else:
                pass

        elif site_is_up is False:
            message.append('Rethinkhealth WordPress site did not load properly.')
            print 'Rethinkhealth WordPress site did not load properly.'

        driver.save_screenshot("wp-screen.png")

        # time.sleep(2)
        driver.quit()
    else:
        pass
    wp_checker_log = '\n'.join(message)

    """
    Function for writing the final output in a file named 'plugin_report.txt'.
    New file will be created if the file is not already exist.
    :param something: final output string
    """
    target = open("wp-checker-log", 'a')
    # target.truncate()
    target.write("\n\n%s" % wp_checker_log)
    target.close()
    return wp_checker_log


def email_sender(wp_checker_log):
    email_log = ''
    message = []
    email_body = wp_checker_log
    # Get username and password from the credential file
    credentials_file = os.path.join(os.path.dirname(__file__), 'login.credentials')
    email_username = Conf_Reader.get_value(credentials_file, 'EMAIL_USER')
    email_password = Conf_Reader.get_value(credentials_file, 'EMAIL_PASSWORD')

    message.append('The automated email is sending, please wait...')
    print 'The automated email is sending, please wait...'
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    # driver.maximize_window()
    base_url = 'https://gmail.com/'
    driver.get(base_url)

    # enter email
    driver.find_element_by_id('Email').clear()
    driver.find_element_by_id('Email').send_keys(email_username)

    # click next
    driver.find_element_by_id('next').click()
    time.sleep(2)

    # enter password
    driver.find_element_by_id('Passwd').clear()
    driver.find_element_by_id('Passwd').send_keys(email_password)

    # click login
    driver.find_element_by_id('signIn').click()

    # verify inbox present
    basic_compose_link = ".//*[@accesskey='c']"
    # basic_compose_link = "//a[contains(text(), 'Compose Mail')]"
    new_compose_link = "//div[contains(text(), 'COMPOSE')]"
    final_compose_link = "html/body/table[3]/tbody/tr/td[1]/table[1]/tbody/tr[1]/td/b/a"

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, basic_compose_link))
        )
        final_compose_link = basic_compose_link
    except:
        message.append('Basic Compose button not found, maybe login failed!')
        print 'Basic Compose button not found, maybe login failed!'

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, new_compose_link))
            )
            final_compose_link = new_compose_link
        except:
            message.append('Compose button not found, maybe login failed!')
            print 'Compose button not found, maybe login failed!'

    # Click gmail Compose button
    driver.find_element_by_xpath(final_compose_link).click()

    # verify gmail composer box appears
    to_field = ".//*[@id='to']"
    cc_field = ".//*[@id='cc']"
    subject_field = ".//*[@name='subject']"
    body_field = ".//*[@name='body']"
    send_button = ".//*[@value='Send']"
    sent_confirmation = ".//*[contains(text(), 'Your message has been sent.')]"

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, to_field))
        )
    except:
        message.append('To field not found, maybe composer box load failed!')
        print 'To field not found, maybe composer box load failed!'
    send_to_emails = 'panth.me@gmail.com; jilani@dev.panth.com'
    driver.find_element_by_xpath(to_field).clear()
    driver.find_element_by_xpath(to_field).send_keys(send_to_emails)
    driver.find_element_by_xpath(subject_field).clear()
    driver.find_element_by_xpath(subject_field).send_keys('Rethinkhealth WordPress WordPress Update Notification Email')
    driver.find_element_by_xpath(body_field).clear()
    driver.find_element_by_xpath(body_field).send_keys(email_body)

    try:
        all_send_buttons = driver.find_elements_by_xpath(send_button)
        all_send_buttons[0].click()
    except:
        message.append('Send button was not clicked')
        print 'Send button was not clicked'

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sent_confirmation)))
    except:
        message.append('Email sent failed!')
        print 'Email sent failed!'

    # time.sleep(1)
    # driver.save_screenshot('Email-screenshoot.png')  # save a screenshot to disk
    driver.quit()
    message.append('Email Job completed.')
    print 'Email Job completed.'


    email_log = '\n'.join(message)
    """
    Function for writing the final output in a file named 'plugin_report.txt'.
    New file will be created if the file is not already exist.
    :param something: final output string
    """
    target = open("wp-checker-log", 'a')
    # target.truncate()
    target.write("\n%s\n" % email_log)
    target.close()

wp_checker_log = wp_checker()
email_sender(wp_checker_log)
