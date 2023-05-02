CREATE TABLE `ADDRESS` (
	`address_id`	VARCHAR NOT NULL,
	`address_block_number`	INTEGER NOT NULL,
	`address_floor_number`	INTEGER,
	`address_apartment_number`	INTEGER,
	`address_street_name`	VARCHAR NOT NULL,
	`address_postal_code`	INTEGER NOT NULL,
	PRIMARY KEY(`address_id`)
);