# FPL Draft Model comparison tool
 Using a Linear Regression model we are able 
 to predict total points for a player based on 
 advanced statistics. Using expected events per 90
allows us to filter out outlier performances and
identify performers who might be valuable if they
were granted more play time.

## Tools
### Player Comparison
Compare the predicted points of two players in the same position

### Positional Predictions
Create csv of all players for a particular position

## Usage
### Player Comparison
```
./run.sh -tool {TYPE} -names {NAMES}
```

## Examples
### Player Comparison
```./run.sh -tool comparison -names Eze Rashford```

### Positional Prediction
```./run.sh -tool prediction -position MID ```

Position Options: GK - DEF - MID - FWD