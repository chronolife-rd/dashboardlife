import template.display as display
import template.css as css
import template.session as session
import streamlit as st

# Initialize streamlit session 
session.init()
session.init_simul()
# Styles
css.run()


session.set_translation()

# Display layers
display.run()




