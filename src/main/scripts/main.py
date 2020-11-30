import time
from pathlib import Path
from nba_player import NBAPlayer
import nba_commisioner
import analyzers.project_analyzer as pa
import loaders.twitter_handle_loader as thl
import pandas as pd
import traceback as tb
import plotly.express as px


def startAnalysis(analysisType, df, points, demo, regressionMethod='1'):
    analyzer = pa.TweetsAnalyzer(df)
    if analysisType == "1":
        analysisReults = analyzer.getSentimentAnalysis(points, regressionMethod=regressionMethod)
        if demo:
            analyzer.sentimentPlot.show()
        return analysisReults
    elif analysisType == "2":
        analysisReults = analyzer.getEmotionAnalysis(points, regressionMethod=regressionMethod)
        if demo:
            analyzer.emotionPlot.show()
        return analysisReults
    elif analysisType == "3":
        analysisReults = analyzer.getEmbeddedAnalysis(points, regressionMethod=regressionMethod)
        if demo:
            analyzer.embeddingPlot.show()
        return analysisReults
    elif analysisType == "4":
        return analyzer.getCombinationAnalysis(points, regressionMethod=regressionMethod)
    else:
        print("Invalid value entered, please try again.")

    return pd.DataFrame()


allTweetsAndStatsDF = nba_commisioner.getAllStatsAndTweetsAllPlayers(updatePickle=False)

