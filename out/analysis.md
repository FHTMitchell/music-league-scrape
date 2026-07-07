# Music League analysis

## Overview

| metric              |   value |
|---------------------|---------|
| Leagues             |       6 |
| Rounds              |      55 |
| Songs submitted     |     663 |
| Distinct submitters |      14 |
| Distinct voters     |      14 |

## Player Ranking

_Players with at least 2 songs submitted, ranked by mean within-round z-score (score normalised against the other songs in the same round). avg_z > 0 means the player typically beats the round average; total_received is the points the player actually banked (forfeits count as 0)._

|   rank | player           |   avg_z |   total_z |   total_received |   songs |
|--------|------------------|---------|-----------|------------------|---------|
|      1 | Sam Mit          |    0.43 |     23.01 |              314 |      53 |
|      2 | Fred N           |    0.23 |     12.75 |              268 |      55 |
|      3 | harryg           |    0.18 |      9.83 |              266 |      55 |
|      4 | Jimbabwe         |    0.18 |      6.08 |              179 |      33 |
|      5 | Josh B           |    0.12 |      5.46 |              186 |      47 |
|      6 | Fergus M         |    0.12 |      6.82 |              227 |      55 |
|      7 | pollyannaw       |    0.05 |      0.87 |               82 |      18 |
|      8 | Joe              |   -0.07 |     -2.99 |              163 |      45 |
|      9 | Joshua W         |   -0.16 |     -8.35 |              179 |      53 |
|     10 | MorbidlyObeseCat |   -0.19 |    -10.18 |              200 |      55 |
|     11 | Solsti           |   -0.19 |     -8.17 |              159 |      43 |
|     12 | Luke G           |   -0.22 |    -10.75 |              164 |      50 |
|     13 | Peter L          |   -0.24 |    -11.59 |              176 |      49 |
|     14 | Sam Mil          |   -0.24 |    -12.6  |              169 |      52 |

## League Winners

_Player with the highest total points banked in each league. Uses received points (forfeits count as 0), matching the real standings._

| league               | player   |   total |   songs |
|----------------------|----------|---------|---------|
| Basic League         | Joe      |      31 |       8 |
| Jamie is a soft boy  | Sam Mit  |     101 |      13 |
| Montage League       | Josh B   |      34 |       8 |
| Personal League      | Sam Mit  |      88 |      12 |
| Show me what you got | Fred N   |      75 |      10 |
| Song for the Season  | Fred N   |      19 |       4 |

## Medal Ranking

_Olympic-style: 3 points for finishing 1st in a round, 2 for 2nd, 1 for 3rd. Ties share the higher rank, so two songs tied for 1st both earn 3 medal points._

|   rank | player           |   gold 🥇 |   silver 🥈 |   bronze 🥉 |   medal_points |
|--------|------------------|----------|------------|------------|----------------|
|      1 | Sam Mit          |       14 |          7 |          6 |             62 |
|      2 | Fred N           |        8 |          7 |          8 |             46 |
|      3 | harryg           |        8 |          7 |          6 |             44 |
|      4 | Fergus M         |        6 |          9 |          4 |             40 |
|      5 | Joe              |        6 |          2 |          4 |             26 |
|      6 | Joshua W         |        6 |          0 |          8 |             26 |
|      7 | Josh B           |        2 |          7 |          5 |             25 |
|      8 | Solsti           |        3 |          5 |          4 |             23 |
|      9 | MorbidlyObeseCat |        3 |          5 |          4 |             23 |
|     10 | Luke G           |        1 |          8 |          4 |             23 |
|     11 | Jimbabwe         |        3 |          3 |          5 |             20 |
|     12 | Sam Mil          |        2 |          4 |          6 |             20 |
|     13 | Peter L          |        2 |          3 |          5 |             17 |
|     14 | pollyannaw       |        3 |          0 |          1 |             10 |

## Biggest Fans

_For each submitter, the voter whose votes land furthest from that voter's own per-round vote distribution. Metric: mean z-score across shared rounds, where z = (vote - voter_round_mean) / voter_round_std and unrated songs in a participated round count as 0. Rounds where the voter gave every song the same vote are dropped (z is undefined). pts is the raw cumulative points for context. See the 'Fan / Hater Heatmap' for the full pair-by-pair view._

