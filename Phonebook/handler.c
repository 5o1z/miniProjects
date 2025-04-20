#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#include "phonebook.h"

// Function to handle adding a contact
void handleAddContact()
{
    char tempName[NAME_LENGTH];
    char tempPhone[PHONE_LENGTH];

    if (index >= MAX_CONTACTS)
    {
        printf("Contact list is full.\n");
        return;
    }

    printf("Enter name: ");
    fgets(tempName, NAME_LENGTH, stdin);
    tempName[strcspn(tempName, "\n")] = 0;

    printf("Enter phone number: ");
    fgets(tempPhone, PHONE_LENGTH, stdin);
    tempPhone[strcspn(tempPhone, "\n")] = 0;

    notes[index] = (Contact *)malloc(sizeof(Contact));
    if (!notes[index])
    {
        printf("Memory allocation failed.\n");
        return;
    }

    addContact(notes[index], tempName, tempPhone);
    printf("Contact number %d added.\n", index + 1);
    index++;
}

// Function to handle deleting a contact
void handleDeleteContact()
{
    printf("Enter the index of the contact to delete: ");
    uint8_t deleteIndex;
    read_int(&deleteIndex);
    deleteIndex--;

    deleteContact(notes, deleteIndex, &index);
    return;
}

// Function to handle exiting the program
void handleExit()
{
    for (uint8_t i = 0; i < index; i++)
    {
        free(notes[i]);
        notes[i] = NULL; // Avoid dangling pointers
    }
    printf("Exiting...\n");
    exit(0);
}

// Handler for display all contacts
void handleDisplayContacts()
{
    if (index == 0)
    {
        printf("No contacts to display.\n");
        return;
    }

    printf("\n=== CONTACT LIST ===\n\n");
    printf("+-----+ %-*s | %-*s +\n", NAME_LENGTH - 1, "Name", PHONE_LENGTH - 1, "Phone");
    printf("+-----+-%.*s-+-%.*s-+\n", NAME_LENGTH - 1, "--------------------------------------------------", PHONE_LENGTH - 1, "---------------");

    for (uint8_t i = 0; i < index; i++)
    {
        printf("| %3d | %-*s | %-*s |\n",
               i + 1,
               NAME_LENGTH - 1, notes[i]->name,
               PHONE_LENGTH - 1, notes[i]->phone);
    }

    printf("+-----+-%.*s-+-%.*s-+\n", NAME_LENGTH - 1, "--------------------------------------------------", PHONE_LENGTH - 1, "---------------");
}
