from faker import Faker
import random
import time
import argparse
import json
from pathlib import Path

fake = Faker()


# this takes a while.
def create_fake_emails(num=1):
    start_time = time.time()
    number_of_emails = int(num)
    if number_of_emails > 10000:
        print("Note: Expect the function that generates a list of random email addresses "
              "to take ~1 second per 10000 emails "
              f"({(number_of_emails//10000)} seconds)\nTry using -ff to load from a file")
    # going to be duplicating the list later so let's device the number we create by 2
    number_of_emails = number_of_emails // 2
    output: list = [fake.email() for x in range(number_of_emails)]
    output.extend(output)
    random.shuffle(output)
    # print(f"create_fake_emails --- fake email list before dedupe\n{output}")
    print("create_fake_emails --- %s seconds ---" % (time.time() - start_time))
    return output


# my implementation
def remove_duplicates(test_list):
    start_time = time.time()
    output_list = []
    tracking_set: set = set()
    for email in test_list:
        if email not in tracking_set:
            output_list.append(email)
            tracking_set.add(email)
    print("remove_duplicates --- %s seconds --- <<<<<<<< my implementation" % (time.time() - start_time))
    return output_list


# standard memory efficient implementation (but slow)
def remove_duplicates_slow(test_list):
    start_time = time.time()
    output_list = []
    for email in test_list:
        if email not in output_list:
            output_list.append(email)
    print("remove_duplicates_slow --- %s seconds ---" % (time.time() - start_time))
    return output_list


# utilizes pythons set, but is not ordered
def remove_duplicates_no_order(test_list):
    start_time = time.time()
    output_list = list(set(test_list))
    print("remove_duplicates_no_order --- %s seconds ---" % (time.time() - start_time))
    return output_list


def are_these_lists_the_same(fast_list, unordered_list):
    fast_list.sort()
    unordered_list.sort()
    return fast_list == unordered_list


def main():
    parser = argparse.ArgumentParser(
        description=(
            "A speed efficient way to de-duplicate a list in Python"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-n", "--number-of-emails", default=100000,
                        help="Choose the number of email addresses you would like to generate for your test"
                             "Note: Don't use with -ff")
    parser.add_argument(
        "-s", "--slow-test",
        action="store_true",
        default=False,
        help="Choose to run the slow tests as well. (Not recommended for lists larger than 10,000)",
    )
    parser.add_argument(
        "-ff", "--from-file",
        default=False,
        help="Specify the file location you wish to read from in relation this this script.",
    )
    parser.add_argument(
        "-w", "--write-file",
        default=False,
        help="Specify the file location you wish to write to in relation this this script.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="see list output. (not recommended for over 20 emails)",
    )
    args = parser.parse_args()
    if args.write_file:
        random_list = create_fake_emails(args.number_of_emails)
        with open(args.write_file, 'w', encoding='utf-8') as file:
            json.dump(random_list, file, ensure_ascii=False, indent=4)
    else:
        if args.from_file:
            file = open(args.from_file)
            random_list = json.load(file)
        else:
            random_list = create_fake_emails(args.number_of_emails)
    if args.debug:
        print(f"random_list:\n{random_list}")
    fast_list = remove_duplicates(random_list)
    if args.debug:
        print(f"fast_list:\n{fast_list}")
    unordered_list = remove_duplicates_no_order(random_list)
    if args.debug:
        print(f"unordered_list:\n{unordered_list}")
    if args.slow_test:
        slow_list = remove_duplicates_slow(random_list)
        if args.debug:
            print(f"slow_list:\n{slow_list}")
        if fast_list == slow_list:
            print("The fast_list and slow_list are identical --- SUCCESS ---")
        else:
            print("The fast_list and slow_list are not identical --- FAIL ---")
    if fast_list != unordered_list:
        print("The fast_list and unordered_list are not identical --- SUCCESS ---")
        print(f"These lists are equal when sorted: {are_these_lists_the_same(fast_list, unordered_list)}")
    else:
        print("The fast_list and unordered_list are identical go play the lottery")


if __name__ == "__main__":
    main()
