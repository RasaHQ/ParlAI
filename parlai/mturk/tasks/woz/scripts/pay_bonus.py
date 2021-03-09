import os
import sys
import csv
from typing import Text

from parlai.mturk.core import mturk_utils

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Bonus file parameter missing")
        exit(1)
    bonus_file: Text = sys.argv[1]
    if not os.path.exists(bonus_file):
        print(f"Bonus file '{bonus_file}' not found.")

    orders = []
    total = 0
    workers = set()

    with open(bonus_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(
            file,
            dialect='excel-tab',
            fieldnames=[
                "PaymentDescription",
                "Directory",
                "Role",
                "WorkerID",
                "AssignmentID",
                "BonusAmount",
                "Reason",
            ],
        )
        for row in reader:
            row = dict(row)
            total += float(row["BonusAmount"])
            workers.add(row["WorkerID"])
            orders.append(row)

    if not orders:
        print("Nothing to pay.")
        exit(0)

    if total == 0.0:
        print("Nothing to pay.")
        exit(0)

    print(
        f"In total, you are going to pay {total:.2f} USD + MTurk fees to {len(workers)} workers."
    )
    print(f"Confirm by entering the amount.")
    confirm = input()
    if float(confirm) - total >= 0.01:
        print("Payment aborted")
        exit(0)

    mturk_utils.setup_aws_credentials()
    client = mturk_utils.get_mturk_client(is_sandbox=False)
    processed_orders = []
    for order in orders:
        print(f"Paying {order['BonusAmount']} to worker {order['WorkerID']}...")
        client.send_bonus(
            WorkerId=order["WorkerID"],
            AssignmentId=order["AssignmentID"],
            Reason=order["Reason"],
            BonusAmount=order["BonusAmount"]
        )
        order.update({"PaymentDescription": "SENT"})
        processed_orders.append(order)


    with open(bonus_file, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=list(processed_orders[0].keys()), dialect='excel-tab'
        )
        writer.writerows(processed_orders)
