import mechanize
# generate a new mechanize Browser instance
if __name__ == '__main__':
    br = mechanize.Browser() # Set browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_redirect(mechanize.HTTPRedirectHandler)
    br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1) # Open the login URL
    br.open("https://db.tt/tr6esxYv")
    for link in br.links():
        if link.text == "Submit":
            br.follow_link(link) # Select the 1st form
    br.select_form(nr=3)
    # Enter the username and password
    import pdb
    pdb.set_trace()
    print br
    # br"fname" = 'test'
    # br"lname" = 'test2mechanize'
    # # Submit the form
    # response = br.submit()
    # print response.read()