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

## Biggest Fans/Haters

_For each submitter, the voter whose votes land highest (fan) and lowest (hater) relative to that voter's own per-round vote distribution. Metric: mean z-score across shared rounds, where z = (vote - voter_round_mean) / voter_round_std. Pairs are required to share at least 10 rounds so a single outlier vote can't crown a fan/hater. Rounds where the voter gave every song the same vote are dropped (z is undefined). fan_pts / hater_pts are the raw cumulative points for context. See the 'Biggest Fans/Haters (everyone)' table at the end of the report for the unfiltered pair-by-pair view._

|   rank | player           | biggest_fan      |   fan_z |   fan_pts |   shared_rounds | biggest_hater    |   hater_z |   hater_pts |
|--------|------------------|------------------|---------|-----------|-----------------|------------------|-----------|-------------|
|      1 | Fred N           | Jimbabwe         |    0.78 |        21 |              11 | Fergus M         |     -0.45 |           5 |
|      2 | Sam Mit          | Fergus M         |    0.74 |        23 |              16 | Peter L          |     -0.32 |           6 |
|      3 | Jimbabwe         | Sam Mit          |    0.72 |        18 |              11 | Josh B           |     -0.18 |           7 |
|      4 | Peter L          | Josh B           |    0.65 |        16 |              12 | MorbidlyObeseCat |     -0.43 |           5 |
|      5 | Solsti           | Sam Mil          |    0.45 |        18 |              14 | Fred N           |     -0.66 |           2 |
|      6 | Fergus M         | Sam Mit          |    0.42 |        12 |              11 | Solsti           |     -0.27 |           4 |
|      7 | harryg           | Fred N           |    0.41 |        14 |              12 | Luke G           |     -0.37 |           2 |
|      8 | Josh B           | Sam Mil          |    0.39 |        20 |              19 | Joshua W         |     -0.54 |           5 |
|      9 | Joe              | Peter L          |    0.32 |        11 |              13 | Sam Mil          |     -0.39 |           1 |
|     10 | Sam Mil          | MorbidlyObeseCat |    0.29 |        19 |              18 | harryg           |     -0.47 |           2 |
|     11 | Luke G           | Fred N           |    0.25 |        20 |              16 | Joshua W         |     -0.5  |           4 |
|     12 | MorbidlyObeseCat | Peter L          |    0.24 |        12 |              15 | Joe              |     -0.41 |           1 |
|     13 | Joshua W         | MorbidlyObeseCat |    0.16 |        16 |              16 | Sam Mil          |     -0.69 |          -1 |

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
|     10 | Eminem           |       3 |            16 |        5.33 |

## Repeats

_Tracks (matched by Spotify track ID) submitted in more than one round, either by the same player or by different players._

|   rank |   plays | song                    | artist                       | players                      |   total_score |
|--------|---------|-------------------------|------------------------------|------------------------------|---------------|
|      1 |       2 | Snacky In My Packy      | Gabby's Dollhouse            | Fred N, harryg               |            12 |
|      2 |       2 | Supermassive Black Hole | Muse                         | Joshua W, pollyannaw         |            10 |
|      3 |       2 | back to friends         | sombr                        | MorbidlyObeseCat, pollyannaw |            10 |
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

## Biggest Fans/Haters (everyone)

_Every (submitter, voter) pair sorted by mean z-score, descending. No minimum-shared-rounds filter — pairs with shared_rounds=1 or 2 will have wildly variable z-scores, so use shared_rounds as your confidence guide. Top of the table = strongest net fan signal; bottom = strongest net hater signal._

