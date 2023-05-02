CREATE TABLE `DRIVER` (
	`driver_id`	CHAR ( 9 ) NOT NULL,
	`driver_name`	VARCHAR NOT NULL,
	`driver_dob`	DATE NOT NULL,
	`driver_hire_date`	DATE NOT NULL,
	`driver_plate_number`	INTEGER,
	`driver_email`	VARCHAR NOT NULL,
	`driver_password`	INTEGER NOT NULL,
	PRIMARY KEY(`driver_id`)
);