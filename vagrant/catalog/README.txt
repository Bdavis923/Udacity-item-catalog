Source code for a Item Catalog website.

Item Catalog website

This is a website that contains that items, from a catalog where you can view, edit or add items.

Getting Started

You can download the repository on your system.

Prerequisites

Download python 2.7.14 using this link https://www.python.org/downloads/
Download GitBash

Running the tests

Open up GitBash
Switch to directory where you downloaded the folder
Run the following commands:
    cd vagrant
    vagrant up
    winpty vagrant ssh
    cd / vagrant
    python database_setup.py
    python populate.py
    python application.py
once the server has started you can open a browser and go to localhost:8000
