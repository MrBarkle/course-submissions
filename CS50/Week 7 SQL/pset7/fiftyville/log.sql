-- A Mystery in Fiftyville: Log File

-- First looking in crime_scene_reports for the report that took place on July 28, 2020 on Chamberlin Street.
-- This is the only known information so far regarding the CS50 Duck being stolen.
SELECT description FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28
AND street = "Chamberlin Street";

    -- According to the crime_scene_reports query: "Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
    -- Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse."

-- Checking interviews that same day
SELECT * FROM interviews WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%courthouse%";

    -- The three witnesses include Ruth, Eugene, and Raymond
    -- Look for security footage from the couthouse parking lot within 10 minutes of the theft, which as we know took place at 10:15am on July 28, 2020.
    -- The theif withdrew money on Fifer Street early that morning
    -- The theif made a phone call for less than a minute as they were leaving the courthouse. They were planning on taking the earliest flight out of Fiftyville the next day.
    -- This plane ticket was to be purchased by the person on the other end of the phone.

-- Looking at earliest flight out of Fiftyville on the 29th to see what information can be aquired.
SELECT * FROM flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1;

    -- id | origin_airport_id | destination_airport_id | year | month | day | hour | minute
    -- 36 | 8                 | 4                      | 2020 | 7     | 29  | 8    | 20

-- Checking where this flight goes:
SELECT city FROM airports WHERE id = 4;

    -- London! (2) The theif escaped to London.

-- Next, to find out who was involved.
-- Security Footage at the courthouse turns up these license plate numbers from 10:10am - 10:25am on the day of the theft.
SELECT name, people.license_plate AS license_plate FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute > 10 AND minute < 25;

    -- name      | license_plate
    -- Sophia    | 13FNH73
    -- Patrick   | 5P2BI95
    -- Ernest    | 94KL13X
    -- Amber     | 6P58WS2
    -- Danielle  | 4328GD8
    -- Roger     | G412CB7
    -- Elizabeth | L93JTIZ
    -- Russell   | 322W7JE
    -- Evelyn    | 0NTHK55

-- Next I'll check the ATM on Fifer Street for account_numbers that withdrew money
SELECT account_number FROM atm_transactions WHERE transaction_type = "withdraw" AND year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street";

    -- 28500762
    -- 28296815
    -- 76054385
    -- 49610011
    -- 16153065
    -- 25506511
    -- 81061156
    -- 26013199

-- Which people do these belong to? AND how many of them had a car at the courthouse within the timeframe of the theft?
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2020
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = "Fifer Street"
AND transaction_type = "withdraw"
AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 10 AND minute <= 25);

    --name
    -- Ernest
    -- Russell
    -- Elizabeth
    -- Danielle

-- What else can we learn about each?
SELECT * FROM people WHERE name IN ("Ernest", "Russell", "Elizabeth", "Danielle");

    -- id     | name      | phone_number   | passport_number | license_plate
    -- 396669 | Elizabeth | (829) 555-5269 | 7049073643      | L93JTIZ
    -- 467400 | Danielle  | (389) 555-5198 | 8496433585      | 4328GD8
    -- 514354 | Russell   | (770) 555-1861 | 3592750733      | 322W7JE
    -- 686048 | Ernest    | (367) 555-5533 | 5773159633      | 94KL13X

-- Any on Flight 36 From Fiftyville to London on July 29, 2020?
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE people.passport_number IN (SELECT passport_number FROM people 
WHERE name IN ("Ernest", "Russell", "Elizabeth", "Danielle"))
AND flights.id = 36;

    -- name
    -- Ernest
    -- Danielle

-- Checking phone calls on the day of the theft that each made
SELECT caller, name, duration, receiver FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE caller IN ("(389) 555-5198","(367) 555-5533")  AND year = 2020 AND month = 7
AND day = 28;

    --caller         | name     | duration | receiver
    --(367) 555-5533 | Berthold | 45       | (375) 555-8161
    --(367) 555-5533 | Deborah  | 120      | (344) 555-9601
    --(367) 555-5533 | Gregory  | 241      | (022) 555-4052
    --(367) 555-5533 | Carl     | 75       | (704) 555-5790
    
-- It would appear that ONLY Ernest made phone calls on the day of the crime, one of which 
-- was for less than 60 seconds (matching the interview description from above) to Berthold.
-- This would make Ernest the theif and Berthold the accomplice. 