|   rank | player           | biggest_fan      |   fan_z |   pts |   shared_rounds |
|--------|------------------|------------------|---------|-------|-----------------|
|      1 | pollyannaw       | harryg           |    0.87 |    16 |              18 |
|      2 | Sam Mit          | Luke G           |    0.68 |    44 |              48 |
|      3 | harryg           | Joe              |    0.53 |    30 |              45 |
|      4 | Josh B           | Sam Mil          |    0.46 |    30 |              43 |
|      5 | Fergus M         | Josh B           |    0.37 |    29 |              46 |
|      6 | Solsti           | Sam Mil          |    0.36 |    27 |              40 |
|      7 | Fred N           | Jimbabwe         |    0.35 |    26 |              33 |
|      8 | Jimbabwe         | Sam Mit          |    0.31 |    22 |              33 |
|      9 | Joshua W         | Peter L          |    0.29 |    26 |              46 |
|     10 | Sam Mil          | MorbidlyObeseCat |    0.29 |    30 |              51 |
|     11 | Joe              | harryg           |    0.26 |    24 |              45 |
|     12 | MorbidlyObeseCat | pollyannaw       |    0.21 |     9 |              18 |
|     13 | Luke G           | Fred N           |    0.19 |    29 |              50 |
|     14 | Peter L          | Joshua W         |    0.16 |    24 |              47 |

## Biggest Haters

_For each submitter, the voter whose votes land furthest from that voter's own per-round vote distribution. Metric: mean z-score across shared rounds, where z = (vote - voter_round_mean) / voter_round_std and unrated songs in a participated round count as 0. Rounds where the voter gave every song the same vote are dropped (z is undefined). pts is the raw cumulative points for context. See the 'Fan / Hater Heatmap' for the full pair-by-pair view._

|   rank | player           | biggest_hater    |   hater_z |   pts |   shared_rounds |
|--------|------------------|------------------|-----------|-------|-----------------|
|      1 | Joe              | pollyannaw       |     -0.52 |     0 |               8 |
|      2 | Sam Mit          | pollyannaw       |     -0.47 |     2 |              18 |
|      3 | Fred N           | pollyannaw       |     -0.46 |     2 |              18 |
|      4 | Joshua W         | Solsti           |     -0.45 |     1 |              41 |
|      5 | pollyannaw       | Fred N           |     -0.42 |     3 |              18 |
|      6 | Peter L          | Sam Mil          |     -0.39 |     5 |              45 |
|      7 | Luke G           | MorbidlyObeseCat |     -0.38 |     5 |              49 |
|      8 | Solsti           | Sam Mit          |     -0.32 |     5 |              43 |
|      9 | MorbidlyObeseCat | Joe              |     -0.29 |     7 |              45 |
|     10 | Josh B           | Joe              |     -0.26 |     6 |              41 |
|     11 | Sam Mil          | Fergus M         |     -0.26 |    11 |              50 |
|     12 | harryg           | Sam Mil          |     -0.17 |    11 |              47 |
|     13 | Fergus M         | Fred N           |     -0.13 |    15 |              55 |
|     14 | Jimbabwe         | Joshua W         |     -0.13 |     8 |              31 |

## Fan / Hater Heatmap

_Mean z-score per (submitter row, voter column) pair. Green = the voter tends to give that submitter higher-than-average votes (fan); red = lower-than-average (hater). Diagonal blank: nobody votes on their own song. Names alphabetised on both axes._

![Fan / Hater Heatmap](fan_hater_heatmap.png)

## Over Performers

_Top 10 songs ranked by how many standard deviations above the round average they scored — a 10 in a round averaging 4 outranks a 10 in a round averaging 8._

|   rank |   z_in_round |   score |   round_avg | song                      | artist                     | player   | league               | round             |
|--------|--------------|---------|-------------|---------------------------|----------------------------|----------|----------------------|-------------------|
|      1 |         2.98 |      18 |           5 | Difyrrwch                 | The Trials of Cato         | Sam Mit  | Personal League      | Henry             |
|      2 |         2.32 |      11 |           5 | Books from Boxes          | Maximo Park                | Joe      | Personal League      | Sam               |
|      3 |         2.25 |      14 |           6 | Hurt                      | Johnny Cash                | Sam Mil  | Show me what you got | Covers            |
|      4 |         2.25 |      13 |           5 | Riders on the Storm       | The Doors                  | Sam Mit  | Personal League      | Mitchell          |
|      5 |         2.24 |      14 |           6 | Night On My Mind          | Sharky                     | Jimbabwe | Show me what you got | Awesome Obscurity |
|      6 |         2.24 |      15 |           4 | 19-2000 - Soulchild Remix | Gorillaz                   | Sam Mit  | Jamie is a soft boy  | Best Remix        |
|      7 |         2.22 |      11 |           5 | Face Down                 | The Red Jumpsuit Apparatus | Solsti   | Personal League      | Jack              |
|      8 |         2.21 |       7 |           3 | Learn to Fly              | Foo Fighters               | Josh B   | Montage League       | Family time       |
|      9 |         2.19 |      14 |           6 | Hit the Road Jack         | Ray Charles                | Luke G   | Show me what you got | Shorties          |
|     10 |         2.12 |       6 |           3 | Fat Lip                   | Sum 41                     | Josh B   | Montage League       | Pre-drinks        |

