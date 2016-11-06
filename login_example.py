from __future__ import division
from datetime import datetime
from calendar import monthrange
from flask import Flask, render_template, url_for, request, session, redirect
from flask.ext.pymongo import PyMongo
import bcrypt, json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'bill'
app.config['MONGO_URI'] = 'mongodb://aman:amanpassword@ds011271.mlab.com:11271/bill'
#mongodb://aman:amanpassword@ds011271.mlab.com:11271/bill
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        #return 'You are logged in as ' + session['username']
        return render_template('home.html', session = session)

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/saveBill', methods=['POST'])
def saveBill():
    bill_json = request.json['bill']
    bill_json = json.loads(bill_json)
    #bill_json = json.loads(bill_json)
    print '----------------------'
    print bill_json
    print '***************'
    for i in bill_json:
        print i,
    bill_details = mongo.db.bill_details
    bill_details.insert({
        'user' : session['username'],
        'electricity_units' : bill_json['electricity_units'],
        'power_backup' : bill_json['power_backup'],
        'late_charges' : bill_json['late_charges'],
        'service_tax' : bill_json['service_tax'],
        'swach_bharat' : bill_json['swach_bharat'],
        'month_number' : bill_json['month_number'],
        'meter_start_date' : bill_json['meter_start_date'],
        'meter_end_date' : bill_json['meter_end_date'],
        'amount_to_be_paid' : bill_json['amount_to_be_paid'],
        'br1' : bill_json['br1'],
        'br2' : bill_json['br2'],
        'br3' : bill_json['br3'],
        'common_room_reading' : bill_json['common_room_reading'],
        'aman_share' : bill_json['aman_share'],
        'gaurav_share' : bill_json['gaurav_share'],
        'karan_share' : bill_json['karan_share'],
        'chandan_share' : bill_json['chandan_share'],
        'rajan_share' : bill_json['rajan_share'],
        'anshul_share' : bill_json['anshul_share']
        })


    # users = mongo.db.users
    # login_user = users.find_one({'name' : request.form['username']})

    # if login_user:
    #     if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
    #         session['username'] = request.form['username']
    #         return redirect(url_for('index'))

    return "Saved Successfully"


