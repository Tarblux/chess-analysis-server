A Chess Analysis Server that processes games asynchronously while serving preprocessed results to a frontend. The stack is Python + Flask for the API, RabbitMQ with Celery for the message queue, PostgreSQL with SQLAlchemy for storage, and a future ML engine for advanced analysis.Dependecies managed with Poetry.

The architecture has two main pipelines:

1. **Async Pipeline:** Celery Beat (scheduler) enqueues jobs like fetching new games or running analysis, which workers process.
2. **Frontend Pipeline:** Serves preprocessed results to the frontend for visualization and interaction.

---

## General Data Visualizations

- **Total Games Played by Time Control**
- **Win Ratio** (Pie Chart or Stacked Bar)
- **Game Table with Filters** (Interactive Table)
- **Total Time Played** (KPI or Bar)
- **GitHub-style Days Played Chart** (Calendar Heatmap)
- **Streaks**: Win/Loss/Draw (Line Chart or Timeline)
- **Top Countries Played Against** (Bar Chart)
- **Country "Passport" Map** (Choropleth Map)
- **Ratings Over Time by Time Control** (Line Chart)
- **Current Rank** (KPI)
- **Top Openings** (Grouped Bar Chart)
- **Openings Radar: Win Rate** (Radar Chart)
- **Result by Opening** (Stacked Bar Chart)
- **Result by Opponent Rating** (Line or Scatter)
- **Games Won By Type** (Pie or Bar)
- **Games Drawn By Type** (Pie)

---

## Special Games Collection (Hand Picked)

| Collection             | Description |
| :--------------------- | :---------- |
| Longest Game           | Handpicked  |
| Quickest Checkmate     | Handpicked  |
| Most Accurate Game     | >10 moves   |
| Least Accurate Win     |             |
| Least Accurate Game    | >10 moves   |
| Personal Favorite Game |             |
| Funny Game             |             |

---

## In-Depth Analysis Visuals

| Visualization                 | Chart Type        | Description / Use                               |
| :---------------------------- | :---------------- | :---------------------------------------------- |
| Accuracy Over Time            | Line Chart        | Track accuracy by time control                  |
| Accuracy by Game Phase        | Grouped Bar Chart | Openings, middlegame, endgame accuracy          |
| Accuracy per Opening          | Bar/Heatmap       | See which openings correlate with best accuracy |

---

## Advanced Analysis

| Visualization                | Chart Type        | Description                                                         |
| :--------------------------- | :---------------- | :------------------------------------------------------------------ |
| Square Occupancy Heatmap     | Board Heatmap     | Most-occupied squares by pieces; filterable by piece, opening, etc. |
| Piece Survival Rate          | Bar Chart         | How often pieces survive to game end                                |
| Who Captures Whom Matrix     | Matrix Chart      | Which pieces capture which opponents most                           |
| Opening Popularity Over Time | Line/Area Chart   | Track opening usage                                                 |
| Game Tree Visualization      | Tree Diagram      | Opening variation tree, color-coded by result                       |
| Center of Gravity Chart      | Line/Vector Chart | Average piece position throughout game                              |
| Initiative Timeline          | Line Chart        | Engine advantage evaluated over game time                           |
| Brilliant Move Search        | Timeline/List     | Filter/search for brilliant moves                                   |
| Move Time vs Accuracy        | Scatter Plot      | Correlate time spent and move quality                               |
| Avg Move Time by Time Control| Bar/Box Plot      | Analyze pace across controls                                        |


---

## Optional / Bonus Visuals

| Visualization       | Chart Type / Display     | Notes                               |
| :------------------ | :----------------------- | :---------------------------------- |
| Move Type Breakdown | List beside player names | Show best, blunder, brilliant, etc. |

---

## Planned Database Tables

### Table: chess_games

| Field           | Description           |
| :-------------- | :-------------------- |
| id              | Primary key           |
| game_id         | Games ID from chess.com|
| date            | Date played           |
| game_url        | Game link             |
| time_control    | e.g., blitz, rapid    |
| time            | Duration/Time Control |
| my_color        | Color played          |
| my_rating       | Rating                |
| opponent_name   | Name                  |
| opponent_url    | Profile link          |
| opponent_rating | Opponent rating       |
| opponent_color  | Opponent's color      |
| opponent_flag   | Opponent country tag  |
| result          | Win/loss/draw         |
| move_count      | Number of moves       |

### Table: chess_games_analysis

