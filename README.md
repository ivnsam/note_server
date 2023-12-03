# note_server
Web application for editing Markdown-based notes

Themes for code highlighting are from https://github.com/develephant/mkdocs-codehilite-themes <br>
Made with PerplexityAI by Ivan Samoylenko, 2023

# how to run on localhost with demo notes
Clone this repository, install requiments and run serv.py
```
pip3 install -r requiments.txt
python3 serv.py -l
```

# command line arguments
-d or --notes_dir - path to directory with notes <br>
-i or --ip IP - set listen address <br>
-l or --local - listen localhost

# To-Do:
1. Optimize loading .css styles on note page
