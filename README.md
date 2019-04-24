## Getting Started

1. Goto data/ directory
2. Run source_matches.py
3. Run source_match_players.py

4. Run process_matches.py
5. Run process_match_players.py

6. Run prepare_trainset.py

## Feature Idea

Some features I can think of

    - Home country
    - Exp level with the season (weather)
    - Familiarity with the pitch
    - Batting power : Past 1 year avg score, avg no of fours, avg no of sixes, number of good batsmans, run rate per over
    - Bowling power : Past 1 year avg no of wickets taken, wicket rate per over, fours and sixes scored by the other team (revered), avg score of the opposition (reversed)
    - Fielding power : Past 1 year avg no of catches and run outs, catches missed (reversed), fours due to poor fielding (reversed)

## Domain Knowledge

1.  **ODI** - one day international, match last for one day. Each team gets 50 overs to bat and 50 overs to bowl. Each over has 6 bowls. The second team who bats should chase the score of the first team. 
2.  **Tests** - test matches last for 3 days if im not wrong, and very slow paced. I'm not very familiar with the rules. Think there is no limit for the number of overs each team gets. Most of the times, test matches end as a draw, without a winner 
3.  **T20** - same as ODI, but each team gets 20 overs to bat and 20 overs to bowl. So its very fast paced, they try to score as much as they can within 20 overs and take risk 
