# Phidash

Template project for Dash dashboards

Run with wsgi.py

### Structure:



### Setup:
* Edit globals in config.py
* Place data and scripts in .data
  * markdowns.py can be used to store longer text in order to keep everything clean
* data is loaded in .dashapp.__init__.py
  * specific data is imported by modules when needed. Avoid changing values.
* .dashapp.tabindex is the main page
  * import tab containers from other files (e.g. exampletab.py and abouttab.py) and update TABS variable
