import json
basic = '''
{
 "basicdependencies": [
        {
          "dep": "ROOT",
          "governor": "0",
          "governorGloss": "ROOT",
          "dependent": "4",
          "dependentGloss": "consists"
        },
        {
          "dep": "det",
          "governor": "3",
          "governorGloss": "cell",
          "dependent": "1",
          "dependentGloss": "A"
        },
             ]
 }
 '''
data = json.loads(basic)
print(data)


  
