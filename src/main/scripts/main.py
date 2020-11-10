import json

with open('docs/TwitterHandles/twitter_handles.json') as json_file:
    twitter_handles = json.load(json_file)

### Instantiate the NBAPlayer objects ###

# players = []
# for handle in TwitterHandles:
#     players.append(NBAPlayer(handle))

# lebron = NBAPlayer(TwitterHandle.lebron_james)

### Pass NBAPlayer(s) to SentimentModeler ###

# import SentimentModeler

# allPlayersModeler = SentimentModeler(players)
# lebronModeler = SentimentModeler([lebron])

### Use the modeler to create visualizations ###

# import RegressionVisualizer
# RegressionVisualization.plot(allPlayersModeler)

# import ComparisonVisualizer
# ComparisonVisualizer.comparePlot(allPlayersModeler, lebronModeler)

