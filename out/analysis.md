# Music League analysis

## Overview

| metric              |   value |
|---------------------|---------|
| Leagues             |       5 |
| Rounds              |      43 |
| Songs submitted     |     520 |
| Distinct submitters |      14 |
| Distinct voters     |      14 |

## Player Ranking

_Players with at least 2 songs submitted, ranked by mean within-round z-score (score normalised against the other songs in the same round). avg_z > 0 means the player typically beats the round average; total_score is the raw points sum._

|   rank | player           |   avg_z |   total_z |   total_score |   songs |
|--------|------------------|---------|-----------|---------------|---------|
|      1 | Sam Mit          |    0.39 |     16.1  |           226 |      41 |
|      2 | Jimbabwe         |    0.19 |      6.28 |           179 |      33 |
|      3 | harryg           |    0.18 |      7.91 |           197 |      43 |
|      4 | Fred N           |    0.17 |      7.12 |           192 |      43 |
|      5 | Josh B           |    0.12 |      4.14 |           131 |      35 |
|      6 | Fergus M         |    0.11 |      4.56 |           169 |      43 |
|      7 | pollyannaw       |    0.05 |      0.88 |            82 |      18 |
|      8 | Joe              |   -0.04 |     -1.23 |           107 |      33 |
|      9 | Luke G           |   -0.08 |     -2.86 |           125 |      38 |
|     10 | Joshua W         |   -0.16 |     -6.4  |           121 |      41 |
|     11 | Peter L          |   -0.21 |     -7.7  |           138 |      37 |
|     12 | Solsti           |   -0.23 |     -7.28 |           106 |      31 |
|     13 | MorbidlyObeseCat |   -0.24 |    -10.3  |           142 |      43 |
|     14 | Sam Mil          |   -0.27 |    -11.1  |           131 |      41 |

## League Winners

_Player with the highest total score in each league._

| league               | player   |   total |   songs |
|----------------------|----------|---------|---------|
| Basic League         | Joe      |      31 |       8 |
| Jamie is a soft boy  | Sam Mit  |     101 |      13 |
| Montage League       | Josh B   |      34 |       8 |
| Show me what you got | Fred N   |      75 |      10 |
| Song for the Season  | Fred N   |      19 |       4 |

## Medal Ranking

_Olympic-style: 3 points for finishing 1st in a round, 2 for 2nd, 1 for 3rd. Ties share the higher rank, so two songs tied for 1st both earn 3 medal points._

|   rank | player           |   gold 🥇 |   silver 🥈 |   bronze 🥉 |   medal_points |
|--------|------------------|----------|------------|------------|----------------|
|      1 | Sam Mit          |       10 |          5 |          5 |             45 |
|      2 | harryg           |        6 |          7 |          5 |             37 |
|      3 | Fred N           |        6 |          5 |          5 |             33 |
|      4 | Fergus M         |        6 |          5 |          4 |             32 |
|      5 | Joe              |        5 |          2 |          2 |             21 |
|      6 | Joshua W         |        5 |          0 |          5 |             20 |
|      7 | Jimbabwe         |        3 |          3 |          5 |             20 |
|      8 | Josh B           |        2 |          4 |          5 |             19 |
|      9 | Luke G           |        1 |          7 |          2 |             19 |
|     10 | Sam Mil          |        2 |          4 |          4 |             18 |
|     11 | MorbidlyObeseCat |        2 |          4 |          4 |             18 |
|     12 | Peter L          |        1 |          3 |          4 |             13 |
|     13 | Solsti           |        2 |          2 |          2 |             12 |
|     14 | pollyannaw       |        3 |          0 |          1 |             10 |

## Biggest Fans

_For each submitter, the voter whose votes land furthest from that voter's own per-round vote distribution. Metric: mean z-score across shared rounds, where z = (vote - voter_round_mean) / voter_round_std and unrated songs in a participated round count as 0. Rounds where the voter gave every song the same vote are dropped (z is undefined). pts is the raw cumulative points for context. See 'Fan / Hater Scores' at the end of the report for the unaggregated pair-by-pair view._

|   rank | player           | biggest_fan      |   fan_z |   pts |   shared_rounds |
|--------|------------------|------------------|---------|-------|-----------------|
|      1 | pollyannaw       | harryg           |    0.87 |    16 |              18 |
|      2 | Sam Mit          | Luke G           |    0.54 |    30 |              36 |
|      3 | harryg           | Joe              |    0.54 |    21 |              33 |
|      4 | Josh B           | Sam Mil          |    0.52 |    24 |              34 |
|      5 | Fergus M         | Josh B           |    0.49 |    23 |              34 |
|      6 | Joe              | harryg           |    0.45 |    20 |              33 |
|      7 | Solsti           | Sam Mil          |    0.41 |    22 |              31 |
|      8 | Luke G           | Sam Mit          |    0.38 |    20 |              36 |
|      9 | Fred N           | Jimbabwe         |    0.35 |    26 |              33 |
|     10 | Jimbabwe         | Sam Mit          |    0.31 |    22 |              33 |
|     11 | Sam Mil          | MorbidlyObeseCat |    0.29 |    23 |              40 |
|     12 | Joshua W         | pollyannaw       |    0.26 |     9 |              16 |
|     13 | MorbidlyObeseCat | pollyannaw       |    0.21 |     9 |              18 |
|     14 | Peter L          | harryg           |    0.21 |    21 |              37 |

