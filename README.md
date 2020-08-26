# BCS Central Grading Approval Bot

You need chromedriver for this to work, match it to your version of Chrome and drop it in `/` and you'll be fine.

You can add a `config.py` matching the format of `config_sample.py` if you don't want to type in your login info every time.

### TODO

Running it headless breaks the navigation, it _should_ be easy to fix but has proven otherwise because splinter has issues clicking on things. Maybe I'll just have it navigate there in a new tab. Can I thread that?? **Note to self**: find out if I can thread that...

It doesn't handle multiple pages of submissions, workaround is to run it multiple times.

Don't run it while the json file is open, it screws up the seek function. I'm not going to fix it because it doesn't break the main functionality, just screws up the appended reports.
