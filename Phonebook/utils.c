#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#include "phonebook.h"

// Function to read input from stdin
void read_input(char *buffer, size_t size)
{
    ssize_t len = read(STDIN_FILENO, buffer, size - 1);
    if (len < 0)
    {
        perror("Error reading input");
        exit(EXIT_FAILURE);
    }

    buffer[len] = '\0';

    size_t i = 0;
    while (buffer[i] != '\0')
    {
        if (buffer[i] == '\n')
        {
            buffer[i] = '\0';
            break;
        }
        i++;
    }
}

// Function to read an integer from stdin
int read_int(uint8_t *value)
{
    char buffer[10];
    read_input(buffer, sizeof(buffer));

    *value = (uint8_t)atoi(buffer);
    return 0;
}

// Function to add a contact
// This function copies the name and phone number into the contact structure
void addContact(Contact *contact, const char *name, const char *phone)
{
    strncpy(contact->name, name, NAME_LENGTH - 1);
    strncpy(contact->phone, phone, PHONE_LENGTH - 1);
}

// Function to delete a contact from the list
void deleteContact(Contact *notes[], uint8_t indexToDelete, uint8_t *currentCount)
{
    if (indexToDelete >= *currentCount)
    {
        printf("Invalid contact index.\n");
        return;
    }

    free(notes[indexToDelete]);

    // Shift remaining contacts to fill the gap
    for (uint8_t i = indexToDelete; i < (*currentCount) - 1; i++)
    {
        notes[i] = notes[i + 1];
    }

    // Set the last pointer to NULL
    notes[*currentCount - 1] = NULL;

    // Decrease the count
    (*currentCount)--;

    printf("Contact deleted successfully.\n");
}

void searchContact(Contact *notes[], const char *name, uint8_t currentCount)
{
    for (uint8_t i = 0; i < currentCount; i++)
    {
        if (strcmp(notes[i]->name, name) == 0)
        {
            printf("Contact found: %s - %s\n", notes[i]->name, notes[i]->phone);
            return;
        }
    }
    printf("Contact not found.\n");
}