## Biggest Haters

_For each submitter, the voter whose votes land furthest from that voter's own per-round vote distribution. Metric: mean z-score across shared rounds, where z = (vote - voter_round_mean) / voter_round_std and unrated songs in a participated round count as 0. Rounds where the voter gave every song the same vote are dropped (z is undefined). pts is the raw cumulative points for context. See 'Fan / Hater Scores' at the end of the report for the unaggregated pair-by-pair view._

|   rank | player           | biggest_hater    |   hater_z |   pts |   shared_rounds |
|--------|------------------|------------------|-----------|-------|-----------------|
|      1 | Joe              | pollyannaw       |     -0.52 |     0 |               8 |
|      2 | Joshua W         | Sam Mil          |     -0.47 |     0 |              36 |
|      3 | Sam Mit          | pollyannaw       |     -0.47 |     2 |              18 |
|      4 | Fred N           | pollyannaw       |     -0.46 |     2 |              18 |
|      5 | MorbidlyObeseCat | Joe              |     -0.44 |     1 |              33 |
|      6 | pollyannaw       | Fred N           |     -0.42 |     3 |              18 |
|      7 | Peter L          | Sam Mil          |     -0.34 |     4 |              36 |
|      8 | Luke G           | harryg           |     -0.32 |     4 |              38 |
|      9 | Solsti           | MorbidlyObeseCat |     -0.27 |     6 |              31 |
|     10 | Sam Mil          | Josh B           |     -0.22 |     6 |              34 |
|     11 | Josh B           | Joe              |     -0.21 |     3 |              29 |
|     12 | Fergus M         | Solsti           |     -0.19 |     6 |              31 |
|     13 | harryg           | Josh B           |     -0.17 |     6 |              34 |
|     14 | Jimbabwe         | Joshua W         |     -0.13 |     8 |              31 |

## Over Performers

_Top 10 songs ranked by how many standard deviations above the round average they scored — a 10 in a round averaging 4 outranks a 10 in a round averaging 8._

|   rank |   z_in_round |   score |   round_avg | song                      | artist         | player     | league               | round             |
|--------|--------------|---------|-------------|---------------------------|----------------|------------|----------------------|-------------------|
|      1 |         2.25 |      14 |           6 | Hurt                      | Johnny Cash    | Sam Mil    | Show me what you got | Covers            |
|      2 |         2.24 |      14 |           6 | Night On My Mind          | Sharky         | Jimbabwe   | Show me what you got | Awesome Obscurity |
|      3 |         2.24 |      15 |           4 | 19-2000 - Soulchild Remix | Gorillaz       | Sam Mit    | Jamie is a soft boy  | Best Remix        |
|      4 |         2.21 |       7 |           3 | Learn to Fly              | Foo Fighters   | Josh B     | Montage League       | Family time       |
|      5 |         2.19 |      14 |           6 | Hit the Road Jack         | Ray Charles    | Luke G     | Show me what you got | Shorties          |
|      6 |         2.12 |       6 |           3 | Fat Lip                   | Sum 41         | Josh B     | Montage League       | Pre-drinks        |
|      7 |         2.1  |       7 |           3 | Kiss and Run              | Quiet Houses   | Fergus M   | Basic League         | Verb              |
|      8 |         2.08 |      12 |           6 | Jolene                    | Dolly Parton   | Fergus M   | Show me what you got | Name Check        |
|      9 |         2.07 |      13 |           4 | Free Bird                 | Lynyrd Skynyrd | Fergus M   | Jamie is a soft boy  | From the grave    |
|     10 |         2.07 |       8 |           3 | Von dutch                 | Charli xcx     | pollyannaw | Montage League       | At the gym        |

## Under Performers

_Top 10 songs ranked by how many standard deviations below the round average they scored. The score column is still the raw points; round_avg is the mean across all songs in that round._

