# Lionbooks
***

### Pre-coding, research, inspiration
***
I first began with reading through the sources given to me by my teacher about coding e-commerce sites! It was really helpful, and I went on to look at Goodreads (which I spent a lot of time on the page source to get a similar aesthetic for Lionbooks), Etsy, and Redbubble!

### Implementation
***
Starting off, I used the files from the finance project as a strong base for the website, as I knew that there were similarities between the finance project and the lionbooks project. I copied and pasted layout.html from finance just as a starting point, but ended up making many changes, especially to the navigation bar. Like the finance project, the whole project was coded with Python, SQL, Javascript, HTML, and CSS!

##### Database
***
To help me out with organization, I made a checklist in google docs of what I wanted to accomplice. I began with setting up the database with 3 tables: users, myBooks, and library. I created users just to hold information about each user for logins, then myBooks for connecting isbn to user_id, and finally library to hold more complete information about each registered book. Though there was a primary key for users to identify a user from another, I ended up taking out any unique or primary key in myBooks and library as I know that many people own duplicates of the same book.

##### Connecting to the API + helpers.py
***
This part was one of the trickiest, and I struggled with it for a very long time. After researching how the Google Cloud API worked, I found out how I needed to fashion the URL in the lookup function of helpers.py in a certain way to obtain the information I needed. I also ended up not using the API key in the url itself as it would result in a lack of information.

Most of the helpers.py functions were similar to the ones in the finance project. However, I added one more separate function: strOfAuthors() that takes in the list of authors given by lookup() and returns it as a string. This was so that I could easily store it into my database as TEXT and display it easily as well.

##### Icon for the tab
***
I knew I wanted something similar to the bag of money favicon used in the finance project for Lionbooks, so I implemented a book version of the favicon!

##### App.py
***
The index page is coded so that the there are different instructions for when the user is entering the homepage vs. clicking on the "details" button of the homepage. Everytime the index/homepage is loaded, the python code obtains the the book information from both myBooks and library to display the updated list of books. This is so that when a book is removed or added, the index page is immediately updated. In terms of why I coded in a details button for each book, it was so that there would be some convenience in handling the books from a user's personal library, instead of again having to search up the isbn for that book. The details button also returns the value of the isbn of its row, allowing me to obtain the isbn needed to access information from the database. The layout of the table displaying the books was made to look similar to the layout of Goodreads.

The search route is triggered when the search button is clicked, where it then error-checks to see if an apology message should show up or redirect the user to the correct information page of the valid isbn. Per the advice left on my finance project, I wanted to see if I could use try... except... for some of the error-checking, but unfortunately struggled to find a solution dealing with non-integer elements. I will definetly work on using that to cut down some of my code!

The info route took the longest to code, as it has a lot of buttons on the page. Making sure that the isbn was coded in as the value of the buttons was the key to connecting the book information. It allowed me to accordingly add or remove the book. I tried my best with cutting out the redundancies in the info route, but still ended up with some (maybe needed) duplications of code. I also believed it to be easiest to create different routes for each shelf, but I will work on ways to make the code more efficient and leaner in the future as well.


##### Styles.css
***
Tinkering around with Bootstrap and W3Schools tutorials allowed me to connect CSS, HTML, and Javascript (sometimes) to create effects like the "sticky" navigation bar, the shelves becoming highlighted a darker beige when hovered over and also when the page is the active page, hover-over colors of the table rows and buttons, dropdown button groups, search bar with a search bar icon, and more! The decision to make the navigation bar "sticky" was because I noticed that it was like that in Goodreads and also the side bar, which follows the user as they scroll down, would look weird without the navigation bar also being "sticky" as well. I chose a Times New Roman font and a beige color to kind of give the aesthetic of an old, yellowed-out page of a book feel. Other decisions on style was based off of just wanting to add a profesionality or clean, smooth look to the website.
