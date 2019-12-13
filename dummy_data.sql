-- Dummy data for picMe, wipes all tables and inserts fresh data


-- wipe all tables

DELETE FROM BelongTo WHERE TRUE;
DELETE FROM Friendgroup WHERE TRUE;
DELETE FROM Follow WHERE TRUE;
DELETE FROM Photo WHERE TRUE;
DELETE FROM Person WHERE TRUE;



-- Create Users (register):


INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('admin', '7095f51c359c0ab163aa05ae1e0435653b074f47b8eae7548aaf6edc0e78605a', 'root', 'rooty', 'this is my bio', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('kevinp', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'kevin', 'perez', ' bios are the worst', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('demmyp', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'demmy', 'perez', ' random strings of text', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('hectorp', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'hector', 'perez', ' i am kevins father', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('rosap', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'rosa', 'perez', 'i am kevins mother', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('marcosb', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'marcos', 'barron', ' i am an alcoholic', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('aidan', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'aidan', 'llora', ' imarcos IS an alcoholic', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('carlosp', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'carlos', 'perez', 'i am kevins brother', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('asim123', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'asim', 'swatti', 'i make great games', 'default.png');
INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`, `profilePicPath`) VALUES ('john123', '6a2c66112fc234d1044071c7877c85844a476ea766190ad62f87d60c5374738c', 'john', 'novak', 'scanifly is a great product', 'default.png');


-- Create Photo posts (Post a photo):

INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic1.png', '0', 'this is file pic1', 'admin');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic2.png', '1', 'this is file pic2', 'kevinp');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic3.png', '0', 'this is file pic3', 'demmyp');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic4.jpg', '1', 'this is file pic4', 'hectorp');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic5.png', '0', 'this is file pic5', 'rosap');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic6.png', '1', 'this is file pic6', 'marcosb');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic7.png', '0', 'this is file pic7', 'aidan');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic8.png', '1', 'this is file pic8', 'carlosp');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic9.png', '0', 'this is file pic9', 'asim123');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES (NULL, CURRENT_TIMESTAMP, 'd2b296a4c02221254b9fb9bfd5b725e7_pic10.png', '1', 'this is file pic10', 'john123');



-- Create follow entries (Folow user)

INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES ('kevinp', 'demmyp', '1');
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES ('kevinp', 'hectorp', '1');
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES ('kevinp', 'rosap', '1');
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES ('demmyp', 'kevinp', '1');
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES ('rosap', 'kevinp', '1');
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES ('hectorp', 'kevinp', '1');


-- Create friend groups (Create group)

INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES ('kevinp', 'Family', 'this is a group for my family :)');
INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES ('kevinp', 'Friends', 'this is a group for my friends :)');
INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES ('john123', 'Work', 'this is the scanifly group');
INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES ('marcosb', 'Drunks', 'ths is gruoop fpor tihue drunjks');


-- Create group rationships (Join groups)

INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('kevinp', 'kevinp', 'Family');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('demmyp', 'kevinp', 'Family');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('hectorp', 'kevinp', 'Family');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('rosap', 'kevinp', 'Family');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('kevinp', 'kevinp', 'Friends');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('aidan', 'kevinp', 'Friends');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('marcosb', 'kevinp', 'Friends');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('asim123', 'kevinp', 'Friends');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('demmyp', 'kevinp', 'Friends');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('john123', 'john123', 'Work');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('asim123', 'john123', 'Work');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('kevinp', 'john123', 'Work');
INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES ('aidan', 'marcosb', 'Drunks');