|   rank |   z_in_round |   score |   round_avg | song                                         | artist           | player   | league              | round                                   |
|--------|--------------|---------|-------------|----------------------------------------------|------------------|----------|---------------------|-----------------------------------------|
|      1 |        -2.82 |     -12 |        4    | Guitar Pick                                  | MEMI             | Joshua W | Jamie is a soft boy | Dirty foreigners                        |
|      2 |        -2.25 |      -4 |        2.09 | Your Heart Is a Muscle the Size of Your Fist | Ramshackle Glory | Fred N   | Basic League        | Body Part                               |
|      3 |        -2.17 |      -1 |        3    | Sheila                                       | Jamie T          | harryg   | Basic League        | Jamie’s round                           |
|      4 |        -2.12 |       0 |        3    | Cigaro                                       | System Of A Down | Sam Mil  | Montage League      | Pre-drinks                              |
|      5 |        -2.1  |     -10 |        4    | Hands Open                                   | Snow Patrol      | Luke G   | Jamie is a soft boy | Song from a video game soundtrack.      |
|      6 |        -2.09 |      -9 |        4    | Into the West                                | Annie Lennox     | Fergus M | Jamie is a soft boy | Worst (Best) songs to play at a funeral |
|      7 |        -2.04 |      -5 |        4    | 21 Seconds                                   | So Solid Crew    | Josh B   | Jamie is a soft boy | Bow Chicka Wow Wow                      |
|      8 |        -1.85 |      -5 |        4    | Angel Of Death                               | Slayer           | Luke G   | Jamie is a soft boy | Freebird!                               |
|      9 |        -1.81 |      -4 |        4    | Nutshell                                     | Alice In Chains  | Joe      | Jamie is a soft boy | You lot are fucking old                 |
|     10 |        -1.81 |      -4 |        4    | Saturday Night                               | Whigfield        | Luke G   | Jamie is a soft boy | You lot are fucking old                 |

## Most Played Artists

_Top 10 artists by number of songs submitted across all rounds._

|   rank | artist           |   plays |   total_score |   avg_score |
|--------|------------------|---------|---------------|-------------|
|      1 | The Wombats      |      12 |            25 |        2.08 |
|      2 | Green Day        |       5 |            27 |        5.4  |
|      3 | System Of A Down |       5 |            17 |        3.4  |
|      4 | Queen            |       3 |            27 |        9    |
|      5 | Gorillaz         |       3 |            26 |        8.67 |
|      6 | Fall Out Boy     |       3 |            20 |        6.67 |
|      7 | The Offspring    |       3 |            19 |        6.33 |
|      8 | Kid Kapichi      |       3 |            18 |        6    |
|      9 | Muse             |       3 |            17 |        5.67 |
|     10 | Good Charlotte   |       3 |            16 |        5.33 |

## Repeats

_Tracks (matched by Spotify track ID) submitted in more than one round, either by the same player or by different players._

|   rank |   plays | song                    | artist                       | players                      |   total_score |
|--------|---------|-------------------------|------------------------------|------------------------------|---------------|
|      1 |       2 | Snacky In My Packy      | Gabby's Dollhouse            | Fred N, harryg               |            12 |
|      2 |       2 | back to friends         | sombr                        | MorbidlyObeseCat, pollyannaw |            10 |
|      3 |       2 | Supermassive Black Hole | Muse                         | Joshua W, pollyannaw         |            10 |
|      4 |       2 | Invaders Must Die       | The Prodigy                  | Sam Mit                      |             6 |
|      5 |       2 | Turn                    | The Wombats                  | Sam Mil                      |             4 |
|      6 |       2 | Heat Waves              | Glass Animals                | Sam Mil, Solsti              |             1 |
|      7 |       2 | Get Low                 | Lil Jon & The East Side Boyz | Josh B, Solsti               |             0 |

## Forfeits

_Points lost on a player's songs when voters in that round failed to cast a ballot. Music League discards votes given by anyone who missed the voting deadline._

|   rank | player           |   songs_with_forfeit |   total_forfeit_points |
|--------|------------------|----------------------|------------------------|
|      1 | MorbidlyObeseCat |                    1 |                     -3 |
|      2 | Sam Mil          |                    2 |                     -5 |
|      3 | Fergus M         |                    2 |                     -6 |
|      4 | Josh B           |                    1 |                     -7 |

## Round Winners

_Highest-scoring song from every round, in chronological order. Ties surface as multiple rows._

