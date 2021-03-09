#!/bin/bash

MODEL_PATH=$1

rasa run --enable-api -m $MODEL_PATH/rasa-v1.9.6_nlu-party_rsvp.tar.gz -p 5011 &