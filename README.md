# phant0m

### motivation

The ideas is to understand stock market performance and build a stock market prediction model using previous price action. The old adage "past performance doesn't guarantee future results" was swept under the rug for this analysis.

There are currently many successful rules-based systems which are considered "trend following" systems. They work surprisingly well when introducing the concept of leverage. They work like so: When the trend is up, buy a leveraged security. When the trend is down, buy a hedge or sell.

However, determining the trend can be difficult and knowing when to buy and sell can often lead to false positives. Is there a way to gain an edge on trend following systems?

### data exploration, unsupervised learning

identifying candle sticks using k-means:

![k-means](https://i.imgur.com/2pqfEMX.png)

There were 6 input features used relating to the candle's attributes such as range, size of wicks (high and low), and size of the body. When k=5, we have large green, small green, flat, small red, and large red. See: price_unsupervised.pynb.

### model building
#### feature engineering

![features](https://i.imgur.com/e9twF7S.png)

We're looking for momentum features, so we looked at moving averages: 3 day, 7 day, and 200 day. 

We also want to know the current day's characterstics: wide range, large green day, flat day, etc.

To keep it simple, we'll focus on binary classification: should we hold until the next day or sell? Our labels are whether the future three-day returns are favorable or worth taking action: -1 for reasonable drop, or 1 for hold.

#### random forest

We're using a random forest for about 10 years worth of data. Max depth of 2-5 only changed accuracy +/- 1%.

![classification_report](https://i.imgur.com/xKxe7xj.png)

### Conclusion

With an accuracy of 76%, it may seem quite powerful. But, since the classes were approximately a 70/30 split, it's only slightly better than guessing the majority class. 

My favorite takeaway: The majority of guesses for -1 (80%) are below the 200 day MA. Precision for -1 guesses is about 40% which is better than I'd expect. Is this better than rules-based system? Probably not.

#### Next steps

- engineer more features
- incorporate to an actual trading model with logic and assess performance
- use deep learning
