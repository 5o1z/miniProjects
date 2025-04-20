#ifndef PHONEBOOK_H
#define PHONEBOOK_H

#include <stdint.h>

#define MAX_CONTACTS 100
#define NAME_LENGTH 50
#define PHONE_LENGTH 15

typedef struct
{
    char name[NAME_LENGTH];
    char phone[PHONE_LENGTH];
} Contact;

extern uint8_t index;
extern uint8_t choice;
extern Contact *notes[MAX_CONTACTS];

// Handlers
void handleAddContact();
void handleDeleteContact();
void handleDisplayContacts();
void handleExit();

// Utils
void read_input(char *buffer, size_t size);
int read_int(uint8_t *value);
void addContact(Contact *contact, const char *name, const char *phone);
void deleteContact(Contact *notes[], uint8_t indexToDelete, uint8_t *currentCount);

#endif
