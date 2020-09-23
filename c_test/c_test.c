
#include <stdio.h>

typedef struct 
{
    char    UserName[10];
    char    UserID;
    char    Age;
}PERSONAL_INFO;


int main(void)
{
    PERSONAL_INFO   PersonnelA;
    PERSONAL_INFO   PersonnelB[2];
    PERSONAL_INFO   * MyRecord;
    char * Pointer;

    sprintf(PersonnelA.UserName,"%s","Jackson");
    PersonnelA.UserID = 10;
    PersonnelA.Age = 40;

    sprintf(PersonnelB[0].UserName,"%s","David");
    PersonnelB[0].UserID = 11;
    PersonnelB[0].Age = 35;

    sprintf(PersonnelB[1].UserName,"%s","Smith");
    PersonnelB[1].UserID = 12;
    PersonnelB[1].Age = 28;

    Pointer = (char *) &PersonnelA;
    printf("Ans 1=%x\n", *(Pointer+10));

    Pointer = (char *) &PersonnelB[1];
    printf("Ans 2=%s\n", &Pointer[1]);

    MyRecord = PersonnelB;
    MyRecord++;
    printf("Ans 3=%d\n", MyRecord->Age);


    return 0;
    // printf("Hello World!! \n");
}