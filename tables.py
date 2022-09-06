from scos_connector import data_classes

tables = {
    'educational_programs': '''CREATE TABLE "educational_programs" (
                "id" INTEGER,
                "external_id" VARCHAR(256) NOT NULL,
                "title"	VARCHAR(256) NOT NULL,
                "direction"	VARCHAR(256) NOT NULL,
                "code_direction" VARCHAR(20),
                "start_year" INTEGER NOT NULL,
                "end_year" INTEGER NOT NULL,
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'study_plans': '''CREATE TABLE "study_plans" (
                "id" INTEGER,
                "external_id" VARCHAR(256) NOT NULL,
                "title"	VARCHAR(256) NOT NULL,
                "direction"	VARCHAR(256) NOT NULL,
                "code_direction" VARCHAR(20),
                "start_year" INTEGER NOT NULL,
                "end_year" INTEGER NOT NULL,
                "education_form" VARCHAR(256) NOT NULL,
                "educational_program_scos_id" INTEGER NOT NULL,
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'disciplines': '''CREATE TABLE "disciplines" (
                "id" INTEGER,
                "external_id" VARCHAR(256) NOT NULL,
                "title"	VARCHAR(256) NOT NULL,
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,               
                "deleted" DATETIME, 
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'study_plan_disciplines': '''CREATE TABLE "study_plan_disciplines" (
                "id" INTEGER,
                "study_plan_scos_id" INTEGER NOT NULL,
                "discipline_scos_id" INTEGER NOT NULL,
                "semester" INTEGER,
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,            
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'students': '''CREATE TABLE "students" (
                "id" INTEGER,
                "external_id" VARCHAR(256) NOT NULL,
                "surname"	VARCHAR(256) NOT NULL,
                "name"	VARCHAR(256) NOT NULL,
                "middle_name"	VARCHAR(256),
                "date_of_birth"	DATE,
                "snils"	VARCHAR(256),
                "inn"	VARCHAR(256),
                "email"	VARCHAR(256),
                "study_year" INTEGER,
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,                
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'study_plan_students': '''CREATE TABLE "study_plan_students" (
                "id" INTEGER,
                "study_plan_scos_id" INTEGER NOT NULL,
                "student_scos_id" INTEGER NOT NULL,
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,                
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'contingent_flows': '''CREATE TABLE "contingent_flows" (
                "id" INTEGER,
                "external_id" VARCHAR(256),
                "student_scos_id" INTEGER NOT NULL,
                "contingent_flow"	VARCHAR(128) NOT NULL,
                "flow_type"	VARCHAR(256) NOT NULL,
                "date"	DATE NOT NULL,
                "faculty"	VARCHAR(256),
                "education_form"	VARCHAR(128) NOT NULL,
                "form_fin"	VARCHAR(256),
                "details"	VARCHAR(256),
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,                
                PRIMARY KEY("id" AUTOINCREMENT));''',
    'marks': '''CREATE TABLE "marks" (
                "id" INTEGER,
                "external_id" VARCHAR(256),
                "discipline" INTEGER NOT NULL,
                "study_plan" INTEGER NOT NULL,
                "student" INTEGER NOT NULL,
                "mark_type"	VARCHAR(128) NOT NULL,
                "mark_value" INTEGER NOT NULL,
                "semester" INTEGER NOT NULL,
                "scos_id" VARCHAR(40),
                "last_update" DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
                "last_scos_update" DATETIME,
                "deleted" DATETIME,                
                PRIMARY KEY("id" AUTOINCREMENT));'''
}

update_trigger_text = '''CREATE TRIGGER %name_last_update AFTER UPDATE ON %name
                    BEGIN
                    UPDATE %name SET last_update = datetime('now', 'localtime') WHERE id = new.id;
                    END;        '''
