CREATE TABLE `DRIVERADDRESS` (
	`driver_id`	INTEGER NOT NULL,
	`address_id`	INTEGER NOT NULL,
	PRIMARY KEY(`driver_id`,`address_id`),
	FOREIGN KEY(`driver_id`) REFERENCES DRIVER(`driver_id`),
	FOREIGN KEY(`address_id`) REFERENCES ADDRESS(`address_id`)
);