while True:
    try:
        # This part is common among both modes (demo and experiment)
        print("For each question, please answer using the number specified. Otherwise the program will crash and"
              " we'll have to start all over again. To quit, type 'q'. Thank you.\n")

        expOrDemo = input("Would you like to run the program in the demo mode (1) or the experiement mode (2)?\n")

        if expOrDemo == "q":
            break
        elif expOrDemo == "1":
            expOrDemo = True
        elif expOrDemo == "2":
            expOrDemo = False
        elif 0 > int(expOrDemo) > 2:
            print("Invalid option selected. Try again.\n")

        predictPoints = input("Would you like to predict the points (1) or accuracy (2) "
                              "of the amount above or below players' average?\n")

        if predictPoints == "q":
            break
        elif predictPoints == "1":
            predictPoints = True
        elif predictPoints == "2":
            predictPoints = False
        elif 0 > int(predictPoints) > 2:
            print("Invalid option selected. Try again.\n")

        allOrPlayer = input("Would you like to predict on one player (1) or all players (2)?\n")

        if allOrPlayer == "q":
            break
        elif 0 > int(allOrPlayer) > 2:
            print("Invalid option selected. Try again.\n")

        singlePlayer = False
        playerKey = 0
        playerNameDict = {}
        if allOrPlayer == "1":  # If one player is wanted for analysis
            singlePlayer = True
            questionString = "Which player would you like to analyze?\n"
            count = 0
            for name in thl.getAllTwitterHandles().keys():
                errorPlayers = ['Devin Booker', 'Trae Young', 'Luka Doncic', 'Donovan Mitchell', 'Jayson Tatum',
                                'Kevin Durant', 'Joel Embiid', 'DeMarcus Cousins', 'Klay Thompson']
                if name not in errorPlayers:
                    count += 1
                    playerNameDict[str(count)] = name
                    questionString += str(count) + ": " + name + "  "
                    if count % 3 == 0:
                        questionString += "\n"
            playerKey = input(questionString + "\n")

        if playerKey == "q":
            break
        else:
            int(playerKey)

        # if the demo mode is chosen continue with the questioning, else loop over all possible setups
        if expOrDemo:
            analysis = input("Which analysis would you like to run?  "
                             "1: Sentiment, 2: Emotion, 3: Embedding, 4: Combination\n")

            if analysis == "q":
                break
            elif 0 > int(analysis) > 4:
                print("Invalid option selected. Try again.\n")

            predictType = input("Would you like to run using LinearRegression (1) or MLP (2) or RandomForest (3)"
                                " to predict outcomes?\n")

            if predictType == "q":
                break
            elif 0 > int(predictPoints) > 3:
                print("Invalid option selected. Try again.\n")

            print("Starting analysis based on the values entered...")
            resultList = list()
            resultList.append(analysis)
            resultList.append(predictType)
            analysisResultsDF = pd.DataFrame()
            resultsDF = pd.DataFrame()
            analysisTypes = {'1': 'Sentiment', '2': 'Emotion', '3': 'Embedded', '4': 'Combined'}
            predictTypes = {'1': 'LinearRegression', '2': 'MLP', '3': 'RandomForest'}
            if singlePlayer:
                player = NBAPlayer(playerNameDict[playerKey])
                playerName = player.name
                playerDF = player.getAllStatsAndTweetsDF()
                playerTweetDocList = player.getAllTweetsAsTextDocumentInputs()
                results = startAnalysis(analysis, playerDF, predictPoints, expOrDemo, predictType)
                resultsDF.insert(0,
                                 results.regResultsDF['y_pred'].name + '_' + analysisTypes[analysis] + '_' +
                                 predictTypes[predictType],
                                 results.regResultsDF['y_pred'],
                                 True)
            else:
                player = None
                playerName = 'All'
                results = startAnalysis(analysis, allTweetsAndStatsDF, predictPoints, expOrDemo, predictType)
                resultsDF.insert(0,
                                 results.regResultsDF['y_pred'].name + '_' + analysisTypes[analysis] + '_' +
                                 predictTypes[predictType],
                                 results.regResultsDF['y_pred'],
                                 True)
            resultList.extend([results.resultsDict[result] for result in results.resultsDict.keys()])
            analysisResultsDF = analysisResultsDF.append([resultList])
        else:
            analysisTypes = {'1': 'Sentiment', '2': 'Emotion', '3': 'Embedded', '4': 'Combined'}
            predictTypes = {'1': 'LinearRegression', '2': 'MLP', '3': 'RandomForest'}
            analysisResultsDF = pd.DataFrame()
            resultsDF = pd.DataFrame()
            for analysis in analysisTypes:
                for predictType in predictTypes.keys():
                    resultList = list()
                    resultList.append(analysisTypes[analysis])
                    resultList.append(predictTypes[predictType])
                    print("Starting analysis based on the values entered...")
                    if singlePlayer:
                        player = NBAPlayer(playerNameDict[playerKey])
                        playerName = player.name
                        playerDF = player.getAllStatsAndTweetsDF()
                        playerTweetDocList = player.getAllTweetsAsTextDocumentInputs()
                        results = startAnalysis(analysis, playerDF, predictPoints, expOrDemo, predictType)
                        resultsDF.insert(0,
                                        results.regResultsDF['y_pred'].name + '_' + analysisTypes[analysis] + '_' +
                                        predictTypes[predictType],
                                        results.regResultsDF['y_pred'],
                                        True)
                    else:
                        player = None
                        playerName = 'All'
                        results = startAnalysis(analysis, allTweetsAndStatsDF, predictPoints, expOrDemo, predictType)
                        resultsDF.insert(0,
                                        results.regResultsDF['y_pred'].name + '_' + analysisTypes[analysis] + '_' +
                                        predictTypes[predictType],
                                        results.regResultsDF['y_pred'],
                                        True)
                    resultList.extend([results.resultsDict[result] for result in results.resultsDict.keys()])
                    analysisResultsDF = analysisResultsDF.append([resultList])

        resultsDF.insert(0,
                         'y_test',
                         results.regResultsDF['y_test'],
                         True)

        print("Resulting analysis measurements:")
        results.print_results(singlePlayer, player, analysis)

        analysisResultsDF.columns = ['analysis_type', 'regressions_model', 'r2', 'mse']
        ### Create visualizations ###
        if predictPoints:
            title = 'Points'
        else:
            title = 'Accuracy'
        fig_mse = px.bar(analysisResultsDF, x="regressions_model", y="mse", color="regressions_model",
                         facet_col="analysis_type", title='MSE - ' + title)
        fig_mse.show()
        fig_r2 = px.bar(analysisResultsDF, x="regressions_model", y="r2", color="regressions_model",
                        facet_col="analysis_type", title='R2 - ' + title)
        fig_r2.show()
        fig_box = px.box(resultsDF.melt(), x="variable", y="value", color="variable", title='Box Plot - ' + title)
        fig_box.show()

    except:  # Bare because we don't care wat the error is, just please don't make us reload the players
        tbError = tb.format_exc()
        print(tbError)
