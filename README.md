# Lionbooks
***
An online platform for readers interested in decluttering their own library and sharing their books. Readers have the option to lend out their own books or to borrow another's.

### Background
***
Inspired by my love for Goodreads and public libraries! For those unfamiliar with Goodreads, their website describes it like this: "Find and read more books you'll love, and keep track of the books you want to read. Be part of the world's largest community of book lovers on Goodreads."

What's Lionbooks? Imagine if Goodreads and your favorite public library had a child! This site allows users to make a community of readers online in this "e-library", where they can lend out and borrow books inside the community! Also, with three shelves: "Currently Reading", "Want-To-Read", and "Read", readers can also use the web site as a organizational tool for their own books.

### Setup
***
Unfortunately, running this project requires a google account so that you can access the API key for Google Books, where book information is obtained from.

First, Aquire an API key:
(For more information, visit https://developers.google.com/books/docs/v1/using)
1. Visit the Google Cloud Credentials Page: https://console.cloud.google.com/projectselector2/apis/credentials?supportedpurview=project. The site may ask you to sign in with a google account, and if you have one, please do so.

2. If this is your first time in Google Cloud, there should be no credentials in the page as you haven't created any projects yet. Click on "create project" and select any name and ID you want (Google Cloud may give you an id based on the name you choose, and that's totally fine). You can also choose any organization or do nothing for it, as well.

3. Once you've created a project, you should be redirected to the credentials page of your project. Near the top of the screen should be "+ Create Credentials". Click on that, then choose "API KEY" from the dropdown choices.

4. Copy your API Key from the pop-up. Feel free to close the pop up as well, as you can always access it by clicking "Show Key" from the list of API Keys in your project credentials page.

Next, open up the CS50 codespace. There, download the project, unzipping it if needed.

In your terminal, type in:
```
$ cd
$ cd lionbooks
lionbooks/ $ export API_KEY=value
```
!! "value" should be replaced by your API key that you copied from Google Cloud.

Next, type in the terminal to run Flask's built-in server:
```
$ flask run
```

The terminal should now have a link that you can COMMAND click on to open the lionbooks site on a new tab.
It might look something like: Running on https://......


### Navigating Lionbooks
***
Congratulations! You're in the Lionbooks website! (Peep the cute stack of books favicon decorating the tab of the website!)

The link should direct you to the login page. The ISBN search bar is login-required, so unless you've already logged in, the search bar shouldn't work for now. Feel free to click on "library" in the navigation bar to browse the library, but no worries if there's no books in there now–later, as you add books to your "my Books" page, they should pop-up in the library, as well!

#### Registering
***
Click on register to create an account. After entering in a valid username and password of your choice as well your email (so others can contact you to borrow your books), you should be logged in!


##### Library vs. My Books
***
If you're confused on the difference between My Books, your PERSONAL library, vs. the "library" in the navigation bar, think of it like this: All the books in My Books are in the "library". However, the books in the "library", which holds ALL the books in the community, won't be in YOUR personal My Books. This is because the library is where readers go to find books they want to borrow! My Books is your own personal library that only holds the books in YOUR real life bookshelves. They can also be organized into three online bookshelves, so it's just for your own organizing needs!


#### Home
***
The page you're at once you register or login, is the homepage. It's also the page you're directed to when you click the logo. The home page displays all the books that you've added to your personal library: My Books. When you first enter the website, it should be empty as you haven't added any books to your personal library yet!

Feel free to play around with the different shelves on the left side of your home page. The shelves should become highlighted when you click on them, indicating you're in that shelf! 'My Books' lists all your books, regardless of which shelf it's in. "Currently Reading" are the books you're (quite obviously, maybe) currently reading. "Want To Read" will display books on your TBR list, and "Read" displays books that you've finished!

#### Searching and Information Page
***
Let's add a book that we own to our online personal library! Find the isbn of the book that you want to add and enter it into the search bar above. As an example, let's do an isbn that represents an edition of "Animal Farm": 9781529038224.

Once you click enter or the search icon, a page with all the information about the searched book should pop-up. In our case, you should see "Animal Farm by George Orwell" with an image of the cover as well as a description of the book below it. The isbn, just in case you want a reminder, is also listed at the bottom of the page.

#### Adding to My Books
***
Below the isbn, however, should be two buttons: "Add to My Books" and "Remove From My Books". You can click on the remove button, but you should get an error–which makes sense, given that you don't own this book online yet! Though we can just add this book to My Books by clicking on the add button, let's add it to a specific shelf. The add button is actually a dropdown, so click on the dropdown button to see the different shelves you can directly add it to. In this example, lets click "Currently Reading" (of course, feel free to do differently if you want)!

Once you click any button, however, you should be redirected to the home page, where the book that you've just added should be displayed! If you click on the shelf that you added it to, it should be displayed there too. Add as many books as you want (you can add the same book twice, if you have duplicates of the book in real life as well!) and also know that you can click on the "details" button of any book to go back to the specific information page for that book!

#### Borrowing from the Library
***
The book that you've just added isn't just in your personal library, however. Click on "library" in the navigation bar to see it displayed there, alongside a link that directs anyone to email you about borrowing the book! Be sure to check your email frequently, so that you can respond to any interested readers! If you do see other books that aren't your own displayed there, that's also good news! If you see a book you'd like to borrow, click on the link "Request to borrow" and you should be redirected to a page that allows you to send an email to that person. Also keep in mind that you can click on the details button of each book to get more information!

#### Removing from My Books
***
Let's say something like this happened in real life: your annoying sibling stole "Animal Farm" from you room, and accidentally ruined it! This means it's not available for borrowing anymore, so let's take it out of My Books (which also means it'll be taken off from the library).

Click on the Lionbooks logo to be taken to the homepage. Click on "details" in the row for "Animal Farm", and you should be taken to the information page for that book. Scroll to the bottom of the page where the "Remove from My Books" button is and click on it. This time, instead of getting an error message about not owning the book, you should be redirected to your home page "My Books" and "Animal Farm" should be gone from your list of books! If you click on "library" in the navigation bar again, you should see that it's gone from there as well!

#### Ending Note
***
I really hope you enjoy exploring the website! If I had more time, I would have added more into it like the ability to comment and make discussion boards for each book. That'll be on my to-do list for sure!

Here is the link to the youtube video presenting Lionbooks!
https://youtu.be/n97lBt_T85o