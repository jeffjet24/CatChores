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
* Need to fix the minutes place in the timestamps under the performed section to have a leading zero in the case of a single digit minutes value. e.g. currently: `Mack fed cat at 11:8 AM`. Needs to be: `Mack fed cat at 11:08 AM` (for version 1.0.0)
* Set the timestamps to use 12 hour format, because @iammann cannot read 24-hour format. (for version 1.0.0)
* Make the colors of the panels a darker color in the CSS, overriding Bootstraps colors. This is needed because of the brightness and viewing angle with the Raspberry Pi touchscreen. It washes out the already pretty light colors that Bootstrap uses for its panels. (for version 1.0.0)
* Edit the `lambda/CatGetPerformed.py` Lambda function to base feeding the cat around 8 AM in the AM, and 8 PM in the PM. As I found that if the cat doesn't get fed until 11 AM, the function will think that it is normal to feed the cat at 11 AM the next day.. While we really want to normalize it around 8 AM and 8 PM everyday. (for version 1.0.1)
* Writing the Python plugin for the Hangouts bot to pull the pictures from the hangouts thread. (for version 1.1.0)
* Giving someone a nice interface (a different interface than the main one) to make a simple request to the API which allows them to customize the timestamp. This would allow someone to register that a task was completed long after it has been completed. So for example: if someone forgot to tap the interface on the tablet after they fed the cat. Or if they didn't have time to add it. (for version 1.2.0)

