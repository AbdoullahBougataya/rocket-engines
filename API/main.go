package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
)

type Record struct {
    Id    int    `json:"id"`
    Engine  string `json:"engine"`
    Origin string `json:"origin"`
}

func main() {
    db, err := sql.Open("sqlite3", "./your-database.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    rows, err := db.Query("SELECT id, name, email FROM your_table")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    var records []Record

    for rows.Next() {
        var record Record
        err := rows.Scan(&record.ID, &record.Name, &record.Email)
        if err != nil {
            log.Fatal(err)
        }
        records = append(records, record)
    }

    if err = rows.Err(); err != nil {
        log.Fatal(err)
    }
}

unsigned int hash(const char *word)
{
    int len = 0;
    while (word[len] != 0)
    {
        len++;
    }
    if (len <= LENGTH + 1)
    {
        if (len == 1)
        {
            return toupper(word[0]) - 'A';
        }
        else if (word[1] != 39)
        {
            // toupper(word[0]) toupper(word[1]) len
            return 24 + (toupper(word[0]) - 'A') + (toupper(word[1]) - 'A') * 26 + len;
        }
        return 24 + (toupper(word[0]) - 'A') + (toupper(word[2]) - 'A') * 26 + len;
    }
    return 0;
}