## Under Performers

_Top 10 songs ranked by how many standard deviations below the round average they scored. The score column is still the raw points; round_avg is the mean across all songs in that round._

|   rank |   z_in_round |   score |   round_avg | song                                         | artist           | player   | league              | round                                   |
|--------|--------------|---------|-------------|----------------------------------------------|------------------|----------|---------------------|-----------------------------------------|
|      1 |        -2.82 |     -12 |        4    | Guitar Pick                                  | MEMI             | Joshua W | Jamie is a soft boy | Dirty foreigners                        |
|      2 |        -2.28 |      -4 |        2.73 | Your Heart Is a Muscle the Size of Your Fist | Ramshackle Glory | Fred N   | Basic League        | Body Part                               |
|      3 |        -2.17 |      -1 |        3    | Sheila                                       | Jamie T          | harryg   | Basic League        | Jamie’s round                           |
|      4 |        -2.12 |       0 |        3    | Cigaro                                       | System Of A Down | Sam Mil  | Montage League      | Pre-drinks                              |
|      5 |        -2.1  |     -10 |        4    | Hands Open                                   | Snow Patrol      | Luke G   | Jamie is a soft boy | Song from a video game soundtrack.      |
|      6 |        -2.09 |      -9 |        4    | Into the West                                | Annie Lennox     | Fergus M | Jamie is a soft boy | Worst (Best) songs to play at a funeral |
|      7 |        -2.04 |      -5 |        4    | 21 Seconds                                   | So Solid Crew    | Josh B   | Jamie is a soft boy | Bow Chicka Wow Wow                      |
|      8 |        -1.94 |       0 |        5    | Whiteboy - Radio Edit                        | James            | Luke G   | Personal League     | Sam                                     |
|      9 |        -1.89 |      -2 |        2.45 | Sugar Man                                    | Rodríguez        | Sam Mit  | Basic League        | Job                                     |
|     10 |        -1.85 |      -5 |        4    | Angel Of Death                               | Slayer           | Luke G   | Jamie is a soft boy | Freebird!                               |

## Polarising Songs

_Top 10 songs that genuinely split the room. Metric: per song, the std of its explicit (non-zero) votes, z-scored against the other songs' stds in the same round. Songs need at least 4 explicit raters AND at least one positive AND at least one negative vote — a standout +N alone is a consensus winner, not polarisation. Leagues without downvotes are excluded by construction (no way to express dislike). total_up / total_down are the sums of positive / |negative| points; up_votes / down_votes are the head-counts._

|   rank |    z |   score |   total_up |   total_down |   up_votes |   down_votes | song                                     | artist            | player           | league              | round                                   |
|--------|------|---------|------------|--------------|------------|--------------|------------------------------------------|-------------------|------------------|---------------------|-----------------------------------------|
|      1 | 2.41 |      -4 |          5 |            9 |          3 |            6 | Saturday Night                           | Whigfield         | Luke G           | Jamie is a soft boy | You lot are fucking old                 |
|      2 | 2.25 |       0 |          5 |            5 |          2 |            4 | Cha-Ching (Till We Grow Older)           | Imagine Dragons   | Fergus M         | Jamie is a soft boy | Deep Cuts                               |
|      3 | 2.16 |      -1 |          6 |            7 |          4 |            4 | Instant Crush (feat. Julian Casablancas) | Daft Punk         | Jimbabwe         | Jamie is a soft boy | Freebird!                               |
|      4 | 2.03 |       4 |         10 |            6 |          5 |            5 | Hayloft                                  | Mother Mother     | Fred N           | Jamie is a soft boy | A family affair                         |
|      5 | 1.91 |       3 |          5 |            2 |          2 |            2 | Faith - Remastered                       | George Michael    | Fred N           | Jamie is a soft boy | From the grave                          |
|      6 | 1.88 |       7 |         10 |            3 |          6 |            2 | Good Riddance (Time of Your Life)        | Green Day         | Peter L          | Jamie is a soft boy | Worst (Best) songs to play at a funeral |
|      7 | 1.72 |       2 |          5 |            3 |          4 |            3 | PROJECT: Yi                              | League of Legends | MorbidlyObeseCat | Basic League        | Jamie’s round                           |
|      8 | 1.71 |       5 |          7 |            2 |          4 |            2 | Black Lungs                              | Architects        | harryg           | Basic League        | Colour                                  |
|      9 | 1.68 |       8 |          9 |            1 |          4 |            1 | Ni**as In Paris                          | JAŸ-Z             | Josh B           | Jamie is a soft boy | He did what?                            |
|     10 | 1.66 |       0 |          4 |            4 |          3 |            3 | Sexy And I Know It                       | LMFAO             | Sam Mil          | Jamie is a soft boy | Bow Chicka Wow Wow                      |