| round_date                | league               | round                                   |   score | song                                                  | artist                          | player           |
|---------------------------|----------------------|-----------------------------------------|---------|-------------------------------------------------------|---------------------------------|------------------|
| 2025-09-14 20:02:18+00:00 | Show me what you got | Awesome Obscurity                       |      14 | Night On My Mind                                      | Sharky                          | Jimbabwe         |
| 2025-09-17 20:48:40+00:00 | Show me what you got | New Hotness                             |      10 | Even In Arcadia                                       | Sleep Token                     | harryg           |
| 2025-09-18 15:38:05+00:00 | Show me what you got | Movie Soundtrack                        |      12 | Danger Zone - From "Top Gun" Original Soundtrack      | Kenny Loggins                   | Fergus M         |
| 2025-09-19 17:21:51+00:00 | Show me what you got | Thanks, Mum and Dad                     |      11 | Teenage Kicks                                         | The Undertones                  | Fergus M         |
| 2025-09-20 23:39:39+00:00 | Show me what you got | Duets                                   |      17 | Under Pressure - Remastered 2011                      | Queen                           | Sam Mit          |
| 2025-09-23 18:12:56+00:00 | Show me what you got | Earworms                                |      11 | Snacky In My Packy                                    | Gabby's Dollhouse               | harryg           |
| 2025-09-26 08:27:49+00:00 | Show me what you got | Crank It Up!                            |      12 | Everytime We Touch                                    | Cascada                         | Solsti           |
| 2025-09-28 21:37:35+00:00 | Show me what you got | Name Check                              |      12 | Jolene                                                | Dolly Parton                    | Fergus M         |
| 2025-09-29 20:29:20+00:00 | Show me what you got | Covers                                  |      14 | Hurt                                                  | Johnny Cash                     | Sam Mil          |
| 2025-10-01 12:46:26+00:00 | Show me what you got | Shorties                                |      14 | Hit the Road Jack                                     | Ray Charles                     | Luke G           |
| 2025-10-10 08:15:49+00:00 | Jamie is a soft boy  | He did what?                            |      13 | Ignition - Remix                                      | R. Kelly                        | Fred N           |
| 2025-10-12 18:02:59+00:00 | Jamie is a soft boy  | Dirty foreigners                        |      13 | ZITTI E BUONI                                         | Måneskin                        | Joe              |
| 2025-10-17 10:49:19+00:00 | Jamie is a soft boy  | Deep Cuts                               |      16 | You're Crashing, But You're No Wave                   | Fall Out Boy                    | Jimbabwe         |
| 2025-10-21 11:11:21+00:00 | Jamie is a soft boy  | From the grave                          |      13 | Free Bird                                             | Lynyrd Skynyrd                  | Fergus M         |
| 2025-10-22 19:34:29+00:00 | Jamie is a soft boy  | A family affair                         |      12 | Teenagers                                             | My Chemical Romance             | Jimbabwe         |
| 2025-10-25 10:23:16+00:00 | Jamie is a soft boy  | Freebird!                               |      11 | 25 or 6 to 4 - 2002 Remaster                          | Chicago                         | Sam Mit          |
| 2025-10-28 19:17:37+00:00 | Jamie is a soft boy  | Worst (Best) songs to play at a funeral |      14 | Zombie                                                | The Cranberries                 | MorbidlyObeseCat |
| 2025-11-01 12:14:24+00:00 | Jamie is a soft boy  | Fight the Power                         |      11 | Wenceslas                                             | Gnome                           | harryg           |
| 2025-11-05 00:39:46+00:00 | Jamie is a soft boy  | You lot are fucking old                 |      11 | Kiss from a Rose                                      | Seal                            | Sam Mit          |
| 2025-11-06 18:48:01+00:00 | Jamie is a soft boy  | Bow Chicka Wow Wow                      |      10 | Theme From Shaft - Remastered 2009                    | Isaac Hayes                     | Sam Mit          |
| 2025-11-06 18:48:01+00:00 | Jamie is a soft boy  | Bow Chicka Wow Wow                      |      10 | The Loophole                                          | Garfunkel and Oates             | harryg           |
| 2025-11-11 20:41:00+00:00 | Jamie is a soft boy  | Hottest record                          |      10 | Teenage Dream                                         | Katy Perry                      | Fred N           |
| 2025-11-11 20:41:00+00:00 | Jamie is a soft boy  | Hottest record                          |      10 | SUPERMODEL                                            | Måneskin                        | Joshua W         |
| 2025-11-16 18:38:37+00:00 | Jamie is a soft boy  | Best Remix                              |      15 | 19-2000 - Soulchild Remix                             | Gorillaz                        | Sam Mit          |
| 2025-11-21 16:43:03+00:00 | Jamie is a soft boy  | Song from a video game soundtrack.      |      13 | The Rebel Path                                        | P.T. Adamczyk                   | Sam Mit          |
| 2026-01-04 16:20:34+00:00 | Montage League       | Waking up                               |       6 | Have A Nice Day                                       | Stereophonics                   | MorbidlyObeseCat |
| 2026-01-07 20:09:23+00:00 | Montage League       | At the gym                              |       8 | Von dutch                                             | Charli xcx                      | pollyannaw       |
| 2026-01-10 14:19:22+00:00 | Montage League       | At work                                 |       8 | Cold Reactor                                          | Everything Everything           | harryg           |
| 2026-01-13 16:05:51+00:00 | Montage League       | Family time                             |       7 | Learn to Fly                                          | Foo Fighters                    | Josh B           |
| 2026-01-16 20:15:26+00:00 | Montage League       | Making dinner                           |       6 | Jump in the Line                                      | Harry Belafonte                 | Joshua W         |
| 2026-01-16 20:15:26+00:00 | Montage League       | Making dinner                           |       6 | Deceptacon                                            | Le Tigre                        | Sam Mit          |
| 2026-01-20 19:32:43+00:00 | Montage League       | Pre-drinks                              |       6 | Fat Lip                                               | Sum 41                          | Josh B           |
| 2026-01-24 20:01:35+00:00 | Montage League       | In the club                             |       5 | Freed From Desire                                     | Gala                            | Peter L          |
| 2026-01-24 20:01:35+00:00 | Montage League       | In the club                             |       5 | Get Low                                               | Lil Jon & The East Side Boyz    | Solsti           |
| 2026-01-24 20:01:35+00:00 | Montage League       | In the club                             |       5 | We Are Your Friends - Justice Vs Simian               | Justice                         | pollyannaw       |
| 2026-01-27 21:15:41+00:00 | Montage League       | The morning after                       |       5 | back to friends                                       | sombr                           | pollyannaw       |
| 2026-02-04 19:35:48+00:00 | Song for the Season  | Spring                                  |       5 | Cutting My Fingers Off                                | Turnover                        | Fred N           |
| 2026-02-07 21:01:29+00:00 | Song for the Season  | Summer                                  |       6 | Hertz                                                 | Amyl and The Sniffers           | Joshua W         |
| 2026-02-07 21:01:29+00:00 | Song for the Season  | Summer                                  |       6 | Wild Flowers                                          | Frank Carter & The Rattlesnakes | harryg           |
| 2026-02-11 13:01:06+00:00 | Song for the Season  | Autumn                                  |       5 | The Boys Of Summer - Remastered 2024                  | Don Henley                      | Fred N           |
| 2026-02-11 13:01:06+00:00 | Song for the Season  | Autumn                                  |       5 | Spooky                                                | Dusty Springfield               | Joshua W         |
| 2026-02-15 12:49:40+00:00 | Song for the Season  | Winter                                  |       6 | The March of the Varangian Guard                      | Turisas                         | Fred N           |
| 2026-02-15 12:49:40+00:00 | Song for the Season  | Winter                                  |       6 | Winter 1 - 2022                                       | Max Richter                     | Sam Mit          |
| 2026-03-11 17:58:26+00:00 | Basic League         | Place                                   |       6 | Walking in Memphis                                    | Marc Cohn                       | Joe              |
| 2026-03-11 17:58:26+00:00 | Basic League         | Place                                   |       6 | Moving to New York                                    | The Wombats                     | Sam Mil          |
| 2026-03-17 00:02:31+00:00 | Basic League         | Name                                    |       6 | Andrew in Drag                                        | The Magnetic Fields             | Fred N           |
| 2026-03-21 15:02:23+00:00 | Basic League         | Animal                                  |       9 | Joker And The Thief                                   | Wolfmother                      | Fergus M         |
| 2026-03-21 15:02:23+00:00 | Basic League         | Animal                                  |       9 | Sardines                                              | Kid Kapichi                     | Joshua W         |
| 2026-03-26 08:04:11+00:00 | Basic League         | Colour                                  |       8 | (Don't Fear) The Reaper                               | Blue Öyster Cult                | Joe              |
| 2026-04-01 00:01:56+00:00 | Basic League         | Job                                     |       7 | The Artist In The Ambulance                           | Thrice                          | Joe              |
| 2026-04-06 00:02:40+00:00 | Basic League         | Body Part                               |       5 | (I Just) Died In Your Arms                            | Cutting Crew                    | Joe              |
| 2026-04-06 00:02:40+00:00 | Basic League         | Body Part                               |       5 | This Must Be the Place (Naive Melody) - 2005 Remaster | Talking Heads                   | Sam Mit          |
| 2026-04-09 18:03:06+00:00 | Basic League         | Verb                                    |       7 | Kiss and Run                                          | Quiet Houses                    | Fergus M         |
| 2026-04-14 21:48:15+00:00 | Basic League         | Jamie’s round                           |       6 | Nightswimming                                         | R.E.M.                          | Sam Mit          |

## Fan / Hater Scores

_Every (submitter, voter) pair sorted by mean z-score, descending. shared_rounds is the count of rounds where both players participated (implicit zero votes filled in for songs the voter didn't rate). Top of the table = strongest net fan signal; bottom = strongest net hater signal._

|   rank | player           | voter            |   avg_z |   total_points |   shared_rounds |
|--------|------------------|------------------|---------|----------------|-----------------|
|      1 | pollyannaw       | harryg           |    0.87 |             16 |              18 |
|      2 | harryg           | Joe              |    0.54 |             21 |              33 |
|      3 | Sam Mit          | Luke G           |    0.54 |             30 |              36 |
|      4 | Josh B           | Sam Mil          |    0.52 |             24 |              34 |
|      5 | Fergus M         | Josh B           |    0.49 |             23 |              34 |
|      6 | Joe              | harryg           |    0.45 |             20 |              33 |
|      7 | Solsti           | Sam Mil          |    0.41 |             22 |              31 |
|      8 | Luke G           | Sam Mit          |    0.38 |             20 |              36 |
|      9 | harryg           | Solsti           |    0.37 |             21 |              31 |
|     10 | Sam Mit          | Fergus M         |    0.35 |             28 |              39 |
|     11 | Sam Mit          | Fred N           |    0.35 |             31 |              41 |
|     12 | Fred N           | Jimbabwe         |    0.35 |             26 |              33 |
|     13 | pollyannaw       | Sam Mil          |    0.32 |             10 |              18 |
|     14 | Jimbabwe         | Sam Mit          |    0.31 |             22 |              33 |
|     15 | Fred N           | Luke G           |    0.3  |             20 |              38 |
|     16 | Jimbabwe         | Solsti           |    0.3  |             23 |              30 |
|     17 | Sam Mil          | MorbidlyObeseCat |    0.29 |             23 |              40 |
|     18 | harryg           | pollyannaw       |    0.28 |             14 |              18 |
|     19 | Sam Mit          | Josh B           |    0.26 |             20 |              33 |
|     20 | Joshua W         | pollyannaw       |    0.26 |              9 |              16 |
|     21 | Sam Mil          | pollyannaw       |    0.24 |              9 |              18 |
|     22 | Luke G           | Fred N           |    0.24 |             23 |              38 |
|     23 | Joshua W         | Peter L          |    0.23 |             18 |              35 |
|     24 | Sam Mit          | Jimbabwe         |    0.23 |             19 |              33 |
|     25 | Joe              | Fred N           |    0.21 |             15 |              33 |
|     26 | Fergus M         | pollyannaw       |    0.21 |             10 |              18 |
|     27 | harryg           | Fergus M         |    0.21 |             23 |              41 |
|     28 | MorbidlyObeseCat | pollyannaw       |    0.21 |              9 |              18 |
|     29 | Joe              | Solsti           |    0.21 |              7 |              21 |
|     30 | Peter L          | harryg           |    0.21 |             21 |              37 |
|     31 | Solsti           | Joshua W         |    0.2  |             17 |              29 |
|     32 | Jimbabwe         | Sam Mil          |    0.2  |             17 |              30 |
|     33 | Jimbabwe         | harryg           |    0.19 |             18 |              33 |
|     34 | Joshua W         | MorbidlyObeseCat |    0.19 |             19 |              40 |
|     35 | harryg           | Joshua W         |    0.18 |             18 |              41 |
|     36 | Peter L          | Joshua W         |    0.18 |             18 |              35 |
|     37 | Fred N           | Solsti           |    0.18 |             16 |              31 |
|     38 | Joshua W         | Joe              |    0.17 |             14 |              33 |
|     39 | Fred N           | Peter L          |    0.17 |             20 |              37 |
|     40 | Fergus M         | Jimbabwe         |    0.17 |             17 |              33 |
|     41 | Peter L          | Josh B           |    0.16 |             17 |              32 |
|     42 | MorbidlyObeseCat | Jimbabwe         |    0.16 |             16 |              33 |
|     43 | Fred N           | Joe              |    0.16 |             15 |              33 |
|     44 | Luke G           | Josh B           |    0.15 |             14 |              33 |
|     45 | Fergus M         | Sam Mil          |    0.14 |             16 |              38 |
|     46 | Jimbabwe         | pollyannaw       |    0.14 |              8 |              17 |
|     47 | Jimbabwe         | Peter L          |    0.12 |             15 |              29 |
|     48 | Sam Mil          | Solsti           |    0.11 |             15 |              31 |
|     49 | Josh B           | pollyannaw       |    0.11 |              6 |              14 |
|     50 | harryg           | Jimbabwe         |    0.11 |             16 |              33 |
|     51 | Fergus M         | MorbidlyObeseCat |    0.1  |             17 |              42 |
|     52 | Fred N           | Fergus M         |    0.1  |             14 |              41 |
|     53 | Sam Mit          | MorbidlyObeseCat |    0.09 |             16 |              40 |
|     54 | Sam Mit          | harryg           |    0.08 |             20 |              41 |
|     55 | Fergus M         | Joe              |    0.08 |             10 |              33 |
|     56 | pollyannaw       | Fergus M         |    0.08 |              7 |              17 |
|     57 | Fergus M         | Joshua W         |    0.07 |             16 |              41 |
|     58 | Joe              | Peter L          |    0.07 |             11 |              27 |
|     59 | Josh B           | harryg           |    0.07 |             12 |              35 |
|     60 | Josh B           | Joshua W         |    0.06 |             10 |              35 |
|     61 | harryg           | MorbidlyObeseCat |    0.06 |             18 |              42 |
|     62 | Jimbabwe         | MorbidlyObeseCat |    0.05 |             18 |              33 |
|     63 | Luke G           | Solsti           |    0.05 |             11 |              26 |
|     64 | pollyannaw       | Jimbabwe         |    0.05 |              8 |              17 |
|     65 | MorbidlyObeseCat | Sam Mil          |    0.04 |             14 |              38 |
|     66 | Sam Mit          | Joshua W         |    0.04 |             13 |              39 |
|     67 | Josh B           | Jimbabwe         |    0.04 |              9 |              26 |
|     68 | Fergus M         | Peter L          |    0.04 |             13 |              37 |
|     69 | MorbidlyObeseCat | Peter L          |    0.04 |             16 |              37 |
|     70 | Josh B           | Luke G           |    0.04 |              9 |              34 |
|     71 | Josh B           | Peter L          |    0.04 |             10 |              33 |
|     72 | Josh B           | Fred N           |    0.04 |              9 |              35 |
|     73 | pollyannaw       | Joe              |    0.03 |              2 |               8 |
|     74 | Fred N           | Sam Mit          |    0.02 |             19 |              41 |
|     75 | Solsti           | Joe              |    0.02 |              5 |              21 |
|     76 | Joe              | Fergus M         |    0.02 |             11 |              31 |
|     77 | Luke G           | pollyannaw       |    0.02 |              4 |              13 |
|     78 | Josh B           | Sam Mit          |    0.02 |             13 |              34 |
|     79 | Josh B           | Fergus M         |    0.01 |             11 |              33 |
|     80 | Joshua W         | Sam Mit          |    0.01 |             12 |              39 |
|     81 | Luke G           | Joe              |    0.01 |             11 |              33 |
|     82 | Fergus M         | Sam Mit          |    0.01 |             15 |              41 |
|     83 | MorbidlyObeseCat | Josh B           |    0.01 |             12 |              34 |
|     84 | pollyannaw       | MorbidlyObeseCat |    0.01 |              7 |              18 |
|     85 | Josh B           | Solsti           |    0.01 |              9 |              27 |
|     86 | harryg           | Fred N           |   -0    |             17 |              43 |
|     87 | Sam Mit          | Solsti           |   -0    |             12 |              31 |
|     88 | Jimbabwe         | Luke G           |    0    |             11 |              28 |
|     89 | Joshua W         | Fred N           |    0    |             13 |              41 |
|     90 | pollyannaw       | Sam Mit          |   -0.01 |              7 |              18 |
|     91 | Peter L          | Fergus M         |   -0.01 |             15 |              35 |
|     92 | Solsti           | Josh B           |   -0.01 |              8 |              27 |
|     93 | Josh B           | MorbidlyObeseCat |   -0.01 |             13 |              34 |
|     94 | Solsti           | Fergus M         |   -0.02 |             11 |              30 |
|     95 | Peter L          | Sam Mit          |   -0.02 |             15 |              36 |
|     96 | Sam Mit          | Sam Mil          |   -0.02 |             14 |              37 |
|     97 | Fred N           | Sam Mil          |   -0.02 |             15 |              38 |
|     98 | Sam Mit          | Joe              |   -0.03 |             11 |              31 |
|     99 | MorbidlyObeseCat | Luke G           |   -0.03 |             14 |              38 |
|    100 | Joshua W         | harryg           |   -0.04 |             14 |              41 |
|    101 | Sam Mil          | Fred N           |   -0.04 |             14 |              41 |
|    102 | Luke G           | Fergus M         |   -0.04 |              7 |              36 |
|    103 | harryg           | Sam Mit          |   -0.05 |             16 |              41 |
|    104 | Fergus M         | Luke G           |   -0.05 |             12 |              38 |
|    105 | Peter L          | Fred N           |   -0.05 |             11 |              37 |
|    106 | pollyannaw       | Peter L          |   -0.06 |              7 |              17 |
|    107 | Jimbabwe         | Fred N           |   -0.06 |             10 |              33 |
|    108 | Sam Mil          | Luke G           |   -0.06 |              9 |              36 |
|    109 | Sam Mil          | Joshua W         |   -0.07 |             12 |              39 |
|    110 | Jimbabwe         | Fergus M         |   -0.07 |             13 |              33 |
|    111 | Joe              | Luke G           |   -0.07 |              8 |              33 |
|    112 | Fred N           | Joshua W         |   -0.07 |             14 |              41 |
|    113 | Fred N           | Josh B           |   -0.07 |             11 |              34 |
|    114 | MorbidlyObeseCat | Fred N           |   -0.08 |             10 |              43 |
|    115 | Joe              | Joshua W         |   -0.08 |             10 |              33 |
|    116 | Jimbabwe         | Joe              |   -0.08 |              8 |              23 |
|    117 | MorbidlyObeseCat | Sam Mit          |   -0.08 |             12 |              41 |
|    118 | Luke G           | Peter L          |   -0.08 |              7 |              32 |
|    119 | Joe              | MorbidlyObeseCat |   -0.09 |             10 |              32 |
|    120 | Sam Mit          | Peter L          |   -0.1  |             10 |              36 |
|    121 | Peter L          | pollyannaw       |   -0.1  |              6 |              17 |
|    122 | harryg           | Luke G           |   -0.11 |              7 |              38 |
|    123 | Jimbabwe         | Josh B           |   -0.11 |              8 |              26 |
|    124 | MorbidlyObeseCat | Fergus M         |   -0.11 |             12 |              41 |
|    125 | Luke G           | Joshua W         |   -0.11 |              7 |              38 |
|    126 | Peter L          | MorbidlyObeseCat |   -0.11 |              8 |              36 |
|    127 | Joshua W         | Jimbabwe         |   -0.12 |              9 |              31 |
|    128 | MorbidlyObeseCat | Joshua W         |   -0.12 |             14 |              41 |
|    129 | Fergus M         | harryg           |   -0.13 |             10 |              43 |
|    130 | Jimbabwe         | Joshua W         |   -0.13 |              8 |              31 |
|    131 | Sam Mil          | Joe              |   -0.13 |              7 |              31 |
|    132 | Luke G           | Sam Mil          |   -0.13 |             10 |              33 |
|    133 | Joshua W         | Luke G           |   -0.14 |              8 |              38 |
|    134 | pollyannaw       | Solsti           |   -0.14 |              5 |              18 |
|    135 | Fred N           | MorbidlyObeseCat |   -0.15 |              9 |              42 |
|    136 | harryg           | Sam Mil          |   -0.16 |              8 |              38 |
|    137 | harryg           | Peter L          |   -0.16 |              9 |              37 |
|    138 | Solsti           | Peter L          |   -0.16 |              7 |              30 |
|    139 | pollyannaw       | Josh B           |   -0.16 |              4 |              14 |
|    140 | Solsti           | pollyannaw       |   -0.16 |              5 |              18 |
|    141 | Sam Mil          | Peter L          |   -0.17 |             10 |              37 |
|    142 | Sam Mil          | harryg           |   -0.17 |              6 |              41 |
|    143 | harryg           | Josh B           |   -0.17 |              6 |              34 |
|    144 | MorbidlyObeseCat | harryg           |   -0.18 |             11 |              43 |
|    145 | Solsti           | Luke G           |   -0.18 |              4 |              26 |
|    146 | Sam Mil          | Jimbabwe         |   -0.18 |              7 |              32 |
|    147 | Joe              | Sam Mit          |   -0.18 |              6 |              31 |
|    148 | Fergus M         | Fred N           |   -0.18 |              9 |              43 |
|    149 | Fergus M         | Solsti           |   -0.19 |              6 |              31 |
|    150 | Solsti           | Jimbabwe         |   -0.19 |              6 |              30 |
|    151 | Sam Mil          | Sam Mit          |   -0.19 |              6 |              40 |
|    152 | Fred N           | harryg           |   -0.2  |             12 |              43 |
|    153 | Peter L          | Joe              |   -0.2  |              4 |              27 |
|    154 | Peter L          | Luke G           |   -0.2  |              7 |              32 |
|    155 | Josh B           | Joe              |   -0.21 |              3 |              29 |
|    156 | Joe              | Josh B           |   -0.21 |              3 |              28 |
|    157 | Sam Mil          | Fergus M         |   -0.21 |              9 |              39 |
|    158 | Sam Mil          | Josh B           |   -0.22 |              6 |              34 |
|    159 | Peter L          | Solsti           |   -0.22 |              7 |              30 |
|    160 | Luke G           | Jimbabwe         |   -0.23 |              3 |              28 |
|    161 | Solsti           | harryg           |   -0.23 |              7 |              31 |
|    162 | Joshua W         | Josh B           |   -0.25 |              0 |              34 |
|    163 | Solsti           | Sam Mit          |   -0.25 |              3 |              31 |
|    164 | Solsti           | Fred N           |   -0.25 |              5 |              31 |
|    165 | MorbidlyObeseCat | Solsti           |   -0.26 |              4 |              31 |
|    166 | Luke G           | MorbidlyObeseCat |   -0.26 |              5 |              37 |
|    167 | Peter L          | Jimbabwe         |   -0.27 |              4 |              29 |
|    168 | Joe              | Jimbabwe         |   -0.27 |              2 |              23 |
|    169 | pollyannaw       | Joshua W         |   -0.27 |              4 |              16 |
|    170 | Solsti           | MorbidlyObeseCat |   -0.27 |              6 |              31 |
|    171 | Joe              | Sam Mil          |   -0.28 |              2 |              28 |
|    172 | Joshua W         | Fergus M         |   -0.3  |              4 |              39 |
|    173 | pollyannaw       | Luke G           |   -0.3  |              2 |              13 |
|    174 | Luke G           | harryg           |   -0.32 |              4 |              38 |
|    175 | Peter L          | Sam Mil          |   -0.34 |              4 |              36 |
|    176 | pollyannaw       | Fred N           |   -0.42 |              3 |              18 |
|    177 | Joshua W         | Solsti           |   -0.43 |              0 |              29 |
|    178 | MorbidlyObeseCat | Joe              |   -0.44 |              1 |              33 |
|    179 | Fred N           | pollyannaw       |   -0.46 |              2 |              18 |
|    180 | Sam Mit          | pollyannaw       |   -0.47 |              2 |              18 |
|    181 | Joshua W         | Sam Mil          |   -0.47 |              0 |              36 |
|    182 | Joe              | pollyannaw       |   -0.52 |              0 |               8 |
