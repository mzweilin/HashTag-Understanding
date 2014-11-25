HashTag-Understanding
=====================

#Dependencies
To install dependencies, navigate to the root of the project and execute (using ruby make, ie rake):
`rake setup`
If you start using a new python library, add it to requirements.txt.  Required ruby gems are listed in the Gemfile.

#Execution Path
The chrome client (under /chrome-ext) makes GET requests to the local host via port 5000.  These requests are defined by server.py, which is run using `python server.py` or just `rake launch`.  To use the pipeline directly, you can use the Job class (consult job.py for an example). Components of the pipeline are defined under the /lib directory and the relevant subdirectory.

#Coding Conventions
Tab Size: 4 spaces (not "\t")