@app.route('/viewBills', methods=['POST', 'GET'])
def viewBills():
    bill_details = mongo.db.bill_details
    if 'username' in session:
        bills = bill_details.find({'user' : session['username']})
        print bills
        return render_template('viewBills.html', session = session, bills = bills)

    return render_template('index.html')



    

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    if 'username' in session:
        
        ###################################
        #your code goes here

        # BILL DETAILS
        electricity_units =  float(request.form.get('electricityCharges', None)) #request.form['electricityCharges']  ## x6
        power_backup = float(request.form.get('powerBackupCharges', None))#request.form['powerBakupCharges']     ## x18
        late_charges = float(request.form.get('lateCharges', None))#request.form['lateCharges'] 
        service_tax = float(request.form.get('serviceTax', None))#request.form['serviceTax']
        swach_bharat = float(request.form.get('swachBharatCharges', None))#request.form['swachBharatCharges']
        month_number = float(request.form.get('monthNumber', None))#request.form['monthNumber']
        meter_start_date = request.form.get('startDate', None)
        meter_end_date = request.form.get('endDate', None)
        print meter_start_date
        total_amount = float(electricity_units*6 + power_backup*18 + late_charges + service_tax + swach_bharat)

        print '## BILL DETAILS ############'
        print
        print 'electricity_units = ' + str(electricity_units) + '| cost = Rs.' + str(electricity_units*6)
        print 'power_backup = ' + str(power_backup) + '| cost = Rs.' + str(power_backup*18)
        print 'late_charges = ' + str(late_charges) + '| cost = Rs.' + str(late_charges)
        print 'service_tax = ' + str(service_tax) + '| cost = Rs.' + str(service_tax)
        print 'swach_bharat = ' + str(swach_bharat) + '| cost = Rs.' + str(swach_bharat)

        print 'amount_to_be_paid = Rs.' + str (electricity_units*6 + power_backup*18 + late_charges + service_tax + swach_bharat)
        print 
        print '######################'
        print

        ## Date calculations
        date_format = '%Y-%m-%d'
        meter_start_date_formatted = datetime.strptime(meter_start_date, date_format)
        meter_end_date_formatted = datetime.strptime(meter_end_date, date_format)
        meter_recorded_days = (meter_end_date_formatted - meter_start_date_formatted).days


        ## METER READINGS
        br1_start = float(request.form.get('br1StartReading', None)) ## 6 Aug
        br1_end = float(request.form.get('br1EndReading', None)) ## 4 oct
        br2_start = float(request.form.get('br2StartReading', None))
        br2_end = float(request.form.get('br2EndReading', None))
        br3_start = float(request.form.get('br3StartReading', None))
        br3_end = float(request.form.get('br3EndReading', None))

        days_in_month = monthrange(2016, int(month_number))[1]
        ## Reading for 30/31 days
        br1 = ( (br1_end - br1_start) / meter_recorded_days ) * days_in_month
        br2 = ( (br2_end - br2_start) / meter_recorded_days ) * days_in_month
        br3 = ( (br3_end - br3_start) / meter_recorded_days ) * days_in_month

        print 'br1_reading = ' + str(br1) + 'br1_reading_c = ' + str(br1*6) 
        print 'br2_reading = ' + str(br2) + 'br2_reading_c = ' + str(br2*6) 
        print 'br3_reading = ' + str(br3) + 'br3_reading_c = ' + str(br3*6) 


        total_reading_all_rooms = br1 + br2 + br3
        common_room_reading = electricity_units - total_reading_all_rooms
        common_room_individual_person = common_room_reading/6

         
        print 'total_reading_all_rooms = ' + str ( total_reading_all_rooms )
        print 'common_room_reading = ' + str ( common_room_reading )
        print 'total_reading_all_rooms + common_room_reading = ' + str ( total_reading_all_rooms + common_room_reading )
        print 'common_room_individual_person = ' + str( common_room_individual_person )
        print '\n'


        br1_tax   = (br1*6 *.14)
        br2_tax   = (br2*6 *.14)
        br3_tax   = (br3*6 *.14)
        print 'br1_tax   = ' + str((br1*6 *.14))
        print 'br2_tax   = ' + str((br2*6 *.14))
        print 'br3_tax   = ' + str((br3*6 *.14))
        power_backup_tax  = 720 * .14
        common_room_tax  = common_room_reading * 6 *.14


        print 'total_tax = ' + str(br1_tax  + br2_tax+ br3_tax + power_backup_tax   + common_room_tax)  

        br1_tax_total = br1_tax + power_backup_tax /3 + common_room_tax/3
        br2_tax_total = br2_tax + power_backup_tax /3 + common_room_tax/3
        br3_tax_total = br3_tax + power_backup_tax /3 + common_room_tax/3

        #print 'br1Tax = ' + str(br1_tax_total) , 'br2 tax = ' + str(br2_tax_total) , 'br3 tax = ' + str(br3_tax_total)




        power_backup_individual_person = 40/6
        print 'yum = ' + str(power_backup_individual_person)
        #service_and_swach_and_late_individual_person = ( service_tax + swach_bharat + late_charges )/6 ## price NOT units


        # br2
        print '#############################################'
        print '(br2/2)*6* = ' + str((br2/2)*6)
        print '(br1/2)*6 = ' + str((br1/2)*6)
        print '(br3/2)*6 = ' + str((br3/2)*6)
        print '(br2_tax/2) = ' + str((br2_tax/2))
        print '(br1_tax/2) = ' + str((br1_tax/2))
        print '(br3_tax/2) = ' + str((br3_tax/2))
        print '(power_backup_individual_person * 18) = ' + str((power_backup_individual_person * 18))
        print 'swach_bharat/6 = ' + str(swach_bharat/6)
        print 'late_charges/6' + str(late_charges/6)
        print
        print 





        print '###############################################'
        karan_share = ((br2/2)*6) + (common_room_individual_person * 6 )+ (power_backup_individual_person * 18) + (br2_tax/2) + power_backup_tax/6   + common_room_tax/6 + (swach_bharat/6) + (late_charges/6)
        chandan_share = (br2/2)*6 + common_room_individual_person * 6 + power_backup_individual_person * 18 +  br2_tax/2 + power_backup_tax/6   + common_room_tax/6 + swach_bharat/6 + late_charges/6
        #br1
        rajan_share = (br1/2)*6 + common_room_individual_person * 6 + power_backup_individual_person * 18 +  br1_tax/2 + power_backup_tax/6   + common_room_tax/6 + swach_bharat/6 + late_charges/6
        anshul_share = (br1/2)*6 + common_room_individual_person * 6 + power_backup_individual_person * 18 +  br1_tax/2 + power_backup_tax/6   + common_room_tax/6 + swach_bharat/6 + late_charges/6
        #br2
        aman_share = (br3/2)*6 + common_room_individual_person * 6 + power_backup_individual_person * 18 +  br3_tax/2 + power_backup_tax/6   + common_room_tax/6 + swach_bharat/6 + late_charges/6
        gaurav_share = (br3/2)*6 + common_room_individual_person * 6 + power_backup_individual_person * 18 +  br3_tax/2 + power_backup_tax/6   + common_room_tax/6 + swach_bharat/6 + late_charges/6

        print 'karan_share + chandan_share + rajan_share + anshul_share + aman_share + gaurav_share' +  str( karan_share + chandan_share + rajan_share + anshul_share + aman_share + gaurav_share )
        print 'total electricity_rum_and_common = ' + str( br1*6 + br2*6 +br3*6 + common_room_individual_person *6*6   )
        print 'power_backup_total = ' + str(power_backup_individual_person*6*18)
        print 'total+power_bacup = ' + str(power_backup_individual_person  *6 *18)

        print 'Aman = ' +  str(aman_share)
        print 'Gaurav = ' +  str(gaurav_share)
        print 'Karan = ' +  str(karan_share)
        print 'Chandan = ' +  str(chandan_share)
        print 'Rajan = ' +  str(rajan_share)
        print 'Anshul = ' +  str(anshul_share)
        ####################################
        bill_info = {
            'electricity_units' : electricity_units,
            'power_backup' : power_backup,
            'late_charges' : late_charges,
            'service_tax' : service_tax,
            'swach_bharat' : swach_bharat,
            'month_number' : month_number,
            'meter_start_date' : str(meter_start_date),
            'meter_end_date' : str(meter_end_date),
            'amount_to_be_paid' : total_amount,
            'br1' : br1,
            'br2' : br2,
            'br3' : br3,
            'common_room_reading' : common_room_reading,
            'aman_share' : aman_share,
            'gaurav_share' : gaurav_share,
            'karan_share' : karan_share,
            'chandan_share' : chandan_share,
            'rajan_share' : rajan_share,
            'anshul_share' : anshul_share

        }
        #print bill_info

        #return 'You are logged in as ' + session['username']
        return render_template('calculate.html', session = session, bill_info = bill_info)

    #return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})#None #users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)