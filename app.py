#Flask App
#Zak Bool, zab0102@arastudent.ac.nz

#Import os and Flask modules
import os
from flask import Flask, render_template, request, flash

SUCCESS_MSG = 'success'
WARNING_MSG = 'warning'
KEY_SIZE = 24
HTML_TEMPLATE = 'flask_app.html'

# Create Flask instance and set the session key
app = Flask(__name__)
app.secret_key = os.urandom(KEY_SIZE)
#app.debug = True

def get_demerit_points(driving_speed, speed_limit, holiday_period = False):
    """
    Calculates demerit points based on how much over the speed limit a driver is driving (if over),
    and deems whether the penalty is mandatory, which changes depending on if it is a holiday period
    """
    #Sets default values for mandatory penalty and amount of penalty points
    mandatory_penalty = False
    penalty_points = 0
    #Creates var for difference in driving speed and speed limit
    speed_over = driving_speed - speed_limit

    #Sets mandatory penalty to True if over my 4 in holiday period or by 5 when not
    if holiday_period and speed_over > 4:
        mandatory_penalty = True

    elif not holiday_period and speed_over > 5:
        mandatory_penalty = True

    #Checks if speed over is above a certain amount and applies points for how much over if so
    if speed_over > 30:
        penalty_points = 50

    elif speed_over > 20:
        penalty_points = 30

    elif speed_over > 10:
        penalty_points = 20

    elif speed_over > 0:
        penalty_points = 10

    #Return mandatory penalty bool and penalty points int as tuple
    return mandatory_penalty, penalty_points
    

@app.route('/', methods = ['POST', 'GET'])
def home():
    """ Home page handler """

    print(f'DEBUG. Function received http method type: {request.method}')
    
    if request.method == 'POST':
        # Get the data that has been sent via http post
        driving_speed = request.form.get('form_first_number')
        speed_limit = request.form.get('form_second_number')
        holiday_period = request.form.get('form_tickbox1')
        print(f'{holiday_period=}')

        #If values are not empty continue on
        if driving_speed != '' and speed_limit != '':
            #Check if driving speed is an int/float and speed limit is an int
            if driving_speed.replace('.','').isdigit() and speed_limit.isdigit():
                #Convert driving speed to float or int depending on how it is formatted, and convert speed_limit to int
                if '.' in driving_speed:
                    driving_speed = float(driving_speed)
                else:
                    driving_speed = int(driving_speed)

                speed_limit = int(speed_limit)

                #Gets penalty points and type of penalty
                penalty_msg = get_demerit_points(driving_speed, speed_limit, holiday_period)

                #Checks if penalty points is 0, else if the penalty is mandatory, or lastly if it is then discretional
                if penalty_msg[1] == 0:
                    flash(f"{driving_speed}km/h in a {speed_limit}km/h zone is not speeding.", SUCCESS_MSG)
                elif penalty_msg[0]:
                    flash(f"The mandatory penalty for driving at {driving_speed}km/h in a {speed_limit}km/h is {penalty_msg[1]} points.", WARNING_MSG)
                elif not penalty_msg[0]:
                    flash(f"The discretional penalty for driving at {driving_speed}km/h in a {speed_limit}km/h is {penalty_msg[1]} points.", WARNING_MSG)

                #Returns results to browser
                return render_template(HTML_TEMPLATE, title='Demerit points calculator', form_first_number=driving_speed, form_second_number=speed_limit, form_tickbox1=holiday_period)

            else:
                #Else values not digits (if not caught elsewhere)
                flash(f'Numbers only please.', WARNING_MSG)

        #Displays warning messages for no speed limit, no driving speed, and both
        elif driving_speed != '' and speed_limit == '':
            flash('Please enter a speed limit.', WARNING_MSG)
        elif driving_speed == '' and speed_limit != '':
            flash('Please enter a driving speed.', WARNING_MSG)
        else:
            # Not all the data was received
            flash('Please enter a driving speed and speed limit.', WARNING_MSG)

    #Returns results on first call and if program doesn't make it to other return
    return render_template(HTML_TEMPLATE, title='Demerit points calculator')

@app.errorhandler(404)
def page_not_found(e):
    """ 404 error handler (page not found) """
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
