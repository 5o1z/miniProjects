#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "phonebook.h"

uint8_t index, choice;
char username[NAME_LENGTH];
Contact *notes[MAX_CONTACTS];

void menu()
{
    printf("\n");
    printf("╔══════════════════════════════════════╗\n");
    printf("║            PHONEBOOK MENU            ║\n");
    printf("╠══════════════════════════════════════╣\n");
    printf("║ 1. Add contact                       ║\n");
    printf("║ 2. Search contact                    ║\n");
    printf("║ 3. Delete contact                    ║\n");
    printf("║ 4. Edit contact                      ║\n");
    printf("║ 5. Display all contacts              ║\n");
    printf("║ 6. Exit                              ║\n");
    printf("╚══════════════════════════════════════╝\n");
    printf("Choose an option (1-6): ");
}

void setup()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int main()
{
    setup();

    printf("Welcome to the Phonebook!\n");
    printf("Please enter your name: ");
    read_input(username, sizeof(username));
    printf("Hello, %s! You can now manage your contacts.\n", username);

    while (1)
    {
        menu();
        read_int(&choice);

        switch (choice)
        {
        case 1:
            handleAddContact();
            break;
        case 2:
            // TODO
            break;
        case 3:
            handleDeleteContact();
            break;
        case 4:
            // TODO
            break;
        case 5:
            handleDisplayContacts();
            break;
        case 6:
            handleExit();
            break;
        default:
            printf("Invalid choice.\n");
            break;
        }
    }

    return 0;
}
