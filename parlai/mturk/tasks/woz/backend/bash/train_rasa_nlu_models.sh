#!/bin/bash

# Start like: /parlai/mturk/tasks/woz/backend/bash/train_rasa_nlu_models.sh -r path/to//ParlAI/resources

# Parse options
while getopts "f:r:" OPT; do
	case $OPT in
	  f ) FORCE_OVERWRITE=($OPTARG) ;;

	  r ) RESOURCES_DIR=($OPTARG) ;;
	esac
done

RASA_VERSION_STRING=($(rasa --version))
RASA_VERSION=${RASA_VERSION_STRING[1]}

for DIR_NAME in "book_ride" "hotel_reserve" "hotel_search" "party_plan" "party_rsvp" "plane_reserve" "plane_search" "restaurant_reserve" "restaurant_search" "ride_change" "ride_status" "apartment_search" "book_apartment_viewing" "book_doctor_appointment" "followup_doctor_appointment" "spaceship_access_codes" "spaceship_life_support" "bank_balance" "bank_fraud_report" "hotel_service_request" "schedule_meeting" "trip_directions" "trivia" "weather"; do

  TRAINED_MODEL_FILE=$RESOURCES_DIR/$DIR_NAME/"rasa-v"$RASA_VERSION"_nlu-"$DIR_NAME".tar.gz"

  if [[ "$FORCE_OVERWRITE" == "true" ]] || [ ! -f "$TRAINED_MODEL_FILE" ]; then
    echo "Training NLU model for $DIR_NAME..."
    rasa train nlu -u $RESOURCES_DIR/$DIR_NAME/nlu_training_data.md -c $RESOURCES_DIR/nlu_model_config.yml --out $RESOURCES_DIR/$DIR_NAME --fixed-model-name "rasa-v"$RASA_VERSION"_nlu-"$DIR_NAME
  else
    echo "$TRAINED_MODEL_FILE already exists, skipping re-training!"
  fi
done

echo "Rasa NLU models retrained!"