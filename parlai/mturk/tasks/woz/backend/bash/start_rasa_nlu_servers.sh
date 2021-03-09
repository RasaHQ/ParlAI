#!/bin/bash

# Start like: /parlai/mturk/tasks/woz/backend/bash/start_rasa_nlu_servers.sh path/to//ParlAI/resources &

RESOURCES_DIR=$1

$RESOURCES_DIR/book_ride/start_nlu_server.sh $RESOURCES_DIR/book_ride
$RESOURCES_DIR/ride_change/start_nlu_server.sh $RESOURCES_DIR/ride_change
$RESOURCES_DIR/ride_status/start_nlu_server.sh $RESOURCES_DIR/ride_status
$RESOURCES_DIR/hotel_search/start_nlu_server.sh $RESOURCES_DIR/hotel_search
$RESOURCES_DIR/hotel_reserve/start_nlu_server.sh $RESOURCES_DIR/hotel_reserve
$RESOURCES_DIR/plane_reserve/start_nlu_server.sh $RESOURCES_DIR/plane_reserve
$RESOURCES_DIR/party_plan/start_nlu_server.sh $RESOURCES_DIR/party_plan
$RESOURCES_DIR/party_rsvp/start_nlu_server.sh $RESOURCES_DIR/party_rsvp
$RESOURCES_DIR/plane_search/start_nlu_server.sh $RESOURCES_DIR/plane_search
$RESOURCES_DIR/restaurant_reserve/start_nlu_server.sh $RESOURCES_DIR/restaurant_reserve
$RESOURCES_DIR/restaurant_search/start_nlu_server.sh $RESOURCES_DIR/restaurant_search
$RESOURCES_DIR/apartment_search/start_nlu_server.sh $RESOURCES_DIR/apartment_search
$RESOURCES_DIR/book_apartment_viewing/start_nlu_server.sh $RESOURCES_DIR/book_apartment_viewing
$RESOURCES_DIR/book_doctor_appointment/start_nlu_server.sh $RESOURCES_DIR/book_doctor_appointment
$RESOURCES_DIR/followup_doctor_appointment/start_nlu_server.sh $RESOURCES_DIR/followup_doctor_appointment
$RESOURCES_DIR/spaceship_access_codes/start_nlu_server.sh $RESOURCES_DIR/spaceship_access_codes
$RESOURCES_DIR/spaceship_life_support/start_nlu_server.sh $RESOURCES_DIR/spaceship_life_support
$RESOURCES_DIR/bank_balance/start_nlu_server.sh $RESOURCES_DIR/bank_balance
$RESOURCES_DIR/bank_fraud_report/start_nlu_server.sh $RESOURCES_DIR/bank_fraud_report
$RESOURCES_DIR/trivia/start_nlu_server.sh $RESOURCES_DIR/trivia
$RESOURCES_DIR/hotel_service_request/start_nlu_server.sh $RESOURCES_DIR/hotel_service_request
$RESOURCES_DIR/weather/start_nlu_server.sh $RESOURCES_DIR/weather
$RESOURCES_DIR/trip_directions/start_nlu_server.sh $RESOURCES_DIR/trip_directions
$RESOURCES_DIR/schedule_meeting/start_nlu_server.sh $RESOURCES_DIR/schedule_meeting

echo "Rasa NLU servers started!"