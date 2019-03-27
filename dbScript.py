import pymysql
import settings

def createTables(DBname):
    #build the connect and select the DB
    mydb = pymysql.connect(settings.localhost, settings.username, settings.password)

    my_cursor = mydb.cursor()

    sql_createDB = "create database " + DBname

    my_cursor.execute(sql_createDB)
    
    sql_selectDB = "USE "+DBname

    sql_createDB = "create database "+DBname


    my_cursor.execute(sql_selectDB)

    # drop the existing table to make the DB clean
    sql_dropTables = "select concat('drop table ',table_name,';') " \
                     "from information_schema.TABLES where table_schema='"+DBname+"';"

    my_cursor.execute(sql_dropTables)

    sql_creatImagesTable = "CREATE TABLE `"+DBname+"`.`Images` (" \
                                                                 "`imageID` INT NOT NULL AUTO_INCREMENT, " \
                                                                 "`imageName` VARCHAR(45) NOT NULL, " \
                                                                 "`image` BLOB NOT NULL, " \
                                                                 "PRIMARY KEY (`imageID`)) " \
                                                                 "ENGINE = InnoDB"

    sql_creatCopyTrailTable = """CREATE TABLE `CognitiveTestDB`.`Copy_Trial` 
    (`copyTrialID` INT NOT NULL AUTO_INCREMENT, 
    `copyTrialPixels` LONGTEXT NULL, 
    `copyTrialStartTime` VARCHAR(45) NULL, 
    `copyTrialEndTime` VARCHAR(45) NULL, 
    PRIMARY KEY (`copyTrialID`), 
    UNIQUE INDEX `copyTrialID_UNIQUE` (`copyTrialID` ASC)
    ) ENGINE = InnoDB"""

    sql_creatParticipantsTable = """CREATE TABLE IF NOT EXISTS `CognitiveTestDB`.`Participants` ( 
    `participantID` VARCHAR(50) NOT NULL, 
    `firstName` VARCHAR(45) NOT NULL, 
    `familyName` VARCHAR(45) NOT NULL, 
    `gender` VARCHAR(45) NOT NULL, 
    `dateOfBirth` VARCHAR(45) NOT NULL, 
    PRIMARY KEY (`participantID`))
    ENGINE = InnoDB"""

    sql_creatRecallTrailTable = """CREATE TABLE IF NOT EXISTS `CognitiveTestDB`.`Recall_Trial` ( 
    `recallTrailID` INT NOT NULL AUTO_INCREMENT, 
    `recallTrialPixels` LONGTEXT NULL, 
    `recallTrailThinkingStartTime` VARCHAR(45) NULL, 
    `recallTrailThinkingEndTime` VARCHAR(45) NULL, 
    `recallTrailDrawingStartTime` VARCHAR(45) NULL, 
    `recallTrailDrawingEndTime` VARCHAR(45) NULL, 
    PRIMARY KEY (`recallTrailID`), 
    UNIQUE INDEX `recallTrailID_UNIQUE` (`recallTrailID` ASC))
    ENGINE = InnoDB"""

    sql_creatSecurityTable = """CREATE TABLE IF NOT EXISTS `CognitiveTestDB`.`Security` ( 
    `userName` VARCHAR(50) NOT NULL, 
    `password` CHAR(64) NOT NULL, 
    INDEX `fk_security_Clinician1_idx` (`userName` ASC), 
    PRIMARY KEY (`userName`), 
    UNIQUE INDEX `userName_UNIQUE` (`userName` ASC), 
    CONSTRAINT `fk_security_Clinician1` 
    FOREIGN KEY (`userName`) 
    REFERENCES `CognitiveTestDB`.`Staff` (`userName`) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION)
    ENGINE = InnoDB"""

    sql_creatStaffTable = """CREATE TABLE IF NOT EXISTS `CognitiveTestDB`.`Staff` ( 
    `userName` VARCHAR(50) NOT NULL, 
    `firstName` VARCHAR(45) NOT NULL, 
    `familyName` VARCHAR(45) NOT NULL, 
    `dateOfBirth` VARCHAR(45) NOT NULL, 
    PRIMARY KEY (`userName`), 
    UNIQUE INDEX `userName_UNIQUE` (`userName` ASC)) 
    ENGINE = InnoDB"""

    sql_creatTrialTable = """CREATE TABLE IF NOT EXISTS `CognitiveTestDB`.`Trails` ( 
    `trialID` INT NOT NULL AUTO_INCREMENT, 
    `participantID` VARCHAR(50) NOT NULL, 
    `userName` VARCHAR(50) NOT NULL, 
    `imageID` INT NOT NULL, 
    `copyTrailID` INT NOT NULL, 
    `recallTrailID` INT NOT NULL, 
    `trialStartTime` VARCHAR(45) NOT NULL, 
    `trailEndTime` VARCHAR(45) NULL, 
    PRIMARY KEY (`trialID`), 
    INDEX `fk_Test Result_Patient_idx` (`participantID` ASC), 
    INDEX `fk_Test Result_Clinician1_idx` (`userName` ASC), 
    INDEX `fk_Tasks_Images1_idx` (`imageID` ASC), 
    INDEX `fk_Tasks_Copy_Task1_idx` (`copyTrailID` ASC), 
    INDEX `fk_Tasks_Recall_Task1_idx` (`recallTrailID` ASC), 
    UNIQUE INDEX `trialID_UNIQUE` (`trialID` ASC), 
    CONSTRAINT `fk_Test Result_Patient` 
    FOREIGN KEY (`participantID`) 
    REFERENCES `CognitiveTestDB`.`Participants` (`participantID`) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION, 
    CONSTRAINT `fk_Test Result_Clinician1` 
    FOREIGN KEY (`userName`) 
    REFERENCES `CognitiveTestDB`.`Staff` (`userName`) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION, 
    CONSTRAINT `fk_Tasks_Images1` 
    FOREIGN KEY (`imageID`) 
    REFERENCES `CognitiveTestDB`.`Images` (`imageID`) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION, 
    CONSTRAINT `fk_Tasks_Copy_Task1` 
    FOREIGN KEY (`copyTrailID`) 
    REFERENCES `CognitiveTestDB`.`Copy_Trial` (`copyTrialID`) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION, 
    CONSTRAINT `fk_Tasks_Recall_Task1` 
    FOREIGN KEY (`recallTrailID`) 
    REFERENCES `CognitiveTestDB`.`Recall_Trial` (`recallTrailID`) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION)
    ENGINE = InnoDB"""

    my_cursor.execute(sql_creatCopyTrailTable)
    my_cursor.execute(sql_creatStaffTable)
    my_cursor.execute(sql_creatRecallTrailTable)
    my_cursor.execute(sql_creatSecurityTable)
    my_cursor.execute(sql_creatParticipantsTable)
    my_cursor.execute(sql_creatImagesTable)
    my_cursor.execute(sql_creatTrialTable)

    mydb.close()

createTables(settings.DBname)
print("Database created")