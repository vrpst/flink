# Technical overview
The path to get from the starting article to the finishing one is found by querying the Wikimedia API for the starting page's text, running it through a parser algorithm to find the first link, and repeating this recusively until one of the Vital Articles is reached, or the path loops (i.e. article A's first link is article B, and article B's first link is article A). At the same time as the first link is found in the page text, the parser also finds and formats the first sentence of the article. All API queries and parsing is carried out on a loading screen, before the game begins.

The parser makes up the bulk of the project's backend. I wrote it before I knew regex to any usable capacity, so it makes use of native Python string-matching techniques. This includes filtering templates, citations/references, and wikitext bold/italic/underline syntax. Finding the first link is generally straightforward—find the first word enclosed in double square brackets (`[[example]]`) not in a template or reference. Finding and accurately fixing the first sentence is made much more complicated by the many different ways a full stop/period can be used, as well as natural variations in formatting that occur when humans write text. I would estimate that the sentence parsing has around a 95% success rate, so it is (infuriatingly!) not perfect. The link and sentence are extracted from the article's full wikitext, which is retrivied through a call to the Wikimedia REST API, using the Python `requests` library.

The frontend is written using `pygame` and involved using it to much greater depth than I had ever done previously. The entire interface is inside a big while loop, with a status variable shifting between the game states (loading, running, end) and the different screens (home, howtoplay, about, game). `pygame` does not have native button support, and I had to write classes to function as button objects from scratch, as well as creating my own text input functionality. The loading screen makes use of multithreading to maintain the animations while the backend makes and parses the API calls; if the loading screen froze, it might give the impression that the game is crashing.

_December 2024_

## Features

- Object-oriented game design
- Complex string pattern matching and substitution
- Interface design with pygame
- Multithreading*
- Internet interactions with requests*
- REST API use*
- JSON parsing*

Technical aspects new to me in this project are marked with an asterisk.
