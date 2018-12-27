# RoyalRoad Web Scraper

A web-scraping script for [RoyalRoad](https://www.royalroad.com) that checks for new chapters for user-specified novels. 
If a new chapter has been released, informs the user through email, in which the contents of the email are a link to the newly released chapter.

The code used for scraping the site, accessing chapter links, comparing with previous version, and updating the file, is all self-created. The GMail API was used to securely transmit the chapter link through an email to the user. 


### File info

**chap_list.txt:**  
Contains the links for the latest version of the chapters for each novel that was specified by the user.

**credentials.json:**
User credentials to securely log into the GMail platform.

**main.py:**
The actual code to run the script.

**novel_list.py:**
Contains the list of novels that the user wishes to be informed about. The novels are identified according to their Fiction ID and name.

**token.json:**
Token that contains the permissions to send an email through the GMail platform for the user.
