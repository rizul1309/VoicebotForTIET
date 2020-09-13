## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 121
* greet
  - utter_greet
* ask_for_cabin
  - action_show_cabin_dir
* deny
  - utter_goodbye

## sad path 123
* greet
  - utter_greet
* ask_for_lab
  - action_show_lab
* deny
  - utter_goodbye



## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