|   rank | player           | voter            |   avg_z |   total_points |   shared_rounds |
|--------|------------------|------------------|---------|----------------|-----------------|
|      1 | Fred N           | pollyannaw       |    2    |              2 |               1 |
|      2 | Joshua W         | pollyannaw       |    1.41 |              7 |               3 |
|      3 | Luke G           | pollyannaw       |    1    |              2 |               1 |
|      4 | Fred N           | Jimbabwe         |    0.78 |             21 |              11 |
|      5 | Sam Mit          | Fergus M         |    0.74 |             23 |              16 |
|      6 | Jimbabwe         | Sam Mit          |    0.72 |             18 |              11 |
|      7 | Peter L          | Josh B           |    0.65 |             16 |              12 |
|      8 | Peter L          | Joshua W         |    0.64 |             16 |              11 |
|      9 | Jimbabwe         | harryg           |    0.64 |             14 |              10 |
|     10 | Sam Mit          | Luke G           |    0.64 |             26 |              16 |
|     11 | Josh B           | pollyannaw       |    0.5  |              4 |               2 |
|     12 | Jimbabwe         | Peter L          |    0.48 |             11 |              10 |
|     13 | Solsti           | Sam Mil          |    0.45 |             18 |              14 |
|     14 | Josh B           | MorbidlyObeseCat |    0.44 |             12 |               9 |
|     15 | Jimbabwe         | Sam Mil          |    0.42 |             14 |              12 |
|     16 | Fergus M         | Sam Mit          |    0.42 |             12 |              11 |
|     17 | harryg           | Fred N           |    0.41 |             14 |              12 |
|     18 | Josh B           | Sam Mil          |    0.39 |             20 |              19 |
|     19 | Sam Mit          | Fred N           |    0.39 |             21 |              17 |
|     20 | Jimbabwe         | MorbidlyObeseCat |    0.38 |             17 |              13 |
|     21 | Fred N           | Joe              |    0.37 |             11 |              12 |
|     22 | harryg           | Solsti           |    0.37 |             17 |              14 |
|     23 | harryg           | Joe              |    0.36 |             12 |              13 |
|     24 | pollyannaw       | Sam Mil          |    0.33 |              4 |               3 |
|     25 | Joe              | Peter L          |    0.32 |             11 |              13 |
|     26 | Sam Mit          | Josh B           |    0.31 |             17 |              15 |
|     27 | Josh B           | Sam Mit          |    0.31 |             12 |              12 |
|     28 | Fred N           | Peter L          |    0.3  |             15 |              15 |
|     29 | Peter L          | harryg           |    0.3  |             19 |              18 |
|     30 | Sam Mit          | Joe              |    0.3  |             10 |              11 |
|     31 | Sam Mil          | MorbidlyObeseCat |    0.29 |             19 |              18 |
|     32 | Jimbabwe         | Solsti           |    0.27 |             14 |              13 |
|     33 | Sam Mit          | harryg           |    0.27 |             14 |              15 |
|     34 | Josh B           | Jimbabwe         |    0.27 |              6 |               7 |
|     35 | harryg           | Joshua W         |    0.27 |             15 |              14 |
|     36 | Solsti           | Joshua W         |    0.26 |             14 |              12 |
|     37 | pollyannaw       | Solsti           |    0.25 |              3 |               2 |
|     38 | Luke G           | Fred N           |    0.25 |             20 |              16 |
|     39 | Fergus M         | pollyannaw       |    0.25 |              9 |               6 |
|     40 | Joe              | Fred N           |    0.25 |             12 |              13 |
|     41 | pollyannaw       | Joshua W         |    0.25 |              4 |               2 |
|     42 | MorbidlyObeseCat | Peter L          |    0.24 |             12 |              15 |
|     43 | harryg           | Sam Mit          |    0.24 |             15 |              13 |
|     44 | MorbidlyObeseCat | Fergus M         |    0.23 |              8 |              10 |
|     45 | Sam Mit          | Solsti           |    0.21 |             10 |              11 |
|     46 | Luke G           | Solsti           |    0.21 |             10 |              13 |
|     47 | Jimbabwe         | Joe              |    0.2  |              8 |              12 |
|     48 | Joe              | harryg           |    0.2  |             15 |              18 |
|     49 | Peter L          | Fred N           |    0.19 |              7 |               9 |
|     50 | harryg           | Jimbabwe         |    0.19 |             11 |              11 |
|     51 | Sam Mit          | Jimbabwe         |    0.19 |             14 |              13 |
|     52 | Jimbabwe         | Luke G           |    0.19 |              9 |              10 |
|     53 | MorbidlyObeseCat | Sam Mil          |    0.18 |             10 |              15 |
|     54 | Joe              | Luke G           |    0.17 |              7 |               9 |
|     55 | harryg           | Fergus M         |    0.16 |             17 |              17 |
|     56 | Joe              | Fergus M         |    0.16 |             10 |              14 |
|     57 | Joe              | Sam Mit          |    0.16 |              5 |               8 |
|     58 | Fergus M         | Josh B           |    0.16 |             19 |              19 |
|     59 | Joshua W         | MorbidlyObeseCat |    0.16 |             16 |              16 |
|     60 | Luke G           | Joe              |    0.15 |              8 |              13 |
|     61 | Fred N           | Joshua W         |    0.14 |             13 |              14 |
|     62 | Sam Mil          | Fergus M         |    0.14 |              6 |               8 |
|     63 | Fred N           | Luke G           |    0.14 |             16 |              18 |
|     64 | Joe              | MorbidlyObeseCat |    0.13 |             10 |              14 |
|     65 | Joshua W         | Peter L          |    0.12 |             13 |              18 |
|     66 | Sam Mil          | Joshua W         |    0.11 |             11 |              12 |
|     67 | MorbidlyObeseCat | Luke G           |    0.11 |             14 |              14 |
|     68 | Sam Mit          | Joshua W         |    0.09 |             10 |              13 |
|     69 | Joshua W         | harryg           |    0.09 |             13 |              15 |
|     70 | Sam Mil          | Peter L          |    0.09 |              7 |              13 |
|     71 | Solsti           | Fergus M         |    0.08 |              7 |               9 |
|     72 | Fred N           | Sam Mil          |    0.07 |             13 |              17 |
|     73 | Luke G           | Sam Mit          |    0.06 |             13 |              16 |
|     74 | Josh B           | harryg           |    0.06 |              9 |              13 |
|     75 | Josh B           | Luke G           |    0.05 |              6 |              13 |
|     76 | MorbidlyObeseCat | harryg           |    0.05 |              7 |              12 |
|     77 | harryg           | MorbidlyObeseCat |    0.04 |             16 |              17 |
|     78 | Fred N           | Josh B           |    0.04 |             10 |              12 |
|     79 | Joe              | Josh B           |    0.04 |              3 |               5 |
|     80 | Joshua W         | Joe              |    0.04 |              8 |              13 |
|     81 | harryg           | Josh B           |    0.03 |              4 |               7 |
|     82 | Joe              | Solsti           |    0.02 |              3 |               7 |
|     83 | Fergus M         | MorbidlyObeseCat |    0.02 |             13 |              18 |
|     84 | Fergus M         | Joe              |    0.02 |              5 |              10 |
|     85 | MorbidlyObeseCat | Josh B           |    0.02 |              9 |              11 |
|     86 | Fergus M         | Jimbabwe         |    0.01 |             12 |              16 |
|     87 | MorbidlyObeseCat | Joshua W         |    0.01 |             13 |              14 |
|     88 | pollyannaw       | Sam Mit          |    0    |              4 |               2 |
|     89 | MorbidlyObeseCat | pollyannaw       |    0    |              7 |               5 |
|     90 | Fergus M         | Sam Mil          |   -0    |             11 |              18 |
|     91 | pollyannaw       | MorbidlyObeseCat |   -0.03 |              4 |               3 |
|     92 | Joe              | Joshua W         |   -0.03 |              8 |              12 |
|     93 | Sam Mil          | Fred N           |   -0.04 |             10 |              15 |
|     94 | Peter L          | Sam Mit          |   -0.04 |             13 |              16 |
|     95 | Peter L          | Fergus M         |   -0.04 |             11 |              14 |
|     96 | Joshua W         | Jimbabwe         |   -0.05 |              7 |              10 |
|     97 | Fergus M         | Joshua W         |   -0.06 |             13 |              15 |
|     98 | Fergus M         | Luke G           |   -0.06 |              9 |              16 |
|     99 | Fred N           | Solsti           |   -0.07 |             14 |              16 |
|    100 | Jimbabwe         | Fred N           |   -0.08 |              6 |              10 |
|    101 | Jimbabwe         | Fergus M         |   -0.08 |             10 |              14 |
|    102 | Sam Mit          | Sam Mil          |   -0.09 |             10 |              13 |
|    103 | Luke G           | Josh B           |   -0.09 |             10 |              15 |
|    104 | Solsti           | harryg           |   -0.09 |              6 |              12 |
|    105 | harryg           | Peter L          |   -0.1  |              6 |              14 |
|    106 | MorbidlyObeseCat | Jimbabwe         |   -0.1  |             10 |              13 |
|    107 | Solsti           | pollyannaw       |   -0.11 |              3 |               2 |
|    108 | Josh B           | Solsti           |   -0.11 |              6 |               8 |
|    109 | Joshua W         | Sam Mit          |   -0.12 |              8 |              14 |
|    110 | Luke G           | Sam Mil          |   -0.12 |              9 |              15 |
|    111 | Fergus M         | Peter L          |   -0.13 |              8 |              17 |
|    112 | Fergus M         | harryg           |   -0.13 |              7 |              15 |
|    113 | Fred N           | harryg           |   -0.13 |             11 |              15 |
|    114 | Solsti           | Jimbabwe         |   -0.14 |              5 |              10 |
|    115 | Sam Mit          | MorbidlyObeseCat |   -0.15 |             13 |              18 |
|    116 | MorbidlyObeseCat | Fred N           |   -0.15 |              4 |              11 |
|    117 | Josh B           | Peter L          |   -0.15 |              6 |              15 |
|    118 | Sam Mil          | Luke G           |   -0.16 |              6 |              11 |
|    119 | Solsti           | Josh B           |   -0.17 |              5 |               9 |
|    120 | Sam Mil          | Solsti           |   -0.17 |             12 |              13 |
|    121 | Peter L          | Solsti           |   -0.17 |              6 |               8 |
|    122 | Joshua W         | Luke G           |   -0.18 |              5 |              11 |
|    123 | Sam Mil          | Joe              |   -0.18 |              4 |              10 |
|    124 | Jimbabwe         | Josh B           |   -0.18 |              7 |              11 |
|    125 | Sam Mil          | Josh B           |   -0.18 |              6 |              17 |
|    126 | Solsti           | MorbidlyObeseCat |   -0.19 |              4 |               7 |
|    127 | Josh B           | Fergus M         |   -0.19 |              9 |              15 |
|    128 | Fergus M         | Fred N           |   -0.21 |              5 |              12 |
|    129 | Solsti           | Joe              |   -0.23 |              2 |               9 |
|    130 | Sam Mil          | Jimbabwe         |   -0.23 |              6 |              13 |
|    131 | MorbidlyObeseCat | Sam Mit          |   -0.23 |              8 |              13 |
|    132 | Luke G           | Jimbabwe         |   -0.24 |              2 |               7 |
|    133 | Solsti           | Luke G           |   -0.25 |              3 |              10 |
|    134 | Joshua W         | Fred N           |   -0.25 |              7 |              10 |
|    135 | Peter L          | Joe              |   -0.26 |              3 |              12 |
|    136 | Luke G           | Peter L          |   -0.26 |              2 |              10 |
|    137 | Fergus M         | Solsti           |   -0.27 |              4 |              11 |
|    138 | pollyannaw       | harryg           |   -0.28 |             10 |               9 |
|    139 | Joe              | Jimbabwe         |   -0.29 |              2 |              11 |
|    140 | Jimbabwe         | Joshua W         |   -0.29 |              5 |               9 |
|    141 | Jimbabwe         | pollyannaw       |   -0.3  |              6 |               5 |
|    142 | MorbidlyObeseCat | Solsti           |   -0.31 |              2 |               6 |
|    143 | Sam Mit          | Peter L          |   -0.32 |              6 |              14 |
|    144 | Luke G           | Fergus M         |   -0.32 |              2 |              15 |
|    145 | Fred N           | Sam Mit          |   -0.32 |              9 |              15 |
|    146 | Peter L          | Jimbabwe         |   -0.33 |              3 |              11 |
|    147 | harryg           | Sam Mil          |   -0.34 |              4 |              13 |
|    148 | Fred N           | MorbidlyObeseCat |   -0.35 |              6 |              13 |
|    149 | Peter L          | Luke G           |   -0.36 |              7 |              15 |
|    150 | harryg           | Luke G           |   -0.37 |              2 |              14 |
|    151 | Peter L          | pollyannaw       |   -0.38 |              5 |               4 |
|    152 | Sam Mil          | Sam Mit          |   -0.38 |              3 |              17 |
|    153 | Joe              | Sam Mil          |   -0.39 |              1 |              12 |
|    154 | Sam Mil          | pollyannaw       |   -0.4  |              6 |               5 |
|    155 | Joshua W         | Fergus M         |   -0.4  |              1 |              11 |
|    156 | Josh B           | Fred N           |   -0.41 |              3 |              10 |
|    157 | MorbidlyObeseCat | Joe              |   -0.41 |              1 |              10 |
|    158 | Luke G           | MorbidlyObeseCat |   -0.41 |              4 |              14 |
|    159 | Solsti           | Peter L          |   -0.41 |              2 |              11 |
|    160 | Luke G           | harryg           |   -0.42 |              2 |              15 |
|    161 | Solsti           | Sam Mit          |   -0.43 |              0 |              12 |
|    162 | Peter L          | MorbidlyObeseCat |   -0.43 |              5 |              13 |
|    163 | Fred N           | Fergus M         |   -0.45 |              5 |              14 |
|    164 | Sam Mil          | harryg           |   -0.47 |              2 |              18 |
|    165 | Joshua W         | Solsti           |   -0.49 |             -1 |               8 |
|    166 | Luke G           | Joshua W         |   -0.5  |              4 |              15 |
|    167 | harryg           | pollyannaw       |   -0.5  |              7 |               6 |
|    168 | pollyannaw       | Jimbabwe         |   -0.5  |              1 |               1 |
|    169 | pollyannaw       | Luke G           |   -0.5  |              1 |               1 |
|    170 | pollyannaw       | Fred N           |   -0.5  |              2 |               2 |
|    171 | Josh B           | Joe              |   -0.53 |              0 |              12 |
|    172 | Peter L          | Sam Mil          |   -0.53 |              1 |               6 |
|    173 | pollyannaw       | Fergus M         |   -0.54 |              2 |               2 |
|    174 | Josh B           | Joshua W         |   -0.54 |              5 |              14 |
|    175 | Solsti           | Fred N           |   -0.66 |              2 |              11 |
|    176 | Joshua W         | Sam Mil          |   -0.69 |             -1 |              12 |
|    177 | Sam Mit          | pollyannaw       |   -0.75 |              2 |               2 |
|    178 | Joshua W         | Josh B           |   -0.79 |             -4 |               8 |
|    179 | pollyannaw       | Josh B           |   -0.79 |              3 |               3 |
|    180 | pollyannaw       | Peter L          |   -1    |              3 |               3 |
