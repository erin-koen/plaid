# erin-koen


> data scraping practice

TODO: Fill out this long description.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background
The take home challenge for the Plaid Software Engineer - Crawler role. 

This was a fun challenge as I'd never worked with Selenium or Beautiful Soup before. I've written a lot of code in Python, but it's either been for the computer science theory portion of Lambda School where we optimized algorithms and built data structures, or it's been writing APIs in Django and Flask. It was super fun to learn a couple new packages by exploring the docs and trying to solve what was an intricate problem. 

My proudest moment in this code is handling the complexity on the 13F page. The naming conventions for the acutal XML file that contains a fund's holdings seem to be fairly lax. THat said, I noticed that the Type column of the table where the link was held was constant - `INFORMATION TABLE`. I used beautiful soup to break each row in the table into an array, found the cell that held `INFORMATION TABLE` and worked backwards from there. This is an obvious assumption on my part, but one I'm happy to make because I dug around a bit and couldn't find an instance where this wasn't the case. 

The Black Rock edge case was also interesting. In this instance, Black Rock is the holding company for a bunch of other funds and money managers, so they leave reporting up to their subsidiaries. I decided just to log that error message to the console, rather than printing a blank TSV file, thinking that as a user I'd rather the immediate feedback.  

## Install

You've successfully unzipped the file if you're reading this text. The next step will be to install the dependencies. Navigate to the directory in your terminal and launch your favorite virtual environment. I happen to prefer pipenv. `Pipenv install` will load all the dependencies (listed in the `Pipefile`) required by the program. They're also listed in the `requirements.txt` in this directory.

This program was built in a code editor and has been run through the terminal. Installation instructions are written accordingly.

## Usage

After navigating to the ERIN_KOEN directory in your terminal, enter `python sec_scraper.py CIK_or_ticker_ofyourchoosing`. The program will run and let you know that a TSV file has been created when it's finished. The TSV file will be named `CIK_todaysdate` where CIK is the ticker or number you entered. 

## Maintainers

[@erin-koen](https://github.com/erin-koen)


## License

MIT © 2019 Erin Koen
