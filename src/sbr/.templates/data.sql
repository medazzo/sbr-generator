/* Generated Admin user with mail='{{mail}}' and password='{{passwordclear}}' */ 
INSERT INTO USER ( ACTIVATED , ACTIVATION_KEY , CREATED_AT , EMAIL , FIRST_NAME , ID , IMAGE_URL , LANG_KEY , LAST_NAME , MAIN_ROLE , NAME , PASSWORD_HASH , PHONE , RESET_DATE , RESET_KEY , UPDATED_AT , VERSION ) VALUES (TRUE, 'ACT-KEY-NOT-NEEDED', NOW(), '{{mail}}', ' Me Admin','{{uuid}}','IMAGE_URL-NOT-NEEDED', 'EN', 'Very strong', 'ROLE_ADMIN','Me Strong Admin', '{{password}}', '0022554411887',NOW() , 'RESET_KEY-NOT-NEEDED' , NOW() , 0);

/* Generated USER with mail='{{umail}}' and password='{{upasswordclear}}' */ 
INSERT INTO USER ( ACTIVATED , ACTIVATION_KEY , CREATED_AT , EMAIL , FIRST_NAME , ID , IMAGE_URL , LANG_KEY , LAST_NAME , MAIN_ROLE , NAME , PASSWORD_HASH , PHONE , RESET_DATE , RESET_KEY , UPDATED_AT , VERSION ) VALUES (TRUE, 'ACT-KEY-NOT-NEEDED', NOW(), '{{umail}}', ' Me User','{{uuuid}}','IMAGE_URL-NOT-NEEDED', 'EN', 'Very Helpful', 'ROLE_USER','Me Useful User', '{{upassword}}', '0022554411887',NOW() , 'RESET_KEY-NOT-NEEDED' , NOW() , 0);