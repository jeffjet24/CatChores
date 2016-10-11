# CatChores
A Cat Chore Management Application


This repo contains the source code for a small side project that I have been working on. 

This project is for a kiosk-like Raspberry Pi project that helps keep track of what cat chores have been completed and when. This is useful for me because I live in an apartment with 4 other people, and we are looking to get a second cat. With getting the second cat, everyone has volunteered to help take care of both cats. In everyone helping take care of the cats, this tool will help communicate which chores have already been done, or need to be done. 

### High Level Ideas:
#### Colors of Panels:
The colors of the panels/buttons on the user interface are to indicate whether the cat chores have been done recently (green, aka success), need to be done soon but are not overdue (yellow, aka warning), and when the chores are past due (red, aka danger). 
#### Timeframes of the chores:
Certain chores need to be done more often than others, so I have come up with timeframes that reflect the frequency of different chores:
* Feeding AM and PM: 24 hours from the last time that each one was done. For example: 24 hours from the last AM feeding until the next AM feeding needs to be done again. 
* Litter boxes: Litter box cleanout is determined overdue after 3 days from the last time that it was done. At Yellow status between 48 and 72 hours.
* Vacuuming and Nail Clipping: This is intended to be done monthly. Yellow between 21 and 35 days from last time doing, and red after > 35 days.

#### Kitty Pictures Screensaver:
So, a lot of the code for this aspect will be missing from the git repo, as lots of this is handled by the built in xscreensaver program. However, I wanted to mention it, as I will have some code related to it, and that it is by far the best part of this project. Because, who doesn't enjoy seeing cute pictures of their cat?

To explain this part, it requires a little bit of backstory. My roommates and I have a mutual Google Hangouts chat where we send only pictures of our cat, and talk about matters related to her. Over the last year or so, we have accumulated over 500 pictures of our single cat... That is a lot of pictures. So, my goal here is to write a script for a Google Hangouts bot using Hangups (https://github.com/tdryer/hangups) to read the messages in that thread, and if it sees a picture attached, download it and save it to a local pictures folder, which xscreensaver does a random photo slideshow of when the Raspberry Pi goes to its screensaver.

## The components of the project are the following:
* Create a User interface that works well on a 800x480 Raspberry Pi touchscreen display. I chose to do this in a web interface.
* Scripts that will perform GET and POST requests to interact with APIs hosted on AWS to put chore records into a DynamoDB table.
* The code in the AWS APIs (Lambda functions) that the interface and scripts will be interacting with to set and retreieve records of chores.
* The Python scripts for the Hangouts bot to use to pull the pictures posted down from Google's servers.


## Things that need to be done:
If you would like to contribute, please feel free to either clone the repo and then make a Pull Request to merge your changes in! If you are looking for a list of the things that need to be done, please check out the issues section for a good place to start. 

