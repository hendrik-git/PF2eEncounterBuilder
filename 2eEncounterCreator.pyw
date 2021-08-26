#! python3
import os
import re  # Regex
import string
import pyexcel as pe
import PySimpleGUI as sg

# ------------------------------------------------
# Functions
# ------------------------------------------------
def CalculateXP(PL, CR):
    if PL == CR + 4:  # Low-threat lackey
        return 10
    if PL == CR + 3:  # Low- or moderate-threat lackey
        return 15
    if PL == CR + 2:  # Any lackey or standard creature
        return 20
    if PL == CR + 1:  # Any standard creature
        return 30
    if PL == CR + 0:  # Any standard creature or low-threat boss
        return 40
    if PL == CR - 1:  # Low- or moderate-threat boss
        return 60
    if PL == CR - 2:  # Moderate- or severe-threat boss
        return 80
    if PL == CR - 3:  # Severe- or extreme-threat boss
        return 120
    if PL == CR - 4:  # Extreme-threat solo boss
        return 160
    return 0  # Not viable for encounter


def CheckCreatureType(values,type):
    if values['Aberration'] is False:  # checkbox not ticked
        if 'Aberration' in type:
            return True
    if values['Animal'] is False:  # checkbox not ticked
        if 'Animal' in type:
            return True
    if values['Beast'] is False:  # checkbox not ticked
        if 'Beast' in type:
            return True
    if values['Celestial'] is False:  # checkbox not ticked
        if 'Celestial' in type:
            return True
    if values['Construct'] is False:  # checkbox not ticked
        if 'Construct' in type:
            return True
    if values['Dragon'] is False:  # checkbox not ticked
        if 'Dragon' in type:
            return True
    if values['Elemental'] is False:  # checkbox not ticked
        if 'Elemental' in type:
            return True
    if values['Fey'] is False:  # checkbox not ticked
        if 'Fey' in type:
            return True
    if values['Fiend'] is False:  # checkbox not ticked
        if 'Fiend' in type:
            return True
    if values['Fungus'] is False:  # checkbox not ticked
        if 'Fungus' in type:
            return True
    if values['Giant'] is False:  # checkbox not ticked
        if 'Giant' in type:
            return True
    if values['Humanoid'] is False:  # checkbox not ticked
        if 'Humanoid' in type:
            return True
    if values['Monitor'] is False:  # checkbox not ticked
        if 'Monitor' in type:
            return True
    if values['Ooze'] is False:  # checkbox not ticked
        if 'Ooze' in type:
            return True
    if values['Plant'] is False:  # checkbox not ticked
        if 'Plant' in type:
            return True
    if values['Undead'] is False:  # checkbox not ticked
        if 'Undead' in type:
            return True
    return False


def IncompatibleAlign(Align1, Align2):
    if Align1 == 'Lawful Good' or Align1 == 'Neutral Good' or Align1 == 'Chaotic Good':
        if Align2 == 'Lawful Evil' or Align2 == 'Neutral Evil' or Align2 == 'Chaotic Evil':
            return 1  # No good with evil creatures

    if Align1 == 'Chaotic Good' or Align1 == 'Chaotic Neutral' or Align1 == 'Chaotic Evil':
        if Align2 == 'Lawful Good' or Align2 == 'Lawful Neutral' or Align2 == 'Lawful Evil':
            return 1  # No chaotic with lawful creatures
    return 0


def FindMonsters(values, target):
    PartyLevel = int(values['PL'])
    XP_Budget = int(values['XP' + str(target)])
    records = pe.iget_records(file_name="2eMonsters.ods")
    for creature in records:
        creatureList = ''
        creature_XP = CalculateXP(PartyLevel, creature['Level'])

        # check if creature is viable
        if creature_XP == 0 or creature_XP > XP_Budget:
            continue

        # check if creature type is selected
        if CheckCreatureType(values, creature['Creature Type']):
            print("%s is %s and will be skipped" % (creature['Name'], creature['Creature Type']))
            continue

        n = XP_Budget / creature_XP

        # construct string of creature
        window['Multiline' + str(target)].print('%dx ' % n + creature['Name'] + ' (%d XP)' % creature_XP)

        if values['ToFile'] is True:
            File.write('%dx ' % n + creature['Name'] + ' (%d XP)' % creature_XP)
            File.write('\n')
    return 1


# ------------------------------------------------
# Create GUI
# ------------------------------------------------
sg.theme('Dark Blue 3')  # please make your windows colorful
col1 = [[sg.Checkbox('Aberration', default=True, key='Aberration')],
        [sg.Checkbox('Animal',     default=True, key='Animal')],
        [sg.Checkbox('Beast',      default=True, key='Beast')],
        [sg.Checkbox('Celestial', default=True, key='Celestial')],
        [sg.Checkbox('Construct', default=True, key='Construct')],
        [sg.Checkbox('Dragon', default=True, key='Dragon')]]
col2 = [[sg.Checkbox('Elemental', default=True, key='Elemental')],
        [sg.Checkbox('Fey', default=True, key='Fey')],
        [sg.Checkbox('Fiend', default=True, key='Fiend')],
        [sg.Checkbox('Fungus', default=True, key='Fungus')],
        [sg.Checkbox('Giant', default=True, key='Giant')],
        [sg.Checkbox('Humanoid', default=True, key='Humanoid')]]
col3 = [[sg.Checkbox('Monitor', default=True, key='Monitor')],
        [sg.Checkbox('Ooze', default=True, key='Ooze')],
        [sg.Checkbox('Plant', default=True, key='Plant')],
        [sg.Checkbox('Undead', default=True, key='Undead')],
        [sg.Text('')],
        [sg.Checkbox('ToFile', default=False, key='ToFile')]]
col4 = [[sg.Text('<40 \u00B1 10 Trivial Threat')],
        [sg.Text(' 60 \u00B1 15 Low Threat')],
        [sg.Text(' 80 \u00B1 20 Moderate Threat')],
        [sg.Text('120 \u00B1 30 Severe Threat')],
        [sg.Text('160 \u00B1 40 Extreme Threat')],
        [sg.Text('\u00B1 party size adjustment')]]
col5 = [[sg.Text('Creatures 1')], [sg.Multiline('', size=(45, 15), key='Multiline1',do_not_clear=False)]]
col6 = [[sg.Text('Creatures 2')], [sg.Multiline('', size=(45, 15), key='Multiline2',do_not_clear=False)]]
col7 = [[sg.Text('XP Budget 1')],
        [sg.Input('80', size=(10, 2), key='XP1')],
        [sg.Text('XP Budget 2')],
        [sg.Input('40', size=(10, 2), key='XP2')],
        [sg.Text('Party Level')],
        [sg.Input('1', size=(10, 2), key='PL')]]

layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3), sg.Column(col7), sg.Column(col4),
           sg.Button('Show', size=(9, 2), key='-IN-')],
          [sg.Column(col5), sg.Column(col6)]]

window = sg.Window('PF2e Encounter Builder', layout)  # create window with given layout


# ------------------------------------------------
# INPUT LOOP
# ------------------------------------------------
while True:
    event, values = window.read()  # can also be written as event, values = window()
    if event is None or event == 'Exit':
        break
    if event == '-IN-':
        File = open('Encounters.txt', 'w')
        FindMonsters(values, 1)
        FindMonsters(values, 2)
        TabsRegex = re.compile('\t')
        LinesRegex = re.compile('\n')
        File.close()

# ------------------------------------------------
# Finish Cleanup
# ------------------------------------------------
window.close()
pe.free_resources()