#Author- BCD Sim
#Description-  Imports a JSON file of metric tap drill sizes and creates user parameters for each size.

import adsk.core, adsk.fusion, adsk.cam, traceback
import json
# import os

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # Specify the path to your JSON file
        file = 'TapDrillMetric.json'
        readPath = 'C://Users/KyleMatheson/OneDrive/00 - BCD Sim/Programming/Fusion360/ConvertCSVtoJSON/JSON/'

        # Initialize empty lists
        sizes = []
        drills = []
        radial_engagements = []
        drill_alternates = []
        radial_engagement_alternates = []

        with open(readPath + file, 'r') as json_file:
            data = json.load(json_file)

        for key in data:
            sizes.append(data[key]['Size'])
            drills.append(data[key]['drill'])
            radial_engagements.append(data[key]['radialEngagement'])
            drill_alternates.append(data[key]['drillAlternate'])
            radial_engagement_alternates.append(data[key]['radialEngagementAlternate'])

        for index in range(len(sizes)):
            pName = (sizes[index].replace('.', '_') + '_tap_drill')  
            pUnit = 'mm'
            pExpression = float(drills[index])
            pComment = ('Tap Drill Size for ' + str(sizes[index]) + 
                        ' with ' + str(radial_engagements[index]) + ' radial engagement.' + 
                        'Alternate drill size is ' + str(drill_alternates[index]) + 
                        ' with ' + str(radial_engagement_alternates[index]) + ' radial engagement.')

            # Convert the float to a string, split it, apply zfill to the parts, and join them back together
            # pExpressionStr = str(pExpression)
            # parts = pExpressionStr.split('.')
            # pExpressionFormatted = '.'.join(part.zfill(2) if part.isdigit() else part for part in parts)
            # pExressionReal = adsk.core.ValueInput.createByString(pExpressionFormatted)
            pExpressionStr = str(pExpression)
            parts = pExpressionStr.split('.')
            # Ensure the part following the decimal always has 2 digits
            if len(parts) > 1 and parts[1].isdigit():
                parts[1] = parts[1].ljust(2, '0')
            pExpressionFormatted = '.'.join(part.zfill(2) if part.isdigit() else part for part in parts)
            pExressionReal = adsk.core.ValueInput.createByString(pExpressionFormatted)           
            design.userParameters.add(pName, pExressionReal, pUnit, pComment)

        ui.messageBox('Metric Tap Drill Parameters Created')
 
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
