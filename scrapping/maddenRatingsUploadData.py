import requests
from bs4 import BeautifulSoup as bs
import urllib
import re
import pandas as pd
import sys
from statistics import mean
sys.path.insert(0,'..')
from security import localDirectories
columnNames = []

from openpyxl import load_workbook

import glob



def formatPlayerRow(row,year,file_name):
    if 'Name' in row:
        name = "'" + row.Name.replace("'","_") + "'"
    elif 'First Name' in row:
        name = "'" + (row['First Name'] + ' ' +
                      row['Last Name']).replace("'","_") + "'"
    elif 'First_Name' in row:
        name = "'" + (row.First_Name + ' ' +
                      row.Last_Name).replace("'","_") + "'"
    elif 'FIRSTNAME' in row:
        name = "'" + (row.FIRSTNAME + ' ' +
                      row.LASTNAME).replace("'","_") + "'"
    elif 'FIRST NAME' in row:
        name = "'" + (row['FIRST NAME'] + ' ' +
                      row['LAST NAME']).replace("'","_") + "'"

    file = file_name.split("\\")[-1]
    team = ("'" +
            file.split("madden")[0].replace('(','').replace('__','_')[:-1] +
            "'")
 
    if 'Position' in row:
        pos = "'" + row.Position + "'"
    elif 'POSITION' in row:
        pos = "'" + row.POSITION + "'"

    if 'Height' in row:
        height = row.Height
    elif 'HEIGHT' in row:
        height = row.HEIGHT
    else:
        height = 'NULL'

    if 'Weight' in row:
        weight = row.Weight
    elif 'WEIGHT' in row:
        weight = row.WEIGHT
    else:
        weight = 'NULL'

    if 'OVR' in row:
        overall = row.OVR
    elif 'Overall' in row:
        overall = row.Overall
    elif 'Overall_Rating' in row:
        overall = row.Overall_Rating
    elif 'OVERALL' in row:
        overall = row.OVERALL
    elif 'OVERALL RATING' in row:
        overall = row['OVERALL RATING']
    elif 'OVERALL\nRATING' in row:
        overall = row['OVERALL\nRATING']
    else:
        overall = 'NULL'

    if 'Speed' in row:
        speed = row.Speed
    elif 'SPEED' in row:
        speed = row.SPEED
    else:
        speed = 'NULL'

    if 'Acceleration' in row:
        accel = row.Acceleration
    elif 'ACCELERATION' in row:
        accel = row.ACCELERATION
    else:
        accel = 'NULL'

    if 'Strength' in row:
        strength = row.Strength
    elif 'STRENGTH' in row:
        strength = row.STRENGTH
    else:
        strength = 'NULL'

    if 'Agility' in row:
        agility = row.Agility
    elif 'AGILITY' in row:
        agility = row.AGILITY
    else:
        agility = 'NULL'

    if 'Awareness' in row:
        aware = row.Awareness
    elif 'AWARENESS' in row:
        aware = row.AWARENESS
    else:
        aware = 'NULL'

    if 'Throw Power' in row:
        throwPower = row['Throw Power']
    elif 'Throw_Power' in row:
        throwPower = row.Throw_Power
    elif 'THROWPOWER' in row:
        throwPower = row.THROWPOWER
    elif 'THROW POWER' in row:
        throwPower = row['THROW POWER']
    else:
        throwPower = 'NULL'

    if 'Throw Accuracy Short' in row:
        throwAcc = mean([row['Throw Accuracy Short'],
                          row['Throw Accuracy Mid'],
                          row['Throw Accuracy Deep']])
    elif 'Throw_Accuracy' in row:
        throwAcc = row.ThrowAccuracy
    elif 'THROWACCURACY' in row:
        throwAcc = row.THROWACCURACY
    elif 'THROW ACCURACY' in row:
        throwAcc = row['THROW ACCURACY']
    elif 'THROW ACCURACY MID' in row:
        throwAcc = mean([row['THROW ACCURACY SHORT'],
                        row['THROW ACCURACY MID'],
                        row['THROW ACCURACY DEEP']])
    elif 'THROW ACCURACY MED' in row:
        throwAcc = mean([row['THROW ACCURACY SHORT'],
                        row['THROW ACCURACY MED'],
                        row['THROW ACCURACY DEEP']])
    elif 'Throw Accuracy' in row:
        throwAcc = row['Throw Accuracy']
    elif 'Short Throw Accuracy' in row:
        throwAcc = mean([row['Short Throw Accuracy'],
                        row['Medium Throw Accuracy'],
                        row['Deep Throw Accuracy']])
    elif 'Short Accuracy' in row:
        throwAcc = mean([row['Short Accuracy'],
                        row['Middle Accuracy'],
                        row['Deep Accuracy']])
    else:
        throwAcc = 'NULL'

    if 'Kick Power' in row:
        kickPower = row['Kick Power']
    elif 'Kick_Power' in row:
        kickPower = row.Kick_Power
    elif 'KICKPOWER' in row:
        kickPower = row.KICKPOWER
    elif 'KICK POWER' in row:
        kickPower = row['KICK POWER']
    else:
        kickPower = 'NULL'

    if 'Kick Accuracy' in row:
        kickAcc = row['Kick Accuracy']
    elif 'Kick_Accuracy' in row:
        kickAcc = row.Kick_Accuracy
    elif 'KICKACCURACY' in row:
        kickAcc = row.KICKACCURACY
    elif 'KICK ACCURACY' in row:
        kickAcc = row['KICK ACCURACY']
    else:
        kickAcc = 'NULL'

    if 'Run Block' in row:
        runBlock = row['Run Block']
    elif 'Run_Block' in row:
        runBlock = row.Run_Block
    elif 'Run_Block_Footwork' in row:
        runBlock = mean([row.Run_Block_Footwork,
                         row.Block_Strength])
    elif 'RUNBLOCK' in row:
        runBlock = row.RUNBLOCK
    elif 'RUNBLOCKSTRENGTH' in row:
        runBlock = mean([row.RUNBLOCKSTRENGTH,
                         row.RUNBLOCKFOOTWORK])
    elif 'RUNBLOCK STRENGTH' in row:
        runBlock = mean([row['RUNBLOCK STRENGTH'],
                         row['RUNBLOCK FOOTWORK']])
    elif 'RUN BLOCK' in row:
        runBlock = row['RUN BLOCK']
    elif 'Run Block Strength' in row:
        runBlock = mean([row['Run Block Strength'],
                         row['Run Block Footwork']])
    elif 'Run Blocking' in row:
        runBlock = row['Run Blocking']
    elif 'Run Block Power' in row:
        runBlock = mean([row['Run Block Power'],
                         row['Run Block Finesse']])
    else:
        runBlock = 'NULL'

    if 'Pass Block' in row:
        passBlock = row['Pass Block']
    elif 'Pass_Block' in row:
        passBlock = row.Pass_Block
    elif 'Pass_Block_Footwork' in row:
        passBlock = mean([row.Pass_Block_Footwork,
                          row.Pass_Block_Strength])
    elif 'PASSBLOCK' in row:
        passBlock = row.PASSBLOCK
    elif 'PASSBLOCKSTRENGTH' in row:
        passBlock = mean([row.PASSBLOCKSTRENGTH,
                          row.PASSBLOCKFOOTWORK])
    elif 'PASSBLOCK STRENGTH' in row:
        passBlock = mean([row['PASSBLOCK STRENGTH'],
                          row['PASSBLOCK FOOTWORK']])
    elif 'PASS BLOCK' in row:
        passBlock = row['PASS BLOCK']
    elif 'Pass Block Strength' in row:
        passBlock = mean([row['Pass Block Strength'],
                          row['Pass Block Footwork']])
    elif 'Pass Blocking' in row:
        passBlock = row['Pass Blocking']
    elif 'Pass Block Power' in row:
        passBock = mean([row['Pass Block Power'],
                         row['Pass Block Finesse']])
    else:
        passBlock = 'NULL'

    if 'Catching' in row:
        catch = row.Catching
    elif 'CATCHING' in row:
        catch = row.CATCHING
    elif 'Catch' in row:
        catch = row.Catch
    else:
        catch = 'NULL'

    if 'Carrying' in row:
        carry = row.Carrying
    elif 'CARRYING' in row:
        carry = row.CARRYING
    else:
        carry = 'NULL'

    if 'Ball Carrier Vision' in row:
        bc = row['Ball Carrier Vision']
    elif 'BC_Vision' in row:
        bc = row.BC_Vision
    elif 'BCVISION' in row:
        bc = row.BCVISION
    elif 'BALL CARRIER VISION' in row:
        bc = row['BALL CARRIER VISION']
    elif 'BC VISION' in row:
        bc = row['BC VISION']
    elif 'BC Vision' in row:
        bc = row['BC Vision']
    else:
        bc = 'NULL'

    if 'Injury' in row:
        injury = row.Injury
    elif 'INJURY' in row:
        injury = row.INJURY
    else:
        injury = 'NULL'

    if 'Toughness' in row:
        tough = row.Toughness
    elif 'TOUGHNESS' in row:
        tough = row.TOUGHNESS
    else:
        tough = 'NULL'

    if 'Stamina' in row:
        stamina = row.Stamina
    elif 'STAMINA' in row:
        stamina = row.STAMINA
    else:
        stamina = 'NULL'

    if 'Route Running' in row:
        route = row['Route Running']
    elif 'Route_Running' in row:
        route = row.Route_Running
    elif 'ROUTERUNNING' in row:
        route = row.ROUTERUNNING
    elif 'ROUTE RUNNING' in row:
        route = row['ROUTE RUNNING']
    elif 'Short Route Runing' in row:
        route = mean([row['Short Route Runing'],
                      row['Medium Route Running'],
                      row['Deep Route Running']])
    elif 'Short Route Running' in row:
        route = mean([row['Short Route Running'],
                      row['Medium Route Running'],
                      row['Deep Route Running']])
    else:
        route = 'NULL'
    
    
    returnText = ("(" + name + "," + #name
                  year + "," +#season
                  team + "," +#team
                  pos + "," +#position
                  str(int(height.split("'")[0])*12+
                            int(height.split("'")[1][:-1])) + "," +#height
                  str(weight) + "," +#weight
                  str(overall) + "," +#overall
                  str(speed) + "," +#speed
                  str(accel) + "," +#acceleration
                  str(strength) + "," +#strength
                  str(agility) + "," +#agility
                  str(aware) + "," +#awareness
                  str(throwPower) + "," +#throw power
                  str(throwAcc) + "," +#throw accuracy
                  str(kickPower) + "," +#kick power
                  str(kickAcc) + "," +#kick accuracy
                  str(passBlock) + "," +#pass block
                  str(runBlock) + "," +#run block
                  str(catch) + "," +#catch
                  str(carry) + "," +#carrying
                  str(bc) + "," +#ball carrier vision
                  str(injury) + "," +#injury
                  str(tough) + "," +#toughness
                  str(stamina) + "," +#stamina
                  str(route) +#route_running
                  "),")

    return returnText

sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect

with DOConnect() as tunnel:
    c, conn = connection(tunnel)
    c.close()

for file_name in glob.glob(localDirectories['madden_files']+'*madden*.xls*'):


    sqlScript = '''insert into madden_ratings.playerRatings
    (player_name, season, team, pos, height, weight, overall, speed,
    acceleration, strength, agility, awareness, throw_power,
    throw_accuracy, kick_power, kic_accuracy, pass_block,
    run_block, catch, carrying, bc_vision, injury,
    toughness, stamina, route_running)
    values '''
    year = re.search('_\d+',file_name)
    if year.group(0) == '_25':
        year = 13
    else:
        year = year.group(0)[1:]
    file=pd.read_excel(file_name)
    for index, row in file.iterrows():

        rowText = formatPlayerRow(row,year,file_name)
        print(rowText)

    break


    