## Most Played Artists

_Top 10 artists by number of songs submitted across all rounds._

|   rank | artist                |   plays |   total_score |   avg_score |
|--------|-----------------------|---------|---------------|-------------|
|      1 | The Wombats           |      12 |            28 |        2.33 |
|      2 | Green Day             |       6 |            36 |        6    |
|      3 | System Of A Down      |       6 |            23 |        3.83 |
|      4 | Gorillaz              |       4 |            29 |        7.25 |
|      5 | Muse                  |       4 |            26 |        6.5  |
|      6 | Red Hot Chili Peppers |       4 |            17 |        4.25 |
|      7 | Queen                 |       3 |            27 |        9    |
|      8 | Fall Out Boy          |       3 |            20 |        6.67 |
|      9 | JAŸ-Z                 |       3 |            20 |        6.67 |
|     10 | Dizzee Rascal         |       3 |            19 |        6.33 |

## Repeats

_Tracks (matched by Spotify track ID) submitted in more than one round, either by the same player or by different players._

|   rank |   plays | song                                         | artist                       | players                      |   total_score |
|--------|---------|----------------------------------------------|------------------------------|------------------------------|---------------|
|      1 |       2 | Fairytale of New York (feat. Kirsty MacColl) | The Pogues                   | MorbidlyObeseCat, Solsti     |            18 |
|      2 |       2 | This Girl (Kungs Vs. Cookin' On 3 Burners)   | Kungs                        | Luke G, Peter L              |            14 |
|      3 |       2 | Dear Maria, Count Me In                      | All Time Low                 | Joshua W, Solsti             |            13 |
|      4 |       2 | Snacky In My Packy                           | Gabby's Dollhouse            | Fred N, harryg               |            12 |
|      5 |       2 | The Bad Touch                                | Bloodhound Gang              | Jimbabwe, Josh B             |            12 |
|      6 |       2 | back to friends                              | sombr                        | MorbidlyObeseCat, pollyannaw |            10 |
|      7 |       2 | Supermassive Black Hole                      | Muse                         | Joshua W, pollyannaw         |            10 |
|      8 |       2 | Ni**as In Paris                              | JAŸ-Z                        | Josh B, Sam Mil              |            10 |
|      9 |       2 | Invaders Must Die                            | The Prodigy                  | Sam Mit                      |             6 |
|     10 |       2 | Misery Business                              | Paramore                     | MorbidlyObeseCat, Solsti     |             6 |
|     11 |       2 | The Times They Are A-Changin'                | Bob Dylan                    | Joshua W, Sam Mil            |             5 |
|     12 |       2 | Turn                                         | The Wombats                  | Sam Mil                      |             4 |
|     13 |       2 | Jack Sparrow                                 | The Lonely Island            | Fergus M, Solsti             |             3 |
|     14 |       2 | Heat Waves                                   | Glass Animals                | Sam Mil, Solsti              |             1 |
|     15 |       2 | Get Low                                      | Lil Jon & The East Side Boyz | Josh B, Solsti               |             0 |
|     16 |       2 | Get Up, Stand Up                             | Bob Marley & The Wailers     | MorbidlyObeseCat, Solsti     |            -2 |
|     17 |       2 | 21 Seconds                                   | So Solid Crew                | Josh B, Peter L              |            -3 |

## Forfeits

_Points a player's songs earned but the player never banked, because they missed the voting deadline. Music League zeroes the points you receive if you don't cast your own ballot (downvotes against you still count). points_lost = score the song earned − points actually received._

|   rank | player           |   songs_forfeited |   total_points_lost |
|--------|------------------|-------------------|---------------------|
|      1 | MorbidlyObeseCat |                 1 |                   3 |
|      2 | Josh B           |                 1 |                   7 |
|      3 | Fergus M         |                 2 |                   7 |
|      4 | Peter L          |                 1 |                   7 |
|      5 | Sam Mil          |                 4 |                  11 |
