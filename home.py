import template.display as display
import template.css as css
import template.session as session

# Initialize streamlit session 
session.init()
session.init_simul()

# Styles
css.run()

# Display layers
display.run()




