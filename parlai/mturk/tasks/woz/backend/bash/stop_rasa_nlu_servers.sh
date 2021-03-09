#!/bin/bash

for PORT_NR in 5005 5006 5007 5008 5009 5010 5011 5012 5013 5014 5015 5016 5017 5018 5019 5020 5021 5022 5023 5024 5025 5026 5027 5028; do
  PID=$(lsof -i :$PORT_NR | awk 'NR > 1 {print $2}')
  kill -9 $PID
done

echo "Rasa NLU servers stopped!"