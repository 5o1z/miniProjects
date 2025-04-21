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

// Handler for searching a contact
void handleSearchContact()
{
    char searchName[NAME_LENGTH];
    printf("Enter the name of the contact to search: ");
    fgets(searchName, NAME_LENGTH, stdin);
    searchName[strcspn(searchName, "\n")] = 0;

    searchContact(notes, searchName, index);
    return;
}

void handleEditContact()
{
    printf("All current contacts:\n");
    handleDisplayContacts();

    printf("Enter the index of the contact to edit: ");
    uint8_t editIndex;
    read_int(&editIndex);
    editIndex--; // Convert to 0-based index

    if (editIndex >= index)
    {
        printf("Invalid contact index.\n");
        return;
    }

    char newName[NAME_LENGTH];
    char newPhone[PHONE_LENGTH];

    printf("Enter new name: ");
    fgets(newName, NAME_LENGTH, stdin);
    newName[strcspn(newName, "\n")] = 0;

    printf("Enter new phone number: ");
    fgets(newPhone, PHONE_LENGTH, stdin);
    newPhone[strcspn(newPhone, "\n")] = 0;

    addContact(notes[editIndex], newName, newPhone);
}
