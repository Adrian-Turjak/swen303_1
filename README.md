## SWEN 303 Assignement 1:

My advice is not to try running this at uni. The uni computers do not allow you sudo access to install python packages via pip, and pacman does not have up-to-date python packages. Pip + venv would be ideal, but we can't install venv either.

If you do want to run it, this is just a standard Django app, and there is a requirements file (although some of those do pre-depend on certain system libraries and may throw installer errors). If you need help getting it to run, email me.

If you just want to see the site and play with it. Click the hosted_demo.html file and it will redirect you to a hosted demo of the site. If for some reason that isn't working, poke me and I'll check it. Url is also: http://150.242.40.236/

There is also an html redirect for the git repo for this project, and the url is also: https://github.com/Adrian-Turjak/swen303_1


Project itself is a standard Django site. Nothing fancy. Uses Bootstrap, and the BaseX client I am using is the official python example client that is in the BaseX github repo.

I decided against node.js because while I am familiar with it, I prefer python and Django. If you have questions, feel free to get in touch.


I will point out that BaseX is awful. Nothing makes any sense. Commands that work for others don't work for me. I spent ages beating my head against this fowl thing and gave up. My focus became on making the site work, look good, and make sense. Most of my code is setup to work if I had known how to do things properly with the database, or working around the database. Given this was meant to be an assignment about UX and user interface design I'm quite annoyed at this awful choice of software for the basis (BaseX that is, node.js is fine).


### Work Completed:

* Core
  * Scenario One:
    * Done
  * Scenario Two:
  	* Done
  * Scenario Three:
  	* Done

* Completion
  * Scenario One:
    * Done
  * Scenario Two:
  	* Partly Done. 
  	* I couldn't figure out how to do this with the database, but most of the code for it is prepped, and I even store the old search on the result html page as part of the refined search form in a hidden input, so doing the refine search is pretty much done, just needs the specific database call to make sense of it.
  * Scenario Three:
  	* Done, but not working.
  	* Both the site, and the server side is ready for this. Problems being that for some reason the database isn't replacing the given XML, and also I can't do validation because I was unable to find a suitable schema file. The validation code is there, just commented out because I don't have the schema file.

* Challenge
  * Scenario One:
  	* Not Done
  * Scenario Two:
  	* Done, although "my searches" is determined by ip address. Ideally I'd swap this to be cookie based.
  	* Regardless, works well, and because of my searches being get requests and in the url itself, I can easily link back to the searches.
  * Scenario Three:
  	* Not Done
  * Scenario Four:
    * Not a requirement but my searches are all url parameters so you can easily link the search itself and share results. I felt this was important and useful.
    * There is probably more random UX stuff that I though would be better for the site as a whole and to make a few of the other scenario's better, but for the life of me I can't remember them right now.