| Field                   | Description                                   |
| :---------------------- | :-------------------------------------------- |
| id                      | Primary key                                   |
| game_id                 | Links to chess_games                          |
| duration                | Game duration                                 |
| opening                 | Player's opening name                         |
| eco                     | Player's opening code                         |
| opp_opening             | Opponent's opening name                       |
| opp_eco                 | Opponent's opening code                       |
| pgn                     | Full game PGN notation                        |
| fen                     | Final position snapshot                       |
| accuracy                | Player's overall accuracy                     |
| opening_accuracy        | Player's Opening Accuracy                     |
| middlegame_accuracy     | Player's Middlegame Accuracy                  |
| endgame_accuracy        | Player's Endgame Accuracy                     |
| opponent_accuracy       | Opponent's overall accuracy                   |
| opp_opening_accuracy    | Opponent's Opening Accuracy                   |
| opp_middlegame_accuracy | Opponent's Middlegame Accuracy                |
| opp_endgame_accuracy    | Opponent's Endgame Accuracy                   |
| opening_moves           | PGN of opening moves                          |
| middlegame_moves        | Sequence of middlegame moves                  |
| endgame_moves           | PGN of endgame moves                          |
| opp_opening_moves       | Opponent's opening PGN                        |
| opp_middlegame_moves    | Opponent's middlegame moves                   |
| opp_endgame_moves       | Opponent's endgame moves                      |
| moves_breakdown         | Player move types (best, blunder, brilliant)  |
| opp_moves_breakdown     | Opponent move types (best, blunder, brilliant)|
| avg_move_time           | Player's average move time                    |
| opp_avg_move_time       | Opponent's average move time                  |
| advantage_timeline      | Engine evaluation timeline (overall trend)    |
| evaluation_timeline     | Engine evaluations per move                   |

### Table: openings
should also consider linking to chess game analysis table to avoid redundancy
| Field        | Description          |
| :----------- | :------------------- |
| id           | Primary key          |
| name         | Opening name         |
| eco          | Opening code         |
| popularity   | Number of times played|
| win_rate     | Win percentage       |
| avg_accuracy | Average accuracy     |
| avg_moves    | Average moves played |

### Table: special_games
| Field        | Description          |
| :----------- | :------------------- |
| id           | Primary key          |
| game_id      | Links to chess_games |
| category     | e.g., longest, quickest|
| description  | Brief description    |

---

## Comprehensive Chart List

| Chart Name                          | Chart Type        |
| :---------------------------------- | :---------------- |
| Total Games Played by Time Control  | Bar Chart         |
| Win Ratio                           | Pie/Stacked Bar   |
| Game Table with Filters             | Interactive Table |
| Total Time Played                   | KPI/Bar           |
| Days Played Heatmap                 | Calendar Heatmap  |
| Streaks (Win/Loss/Draw)             | Line/Timeline     |
| Top Countries Played Against        | Bar Chart         |
| Country "Passport" Map              | Choropleth Map    |
| Ratings Over Time                   | Line Chart        |
| Current Rank                        | KPI               |
| Top Openings                        | Grouped Bar       |
| Openings Radar (Win Rate)           | Radar             |
| Result by Opening                   | Stacked Bar       |
| Result by Opponent Rating           | Line/Scatter      |
| Games Won By Type                   | Pie/Bar           |
| Games Drawn By Type                 | Pie               |
| Accuracy Over Time                  | Line              |
| Accuracy by Game Phase              | Bar               |
| Brilliant Move Search               | Timeline/List     |
| Avg Move Time by Time Control       | Bar/Box Plot      |
| Correlation of Move Time\& Accuracy | Scatter Plot      |
| Accuracy per Opening                | Bar/Heatmap       |
| Square Occupancy Heatmap            | Board Heatmap     |
| Piece Survival Rate                 | Bar               |
| Who Captures Whom Matrix            | Matrix            |
| Game Tree Visualization             | Tree Diagram      |
| Center of Gravity Chart             | Vector/Line       |
| Initiative Timeline                 | Line              |
| Move Type Breakdown                 | List              |
| Opening Popularity Over Time        | Line/Area         |

---

## Chart Types Used

| Chart Type             | Usage Example                                    |
| :--------------------- | :----------------------------------------------- |
| Bar Chart              | Time control distribution, top countries         |
| Grouped Bar Chart      | Top openings, accuracy by phase                  |
| Stacked Bar Chart      | Win ratio, result by opening                     |
| Pie Chart              | Win ratio, games won type                        |
| Line Chart             | Ratings over time, streaks                       |
| Scatter Plot           | Move time vs accuracy, result by opponent rating |
| Radar Chart            | Openings win rate                                |
| Calendar Heatmap       | GitHub day chart                                 |
| Choropleth Map         | Country passport map                             |
| Board Heatmap          | Square occupancy                                 |
| Matrix Chart           | Captures breakdown                               |
| Vector/Flow Chart      | Center of gravity movement                       |
| Timeline               | Streaks, advantage timeline                      |
| KPI                    | Current rank, total time played                  |
| Area Chart             | Opening popularity                               |
| Interactive Table      | Games table                                      |
| Branching Tree Diagram | Opening variation visualization                  |
| Filtered Game List     | Brilliant moves, special games                   |

---

## Extras \& Ideas

- **Daily summaries and tags**: e.g. 'comeback', 'funny', 'tactical masterpiece'.
- **GitHub-style days chart**: Hover for wins/losses and accuracy color coding.
- **Game blurb section**: Comment beneath each chart on trends or insights
