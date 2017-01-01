# Overview
This was setup in two main pieced.  One to download and store the XML and the other to parse through the saved XML files.  My idea on how this would be run, for now, would be as a cron or some other scheduled task that would first download files and then parse through them.

In production I would expect this logic to be hit through some endpoint.  I have written the majority of the code in a way that would allow all the heavy logic to be flexible enough to be run in a few different ways with a small amount of logic changes.

After looking over everything I suppose an argument could be made that this was 'over-engineered', so I have listed some reasons why I decided to write this code as I did.

* To make the code flexible I needed to make sure that there was as little hard-coding as possible in the logic.  I made the constants file as a way to seperate contextual information from the code.  One of my first changes would be to move this contextual data to config files and have a config parser setup the data for the program to run.  This allows greater flexibility when wanting to parse XML files differently based on config files alone.
* Writing some of the unit tests took longer than the code, but without them refactoring would be more difficult and take more time in the end.  Also I see the unittests as a way of documenting the expected behaviour of the program.  The unittests would need to be amended so that all functionality had positive and negative test cases as well as some edge cases caught.

## Instructions
#### Running Unittests
* Navigate to the root of the project
* To Run Tests :: ```python -m unittest discover -v```

#### Running Full Program
* From the project root :: ```python run.py```
* Navigate to the data directory to see the XML and related CSV

#### Bugs
* RESOLVED: Issue [#3](https://github.com/howard-roark/booj_two/issues/3)
  * See [1d52568](https://github.com/howard-roark/booj_two/pull/7/commits/1d525687de33f1f12de97eaf4bad053eb9ea0b68)
