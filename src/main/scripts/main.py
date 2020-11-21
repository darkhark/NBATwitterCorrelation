from nba_player import NBAPlayer
import nba_commisioner
import analyzers.project_analyzer as pa
import loaders.twitter_handle_loader as thl
import pandas as pd
import traceback as tb


def startAnalysis(analysisType, df, tweetsList, regressionMethod='1'):
    analyzer = pa.TweetsAnalyzer(df)
    if analysisType == "1":
        # return analyzer.getSentimentAnalysis(tweetsList, regression=useRegres)
        return analyzer.getSentimentAnalysis(regressionMethod=regressionMethod)
    elif analysisType == "2":
        return analyzer.getEmotionAnalysis(regressionMethod=regressionMethod)
    elif analysisType == "3":
        return analyzer.getEmbeddedAnalysis(regressionMethod=regressionMethod)
    elif analysisType == "4":
        return analyzer.getCombinationAnalysis(tweetsList, regressionMethod=regressionMethod)
    else:
        print("Invalid value entered, please try again.")
    return pd.DataFrame()


allTweetsAndStatsDF = nba_commisioner.getAllStatsAndTweetsAllPlayers(updatePickle=True)
print("Just a few more things to collect...")
allTweetsTextDocumentInputsList = nba_commisioner.getAllTweetsAllPlayersAsTextDocumentInputList()

while True:
    try:
        print("For each question, please answer using the number specified. Otherwise the program will crash and"
              " we'll have to start all over again. To quit, type 'q'. Thank you.\n")
        allOrPlayer = input("Would you like to predict on one player (1) or all players (2)?\n")

        if allOrPlayer == "q":
            break
        else:
            int(allOrPlayer)

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

        analysis = input("Which analysis would you like to run?  "
                         "1: Sentiment, 2: Emotion, 3: Embedding, 4: Combination\n")
        if analysis == "q":
            break
        else:
            int(analysis)

        predictType = input("Would you like to run using LinearRegression (1) or MLP (2) or RandomForest (3)"
                            " to predict outcomes?\n")

        if predictType == "q":
            break
        else:
            int(predictType)

        print("Starting analysis based on the values entered...")

        resultsDictOrDF = pd.DataFrame()
        if singlePlayer:
            player = NBAPlayer(playerNameDict[playerKey])
            playerDF = player.getAllStatsAndTweetsDF()
            playerTweetDocList = player.getAllTweetsAsTextDocumentInputs()
            resultsDictOrDF = startAnalysis(analysis, playerDF, playerTweetDocList, predictType)
        else:
            resultsDictOrDF = startAnalysis(analysis, allTweetsAndStatsDF, allTweetsTextDocumentInputsList, predictType)

        print("Resulting analysis measurements:")
        print(resultsDictOrDF)

        ### Create visualizations ###

        # import RegressionVisualizer
        # RegressionVisualization.plot(allPlayersModeler)

        # import ComparisonVisualizer
        # ComparisonVisualizer.comparePlot(allPlayersModeler, lebronModeler)

    except:  # Bare because we don't care wat the error is, just please don't make us reload the players
        tbError = tb.format_exc()
        print(tbError)
