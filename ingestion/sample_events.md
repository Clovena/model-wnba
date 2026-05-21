# Events Sample Output

## Notes and Takeaways

At the highest level, the following is available:
* `id` (on ESPN's platform)
* `date` with timestamp
* `name` - spelled out Team A vs Team B
* `shortName` - abbreviated TMA @ TMB

`season` json includes:
* four-digit `year`
* `type` - 1 for preseason, TBD
* `slug` string corresponding to `type`

`competitions` array includes:
* `attendance`
* `timeValid`
* `neutralSite`
* `conferenceCompetition`
* `playByPlayAvailable`
* `recent`
* `venue` json
  * `venue.id` and `venue.name`
  * `venue.address` json incl. `city` and `state`
  * `venue.indoor` bool
* `competitors` array - team metadata for both sides `0` and `1`
  * `competitors.score`, critically
  * per-period `linescores` - periods `0,1,2,3`
  * team-level `statistics` array
  * team leaders for points, rebounds, assists, rating
    * player metadata
  * records per team *before* the game in focus
* `notes` array - provided by ESPN
* `status` json for live-time metadata
* `broadcasts[], geoBroadcasts[], format{}`
* `highlights` array

`links` array includes links for Gamecast, Box Score, and Play-by-Play

root-level `status{}` similar to `competitions.status{}`

## Raw JSON

```json
{
  "id": "401765028",
  "uid": "s:40~l:59~e:401765028",
  "date": "2025-05-09T23:00Z",
  "name": "Connecticut Sun at New York Liberty",
  "shortName": "CON @ NY",
  "season": {
    "year": 2025,
    "type": 1,
    "slug": "preseason"
  },
  "competitions": [
    {
      "id": "401765028",
      "uid": "s:40~l:59~e:401765028~c:401765028",
      "date": "2025-05-09T23:00Z",
      "attendance": 8395,
      "type": {
        "id": "1",
        "abbreviation": "STD"
      },
      "timeValid": true,
      "neutralSite": false,
      "conferenceCompetition": false,
      "playByPlayAvailable": true,
      "recent": false,
      "venue": {
        "id": "3559",
        "fullName": "Barclays Center",
        "address": {
          "city": "Brooklyn",
          "state": "NY"
        },
        "indoor": true
      },
      "competitors": [
        {
          "id": "9",
          "uid": "s:40~l:59~t:9",
          "type": "team",
          "order": 0,
          "homeAway": "home",
          "winner": false,
          "team": {
            "id": "9",
            "uid": "s:40~l:59~t:9",
            "location": "New York",
            "name": "Liberty",
            "abbreviation": "NY",
            "displayName": "New York Liberty",
            "shortDisplayName": "Liberty",
            "color": "86cebc",
            "alternateColor": "000000",
            "isActive": true,
            "venue": {
              "id": "3559"
            },
            "links": [
              {
                "rel": [
                  "clubhouse",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/_/name/ny/new-york-liberty",
                "text": "Clubhouse",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "clubhouse",
                  "mobile",
                  "team"
                ],
                "href": "https://m.espn.com/wnba/clubhouse?teamId=9",
                "text": "Clubhouse",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "roster",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/roster/_/name/ny/new-york-liberty",
                "text": "Roster",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "stats",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/stats/_/name/ny/new-york-liberty",
                "text": "Statistics",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "schedule",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/schedule/_/name/ny",
                "text": "Schedule",
                "isExternal": false,
                "isPremium": false
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/wnba/500/ny.png"
          },
          "score": "86",
          "linescores": [
            {
              "value": 27.0,
              "displayValue": "27",
              "period": 1
            },
            {
              "value": 23.0,
              "displayValue": "23",
              "period": 2
            },
            {
              "value": 18.0,
              "displayValue": "18",
              "period": 3
            },
            {
              "value": 18.0,
              "displayValue": "18",
              "period": 4
            }
          ],
          "statistics": [
            {
              "name": "rebounds",
              "abbreviation": "REB",
              "displayValue": "23"
            },
            {
              "name": "avgRebounds",
              "abbreviation": "REB",
              "displayValue": "0.0"
            },
            {
              "name": "assists",
              "abbreviation": "AST",
              "displayValue": "24"
            },
            {
              "name": "fieldGoalsAttempted",
              "abbreviation": "FGA",
              "displayValue": "58"
            },
            {
              "name": "fieldGoalsMade",
              "abbreviation": "FGM",
              "displayValue": "33"
            },
            {
              "name": "fieldGoalPct",
              "abbreviation": "FG%",
              "displayValue": "56.9"
            },
            {
              "name": "freeThrowPct",
              "abbreviation": "FT%",
              "displayValue": "60.0"
            },
            {
              "name": "freeThrowsAttempted",
              "abbreviation": "FTA",
              "displayValue": "15"
            },
            {
              "name": "freeThrowsMade",
              "abbreviation": "FTM",
              "displayValue": "9"
            },
            {
              "name": "points",
              "abbreviation": "PTS",
              "displayValue": "86"
            },
            {
              "name": "threePointPct",
              "abbreviation": "3P%",
              "displayValue": "47.8"
            },
            {
              "name": "threePointFieldGoalsAttempted",
              "abbreviation": "3PA",
              "displayValue": "23"
            },
            {
              "name": "threePointFieldGoalsMade",
              "abbreviation": "3PM",
              "displayValue": "11"
            },
            {
              "name": "avgPoints",
              "abbreviation": "PTS",
              "displayValue": "0.0"
            },
            {
              "name": "avgAssists",
              "abbreviation": "AST",
              "displayValue": "0.0"
            },
            {
              "name": "threePointFieldGoalPct",
              "abbreviation": "3P%",
              "displayValue": "47.8"
            }
          ],
          "leaders": [
            {
              "name": "points",
              "displayName": "Points",
              "shortDisplayName": "Pts",
              "abbreviation": "Pts",
              "leaders": [
                {
                  "displayValue": "12",
                  "value": 12.0,
                  "athlete": {
                    "id": "4038379",
                    "fullName": "Marine Johannes",
                    "displayName": "Marine Johannes",
                    "shortName": "M. Johannes",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/4038379/marine-johannes"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/4038379.png",
                    "jersey": "23",
                    "position": {
                      "abbreviation": "G"
                    },
                    "team": {
                      "id": "9"
                    },
                    "active": true
                  },
                  "team": {
                    "id": "9"
                  }
                }
              ]
            },
            {
              "name": "rebounds",
              "displayName": "Rebounds",
              "shortDisplayName": "Reb",
              "abbreviation": "Reb",
              "leaders": [
                {
                  "displayValue": "5",
                  "value": 5.0,
                  "athlete": {
                    "id": "2566453",
                    "fullName": "Isabelle Harrison",
                    "displayName": "Isabelle Harrison",
                    "shortName": "I. Harrison",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/2566453/isabelle-harrison"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/2566453.png",
                    "jersey": "21",
                    "position": {
                      "abbreviation": "F"
                    },
                    "team": {
                      "id": "9"
                    },
                    "active": true
                  },
                  "team": {
                    "id": "9"
                  }
                }
              ]
            },
            {
              "name": "assists",
              "displayName": "Assists",
              "shortDisplayName": "Ast",
              "abbreviation": "Ast",
              "leaders": [
                {
                  "displayValue": "6",
                  "value": 6.0,
                  "athlete": {
                    "id": "4066533",
                    "fullName": "Sabrina Ionescu",
                    "displayName": "Sabrina Ionescu",
                    "shortName": "S. Ionescu",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/4066533/sabrina-ionescu"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/4066533.png",
                    "jersey": "20",
                    "position": {
                      "abbreviation": "G"
                    },
                    "team": {
                      "id": "9"
                    },
                    "active": true
                  },
                  "team": {
                    "id": "9"
                  }
                }
              ]
            },
            {
              "name": "rating",
              "displayName": "Rating",
              "shortDisplayName": "RAT",
              "abbreviation": "RAT",
              "leaders": [
                {
                  "displayValue": "11 PTS, 3 STL",
                  "value": 26.549999237060547,
                  "athlete": {
                    "id": "4433386",
                    "fullName": "Jaylyn Sherrod",
                    "displayName": "Jaylyn Sherrod",
                    "shortName": "J. Sherrod",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/4433386/jaylyn-sherrod"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/4433386.png",
                    "jersey": "00",
                    "position": {
                      "abbreviation": "G"
                    },
                    "team": {
                      "id": "9"
                    },
                    "active": false
                  },
                  "team": {
                    "id": "9"
                  }
                }
              ]
            }
          ],
          "records": [
            {
              "name": "overall",
              "abbreviation": "Game",
              "type": "total",
              "summary": "0-1"
            },
            {
              "name": "Home",
              "type": "home",
              "summary": "0-1"
            },
            {
              "name": "Road",
              "type": "road",
              "summary": "0-0"
            }
          ]
        },
        {
          "id": "18",
          "uid": "s:40~l:59~t:18",
          "type": "team",
          "order": 1,
          "homeAway": "away",
          "winner": true,
          "team": {
            "id": "18",
            "uid": "s:40~l:59~t:18",
            "location": "Connecticut",
            "name": "Sun",
            "abbreviation": "CON",
            "displayName": "Connecticut Sun",
            "shortDisplayName": "Sun",
            "color": "f05023",
            "alternateColor": "0a2240",
            "isActive": true,
            "venue": {
              "id": "2160"
            },
            "links": [
              {
                "rel": [
                  "clubhouse",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/_/name/con/connecticut-sun",
                "text": "Clubhouse",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "clubhouse",
                  "mobile",
                  "team"
                ],
                "href": "https://m.espn.com/wnba/clubhouse?teamId=18",
                "text": "Clubhouse",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "roster",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/roster/_/name/con/connecticut-sun",
                "text": "Roster",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "stats",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/stats/_/name/con/connecticut-sun",
                "text": "Statistics",
                "isExternal": false,
                "isPremium": false
              },
              {
                "rel": [
                  "schedule",
                  "desktop",
                  "team"
                ],
                "href": "https://www.espn.com/wnba/team/schedule/_/name/con",
                "text": "Schedule",
                "isExternal": false,
                "isPremium": false
              }
            ],
            "logo": "https://a.espncdn.com/i/teamlogos/wnba/500/con.png"
          },
          "score": "94",
          "linescores": [
            {
              "value": 25.0,
              "displayValue": "25",
              "period": 1
            },
            {
              "value": 28.0,
              "displayValue": "28",
              "period": 2
            },
            {
              "value": 31.0,
              "displayValue": "31",
              "period": 3
            },
            {
              "value": 10.0,
              "displayValue": "10",
              "period": 4
            }
          ],
          "statistics": [
            {
              "name": "rebounds",
              "abbreviation": "REB",
              "displayValue": "32"
            },
            {
              "name": "avgRebounds",
              "abbreviation": "REB",
              "displayValue": "0.0"
            },
            {
              "name": "assists",
              "abbreviation": "AST",
              "displayValue": "24"
            },
            {
              "name": "fieldGoalsAttempted",
              "abbreviation": "FGA",
              "displayValue": "66"
            },
            {
              "name": "fieldGoalsMade",
              "abbreviation": "FGM",
              "displayValue": "32"
            },
            {
              "name": "fieldGoalPct",
              "abbreviation": "FG%",
              "displayValue": "48.5"
            },
            {
              "name": "freeThrowPct",
              "abbreviation": "FT%",
              "displayValue": "82.6"
            },
            {
              "name": "freeThrowsAttempted",
              "abbreviation": "FTA",
              "displayValue": "23"
            },
            {
              "name": "freeThrowsMade",
              "abbreviation": "FTM",
              "displayValue": "19"
            },
            {
              "name": "points",
              "abbreviation": "PTS",
              "displayValue": "94"
            },
            {
              "name": "threePointPct",
              "abbreviation": "3P%",
              "displayValue": "42.3"
            },
            {
              "name": "threePointFieldGoalsAttempted",
              "abbreviation": "3PA",
              "displayValue": "26"
            },
            {
              "name": "threePointFieldGoalsMade",
              "abbreviation": "3PM",
              "displayValue": "11"
            },
            {
              "name": "avgPoints",
              "abbreviation": "PTS",
              "displayValue": "0.0"
            },
            {
              "name": "avgAssists",
              "abbreviation": "AST",
              "displayValue": "0.0"
            },
            {
              "name": "threePointFieldGoalPct",
              "abbreviation": "3P%",
              "displayValue": "42.3"
            }
          ],
          "leaders": [
            {
              "name": "points",
              "displayName": "Points",
              "shortDisplayName": "Pts",
              "abbreviation": "Pts",
              "leaders": [
                {
                  "displayValue": "17",
                  "value": 17.0,
                  "athlete": {
                    "id": "918",
                    "fullName": "Tina Charles",
                    "displayName": "Tina Charles",
                    "shortName": "T. Charles",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/918/tina-charles"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/918.png",
                    "jersey": "31",
                    "position": {
                      "abbreviation": "C"
                    },
                    "team": {
                      "id": "18"
                    },
                    "active": false
                  },
                  "team": {
                    "id": "18"
                  }
                }
              ]
            },
            {
              "name": "rebounds",
              "displayName": "Rebounds",
              "shortDisplayName": "Reb",
              "abbreviation": "Reb",
              "leaders": [
                {
                  "displayValue": "7",
                  "value": 7.0,
                  "athlete": {
                    "id": "4398966",
                    "fullName": "Olivia Nelson-Ododa",
                    "displayName": "Olivia Nelson-Ododa",
                    "shortName": "O. Nelson-Ododa",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/4398966/olivia-nelson-ododa"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/4398966.png",
                    "jersey": "10",
                    "position": {
                      "abbreviation": "C"
                    },
                    "team": {
                      "id": "18"
                    },
                    "active": true
                  },
                  "team": {
                    "id": "18"
                  }
                }
              ]
            },
            {
              "name": "assists",
              "displayName": "Assists",
              "shortDisplayName": "Ast",
              "abbreviation": "Ast",
              "leaders": [
                {
                  "displayValue": "7",
                  "value": 7.0,
                  "athlete": {
                    "id": "3058908",
                    "fullName": "Lindsay Allen",
                    "displayName": "Lindsay Allen",
                    "shortName": "L. Allen",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/3058908/lindsay-allen"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/3058908.png",
                    "jersey": "15",
                    "position": {
                      "abbreviation": "G"
                    },
                    "team": {
                      "id": "18"
                    },
                    "active": false
                  },
                  "team": {
                    "id": "18"
                  }
                }
              ]
            },
            {
              "name": "rating",
              "displayName": "Rating",
              "shortDisplayName": "RAT",
              "abbreviation": "RAT",
              "leaders": [
                {
                  "displayValue": "15 PTS, 7 REB",
                  "value": 29.149999618530273,
                  "athlete": {
                    "id": "4398966",
                    "fullName": "Olivia Nelson-Ododa",
                    "displayName": "Olivia Nelson-Ododa",
                    "shortName": "O. Nelson-Ododa",
                    "links": [
                      {
                        "rel": [
                          "playercard",
                          "desktop",
                          "athlete"
                        ],
                        "href": "https://www.espn.com/wnba/player/_/id/4398966/olivia-nelson-ododa"
                      }
                    ],
                    "headshot": "https://a.espncdn.com/i/headshots/wnba/players/full/4398966.png",
                    "jersey": "10",
                    "position": {
                      "abbreviation": "C"
                    },
                    "team": {
                      "id": "18"
                    },
                    "active": true
                  },
                  "team": {
                    "id": "18"
                  }
                }
              ]
            }
          ],
          "records": [
            {
              "name": "overall",
              "abbreviation": "Game",
              "type": "total",
              "summary": "1-1"
            },
            {
              "name": "Home",
              "type": "home",
              "summary": "0-0"
            },
            {
              "name": "Road",
              "type": "road",
              "summary": "1-1"
            }
          ]
        }
      ],
      "notes": [],
      "status": {
        "clock": 0.0,
        "displayClock": "0.0",
        "period": 4,
        "type": {
          "id": "3",
          "name": "STATUS_FINAL",
          "state": "post",
          "completed": true,
          "description": "Final",
          "detail": "Final",
          "shortDetail": "Final"
        }
      },
      "broadcasts": [
        {
          "market": "home",
          "names": [
            "WWOR-TV",
            "Liberty Live"
          ]
        },
        {
          "market": "away",
          "names": [
            "WNBA League Pass"
          ]
        }
      ],
      "format": {
        "regulation": {
          "periods": 4
        }
      },
      "startDate": "2025-05-09T23:00Z",
      "broadcast": "",
      "geoBroadcasts": [
        {
          "type": {
            "id": "1",
            "shortName": "TV"
          },
          "market": {
            "id": "2",
            "type": "Home"
          },
          "media": {
            "shortName": "WWOR-TV"
          },
          "lang": "en",
          "region": "us"
        },
        {
          "type": {
            "id": "4",
            "shortName": "Streaming"
          },
          "market": {
            "id": "2",
            "type": "Home"
          },
          "media": {
            "shortName": "Liberty Live"
          },
          "lang": "en",
          "region": "us"
        }
      ],
      "highlights": []
    }
  ],
  "links": [
    {
      "language": "en-US",
      "rel": [
        "summary",
        "desktop",
        "event"
      ],
      "href": "https://www.espn.com/wnba/game/_/gameId/401765028/sun-liberty",
      "text": "Gamecast",
      "shortText": "Gamecast",
      "isExternal": false,
      "isPremium": false
    },
    {
      "language": "en-US",
      "rel": [
        "boxscore",
        "desktop",
        "event"
      ],
      "href": "https://www.espn.com/wnba/boxscore/_/gameId/401765028",
      "text": "Box Score",
      "shortText": "Box Score",
      "isExternal": false,
      "isPremium": false
    },
    {
      "language": "en-US",
      "rel": [
        "pbp",
        "desktop",
        "event"
      ],
      "href": "https://www.espn.com/wnba/playbyplay/_/gameId/401765028",
      "text": "Play-by-Play",
      "shortText": "Play-by-Play",
      "isExternal": false,
      "isPremium": false
    }
  ],
  "status": {
    "clock": 0.0,
    "displayClock": "0.0",
    "period": 4,
    "type": {
      "id": "3",
      "name": "STATUS_FINAL",
      "state": "post",
      "completed": true,
      "description": "Final",
      "detail": "Final",
      "shortDetail": "Final"
    }
  }
}
```