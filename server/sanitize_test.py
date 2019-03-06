import unittest
import sanitize as s
import logging
import json
import psycopg2
import datetime
from psycopg2.extensions import AsIs

class sanitizeTest(unittest.TestCase):

    def test_cookieCheck(self):
        logging.info("Test cookieCheck")
        # This function only calls checkHashCookie and checkTimeCookie
        # Should work if checkHashCookie and checkTimeCookie is working

    def test_getHashCookie(self):
        logging.info("Test getHashCookie")
        sanitizer = s.Sanitizer()

        # Should generate and print 3 different cookies
        cookie = sanitizer.getHashCookie()
        print("cookie 1", cookie)
        
        cookie = sanitizer.getHashCookie()
        print("cookie 2", cookie)
        
        cookie = sanitizer.getHashCookie()
        print("cookie 3", cookie)
        
        self.assertNotIn(sanitizer.getHashCookie(), sanitizer.getHashCookie())


    def test_checkHashCookie(self):
        logging.info("Test checkHashCookie")
        sanitizer = s.Sanitizer()
         
        cookieHash1 = sanitizer.getHashCookie().decode('utf-8')
        self.assertTrue(sanitizer.checkHashCookie(cookieHash1))

        # hash generated by sanitizer with some characters changed, should be unvalid
        cookieHash2 = "$2b$12$swUd.H2yI1GFO05h/946o.v8qJS4eQE8y0fMxt5u2Nr433wAGWQDW"
        self.assertFalse(sanitizer.checkHashCookie(cookieHash2))


    def test_checkTimeCookie(self):
        logging.info("Test checkTimeCookie")
        sanitizer = s.Sanitizer()

        # must be on the form "%Y-%m-%d %H:%M:%S" --> example "2019-01-01 00:00:00"
        # based on sanitize.__TIME_BETWEEN_POSTS = 10 (seconds)
        
        # Check now
        now = datetime.datetime.now()
        cookieTime = now.strftime("%Y-%m-%d %H:%M:%S")        
        self.assertFalse(sanitizer.checkTimeCookie(cookieTime))

        # Check tomorrow
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        cookieTime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.assertFalse(sanitizer.checkTimeCookie(cookieTime))

        # Check now minus 9 seconds
        now = datetime.datetime.now() - datetime.timedelta(seconds=9)
        cookieTime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.assertFalse(sanitizer.checkTimeCookie(cookieTime))

        # Check now minus 10 seconds
        now = datetime.datetime.now() - datetime.timedelta(seconds=10)
        cookieTime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(sanitizer.checkTimeCookie(cookieTime))

        # Check some day in the past
        cookieTime = "2019-01-01 00:00:00"
        self.assertTrue(sanitizer.checkTimeCookie(cookieTime))


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    unittest.main()
