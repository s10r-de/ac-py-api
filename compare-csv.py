#!/usr/bin/which python3
#
# USAGE:
# python3 compare-csv.py export-cloud.csv export-backup-system.csv
#
# it will generate 2 CSV Files:
# - items-different.csv
# - items-missing.csv
#

import sys
import re
import csv


def item_is_equal(a, b):
    if a["Project ID"] != b["Project ID"]:
        return False
    if a["Project"] != b["Project"]:
        return False
    if a["Task Number"] != b["Task Number"]:
        return False
    if a["Name"] != b["Name"]:
        return False
    if a["Task List"] != b["Task List"]:
        return False
    if a["Created On"] != b["Created On"]:
        return False
    if a["Created By"] != b["Created By"]:
        return False
    if a["Due On"] != b["Due On"]:
        return False
    if a["Start On"] != b["Start On"]:
        return False
    if a["Created By ID"] != b["Created By ID"]:
        return False
    if a["Labels"] != b["Labels"]:
        return False
    if a["Assignee ID"] != b["Assignee ID"]:
        return False
    if a["Is Important"] != b["Is Important"]:
        return False
    if a["Task List ID"] != b["Task List ID"]:
        return False
    if a["Assignee"] != b["Assignee"]:
        return False
    if a["Completed On"] != b["Completed On"]:
        return False
    if a["Completed By"] != b["Completed By"]:
        return False
    if a["Type"] != b["Type"]:
        return False
    return True


def main(args: list) -> None:
    file1 = args[1]
    file2 = args[2]
    print(f"compare {file1} and {file2}")

    ob = re.compile(r".*o\.\s*B\..*")
    fieldnames1 = None
    all_tasks1 = {}
    with open(file1, "r", encoding="utf-8") as fh1:
        csv1 = csv.DictReader(fh1)
        for row in csv1:
            if ob.match(row["Project"]):
                continue
            unique_id = "%08d-%08d" % (int(row["Project ID"]), int(row["Task Number"]))
            all_tasks1[unique_id] = row
            if fieldnames1 is None:
                fieldnames1 = list(row.keys())

    all_tasks2 = {}
    with open(file2, "r", encoding="utf-8") as fh2:
        csv2 = csv.DictReader(fh2)
        for row in csv2:
            if ob.match(row["Project"]):
                continue
            unique_id = "%08d-%08d" % (int(row["Project ID"]), int(row["Task Number"]))
            all_tasks2[unique_id] = row

    items_missing = {}
    items_different = {}
    for id, item in all_tasks1.items():
        if id not in all_tasks2.keys():
            items_missing[id] = item
        else:
            if not item_is_equal(item, all_tasks2[id]):
                items_different[id] = (item, all_tasks2[id])

    with open("items-missing.csv", "w", encoding="utf-8") as fh3:
        writer = csv.DictWriter(fh3, fieldnames=fieldnames1)
        writer.writeheader()
        for id, item in items_missing.items():
            writer.writerow(item)

    fieldnames2 = [
        "filename",
        "Project ID",
        "Project",
        "Task Number",
        "Name",
        "Task List",
        "Created On",
        "Created By",
        "Due On",
        "Start On",
        "Created By ID",
        "Labels",
        "Assignee ID",
        "Is Important",
        "Task List ID",
        "Assignee",
        "Completed On",
        "Completed By",
        "Type",
    ]
    print(fieldnames2)
    with open("items-different.csv", "w", encoding="utf-8") as fh4:
        writer = csv.DictWriter(fh4, fieldnames=fieldnames2, restval="qqq")
        writer.writeheader()
        for id, item in items_different.items():
            item_a = {}
            item_a["filename"] = file1
            item_a["Project ID"] = item[0]["Project ID"]
            item_a["Project"] = item[0]["Project"]
            item_a["Task Number"] = item[0]["Task Number"]
            item_a["Name"] = item[0]["Name"]
            item_a["Task List"] = item[0]["Task List"]
            item_a["Created On"] = item[0]["Created On"]
            item_a["Created By"] = item[0]["Created By"]
            item_a["Due On"] = item[0]["Due On"]
            item_a["Start On"] = item[0]["Start On"]
            item_a["Created By ID"] = item[0]["Created By ID"]
            item_a["Labels"] = item[0]["Labels"]
            item_a["Assignee ID"] = item[0]["Assignee ID"]
            item_a["Is Important"] = item[0]["Is Important"]
            item_a["Task List ID"] = item[0]["Task List ID"]
            item_a["Assignee"] = item[0]["Assignee"]
            item_a["Completed On"] = item[0]["Completed On"]
            item_a["Completed By"] = item[0]["Completed By"]
            item_a["Type"] = item[0]["Type"]
            item_b = {}
            item_b["filename"] = file2
            item_b["Project ID"] = item[1]["Project ID"]
            item_b["Project"] = item[1]["Project"]
            item_b["Task Number"] = item[1]["Task Number"]
            item_b["Name"] = item[1]["Name"]
            item_b["Task List"] = item[1]["Task List"]
            item_b["Created On"] = item[1]["Created On"]
            item_b["Created By"] = item[1]["Created By"]
            item_b["Due On"] = item[1]["Due On"]
            item_b["Start On"] = item[1]["Start On"]
            item_b["Created By ID"] = item[1]["Created By ID"]
            item_b["Labels"] = item[1]["Labels"]
            item_b["Assignee ID"] = item[1]["Assignee ID"]
            item_b["Is Important"] = item[1]["Is Important"]
            item_b["Task List ID"] = item[1]["Task List ID"]
            item_b["Assignee"] = item[1]["Assignee"]
            item_b["Completed On"] = item[1]["Completed On"]
            item_b["Completed By"] = item[1]["Completed By"]
            item_b["Type"] = item[1]["Type"]
            writer.writerow(item_a)
            writer.writerow(item_b)

    print("done.")


if __name__ == "__main__":
    main(sys.argv)
